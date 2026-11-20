# Recreating every mod from scratch

This is the full trail for all five mods: what the code does, how each site was found, the exact bytes,
and how to prove the patch is live. No prior work from this repo is required beyond the pristine APK.

Offsets are file offsets into `lib/arm64-v8a/libcandycrushsaga.so` from `com.king.candycrushsaga`
1.325.0.1 (versionCode `13250011`, 84,485,416 bytes, SHA-256
`b123d846d5b4f6e503c4139503b193645b1f803aa95cbbe6dcbbc92c2170ebf1` — recompute yours and compare before
trusting any offset).

## 0. Why offsets are also addresses

The library is a normal ELF shared object. Its `.text` section has `sh_addr == sh_offset`, i.e. the first
byte of code is at virtual address `0x1d28150` *and* file offset `0x1d28150`. Every patch below is written
at the same number for both, so a hex editor, a Python slice and `capstone` all agree without a translator.
Confirm before starting:

```python
from elftools.elf.elffile import ELFFile
with open("libcandycrushsaga.so", "rb") as f:
    t = ELFFile(f).get_section_by_name(".text")
    assert t["sh_addr"] == t["sh_offset"], "offsets need translation, adjust your tooling"
```

## 1. Acquisition and tooling

The phone is unrooted, so a modified APK must be signed and installed over the Play Store build (which
means uninstalling first, and losing local progress — progress is cloud-saved on the King account).

```sh
adb shell pm path com.king.candycrushsaga          # -> base.apk (single split for this build)
adb pull /data/app/.../base.apk base.apk
unzip -j base.apk lib/arm64-v8a/libcandycrushsaga.so -d .
```

Needed: Python 3 + `capstone` + `pyelftools`, Android SDK build-tools (`zipalign`, `apksigner`), a keystore,
`adb`. Never install with the incremental path — `adb install --no-incremental -r -d` — because an
incremental install survives the adb host dying badly and leaves a half-materialised app.

Work on a copy. Keep `base.apk` and the pristine `.so` untouched; `tools/mkpatch.py` re-copies the pristine
library on every run and aborts if a site is already patched.

## 2. How sites are found at all

Strings are the entry point, not the offset. The binary is stripped, so a symbol name only exists if it
appears in a log, an assert or a UI string. From there:

1. `grep -abo "some string" libcandycrushsaga.so` → file offset.
2. Find the code that loads that address: `adrp xN, #page` + `add xN, xN, #off` pairs. Their sum is the
   string address; the instruction after the pair is what consumes it. A precomputed map of
   `string address -> [code sites]` turns this into a lookup (`work/xrefs.pkl`, built by scanning `.text`
   for `adrp`/`add` pairs).
3. Read upward from the reference to the enclosing function, identify the vtable slot or the branch, and
   decide what a single instruction can change.
4. Confirm the guess dynamically before committing to a patch: count calls, dump arguments, or hook the
   function and observe. This build no longer ships Frida's gadget, so dynamic work needs it re-added
   (apktool decode, `libgadget.so` in `lib/arm64-v8a`, one `System.loadLibrary("gadget")` in the launcher
   activity, `adb forward tcp:27042`) — the offsets are the same either way.
5. Static confirmation works too: the modified instruction set must still pass a disassembler, and the
   patched site must disassemble to what you intended.

Two rules learned the hard way:

* patch the **getter**, never the storage, when the UI must agree with the game;
* a getter can be too hot to lie. Verify with a call count before patching something that looks correct.

## 3. Mod 1 — moves counter is a constant

**Behaviour wanted:** the HUD move count never falls below what you set.

`CGameState::GetMoves` is at `0x2a031b4` and is the only source of the counter:

```
total = A(variant @+0x100)     ; moves granted for the level
used  = B(variant @+0x60)      ; moves consumed
return total - used
```

Its vtable slot is `+0x118`; two thin wrappers sit on top — `IsOutOfMoves` = `GetMoves() < 1` at
`0x2a032b8` and the inverse at `0x2a03294`. Everything (HUD, booster availability, sugar crush, the lose
check) reads through those, which is why replacing the function body keeps the whole game consistent:

