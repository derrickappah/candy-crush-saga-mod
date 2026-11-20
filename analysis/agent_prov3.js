const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;
Interceptor.attach(m.base.add(0x288b1bc), {
  onEnter() {
    if (n++ > 3) return;
    let o = ptr(0), vt = ptr(0), t = ptr(0);
    try { o = this.context.x0.add(8).readPointer(); } catch (e) {}
    try { vt = o.readPointer(); } catch (e) {}
    try { t = vt.add(0x38).readPointer(); } catch (e) {}
    send("recObj=" + o + " vtOff=" + (vt.isNull() ? "?" : vt.sub(m.base)) +
         " slot38=" + (t.isNull() ? "?" : t.sub(m.base)) + " flag=" + this.context.w1);
  },
});
send("ready");
