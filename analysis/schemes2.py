import re, sys

path = r"C:\Users\DELL\Downloads\candy crach 2\work\decoded_smali\AndroidManifest.xml"
s = open(path, encoding="utf-8", errors="replace").read()
for m in re.finditer(r'android:(scheme|host)="([^"]+)"', s):
    print(m.group(1), m.group(2))
print("---- data tags ----")
for m in re.finditer(r"<data [^>]{0,200}>", s):
    print(m.group(0)[:160])
