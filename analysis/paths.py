import re, sys, collections

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
d = open(PATH, "rb").read()
kw = sys.argv[1] if len(sys.argv) > 1 else "/src/"
strs = set(re.findall(rb"[/A-Za-z0-9_.\-]{4,200}", d))
sel = sorted(s.decode("ascii", "ignore") for s in strs if kw.encode() in s)
print("count", len(sel))
for s in sel:
    print(s)
