"""Recover the console command registry by scanning for calls to the register function
and resolving the name/description string arguments loaded just before them.

Uses op_str parsing (no capstone detail) so it works without CS_ERR_DETAIL.
"""
import io, sys, re
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
raw = open(PATH, "rb").read()
e = ELFFile(io.BytesIO(raw))
t = e.get_section_by_name(".text")
ta, to, ts = t["sh_addr"], t["sh_offset"], t["sh_size"]

REG = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x25CC3CC

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

RE_ADRP = re.compile(r"^(x\d+), #0x([0-9a-f]+)$")
RE_ADD = re.compile(r"^(x\d+), (x\d+), #0x([0-9a-f]+)$")


def cstr(a):
    if not (0 < a < len(raw)):
        return None
    e2 = raw.find(b"\x00", a, a + 300)
    if e2 < 0:
        return None
    try:
        s = raw[a:e2].decode("utf-8")
    except UnicodeDecodeError:
        return None
    return s if all(32 <= ord(c) < 127 or c == "\n" for c in s) else None


def scan(lo, hi):
    regs = {}
    for ins in md.disasm(raw[lo:hi], lo):
        m, ops = ins.mnemonic, ins.op_str
        if m == "adrp":
            g = RE_ADRP.match(ops)
            if g:
                regs[g.group(1)] = int(g.group(2), 16)
        elif m == "add":
            g = RE_ADD.match(ops)
            if g and g.group(2) in regs:
                regs[g.group(1)] = regs[g.group(2)] + int(g.group(3), 16)
        elif m == "bl":
            if not ops.startswith("#0x") or int(ops[3:], 16) != REG:
                continue
            name = desc = None
            v1, v2 = regs.get("x1"), regs.get("x2")
            if v1:
                name = cstr(v1)
            if v2:
                desc = cstr(v2)
            if name and desc and 1 <= len(name) <= 120:
                yield ins.address, name, desc


seen = set()
out = []
pos = 0
step = 1 << 19
while pos < ts:
    for site, name, desc in scan(ta + pos, ta + min(pos + step, ts)):
        if (name, desc) in seen:
            continue
        seen.add((name, desc))
        out.append((site, name, desc))
    pos += step

out.sort()
for site, name, desc in out:
    print(f"{site:#x}\t{name}\t{desc[:110].replace(chr(10), ' / ')}")
print("total", len(out))
