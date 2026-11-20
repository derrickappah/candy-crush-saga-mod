const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;
const seen = {};
Interceptor.attach(m.base.add(0x1d593b0), {
  onEnter() {
    if (n++ > 900) return;
    let s = "?";
    try { s = this.context.x1.readCString(44); } catch (e) { return; }
    if (seen[s]) return;
    seen[s] = 1;
    let v = "?";
    try { v = this.context.x2.readS32(); } catch (e) {}
    send(s + " = " + v);
  },
});
send("ready");
