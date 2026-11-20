import zipfile, json

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
pat = bytes.fromhex("0804 40F9 0005 40B9 C003 5FD6".replace(" ", ""))

hits = []
i = raw.find(pat)
while i != -1:
    hits.append(i)
    i = raw.find(pat, i + 1)
print("hits", len(hits))

vt = json.load(open(r"C:\Users\DELL\Downloads\candy crach 2\work\vtables.json"))
byfunc = {}
for e in vt:
    for f in e["funcs"]:
        byfunc.setdefault(f, []).append((e["vtable"], e["cls"]))

for h in hits:
    users = byfunc.get(h, [])
    names = sorted({c for _, c in users})
    print(f"{h:#x} -> {names[:4]}")
