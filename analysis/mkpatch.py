import shutil, os

SRC = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
OUT = r"C:\Users\DELL\Downloads\candy crach 2\work\patch\lib\arm64-v8a\libcandycrushsaga.so"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)
d = bytearray(open(OUT, "rb").read())

NOP = bytes.fromhex("1F2003D5")
MOV_W0_1_RET = bytes.fromhex("20008052" "C0035FD6")

PATCHES = [
    # 1) CGameState::GetMoves -> always 101
    (0x2A031B4, bytes.fromhex("A00C8052" "C0035FD6")),
    # 2) console adapter factory: treat non-production env (skip `env == 2` early-out)
    (0x1E83A18, bytes.fromhex("3FFD0371")),          # cmp w9, #0xff
    # 3) ab.ccsm_content_in_level_testing_menu -> true (enables CCsm testing menu)
    (0x1E81BF8, MOV_W0_1_RET),
    # 4) Debug.DebugViewAvailable -> always true (shows Console / Stats buttons)
    (0x1F0FC54, NOP),
    (0x1F0FC5C, NOP),
    # 5) life regeneration interval -> 1 second (lives refill almost instantly)
    (0x1E89B60, bytes.fromhex("280080D2")),          # ldrsW x8,[x19,#0x40] -> mov x8,#1
    (0x1E89C7C, bytes.fromhex("290080D2")),          # ldrsW x9,[x19,#0x40] -> mov x9,#1
    # 6) life-pool refill tick: use 1s interval instead of the pooled 1800s
    (0x1EC9C80, bytes.fromhex("2A0080D2")),          # ldrsw x10,[x19,#0x10] -> mov x10,#1
    # 7) CBoosterInventoryModel::GetAmount -> always 99 (unlimited boosters)
    (0x22FB08C, bytes.fromhex("600C8052")),          # add w0,w9,w8 -> mov w0,#99
    # 8) CInMemoryBoosterData amount getter -> always 99 (UI path for booster counts)
    (0x288B294, bytes.fromhex("600C8052")),          # ldr w0,[x8,#4] -> mov w0,#99
    # 9) level-result handling: drop the "not won" branch, so every finished level is a win
    (0x2ABB69C, NOP),                                # tbz w0,#0,#0x2abb704 -> nop
]

for off, new in PATCHES:
    old = bytes(d[off:off + len(new)])
    print(f"{off:#x}  {old.hex()} -> {new.hex()}")
    assert old != new, f"already patched at {off:#x}"
    d[off:off + len(new)] = new

open(OUT, "wb").write(d)

from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
for off, new in PATCHES:
    print(f"--- {off:#x}")
    for ins in md.disasm(bytes(d[off:off + len(new)]), off):
        print(f"    {ins.address:#x}: {ins.mnemonic} {ins.op_str}")
print("written", len(d))
