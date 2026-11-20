import zipfile, io
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
ta, to = t["sh_addr"], t["sh_offset"]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

start, end = 0x20f3000, 0x20f7000
for i in md.disasm(raw[to + (start - ta): to + (end - ta)], start):
    if i.mnemonic.startswith("str") and (i.op_str.endswith("#0x14]") or i.op_str.endswith("#0x18]")):
        print(f"{i.address:#x} {i.mnemonic} {i.op_str}")
