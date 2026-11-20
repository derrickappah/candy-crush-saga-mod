import re, sys

path = sys.argv[1]
pats = [p.encode() for p in sys.argv[2].split(",")]
d = open(path, "rb").read()
strs = re.findall(rb"[ -~]{5,160}", d)
seen = set()
for s in strs:
    if any(p in s for p in pats):
        t = s.decode("ascii", "ignore")
        if t not in seen:
            seen.add(t)
            print(t)