```
pristine  sub  sp, sp, #0x60                ...
patched   mov  w0, #101        A0 0C 80 52
          ret                  C0 03 5F D6
```

`#101` is `#0x65`; any imm16 up to 65535 works. **Zero does not**: the out-of-moves check runs on level
entry before a result object exists, so `moves == 0` fails the level instantly. `1` is the useful low value
(one move, then the level ends and — with mod 5 — counts as a win).

Verification: HUD reads the constant, a swap decrements it to the constant again, and the level does not
end at 101 moves.

## 4. Mod 2 — console, testing menu, debug view

Three gates, all in the debug/console plumbing, plus two asset flags.

```
pristine  0x1e83a18  cmp  w9, #2            console adapter factory, early-outs on the production env
patched              cmp  w9, #0xff         3F FD 03 71

pristine  0x1e81bf8  stp  x29, x30, ...     ab.ccsm_content_in_level_testing_menu
patched              mov  w0, #1            20 00 80 52
                     ret                  C0 03 5F D6

pristine  0x1f0fc54  cbz  x8, ...           Debug.DebugViewAvailable, first condition
patched              nop                    1F 20 03 D5
pristine  0x1f0fc5c  cbz  ...               second condition
patched              nop                    1F 20 03 D5
```

The console is *still* gated on config, and that part is an asset edit, not a patch: in
`assets/res_output/configs/common_live.settings` and `_fiction_default.settings` set

```json
"UseConsole": true, "ConsoleMaxLines": 40, "HaveDebugRenderer": true, "UseStatsView": true
```

Both files are 2,050 bytes; they are copied verbatim into the overlay. Without them the console object
exists but never draws.

Reachability: the console row lives in the **in-level** Settings dialog (open any level, tap the gear),
under `Debug | Console`, and the console overlay stays up after the dialog is closed. The map's settings
has no such row.

Driving it from adb: `input text "cmd%sarg"` — a literal space is lost, `%s` is the separator — and
`input keyevent 66` to submit. `clear` empties the scrollback; useful, because the view otherwise stays
where it was and looks like the command did nothing.

## 5. Mod 3 — lives refill in one second

The life system is `CLifeManipulationLogic` plus a pool record
`{ lives @+0x00, nextTick @+0x08, interval @+0x10, max @+0x14 }`. Each tick copies the record and only
increments when `nextTick + interval <= now`. The interval is loaded in three places; all three become `1`:

```
pristine  0x1ec9c80  ldrsw x10, [x19, #0x10]   pool record interval (1800 s)
patched              mov   x10, #1             2A 00 80 D2

pristine  0x1e89b60  ldrsw x8,  [x19, #0x40]   regenerator schedule
patched              mov   x8,  #1             28 00 80 D2
pristine  0x1e89c7c  ldrsw x9,  [x19, #0x40]
patched              mov   x9,  #1             29 00 80 D2
```

The regenerator must be patched alongside the tick or the pool refills but the scheduler keeps booking the
next attempt 30 minutes out. With both, the cap of 5 is reached in seconds and the HUD reads `Full`.

Verification: spend lives to 0, watch the counter climb within seconds and the HUD settle on `Full`.

## 6. Mod 4 — boosters read 99 and unowned ones are selectable

Two getters, because the UI has two paths. The inventory model is one:

```
CBoosterInventoryModel::GetAmount
pristine  0x22fb08c  add  w0, w9, w8            bonusSum + stored
patched              mov  w0, #99               60 0C 80 52
```

The pre-level menu does **not** go through it. Its handler walks
`button -> [menu+0x28] service -> CSaveDataPersistedBoosterData -> CSaveData record -> CInMemoryBoosterData`
and reads `[record+4]` directly, so the second site is the amount getter of `CInMemoryBoosterData` at
`0x288b290`:

```
pristine  0x288b294  ldr  w0, [x8, #4]
patched              mov  w0, #99               60 0C 80 52
```

Only one vtable in the binary references `0x288b290` (`0x4e41548`), so it is booster-specific — patching it
cannot bleed into another inventory type.

Amounts are still written back to `[record+4]` when a booster is spent; the getter lies, the storage stays
truthful. The count therefore always reads 99 and never runs out, but the save file will not show 99.

