import zipfile, json, struct

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")

vt = json.load(open(r"C:\Users\DELL\Downloads\candy crach 2\work\vtables.json"))
byfunc = {}
for e in vt:
    for f in e["funcs"]:
        byfunc.setdefault(f, set()).add(e["cls"])

pre = bytes.fromhex("080440F9")
ret = bytes.fromhex("C0035FD6")
out = []
i = raw.find(pre)
while i != -1:
    for off in range(0, 0x80, 4):
        w = 0xB9400000 | ((off // 4) << 10) | (8 << 5)
        ins = struct.pack("<I", w)
        if raw[i + 4:i + 8] == ins and raw[i + 8:i + 12] == ret:
            out.append((i, off))
    i = raw.find(pre, i + 1)

for a, off in out:
    print(f"{a:#x} field +{off:#x} -> {sorted(byfunc.get(a, []))[:3]}")
