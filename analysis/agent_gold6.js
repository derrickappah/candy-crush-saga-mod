const m = Process.findModuleByName("libcandycrushsaga.so");
let np = 0, nf = 0;
Interceptor.attach(m.base.add(0x20f5a28), { onEnter() { np++; } });
Interceptor.attach(m.base.add(0x20f5a30), { onEnter() { nf++; } });
setInterval(() => { send("paid=" + np + " free=" + nf); }, 3000);
send("ready");
