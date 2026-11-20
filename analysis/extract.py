import zipfile, os, sys, collections

src = sys.argv[1]
dst = sys.argv[2]
z = zipfile.ZipFile(src)
z.extractall(dst)
print("extracted to", dst)

# summarize res_output pack structure
base = os.path.join(dst, "assets", "res_output")
if os.path.isdir(base):
    print("=== res_output top-level entries ===")
    for name in sorted(os.listdir(base))[:200]:
        p = os.path.join(base, name)
        if os.path.isdir(p):
            n = sum(len(f) for _, _, f in os.walk(p))
            print(f"DIR  files={n:6d}  {name}")
        else:
            print(f"FILE {os.path.getsize(p):8d}  {name}")
