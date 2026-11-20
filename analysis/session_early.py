import sys, time, frida

AGENT = sys.argv[1]
dev = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
name = "com.king.candycrushsaga"
s = None
for i in range(600):
    try:
        s = dev.attach(name)
        break
    except Exception:
        time.sleep(0.05)
if s is None:
    print("attach failed")
    sys.exit(1)
print("attached")


def on_msg(m, d):
    if m["type"] == "send":
        print("MSG", m["payload"], flush=True)
    else:
        print("ERR", m.get("stack") or m.get("description"), flush=True)


script = s.create_script(open(AGENT, encoding="utf-8").read())
script.on("message", on_msg)
script.load()
print("loaded", flush=True)
time.sleep(45)
