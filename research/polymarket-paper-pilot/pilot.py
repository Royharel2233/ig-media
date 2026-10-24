#!/usr/bin/env python3
"""
Polymarket paper-trading pilot. NO REAL MONEY. Read-only public data.
Deterministic tape-reconstruction sim: every decision uses only data that was
publicly available at the decision timestamp, so state is replayable from genesis.

Strategies (paper):
  A: maker near-certain buying on crypto 5m/15m up/down markets.
     At T-lag before close, if last tape trade of an outcome >= min_px, we "rest a bid"
     at a proxy price. Fill (strict) = later trade prints strictly below our bid.
  B: taker spot-lag. At T-30s, if Coinbase TWAP-to-date in window deviates from
     window-start price by >= threshold, "market buy" the direction at an ask proxy.
Fees: maker 0. Taker fee = shares * 0.07 * p * (1-p) (Polymarket docs, crypto).
Rebate (estimate only, reported separately): 20% of tape taker fees on the market,
pro-rata by our notional / market volume.
"""
import json, os, sys, time, urllib.request, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(BASE, "ledger.jsonl")
STATE = os.path.join(BASE, "state.json")
UA = {"User-Agent": "paper-pilot/1.0"}
ASSETS = {"btc": "BTC-USD", "eth": "ETH-USD", "sol": "SOL-USD", "xrp": "XRP-USD"}
SERIES = {"5m": 300, "15m": 900}
CLIP_USD = 15.0
BANKROLL = 1000.0
MAX_OPEN_EXPOSURE = 250.0
DAILY_STOP = -50.0
FEE_RATE = 0.07  # crypto taker

