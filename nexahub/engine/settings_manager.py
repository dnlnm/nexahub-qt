import json
import os
import sys
import winreg
from pathlib import Path
from typing import Dict, List, Any


class SettingsManager:
    """Manages application settings persistence."""

    def __init__(self):
        self.config_dir = Path.home() / ".nexahub"
        self.config_file = self.config_dir / "config.json"
        self.config: Dict[str, Any] = {}
        self._load_default_config()
        self._load_config()

        # Sync auto-start with registry
        self._update_registry_startup(self.auto_start)

    def _load_default_config(self):
        """Load default configuration."""
        self.config = {
            "auto_start": True,
            "minimize_to_tray": True,
            "default_layer": 0,
            "oled_timeout": 30,
            "show_overlay": True,
            "auto_switch_layer": True,
            "click_through_mode": False,
            "layer_mappings": [],
        }

    def _load_config(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
            except (json.JSONDecodeError, IOError):
                pass

    def save_config(self):
        """Save configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key: str, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set a configuration value."""
        self.config[key] = value

    def get_layer_mappings(self) -> List[Dict[str, Any]]:
        """Get layer mappings sorted by priority (specific first)."""
        mappings = self.config.get("layer_mappings", [])
        # Sort: window_title present first, then by layer number
        return sorted(
            mappings, key=lambda x: (x.get("window_title") is None, x.get("layer", 0))
        )

    def add_layer_mapping(
        self, layer: int, process_name: str, window_title: str = None
    ):
        """Add a new layer mapping."""
        mapping = {
            "layer": layer,
            "process_name": process_name,
            "window_title": window_title,
        }
        self.config["layer_mappings"].append(mapping)

    def remove_layer_mapping(self, index: int):
        """Remove a layer mapping by index."""
        if 0 <= index < len(self.config["layer_mappings"]):
            del self.config["layer_mappings"][index]

    def _update_registry_startup(self, enable: bool):
        """Update Windows registry for auto-start."""
        # Only run if frozen (compiled app) to avoid registering python interpreter during dev
        if not getattr(sys, "frozen", False) and "__compiled__" not in globals():
            return

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "NexaHub"

        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS
            )

            if enable:
                exe_path = sys.executable
                cmd = f'"{exe_path}"'
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                except FileNotFoundError:
                    pass

            winreg.CloseKey(key)
        except Exception as e:
            print(f"Failed to update registry: {e}")

    @property
    def auto_start(self) -> bool:
        return self.config.get("auto_start", True)

    @auto_start.setter
    def auto_start(self, value: bool):
        self.config["auto_start"] = value
        self._update_registry_startup(value)

    @property
    def minimize_to_tray(self) -> bool:
        return self.config.get("minimize_to_tray", True)

    @minimize_to_tray.setter
    def minimize_to_tray(self, value: bool):
        self.config["minimize_to_tray"] = value

    @property
    def default_layer(self) -> int:
        return self.config.get("default_layer", 0)

    @default_layer.setter
    def default_layer(self, value: int):
        self.config["default_layer"] = value

    @property
    def oled_timeout(self) -> int:
        return self.config.get("oled_timeout", 30)

    @oled_timeout.setter
    def oled_timeout(self, value: int):
        self.config["oled_timeout"] = value

    @property
    def show_overlay(self) -> bool:
        return self.config.get("show_overlay", True)

    @show_overlay.setter
    def show_overlay(self, value: bool):
        self.config["show_overlay"] = value

    @property
    def auto_switch_layer(self) -> bool:
        return self.config.get("auto_switch_layer", True)

    @auto_switch_layer.setter
    def auto_switch_layer(self, value: bool):
        self.config["auto_switch_layer"] = value

    @property
    def click_through_mode(self) -> bool:
        return self.config.get("click_through_mode", False)

    @click_through_mode.setter
    def click_through_mode(self, value: bool):
        self.config["click_through_mode"] = value

    def export_config(self, file_path: str):
        """Export configuration to a file."""
        with open(file_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def import_config(self, file_path: str):
        """Import configuration from a file."""
        with open(file_path, "r") as f:
            new_config = json.load(f)
            # Basic validation could be added here
            self.config = new_config
            self.save_config()  # Save to default location

            # Update registry if auto_start changed
            self._update_registry_startup(self.auto_start)
