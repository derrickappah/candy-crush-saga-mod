const m = Process.findModuleByName("libcandycrushsaga.so");
const VT = m.base.add(0x4ddd1b0);
const FN = m.base.add(0x22fafd0);
const call = new NativeFunction(FN, "int", ["pointer", "int"]);
const pat = Memory.alloc(8);
pat.writePointer(VT);
const bytes = new Uint8Array(pat.readByteArray(8));
const hex = Array.from(bytes).map((x) => ("0" + x.toString(16)).slice(-2)).join(" ");

let found = 0;
for (const r of Process.enumerateRanges("rw-")) {
  if (found >= 3) break;
  let hits = [];
  try { hits = Memory.scanSync(r.base, r.size, hex); } catch (e) { continue; }
  for (const h of hits) {
    if (found >= 3) break;
    found++;
    let out = "obj=" + h.address + " :";
    for (const id of [1, 2, 3, 4, 5, 12, 99]) {
      let v = "E";
      try { v = call(h.address, id); } catch (e) { v = "E"; }
      out += " id" + id + "=" + v;
    }
    send(out);
  }
}
send("objects=" + found + " hex=" + hex);
