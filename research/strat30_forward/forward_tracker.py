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
    uni = universe()
    data = {}
    for cid, sym in uni:
        try:
            rows = completed_closes(series_mexc(sym, 10))
            if len(rows) >= 8:
                data[(cid, sym)] = rows
        except Exception:
            pass
        time.sleep(1.2)
    if not data:
        print('NO DATA'); return
    last_close = max(r[-1][0] for r in data.values())

    # 1. EXECUTE pending signal at this close (NEXT-BAR: signal close t -> execute close t+1)
    ps = st.get('pending_signal')
    if ps and last_close > datetime.date.fromisoformat(ps['signal_date']):
        prev_n = len(st['positions'])
        positions = []
        for pick in ps['picks']:
            rows = data.get((pick['cid'], pick['sym']))
            if rows and rows[-1][0] == last_close:
                positions.append({'cid': pick['cid'], 'sym': pick['sym'],
                                  'entry_px': rows[-1][1], 'entry_date': str(last_close),
                                  'last_px': rows[-1][1], 'ret_since_entry': 0.0})
        if positions:
            changes = max(len(positions), prev_n)
            st['cash_mult'] *= (1 - COST) ** changes
            st['positions'] = positions
            st['rebalances'].append({'signal_date': ps['signal_date'],
                'exec_date': str(last_close),
                'picks': [{'sym': p['sym'], 'entry_px': p['entry_px']} for p in positions],
                'universe_n': ps.get('universe_n')})
            if st['started_utc'] is None:
                st['started_utc'] = str(last_close)
            st['last_rebal_date'] = str(last_close)
            print('EXECUTED next-bar at', last_close, [(p['sym'], p['entry_px']) for p in positions])
        else:
            print('PENDING SIGNAL UNEXECUTABLE (no price rows at close); kept pending')
        st['pending_signal'] = None

    # 2. daily mark of open positions
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
            print('MARK', last_close, [(p['sym'], round(p['ret_since_entry'],3)) for p in st['positions']])

    # 3. NEW SIGNAL every 7 days (computed at this close; executes at the NEXT close)
    last_sig = st.get('last_signal_date')
    if last_sig is None or (last_close - datetime.date.fromisoformat(last_sig)).days >= REBAL_DAYS:
        ranked = []
        for (cid, sym), rows in data.items():
            if rows[-1][0] == last_close and len(rows) >= 8:
                ranked.append((rows[-1][1]/rows[-8][1] - 1, cid, sym))
        ranked.sort(reverse=True)
        picks = [{'cid': c, 'sym': s, 'r7': round(r, 4)} for r, c, s in ranked[:3]]
        st['pending_signal'] = {'signal_date': str(last_close), 'picks': picks,
                                'universe_n': len(ranked),
                                'note': 'next-bar: executes at the next completed UTC close'}
        st['last_signal_date'] = str(last_close)
        print('SIGNAL', last_close, picks, 'n_uni', len(ranked))

    if st['positions']:
        avg = sum(p['ret_since_entry'] for p in st['positions'])/len(st['positions'])
        print('OPEN-RET avg %.3f cash_mult %.4f n_rebal %d' % (avg, st['cash_mult'], len(st['rebalances'])))
    save(st)

if __name__ == '__main__':
    main()
