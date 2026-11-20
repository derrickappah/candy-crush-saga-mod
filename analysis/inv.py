import zipfile, collections, sys

path = sys.argv[1]
z = zipfile.ZipFile(path)
infos = z.infolist()
print("entries:", len(infos))
print("uncompressed MB:", round(sum(i.file_size for i in infos) / 1048576, 2))
c = collections.Counter()
for i in infos:
    n = i.filename
    parts = n.split("/")
    if len(parts) == 1:
        c["<ROOTFILE> " + n] += i.file_size
    elif parts[0] == "lib" and len(parts) > 2:
        c["lib/" + parts[1] + "/" + parts[2]] += i.file_size
    elif parts[0] == "lib":
        c["lib/" + parts[1]] += i.file_size
    else:
        c[parts[0] + "/"] += i.file_size
print("=== size by bucket ===")
for k, v in c.most_common(50):
    print(f"{v/1048576:9.2f} MB  {k}")
print("=== abis ===", sorted({i.filename.split('/')[1] for i in infos if i.filename.startswith('lib/')}))
print("=== root files ===", [i.filename for i in infos if '/' not in i.filename])
print("=== native libs ===")
for i in infos:
    if i.filename.startswith("lib/") and i.filename.endswith(".so"):
        print(f"{i.file_size:12d}  {i.filename}")
print("=== assets sample (first 60) ===")
for i in infos:
    if i.filename.startswith("assets/"):
        print(f"{i.file_size:12d}  {i.filename}")
