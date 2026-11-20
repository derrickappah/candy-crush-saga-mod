import zipfile

z = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk")
needles = [b"HardCurrency.", b"GoldBar", b"gold_bar", b"Currency.Balance"]
hits = 0
for i in z.infolist():
    n = i.filename
    if not n.startswith("assets/") or i.is_dir():
        continue
    if i.file_size > 3_000_000:
        continue
    try:
        d = z.read(n)
    except Exception:
        continue
    if b"\x00" in d[:200]:
        continue
    for nd in needles:
        if nd in d:
            idx = d.find(nd)
            print(n, "|", nd.decode(), "|", d[max(0, idx - 60):idx + 60].decode("utf-8", "replace").replace("\n", " "))
            hits += 1
            break
    if hits > 25:
        break
