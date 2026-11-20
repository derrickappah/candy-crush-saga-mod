const m = Process.findModuleByName("libcandycrushsaga.so");
Interceptor.attach(m.base.add(0x1d593b0), {
  onEnter() {
    let s = "";
    try { s = this.context.x1.readCString(72); } catch (e) { return; }
    if (!s) return;
    if (s.indexOf("Gold") < 0 && s.indexOf("User.") < 0 && s.indexOf("Currency") < 0) return;
    let v = "?";
    try { v = this.context.x2.readS32(); } catch (e) {}
    send(s + " = " + v + " lr=" + this.returnAddress.sub(m.base) + " x0=" + this.context.x0);
  },
});
send("ready");
