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
        "layer": "#4A90D9",  # Blue - layer functions (TO, MO, etc.)
        "basic": "#5CB85C",  # Green - basic keys
        "mod": "#F0AD4E",  # Orange - modifiers
        "special": "#D9534F",  # Red - special functions
        "transparent": "#777777",  # Gray - KC_TRNS
        "none": "#333333",  # Dark gray - KC_NO
        "pressed": "#FFFFFF",  # White - pressed key highlight
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

        # Create labels for each key position
        for idx, (row, col) in enumerate(self.KEY_POSITIONS):
            label = QLabel("-")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedSize(60, 40)
            label.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
            label.setStyleSheet(self._get_label_style("#555555"))

            # Add to grid with proper positioning
            if row == 0 and col == 0:
                # First key in first row - center it across 4 columns if it was alone
                # But since we have other keys in Row 0 now, let's keep it centered
                # as if it were the only key (matching the physical look)
                grid.addWidget(label, 0, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)
            else:
                # Other keys - normal positioning
                grid.addWidget(label, row, col, Qt.AlignmentFlag.AlignCenter)

            # Hide keys 1, 2, and 3 by default as requested
            if idx in (1, 2, 3):
                label.hide()

            self.key_labels.append(label)

        layout.addLayout(grid)

        # Set container style
        self.setStyleSheet("""
            KeymapGrid {
                background-color: rgba(40, 40, 40, 220);
                border-radius: 8px;
            }
        """)

    def _get_label_style(
        self, bg_color: str, text_color: str = "#FFFFFF", pressed: bool = False
    ) -> str:
        """Generate stylesheet for a key label."""
        border = "2px solid #FFFFFF" if pressed else "1px solid rgba(255, 255, 255, 30)"
        return f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border: {border};
                border-radius: 4px;
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
            label.setStyleSheet(self._get_label_style(color, pressed=is_pressed))

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
        label.setStyleSheet(self._get_label_style(color, pressed=pressed))

    def clear(self):
        """Clear all key labels."""
        self._pressed_keys.clear()
        self._keycode_colors.clear()
        for label in self.key_labels:
            label.setText("-")
            label.setStyleSheet(self._get_label_style("#555555"))
