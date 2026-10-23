#!/usr/bin/env python3
"""strat30_fetch.py - fetch daily close series for the 30-day strategy screen.
Public endpoints only, no keys. Writes one JSON per asset: {"source": "mexc", "prices": [[open_time_ms, close], ...]}
Usage: python3 strat30_fetch.py
Endpoints:
  basket:  GET https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1
  series:  GET https://api.mexc.com/api/v3/klines?symbol={SYM}USDT&interval=1d&limit=40
  x-check: GET https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency=usd&days=31&interval=daily
Note: MEXC symbol mapping uses the CoinGecko 'symbol' field uppercased + 'USDT';
mismatches are documented in mexc_info.json, not silently filled.
CoinGecko free tier rate-limits hard (~429s); space calls >= 15-20s.
"""
import json, time, urllib.request, os

HERE = os.path.dirname(os.path.abspath(__file__))

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'research/1.0'})
    return json.load(urllib.request.urlopen(req, timeout=30))

def main():
    markets = get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1')
    basket = [c['id'] for c in markets]
    json.dump(basket, open(os.path.join(HERE, 'basket.json'), 'w'))
    symbols = {c['id']: c['symbol'].upper() for c in markets}
    json.dump(symbols, open(os.path.join(HERE, 'symbols.json'), 'w'))
    info = {}
    for cid in basket:
        sym = symbols[cid] + 'USDT'
        try:
            k = get(f'https://api.mexc.com/api/v3/klines?symbol={sym}&interval=1d&limit=40')
            prices = [[row[0], float(row[4])] for row in k]
            json.dump({'source': 'mexc', 'symbol': sym, 'prices': prices},
                      open(os.path.join(HERE, cid + '.json'), 'w'))
            info[cid] = {'symbol': sym, 'rows': len(prices)}
        except Exception as e:
            info[cid] = {'symbol': sym, 'error': str(e)}
        time.sleep(1.5)
    json.dump(info, open(os.path.join(HERE, 'mexc_info.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
