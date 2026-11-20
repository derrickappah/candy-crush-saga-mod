import struct, sys

path = sys.argv[1]
d = open(path, "rb").read()
e_shoff = struct.unpack_from("<Q", d, 0x28)[0]
e_shentsize = struct.unpack_from("<H", d, 0x3A)[0]
e_shnum = struct.unpack_from("<H", d, 0x3C)[0]
e_shstrndx = struct.unpack_from("<H", d, 0x3E)[0]
print("shoff", e_shoff, "shnum", e_shnum, "shstrndx", e_shstrndx, "entsize", e_shentsize)

def sh(i):
    off = e_shoff + i * e_shentsize
    name, typ, flags, addr, offset, size, link, info, align, entsize = struct.unpack_from("<IIQQQQIIQQ", d, off)
    return dict(name=name, typ=typ, flags=flags, offset=offset, size=size, entsize=entsize, link=link)

shstr = sh(e_shstrndx)
def sname(n):
    e = d.index(b"\0", shstr["offset"] + n)
    return d[shstr["offset"] + n:e].decode("ascii", "replace")

tot_sym = 0
for i in range(e_shnum):
    s = sh(i)
    nm = sname(s["name"])
    cnt = s["size"] // 24 if s["entsize"] == 24 else ""
    print(f"  {i:3d} {nm:28s} type={s['typ']:3d} flags={s['flags']:4d} off={s['offset']:10d} size={s['size']:10d} entsize={s['entsize']} nsym={cnt}")
    if nm in (".dynsym", ".symtab"):
        tot_sym += s["size"] // 24 if s["entsize"] == 24 else 0
print("total symbols:", tot_sym)
print("has .symtab:", any(sname(sh(i)["name"]) == ".symtab" for i in range(e_shnum)))
