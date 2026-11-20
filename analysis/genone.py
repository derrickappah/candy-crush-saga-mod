import json

orig = {
    0x3B15C38: "001840b9c0035fd6",
    0x2E85924: "001840b9c0035fd6",
    0x48067C0: "001840b9c0035fd6",
    0x3B15D54: "001440b9c0035fd6",
}

TEMPLATE = """const m = Process.findModuleByName("libcandycrushsaga.so");
const orig = %s;
const target = %d;
for (const k in orig) {
  const p = m.base.add(Number(k));
  Memory.protect(p, 8, "rwx");
  p.writeByteArray(orig[k].match(/../g).map((h) => parseInt(h, 16)));
}
send("restored");
const q = m.base.add(target);
Memory.protect(q, 8, "rwx");
q.writeByteArray([0x00, 0x4c, 0x9d, 0x52, 0xc0, 0x03, 0x5f, 0xd6]);
send("patched " + target.toString(16));
send("done");
"""

table = json.dumps({hex(k): v for k, v in orig.items()})
for i, t in enumerate(orig):
    open(rf"C:\Users\DELL\Downloads\candy crach 2\work\agent_one{i}.js", "w").write(
        TEMPLATE % (table, t))
print("ok")
