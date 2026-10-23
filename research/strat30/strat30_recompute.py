#!/usr/bin/env python3
"""strat30_recompute.py - AUDIT v2 of the 30-day crypto strategy screen.

Audit fixes over v1 (RESULTS.md v1, superseded):
1. TRUNCATION AT REQUEST TIME: request received 2026-10-23T21:27Z. The MEXC
   daily candle opened 2026-10-23 00:00Z was INCOMPLETE at request time and is
   excluded. Last valid completed close = candle opened 2026-10-22 00:00Z.
   Test grid: UTC daily closes 2026-09-24 .. 2026-10-22 (29 closes).
2. STABLECOIN EXCLUSION: DESIGN specified a NON-stablecoin basket. v1 let
   usd1-wlfi through (picked Oct 8). All pegged/RWA instruments now excluded.
3. EXECUTION TIMING: signals computed from closes up to and including day t.
   - 'next' (primary): trade at close of day t+1 (next bar); no same-close fills.
   - 'same' (idealized, reported for comparison): trade at close t.
4. M2/M3/M4 all recomputed on the corrected grid under both conventions.
Data: per-coin JSON files (source: MEXC public klines GET
https://api.mexc.com/api/v3/klines?symbol={SYM}USDT&interval=1d&limit=40),
prices rows = [open_time_ms, close]. QNT cross-verified vs CoinGecko
GET https://api.coingecko.com/api/v3/coins/quant-network/market_chart?vs_currency=usd&days=31&interval=daily
"""
import json, os, datetime, glob

HERE = os.path.dirname(os.path.abspath(__file__))
STABLE_RWA = {'blackrock-usd-institutional-digital-liquidity-digital-fund',
 'blackrock-usd-institutional-digital-liquidity-fund','global-dollar','hashnote-usyc',
 'ondo-us-dollar-yield','pax-gold','ripple-usd','spiko-amundi-overnight-swap-fund-eur',
 'tether-gold','usd1-wlfi'}
GRID_FIRST = datetime.date(2026,9,24)   # first test close
GRID_LAST  = datetime.date(2026,10,22)  # last completed close at request time
COST = 0.001  # 0.1% per position change (frozen in DESIGN)

def load(cid):
    p = os.path.join(HERE, cid + '.json')
    if not os.path.exists(p): return None
    d = json.load(open(p))
    rows = [(datetime.datetime.utcfromtimestamp(r[0]/1000).date(), float(r[1])) for r in d['prices']]
    rows.sort()
    return rows

basket = json.load(open(os.path.join(HERE,'basket.json')))
assets = [c for c in basket if c not in STABLE_RWA]
series = {}
skipped = []
for c in assets:
    s = load(c)
    if not s or len(s) < 12:
        skipped.append(c); continue
    series[c] = dict(s)

def closes(cid):
    return series[cid]

def grid_dates(cid):
    return sorted(d for d in series[cid] if GRID_FIRST <= d <= GRID_LAST)

def ret(cid, d0, d1):
    s = series[cid]
    if d0 not in s or d1 not in s: return None
    return s[d1]/s[d0] - 1

# ---------- M1 buy & hold majors ----------
m1 = {}
for m in ['bitcoin','ethereum','solana']:
    g = grid_dates(m)
    m1[m] = round(ret(m, g[0], g[-1])*100, 2)

# ---------- M2 trend filter (7d SMA), both execution conventions ----------
def sma7(vals, i):
    if i < 6: return None
    return sum(vals[i-6:i+1])/7.0

def trend(cid, exec_mode):
    s = series[cid]; dates = sorted(s); vals = [s[d] for d in dates]
    gi = [i for i,d in enumerate(dates) if GRID_FIRST <= d <= GRID_LAST]
    if not gi: return None
    pos = 1.0; cash_mult = 1.0; switches = 0
    # same-close: at day t, signal from close t, position applies to return t->t+1
    # next-close: signal from close t, trade at close t+1 -> position for t+1->t+2
    pending = None
    for k in range(gi[0], gi[-1]):
        i = k  # return day: dates[k] -> dates[k+1]
        sig_now = None
        sm = sma7(vals, k)
        if sm is not None:
            sig_now = 1.0 if vals[k] > sm else 0.0
        if exec_mode == 'same' and sig_now is not None and sig_now != pos:
            pos = sig_now; switches += 1; cash_mult *= (1-COST)
        if exec_mode == 'next' and pending is not None and pending != pos:
            pos = pending; switches += 1; cash_mult *= (1-COST)
            pending = None
        r = vals[k+1]/vals[k] - 1
        cash_mult *= (1 + pos*r)
        if exec_mode == 'next' and sig_now is not None and sig_now != pos:
            pending = sig_now
    return round((cash_mult-1)*100, 2), switches

