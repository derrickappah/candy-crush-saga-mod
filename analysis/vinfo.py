import json, sys

v = json.load(open(r"C:\Users\DELL\Downloads\candy crach 2\work\vtables.json"))
targets = {int(a, 16) for a in sys.argv[1:]}
for e in v:
    for i, f in enumerate(e["funcs"]):
        if f in targets:
            print(f"{e['cls']} vtable={e['vtable']:#x} slot={i} func={f:#x}")
