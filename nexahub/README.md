# NexaHub - QMK Macropad Companion App

A Windows companion application for QMK-based macropads that provides automatic layer switching based on active applications, OLED timeout control, and system tray integration.

## Features

- **Automatic Layer Switching**: Change macropad layers based on the active application/window
- **OLED Timeout Control**: Configure display timeout (10s, 30s, 60s, or never)
- **System Tray Integration**: Runs in background with tray icon
- **Simple Configuration**: Easy-to-use table interface for layer mappings
- **Exact Matching**: Case-sensitive matching for process names and window titles

## Installation

1. Download the latest `NexaHub.exe` from releases
2. Run the executable
3. The app will start minimized to system tray
4. Double-click the tray icon to open settings

## Building from Source

### Requirements

- Python 3.10+
- Windows 10/11

### Setup

```bash
cd nexahub
pip install -r requirements.txt
```

### Build

```bash
build.bat
```

The compiled executable will be in `dist/NexaHub.exe`.

## Usage

### Layer Mappings

Configure which layer to activate for specific applications:

1. Open NexaHub settings (double-click tray icon)
2. Click "Add Mapping"
3. Enter:
   - **Layer**: The layer number (0-4)
   - **Process Name**: Exact process name (e.g., `chrome.exe`, `code.exe`)
   - **Window Title** (optional): Exact window title for specific matches
4. Click "Save"

### Priority System

Mappings are matched in priority order:
1. Process name + Window title (most specific)
2. Process name only
3. Default layer (fallback)

### OLED Timeout

Set when the macropad's OLED display should turn off:
- 10 seconds
- 30 seconds (default)
- 60 seconds
- Never (always on)

## QMK Firmware Requirements

Your QMK firmware must support:
- Raw HID (already configured in your keymap)
- Extended HID commands for OLED timeout

The firmware changes are included in the `keymap.c` updates.

## Configuration

Settings are stored in:
```
%USERPROFILE%\.nexahub\config.json
```

## License

MIT License

## Support

For issues and feature requests, please use the GitHub issue tracker.
