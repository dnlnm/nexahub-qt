from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QLineEdit,
    QCheckBox,
    QGroupBox,
    QMessageBox,
    QHeaderView,
    QSpinBox,
    QFileDialog,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from typing import Optional, List, Dict, Any


APP_VERSION = "1.0.0"


class MainWindow(QMainWindow):
    """Main settings window for NexaHub."""

    settings_changed = Signal()
    quit_requested = Signal()

    def __init__(self, settings_manager, hid_manager, parent=None):
        super().__init__(parent)
        self.settings = settings_manager
        self.hid = hid_manager

        self.setWindowTitle(f"NexaHub v{APP_VERSION} - QMK Companion")
        self.setMinimumSize(600, 500)

        self._setup_ui()

        # Track last active window for autofill
        self.last_active_process = ""
        self.last_active_title = ""

        self._load_settings()

    def _setup_ui(self):
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)

        # Status bar
        self.status_label = QLabel("Status: Not connected")
        layout.addWidget(self.status_label)

        # Device Settings Group
        device_group = QGroupBox("Device Settings")
        device_layout = QVBoxLayout(device_group)

        # Default layer
        default_layer_layout = QHBoxLayout()
        default_layer_layout.addWidget(QLabel("Default Layer:"))
        self.default_layer_combo = QComboBox()
        self.default_layer_combo.addItems([str(i) for i in range(5)])
        default_layer_layout.addWidget(self.default_layer_combo)
        default_layer_layout.addStretch()
        device_layout.addLayout(default_layer_layout)

        # OLED Timeout
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("OLED Timeout:"))
        self.timeout_combo = QComboBox()
        self.timeout_combo.addItem("10 seconds", 10)
        self.timeout_combo.addItem("30 seconds", 30)
        self.timeout_combo.addItem("60 seconds", 60)
        self.timeout_combo.addItem("Never", 0)
        timeout_layout.addWidget(self.timeout_combo)
        timeout_layout.addStretch()
        device_layout.addLayout(timeout_layout)

        layout.addWidget(device_group)

        # Layer Mappings Group
        mappings_group = QGroupBox("Layer Mappings")
        mappings_layout = QVBoxLayout(mappings_group)

        # Auto switch layer checkbox
        self.auto_switch_layer_checkbox = QCheckBox(
            "Enable automatic layer switching based on active window"
        )
        mappings_layout.addWidget(self.auto_switch_layer_checkbox)

        # Table
        self.mappings_table = QTableWidget()
        self.mappings_table.setColumnCount(3)
        self.mappings_table.setHorizontalHeaderLabels(
            ["Process Name", "Window Title (Optional)", "Layer"]
        )
        self.mappings_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.mappings_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.mappings_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Fixed
        )
        self.mappings_table.setColumnWidth(2, 60)
        self.mappings_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.mappings_table.setAlternatingRowColors(True)
        # Always show scrollbar
        self.mappings_table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        mappings_layout.addWidget(self.mappings_table)

        # Buttons
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Mapping")
        self.add_button.clicked.connect(self._add_mapping)
        button_layout.addWidget(self.add_button)

        self.autofill_button = QPushButton("Autofill from Active Window")
        self.autofill_button.clicked.connect(self._add_active_mapping)
        button_layout.addWidget(self.autofill_button)

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self._remove_mapping)
        button_layout.addWidget(self.remove_button)

        button_layout.addStretch()
        mappings_layout.addLayout(button_layout)

        # Window info display
        self.window_info_label = QLabel("Active: N/A | Title: N/A")
        self.window_info_label.setStyleSheet("color: gray; font-size: 11px;")
        mappings_layout.addWidget(self.window_info_label)

        layout.addWidget(mappings_group)

        # General Settings Group
        general_group = QGroupBox("General Settings")
        general_layout = QVBoxLayout(general_group)

        # Auto-start checkbox
        self.auto_start_checkbox = QCheckBox("Start NexaHub on Windows startup")
        general_layout.addWidget(self.auto_start_checkbox)

        # Minimize to tray checkbox
        self.minimize_checkbox = QCheckBox("Close to system tray")
        general_layout.addWidget(self.minimize_checkbox)

        # Import/Export buttons
        config_buttons_layout = QHBoxLayout()

        self.import_button = QPushButton("Import Config")
        self.import_button.clicked.connect(self._import_settings)
        config_buttons_layout.addWidget(self.import_button)

        self.export_button = QPushButton("Export Config")
        self.export_button.clicked.connect(self._export_settings)
        config_buttons_layout.addWidget(self.export_button)

        general_layout.addLayout(config_buttons_layout)

        layout.addWidget(general_group)





        # Save/Cancel buttons
        action_layout = QHBoxLayout()

        # Version label
        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setStyleSheet("color: #888888; font-size: 10px;")
        action_layout.addWidget(version_label)

        action_layout.addStretch()

        self.save_button = QPushButton("Save")
        self.save_button.setDefault(True)
        self.save_button.clicked.connect(self._save_settings)
        action_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self._cancel_settings)
        action_layout.addWidget(self.cancel_button)

        layout.addLayout(action_layout)

    def _load_settings(self):
        """Load settings into UI."""
        self.auto_start_checkbox.setChecked(self.settings.auto_start)
        self.minimize_checkbox.setChecked(self.settings.minimize_to_tray)
        self.auto_switch_layer_checkbox.setChecked(self.settings.auto_switch_layer)

        # Set default layer
        index = self.default_layer_combo.findText(str(self.settings.default_layer))
        if index >= 0:
            self.default_layer_combo.setCurrentIndex(index)

        # Set OLED timeout
        timeout = self.settings.oled_timeout
        index = self.timeout_combo.findData(timeout)
        if index >= 0:
            self.timeout_combo.setCurrentIndex(index)

        # Load mappings
        self._load_mappings()

    def _load_mappings(self):
        """Load layer mappings into table."""
        mappings = self.settings.get_layer_mappings()
        self.mappings_table.setRowCount(len(mappings))

        for row, mapping in enumerate(mappings):
            # Process name
            process_item = QTableWidgetItem(mapping.get("process_name", ""))
            self.mappings_table.setItem(row, 0, process_item)

            # Window title
            title = mapping.get("window_title", "")
            title_item = QTableWidgetItem(title if title else "")
            self.mappings_table.setItem(row, 1, title_item)

            # Layer
            layer_combo = QComboBox()
            layer_combo.addItems([str(i) for i in range(5)])

            # Center text
            layer_combo.setEditable(True)
            layer_combo.lineEdit().setReadOnly(True)
            layer_combo.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
            for i in range(layer_combo.count()):
                layer_combo.setItemData(
                    i, Qt.AlignmentFlag.AlignCenter, Qt.ItemDataRole.TextAlignmentRole
                )

            current_layer = str(mapping.get("layer", 0))
            index = layer_combo.findText(current_layer)
            if index >= 0:
                layer_combo.setCurrentIndex(index)
            self.mappings_table.setCellWidget(row, 2, layer_combo)

    def _add_mapping(self):
        """Add a new empty layer mapping row."""
        row = self.mappings_table.rowCount()
        self.mappings_table.insertRow(row)

        # Process name (Placeholder)
        process_item = QTableWidgetItem("process.exe")
        self.mappings_table.setItem(row, 0, process_item)

        # Window title (Empty)
        title_item = QTableWidgetItem("")
        self.mappings_table.setItem(row, 1, title_item)

        self._setup_layer_combo(row)

    def _add_active_mapping(self):
        """Add a new layer mapping row using active window info."""
        row = self.mappings_table.rowCount()
        self.mappings_table.insertRow(row)

        # Process name (Autofill)
        process_item = QTableWidgetItem(self.last_active_process)
        self.mappings_table.setItem(row, 0, process_item)

        # Window title (Autofill)
        title_str = self.last_active_title if self.last_active_title else ""
        title_item = QTableWidgetItem(title_str)
        self.mappings_table.setItem(row, 1, title_item)

        self._setup_layer_combo(row)

    def _setup_layer_combo(self, row):
        """Helper to setup the layer combobox for a row."""
        # Layer
        layer_combo = QComboBox()
        layer_combo.addItems([str(i) for i in range(5)])

        # Center text
        layer_combo.setEditable(True)
        layer_combo.lineEdit().setReadOnly(True)
        layer_combo.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        for i in range(layer_combo.count()):
            layer_combo.setItemData(
                i, Qt.AlignmentFlag.AlignCenter, Qt.ItemDataRole.TextAlignmentRole
            )

        self.mappings_table.setCellWidget(row, 2, layer_combo)

    def _remove_mapping(self):
        """Remove selected mapping row."""
        current_row = self.mappings_table.currentRow()
        if current_row >= 0:
            self.mappings_table.removeRow(current_row)

    def _save_settings(self):
        """Save settings from UI."""
        try:
            # General settings
            self.settings.auto_start = self.auto_start_checkbox.isChecked()
            self.settings.minimize_to_tray = self.minimize_checkbox.isChecked()
            self.settings.auto_switch_layer = (
                self.auto_switch_layer_checkbox.isChecked()
            )
            self.settings.default_layer = int(self.default_layer_combo.currentText())
            self.settings.oled_timeout = self.timeout_combo.currentData()

            # Layer mappings
            mappings = []
            for row in range(self.mappings_table.rowCount()):
                process_item = self.mappings_table.item(row, 0)
                title_item = self.mappings_table.item(row, 1)
                layer_widget = self.mappings_table.cellWidget(row, 2)

                if process_item and layer_widget:
                    try:
                        layer = int(layer_widget.currentText())
                        process_name = process_item.text().strip()
                        window_title = title_item.text().strip() if title_item else None

                        if process_name:  # Only add if process name is provided
                            mapping = {
                                "layer": layer,
                                "process_name": process_name,
                                "window_title": window_title if window_title else None,
                            }
                            mappings.append(mapping)
                    except ValueError:
                        continue

            self.settings.config["layer_mappings"] = mappings
            self.settings.save_config()

            # Apply OLED timeout to device
            timeout_option = self._timeout_to_option(self.settings.oled_timeout)
            if self.hid.connected:
                self.hid.set_oled_timeout(timeout_option)

            self.settings_changed.emit()

            QMessageBox.information(self, "Success", "Settings saved successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")

    def _import_settings(self):
        """Import settings from a JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Settings", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                self.settings.import_config(file_path)
                self._load_settings()
                self.settings_changed.emit()
                QMessageBox.information(
                    self, "Success", "Settings imported successfully!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to import settings: {str(e)}"
                )

    def _export_settings(self):
        """Export settings to a JSON file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Settings", "nexahub_config.json", "JSON Files (*.json)"
        )
        if file_path:
            try:
                self.settings.export_config(file_path)
                QMessageBox.information(
                    self, "Success", "Settings exported successfully!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to export settings: {str(e)}"
                )

    def _cancel_settings(self):
        """Reload settings and close."""
        self._load_settings()
        self.hide()

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

    def update_connection_status(self, connected: bool, error_msg: str = ""):
        """Update the connection status label."""
        if connected:
            self.status_label.setText("Status: Connected to device")
            self.status_label.setStyleSheet("color: green;")
        else:
            if error_msg:
                self.status_label.setText(f"Status: Not connected ({error_msg})")
            else:
                self.status_label.setText("Status: Not connected")
            self.status_label.setStyleSheet("color: red;")

    def update_window_info(self, process_name: str, window_title: Optional[str]):
        """Update the current window info display."""
        if hasattr(self, "window_info_label"):
            title_str = window_title if window_title else "N/A"
            self.window_info_label.setText(
                f"Active: {process_name} | Title: {title_str}"
            )

            # Update last active window (ignore self)
            # Check if title contains "NexaHub" or if it matches our window title
            is_self = False
            if window_title and "NexaHub" in window_title:
                is_self = True

            if not is_self:
                self.last_active_process = process_name
                self.last_active_title = window_title

    def closeEvent(self, event):
        """Handle window close event."""
        if self.settings.minimize_to_tray:
            event.ignore()
            self.hide()
        else:
            event.accept()
            self.quit_requested.emit()
