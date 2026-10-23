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

# captions: progressive word highlight; line = sentence; current word + next word amber
sents = re.split(r'(?<=[.!?]) ', script)
idx = 0; sent_ranges = []
for s in sents:
    n = len(s.split()); sent_ranges.append((idx, idx+n, s)); idx += n
def ass_time(t):
    t = max(t, 0); h = int(t//3600); m = int((t%3600)//60); sec = t%60
    return f"{h}:{m:02d}:{sec:05.2f}"
events = []
for (a, b, sent) in sent_ranges:
    words = sent.split()
    for i in range(len(words)):
        t0 = time_of(a+i); t1 = end_of(a+i) if i == len(words)-1 else time_of(a+i+1)
        parts = []
        for j, w in enumerate(words):
            if i <= j <= i+1:
                parts.append(r"{\c&H00B3FF&}" + w + r"{\c&HFFFFFF&}")
            else:
                parts.append(w)
        line = " ".join(parts) + "‏"
        events.append(f"Dialogue: 0,{ass_time(t0)},{ass_time(t1)},Default,,0,0,0,,{line}")
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
open("captions_fuel.ass","w").write(hdr + "\
".join(events) + "\
")
print(len(events), "events;", cfg)