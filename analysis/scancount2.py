import struct, io, sys
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
import zipfile

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
taddr, toff, tsize = t["sh_addr"], t["sh_offset"], t["sh_size"]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

shown = 0
for i in range(tsize // 4):
    w = struct.unpack_from("<I", raw, toff + i * 4)[0]
    if w != 0xB9400100:  # ldr w0, [x8]
        continue
    pc = taddr + i * 4
    back = raw[toff + (i - 14) * 4: toff + (i + 3) * 4]
    lines = list(md.disasm(back, pc - 14 * 4))
    txt = " ".join(f"{x.mnemonic} {x.op_str}" for x in lines)
    if "[x8, #0x1c]" not in txt or "csel" not in txt:
        continue
    print("=== @", hex(pc))
    for ins in lines:
        print(f"   {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
    print()
    shown += 1
    if shown >= 4:
        break
print("shown", shown)
