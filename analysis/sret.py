import zipfile, io
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
ta, to = t["sh_addr"], t["sh_offset"]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

A = [0x21cef50,0x21cf074,0x21d20b0,0x21d20b4,0x21d02e4,0x21d09b0,0x21cf0e8,0x21cf654,
     0x21d09e0,0x21d2224,0x21d200c,0x21d20b8,0x21d29a0,0x21d22f8,0x21d2664,0x21d2818,
     0x21d2860,0x21d2878,0x21d2018,0x21d1dd8]

for f in A:
    ins = list(md.disasm(raw[to + (f - ta): to + (f - ta) + 0x120], f))[:24]
    sret = any(i.mnemonic.startswith(("str", "stp")) and i.op_str.rstrip().endswith("x8]")
               for i in ins)
    if sret:
        print(f"--- {f:#x} (sret candidate)")
        for i in ins[:8]:
            print(f"    {i.address:#x}: {i.mnemonic} {i.op_str}")
