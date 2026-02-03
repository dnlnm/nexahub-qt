from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QAction, QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Signal, Qt


class TrayIcon(QSystemTrayIcon):
    """System tray icon for NexaHub."""

    show_window_requested = Signal()
    quit_requested = Signal()
    overlay_toggle_requested = Signal(bool)
    click_through_toggle_requested = Signal(bool)

    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings = settings_manager

        # Create a simple icon programmatically
        self._create_icon()
        self.setToolTip("NexaHub - QMK Companion")

        # Create context menu
        self._setup_menu()

        # Connect activated signal
        self.activated.connect(self._on_activated)

    def _create_icon(self):
        """Create the tray icon."""
        import os

        # Try to find the icon in resources
        # Assuming structure: nexahub/ui/tray_icon.py -> nexahub/resources/icon.png
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "resources", "icon.png")

        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
        else:
            # Fallback to programmatic icon
            # Create a 64x64 pixmap with a gradient background
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.GlobalColor.transparent)

            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw rounded rectangle background
            painter.setBrush(QColor(52, 152, 219))  # Nice blue color
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(4, 4, 56, 56, 12, 12)

            # Draw "N" text
            painter.setPen(QColor(255, 255, 255))
            font = QFont("Arial", 32, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "N")

            painter.end()

            self.setIcon(QIcon(pixmap))

    def _setup_menu(self):
        """Setup the context menu."""
        menu = QMenu()

        # Show action
        show_action = QAction("Show NexaHub", self)
        show_action.triggered.connect(self.show_window_requested.emit)
        menu.addAction(show_action)

        menu.addSeparator()

        # Overlay toggle action (persistent, synced with settings)
        self.overlay_action = QAction("Show Overlay", self)
        self.overlay_action.setCheckable(True)
        self.overlay_action.setChecked(self.settings.show_overlay)
        self.overlay_action.triggered.connect(self._on_overlay_toggled)
        menu.addAction(self.overlay_action)

        # Click-through toggle action (persistent)
        self.click_through_action = QAction("Click-Through Mode", self)
        self.click_through_action.setCheckable(True)
        self.click_through_action.setChecked(self.settings.click_through_mode)
        self.click_through_action.triggered.connect(self._on_click_through_toggled)
        menu.addAction(self.click_through_action)

        menu.addSeparator()

        # Quit action
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_requested.emit)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

    def set_overlay_checked(self, checked: bool):
        """Update the overlay toggle state without emitting signal."""
        self.overlay_action.setChecked(checked)

    def set_click_through_checked(self, checked: bool):
        """Update the click-through toggle state without emitting signal."""
        self.click_through_action.setChecked(checked)

    def _on_overlay_toggled(self, checked: bool):
        """Handle overlay toggle and persist the setting."""
        self.settings.show_overlay = checked
        self.settings.save_config()
        self.overlay_toggle_requested.emit(checked)

    def _on_click_through_toggled(self, checked: bool):
        """Handle click-through toggle and persist the setting."""
        self.settings.click_through_mode = checked
        self.settings.save_config()
        self.click_through_toggle_requested.emit(checked)

    def _on_activated(self, reason):
        """Handle tray icon activation."""
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.show_window_requested.emit()

    def show_notification(self, title: str, message: str):
        """Show a system notification."""
        self.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 3000)
