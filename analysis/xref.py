import zipfile, io, sys
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
ta, to, ts = t["sh_addr"], t["sh_offset"], t["sh_size"]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

targets = {int(a, 16) for a in sys.argv[1:]}
step = 1 << 20
pos = 0
while pos < ts:
    chunk = raw[to + pos: to + min(pos + step, ts)]
    for i in md.disasm(chunk, ta + pos):
        if i.mnemonic in ("bl", "b") and i.operands:
            try:
                if i.operands[-1].imm in targets:
                    print(f"{i.address:#x} {i.mnemonic} -> {i.operands[-1].imm:#x}")
            except Exception:
                pass
    pos += step
