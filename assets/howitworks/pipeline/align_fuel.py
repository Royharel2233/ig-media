import json, re, difflib, unicodedata
script = open("vo_fuel.txt").read().strip()
script_words = script.split()
whis = json.load(open("asr_fuel.json"))
norm = lambda w: re.sub(r'[.,!?;:«»"\']', '', ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c) != 'Mn'))
sw = [norm(w) for w in script_words]; ww = [norm(w["w"]) for w in whis]
sm = difflib.SequenceMatcher(None, sw, ww)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2-i1): mapping[i1+k] = j1+k
    else:
        for k in range(i2-i1): mapping[i1+k] = j1 + min(k, max(j2-j1-1,0))
def time_of(i): return whis[mapping[i]]["t"]
def end_of(i): w = whis[mapping[i]]; return w["t"] + w["d"]
def fw(sub, start=0):
    for i in range(start, len(sw)):
        if sub in sw[i]: return i
    raise KeyError(sub)
i_venturi = fw("צוואר")
i_block = fw("חוסם")
i_click = fw("קליק", start=i_block)
i_round = fw("לעגל")
i_canister = fw("הפחם")
i_cta = fw("מכיר")
cfg = {
 "fps": 24,
 "t_insert_start": time_of(i_venturi) - 0.8,
 "t_insert_end":   end_of(fw("הקנה")) + 0.4,
 "t_pulse_start":  time_of(i_block) - 1.2,
 "t_pulse_end":    end_of(i_click) + 0.5,
 "t_turn_start":   time_of(i_round) - 0.6,
 "t_canister":     time_of(i_canister) - 0.6,
 "t_turn_end":     end_of(fw("דולרים")) + 0.4,
}
cfg["t_end"] = end_of(len(sw)-1) + 1.3
cfg["frames"] = int(cfg["t_end"] * cfg["fps"]) + 1
json.dump(cfg, open("config_fuel.json","w"), indent=1)
json.dump(cfg, open("config_fuel_cam.json","w"), indent=1)

# captions: progressive word highlight over SHORT display lines (<=5 words / 32 chars per
# group, sentence boundaries respected) - regression fix 23.10: sentence-per-line produced
# 4-5-line paragraph blocks (28-word sentence). current word + next word amber. Proper \n
# line endings (the old "\\" continuation glued all events onto one line and libass saw 0 events).
sents = re.split(r'(?<=[.!?]) ', script)
groups = []
for s in sents:
    ws = s.split(); g = []
    for w in ws:
        if g and (len(g) >= 5 or len(' '.join(g + [w])) > 32):
            groups.append(g); g = []
        g.append(w)
    if g: groups.append(g)
def ass_time(t):
    t = max(t, 0); h = int(t//3600); m = int((t%3600)//60); sec = t%60
    return f"{h}:{m:02d}:{sec:05.2f}"
events = []
idx = 0
for g in groups:
    for i in range(len(g)):
        gi = idx + i
        t0 = time_of(gi)
        t1 = end_of(gi) if gi == len(script_words)-1 else time_of(gi+1)
        parts = []
        for j, w in enumerate(g):
            if i <= j <= i+1:
                parts.append(r"{\c&H00B3FF&}" + w + r"{\c&HFFFFFF&}")
            else:
                parts.append(w)
        events.append(f"Dialogue: 0,{ass_time(t0)},{ass_time(t1)},Default,,0,0,0,," + " ".join(parts) + "\u200f")
    idx += len(g)
events.append(f"Dialogue: 0,{ass_time(end_of(len(script_words)-1))},{ass_time(cfg['t_end'])},Default,,0,0,0,," + " ".join(groups[-1]) + "\u200f")
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Secular One,68,&H00FFFFFF,&H0000B3FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,3.2,0,2,40,40,160,178

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open("captions_fuel.ass","w",encoding="utf-8").write(hdr + "\n".join(events) + "\n")
print(len(events), "events;", cfg)