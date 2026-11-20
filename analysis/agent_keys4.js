const m = Process.findModuleByName("libcandycrushsaga.so");
let n = 0;
Interceptor.attach(m.base.add(0x1d593b0), {
  onEnter() {
    if (n++ > 4000) return;
    let s = "";
    try { s = this.context.x1.readCString(64); } catch (e) { return; }
    let v = "?";
    try { v = this.context.x2.readS32(); } catch (e) {}
    send(v + "\t" + s + "\t" + this.returnAddress.sub(m.base));
  },
});
send("ready");
