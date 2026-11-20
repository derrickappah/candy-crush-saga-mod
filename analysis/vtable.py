import re, struct, json, sys
from elftools.elf.elffile import ELFFile

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
raw = open(PATH, "rb").read()

with open(PATH, "rb") as f:
    e = ELFFile(f)
    secs = {s.name: s for s in e.iter_sections()}
    rodata = secs[".rodata"]
    ro_addr, ro_off, ro_size = rodata["sh_addr"], rodata["sh_offset"], rodata["sh_size"]
    drr = secs[".data.rel.ro"]
    drr_addr, drr_off, drr_size = drr["sh_addr"], drr["sh_offset"], drr["sh_size"]
    text = secs[".text"]
    text_addr, text_off, text_size = text["sh_addr"], text["sh_offset"], text["sh_size"]
    rela = secs[".rela.dyn"]
    rela_off, rela_size = rela["sh_offset"], rela["sh_size"]

# 1. RTTI name strings -> vaddr
names = {}
for m in re.finditer(rb"(?<![0-9A-Za-z_])([0-9]{1,3})([A-Z][0-9A-Za-z_]{2,120})", raw[ro_off:ro_off + ro_size]):
    ln = int(m.group(1))
    enc = m.group(2)
    if 1 <= ln <= len(enc) <= 130:
        names[m.start() + ro_off] = enc[:ln].decode("ascii", "ignore")
print("name strings:", len(names))

# 2. relocations
relocs = []  # (offset_vaddr, addend)
for i in range(0, rela_size, 24):
    off, info, addend = struct.unpack_from("<QQq", raw, rela_off + i)
    typ = info & 0xFFFFFFFF
    if typ == 1027:  # R_AARCH64_RELATIVE
        relocs.append((off, addend))
print("relative relocs:", len(relocs))
by_off = dict(relocs)

# 3. typeinfo objects: reloc whose addend is a name string vaddr (points to len byte)
ti_by_name = {}
for off, addend in relocs:
    if addend in names:
        # typeinfo start = off - 8  (vtable ptr, then __type_name at off)
        ti_by_name[off - 8] = names[addend]
print("typeinfo objects:", len(ti_by_name))

# 4. vtables: reloc whose addend == typeinfo start, at offset vtable_start+8
funcs = {}
out = []
for off, addend in relocs:
    if addend in ti_by_name:
        vtsym = off - 8
        cls = ti_by_name[addend]
        # walk forward collecting function pointers
        entries = []
        p = vtsym + 16
        while p in by_off and by_off[p] != 0:
            tgt = by_off[p]
            if not (text_addr <= tgt < text_addr + text_size):
                break
            entries.append(tgt)
            p += 8
        if entries:
            out.append((cls, vtsym, entries))

print("classes with vtables:", len(out))
json.dump([{"cls": c, "vtable": v, "funcs": f} for c, v, f in out], open("vtables.json", "w"))
for c, v, f in out[:15]:
    print(f"{c} vtable={v:#x} nfuncs={len(f)} first={f[0]:#x}")
