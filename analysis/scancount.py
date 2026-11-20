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

PAT = 0x91002148  # add x8, x10, #0x20
for i in range(tsize // 4):
    w = struct.unpack_from("<I", raw, toff + i * 4)[0]
    if w != PAT:
        continue
    pc = taddr + i * 4
    code = raw[toff + i * 4: toff + (i + 6) * 4]
    lines = [(ins.address, ins.mnemonic, ins.op_str) for ins in md.disasm(code, pc)]
    if any(m == "ldr" and o.startswith("w0, [x8]") for _, m, o in lines[1:6]):
        print("=== candidate @", hex(pc))
        back = raw[toff + (i - 40) * 4: toff + (i + 6) * 4]
        for ins in md.disasm(back, pc - 40 * 4):
            mark = ">>" if ins.address == pc else "  "
            print(f" {mark} {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
        print()
        if len(sys.argv) > 1:
            break
