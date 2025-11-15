



```markdown
# BLE CGM-like Attack Lab — Reproducible Traffic Capture
```

```markdown
## Objective

Generate labeled Bluetooth Low Energy (BLE) attack traffic against a CGM-like peripheral, capture packets with a Nordic sniffer + Wireshark, and export PCAP/CSV for downstream ML experiments. The repository includes WHAD-based Python scripts for common attack patterns and a Windows sniffer workflow.
```

### 3\. Bill of materials (BOM)

```markdown
**Hardware:**
* Nordic nRF52840 Dongle (PCA10059) — Wireshark BLE sniffer.
* MakerDiary nRF52840-MDK USB Dongle — BLE attacker on Ubuntu.
* ST NUCLEO-L476RG — target MCU board.
* ST X-NUCLEO-BNRG2A1 (BlueNRG-M2SP) — BLE expansion card for the target.
* 2× quality USB cables (avoid marginal leads); optional powered USB hub.

**Software:**
* Windows 11 + Wireshark 4.x + Nordic nRF Sniffer for BLE (extcap + firmware).
* Ubuntu 22.04/24.04 with Python 3.11 and `whad` (`pip install whad`).

**Ethics:**
* Perform experiments only on devices you own or are authorized to test.
```

### 4\. Repository layout

````markdown

ble-cgm-ble-attack-lab/
├── README.md
├── docs/
│   ├── lab_topology.md
│   ├── hardware_setup_windows_sniffer.md
│   ├── hardware_setup_ubuntu_attacker.md
│   ├── hardware_setup_st_target.md
│   └── img/
├── scripts/
│   ├── whad_utils.py
│   ├── gatt_dump.py
│   ├── write_flood.py
│   ├── long_write_abuse.py
│   ├── read_all_loop.py
│   ├── discovery_loop.py
│   ├── mtu_loop.py
│   ├── connect_churn.py
│   ├── subscribe_notify.py
│   └── subscribe_and_write.py
├── capture/
│   ├── wireshark_profile_notes.md
│   └── tshark_commands.md
└── analysis/
    └── README.md
````


### 5. Lab topology

[Ubuntu laptop] --USB--> [nRF52840-MDK]        (Attacker/Central)

[Windows 11 PC]--USB--> [nRF52840 Dongle]     (Sniffer)

[STM32 NUCLEO-L476RG + X-NUCLEO-BNRG2A1]      (Target/Peripheral)


### 6. Target peripheral — GATT profile (CGM-like)

```markdown

## Target peripheral — GATT profile (CGM-like)

* **Service:** `d973f2e0-b19e-11e2-9e96-0800200c9a66`
* **Notify characteristic:** `d973f2e1-b19e-11e2-9e96-0800200c9a66`
* **Write/WWR characteristic:** `d973f2e2-b19e-11e2-9e96-0800200c9a66`

**Validation:**
```bash
export TARGET_MAC=AA:BB:CC:DD:EE:FF
python3 scripts/gatt_dump.py
# Expect to see the service above and its two characteristics
````

### 7. Sniffer node — Windows 11 + Wireshark

```markdown

1.  Install Wireshark ≥ 4.0.
2.  Install Nordic nRF Sniffer for BLE (extcap + firmware) and flash the nRF52840 Dongle when prompted.
3.  Start Wireshark → select Nordic nRF Sniffer for Bluetooth LE interface.
4.  Use the Sniffer toolbar to follow the target device (by address). If unknown, begin capture and select from device list.
5.  Save captures under `capture/` using a consistent convention: `capture/<YYYYMMDD>_<attack>_<runN>.pcapng`.
````

### 8\. Attacker node — Ubuntu + WHAD

````markdown

**Installation:**
```bash
python3 -m pip install --upgrade pip
pip install whad
````

**Environment setup:**

```bash
export TARGET_MAC="AA:BB:CC:DD:EE:FF"
export CHAT_SERVICE_UUID="d973f2e0-b19e-11e2-9e96-0800200c9a66"
export NOTIFY_CHAR_UUID="d973f2e1-b19e-11e2-9e96-0800200c9a66"
export WRITE_CHAR_UUID="d973f2e2-b19e-11e2-9e96-0800200c9a66"

# 15-minute runs by default
export RUN_DURATION_S=900
```

