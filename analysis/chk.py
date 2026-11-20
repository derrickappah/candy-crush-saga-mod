import zipfile

z = zipfile.ZipFile("chk.apk")
d = z.read("assets/res_output/configs/common_live.settings").decode()
print("UseConsole true" if '"UseConsole": true' in d else "orig settings")
dex = [x for x in z.namelist() if x.endswith(".dex")]
print("dex entries:", dex)
data = b"".join(z.read(x) for x in dex)
print("ModLoader in dex:", b"ModLoader" in data)
print("libgadget present:", any("gadget" in n for n in z.namelist()))
man = z.read("AndroidManifest.xml")
print("manifest bytes:", len(man))
