import json, sys

v = json.load(open(r"C:\Users\DELL\Downloads\candy crach 2\work\vtables.json"))
kw = [k.lower() for k in sys.argv[1].split(",")]
for e in v:
    if any(k in e["cls"].lower() for k in kw):
        print(f"{e['cls']:52s} vtable={e['vtable']:#x} n={len(e['funcs'])}")
        print("   ", " ".join(hex(x) for x in e["funcs"]))
