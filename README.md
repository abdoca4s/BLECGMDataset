# BLE CGM Dataset

A comprehensive dataset for Bluetooth Low Energy (BLE) Continuous Glucose Monitor (CGM) vulnerability research and analysis.

## Overview

This repository contains a dataset generated for studying BLE CGM vulnerabilities, including packet captures, processed data, and the firmware used for simulations. The dataset was created using a controlled experimental setup with various development boards and BLE sniffing equipment.

## Repository Structure

```
BLECGMDataset/
├── firmware/           # Firmware files used in the simulation
├── dataset/
│   ├── pcap/          # Raw packet capture files
│   └── csv/           # Processed data in CSV format
└── README.md          # This file
```

## Hardware Setup

The following hardware components were used to generate this dataset:

### Target Device (CGM Simulation)
- **Nucleo-BNRG2A1**: BLE expansion board
- **ST Board Nucleo-L476RG**: STM32 Nucleo-64 development board with STM32L476RG MCU
- **Firmware**: Sample BLE application from STMicroelectronics Nucleo site

### BLE Sniffer
- **nRF52840-dongle**: Used with sniffer firmware for capturing BLE packets
- **Purpose**: Passive monitoring and packet capture of BLE communication

### Attack Device (TX Attacker)
- **nRF52840-MDK**: Used as a transmitter for attack simulations
- **Purpose**: Active transmission for vulnerability testing

## Setup Instructions

### 1. Target Device Setup (Nucleo Boards)

1. Connect the Nucleo-BNRG2A1 expansion board to the ST Nucleo-L476RG board
2. Download the Sample BLE application from the [STMicroelectronics Nucleo website](https://www.st.com/)
3. Flash the Sample BLE application to the Nucleo-L476RG using STM32CubeProgrammer or similar tools
4. Configure the BLE application to simulate a CGM device

### 2. BLE Sniffer Setup (nRF52840-dongle)

1. Flash the sniffer firmware to the nRF52840-dongle
2. Install nRF Sniffer for Bluetooth LE software
3. Connect the dongle to your workstation
4. Configure Wireshark with the nRF Sniffer plugin
5. Start capturing BLE packets

### 3. Attack Device Setup (nRF52840-MDK)

1. Program the nRF52840-MDK with custom TX attack firmware
2. Configure attack parameters (timing, packet types, etc.)
3. Position the device appropriately for the experimental setup

## Dataset Description

### PCAP Files
- Contains raw BLE packet captures
- Captured using nRF52840-dongle with sniffer firmware
- Includes normal operation and attack scenarios
- Can be analyzed using Wireshark or similar tools

### CSV Files
- Processed and structured data extracted from PCAP files
- Includes timestamps, packet types, RSSI values, and other relevant metrics
- Ready for data analysis and machine learning applications

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/abdoca4s/BLECGMDataset.git
   cd BLECGMDataset
   ```

2. Access the dataset:
   - PCAP files: `dataset/pcap/`
   - CSV files: `dataset/csv/`
   - Firmware: `firmware/`

3. Analyze the data using your preferred tools (Wireshark, Python, R, etc.)

## Research Applications

This dataset can be used for:
- BLE security vulnerability analysis
- CGM device security assessment
- Attack detection and prevention algorithm development
- Machine learning model training for anomaly detection
- Protocol analysis and reverse engineering

## Citation

If you use this dataset in your research, please cite this repository:

```
@misc{blecgmdataset,
  author = {abdoca4s},
  title = {BLE CGM Dataset},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/abdoca4s/BLECGMDataset}
}
```

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Acknowledgments

- STMicroelectronics for the Nucleo development boards and Sample BLE application
- Nordic Semiconductor for nRF52840 development tools
- The BLE security research community