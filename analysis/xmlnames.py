import zipfile, re, sys

z = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk")
f = "assets/res_output/bundled/candycrushsaga/assets/scenes/settings/menu_settings_fullscreen.xml"
d = z.read(f).decode("utf-8", "replace")

pat = sys.argv[1] if len(sys.argv) > 1 else r'[Nn]ame="([^"]{3,40})"'
for m in re.finditer(pat, d):
    print(m.group(1) if m.groups() else m.group(0))
