"""
Floating control panel for recording operations.
Always-on-top toolbar with session controls and status.
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPoint
from PyQt5.QtGui import QPalette, QColor


class ControlPanel(QWidget):
    """Compact floating toolbar for recording control."""
    
    start_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    highlight_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize control panel."""
        super().__init__(parent)
        
        # Window flags for always-on-top floating window
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        
        self.setFixedSize(650, 90)
        
        # State
        self.is_recording = False
        self.step_count = 0
        self.elapsed_seconds = 0
        self.drag_position = None
        
        # Timer for session duration
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_timer)
        
        self._setup_ui()
        self._apply_styles()
        self._position_window()
        
        # Set cursor to indicate draggable window
        self.setCursor(Qt.OpenHandCursor)
    
    def _setup_ui(self) -> None:
        """Setup UI components."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(8)
        
        # Top row: status and counters
        top_row = QHBoxLayout()
        
        # Status indicator (colored dot)
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("font-size: 20pt; color: #6B7280;")  # Gray
        top_row.addWidget(self.status_indicator)
        
        # Step counter
        self.step_label = QLabel("Steps: 0")
        self.step_label.setStyleSheet("font-size: 11pt; font-weight: bold;")
        top_row.addWidget(self.step_label)
        
        top_row.addSpacing(15)
        
        # Session timer
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setStyleSheet("font-size: 11pt; font-family: 'Courier New';")
        top_row.addWidget(self.timer_label)
        
        top_row.addStretch()
        
        main_layout.addLayout(top_row)
        
        # Bottom row: control buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(8)
        
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self._on_start)
        button_row.addWidget(self.start_btn)
        
        self.highlight_btn = QPushButton("Highlight")
        self.highlight_btn.clicked.connect(self._on_highlight)
        self.highlight_btn.setEnabled(False)
        button_row.addWidget(self.highlight_btn)
        
        self.stop_btn = QPushButton("Stop & Report (F9)")
        self.stop_btn.clicked.connect(self._on_stop)
        self.stop_btn.setEnabled(False)
        button_row.addWidget(self.stop_btn)
        
        main_layout.addLayout(button_row)
    
    def _apply_styles(self) -> None:
        """Apply custom stylesheet."""
        self.setStyleSheet("""
            QWidget {
                background-color: #1B3A6B;
                border-radius: 8px;
                color: white;
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 9pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton:pressed {
                background-color: #1E40AF;
            }
            QPushButton:disabled {
                background-color: #4B5563;
                color: #9CA3AF;
            }
            QPushButton#stopBtn {
                background-color: #DC2626;
            }
            QPushButton#stopBtn:hover {
                background-color: #B91C1C;
            }
        """)
        
        # Set button object names for specific styling
        self.stop_btn.setObjectName("stopBtn")
    
    def _position_window(self) -> None:
        """Position window in top-right corner of screen."""
        from PyQt5.QtWidgets import QApplication
        
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 20
        y = 20
        self.move(x, y)
    
    def _on_start(self) -> None:
        """Handle start button click."""
        self.start_clicked.emit()
    
    def _on_highlight(self) -> None:
        """Handle highlight button click."""
        self.highlight_clicked.emit()
    
    def _on_stop(self) -> None:
        """Handle stop button click."""
        self.stop_clicked.emit()
    
    def start_recording(self) -> None:
        """Update UI for recording state."""
        self.is_recording = True
        self.elapsed_seconds = 0
        
        # Update status indicator (green)
        self.status_indicator.setStyleSheet("font-size: 20pt; color: #16A34A;")
        
        # Update buttons - Start disabled, others enabled
        self.start_btn.setEnabled(False)
        self.highlight_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        
        # Start timer
        self.timer.start(1000)  # Update every second
    
    def stop_recording(self) -> None:
        """Update UI for stopped state - return to initial state."""
        self.is_recording = False
        
        # Update status indicator (gray)
        self.status_indicator.setStyleSheet("font-size: 20pt; color: #6B7280;")
        
        # Return to initial state - Start enabled, others disabled
        self.start_btn.setEnabled(True)
        self.highlight_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        
        # Stop timer
        self.timer.stop()
    
    def increment_step_count(self) -> None:
        """Increment and update step counter."""
        self.step_count += 1
        self.step_label.setText(f"Steps: {self.step_count}")
    
    def reset_counters(self) -> None:
        """Reset step count and timer."""
        self.step_count = 0
        self.elapsed_seconds = 0
        self.step_label.setText("Steps: 0")
        self.timer_label.setText("00:00:00")
    
    def _update_timer(self) -> None:
        """Update timer display (called every second)."""
        self.elapsed_seconds += 1
        
        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60
        
        self.timer_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def mousePressEvent(self, event) -> None:
        """Enable window dragging - works in all states (idle, recording, paused)."""
        if event.button() == Qt.LeftButton:
            # Record the offset from window top-left to click position
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            # Change cursor to closed hand to indicate dragging
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
        else:
            event.ignore()
    
    def mouseMoveEvent(self, event) -> None:
        """Handle window dragging - smooth movement across screens."""
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            # Move window to new position, maintaining the offset
            self.move(event.globalPos() - self.drag_position)
            event.accept()
        else:
            event.ignore()
    
    def mouseReleaseEvent(self, event) -> None:
        """Complete window dragging."""
        if event.button() == Qt.LeftButton:
            # Reset drag position
            self.drag_position = None
            # Change cursor back to open hand
            self.setCursor(Qt.OpenHandCursor)
            event.accept()
        else:
            event.ignore()
