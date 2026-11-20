# Analysis workspace

Every script used to find the patch sites, plus the recovery notes. Nothing here is needed to *build*
the mod — that is `tools/mkpatch.py` — but this is the trail, including the dead ends.

Paths in most scripts point at `work/ext/lib/arm64-v8a/libcandycrushsaga.so` (the pristine library) and
`work/xrefs.pkl`; adjust the two constants at the top if you keep them elsewhere.

## Static tooling

| Script | Purpose |
|---|---|
| `mkxrefs.py` | scans `.text` for `adrp`/`add` pairs and writes `xrefs.pkl`, a map of rodata string address to the code sites that load it |
| `sxref.py` | lookup in that map: `sxref.py "<string>"` prints the string address and every referrer |
| `xref.py` | BL/B scanner: `xref.py <hex target...>` lists call sites of an address |
| `xr.py` | disassembler around a site: `xr.py d <hex> <count>` |
| `mkbl.py` | writes `blmap.pkl`, a full branch map used for reachability |
| `vtable.py`, `vcall.py`, `slots.py`, `rtti.py`, `prolog.py` | vtable / slot / function-boundary helpers |
| `cmdreg.py` | recovers the console command registry by resolving the name and description arguments passed to the register call |
| `ocr.py` | OCR of a screenshot crop, so the game can be read without image input |

## Probes (Frida)

`session.py` / `session_early.py` / `session_early2.py` drive a probe script against the running game.
The `agent_*.js` files are the probes themselves:

* `agent_moves.js`, `agent_lives*.js`, `agent_boost.js` — confirm the moves, life and booster sites
  (call counts, arguments, resulting values) before patching.
* `agent_cnt.js`, `agent_set232.js`, `genset.py`, `gencnt.py` — enumerate `str w1,[x0,#N]; ret` setters and
  count how often each candidate is hit; this is how the "hot getter" trap was found.
* `agent_gold*.js`, `agent_bal*.js`, `agent_find*.js`, `agent_watch*.js`, `agent_ds.js` — the unresolved
  gold-bar hunt: balance setter/getter candidates, data-source accessors, and memory scans for the HUD text.
* `agent_skip*.js`, `agent_mvcalls.js`, `agent_check2.js` — level-result branch verification.
* `agent_field*.js`, `agent_fields2.js`, `agent_discover.js`, `agent_keys*.js` — object layout dumping.

Read the header comment of a probe before reuse; several are one-off and hard-code an address.

## Notes

* `cmdtable.txt` — semi-automatic command-table recovery (name, register site, description). Noisy: it
  also catches JSON keys, so treat it as candidates, not a list.
* `reg.txt` — the clean subset produced by `tools/cmdreg.py`.

Findings, including what did not work, are written up in [../docs/patches.md](../docs/patches.md) and
[../docs/recreating-the-mods.md](../docs/recreating-the-mods.md).

## Not in git

The pristine and patched libraries, the APKs, the `.idsig` files, the save dumps and the raw screenshots
are all either generated or published as release assets.
