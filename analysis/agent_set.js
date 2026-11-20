const m = Process.findModuleByName("libcandycrushsaga.so");
const guards = [0x360172c, 0x3601734, 0x360173c, 0x3601744, 0x360174c,
                0x3601754, 0x360175c, 0x3601764, 0x360176c, 0x3601774];
let n = 0;
guards.forEach((a, i) => {
  try {
    Interceptor.attach(m.base.add(a), {
      onEnter() {
        if (n++ > 40) return;
        const v = this.context.x8.toUInt32();
        send("guard" + i + " bit0=" + (v & 1));
      },
    });
  } catch (e) {}
});
Interceptor.attach(m.base.add(0x3601974), {
  onEnter() { send("BUILD DebugConsole row"); },
});
send("ready");
