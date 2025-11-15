import time
from typing import Optional, Iterable, Any, Tuple
from whad.device import WhadDevice
from whad.ble import Central
from whad.ble.profile.attribute import UUID
from whad.ble.exceptions import ConnectionLostException
try:
    from whad.exceptions import WhadDeviceTimeout
except Exception:
    class WhadDeviceTimeout(Exception): ...
try:
    from whad.ble.stack.gatt.exceptions import GattTimeoutException
except Exception:
    class GattTimeoutException(Exception): ...
HCI_IFACE = "uart0"
ADDR_IS_RANDOM = False
TIMEOUT_S = 45.0
POST_CONNECT_WAIT = 0.5
RAPID_BACKOFF_SEQ = [0.05,0.08,0.10,0.12,0.15,0.20]
RETRIES = 50
def _central(): return Central(WhadDevice.create(HCI_IFACE))
def _safe_disconnect(c: Optional[Central], dev=None):
    try:
        if c and dev: c.disconnect(dev)
    except Exception: ...
    try:
        if c: c.stop()
    except Exception: ...
def _services(dev: Any):
    try: return dev.services()
    except Exception: return []
def _characteristics(svc: Any):
    try: return svc.characteristics()
    except Exception: return []
def connect_fast(target_mac: str, do_discover: bool = False):
    last_err=None
    for _ in range(RETRIES):
        c=dev=None
        try:
            c=_central()
            dev=c.connect(target_mac, timeout=TIMEOUT_S, random=ADDR_IS_RANDOM)
            if POST_CONNECT_WAIT>0: time.sleep(POST_CONNECT_WAIT)
            if do_discover:
                try: dev.discover(include_values=False)
                except Exception: ...
            return c,dev
        except Exception as e:
            last_err=e
        finally:
            if dev or c: _safe_disconnect(c,dev)
        time.sleep(0.1)
    raise last_err if last_err else RuntimeError("connect failed")
def resolve_write_handle(dev, chat_service_uuid: str, write_char_uuid: str):
    try:
        ch = dev.find_characteristic_by_uuid(UUID(write_char_uuid))
        if ch and getattr(ch,"handle",None): return ch.handle
    except Exception: ...
    return None
def enable_notifications(dev, notify_char_uuid: str):
    try: ch = dev.find_characteristic_by_uuid(UUID(notify_char_uuid))
    except Exception: ch=None
    if not ch: return None
    try:
        for d in ch.descriptors():
            u=str(getattr(d,"uuid","")).lower()
            if u in ("2902","0x2902","00002902-0000-1000-8000-00805f9b34fb"):
                dev.write_descriptor(d.handle, b"\x01\x00")
                return d.handle
    except Exception: ...
    return None
