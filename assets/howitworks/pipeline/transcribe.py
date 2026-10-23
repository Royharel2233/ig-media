import json, sys
from faster_whisper import WhisperModel
m = WhisperModel("base", device="cpu", compute_type="int8")
segs, _ = m.transcribe(sys.argv[1], language="he", word_timestamps=True)
words = [{"w": w.word, "t": round(w.start,3), "d": round(w.end-w.start,3)} for s in segs for w in s.words]
json.dump(words, open(sys.argv[2],"w"), ensure_ascii=False)
print(len(words), "words")