import pickle, sys

d = pickle.load(open(r"C:\Users\DELL\Downloads\candy crach 2\work\xrefs.pkl", "rb"))
refs = d["refs"]
for a in sys.argv[1:]:
    t = int(a, 16)
    print(f"{t:#x} refs: {[hex(x) for x in refs.get(t, [])]}")