Ensure your WHAD device interface is `uart0` (the scripts use this logical name). The MakerDiary MDK typically enumerates as `/dev/ttyACM*` and is mapped by WHAD as `uart0` automatically.


```markdown

## Included attack scripts

* `write_flood.py`: High-frequency Write Commands to `f2e2`.
* `long_write_abuse.py`: Uses Write Long/Execute Write procedures.
* `read_all_loop.py`: Reads all discovered attributes repeatedly.
* `discovery_loop.py`: Repeats full service/characteristic discovery.
* `mtu_loop.py`: Repeatedly negotiates different MTU sizes.
* `connect_churn.py`: Rapid connect/disconnect cycles.
* `subscribe_notify.py`: Subscribes to `f2e1` and logs notifications.
* `subscribe_and_write.py`: Subscribes to `f2e1` while writing to `f2e2`.
````
**Example run:**
```bash
export RUN_DURATION_S=900
python3 scripts/write_flood.py
````

### 10. End-to-end experiment procedure

```markdown

## End-to-end experiment procedure

1.  **Layout & RF hygiene:** Ensure nodes are positioned for good signal; check USB cables.
2.  **Target bring-up:** Flash target firmware; verify peripheral advertising.
3.  **Start sniffer capture:** In Wireshark, select the nRF sniffer interface, follow the target MAC, and start the capture. Verify LL, L2CAP, and ATT packets.
4.  **Run attacks:** Execute the desired attack script(s) from the attacker node. A full run might be:
    * `write_flood.py` (15 min)
    * Wait 60 s
    * `read_all_loop.py` (15 min)
    * Wait 60 s
    * `discovery_loop.py` (15 min)
    * Wait 60 s
    * `connect_churn.py` (15 min)
5.  **Save PCAPs:** Stop the sniffer and save the file using the convention (`<YYYYMMDD>_<attack>_<runN>.pcapng`).
````

### 11\. CSV export for ML (tshark)

````markdown
````
```bash
tshark -r capture/2025-11-14_write_flood_run1.pcapng \
  -T fields -E header=y -E separator=, \
  -e frame.time_epoch -e nordic_ble.channel -e btle.access_address \
  -e btatt.opcode -e btatt.handle -e frame.len -e btle.length \
  > capture/2025-11-14_write_flood_run1.csv
````

### 12. Automation (batch runs)

```markdown
````
```bash
export RUN_DURATION_S=900

for s in write_flood.py read_all_loop.py discovery_loop.py connect_churn.py; do
  echo "[*] starting $s at $(date)"
  python3 "scripts/$s"
  echo "[*] finished $s at $(date)"
  sleep 60
done
````


### 13. Troubleshooting

## Troubleshooting

* **No frames in Wireshark:** Ensure the Nordic sniffer interface is selected, not a Wi-Fi/Ethernet adapter. Ensure you are "following" the correct device address.
* **Attacker fails to connect:** Swap the USB cable. Unplug and replug the MDK dongle. Verify WHAD sees `uart0`. Reboot the target peripheral.
* **Low notification rate:** Ensure CCCD is enabled by the client script (`subscribe_notify.py` handles this). Tune `WRITE_SLEEP_S` variables in scripts.
* **Large PCAPs:** Use Wireshark/tshark ring buffers for long captures or capture separate files per attack run.
````
````
### 14\. Data management


Maintain a `capture/manifest.csv` file mapping captures to metadata.
* **Columns:** `timestamp`, `attack`, `run`, `filename`, `duration_s`, `notes`, `firmware_hash`

Record environment variables, target firmware commit hash, node distances, RF obstacles, average RSSI, and observed channel conditions for reproducibility.


### 15\. License & attribution


## License & attribution

This lab guide and scripts are intended for research and education. Use responsibly and within legal/organizational policy boundaries.
