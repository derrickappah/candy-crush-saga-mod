const addr = ptr("0x79ec6c9200");
try {
  send(addr.readCString(0x400).replace(/[\x00-\x08\x0b-\x1f]/g, "."));
} catch (e) {
  send("read err " + e);
}
send("done");
