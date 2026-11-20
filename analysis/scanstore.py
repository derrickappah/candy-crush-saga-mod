import struct, sys
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk"
import zipfile
raw = zipfile.ZipFile(PATH).read("lib/arm64-v8a/libcandycrushsaga.so")

# parse ELF from memory image
import io
from elftools.elf.elffile import ELFFile
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
taddr, toff, tsize = t["sh_addr"], t["sh_offset"], t["sh_size"]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

targets = [int(x, 16) for x in sys.argv[1].split(",")]
# STR (immediate, unsigned offset): size in bits 30-31, opcode 111001 -> 0xB9000000 for W
hits = 0
for i in range(tsize // 4):
    w = struct.unpack_from("<I", raw, toff + i * 4)[0]
    opc = w & 0xFFC00000
    if opc not in (0xB9000000, 0xF9000000, 0x39000000):
        continue
    imm = (w >> 10) & 0xFFF
    off = imm * (8 if opc == 0xF9000000 else (1 if opc == 0x39000000 else 4))
    if off not in targets:
        continue
    pc = taddr + i * 4
    print(f"=== store{off:#x} @ {pc:#x}")
    code = raw[toff + (i - 6) * 4: toff + (i + 4) * 4]
    for ins in md.disasm(code, pc - 6 * 4):
        print(f"    {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
    hits += 1
    if hits > 40:
        break
print("hits", hits)
