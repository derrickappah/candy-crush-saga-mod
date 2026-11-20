"""Rebuild an APK by overlaying files onto the original ZIP, preserving entry order,
compression method and metadata. Alignment/signing are done afterwards by zipalign/apksigner."""
import sys, os, zipfile

base, out, overlay = sys.argv[1], sys.argv[2], sys.argv[3]

over = {}
for dirpath, _, files in os.walk(overlay):
    for f in files:
        p = os.path.join(dirpath, f)
        rel = os.path.relpath(p, overlay).replace("\\", "/")
        over[rel] = p

zin = zipfile.ZipFile(base)
names = set(zin.namelist())
missing = [k for k in over if k not in names]
print("overlay files:", len(over), "new files:", missing)

with zipfile.ZipFile(out, "w") as zout:
    for info in zin.infolist():
        data = None
        if info.filename in over:
            with open(over[info.filename], "rb") as fh:
                data = fh.read()
            print(f"  replaced {info.filename} ({len(data)} bytes)")
        else:
            data = zin.read(info.filename)
        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        zi.compress_type = info.compress_type
        zi.external_attr = info.external_attr
        zi.internal_attr = info.internal_attr
        zi.create_system = info.create_system
        zout.writestr(zi, data)
    for k in missing:
        with open(over[k], "rb") as fh:
            data = fh.read()
        zi = zipfile.ZipInfo(k)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zout.writestr(zi, data)
        print(f"  added {k}")
print("wrote", out, os.path.getsize(out))
