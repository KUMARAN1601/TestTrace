"""
Session setup dialog for capturing test case metadata before recording.
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                             QPushButton, QHBoxLayout, QLabel, QMessageBox)
from PyQt5.QtCore import Qt

from session_model import TestSession


class SessionDialog(QDialog):
    """Dialog for setting up a new test session."""
    
    def __init__(self, parent=None, default_tester="", default_module="",
                 default_environment=""):
        """
        Initialize session dialog.
        
        Args:
            parent: Parent widget
            default_tester: Default tester name from settings
            default_module: Default module from settings
            default_environment: Default environment from settings
        """
        super().__init__(parent)
        self.setWindowTitle("New Test Session Setup")
        self.setModal(True)
        self.setMinimumWidth(600)
        
        self.session: TestSession = None
        self.default_tester = default_tester
        self.default_module = default_module
        self.default_environment = default_environment
        
        self._setup_ui()
        self._apply_styles()
    
    def _setup_ui(self) -> None:
        """Setup dialog UI components."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # Title
        title = QLabel("Test Session Setup")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2563EB;")
        main_layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Enter test case details below. Fields marked with * are required."
        )
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # Test Case ID *
        self.tc_id_input = QLineEdit()
        self.tc_id_input.setPlaceholderText("e.g., TC_VISA_AUTH_001")
        form_layout.addRow("Test Case ID: *", self.tc_id_input)
        
        # Test Case Name *
        self.tc_name_input = QLineEdit()
        self.tc_name_input.setPlaceholderText("e.g., VISA Authorization - Approval Flow")
        form_layout.addRow("Test Case Name: *", self.tc_name_input)
        
        # Module / Feature * (Changed to text input)
        self.module_input = QLineEdit()
        self.module_input.setPlaceholderText("e.g., Authorization, Settlement, Dispute")
        if self.default_module:
            self.module_input.setText(self.default_module)
        form_layout.addRow("Module / Feature: *", self.module_input)
        
        # Environment * (Changed to text input)
        self.environment_input = QLineEdit()
        self.environment_input.setPlaceholderText("e.g., SIT, UAT, PROD, Dev")
        if self.default_environment:
            self.environment_input.setText(self.default_environment)
        form_layout.addRow("Environment: *", self.environment_input)
        
        # Tester Name *
        self.tester_name_input = QLineEdit()
        self.tester_name_input.setPlaceholderText("e.g., Kumaran")
        if self.default_tester:
            self.tester_name_input.setText(self.default_tester)
        form_layout.addRow("Tester Name: *", self.tester_name_input)
        
        main_layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.ok_button = QPushButton("Start Recording")
        self.ok_button.clicked.connect(self._on_ok)
        button_layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
    
    def _apply_styles(self) -> None:
        """Apply custom stylesheet."""
        self.setStyleSheet("""
            QDialog {
                background-color: #1B2333;
            }
            QLabel {
                color: white;
                font-size: 10pt;
            }
            QLineEdit, QTextEdit {
                background-color: #232D3F;
                color: white;
                border: 1px solid #2563EB;
                border-radius: 4px;
                padding: 8px;
                font-size: 10pt;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #2563EB;
            }
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 10pt;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:pressed {
                background-color: #1E40AF;
            }
        """)
    
    def _on_ok(self) -> None:
        """Validate inputs and create session."""
        # Validate required fields
        errors = []
        
        tc_id = self.tc_id_input.text().strip()
        if not tc_id:
            errors.append("Test Case ID is required")
        
        tc_name = self.tc_name_input.text().strip()
        if not tc_name:
            errors.append("Test Case Name is required")
        
        module = self.module_input.text().strip()
        if not module:
            errors.append("Module / Feature is required")
        
        environment = self.environment_input.text().strip()
        if not environment:
            errors.append("Environment is required")
        
        tester_name = self.tester_name_input.text().strip()
        if not tester_name:
            errors.append("Tester Name is required")
        
        # Show errors if any
        if errors:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please fix the following errors:\n\n" + "\n".join(f"• {e}" for e in errors)
            )
            return
        
        # Create session
        self.session = TestSession(
            tc_id=tc_id,
            tc_name=tc_name,
            module=module,
            environment=environment,
            tester_name=tester_name
        )
        
        self.accept()
    
    def get_session(self) -> TestSession:
        """
        Get the created session.
        
        Returns:
            TestSession instance, or None if dialog was cancelled
        """
        return self.session
