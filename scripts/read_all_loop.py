# read_all_loop.py

import os
import time
from whad_utils import connect_fast, _safe_disconnect, _services, _characteristics

TARGET_MAC = os.environ.get("TARGET_MAC", "02:80:e1:78:42:d0")
RUN_DURATION_S = float(os.environ.get("RUN_DURATION_S", "300"))
READ_SLEEP_S = float(os.environ.get("READ_SLEEP_S", "0.0"))
VERBOSE = True


def main():
    t_end = time.time() + RUN_DURATION_S
    total = 0
    c = dev = None
    readable = None
    while time.time() < t_end:
        try:
            if not dev:
                c, dev = connect_fast(TARGET_MAC, do_discover=True)
                readable = []
                for s in _services(dev):
                    for ch in _characteristics(s):
                        props = getattr(ch, "properties", None)
                        sprops = (getattr(props, "to_string", lambda: str(props))() or "").lower()
                        if "read" in sprops:
                            readable.append(ch)
                if not readable:
                    raise RuntimeError("no readable chars")
            for ch in readable:
                try:
                    _ = ch.read()
                    total += 1
                except Exception:
                    raise
                if READ_SLEEP_S:
                    time.sleep(READ_SLEEP_S)
        except Exception as e:
            if VERBOSE:
                print(f"[warn] read_all transient: {e}")
            _safe_disconnect(c, dev)
            c = dev = None
            readable = None
            continue
    print("reads=", total, "duration_s=", RUN_DURATION_S)


if __name__ == "__main__":
    main()
