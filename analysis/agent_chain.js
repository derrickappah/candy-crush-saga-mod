const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;
Interceptor.attach(m.base.add(0x28cacb8), {
  onEnter() {
    if (n++ > 3) return;
    let o = ptr(0), vt = ptr(0), t = ptr(0);
    try { o = this.context.x0.add(0x50).readPointer(); } catch (e) {}
    try { vt = o.readPointer(); } catch (e) {}
    try { t = vt.add(0x10).readPointer(); } catch (e) {}
    let out = "chain vtOff=" + (vt.isNull() ? "?" : vt.sub(m.base)) +
              " targetOff=" + (t.isNull() ? "?" : t.sub(m.base)) + " id=" + this.context.w1;
    try {
      const o2 = o.add(0x50).readPointer();
      const vt2 = o2.readPointer();
      const t2 = vt2.add(0x10).readPointer();
      out += " | l2 vtOff=" + vt2.sub(m.base) + " targetOff=" + t2.sub(m.base);
    } catch (e) {}
    send(out);
  },
});
send("ready");
