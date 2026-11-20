const m = Process.findModuleByName("libcandycrushsaga.so");
const seen = {};
let n = 0;

Interceptor.attach(m.base.add(0x2a031b4), {
  onEnter() {
    if (n++ > 4000) return;
    const lr = this.returnAddress.sub(m.base).toString(16);
    if (seen[lr]) return;
    seen[lr] = 1;
    send("caller " + lr);
  },
});
send("ready");
