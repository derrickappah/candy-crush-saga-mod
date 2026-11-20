import struct, pickle
from elftools.elf.elffile import ELFFile

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
with open(PATH, "rb") as f:
    e = ELFFile(f)
    text = e.get_section_by_name(".text")
    taddr, toff, tsize = text["sh_addr"], text["sh_offset"], text["sh_size"]
raw = open(PATH, "rb").read()[toff:toff + tsize]

bl = {}
for i in range(tsize // 4):
    w = struct.unpack_from("<I", raw, i * 4)[0]
    if (w & 0xFC000000) == 0x94000000:
        imm = w & 0x3FFFFFF
        if imm & 0x2000000:
            imm -= 0x4000000
        tgt = taddr + i * 4 + imm * 4
        bl.setdefault(tgt, []).append(taddr + i * 4)
print("bl targets:", len(bl), "sites:", sum(len(v) for v in bl.values()))
pickle.dump(bl, open("blmap.pkl", "wb"))
