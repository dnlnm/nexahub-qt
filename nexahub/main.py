import sys
import os
from typing import Optional

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, Qt, QObject, Signal

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.settings_manager import SettingsManager
from engine.hid_manager import HIDManager
from engine.window_monitor import WindowMonitor
from ui.main_window import MainWindow
from ui.tray_icon import TrayIcon
from ui.overlay_window import OverlayWindow


class HIDSignalBridge(QObject):
    """Bridge to handle HID events in the GUI thread."""

    layer_event = Signal(int)
    keymap_event = Signal(list, object)  # keycodes, encoder_keycodes (tuple)
    key_press_event = Signal(int, int, bool)  # row, col, pressed
    window_event = Signal(str, object)


class NexaHubApp:
    """Main application controller."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Set application icon
        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "resources", "icon.png"
        )
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))

        # Initialize components
        self.settings = SettingsManager()
        self.hid = HIDManager()
        self.window_monitor: Optional[WindowMonitor] = None

        # Initialize UI
        self.main_window = MainWindow(self.settings, self.hid)
        self.tray_icon = TrayIcon(self.settings)
        self.overlay_window = OverlayWindow()

        # Show overlay based on persistent setting and apply click-through mode
        if self.settings.show_overlay:
            self.overlay_window.show()
        self.overlay_window.set_click_through(self.settings.click_through_mode)

        # Current state
        self.current_layer: Optional[int] = None
        self._cached_keycodes: Optional[list] = None

        self._setup_connections()
        self._setup_timers()
        # Setup HID bridge
        self.hid_bridge = HIDSignalBridge()
        self.hid_bridge.layer_event.connect(self._on_layer_event)
        self.hid_bridge.keymap_event.connect(self._on_keymap_event)
        self.hid_bridge.key_press_event.connect(self._on_key_press_event)
        self.hid_bridge.window_event.connect(self._on_window_changed)

        # Register HID callback
        self.hid.register_callback(self._on_hid_data)

        # Connect to device after setting up signals and callbacks
        self._connect_to_device()

    def _setup_connections(self):
        """Setup signal connections."""
        # Tray icon signals
        self.tray_icon.show_window_requested.connect(self._show_main_window)
        self.tray_icon.quit_requested.connect(self._quit)
        self.tray_icon.overlay_toggle_requested.connect(self._on_tray_overlay_toggle)
        self.tray_icon.click_through_toggle_requested.connect(
            self._on_tray_click_through_toggle
        )

        # Main window signals
        self.main_window.settings_changed.connect(self._on_settings_changed)
        self.main_window.quit_requested.connect(self._quit)

    def _setup_timers(self):
        """Setup periodic timers."""
        # Reconnection timer
        self.reconnect_timer = QTimer()
        self.reconnect_timer.timeout.connect(self._check_connection)
        self.reconnect_timer.start(2000)  # Check connection every 2 seconds

        # Window info update timer
        self.window_info_timer = QTimer()
        self.window_info_timer.timeout.connect(self._update_window_info)
        self.window_info_timer.start(500)  # Update window info every 500ms

        # Keymap polling timer
        self.keymap_poll_timer = QTimer()
        self.keymap_poll_timer.timeout.connect(self._poll_keymap)
        self.keymap_poll_timer.start(2000)  # Poll every 2 seconds

    def _check_connection(self):
        """Check if device is still connected and update UI."""
        was_connected = self.hid.connected

        # Try to verify connection by sending a ping command
        if self.hid.connected:
            # Try to get current layer as a ping
            if not self.hid.send_command(0x02):
                # Command failed, device disconnected
                self.hid.connected = False
                self.hid.disconnect()
                print("Device disconnected detected")

        # If not connected, try to reconnect
        if not self.hid.connected:
            if was_connected:
                # Was connected but now disconnected
                self.main_window.update_connection_status(False, "Device disconnected")
                self.tray_icon.show_notification("NexaHub", "Device disconnected")
            # Try to connect
            self._connect_to_device()

    def _connect_to_device(self):
        """Attempt to connect to the QMK device."""
        if not self.hid.connected:
            if self.hid.find_device():
                self.main_window.update_connection_status(True)
                self.tray_icon.show_notification("NexaHub", "Connected to QMK keyboard")
                self._start_window_monitoring()
                self._apply_current_settings()
                # Fetch initial layer immediately to update UI
                self.hid.get_current_layer()
            else:
                # Pass error message to UI
                error_msg = self.hid.last_error[:50] if self.hid.last_error else ""
                self.main_window.update_connection_status(False, error_msg)

    def _update_window_info(self):
        """Update the current window info display."""
        if self.window_monitor:
            window_info = self.window_monitor.get_current_window()
            if window_info:
                process_name, window_title = window_info
                self.main_window.update_window_info(process_name, window_title)

    def _start_window_monitoring(self):
        """Start monitoring active window changes."""
        if self.window_monitor is None:
            # Pass a lambda that emits the signal from the monitor's thread
            self.window_monitor = WindowMonitor(
                lambda p, t: self.hid_bridge.window_event.emit(p, t)
            )

        if not self.window_monitor.running:
            self.window_monitor.start()

    def _on_hid_data(self, data: bytes):
        """Handle raw HID data from device."""
        # Handle Report ID if present (usually 0x00 at start)
        payload = data
        if len(data) > 0 and data[0] == 0x00:
            payload = data[1:]

        # Check for Layer Change Event: [0xFB, 0x01, LayerID]
        if len(payload) > 2 and payload[0] == 0xFB and payload[1] == 0x01:
            layer_id = payload[2]
            self.hid_bridge.layer_event.emit(layer_id)

        # Check for Key Event: [0xFB, 0x02, row, col, pressed]
        if len(payload) > 4 and payload[0] == 0xFB and payload[1] == 0x02:
            row = payload[2]
            col = payload[3]
            pressed = payload[4] == 1
            self.hid_bridge.key_press_event.emit(row, col, pressed)

    def _on_layer_event(self, layer_id: int):
        """Handle layer change event on GUI thread."""
        if self.current_layer != layer_id:
            self.current_layer = layer_id

            # Update overlay if visible
            if self.overlay_window.isVisible():
                self.overlay_window.update_layer(layer_id)
                # Fetch keymap for new layer
                self._poll_keymap()

            # Log/debug
            print(f"Device switched to layer: {layer_id}")

    def _on_keymap_event(self, keycodes: list, encoder_keycodes: tuple):
        """Handle keymap update event on GUI thread."""
        # Update always if we have new data
        self._cached_keycodes = keycodes

        # Update overlay if visible
        if self.overlay_window.isVisible():
            self.overlay_window.update_keymap(keycodes, encoder_keycodes)

    def _on_key_press_event(self, row: int, col: int, pressed: bool):
        """Handle key press/release event on GUI thread."""
        # Update overlay if visible
        if self.overlay_window.isVisible():
            self.overlay_window.update_key_press(row, col, pressed)

    def _poll_keymap(self):
        """Poll keymap from device for current layer."""
        if not self.hid.connected or self.current_layer is None:
            return

        # Fetch keycodes for current layer
        keycodes = self.hid.get_layer_keycodes(self.current_layer)
        encoder_keycodes = self.hid.get_encoder_keycodes(self.current_layer, 0)
        if keycodes:
            self.hid_bridge.keymap_event.emit(keycodes, encoder_keycodes)

    def _on_window_changed(self, process_name: str, window_title: Optional[str]):
        """Handle window change event."""
        if not self.hid.connected:
            return

        # Check if auto switch layer is enabled
        if not self.settings.auto_switch_layer:
            return

        # Find matching layer
        target_layer = self._find_matching_layer(process_name, window_title)

        if target_layer is not None:
            if target_layer != self.current_layer:
                if self.hid.switch_layer(target_layer):
                    self.current_layer = target_layer
                    # Update overlay if visible
                    if self.overlay_window.isVisible():
                        self.overlay_window.update_layer(self.current_layer)
                        # We don't call _poll_keymap() here anymore because the keyboard
                        # will send a Layer Event notification (0xFB 0x01) which
                        # triggers _on_layer_event, ensuring we fetch the keymap
                        # at the right time without HID collisions.

    def _find_matching_layer(
        self, process_name: str, window_title: Optional[str]
    ) -> Optional[int]:
        """Find the matching layer for the current window."""
        mappings = self.settings.get_layer_mappings()

        # Priority 1: Match process + window title (exact, case-sensitive)
        for mapping in mappings:
            if (
                mapping.get("window_title")
                and mapping["process_name"] == process_name
                and mapping["window_title"] == window_title
            ):
                return mapping["layer"]

        # Priority 2: Match process only
        for mapping in mappings:
            if mapping["process_name"] == process_name and not mapping.get(
                "window_title"
            ):
                return mapping["layer"]

        # Priority 3: Default layer
        return self.settings.default_layer

    def _apply_current_settings(self):
        """Apply current settings to the device."""
        if not self.hid.connected:
            return

        # Apply OLED timeout
        timeout_option = self._timeout_to_option(self.settings.oled_timeout)
        self.hid.set_oled_timeout(timeout_option)

    def _timeout_to_option(self, timeout: int) -> int:
        """Convert timeout seconds to option index."""
        if timeout == 10:
            return 0
        elif timeout == 30:
            return 1
        elif timeout == 60:
            return 2
        else:
            return 3  # Never

    def _on_tray_overlay_toggle(self, enabled: bool):
        """Handle overlay toggle from system tray (setting is now persistent)."""
        if enabled:
            self.overlay_window.show()
            if self.current_layer is not None:
                self.overlay_window.update_layer(self.current_layer)
                self._poll_keymap()
        else:
            self.overlay_window.hide()

    def _on_tray_click_through_toggle(self, enabled: bool):
        """Handle click-through toggle from system tray."""
        self.overlay_window.set_click_through(enabled)
        # Show notification to inform user
        mode = "enabled" if enabled else "disabled"
        self.tray_icon.show_notification(
            "NexaHub",
            f"Click-through mode {mode}. {'Mouse events will pass through.' if enabled else 'You can now drag the overlay.'}",
        )

    def _on_settings_changed(self):
        """Handle settings changes."""
        self._apply_current_settings()

        # Apply overlay visibility based on persistent setting
        if self.settings.show_overlay:
            self.overlay_window.show()
            if self.current_layer is not None:
                self.overlay_window.update_layer(self.current_layer)
                # Fetch keymap when showing overlay
                self._poll_keymap()
        else:
            self.overlay_window.hide()

    def _show_main_window(self):
        """Show the main settings window."""
        # On some systems (especially Linux), show() might not restore from minimized state
        if self.main_window.isMinimized():
            self.main_window.showNormal()
        else:
            self.main_window.show()

        self.main_window.raise_()
        self.main_window.activateWindow()

    def _quit(self):
        """Quit the application."""
        if self.window_monitor:
            self.window_monitor.stop()
        self.hid.disconnect()
        self.overlay_window.close()
        self.app.quit()

    def run(self):
        """Run the application."""
        # Show tray icon
        self.tray_icon.show()

        # Show main window on first run
        self._show_main_window()

        return self.app.exec()


def main():
    """Entry point."""
    app = NexaHubApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
