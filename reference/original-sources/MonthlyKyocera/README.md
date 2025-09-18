# Kyocera Meter Reading Management System

## 🚀 Quick Start

```bash
# Process a single device
python3 scripts/process_device.py W7F3601552

# Process all devices
python3 scripts/process_all.py

# Retrieve archived file
python3 retrieve_archived.py
```

## 📁 Repository Structure

```
MonthlyKyocera/
├── devices/              # Main working directory (organized by model/serial)
├── scripts/              # Processing scripts and agents
├── specs/                # Specifications and planning documents
├── .archive/             # Archived original files with short names
├── device_registry/      # Master device registry and metadata
├── project/              # Project documentation
└── README.md            # This file
```

## 🗄️ Archive System

All original files have been archived with intelligent short naming:
- **E_** = Email files (.eml, .msg)
- **S_** = Scan images (.png, .jpg)
- **D_** = Data files (.csv, .ods)
- **P_** = PDF files
- **T_** = Text files (.txt, .md)

Example: `E_W7F3601552_a3b2c1d4.eml`
- E = Email type
- W7F3601552 = Device serial
- a3b2c1d4 = Unique hash
- .eml = Original extension

## 📊 Device Registry

28 devices tracked across 2 models:
- **TASKalfa 5004i**: 17 devices
- **TASKalfa 5054ci**: 11 devices

## 🔍 File Retrieval

To retrieve an archived file by original name:
```bash
python3 retrieve_archived.py
# Enter search term when prompted
```

## 📈 Processing Status
- ✅ Files archived with mapping (374 files)
- ✅ Device registry created (28 devices)
- ✅ Repository organized by device
- ⏳ Ready for automated processing

## 🤖 Agent Architecture
5 specialized agents for processing:
1. Orchestrator - Coordinates all processing
2. Scan Agent - Processes device screenshots  
3. Email Agent - Handles .eml and .msg files
4. Data Agent - Validates and stores data
5. Report Agent - Generates outputs

## 📚 Documentation
- [Project Status](project/PROJECT_STATUS.md)
- [Device Registry](device_registry/DEVICE_REGISTRY.md)
- [Agent Architecture](project/AGENT_ARCHITECTURE.md)
- [Technical Specs](specs/)