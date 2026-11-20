import zipfile, re

d = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read("AndroidManifest.xml")
s = d.decode("utf-8", "replace")
seen = set()
for m in re.finditer(r'[A-Za-z][A-Za-z0-9+.-]{1,20}://[^"<> ]{0,50}', s):
    v = m.group(0)
    if v not in seen:
        seen.add(v)
        print(v[:70])
for m in re.finditer(r'(?:scheme|host)="([^"]{2,40})"', s):
    print("ATTR", m.group(1))