Verification: the in-level booster bar shows 99 on all five slots, the pre-level menu shows 99 on cards that
were never owned, and tapping one actually grants it.

## 7. Mod 5 — every finished level counts as a win

`0x2abb5ec` is the level-result routine. It builds a result object, calls its `won?` getter (vtable `+0x18`)
and then either keeps the object (`0x2abb6a0`: stars, progress, map advance) or destroys it (`0x2abb704`):

```
pristine  0x2abb69c  tbz  w0, #0, #0x2abb704     branch to the "not won" path
patched              nop                          1F 20 03 D5
```

With the branch gone, the losing path is unreachable and any level that *ends* is scored as completed.

The practical skip: enter the level, tap the top-right exit, wait for the bonus animation, tap `Tap to
skip`. The map advances one node. Note that the Settings `Quit level` row is a different path and still
gives `Level failed!` — use the exit button.

Verification: three consecutive levels, each entered and immediately left, with the map node advancing each
time. `0` moves (mod 1) is not enough on its own for the same reason as above.

## 8. Rebuild, sign, install

`tools/repackage.py` rewrites the APK entry by entry in the original order, preserving compression method
and timestamps, and substitutes or adds files from an overlay directory. Overlay = the patched `.so` plus
the two settings files, nothing else.

```sh
python tools/mkpatch.py libcandycrushsaga.so          # -> build/lib/arm64-v8a/libcandycrushsaga.so
python tools/repackage.py base.apk mod.apk build
zipalign -f -P 16 4 mod.apk mod_aligned.apk
apksigner sign --ks ~/.android/debug.keystore --ks-pass pass:android \
    --key-pass pass:android --ks-key-alias androiddebugkey --out mod-signed.apk mod_aligned.apk
apksigner verify --print-certs mod-signed.apk
adb uninstall com.king.candycrushsaga
adb install --no-incremental -r -d mod-signed.apk
```

`-P 16` keeps 16 KiB page alignment, required for the native library to load on newer Android.
`verify --print-certs` must print the debug certificate; if the APK is unsigned or signed with another key,
the install fails with `INSTALL_FAILED_UPDATE_INCOMPATIBLE`.

Disk space is a real constraint: the APK is ~150 MB and repacking plus signing briefly needs a few GB. A
failed `zipalign` with `Malformed APK: not a ZIP archive` right after `failed rewriting` means the disk
filled, not a corrupt build.

## 9. Confirming the shipped file

Before installing, prove the built library is the wanted one — disassemble each site and compare:

```python
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
for off in (0x2a031b4, 0x1e83a18, 0x1e81bf8, 0x1f0fc54, 0x1f0fc5c, 0x1e89b60,
            0x1e89c7c, 0x1ec9c80, 0x22fb08c, 0x288b294, 0x2abb69c):
    ins = next(md.disasm(d[off:off + 8], off))
    print(f"{off:#x}: {ins.mnemonic} {ins.op_str}")
```

After install, the same offsets must exist in the installed copy; `adb pull` reaches the base APK path
without root because the file is world-readable. In-game behaviour is the real test, and it is cheap:
HUD number, lives counter, booster slots, and one level entered and abandoned.

## 10. Rollback

Reinstall the untouched `base.apk` (signed with the same debug key) or build with an empty overlay. Since
every patch is a single instruction, partial rollback is just omitting that line from `PATCHES`.

## 11. Ideas that did not work

Kept so they are not retried blindly:

| Site | Idea | Outcome |
|------|------|---------|
| `0x3b15c38`, `0x3b15d54` | scale getters → constant gold | ~270k calls/min; constant value turns the whole scene magenta (they feed atlas/quad counts) |
| `0x20f5a28`, `0x20f5a30` | `HardCurrency` paid/free getters | dormant on the map, 0 calls in a 60 s count, no visible change |
| `0x1d593b0` | generic data-source `SetValue` | only carries `BoosterWheel.*` and `SeasonPass.TimeLeft`, never currency |
| `0x2a031b4` with `mov w0, #0` | instant level end | fails on entry, out-of-moves check beats the result object |
