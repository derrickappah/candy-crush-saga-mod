from elftools.elf.elffile import ELFFile
import sys

PATH = r"C:\Users\DELL\Downloads\candy crach 2\work\ext\lib\arm64-v8a\libcandycrushsaga.so"
with open(PATH, "rb") as f:
    e = ELFFile(f)
    for secname in (".dynsym",):
        sec = e.get_section_by_name(secname)
        names = [s.name for s in sec.iter_symbols()]
        print(secname, len(names))
        ztv = [n for n in names if n.startswith("_ZTV")]
        zti = [n for n in names if n.startswith("_ZTI")]
        zts = [n for n in names if n.startswith("_ZTS")]
        print("  _ZTV:", len(ztv), " _ZTI:", len(zti), " _ZTS:", len(zts))
        for n in ztv[:25]:
            print("   ", n)
        for n in zti[:10]:
            print("   ", n)
