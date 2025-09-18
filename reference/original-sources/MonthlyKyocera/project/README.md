# Kyocera Meter Reading Management System

A comprehensive Python-based solution for automating the processing, archival, and management of monthly meter readings from Kyocera office devices.

## Features

- **Web Dashboard**: Astro-powered analytics dashboard with Tailwind CSS and shadcn/ui
- **Terminal UI (TUI)**: Interactive interface for easy navigation and management
- **Automated Processing**: Batch process emails containing meter readings
- **Smart Storage**: DuckDB for long-term archival with fast queries
- **Multiple Formats**: Export to PDF, TXT, Markdown, and YAML
- **File Preservation**: Original .eml files are never deleted, intelligently stored
- **Git Integration**: Smart branch naming with timestamp-based history preservation
- **Analytics & Reporting**: Usage trends, departmental reports, and data visualization

## Prerequisites

### Backend Requirements
- **Python 3.11+** (Windows, Linux, macOS)
- **UV Package Manager** - Fast, reliable Python package management
  ```bash
  # Install UV (one-time setup)
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # or on Windows:
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **Required Python packages (managed by UV):**
  - `fpdf2` - PDF generation
  - `duckdb` - Archive database
  - `textual` or `rich` - Terminal UI
  - `pyyaml` - YAML support
  - `pytest` - Testing framework
  - `fastapi` - REST API framework
  - `uvicorn` - ASGI server

### Web Dashboard Requirements
- **Node.js 18+** and npm/pnpm
- **Astro** with the following integrations:
  - `@astrojs/tailwind` - Tailwind CSS integration
  - `@astrojs/react` - React components for shadcn/ui
  - `tailwindcss` - Utility-first CSS
  - `shadcn/ui` - Modern UI components
  - `recharts` or `chart.js` - Data visualization

- **Folder Structure:**
  - Place all Outlook `.eml` files in the `emails/` folder.
  - Each device has a folder in `devices/`, named as `001_SERIALNUMBER` (for uncategorized) or under the correct model folder.
  - Scripts are in the `scripts/` folder.
  - **Enforced device folder structure:**
    ```
    devices/
      TASKalfa-5004i/
        <SERIAL>/
          <YYYY-MM-DD>/
            <files>
      TASKalfa-5054ci/
        <SERIAL>/
          <YYYY-MM-DD>/
            <files>
    ```
    - All output files and original `.eml` files are placed in the date subfolder for each serial.
    - No extra nesting of model folders is allowed.
    - Use the cleanup script if you ever see repeated model folders or files not in a date subfolder.

## Folder Structure Rules and Best Practices

- Device folders must never be nested inside another model folder (e.g., `devices/TASKalfa-5004i/TASKalfa-5004i/` is invalid).
- All device data must be under `devices/<MODEL>/<SERIAL>/<YYYY-MM-DD>/`.
- If a date cannot be extracted from a file, it will be placed in an `unknown-date` folder. Review these manually and move to the correct date folder if possible.
- The autofix script will aggressively flatten any repeated model folders and attempt to extract dates from file content before using `unknown-date`.
- **Do not manually move device folders into model folders.** Always use the provided scripts to avoid double-nesting or structure errors.
- The app will check and fix the folder structure before and after every run, and will warn you if problems remain.

## Installation

### Setting Up Python Environment with UV
```bash
# 1. Clone the repository
git clone <repository-url>
cd MonthlyKyocera

# 2. Create virtual environment with UV
uv venv

# 3. Activate the environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# 4. Install all dependencies
uv pip install -r requirements.txt

# 5. Install development dependencies (optional)
uv pip install -r requirements-dev.txt
```

## Running the App

### Backend Processing
1. Place all `.eml` files in the `emails/` folder.
2. From the repo root, run:
   ```sh
   uv run python run.py
   ```
   This will:
   - **Autofix the folder structure** (no repeated model folders, no misplaced files)
   - Print the current date
   - Process all `.eml` files (extract, convert, and move to the correct device/model folder)
   - Update device status documentation
   - Archive data to DuckDB

3. Launch the Terminal UI:
   ```sh
   uv run python -m src.tui.meter_tui
   ```

### Web Dashboard
1. Navigate to the web directory:
   ```sh
   cd web
   ```

2. Install dependencies:
   ```sh
   npm install
   # or
   pnpm install
   ```

3. Start the development server:
   ```sh
   npm run dev
   ```

4. Build for production:
   ```sh
   npm run build
   ```

### API Server
Start the FastAPI backend for the web dashboard:
```sh
uv run uvicorn src.api.meter_api:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

## What Happens During Processing

- For each `.eml` file:
  - Extracts device serial from filename, subject, or body (pre- and post-conversion)
  - Recursively finds the correct device folder (even in subfolders)
  - Extracts the plain text body, model, and sent date from the email
  - Generates a PDF and a `.txt` file with the email body
  - Moves the original `.eml`, `.txt`, and `.pdf` into the correct device/date folder in `devices/<MODEL>/<SERIAL>/<YYYY-MM-DD>/`
  - Moves the device folder to the correct model subfolder if a match is found (automatic, never nested)
  - Names all output files as `<email-date>_<model>_<serial>_<current-date>_meter_reading.txt/pdf` (with a unique suffix if needed)
- After processing, the `emails/` folder will be empty (except for the README placeholder).
- Device folders are organized by model if detected (e.g., `devices/TASKalfa-5054ci/`).
- All actions, errors, and file moves are logged in `SUMMARY.md` (auto-archived monthly).
- Device status is updated in `devices/DEVICE_STATUS.md`.

## File Naming Convention
- `<email-date>_<model>_<serial>_<current-date>_meter_reading.txt`
- `<email-date>_<model>_<serial>_<current-date>_meter_reading.pdf`
- Example: `2025-04-23_TASKalfa5054ci_W792300234_2025-04-24_meter_reading.txt`
- If a file with the same name exists, a numeric suffix is added (e.g., `_1`, `_2`, ...)

## Database & Archive

The system uses **DuckDB** for efficient long-term storage and querying of meter readings:
- Database location: `database/meter_readings.duckdb`
- Automatic archival of processed readings
- Fast queries for reporting and analytics
- Backup exports to Markdown and YAML formats

## Git Workflow

This project uses a timestamp-based branch naming strategy:
- **Branch format**: `YYYY-MM-DD-HH-MM-SS-description`
- **Main branch**: Default branch, always preserved
- **History branches**: Each commit creates a timestamped branch for version history
- **No deletion**: Historical branches are never deleted, preserving complete history

Example:
```bash
# Branches created automatically on commit:
2025-09-11-14-30-45-initial-setup
2025-09-11-15-22-10-add-duckdb-support
2025-09-11-16-45-30-implement-tui-interface
```

## Notes
- Original .eml files are preserved in `emails/archive/` after processing
- No manual folder moving is required; all is handled by the scripts
- For advanced PDF conversion or .msg file support, further customization is needed
- Errors and summary of actions are always available in `SUMMARY.md`
- Serial number extraction and verification is performed both before and after conversion for maximum reliability
- Device status tracking in `devices/DEVICE_STATUS.md`

---

