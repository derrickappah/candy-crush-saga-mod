import zipfile, io
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
ta, to = t["sh_addr"], t["sh_offset"]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

start, end = 0x21dd000, 0x21df500
prev = None
starts = []
for i in md.disasm(raw[to + (start - ta): to + (end - ta)], start):
    if i.mnemonic in ("sub", "stp") and i.op_str.startswith("sp, sp") and prev in ("ret", "b", "nop", "bl", None):
        starts.append(i.address)
    if i.mnemonic == "stp" and i.op_str.startswith("x29, x30, [sp, #-") and prev in ("ret", "b", "nop", None):
        starts.append(i.address)
    prev = i.mnemonic
for s in starts:
    if 0x21ddd00 <= s <= 0x21de000:
        print(f"{s:#x}")