m2 = {}
for m in ['bitcoin','ethereum','solana']:
    m2[m] = {'next': trend(m,'next'), 'same': trend(m,'same')}

# ---------- M3 weekly top-3 cross-sectional momentum ----------
def trailing7(cid, d):
    s = series[cid]
    d0 = d - datetime.timedelta(days=7)
    if d0 not in s or d not in s: return None
    return s[d]/s[d0] - 1

def momentum(exec_mode, exclude=None, restrict=None, topn=3):
    exclude = exclude or set()
    cands = [c for c in series if c not in exclude and (restrict is None or c in restrict)]
    rebs = [GRID_FIRST + datetime.timedelta(days=7*i) for i in range(5)]
    mult = 1.0; picks_log = []
    for t in rebs:
        exec_date = t if exec_mode=='same' else t + datetime.timedelta(days=1)
        # next rebalance exec date
        idx = rebs.index(t)
        nxt = rebs[idx+1] if idx+1 < len(rebs) else None
        hold_end = (nxt if exec_mode=='same' else (nxt + datetime.timedelta(days=1) if nxt else None))
        ranked = sorted(((trailing7(c,t), c) for c in cands if trailing7(c,t) is not None), reverse=True)
        picks = [c for _,c in ranked[:topn]]
        picks_log.append((str(t), str(exec_date), picks))
        if exec_date > GRID_LAST: 
            picks_log[-1] = picks_log[-1] + ('UNEXECUTABLE-after-grid-end',)
            continue
        seg = []
        for c in picks:
            end = hold_end if hold_end and hold_end <= GRID_LAST else GRID_LAST
            r = ret(c, exec_date, end)
            if r is not None: seg.append(r)
        if seg:
            mult *= (1 + sum(seg)/len(seg)) * (1-COST)**topn
    return round((mult-1)*100, 2), picks_log

def ew_baseline(exec_mode):
    cands = list(series)
    rebs = [GRID_FIRST + datetime.timedelta(days=7*i) for i in range(5)]
    mult = 1.0
    for idx,t in enumerate(rebs):
        exec_date = t if exec_mode=='same' else t + datetime.timedelta(days=1)
        if exec_date > GRID_LAST: continue
        nxt = rebs[idx+1] if idx+1 < len(rebs) else None
        hold_end = nxt if exec_mode=='same' else (nxt + datetime.timedelta(days=1) if nxt else None)
        end = hold_end if hold_end and hold_end <= GRID_LAST else GRID_LAST
        rs = [ret(c, exec_date, end) for c in cands]
        rs = [r for r in rs if r is not None]
        if rs: mult *= (1 + sum(rs)/len(rs)) * (1-COST)
    return round((mult-1)*100, 2)

m3 = {
 'next': momentum('next'),
 'same': momentum('same'),
 'ew_next': ew_baseline('next'),
 'ew_same': ew_baseline('same'),
 'next_exQNT': momentum('next', exclude={'quant-network'}),
 'same_exQNT': momentum('same', exclude={'quant-network'}),
}
liquid20 = ['bitcoin','ethereum','ripple','solana','binancecoin','dogecoin','cardano','tron','hyperliquid','bitcoin-cash','chainlink','stellar','litecoin','the-open-network','avalanche-2','shiba-inu','polkadot','uniswap','near','monero']
m3['next_liquid20'] = momentum('next', restrict=[c for c in liquid20 if c in series])
m3['same_liquid20'] = momentum('same', restrict=[c for c in liquid20 if c in series])

# ---------- M4 dip-buy majors ----------
def dipbuy(cid):
    s = series[cid]; dates = sorted(d for d in s if GRID_FIRST <= d <= GRID_LAST)
    vals = [s[d] for d in dates]
    sigs = 0
    for i,d in enumerate(dates):
        hist = [s[x] for x in dates[max(0,i-7):i+1]]
        if len(hist) < 7: continue
        if vals[i] <= max(hist)*0.90: sigs += 1
    return sigs
m4 = {m: dipbuy(m) for m in ['bitcoin','ethereum','solana']}

out = {
 'grid': [str(GRID_FIRST), str(GRID_LAST)],
 'n_assets_tested': len(series), 'skipped_no_series': skipped,
 'stable_rwa_excluded': sorted(STABLE_RWA),
 'M1_buyhold_pct': m1, 'M2_trend_pct_(ret,switches)': m2,
 'M3_momentum_pct': m3, 'M4_dipbuy_signals': m4,
}
json.dump(out, open(os.path.join(HERE,'strat30_v2_results.json'),'w'), indent=1)
print(json.dumps(out, indent=1))
