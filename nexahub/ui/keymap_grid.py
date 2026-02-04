"""Keymap grid widget for displaying QMK keycodes."""

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QFont
from typing import List, Optional

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.qmk_keycodes import get_keycode_name, shorten_keycode_name


class KeymapGrid(QWidget):
    """Visual grid display of QMK keycodes matching NexaPad layout."""

    # NexaPad physical layout (4x4)
    # Total: 16 keys in matrix

    # Matrix positions in order they appear in EEPROM (Row Major)
    KEY_POSITIONS = [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),  # Row 0
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3),  # Row 1
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),  # Row 2
        (3, 0),
        (3, 1),
        (3, 2),
        (3, 3),  # Row 3
    ]

    # Color coding for different keycode types
    COLORS = {
        "layer": "rgba(74, 144, 217, 160)",  # Blue - layer functions (TO, MO, etc.)
        "basic": "rgba(92, 184, 92, 160)",   # Green - basic keys
        "mod": "rgba(240, 173, 78, 160)",    # Orange - modifiers
        "special": "rgba(217, 83, 79, 160)",  # Red - special functions
        "transparent": "rgba(119, 119, 119, 140)", # Gray - KC_TRNS
        "none": "rgba(51, 51, 51, 140)",      # Dark gray - KC_NO
        "pressed": "rgba(255, 255, 255, 220)", # White - pressed key highlight
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.key_labels: List[QLabel] = []
        self._pressed_keys: set = set()  # Track pressed keys as (row, col) tuples
        self._keycode_colors: dict = {}  # Store original colors for each key index
        self._setup_ui()

    def _setup_ui(self):
        """Setup the keymap grid UI."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

        # Create grid layout
        grid = QGridLayout()
        grid.setSpacing(4)
        grid.setSizeConstraint(QGridLayout.SizeConstraint.SetFixedSize)

        # Create encoder labels (CW/CCW) (Circle)
        self.enc_ccw_label = QLabel("CCW")
        self.enc_ccw_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.enc_ccw_label.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        self.enc_ccw_label.setFixedSize(50, 50)  # Circle size
        self.enc_ccw_label.setStyleSheet(self._get_label_style("#333333", is_circle=True))
        grid.addWidget(self.enc_ccw_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self.enc_cw_label = QLabel("CW")
        self.enc_cw_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.enc_cw_label.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        self.enc_cw_label.setFixedSize(50, 50)  # Circle size
        self.enc_cw_label.setStyleSheet(self._get_label_style("#333333", is_circle=True))
        grid.addWidget(self.enc_cw_label, 0, 3, Qt.AlignmentFlag.AlignCenter)

        # Create labels for each key position
        for idx, (row, col) in enumerate(self.KEY_POSITIONS):
            label = QLabel("-")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
            label.setFixedSize(60, 40)
            
            # Knob is now square, same as others
            label.setStyleSheet(self._get_label_style("#555555", is_circle=False))

            # Add to grid with proper positioning
            if idx == 0:
                # Knob button - center in middle columns
                grid.addWidget(label, 0, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)
            elif idx in (1, 2, 3):
                # Hidden keys - don't add to grid to prevent layout issues
                label.hide()
            else:
                # Other keys - normal positioning
                grid.addWidget(label, row, col, Qt.AlignmentFlag.AlignCenter)

            self.key_labels.append(label)

        layout.addLayout(grid)

        # Set container style
        self.setStyleSheet("""
            KeymapGrid {
                background-color: rgba(40, 40, 40, 160);
                border-radius: 8px;
            }
        """)

    def _get_label_style(
        self, bg_color: str, text_color: str = "#FFFFFF", pressed: bool = False, is_circle: bool = False
    ) -> str:
        """Generate stylesheet for a key label."""
        border = "2px solid #FFFFFF" if pressed else "1px solid rgba(255, 255, 255, 30)"
        border_radius = "25px" if is_circle else "4px"
        return f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border: {border};
                border-radius: {border_radius};
                padding: 2px;
            }}
        """

    def _get_keycode_color(self, keycode: int) -> str:
        """Determine color based on keycode type."""
        if keycode == 0x0000:
            return self.COLORS["none"]
        if keycode == 0x0001:
            return self.COLORS["transparent"]

        # Layer functions (TO, MO, DF, TG, OSL, TT)
        if 0x5200 <= keycode <= 0x52DF:
            return self.COLORS["layer"]

        # Layer-Tap
        if 0x4000 <= keycode <= 0x4FFF:
            return self.COLORS["layer"]

        # Mod-Tap
        if 0x2000 <= keycode <= 0x3FFF:
            return self.COLORS["mod"]

        # Mods
        if 0x0100 <= keycode <= 0x1FFF:
            return self.COLORS["mod"]

        # Special functions (RGB, Audio, etc.)
        if keycode >= 0x7000:
            return self.COLORS["special"]

        # Basic keys
        return self.COLORS["basic"]

    def update_keycodes(self, keycodes: List[int]) -> bool:
        """Update the displayed keycodes.

        Args:
            keycodes: List of 16 keycode values

        Returns:
            bool: True if anything changed, False otherwise
        """
        if len(keycodes) != 16:
            print(f"Warning: Expected 16 keycodes, got {len(keycodes)}")
            return False

        # Check if anything actually changed
        if hasattr(self, "_last_keycodes") and self._last_keycodes == keycodes:
            return False

        self._last_keycodes = list(keycodes)

        for idx, keycode in enumerate(keycodes):
            if idx >= len(self.key_labels):
                break

            label = self.key_labels[idx]

            # Explicitly ignore keys 1, 2, and 3 as requested by the user
            if idx in (1, 2, 3):
                label.hide()
                continue

            label.show()

            # Get keycode name
            name = get_keycode_name(keycode)

            # Shorten for display
            display_name = shorten_keycode_name(name, max_len=8)
            label.setText(display_name)

            # Set color based on keycode type
            color = self._get_keycode_color(keycode)
            self._keycode_colors[idx] = color

            # Check if this key is currently pressed
            key_row = idx // 4
            key_col = idx % 4
            is_pressed = (key_row, key_col) in self._pressed_keys
            # Knob is now square (is_circle=False)
            label.setStyleSheet(self._get_label_style(color, pressed=is_pressed, is_circle=False))

        return True

    def set_key_pressed(self, row: int, col: int, pressed: bool):
        """Set the pressed state of a key.

        Args:
            row: Matrix row (0-3)
            col: Matrix column (0-3)
            pressed: True if pressed, False if released
        """
        # Calculate key index from row/col
        key_idx = row * 4 + col

        if key_idx < 0 or key_idx >= len(self.key_labels):
            return

        # Update pressed keys set
        key_pos = (row, col)
        if pressed:
            self._pressed_keys.add(key_pos)
        else:
            self._pressed_keys.discard(key_pos)

        # Update visual state
        label = self.key_labels[key_idx]

        # Get the original color for this key
        color = self._keycode_colors.get(key_idx, "#555555")
        # Knob is now square (is_circle=False)
        label.setStyleSheet(self._get_label_style(color, pressed=pressed, is_circle=False))

    def update_encoder(self, ccw_keycode: int, cw_keycode: int):
        """Update encoder CCW/CW labels."""
        # CCW
        name = shorten_keycode_name(get_keycode_name(ccw_keycode), 8)
        self.enc_ccw_label.setText(f"CCW\n{name}")
        color = self._get_keycode_color(ccw_keycode)
        self.enc_ccw_label.setStyleSheet(self._get_label_style(color, is_circle=True))

        # CW
        name = shorten_keycode_name(get_keycode_name(cw_keycode), 8)
        self.enc_cw_label.setText(f"CW\n{name}")
        color = self._get_keycode_color(cw_keycode)
        self.enc_cw_label.setStyleSheet(self._get_label_style(color, is_circle=True))

    def clear(self):
        """Clear all key labels."""
        self._pressed_keys.clear()
        self._keycode_colors.clear()
        for label in self.key_labels:
            label.setText("-")
            label.setStyleSheet(self._get_label_style("#555555"))
