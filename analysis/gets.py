import zipfile, io
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
ta, to = t["sh_addr"], t["sh_offset"]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

start, end = 0x288b000, 0x288c000
ins = list(md.disasm(raw[to + (start - ta): to + (end - ta)], start))
for i in range(len(ins) - 3):
    a, b, c = ins[i], ins[i + 1], ins[i + 2]
    if (a.mnemonic == "ldr" and a.op_str.startswith("x8, [x0, #8]")
            and b.mnemonic == "ldr" and b.op_str.startswith("w0, [x8")
            and c.mnemonic == "ret"):
        print(f"{a.address:#x}  ldr {b.op_str}")
