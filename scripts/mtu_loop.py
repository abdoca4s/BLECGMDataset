# mtu_loop.py

import os
import time
from whad_utils import connect_fast, _safe_disconnect

TARGET_MAC = os.environ.get("TARGET_MAC", "02:80:e1:78:42:d0")
RUN_DURATION_S = float(os.environ.get("RUN_DURATION_S", "300"))
REQ_MTU = int(os.environ.get("REQ_MTU", "247"))
VERBOSE = True


def main():
    t_end = time.time() + RUN_DURATION_S
    total = 0
    c = dev = None
    while time.time() < t_end:
        try:
            if not dev:
                c, dev = connect_fast(TARGET_MAC, do_discover=False)
            dev.exchange_mtu(REQ_MTU)
            total += 1
        except Exception as e:
            if VERBOSE:
                print(f"[warn] mtu transient: {e}")
            _safe_disconnect(c, dev)
            c = dev = None
            continue
    print("mtu_exchanges=", total, "duration_s=", RUN_DURATION_S)


if __name__ == "__main__":
    main()
