const m = Process.findModuleByName("libcandycrushsaga.so");
const A = [0x1db9e0c,0x1db9f74,0x1e809b4,0x1e828f0,0x1e829a8,0x220db88,0x248bbdc,
           0x2841de0,0x2880ad0,0x2a01b98,0x3090b90,0x3096f20];
const seen = {};
let n = 0;
A.forEach((a) => {
  try {
    Interceptor.attach(m.base.add(a), {
      onEnter() {
        const k = a.toString(16);
        if (seen[k] || n++ > 60) return;
        seen[k] = 1;
        send("hit " + k + " self=" + this.context.x0);
      },
    });
  } catch (e) {}
});
send("ready " + A.length);
