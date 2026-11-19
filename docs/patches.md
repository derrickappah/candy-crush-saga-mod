# Patch reference

All sites are file offsets inside `lib/arm64-v8a/libcandycrushsaga.so`, 1.325.0.1, arm64-v8a.
`.text` is mapped with `sh_addr == sh_offset`, so the file offset is also the virtual address.

Disassembly was done with `capstone`; every site was confirmed against the pristine library before
patching and read back from the running process afterwards.

## 1. `0x2a031b4` — moves constant

```
pristine:  sub sp, sp, #0x60                 (entry of CGameState::GetMoves)
patched:   mov w0, #101 ; ret                A0 0C 80 52  C0 03 5F D6
```

`GetMoves` (vtable slot `0x118`) is the single source of truth for the counter:

```
total = A(variant@+0x100)      // moves granted
used  = B(variant@+0x60)       // moves consumed
return total - used
```

Two thin wrappers sit on it — `IsOutOfMoves` = `GetMoves() < 1` (`0x2a032b8`) and the inverse at
`0x2a03294` — so HUD, boosters, sugar crush and the lose check all stay consistent.

`#101` is `#0x65`. Driving it to `0` **fails the level on entry**: the out-of-moves check runs before a
result object exists. `1` works and makes each level end after one move if you want a faster loop.

## 2–3. `0x1e83a18`, `0x1e81bf8` — testing menu / console gate

```
pristine:  cmp w9, #2                        (console adapter factory early-out on production env)
patched:   cmp w9, #0xff                     3F FD 03 71

pristine:  stp x29, x30, ...                 (ab.ccsm_content_in_level_testing_menu)
patched:   mov w0, #1 ; ret                  20 00 80 52  C0 03 5F D6
```

## 4–5. `0x1f0fc54`, `0x1f0fc5c` — `Debug.DebugViewAvailable`

```
pristine:  cbz x8, ...
patched:   nop                               1F 20 03 D5
```

Removes both conditions so the debug view is reported available. The console itself is still gated on
`"UseConsole": true` in `assets/res_output/configs/common_live.settings` and `_fiction_default.settings`
(`"ConsoleMaxLines": 40, "HaveDebugRenderer": true, "UseStatsView": true` alongside it) — those are asset
edits, not patches, and are part of the overlay.

## 6–9. `0x1ec9c80`, `0x1e89b60`, `0x1e89c7c` — lives

```
pristine:  ldrsw x10, [x19, #0x10]           (pool record interval, 1800 s)
patched:   mov x10, #1                       2A 00 80 D2

pristine:  ldrsw x8, [x19, #0x40]            (regenerator schedule)
patched:   mov x8, #1                        28 00 80 D2
pristine:  ldrsw x9, [x19, #0x40]
patched:   mov x9, #1                        29 00 80 D2
```

`CLifeManipulationLogic` refills in a per-call tick that copies the pool record
(`{lives @+0x00, nextTick @+0x08, interval @+0x10, max @+0x14}`) and only increments when
`nextTick + interval <= now`. With the interval at 1 s the tick adds a life every second up to the cap of
5, and the regenerator schedules its next attempt 1 s out to match.

Observed: `lives=0` → `5 / "Full"` within seconds.

## 10–11. `0x22fb08c`, `0x288b294` — boosters

```
pristine:  add w0, w9, w8                    (CBoosterInventoryModel::GetAmount, bonusSum + stored)
patched:   mov w0, #99                       60 0C 80 52

pristine:  ldr w0, [x8, #4]                  (CInMemoryBoosterData amount getter, 0x288b290)
patched:   mov w0, #99                       60 0C 80 52
```

The pre-level menu never touches the inventory model. Its handler walks
`button -> [menu+0x28] service -> CSaveDataPersistedBoosterData -> CSaveData record -> CInMemoryBoosterData`
and reads `[record+4]`, which is why site 11 exists. Only one vtable in the binary references
`0x288b290` (`0x4e41548`), so it is booster-specific.

Amounts are still written back to the real field when a booster is spent — the getter has to lie, not the
storage. Do not expect the save file to change.

## 12. `0x2abb69c` — level result

```
pristine:  tbz w0, #0, #0x2abb704            (w0 = result object's "won" getter, vtable +0x18)
patched:   nop                               1F 20 03 D5
```

The result routine at `0x2abb5ec` builds a result object, asks it whether the player won, and then either
keeps it (`0x2abb6a0`: stars, progress, map advance) or destroys it (`0x2abb704`). NOP-ing the branch
makes the losing path unreachable, so any level that ends is scored as completed.

Practical skip: enter the level, tap the top-right exit, wait for the bonus animation, tap to skip. The
level completes and the map advances. Verified on three consecutive levels.

## Sites that did not work

Recorded so they are not rediscovered:

| Site | Idea | Result |
|------|------|--------|
| `0x3b15c38`, `0x3b15d54` | profile scale getters → constant gold | ~270k calls/min, but patching renders the scene fully magenta (they feed atlas/quad counts) |
| `0x20f5a28`, `0x20f5a30` | `HardCurrency` model paid/free balance getters | never called on the map (0 hits in a 60 s count), no visible change |
| `0x1d593b0` | generic data-source `SetValue` | only ever carries `BoosterWheel.*` and `SeasonPass.TimeLeft`, not currency |
