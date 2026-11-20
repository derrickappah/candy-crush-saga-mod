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
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

hits = 0
for i in range(tsize // 4):
    w = struct.unpack_from("<I", raw, toff + i * 4)[0]
    # ldr xt, [xn, #imm] : F9400000 base, imm12 in bits 10..21
    if (w & 0xFFC00000) != 0xF9400000:
        continue
    if ((w >> 10) & 0xFFF) * 8 != imm:
        continue
    rd = w & 0x1F
    # look ahead up to 3 insns for blr rd
    for k in range(1, 5):
        w2 = struct.unpack_from("<I", raw, toff + (i + k) * 4)[0]
        if w2 == 0xD63F0000 | (rd << 5):  # blr rd
            pc = taddr + i * 4
            print(f"=== indirect call slot {imm:#x} @ {pc:#x}")
            code = raw[toff + (i - 8) * 4: toff + (i + 4) * 4]
            for ins in md.disasm(code, pc - 8 * 4):
                print(f"    {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
            hits += 1
            break
    if hits > int(sys.argv[2] if len(sys.argv) > 2 else 30):
        break
print("hits", hits)
