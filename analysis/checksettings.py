import zipfile, sys

z = zipfile.ZipFile(sys.argv[1])
for name in ("assets/res_output/configs/common_live.settings", "assets/res_output/configs/_fiction_default.settings"):
    try:
        d = z.read(name).decode()
    except KeyError:
        print(name, "MISSING")
        continue
    print(name)
    for key in ("UseConsole", "ConsoleMaxLines", "UseStatsView", "HaveDebugRenderer"):
        for line in d.splitlines():
            if key in line:
                print("   ", line.strip())
