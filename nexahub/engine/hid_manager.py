import time
import threading
from typing import Optional, Callable, List, Dict, Any
from pywinusb import hid


class HIDManager:
    """Manages HID communication with QMK keyboard."""

    # NexaPad VID/PID
    VENDOR_ID = 0x4E4B  # "NK" in hex
    PRODUCT_ID = 0x0001
    USAGE_PAGE = 0xFF60
    USAGE_ID = 0x61

    # VIA Protocol command IDs
    VIA_CMD_GET_KEYMAP_BUFFER = 0x12

    # NexaPad matrix dimensions
    MATRIX_ROWS = 4
    MATRIX_COLS = 4
    NUM_KEYS = 16  # Full 4x4 matrix

    # Vial Protocol
    VIA_CMD_VIAL_PREFIX = 0xFE
    VIAL_CMD_GET_ENCODER = 0x03

    def __init__(self):
        self.device: Optional[hid.HidDevice] = None
        self.connected = False
        self.report_queue: List[bytes] = []
        self.callbacks: List[Callable[[bytes], None]] = []
        self._lock = threading.Lock()
        self.last_error: Optional[str] = None
        self._response_event = threading.Event()
        self._last_response: Optional[bytes] = None

    def find_device(self) -> bool:
        """Find and connect to the QMK keyboard."""
        try:
            self.last_error = None

            # Get all HID devices
            all_devices = hid.HidDeviceFilter().get_devices()

            # Debug: Print all HID devices
            print(
                f"Looking for device with VID={hex(self.VENDOR_ID)}, PID={hex(self.PRODUCT_ID)}"
            )
            device_count = len(all_devices) if all_devices else 0
            print(f"Total HID devices found: {device_count}")

            if not all_devices:
                self.last_error = "No HID devices found"
                print(self.last_error)
                return False

            # Find devices matching VID/PID
            matching_devices = []
            for device in all_devices:
                vid = device.vendor_id
                pid = device.product_id

                print(
                    f"  Found: VID={hex(vid)}, PID={hex(pid)}, Product={device.product_name}"
                )

                if vid == self.VENDOR_ID and pid == self.PRODUCT_ID:
                    matching_devices.append(device)
                    print(f"    -> Matches VID/PID!")

            print(f"Devices matching VID/PID: {len(matching_devices)}")

            # Try each matching device
            for device in matching_devices:
                try:
                    print(f"Trying device: {device.product_name}")

                    # Open device to get capabilities
                    device.open()

                    # Get usage page and usage from hid_caps
                    caps = device.hid_caps
                    if caps:
                        usage_page = caps.usage_page
                        usage = caps.usage
                        print(
                            f"  Opened - UsagePage={hex(usage_page)}, Usage={hex(usage)}"
                        )

                        # Check if this is the Raw HID interface
                        if usage_page == self.USAGE_PAGE and usage == self.USAGE_ID:
                            print(f"  Raw HID interface found! Connecting...")
                            self.device = device
                            if self.device is not None:
                                self.device.set_raw_data_handler(self._on_data_received)
                            self.connected = True
                            print(f"  Successfully connected!")
                            return True
                        else:
                            print(
                                f"  Not Raw HID (expected {hex(self.USAGE_PAGE)}/{hex(self.USAGE_ID)})"
                            )
                            device.close()
                    else:
                        print(f"  No hid_caps available")
                        device.close()

                except Exception as e:
                    print(f"  Error: {e}")
                    try:
                        device.close()
                    except:
                        pass
                    self.last_error = str(e)
                    continue

            self.last_error = (
                f"Found {len(matching_devices)} device(s) but no Raw HID interface"
            )
            print(f"Connection failed: {self.last_error}")
            return False

        except Exception as e:
            self.last_error = f"Exception in find_device: {e}"
            print(f"Connection failed: {self.last_error}")
            return False

    def disconnect(self):
        """Disconnect from the device."""
        if self.device:
            try:
                self.device.close()
            except Exception:
                pass
            self.device = None
            self.connected = False

    def send_command(self, command: int, data: bytes = b"") -> bool:
        """Send a command to the keyboard.

        Command structure: [0xFC][Command][Data...]
        """
        if not self.connected or not self.device:
            return False

        try:
            # Build report: [ReportID][0xFC][Command][Data...][Padding]
            report = bytearray(64)
            report[0] = 0x00  # Report ID
            report[1] = 0xFC  # Magic byte
            report[2] = command

            # Copy data
            for i, byte in enumerate(data[:61]):
                report[3 + i] = byte

            with self._lock:
                self.device.send_output_report(report)
            return True

        except Exception:
            self.connected = False
            return False

    def switch_layer(self, layer: int) -> bool:
        """Switch to a specific layer."""
        return self.send_command(0x01, bytes([layer]))

    def get_current_layer(self) -> Optional[int]:
        """Get the current layer from the keyboard."""
        if self.send_command(0x02):
            # Wait for response (simplified - in production use async)
            time.sleep(0.1)
            # Response would be handled by _on_data_received
            return None
        return None

    def set_oled_timeout(self, timeout_option: int) -> bool:
        """Set OLED timeout (0=10s, 1=30s, 2=60s, 3=never)."""
        return self.send_command(0x03, bytes([timeout_option]))

    def get_oled_timeout(self) -> Optional[int]:
        """Get current OLED timeout setting."""
        if self.send_command(0x04):
            time.sleep(0.1)
            return None
        return None

    def _on_data_received(self, data: bytes):
        """Handle incoming HID reports."""
        # Store response for synchronous calls
        self._last_response = bytes(data)
        self._response_event.set()

        # Notify all registered callbacks
        for callback in self.callbacks:
            try:
                callback(data)
            except Exception:
                pass

    def register_callback(self, callback: Callable[[bytes], None]):
        """Register a callback for incoming data."""
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def unregister_callback(self, callback: Callable[[bytes], None]):
        """Unregister a callback."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def get_keymap_buffer(self, offset: int, size: int) -> Optional[bytes]:
        """Get keymap buffer from device using VIA protocol.

        Uses command 0x12 (id_dynamic_keymap_get_buffer).

        Args:
            offset: Byte offset into keymap buffer
            size: Number of bytes to read (max 28)

        Returns:
            Raw buffer data or None if failed
        """
        if not self.connected or not self.device:
            return None

        try:
            # Build VIA report: [ReportID][Command][offset_high][offset_low][size][padding...]
            report = bytearray(64)
            report[0] = 0x00  # Report ID
            report[1] = self.VIA_CMD_GET_KEYMAP_BUFFER  # Command ID
            report[2] = (offset >> 8) & 0xFF  # Offset high byte
            report[3] = offset & 0xFF  # Offset low byte
            report[4] = size  # Size (max 28)

            with self._lock:
                # Clear any previous response state before sending
                self._response_event.clear()
                self._last_response = None
                self.device.send_output_report(report)

            # Wait for response with timeout, but loop to filter out other reports
            # (like layer change events) that might arrive in the meantime
            start_time = time.time()
            timeout = 0.5
            while time.time() - start_time < timeout:
                remaining = timeout - (time.time() - start_time)
                if remaining > 0 and self._response_event.wait(timeout=remaining):
                    # Check if this response matches our command
                    resp = self._last_response
                    if resp and len(resp) > 1:
                        # Command ID is at index 1 if ReportID is 0x00, otherwise index 0
                        resp_cmd = resp[1] if resp[0] == 0x00 else resp[0]
                        if resp_cmd == self.VIA_CMD_GET_KEYMAP_BUFFER:
                            return resp
                        
                    # Not our response (e.g., it was an 0xFB event), clear and wait again
                    self._response_event.clear()
                else:
                    break

            return None

        except Exception as e:
            print(f"Error getting keymap buffer: {e}")
            self.connected = False
            return None

    def get_layer_keycodes(self, layer: int) -> Optional[List[int]]:
        """Get all keycodes for a specific layer.

        Args:
            layer: Layer number (0-4)

        Returns:
            List of 16 keycode values or None if failed
        """
        if layer < 0 or layer >= 5:
            return None

        # Calculate offset: layer * MATRIX_ROWS * MATRIX_COLS * 2 bytes per keycode
        offset = layer * self.MATRIX_ROWS * self.MATRIX_COLS * 2

        # Read all keycodes for this layer (16 keys * 2 bytes = 32 bytes)
        # Note: VIA buffer limit is 28 bytes per request, so we split it
        keycodes = []
        
        # Split into two requests: 8 keys each (16 bytes each)
        for chunk in [0, 1]:
            chunk_offset = offset + (chunk * 8 * 2)
            response = self.get_keymap_buffer(chunk_offset, 16)
            
            if not response or len(response) < 16:
                return None

            # Data starts at position 5 (if ReportID present) or position 4 (if not)
            data_start = 5 if response[0] == 0x00 else 4

            for i in range(8):
                idx = data_start + (i * 2)
                if idx + 1 < len(response):
                    kc = (response[idx] << 8) | response[idx + 1]
                    keycodes.append(kc)
                else:
                    keycodes.append(0)  # KC_NO

        return keycodes

    def get_encoder_keycodes(self, layer: int, encoder_idx: int) -> Optional[tuple[int, int]]:
        """Get encoder keycodes (CCW, CW) for a specific layer and encoder.

        Args:
            layer: Layer number
            encoder_idx: Encoder index (0-based)

        Returns:
            Tuple of (ccw_keycode, cw_keycode) or None if failed
        """
        if not self.connected or not self.device:
            return None

        try:
            # Build Vial report: [ReportID][VIA_Prefix][Vial_Cmd][Layer][EncoderIdx][padding...]
            report = bytearray(64)
            report[0] = 0x00
            report[1] = self.VIA_CMD_VIAL_PREFIX
            report[2] = self.VIAL_CMD_GET_ENCODER
            report[3] = layer
            report[4] = encoder_idx

            with self._lock:
                self._response_event.clear()
                self._last_response = None
                self.device.send_output_report(report)

            # Wait for response
            start_time = time.time()
            timeout = 0.5
            while time.time() - start_time < timeout:
                remaining = timeout - (time.time() - start_time)
                if remaining > 0 and self._response_event.wait(timeout=remaining):
                    resp = self._last_response
                    # Check for Vial prefix match matches
                    if resp and len(resp) > 3:
                         # Response format: [ReportID][CmdID][CCW_H][CCW_L][CW_H][CW_L]
                         # But wait, Vial firmware writes response directly to msg buffer.
                         # msg[0]... from vial_handle_cmd start at offset 0 of DATA (which is index 1 of report usually? or index 0 if raw?)
                         # hidapi/pywinusb: input reports usually have Report ID at 0.
                         #
                         # vial.c:
                         # case vial_get_encoder:
                         #    msg[0] = ccw >> 8; msg[1] = ccw & 0xFF;
                         #    msg[2] = cw >> 8;  msg[3] = cw & 0xFF;
                         #
                         # The `msg` passed to `vial_handle_cmd` is `data` from `raw_hid_receive`.
                         # command_id is at data[0].
                         # In `raw_hid_receive`:
                         #   vial_handle_cmd(data, length);
                         #   raw_hid_send(data, length);
                         #
                         # The `data` buffer includes the command bytes initially.
                         # When `vial_handle_cmd` returns, `msg` (data) has been modified in place.
                         #
                         # If we send: [0x00, 0xFE, 0x03, Layer, Idx...]
                         # The firmware receives `data` starting at 0xFE.
                         # `msg[0]` is 0xFE. `msg[1]` is 0x03.
                         #
                         # Wait, `vial_handle_cmd` checks `msg[1]`.
                         # `msg[0]` is `id_vial_prefix` (0xFE).
                         #
                         # Inside `vial_get_encoder`:
                         # msg[0] = keycode >> 8 ...
                         # msg[1] = ...
                         #
                         # So it OVERWRITES the 0xFE at the start of the buffer!
                         #
                         # So the response we get back will start with the CCW keycode high byte at index 0 (or index 1 if ReportID is included).
                         
                         # pywinusb usually returns raw data. If ReportID is 0, it might be stripped or present.
                         # In `get_keymap_buffer`, we checked `resp[0] == 0xVIA_CMD`.
                         #
                         # If `vial_get_encoder` overwrites msg[0], then we can't identify the response by command ID easily!
                         # This is a known issue/feature of Vial/QMK raw HID. It's half-duplex essentially.
                         #
                         # However, since we acquire a lock and clear `_response_event`, the first report we get *should* be the response.
                         # But `_on_data_received` could pick up other events (like 0xFB layer changes).
                         # We need to filter.
                         #
                         # Encoder response will NOT start with 0xFB or 0xFC or 0xFE (likely, unless keycode is huge).
                         # But it *could* start with anything.
                         #
                         # Actually, in `vial_handle_cmd`:
                         # `vial_get_keyboard_id` sets msg[0]..3 to version.
                         # `vial_get_encoder` sets msg[0]..3 to keycodes.
                         #
                         # We have to assume if we sent a request, the next non-event packet is our response.
                         # The events start with 0xFB.
                         
                         data_start = 1 if resp[0] == 0x00 else 0
                         # If using 0x00 report ID, the first byte of actual data is at 1.
                         
                         if resp[data_start] == 0xFB: # Event packet
                             self._response_event.clear()
                             continue
                             
                         # Assume it's our response
                         idx = data_start
                         ccw = (resp[idx] << 8) | resp[idx+1]
                         cw = (resp[idx+2] << 8) | resp[idx+3]
                         return (ccw, cw)
                    
                    self._response_event.clear()
                else:
                    break
                    
            return None

        except Exception as e:
            print(f"Error getting encoder keycodes: {e}")
            self.connected = False
            return None
