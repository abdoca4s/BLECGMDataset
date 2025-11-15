import os, time
from whad_utils import connect_fast, resolve_write_handle, _safe_disconnect
TARGET_MAC=os.environ.get("TARGET_MAC","02:80:e1:78:42:d0")
CHAT_SERVICE_UUID=os.environ.get("CHAT_SERVICE_UUID","d973f2e0-b19e-11e2-9e96-0800200c9a66")
WRITE_CHAR_UUID=os.environ.get("WRITE_CHAR_UUID","d973f2e2-b19e-11e2-9e96-0800200c9a66")
RUN_DURATION_S=float(os.environ.get("RUN_DURATION_S","300"))
WRITE_SLEEP_S=float(os.environ.get("WRITE_SLEEP_S","0.0"))
def main():
    t_end=time.time()+RUN_DURATION_S; total=0; c=dev=ch=None; payload=bytes(range(20))
    while time.time()<t_end:
        try:
            if not dev:
                c,dev=connect_fast(TARGET_MAC, do_discover=False)
                h=resolve_write_handle(dev, CHAT_SERVICE_UUID, WRITE_CHAR_UUID)
                if not h: raise RuntimeError("no writable handle")
                ch=dev.find_characteristic_by_handle(h)
            ch.write(payload, with_response=False); total+=1
            if WRITE_SLEEP_S: time.sleep(WRITE_SLEEP_S)
        except Exception:
            _safe_disconnect(c,dev); c=dev=ch=None; continue
    print("writes=", total)
if __name__=="__main__": main()
