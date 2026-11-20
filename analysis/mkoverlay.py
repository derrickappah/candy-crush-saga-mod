import os, shutil, sys

src = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\assets\res_output\configs"
ov = r"C:\Users\DELL\Downloads\candy crach 2\work\overlay"
os.makedirs(os.path.join(ov, "assets", "res_output", "configs"), exist_ok=True)
for name in ("common_live.settings", "_fiction_default.settings"):
    s = open(os.path.join(src, name), encoding="utf-8").read()
    s = s.replace('"UseConsole": false', '"UseConsole": true')
    s = s.replace('"ConsoleMaxLines": 0', '"ConsoleMaxLines": 40')
    s = s.replace('"HaveDebugRenderer": false', '"HaveDebugRenderer": true')
    s = s.replace('"UseStatsView": false', '"UseStatsView": true')
    open(os.path.join(ov, "assets", "res_output", "configs", name), "w", encoding="utf-8", newline="\n").write(s)
    print(name, "UseConsole" in s, s.count('"UseConsole": true'))
