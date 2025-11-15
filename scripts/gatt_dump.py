import os
from whad_utils import connect_fast, _safe_disconnect, _services, _characteristics
TARGET_MAC = os.environ.get("TARGET_MAC","02:80:e1:78:42:d0")
def main():
    c=dev=None
    try:
        c,dev=connect_fast(TARGET_MAC, do_discover=True)
        print("=== GATT dump ===")
        for svc in _services(dev):
            print("SERVICE", getattr(svc,"uuid",None))
            for ch in _characteristics(svc):
                props=getattr(ch,"properties",None)
                tostr=getattr(props,"to_string",lambda: str(props))()
                print("  CHAR", getattr(ch,"uuid",None), "handle=", getattr(ch,"handle","?"), "props=", tostr)
    finally:
        _safe_disconnect(c,dev)
if __name__=="__main__": main()
