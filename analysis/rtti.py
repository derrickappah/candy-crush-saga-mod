import re, sys, collections

# Itanium RTTI type names are stored as <len><encoding> strings, e.g. "24CMemoryTamperingDetector"
PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
d = open(PATH, "rb").read()

pat = re.compile(rb"(?<![0-9A-Za-z_])(\d{1,3})([A-Z][0-9A-Za-z_]{2,120})")
names = collections.Counter()
for m in pat.finditer(d):
    ln = int(m.group(1))
    enc = m.group(2)
    if 1 <= ln <= len(enc) <= 130:
        enc = enc[:ln].decode("ascii", "ignore")
        names[enc] += 1

print("distinct RTTI encodings:", len(names))

kw = sys.argv[1].split(",") if len(sys.argv) > 1 else None
sel = [n for n in names if kw is None or any(k.lower() in n.lower() for k in kw)]
print("selected:", len(sel))
for n in sorted(sel):
    print(n)
