#!/usr/bin/env python3
"""audit_recompute.py - independent reimplementation used for AUDIT_INDEPENDENT.md.
Reads the frozen per-coin series in this directory, recomputes M1-M4 from scratch,
optionally with the corrected basket (USDF excluded, true TON from CoinGecko substituted).
Usage: python3 audit_recompute.py [--corrected ton_cg.json]
No worker code is imported; conventions documented in AUDIT_INDEPENDENT.md."""
import json, datetime, sys, os
D=datetime.date; G0,G1=D(2026,9,24),D(2026,10,22); ONE=datetime.timedelta(days=1); COST=0.001
HERE=os.path.dirname(os.path.abspath(__file__))
STABLE={'blackrock-usd-institutional-digital-liquidity-digital-fund',
 'blackrock-usd-institutional-digital-liquidity-fund','global-dollar','hashnote-usyc',
 'ondo-us-dollar-yield','pax-gold','ripple-usd','spiko-amundi-overnight-swap-fund-eur',
 'tether-gold','usd1-wlfi'}
corrected = len(sys.argv)>2 and sys.argv[1]=='--corrected'
if corrected: STABLE = STABLE | {'falcon-finance'}
basket=json.load(open(os.path.join(HERE,'basket.json')))
S={}
for c in basket:
    if c in STABLE: continue
    p=os.path.join(HERE,c+'.json')
    if not os.path.exists(p): continue
    d=json.load(open(p))
    s={datetime.datetime.utcfromtimestamp(ts/1000).date():float(v) for ts,v in d['prices']}
    if len(s)>=12: S[c]=s
if corrected:
    cg=json.load(open(sys.argv[2]))
    raw={datetime.datetime.utcfromtimestamp(ts/1000).date():float(p) for ts,p in cg['prices']}
    S['the-open-network']={d-ONE:p for d,p in raw.items()}  # CG label d = UTC close of d-1
def ret(c,a,b):
    s=S[c]; return s[b]/s[a]-1 if a in s and b in s else None
rebs=[G0+7*ONE*i for i in range(5)]
def mom(restrict=None,nextbar=True,exclude=set(),topn=3):
    mult=1.0; log=[]
    cands=[c for c in S if c not in exclude and (restrict is None or c in restrict)]
    for i,t in enumerate(rebs):
        ex=t+ONE if nextbar else t
        nxt=rebs[i+1] if i+1<len(rebs) else None
        end=(nxt+ONE if nextbar else nxt) if nxt else None
        if end is None or end>G1: end=G1
        ranked=sorted(((S[c][t]/S[c][t-7*ONE]-1,c) for c in cands if t in S[c] and t-7*ONE in S[c]),reverse=True)
        picks=[c for _,c in ranked[:topn]]; log.append((str(t),str(ex),picks))
        if ex>G1: continue
        seg=[r for r in (ret(c,ex,end) for c in picks) if r is not None]
        if seg: mult*=(1+sum(seg)/len(seg))*(1-COST)**topn
    return round((mult-1)*100,2),log
def ew(nextbar=True):
    mult=1.0
    for i,t in enumerate(rebs):
        ex=t+ONE if nextbar else t
        nxt=rebs[i+1] if i+1<len(rebs) else None
        end=(nxt+ONE if nextbar else nxt) if nxt else None
        if end is None or end>G1: end=G1
        if ex>G1: continue
        rs=[r for r in (ret(c,ex,end) for c in S) if r is not None]
        mult*=(1+sum(rs)/len(rs))*(1-COST)
    return round((mult-1)*100,2)
def trend(c,nextbar):
    s=S[c]; dates=sorted(s); v=[s[d] for d in dates]
    gi=[i for i,d in enumerate(dates) if G0<=d<=G1]
    pos=1.0; m=1.0; sw=0; pend=None
    for k in range(gi[0],gi[-1]):
        sm=sum(v[k-6:k+1])/7 if k>=6 else None
        sig=None if sm is None else (1.0 if v[k]>sm else 0.0)
        if not nextbar and sig is not None and sig!=pos: pos=sig; sw+=1; m*=(1-COST)
        if nextbar and pend is not None and pend!=pos: pos=pend; pend=None; sw+=1; m*=(1-COST)
        m*=(1+pos*(v[k+1]/v[k]-1))
        if nextbar and sig is not None and sig!=pos: pend=sig
    return round((m-1)*100,2),sw
def dipbuy(c):
    s=S[c]; dates=sorted(d for d in s if G0<=d<=G1); out=[]
    for i,d in enumerate(dates):
        hist=[s[x] for x in dates[max(0,i-6):i+1]]   # true trailing 7-day incl today
        if len(hist)<7: continue
        if s[d]<=max(hist)*0.90: out.append(str(d))
    return out
liq20=['bitcoin','ethereum','ripple','solana','binancecoin','dogecoin','cardano','tron',
 'hyperliquid','bitcoin-cash','chainlink','stellar','litecoin','the-open-network',
 'avalanche-2','shiba-inu','polkadot','uniswap','near','monero']
res={'corrected_basket':corrected,
 'M1':{m:round(ret(m,G0,G1)*100,2) for m in ['bitcoin','ethereum','solana']},
 'M2':{m:{'next':trend(m,True),'same':trend(m,False)} for m in ['bitcoin','ethereum','solana']},
 'M3_next':mom(),'M3_same':mom(nextbar=False),
 'M3_next_exQNT':mom(exclude={'quant-network'}),'M3_same_exQNT':mom(exclude={'quant-network'},nextbar=False),
 'M3_liquid20_next':mom(restrict=[c for c in liq20 if c in S]),
 'M3_liquid20_same':mom(restrict=[c for c in liq20 if c in S],nextbar=False),
 'EW_next':ew(),'EW_same':ew(False),
 'M4':{m:dipbuy(m) for m in ['bitcoin','ethereum','solana']}}
print(json.dumps(res,indent=1))
