const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;

function log(tag, self) {
  if (!self || self.isNull()) return;
  const vt = self.readPointer();
  const fn = vt.add(0x30).readPointer();
  let v = "?";
  try { v = new NativeFunction(fn, "int", ["pointer"])(self); } catch (e) { v = "E:" + e; }
  send(tag + " obj=" + self + " vt=" + vt + " fn30=" + fn + " ret=" + v);
}

Interceptor.attach(m.base.add(0x1f2629c), {
  onEnter() {
    if (n++ > 6) return;
    const c = this.context.x0;
    let sub = null;
    try { sub = c.add(0x10).readPointer(); } catch (e) {}
    send("GetLives ctrl=" + c + " sub=" + sub);
    log(" sub30", sub);
  },
});

Interceptor.attach(m.base.add(0x1f26244), {
  onEnter() {
    if (n > 20) return;
    n++;
    const c = this.context.x0;
    let sub = null;
    try { sub = c.add(8).readPointer(); } catch (e) {}
    send("GetNext ctrl=" + c + " sub=" + sub);
    log(" sub38", sub);
  },
});
send("ready");
