import zipfile, json

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")

vt = json.load(open(r"C:\Users\DELL\Downloads\candy crach 2\work\vtables.json"))
byfunc = {}
for e in vt:
    for f in e["funcs"]:
        byfunc.setdefault(f, set()).add(e["cls"])

ret = bytes.fromhex("C0035FD6")
for name, hexs in (("paid +0x14", "001440B9"), ("free +0x18", "001840B9")):
    pat = bytes.fromhex(hexs) + ret
    hits = []
    i = raw.find(pat)
    while i != -1:
        hits.append(i)
        i = raw.find(pat, i + 1)
    print(name, len(hits))
    for h in hits:
        print("  ", hex(h), sorted(byfunc.get(h, []))[:3])
