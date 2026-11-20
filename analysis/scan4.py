import zipfile, io
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

raw = zipfile.ZipFile(r"C:\Users\DELL\Downloads\candy crach 2\work\orig\base.apk").read(
    "lib/arm64-v8a/libcandycrushsaga.so")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
start = 0
while True:
    i = raw.find(b"\x48\x81\x00\x91", start)
    if i < 0:
        break
    start = i + 1
    if i % 4:
        continue
    print(f"=== site {i:#x}")
    for ins in md.disasm(raw[i - 24: i + 40], i - 24):
        mark = ">>" if ins.address == i else "  "
        print(f" {mark} {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
    print()
