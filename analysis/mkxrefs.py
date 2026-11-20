import struct, json, pickle, sys
from elftools.elf.elffile import ELFFile

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
with open(PATH, "rb") as f:
    e = ELFFile(f)
    text = e.get_section_by_name(".text")
    taddr, toff, tsize = text["sh_addr"], text["sh_offset"], text["sh_size"]

raw = open(PATH, "rb").read()
text = raw[toff:toff + tsize]

refs = {}
def se21(v):
    return v - (1 << 21) if v & (1 << 20) else v

n = tsize // 4
adrp = {}  # reg -> (page, insn_addr)
count = 0
for i in range(n):
    w = struct.unpack_from("<I", text, i * 4)[0]
    pc = taddr + i * 4
    if (w & 0x9F000000) == 0x90000000:
        rd = w & 0x1F
        imm = ((w >> 5) & 0x7FFFF) << 2 | ((w >> 29) & 0x3)
        page = (pc & ~0xFFF) + (se21(imm) << 12)
        adrp[rd] = (page, pc)
    elif w in (0xD65F03C0,):  # ret
        adrp.clear()
    else:
        if adrp:
            op = w & 0xFF800000
            if op == 0x91000000 or op == 0xF9400000 or op == 0x39400000 or op == 0xB9400000 or op == 0x79400000 or op == 0x39400000 and False:
                pass
            # ADD immediate, 64-bit, shift 0
            if op == 0x91000000:
                rn = (w >> 5) & 0x1F
                rd = w & 0x1F
                if rn in adrp and ((w >> 22) & 0x3) == 0:
                    page = adrp[rn][0]
                    tgt = page + ((w >> 10) & 0xFFF)
                    refs.setdefault(tgt, []).append(pc)
                    count += 1
            # LDR (unsigned offset) 64-bit
            elif op == 0xF9400000:
                rn = (w >> 5) & 0x1F
                if rn in adrp:
                    page = adrp[rn][0]
                    tgt = page + (((w >> 10) & 0xFFF) * 8)
                    refs.setdefault(tgt, []).append(pc)
                    count += 1
            # LDR (literal) word/byte
            elif (w & 0x3B000000) == 0x18000000:
                imm = (w >> 5) & 0x7FFFF
                if imm & 0x40000:
                    imm -= 0x80000
                tgt = pc + imm * 4
                refs.setdefault(tgt, []).append(pc)
                count += 1

print("refs:", count, "targets:", len(refs))
pickle.dump({"taddr": taddr, "refs": refs}, open("xrefs.pkl", "wb"))
