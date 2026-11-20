const m = Process.findModuleByName("libcandycrushsaga.so");
const KEY = m.base.add(0x9516f7);
let n = 0;

Interceptor.attach(m.base.add(0x1d593b0), {
  onEnter() {
    const k = this.context.x1;
    if (!k || k.isNull() || !k.equals(KEY)) return;
    if (n++ > 8) return;
    let v = null;
    try { v = this.context.x2.readS32(); } catch (e) { v = "E"; }
    send("Boosters.Count val=" + v + " ds=" + this.context.x0);
    const bt = Thread.backtrace(this.context, Backtracer.ACCURATE)
      .map((a) => a.sub(m.base).toString()).join(" ");
    send("bt " + bt);
    const ap = Thread.backtrace(this.context, Backtracer.FUZZY)
      .map((a) => a.sub(m.base).toString()).join(" ");
    send("fz " + ap);
  },
});
send("ready");
