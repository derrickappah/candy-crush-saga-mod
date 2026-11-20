import subprocess, sys, time, frida

ADB = r"C:\Users\DELL\AppData\Local\Android\Sdk\platform-tools\adb.exe"
AGENT = sys.argv[1]
dev = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
s = None
for i in range(1200):
    try:
        out = subprocess.check_output([ADB, "shell", "pidof", "com.king.candycrushsaga"], timeout=5).split()
        if out:
            s = dev.attach(int(out[0]))
            print("attached at iter", i, flush=True)
            break
    except Exception:
        pass
    time.sleep(0.05)
if s is None:
    print("attach failed", flush=True)
    sys.exit(1)


def on_msg(m, d):
    if m["type"] == "send":
        print("MSG", m["payload"], flush=True)
    else:
        print("ERR", m.get("stack") or m.get("description"), flush=True)


script = s.create_script(open(AGENT, encoding="utf-8").read())
script.on("message", on_msg)
script.load()
print("loaded", flush=True)
time.sleep(40)
