import zipfile, struct, json

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
ret = bytes.fromhex("C0035FD6")

hits = []
for off in range(0, 0x60, 4):
    w = 0xB9000000 | ((off // 4) << 10) | 1
    pat = struct.pack("<I", w) + ret
    i = raw.find(pat)
    while i != -1:
        hits.append((i, off))
        i = raw.find(pat, i + 1)

print(len(hits))
print(json.dumps([h[0] for h in hits]))
