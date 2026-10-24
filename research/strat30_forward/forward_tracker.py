#!/usr/bin/env python3
"""forward_tracker.py - forward paper tracking of the audited weekly top-3 momentum rule.
FROZEN design: FORWARD_DESIGN.md (2026-10-24). Paper only. Run daily after UTC close."""
import json, os, time, datetime, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, 'state.json')
COST = 0.001
REBAL_DAYS = 7
PEGGED_RWA_HINTS = ('usd','usdt','usdc','dai','fdusd','pyusd','usde','usdf','usd1','usyc','buidl',
 'gold','paxg','xaut','eurc','ageur','ousg','ustb','bento','global-dollar','heloc','spiko',
 'hashnote','ondo-us-dollar-yield','blackrock','tether-gold','pax-gold','ripple-usd','usdd','usds','susd')

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'research/1.0'})
    return json.load(urllib.request.urlopen(req, timeout=30))

def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {'started_utc': None, 'positions': [], 'cash_mult': 1.0, 'marks': [],
            'rebalances': [], 'last_rebal_date': None, 'last_mark_date': None}

def save(st): json.dump(st, open(STATE, 'w'), indent=1)

def universe():
    mk = get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1')
    out = []
    for c in mk:
        cid, sym = c['id'], c['symbol'].upper()
        if any(h in cid for h in PEGGED_RWA_HINTS) or any(h in sym.lower() for h in PEGGED_RWA_HINTS):
            continue
        out.append((cid, sym))
    return out

def series_mexc(sym, limit=10):
    k = get(f'https://api.mexc.com/api/v3/klines?symbol={sym}USDT&interval=1d&limit={limit}')
    return [(datetime.datetime.utcfromtimestamp(r[0]/1000).date(), float(r[4])) for r in k]

def completed_closes(rows):
    """Drop today's (incomplete) candle; keep only completed UTC daily closes."""
    today = datetime.datetime.utcnow().date()
    return [(d, c) for d, c in rows if d < today]

def main():
    st = load_state()
    now = datetime.datetime.utcnow()
    uni = universe()
    data = {}
    for cid, sym in uni:
        try:
            rows = completed_closes(series_mexc(sym, 10))
            if len(rows) >= 8:
                data[(cid, sym)] = rows
        except Exception as e:
            pass
        time.sleep(1.2)
    if not data:
        print('NO DATA'); return
    last_close = max(r[-1][0] for r in data.values())
    # daily mark
    if st['positions'] and st.get('last_mark_date') != str(last_close):
        seg = []
        for p in st['positions']:
            rows = data.get((p['cid'], p['sym']))
            if rows and rows[-1][0] == last_close:
                p['last_px'] = rows[-1][1]
                p['ret_since_entry'] = p['last_px']/p['entry_px'] - 1
                seg.append(p['ret_since_entry'])
        if seg:
            st['marks'].append({'date': str(last_close), 'avg_open_ret': sum(seg)/len(seg)})
            st['last_mark_date'] = str(last_close)
    # weekly rebalance
    due = (st['last_rebal_date'] is None or
           (last_close - datetime.date.fromisoformat(st['last_rebal_date'])).days >= REBAL_DAYS)
    if due:
        ranked = []
        for (cid, sym), rows in data.items():
            if rows[-1][0] == last_close and len(rows) >= 8:
                r7 = rows[-1][1]/rows[-8][1] - 1
                ranked.append((r7, cid, sym, rows[-1][1]))
        ranked.sort(reverse=True)
        picks = ranked[:3]
        changes = max(len(picks), len(st['positions']))
        st['cash_mult'] *= (1 - COST) ** changes
        st['positions'] = [{'cid': cid, 'sym': sym, 'entry_px': px, 'entry_date': str(last_close),
                            'last_px': px, 'ret_since_entry': 0.0} for r7, cid, sym, px in picks]
        st['rebalances'].append({'date': str(last_close),
                                 'picks': [{'sym': s, 'r7': round(r, 4)} for r, c, s, p in picks],
                                 'universe_n': len(ranked)})
        st['last_rebal_date'] = str(last_close)
        if st['started_utc'] is None:
            st['started_utc'] = str(last_close)
        print('REBALANCE', last_close, [(s, round(r,3)) for r,c,s,p in picks], 'n_uni', len(ranked))
    else:
        print('MARK only', last_close, [ (p['sym'], round(p['ret_since_entry'],3)) for p in st['positions'] ])
    # forward performance since tracking start (equal-weight open positions vs entry, cost-adjusted)
    if st['positions']:
        avg = sum(p['ret_since_entry'] for p in st['positions'])/len(st['positions'])
        print('OPEN-RET avg %.3f cash_mult %.4f n_rebal %d' % (avg, st['cash_mult'], len(st['rebalances'])))
    save(st)

if __name__ == '__main__':
    main()
