import pickle, sys

bl = pickle.load(open(r"C:\Users\DELL\Downloads\candy crach 2\work\blmap.pkl", "rb"))
for a in sys.argv[1:]:
    t = int(a, 16)
    sites = bl.get(t, [])
    print(f"{t:#x}: {len(sites)} callers")
    for s in sites:
        print(f"   {s:#x}")
