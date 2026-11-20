import zipfile, io, json
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
taddr, toff, tsize = t["sh_addr"], t["sh_offset"], t["sh_size"]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

funcs = [0x22fc410, 0x22fc504, 0x22faeec, 0x22fafd0, 0x22fb0f8, 0x22fb1dc,
         0x22fb364, 0x22fb750, 0x22fb8d8, 0x22fb9fc, 0x22fbad0, 0x22fbad4,
         0x22fbdc4, 0x22fbdd4, 0x22fbf00, 0x22fbf10, 0x22fc070, 0x22fc2d0]

for idx, f in enumerate(funcs):
    off = toff + (f - taddr)
    code = raw[off: off + 0x400]
    ins = []
    for i in md.disasm(code, f):
        ins.append(i)
        if i.mnemonic == "ret" or len(ins) > 120:
            break
    tail = ins[-6:]
    print(f"--- slot {idx} @ {f:#x}  ({len(ins)} insns)")
    for i in tail:
        print(f"    {i.address:#x}: {i.mnemonic:8s} {i.op_str}")
