Modded `com.king.candycrushsaga` 1.325.0.1 (versionCode `13250011`), arm64-v8a only, built from a pulled
Play Store APK and re-signed with a debug key.

| | |
|---|---|
| File | `CandyCrushMod-1.325.0.1.apk` |
| Size | 156,201,567 bytes |
| SHA-256 | `1b24ba7c7606df0305e8453fccad3fa3cf2038fce933f0791c2e2ee56725685e` |
| Signer | debug certificate, SHA-256 `7b0d6235…` |
| Tested | Samsung SM-S901W, Android 16 (SDK 36), unrooted |

## Patches

Twelve instruction patches in `lib/arm64-v8a/libcandycrushsaga.so`, plus the console config flags:

* moves counter pinned at **101**
* lives refill on a **1 second** interval
* booster amounts read **99**, unowned boosters become selectable
* every finished level is scored as a **win** — enter a level, tap the top-right exit, and it counts as completed
* console / in-level testing menu / debug view unlocked (console is in the in-level Settings dialog)
* `UseConsole`, `ConsoleMaxLines`, `HaveDebugRenderer`, `UseStatsView` in the two live settings assets

Full table with the original bytes: [`docs/patches.md`](https://github.com/derrickappah/candy-crush-saga-mod/blob/master/docs/patches.md).
How each one is recreated: [`docs/recreating-the-mods.md`](https://github.com/derrickappah/candy-crush-saga-mod/blob/master/docs/recreating-the-mods.md).

## Install

The APK is signed with a debug key, so it cannot go over the Play Store build:

```sh
adb uninstall com.king.candycrushsaga     # local progress is lost, the King account restores it
adb install --no-incremental -r -d CandyCrushMod-1.325.0.1.apk
```

`--no-incremental` matters; an incremental install leaves a half-materialised app if the adb host drops.

Verify the download first:

```sh
sha256sum -c SHA256SUMS.txt
```

## Notes

* Gold bars are **not** modded. The economy is server-authoritative; the obvious getters are either dormant
  or, when forced to a constant, turn the renderer magenta.
* Only arm64-v8a is patched. Other ABIs present in the APK are untouched.
* Play Store updates will not apply while this is installed — pull a new base APK and re-patch.
* Built for personal use; Candy Crush Saga is © King. No game assets are redistributed here.
