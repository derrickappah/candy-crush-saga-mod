import pickle, sys, re

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
raw = open(PATH, "rb").read()
data = pickle.load(open(r"C:\Users\DELL\Downloads\candy crach 2\work\xrefs.pkl", "rb"))
refs = data["refs"]
# .rodata bounds
import struct
from elftools.elf.elffile import ELFFile
with open(PATH, "rb") as f:
    e = ELFFile(f)
    ro = e.get_section_by_name(".rodata")
    roaddr, rooff, rosize = ro["sh_addr"], ro["sh_offset"], ro["sh_size"]

word = sys.argv[1]
exact = sys.argv[2] == "1" if len(sys.argv) > 2 else True
nul = b"\x00"
start = rooff
hits = []
while True:
    i = raw.find(word.encode(), start, rooff + rosize)
    if i < 0:
        break
    start = i + 1
    if exact:
        if raw[i - 1] != 0 and i > rooff:
            continue
        if raw[i + len(word)] != 0:
            continue
    hits.append(roaddr + (i - rooff))
for h in hits:
    print(f"{word!r} @ {h:#x} refs={[hex(x) for x in refs.get(h, [])]}")
