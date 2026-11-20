import zipfile, io, struct
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
taddr, toff, tsize = t["sh_addr"], t["sh_offset"], t["sh_size"]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

hits = 0
for i in range(tsize // 4):
    w = struct.unpack_from("<I", raw, toff + i * 4)[0]
    if (w & 0xFFC00000) != 0xB9000000:
        continue
    if ((w >> 10) & 0xFFF) != 0x24 // 4:
        continue
    pc = taddr + i * 4
    back = raw[toff + (i - 8) * 4: toff + (i + 4) * 4]
    lines = list(md.disasm(back, pc - 8 * 4))
    txt = " ".join(f"{x.mnemonic} {x.op_str}" for x in lines)
    if "sub" not in txt:
        continue
    print("=== store 0x24 @", hex(pc))
    for ins in lines:
        mark = ">>" if ins.address == pc else "  "
        print(f" {mark} {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
    print()
    hits += 1
    if hits >= 6:
        break
print("hits", hits)
