import json, pickle, re, struct, sys
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
raw = open(PATH, "rb").read()
with open(PATH, "rb") as f:
    e = ELFFile(f)
    secs = {s.name: s for s in e.iter_sections()}
    text = secs[".text"]
    taddr, toff, tsize = text["sh_addr"], text["sh_offset"], text["sh_size"]
    ro = secs[".rodata"]
    roaddr, rooff, rosize = ro["sh_addr"], ro["sh_offset"], ro["sh_size"]

data = pickle.load(open("xrefs.pkl", "rb"))
refs = data["refs"]

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = False

PROLOGUES = [
    bytes.fromhex("fd7bbfa9"),  # stp x29,x30,[sp,#-0x10]!
    bytes.fromhex("fd7bbf69"),  # stp x29,x30,[sp,#-0x10]
]

def find_string(s):
    b = s.encode()
    out = []
    start = 0
    while True:
        i = raw.find(b, start)
        if i < 0:
            break
        if rooff <= i < rooff + rosize:
            out.append(roaddr + (i - rooff))
        start = i + 1
    return out

def func_start(addr):
    """scan backwards for a plausible prologue; return best (earliest plausible) candidate"""
    off = toff + (addr - taddr)
    best = None
    for back in range(4, 0x1000, 4):
        o = off - back
        if o < toff:
            break
        w = raw[o:o + 4]
        # stp x29,x30,[sp,#-imm]! : A9B?7BFD family -> match loosely
        if w[0] == 0xFD and w[1] == 0x7B and (w[3] == 0xA9):
            best = taddr + (o - toff)
        # sub sp, sp, #imm  (0xD10?), or paciasp / bti
        ww = struct.unpack("<I", w)[0]
        if (ww & 0xFFC003FF) == 0xD10003FF:
            best = taddr + (o - toff)
        if ww == 0xD503233F or ww == 0xD503245F:
            cand = taddr + (o - toff)
            if best is None or cand < best:
                best = cand
    return best

def show(addr, n=120, before=0):
    off = toff + (addr - taddr)
    code = raw[off - before * 4: off + n * 4]
    base = addr - before * 4
    print(f"--- disasm @ {addr:#x} (file off {off:#x})")
    for ins in md.disasm(code, base):
        mark = ">>" if ins.address == addr else "  "
        print(f"{mark} {ins.address:#010x}: {ins.mnemonic:10s} {ins.op_str}")

def xrefs_to_string(s):
    addrs = find_string(s)
    print(f"string {s!r} at {[hex(a) for a in addrs]}")
    for a in addrs:
        for site in refs.get(a, []):
            print(f"  ref @ {site:#x}  func~{hex(func_start(site) or 0)}")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "s":
        xrefs_to_string(sys.argv[2])
    elif cmd == "d":
        show(int(sys.argv[2], 16), int(sys.argv[3]) if len(sys.argv) > 3 else 120)
    elif cmd == "f":
        a = int(sys.argv[2], 16)
        print(f"func start ~ {func_start(a):#x}" if func_start(a) else "no start found")
