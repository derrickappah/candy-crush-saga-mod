import os, re, sys

root = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\assets"
pat = re.compile(sys.argv[1], re.I)
hits = 0
for dirpath, _, files in os.walk(root):
    for f in files:
        if not f.lower().endswith((".xml", ".json", ".prop", ".settings", ".txt", ".md", ".csv")):
            continue
        p = os.path.join(dirpath, f)
        try:
            t = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for m in pat.finditer(t):
            s = max(0, m.start() - 80)
            print(f"--- {p}\n    ...{t[s:m.end()+120].replace(chr(10),' | ')}")
            hits += 1
            break
        if hits > 60:
            sys.exit()
