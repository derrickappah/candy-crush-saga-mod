const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;

function cstr(p) {
  try { return p.readCString(48); } catch (e) { return "?"; }
}

Interceptor.attach(m.base.add(0x1d593b0), {
  onEnter() {
    if (n++ > 60) return;
    const s = cstr(this.context.x1);
    let v = "?";
    try { v = this.context.x2.readS32(); } catch (e) {}
    send(s + " = " + v);
  },
});
send("ready");