def get(url, timeout=25, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(1.5 * (i + 1))

def iso(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%SZ")

def fetch_market(slug):
    ev = get(f"https://gamma-api.polymarket.com/events?slug={slug}")
    if not ev:
        return None
    ms = ev[0].get("markets") or []
    return ms[0] if ms else None

def fetch_trades(cid):
    out, off = [], 0
    while True:
        d = get(f"https://data-api.polymarket.com/trades?market={cid}&limit=10000&offset={off}", timeout=40)
        if not d:
            break
        out.extend(d)
        if len(d) < 10000 or off >= 10000:
            break
        off += 10000
    out.sort(key=lambda t: t["timestamp"])
    return out

def fetch_candles(product, start_ts, end_ts):
    # Coinbase 1m candles, max 300/call -> chunk 4h
    candles = {}
    t = start_ts
    while t < end_ts:
        e = min(t + 300 * 60, end_ts)
        d = get(f"https://api.exchange.coinbase.com/products/{product}/candles?granularity=60&start={iso(t)}&end={iso(e)}")
        for c in d:  # [time, low, high, open, close, volume], time = candle start
            candles[c[0]] = {"low": c[1], "high": c[2], "open": c[3], "close": c[4]}
        t = e
    return candles

def r2(p):  # floor to cent tick
    return int(p * 100) / 100.0

def evaluate_market(m, trades, candles, now):
    """Return list of ledger rows for one market."""
    slug = m["slug"]
    asset = slug.split("-")[0]
    series = "5m" if "-5m-" in slug else "15m"
    wstart = int(slug.rsplit("-", 1)[1])
    dur = SERIES[series]
    wend = wstart + dur
    outcomes = json.loads(m["outcomes"])           # ["Up","Down"]
    token_ids = json.loads(m["clobTokenIds"])
    prices = [float(x) for x in json.loads(m["outcomePrices"])]
    closed = bool(m.get("closed"))
    rows = []
    # winner (only when settleable)
    winner = None
    provisional = False
    if closed and max(prices) >= 0.99:
        winner = prices.index(max(prices))
    elif now > wend + 1200 and max(prices) >= 0.995:
        winner, provisional = prices.index(max(prices)), True
    total_vol = sum(t["size"] * t["price"] for t in trades)
    tape_fee_pool = sum(t["size"] * FEE_RATE * t["price"] * (1 - t["price"]) for t in trades)

    def settle_fields(status_fill):
        if winner is None:
            return {"status": status_fill, "pnl": None, "winner": None}
        return {"winner": outcomes[winner]}

    # ---------- Strategy A: maker near-certain bid ----------
    for lag, vmin, vname in [(90, 0.95, "A90"), (45, 0.95, "A45"), (90, 0.90, "A90d")]:
        dec = wend - lag
        pre = [t for t in trades if t["timestamp"] < dec]
        if not pre or dec - pre[-1]["timestamp"] > 60:
            rows.append({"strategy": "A", "variant": vname, "slug": slug, "asset": asset,
                         "series": series, "window_start": wstart, "end": wend,
                         "status": "skipped_stale"})
            continue
        L = pre[-1]
        lp = L["price"]
        if lp < vmin or lp > 0.995:
            rows.append({"strategy": "A", "variant": vname, "slug": slug, "asset": asset,
                         "series": series, "window_start": wstart, "end": wend,
                         "status": "skipped_price", "ref_px": lp})
            continue
        bid = r2(lp) if L["side"] == "SELL" else r2(lp - 0.01)
        bid = min(0.99, max(0.90, bid))
        shares = CLIP_USD / bid
        token = L["asset"]
        side_idx = 0 if token == token_ids[0] else 1
        strict = [t for t in trades if dec <= t["timestamp"] <= wend and t["asset"] == token and t["price"] < bid - 1e-9]
        touch = [t for t in trades if dec <= t["timestamp"] <= wend and t["asset"] == token and t["side"] == "SELL" and t["price"] <= bid + 1e-9]
        base = {"strategy": "A", "variant": vname, "slug": slug, "asset": asset, "series": series,
                "window_start": wstart, "end": wend, "decision_ts": dec, "side": outcomes[side_idx],
                "token_id": token, "ref_trade_ts": L["timestamp"], "ref_px": lp, "ref_side": L["side"],
                "px": bid, "shares": round(shares, 4), "notional": CLIP_USD, "fee": 0.0,
                "fill_touch": bool(touch),
                "rebate_est": round(0.20 * tape_fee_pool * (CLIP_USD / total_vol), 6) if total_vol else 0.0}
        if not strict:
            rows.append({**base, "status": "unfilled", "winner": outcomes[winner] if winner is not None else None})
            continue
        row = {**base, "fill": "strict", "fill_ts": strict[0]["timestamp"], "provisional": provisional}
        if winner is None:
            row["status"] = "open"
        else:
            win = side_idx == winner
            row["status"] = "win" if win else "loss"
            row["pnl"] = round(shares * (1 - bid), 4) if win else round(-CLIP_USD, 4)
            row["winner"] = outcomes[winner]
        rows.append(row)

    # ---------- Strategy B: taker spot-lag ----------
    dec = wend - 30
    # spot signal: window-start open + TWAP-to-date of complete candles
    c0 = candles.get(wstart)
    comp = [candles[t]["close"] for t in sorted(candles) if wstart <= t and t + 60 <= dec]
    if c0 is None or not comp:
        rows.append({"strategy": "B", "slug": slug, "asset": asset, "series": series,
                     "window_start": wstart, "end": wend, "status": "skipped_nospot"})
    else:
        start_px = c0["open"]
        twap = sum(comp) / len(comp)
        move = (twap - start_px) / start_px
        for thr, vname in [(0.0005, "B05"), (0.0002, "B02"), (0.0010, "B10")]:
            if abs(move) < thr:
                rows.append({"strategy": "B", "variant": vname, "slug": slug, "asset": asset,
                             "series": series, "window_start": wstart, "end": wend,
                             "status": "skipped_nosignal", "spot_move": round(move, 6)})
                continue
            dir_idx = 0 if move > 0 else 1
            token = token_ids[dir_idx]
            pre = [t for t in trades if t["timestamp"] < dec and t["asset"] == token]
            if not pre or dec - pre[-1]["timestamp"] > 45:
                rows.append({"strategy": "B", "variant": vname, "slug": slug, "asset": asset,
                             "series": series, "window_start": wstart, "end": wend,
                             "status": "skipped_stale", "spot_move": round(move, 6)})
                continue
            L = pre[-1]
            ap = L["price"] if L["side"] == "BUY" else L["price"] + 0.01
            ap = min(ap, 0.99)
            if ap > 0.97 or ap < 0.50:
                rows.append({"strategy": "B", "variant": vname, "slug": slug, "asset": asset,
                             "series": series, "window_start": wstart, "end": wend,
                             "status": "skipped_price", "spot_move": round(move, 6), "ask_proxy": round(ap, 4)})
                continue
            shares = CLIP_USD / ap
            fee = shares * FEE_RATE * ap * (1 - ap)
            base = {"strategy": "B", "variant": vname, "slug": slug, "asset": asset, "series": series,
                    "window_start": wstart, "end": wend, "decision_ts": dec, "side": outcomes[dir_idx],
                    "token_id": token, "ref_trade_ts": L["timestamp"], "ref_px": L["price"],
                    "ref_side": L["side"], "px": round(ap, 4), "shares": round(shares, 4),
                    "notional": CLIP_USD, "fee": round(fee, 4), "spot_move": round(move, 6),
                    "start_px": start_px, "twap_to_date": round(twap, 2), "provisional": provisional}
            if winner is None:
                base["status"] = "open"
            else:
                win = dir_idx == winner
                base["status"] = "win" if win else "loss"
                base["pnl"] = round(shares - CLIP_USD - fee, 4) if win else round(-CLIP_USD - fee, 4)
                base["winner"] = outcomes[winner]
            rows.append(base)
    return rows

def load_ledger_keys():
    keys = set()
    if os.path.exists(LEDGER):
        with open(LEDGER) as f:
            for line in f:
                try:
                    r = json.loads(line)
                    keys.add((r.get("strategy"), r.get("variant"), r.get("slug"), r.get("status") in ("open",)))
                except Exception:
                    pass
    return keys

def main():
    now = int(time.time())
    state = {"genesis": None, "cursors": {}, "start_ts": now}
    if os.path.exists(STATE):
        state = json.load(open(STATE))
    genesis = state.get("genesis")
    if "--genesis" in sys.argv:
        genesis = int(sys.argv[sys.argv.index("--genesis") + 1])
        state["genesis"] = genesis
        state["cursors"] = {}
    if genesis is None:
        print("need genesis"); sys.exit(1)
    process_until = now - 120
    if "--until" in sys.argv:
        process_until = min(process_until, int(sys.argv[sys.argv.index("--until") + 1]))
    # fetch candles once per asset covering the whole processing span
    earliest = min((state["cursors"].get(s, genesis) for s in SERIES), default=genesis)
    candle_cache = {}
    for asset, product in ASSETS.items():
        try:
            candle_cache[asset] = fetch_candles(product, earliest - 900, process_until + 300)
        except Exception as e:
            print(f"ERR candles {asset}: {e}")
            candle_cache[asset] = {}
    new_rows, n_markets = [], 0
    for series, dur in SERIES.items():
        cur = (state["cursors"].get(series, genesis) // dur) * dur
        w = cur
        while w + dur <= process_until:
            for asset in ASSETS:
                slug = f"{asset}-updown-{series}-{w}"
                try:
                    m = fetch_market(slug)
                except Exception as e:
                    print(f"ERR market {slug}: {e}")
                    continue
                if not m:
                    continue
                n_markets += 1
                try:
                    trades = fetch_trades(m["conditionId"])
                except Exception as e:
                    print(f"ERR trades {slug}: {e}")
                    continue
                try:
                    new_rows.extend(evaluate_market(m, trades, candle_cache.get(asset, {}), now))
                except Exception as e:
                    print(f"ERR eval {slug}: {e}")
            w += dur
        state["cursors"][series] = max(cur, w)
    # merge with existing ledger: dedupe by (strategy, variant, slug), preferring more-final rows
    existing = {}
    if os.path.exists(LEDGER):
        with open(LEDGER) as f:
            for line in f:
                try:
                    r = json.loads(line)
                    existing[(r.get("strategy"), r.get("variant"), r.get("slug"))] = r
                except Exception:
                    pass
    rank = lambda s: {"skipped_stale":0,"skipped_price":0,"skipped_nosignal":0,"skipped_nospot":0,"unfilled":1,"open":2,"win":3,"loss":3,"refund":3}.get(s, 0)
    added = upgraded = 0
    for r in new_rows:
        k = (r.get("strategy"), r.get("variant"), r.get("slug"))
        old = existing.get(k)
        if old is None:
            existing[k] = r; added += 1
        elif rank(r.get("status")) > rank(old.get("status")):
            existing[k] = r; upgraded += 1
    with open(LEDGER, "w") as f:
        for k in sorted(existing, key=lambda x: (existing[x].get("window_start") or 0, str(x))):
            f.write(json.dumps(existing[k]) + "\n")
    rows = list(existing.values())
    def stats(filt):
        sel = [r for r in rows if filt(r)]
        fills = [r for r in sel if r.get("status") in ("win", "loss", "open")]
        settled = [r for r in sel if r.get("status") in ("win", "loss")]
        wins = [r for r in settled if r["status"] == "win"]
        net = sum(r.get("pnl", 0) for r in settled)
        fees = sum(r.get("fee", 0) for r in settled)
        return {"signals": len(fills) + len([r for r in sel if r.get("status")=="unfilled"]),
                "fills": len(fills), "open": len([r for r in fills if r["status"]=="open"]),
                "settled": len(settled), "wins": len(wins),
                "win_rate": round(len(wins)/len(settled),4) if settled else None,
                "net": round(net,2), "fees": round(fees,2),
                "worst": min([r.get("pnl",0) for r in settled], default=0)}
    summary = {"markets_processed": n_markets, "added": added, "upgraded": upgraded,
               "A90": stats(lambda r: r.get("variant")=="A90"), "A45": stats(lambda r: r.get("variant")=="A45"),
               "A90d": stats(lambda r: r.get("variant")=="A90d"),
               "B05": stats(lambda r: r.get("variant")=="B05"), "B02": stats(lambda r: r.get("variant")=="B02"),
               "B10": stats(lambda r: r.get("variant")=="B10"),
               "cursors": state["cursors"], "now": now}
    json.dump(state, open(STATE, "w"), indent=1)
    json.dump(summary, open(os.path.join(BASE, "summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))

if __name__ == "__main__":
    main()
