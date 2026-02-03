from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QApplication,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QColor, QPalette, QFont

import sys
import os
import ctypes
from ctypes import wintypes

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.keymap_grid import KeymapGrid

# Win32 API constants
WS_EX_TRANSPARENT = 0x00000020
GWL_EXSTYLE = -20

# Load user32.dll functions (Windows only)
user32 = None
if sys.platform == "win32":
    try:
        user32 = ctypes.windll.user32
        SetWindowLong = user32.SetWindowLongW
        SetWindowLong.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.LONG]
        SetWindowLong.restype = wintypes.LONG

        GetWindowLong = user32.GetWindowLongW
        GetWindowLong.argtypes = [wintypes.HWND, ctypes.c_int]
        GetWindowLong.restype = wintypes.LONG
    except (AttributeError, ImportError):
        user32 = None


class OverlayWindow(QWidget):
    """Always-on-top frameless window to show current layer and keymap."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Window flags for always-on-top, frameless, and no taskbar entry
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        # Enable usage of transparent background
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Prevent the overlay from taking focus when shown
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Initialize UI
        self._setup_ui()

        # Dragging state
        self.dragging = False
        self.offset = QPoint()
        self._click_through_enabled = False

        # Set initial position (top-right corner by default)
        self._set_initial_position()

    def _setup_ui(self):
        """Setup the user interface."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # Note: We don't set SetFixedSize on the top-level layout to prevent
        # Qt from automatically resizing from the top-left. We handle it
        # manually in adjustSize() to maintain the bottom-right anchor.

        # Container widget for styling
        self.container = QWidget()
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            QWidget#container {
                background-color: rgba(30, 30, 30, 200);
                border: 1px solid rgba(100, 100, 100, 150);
                border-radius: 10px;
            }
        """)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(15, 8, 15, 8)
        container_layout.setSpacing(8)
        # Force the container to always shrink/grow to fit its contents
        container_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

        # Label for "LAYER"
        self.title_label = QLabel("LAYER")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 10px;
            font-weight: bold;
            color: #aaaaaa;
            letter-spacing: 1px;
        """)
        container_layout.addWidget(self.title_label)

        # Label for Layer ID
        self.layer_label = QLabel("0")
        self.layer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layer_label.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
        """)
        container_layout.addWidget(self.layer_label)

        # Toggle button for keymap
        self.toggle_keymap_btn = QPushButton("▼ Keymap")
        self.toggle_keymap_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888888;
                font-family: 'Segoe UI', sans-serif;
                font-size: 9px;
                padding: 2px;
            }
            QPushButton:hover {
                color: #aaaaaa;
            }
        """)
        self.toggle_keymap_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_keymap_btn.clicked.connect(self._toggle_keymap)
        container_layout.addWidget(self.toggle_keymap_btn)

        # Keymap grid (initially visible)
        self.keymap_grid = KeymapGrid()
        container_layout.addWidget(self.keymap_grid)

        layout.addWidget(self.container)

        # Resize to fit content
        self.adjustSize()

    def adjustSize(self, anchor=None):
        """Override adjustSize to maintain the bottom-right anchor."""
        if not self.isVisible():
            super().adjustSize()
            return

        # Capture current bottom-right anchor if none provided
        if anchor is None:
            anchor = self.geometry().bottomRight()
        
        # Invalidate layouts to ensure fresh size hints
        if self.layout():
            self.layout().invalidate()
            self.layout().activate()
        if self.container.layout():
            self.container.layout().invalidate()
            self.container.layout().activate()
        
        # Get the required size to fit the container
        target_size = self.layout().sizeHint()
        
        # Use setFixedSize to force the window to shrink and stay that size
        self.setFixedSize(target_size)
        
        # Move back to anchor
        new_geom = self.geometry()
        new_geom.moveBottomRight(anchor)
        self.move(new_geom.topLeft())

    def _toggle_keymap(self):
        """Toggle visibility of keymap grid."""
        # Capture anchor BEFORE visibility change
        anchor = self.geometry().bottomRight()
        
        if self.keymap_grid.isVisible():
            self.keymap_grid.hide()
            self.toggle_keymap_btn.setText("▶ Keymap")
        else:
            self.keymap_grid.show()
            self.toggle_keymap_btn.setText("▼ Keymap")
        
        # Apply resize anchored to the pre-change position
        self.adjustSize(anchor=anchor)

    def update_keymap(self, keycodes: list):
        """Update the displayed keymap."""
        anchor = self.geometry().bottomRight()
        if self.keymap_grid.update_keycodes(keycodes):
            self.adjustSize(anchor=anchor)

    def update_key_press(self, row: int, col: int, pressed: bool):
        """Update the visual state of a key press."""
        self.keymap_grid.set_key_pressed(row, col, pressed)

    def _set_initial_position(self):
        """Set window position to bottom-right of primary screen."""
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            # Position at bottom-right, with some padding
            x = geometry.width() - self.width() - 50
            y = geometry.height() - self.height() - 50
            self.move(x, y)

    def update_layer(self, layer_id: int):
        """Update the displayed layer."""
        if self.layer_label.text() == str(layer_id):
            return
        anchor = self.geometry().bottomRight()
        self.layer_label.setText(str(layer_id))
        self.adjustSize(anchor=anchor)

    def set_click_through(self, enabled: bool):
        """Enable or disable click-through mode using Win32 API.

        When enabled, mouse events pass through to windows below.
        When disabled, the window can be dragged.
        """
        self._click_through_enabled = enabled

        if not user32:
            return

        # Get the native window handle (HWND)
        hwnd = self.winId()

        # Get current extended style
        ex_style = GetWindowLong(hwnd, GWL_EXSTYLE)

        if enabled:
            # Add WS_EX_TRANSPARENT flag to make mouse events pass through
            ex_style |= WS_EX_TRANSPARENT
        else:
            # Remove WS_EX_TRANSPARENT flag
            ex_style &= ~WS_EX_TRANSPARENT

        # Apply the new style
        SetWindowLong(hwnd, GWL_EXSTYLE, ex_style)

    def toggle_click_through(self):
        """Toggle click-through mode on/off."""
        self.set_click_through(not self._click_through_enabled)

    # --- Dragging Logic ---
    def mousePressEvent(self, event):
        if self._click_through_enabled:
            event.ignore()
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.globalPosition().toPoint() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._click_through_enabled:
            event.ignore()
            return
        if self.dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        if self._click_through_enabled:
            event.ignore()
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()
