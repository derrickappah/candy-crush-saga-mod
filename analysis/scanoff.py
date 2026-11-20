import struct, sys
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
with open(PATH, "rb") as f:
    e = ELFFile(f)
    t = e.get_section_by_name(".text")
    taddr, toff, tsize = t["sh_addr"], t["sh_offset"], t["sh_size"]
raw = open(PATH, "rb").read()

imm = int(sys.argv[1], 16)
skip_sp = (len(sys.argv) > 3 and sys.argv[3] == 'nosp')
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
hits = 0
for i in range(tsize // 4):
    w = struct.unpack_from("<I", raw, toff + i * 4)[0]
    if (w & 0xFFC00000) == 0x39400000 and ((w >> 10) & 0xFFF) == imm:
        if skip_sp and ((w >> 5) & 0x1F) == 31:
            continue
        pc = taddr + i * 4
        print(f"=== ldrb @ {pc:#x}")
        code = raw[toff + i * 4: toff + i * 4 + limit * 4]
        for ins in md.disasm(code, pc):
            print(f"    {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
        hits += 1
        if hits > 25:
            break
print("hits", hits)
