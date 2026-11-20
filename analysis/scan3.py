import struct, io
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
import zipfile

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
taddr, toff, tsize = t["sh_addr"], t["sh_offset"], t["sh_size"]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

PAT = 0x91008148  # add x8, x10, #0x20
n = 0
for i in range(tsize // 4):
    w = struct.unpack_from("<I", raw, toff + i * 4)[0]
    if w != PAT:
        continue
    pc = taddr + i * 4
    code = raw[toff + i * 4: toff + (i + 8) * 4]
    nxt = [(ins.address, ins.mnemonic, ins.op_str) for ins in md.disasm(code, pc)][1:8]
    for a, mn, ops in nxt:
        if mn == "ldr" and ops.startswith("w0, [x8]"):
            print(f"=== GETTER? {a:#x}  (find at {pc:#x})")
            back = raw[toff + (i - 8) * 4: toff + (i + 10) * 4]
            for ins in md.disasm(back, pc - 8 * 4):
                mark = ">>" if ins.address == a else "  "
                print(f" {mark} {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
            print()
            n += 1
            break
print("total", n)
