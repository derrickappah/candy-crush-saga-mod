import re, sys

d = open(sys.argv[1], "rb").read().decode("utf-16-le", "replace")
print("chars", len(d))
keys = sorted(set(re.findall(r'"([A-Za-z_.0-9]{3,40})"', d)))
for k in keys[:80]:
    print(k)
print("--- numbers near booster-ish keys ---")
for m in re.finditer(r'"([A-Za-z_.0-9]*[Bb]ooster[A-Za-z_.0-9]*)"\s*:\s*([^,}\]]{1,40})', d):
    print(m.group(1), "=", m.group(2)[:40])
