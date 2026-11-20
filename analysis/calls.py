import struct, sys
from elftools.elf.elffile import ELFFile

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
with open(PATH, "rb") as f:
    e = ELFFile(f)
    t = e.get_section_by_name(".text")
    taddr, toff, tsize = t["sh_addr"], t["sh_offset"], t["sh_size"]
raw = open(PATH, "rb").read()

start = int(sys.argv[1], 16)
end = int(sys.argv[2], 16)
o = toff + (start - taddr)
for i in range((end - start) // 4):
    w = struct.unpack_from("<I", raw, o + i * 4)[0]
    pc = start + i * 4
    if (w & 0xFC000000) == 0x94000000 or (w & 0xFC000000) == 0x14000000:
        imm = w & 0x3FFFFFF
        if imm & 0x2000000:
            imm -= 0x4000000
        tgt = pc + imm * 4
        kind = "BL" if (w & 0xFC000000) == 0x94000000 else "B "
        print(f"{pc:#x} {kind} -> {tgt:#x}")
