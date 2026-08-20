"""
Main application window and controller for TestTrace Recorder.
Manages application workflow, system tray, and component coordination.
"""
import os
import sys
import json
from PyQt5.QtWidgets import (QMainWindow, QSystemTrayIcon, QMenu, QMessageBox,
                             QApplication)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon

from session_model import TestSession, TestStep
from recorder import Recorder
from highlighter import Highlighter
from ui.control_panel import ControlPanel
from ui.session_dialog import SessionDialog
from ui.step_review import StepReviewWindow


class HotkeyThread(QThread):
    """Background thread for keyboard hotkey monitoring."""
    
    capture_hotkey = pyqtSignal()
    stop_hotkey = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize hotkey thread."""
        super().__init__(parent)
        self.running = True
        self.keyboard_module = None
    
    def run(self) -> None:
        """Monitor for hotkeys in background thread."""
        try:
            import keyboard
            self.keyboard_module = keyboard
            
            # Register hotkeys with error handling
            try:
                keyboard.add_hotkey('f8', lambda: self.capture_hotkey.emit())
                keyboard.add_hotkey('f9', lambda: self.stop_hotkey.emit())
                
                # Keep thread alive
                keyboard.wait()
            except Exception as e:
                print(f"Hotkey registration error: {e}")
                print("Hotkeys may not work. You can use buttons on the control panel instead.")
            
        except ImportError as e:
            print(f"Keyboard module not available: {e}")
        except Exception as e:
            print(f"Hotkey thread error: {e}")
    
    def stop(self) -> None:
        """Stop hotkey monitoring."""
        self.running = False
        if self.keyboard_module:
            try:
                self.keyboard_module.unhook_all()
            except Exception as e:
                print(f"Error unhooking keyboard: {e}")
        self.quit()


class MainWindow(QMainWindow):
    """Main application window and controller."""
    
    def __init__(self, base_dir: str = None):
        """
        Initialize main window.
        
        Args:
            base_dir: Base directory for the application (for .exe support)
        """
        super().__init__()
        self.setWindowTitle("TestTrace Recorder")
        self.setGeometry(100, 100, 800, 600)
        
        # Store base directory
        self.base_dir = base_dir or os.path.dirname(os.path.abspath(__file__))
        
        # Load settings
        self.settings_path = os.path.join(self.base_dir, "config", "settings.json")
        self.settings = self._load_settings()
        
        # Initialize components with base_dir
        self.recorder = Recorder(self.settings_path, base_dir=self.base_dir)
        self.control_panel = ControlPanel()
        self.control_panel.main_window = self  # Set reference to main window
        self.highlighter = Highlighter(base_dir=self.base_dir)
        self.current_session: TestSession = None
        self.pending_step: TestStep = None
        
        # Hotkey thread
        self.hotkey_thread = HotkeyThread()
        
        # Setup connections
        self._setup_connections()
        
        # Setup system tray
        self._setup_system_tray()
        
        # Hide main window (we use control panel instead)
        self.hide()
        
        # Show control panel
        self.control_panel.show()
        
        # Start hotkey monitoring with error handling
        try:
            self.hotkey_thread.start()
        except Exception as e:
            print(f"Warning: Could not start hotkey monitoring: {e}")
            print("Hotkeys (F8/F9/F10) may not work. Use control panel buttons instead.")
    
    def _load_settings(self) -> dict:
        """Load application settings."""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        return {
            "output_dir": "./output",
            "tester_name": "",
            "last_module": "Authorization",
            "last_environment": "SIT"
        }
    
    def _save_settings(self) -> None:
        """Save application settings."""
        try:
            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            with open(self.settings_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def _setup_connections(self) -> None:
        """Connect signals and slots."""
        # Control panel signals
        self.control_panel.start_clicked.connect(self._on_start_recording)
        self.control_panel.stop_clicked.connect(self._on_stop_recording)
        self.control_panel.highlight_clicked.connect(self._on_highlight_evidence)
        
        # Recorder signals
        self.recorder.step_captured.connect(self._on_step_captured)
        self.recorder.error_occurred.connect(self._on_recorder_error)
        
        # Highlighter signals
        self.highlighter.confirmed.connect(self._on_step_confirmed)
        self.highlighter.skipped.connect(self._on_step_skipped)
        
        # Hotkey signals
        self.hotkey_thread.capture_hotkey.connect(self._on_manual_capture)
        self.hotkey_thread.stop_hotkey.connect(self._on_stop_recording)
    
    def _setup_system_tray(self) -> None:
        """Setup system tray icon and menu."""
        # Create tray icon
        self.tray_icon = QSystemTrayIcon(self)
        
        # Use default icon (in production, load from assets/icon.ico)
        self.tray_icon.setIcon(self.style().standardIcon(self.style().SP_ComputerIcon))
        
        # Create tray menu
        tray_menu = QMenu()
        
        open_action = tray_menu.addAction("Open Control Panel")
        open_action.triggered.connect(self._show_control_panel)
        
        new_session_action = tray_menu.addAction("New Session")
        new_session_action.triggered.connect(self._on_start_recording)
        
        tray_menu.addSeparator()
        
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(self._on_exit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Tray icon click
        self.tray_icon.activated.connect(self._on_tray_activated)
    
    def _on_tray_activated(self, reason) -> None:
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.Trigger:  # Left click
            self._show_control_panel()
    
    def _show_control_panel(self) -> None:
        """Show and raise control panel."""
        self.control_panel.show()
        self.control_panel.raise_()
        self.control_panel.activateWindow()
    
    @pyqtSlot()
    def _on_start_recording(self) -> None:
        """Handle start recording request."""
        # Ensure control panel is visible before showing dialog
        self.control_panel.setVisible(True)
        self.control_panel.show()
        self.control_panel.raise_()
        self.control_panel.activateWindow()
        
        # Show session setup dialog with control panel as parent
        dialog = SessionDialog(
            self.control_panel,
            default_tester=self.settings.get("tester_name", ""),
            default_module=self.settings.get("last_module", ""),
            default_environment=self.settings.get("last_environment", "")
        )
        
        # Execute dialog and ensure control panel visibility after
        dialog_result = dialog.exec_()
        
        # CRITICAL: Restore control panel visibility immediately after dialog closes
        self.control_panel.setVisible(True)
        self.control_panel.show()
        self.control_panel.raise_()
        self.control_panel.activateWindow()
        
        if dialog_result != SessionDialog.Accepted:
            # Dialog cancelled - control panel already restored above
            return
        
        # Get session from dialog
        self.current_session = dialog.get_session()
        if not self.current_session:
            # Session creation failed - control panel already visible
            return
        
        # Save preferences
        self.settings["tester_name"] = self.current_session.tester_name
        self.settings["last_module"] = self.current_session.module
        self.settings["last_environment"] = self.current_session.environment
        self._save_settings()
        
        # Start recorder
        try:
            recorder_started = self.recorder.start(self.current_session)
        except Exception as e:
            print(f"Recorder start error: {e}")
            recorder_started = False
        
        if recorder_started:
            # Reset and update control panel
            self.control_panel.reset_counters()
            self.control_panel.start_recording()
            
            # Force control panel to be visible and on top
            self.control_panel.setVisible(True)
            self.control_panel.show()
            self.control_panel.raise_()
            self.control_panel.activateWindow()
            self.control_panel.repaint()
            
            # Process pending events to ensure UI updates
            from PyQt5.QtWidgets import QApplication
            QApplication.processEvents()
            
            # Set control panel bounds for click filtering
            self._update_control_panel_bounds()
            
            try:
                self.tray_icon.showMessage(
                    "TestTrace Recorder",
                    f"Recording started: {self.current_session.tc_id}",
                    QSystemTrayIcon.Information,
                    2000
                )
            except Exception as e:
                print(f"Tray notification error: {e}")
        else:
            # Recording failed to start
            QMessageBox.warning(
                self.control_panel,
                "Recording Failed",
                "Failed to start recording. Check console for errors."
            )
            # Control panel visibility already ensured above
    
    @pyqtSlot()
    def _on_stop_recording(self) -> None:
        """Handle stop recording request."""
        if not self.recorder.is_recording:
            return
        
        # Stop recorder and get session
        session = self.recorder.stop()
        self.control_panel.stop_recording()
        
        # DEBUG: Verify session data
        print(f"\n=== STOP RECORDING DEBUG ===")
        print(f"Session from recorder.stop(): {session}")
        print(f"self.current_session: {self.current_session}")
        print(f"Are they the same object? {session is self.current_session}")
        if session:
            print(f"Steps in recorder session: {len(session.steps)}")
            for i, step in enumerate(session.steps):
                print(f"  Step {i+1}: {step.description} - {step.result}")
        if self.current_session:
            print(f"Steps in current_session: {len(self.current_session.steps)}")
            for i, step in enumerate(self.current_session.steps):
                print(f"  Step {i+1}: {step.description} - {step.result}")
        print(f"============================\n")
        
        if not session or not session.steps:
            QMessageBox.information(
                self.control_panel,
                "No Steps Captured",
                "No steps were captured during this session."
            )
            return
        
        # Generate report directly
        try:
            from report_generator import ReportGenerator
            
            # Show progress message
            try:
                self.tray_icon.showMessage(
                    "TestTrace Recorder",
                    "Generating evidence report...",
                    QSystemTrayIcon.Information,
                    2000
                )
            except Exception:
                pass
            
            # Generate report (saves to local output folder by default)
            generator = ReportGenerator(base_dir=self.base_dir)
            output_dir = self.settings.get("output_dir")
            report_path = generator.generate(session, output_dir)
            
            # Verify file was created
            if not os.path.exists(report_path):
                raise Exception(f"Report file was not created at {report_path}")
            
            # Show SUCCESS message box
            QMessageBox.information(
                self.control_panel,
                "Report Generated Successfully",
                f"Evidence report has been generated successfully!\n\n"
                f"Location:\n{os.path.abspath(report_path)}\n\n"
                f"Click OK to view options."
            )
            
            # Show custom completion dialog with multiple options
            self._show_report_completion_dialog(report_path)
            
        except Exception as e:
            QMessageBox.critical(
                self.control_panel,
                "Report Generation Failed",
                f"Failed to generate report:\n{str(e)}"
            )
    
    def _show_report_completion_dialog(self, report_path: str) -> None:
        """Show custom dialog for report completion with Open Document and Open Folder options."""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
        
        dialog = QDialog(self.control_panel)
        dialog.setWindowTitle("Report Generated Successfully")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout(dialog)
        
        # Success message
        success_label = QLabel("✅ Evidence report generated successfully!")
        success_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #16A34A; margin: 10px;")
        layout.addWidget(success_label)
        
        # File path
        path_label = QLabel(f"Location:\n{report_path}")
        path_label.setStyleSheet("font-size: 10pt; margin: 10px; color: #1B2333;")
        path_label.setWordWrap(True)
        layout.addWidget(path_label)
        
        layout.addSpacing(10)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Open Word Document button
        open_doc_btn = QPushButton("📄 Open Word Document")
        open_doc_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        open_doc_btn.clicked.connect(lambda: self._open_report_document(report_path, dialog))
        button_layout.addWidget(open_doc_btn)
        
        # Open Folder button
        open_folder_btn = QPushButton("📁 Open Export Folder")
        open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        open_folder_btn.clicked.connect(lambda: self._open_output_folder(report_path, dialog))
        button_layout.addWidget(open_folder_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # Show dialog and wait for user action
        dialog.exec_()
        
        # After dialog closes, exit the application
        self._cleanup_and_exit()
    
    def _cleanup_and_exit(self) -> None:
        """Clean up resources and exit the application."""
        try:
            # Stop hotkey monitoring
            if hasattr(self, 'hotkey_thread'):
                self.hotkey_thread.stop()
                self.hotkey_thread.wait(1000)  # Wait up to 1 second
            
            # Hide control panel
            self.control_panel.hide()
            
            # Hide tray icon
            if hasattr(self, 'tray_icon'):
                self.tray_icon.hide()
            
            # Close main window
            self.close()
            
            # Quit application
            QApplication.instance().quit()
            
        except Exception as e:
            print(f"Cleanup error: {e}")
            # Force quit even if cleanup fails
            QApplication.instance().quit()
    
    def _open_report_document(self, report_path: str, dialog) -> None:
        """Open the generated Word document and close application."""
        try:
            if sys.platform == 'win32':
                os.startfile(report_path)
            elif sys.platform == 'darwin':
                import subprocess
                subprocess.Popen(['open', report_path])
            else:
                import subprocess
                subprocess.Popen(['xdg-open', report_path])
            
            # Close dialog
            dialog.accept()
            
        except Exception as e:
            QMessageBox.warning(
                dialog,
                "Cannot Open Document",
                f"Failed to open Word document:\n{str(e)}\n\nPlease open it manually from:\n{report_path}"
            )
            # Don't exit on error, let user handle it
    
    def _open_output_folder(self, report_path: str, dialog) -> None:
        """Open the output folder in File Explorer."""
        try:
            output_dir = os.path.dirname(os.path.abspath(report_path))
            
            if sys.platform == 'win32':
                # Use explorer to open folder and select file
                os.system(f'explorer /select,"{report_path}"')
            elif sys.platform == 'darwin':
                import subprocess
                subprocess.Popen(['open', output_dir])
            else:
                import subprocess
                subprocess.Popen(['xdg-open', output_dir])
            
            dialog.accept()
            
        except Exception as e:
            QMessageBox.warning(
                dialog,
                "Cannot Open Folder",
                f"Failed to open output folder:\n{str(e)}"
            )
    
    @pyqtSlot()
    def _on_manual_capture(self) -> None:
        """Handle manual capture hotkey (F8) - NO TOAST."""
        if self.recorder.is_recording:
            self.recorder.manual_capture()
    
    @pyqtSlot()
    def _on_highlight_evidence(self) -> None:
        """Handle highlight evidence button click - ONLY EXPLICIT TRIGGER."""
        if self.recorder.is_recording:
            # PAUSE mouse listener during highlight UI interaction
            self.recorder.pause_listener()
            
            # Trigger highlighter in manual mode
            self.highlighter.show_for_manual_highlight(self.current_session)
    
    @pyqtSlot(TestStep)
    def _on_step_captured(self, step: TestStep) -> None:
        """
        Handle step captured event - show highlighter for annotation.
        ONLY for manual captures (F8) - auto-captures are silent.
        
        Args:
            step: Captured TestStep with screenshot
        """
        # Store pending step
        self.pending_step = step
        
        # Show highlighter for annotation (ONLY for manual F8 captures)
        self.highlighter.show_step(step)
    
    @pyqtSlot(TestStep)
    def _on_step_confirmed(self, step: TestStep) -> None:
        """
        Handle step annotation confirmed.
        
        Args:
            step: Annotated TestStep
        """
        # Add step to session
        if self.current_session:
            self.current_session.add_step(step)
            self.control_panel.increment_step_count()
        
        self.pending_step = None
        
        # RESUME mouse listener after highlight action completes
        self.recorder.resume_listener()
        
        # Ensure control panel stays visible and active after highlighting
        # Use QTimer to delay slightly so dialog can close first
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, self._restore_control_panel_visibility)
    
    def _restore_control_panel_visibility(self) -> None:
        """Restore control panel visibility with multiple techniques."""
        self.control_panel.setVisible(True)
        self.control_panel.show()
        self.control_panel.raise_()
        self.control_panel.activateWindow()
        self.control_panel.repaint()
        
        # Process events to ensure UI updates
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        
        # Update control panel bounds in case it moved
        self._update_control_panel_bounds()
    
    def _update_control_panel_bounds(self) -> None:
        """Update the control panel bounding box in the recorder for click filtering."""
        try:
            geometry = self.control_panel.geometry()
            self.recorder.set_control_panel_rect(
                geometry.x(),
                geometry.y(),
                geometry.width(),
                geometry.height()
            )
        except Exception as e:
            print(f"Failed to update control panel bounds: {e}")
    
    @pyqtSlot()
    def _on_step_skipped(self) -> None:
        """Handle step annotation skipped."""
        self.pending_step = None
        
        # RESUME mouse listener after highlight action is cancelled
        self.recorder.resume_listener()
        
        # Ensure control panel stays visible after skipping
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, self._restore_control_panel_visibility)
    
    @pyqtSlot(str)
    def _on_recorder_error(self, error_msg: str) -> None:
        """
        Handle recorder error.
        
        Args:
            error_msg: Error message
        """
        self.tray_icon.showMessage(
            "TestTrace Recorder - Error",
            error_msg,
            QSystemTrayIcon.Warning,
            3000
        )
    
    @pyqtSlot(str)
    def _on_report_generated(self, report_path: str) -> None:
        """
        Handle report generation complete.
        
        Args:
            report_path: Path to generated report
        """
        # Show notification
        self.tray_icon.showMessage(
            "Report Generated",
            f"Evidence report saved successfully!",
            QSystemTrayIcon.Information,
            2000
        )
        
        # Open output folder
        try:
            import subprocess
            output_dir = os.path.dirname(report_path)
            if sys.platform == 'win32':
                os.startfile(output_dir)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', output_dir])
            else:
                subprocess.Popen(['xdg-open', output_dir])
        except Exception as e:
            print(f"Failed to open output folder: {e}")
    
    def _on_exit(self) -> None:
        """Handle application exit."""
        # Confirm if recording
        if self.recorder.is_recording:
            reply = QMessageBox.question(
                self.control_panel,
                "Recording in Progress",
                "Recording is in progress. Are you sure you want to exit?\n\n"
                "All unsaved data will be lost.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
        
        # Stop components
        self.recorder.stop()
        self.hotkey_thread.stop()
        
        # Quit application
        QApplication.quit()
    
    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Just hide the window, don't exit
        event.ignore()
        self.hide()
