"""Build a patched copy of libcandycrushsaga.so.

Inputs:  the pristine library extracted from the APK of Candy Crush Saga 1.325.0.1
         (arm64-v8a, 84,485,416 bytes, SHA-256 in README).
Output:  build/lib/arm64-v8a/libcandycrushsaga.so

Then repackage:

    python tools/repackage.py base.apk out.apk build
    zipalign -f -P 16 4 out.apk out_a.apk
    apksigner sign --ks ~/.android/debug.keystore --ks-pass pass:android \
        --key-pass pass:android --ks-key-alias androiddebugkey --out mod.apk out_a.apk
"""
import os, shutil, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "libcandycrushsaga.so"
OUT = os.path.join("build", "lib", "arm64-v8a", "libcandycrushsaga.so")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)
d = bytearray(open(OUT, "rb").read())

NOP = bytes.fromhex("1F2003D5")
MOV_W0_1_RET = bytes.fromhex("20008052" "C0035FD6")

# (offset, new bytes) — every site is inside .text, whose vaddr equals its file offset
PATCHES = [
    # CGameState::GetMoves -> always 101 (movz w0,#0x65 ; ret)
    (0x2A031B4, bytes.fromhex("A00C8052" "C0035FD6")),
    # console adapter factory: skip the `env == 2` production early-out
    (0x1E83A18, bytes.fromhex("3FFD0371")),          # cmp w9, #0xff
    # ab.ccsm_content_in_level_testing_menu -> true
    (0x1E81BF8, MOV_W0_1_RET),
    # Debug.DebugViewAvailable -> true (both conditions)
    (0x1F0FC54, NOP),
    (0x1F0FC5C, NOP),
    # life regeneration interval -> 1 second
    (0x1E89B60, bytes.fromhex("280080D2")),          # -> mov x8,#1
    (0x1E89C7C, bytes.fromhex("290080D2")),          # -> mov x9,#1
    # life-pool refill tick: 1 s instead of the pooled 1800 s
    (0x1EC9C80, bytes.fromhex("2A0080D2")),          # -> mov x10,#1
    # CBoosterInventoryModel::GetAmount -> always 99
    (0x22FB08C, bytes.fromhex("600C8052")),          # add w0,w9,w8 -> mov w0,#99
    # CInMemoryBoosterData amount getter (the path the UI uses) -> always 99
    (0x288B294, bytes.fromhex("600C8052")),          # ldr w0,[x8,#4] -> mov w0,#99
    # level-result handler: drop the "not won" branch, every finished level counts as a win
    (0x2ABB69C, NOP),                                # tbz w0,#0,#0x2abb704 -> nop
]

for off, new in PATCHES:
    old = bytes(d[off:off + len(new)])
    if old == new:
        raise SystemExit(f"already patched at {off:#x}")
    d[off:off + len(new)] = new

open(OUT, "wb").write(d)

from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
for off, new in PATCHES:
    for ins in md.disasm(bytes(d[off:off + len(new)]), off):
        print(f"{ins.address:#x}: {ins.mnemonic} {ins.op_str}")
print("written", OUT, len(d))
