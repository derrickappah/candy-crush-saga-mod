import zipfile

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")

for name, hexs in (("paid +4", "000440B9C0035FD6"), ("free +8", "000840B9C0035FD6")):
    pat = bytes.fromhex(hexs)
    hits = []
    i = raw.find(pat)
    while i != -1:
        hits.append(i)
        i = raw.find(pat, i + 1)
    print(name, len(hits), [hex(h) for h in hits[:20]])
