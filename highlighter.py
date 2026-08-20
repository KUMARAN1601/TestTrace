"""
Full-screen annotation overlay for captured screenshots.
Allows testers to draw highlight rectangles and add step metadata.
"""
from typing import Optional
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QHBoxLayout, QVBoxLayout, QWidget)
from PyQt5.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage, QFont
from PIL import Image, ImageDraw, ImageGrab
import os
from datetime import datetime

from session_model import TestStep


class HighlightNamingDialog(QDialog):
    """Modal dialog for naming highlighted evidence."""
    
    def __init__(self, parent=None):
        """Initialize naming dialog."""
        super().__init__(parent)
        self.setWindowTitle("Name Highlighted Evidence")
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setModal(True)
        self.setFixedWidth(600)
        
        self.description = ""
        self.result = "Pass"  # Default result
        self.reselect_requested = False
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup UI components."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Instruction label
        instruction = QLabel("Describe what you've highlighted:")
        instruction.setStyleSheet("font-size: 11pt; font-weight: bold;")
        layout.addWidget(instruction)
        
        # Description input
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("e.g., Highlighted Customer Name Field 'John Smith'")
        self.description_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 10pt;
                border: 2px solid #2563EB;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.description_input)
        
        layout.addSpacing(10)
        
        # Result dropdown
        result_row = QHBoxLayout()
        result_label = QLabel("Result:")
        result_label.setStyleSheet("font-size: 10pt; font-weight: bold;")
        result_row.addWidget(result_label)
        
        self.result_combo = QComboBox()
        self.result_combo.addItems(["Pass", "Fail", "Blocked"])
        self.result_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 2px solid #2563EB;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #2563EB;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #2563EB;
                selection-color: white;
            }
        """)
        result_row.addWidget(self.result_combo)
        result_row.addStretch()
        layout.addLayout(result_row)
        
        layout.addSpacing(10)
        
        # Button row
        button_row = QHBoxLayout()
        
        self.reselect_btn = QPushButton("Re-select Area")
        self.reselect_btn.setStyleSheet("""
            QPushButton {
                background-color: #F59E0B;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 10pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D97706;
            }
        """)
        self.reselect_btn.clicked.connect(self._on_reselect)
        button_row.addWidget(self.reselect_btn)
        
        button_row.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 10pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        button_row.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("Save Highlight & Evidence")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #16A34A;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 10pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #15803D;
            }
        """)
        self.save_btn.clicked.connect(self._on_save)
        button_row.addWidget(self.save_btn)
        
        layout.addLayout(button_row)
        
        # Focus on input
        self.description_input.setFocus()
    
    def _on_reselect(self) -> None:
        """Handle re-select button."""
        self.reselect_requested = True
        self.accept()
    
    def _on_save(self) -> None:
        """Handle save button."""
        self.description = self.description_input.text().strip()
        if not self.description:
            self.description_input.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    font-size: 10pt;
                    border: 2px solid #DC2626;
                    border-radius: 6px;
                }
            """)
            self.description_input.setPlaceholderText("Description is required!")
            return
        
        self.result = self.result_combo.currentText()
        self.reselect_requested = False
        self.accept()
    
    def get_result(self):
        """Get dialog result."""
        return {
            "description": self.description,
            "result": self.result,
            "reselect": self.reselect_requested
        }


class Highlighter(QDialog):
    """Full-screen overlay for annotating captured screenshots."""
    
    confirmed = pyqtSignal(TestStep)
    skipped = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize highlighter dialog."""
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint |
            Qt.Dialog
        )
        self.setModal(True)
        
        self.step: Optional[TestStep] = None
        self.screenshot: Optional[Image.Image] = None
        self.pixmap: Optional[QPixmap] = None
        self.manual_mode = False
        self.current_session = None
        
        # Drawing state
        self.is_drawing = False
        self.drawing_locked = False  # Lock after first rectangle drawn
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.highlight_rect = QRect()
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Image display area (handled by paintEvent)
        # Takes up most of the screen
        
        # Bottom control panel (ONLY for F8 captures, hidden for Highlight button)
        self.control_panel = QWidget()
        self.control_panel.setStyleSheet("""
            QWidget {
                background-color: #1B2333;
                border-top: 2px solid #2563EB;
            }
            QLabel {
                color: white;
                font-size: 10pt;
            }
            QLineEdit {
                background-color: #232D3F;
                color: white;
                border: 1px solid #2563EB;
                border-radius: 4px;
                padding: 8px;
                font-size: 10pt;
            }
            QComboBox {
                background-color: #232D3F;
                color: white;
                border: 1px solid #2563EB;
                border-radius: 4px;
                padding: 6px;
                font-size: 10pt;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
            }
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 10pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            QPushButton#skipBtn {
                background-color: #6B7280;
            }
            QPushButton#skipBtn:hover {
                background-color: #4B5563;
            }
        """)
        
        panel_layout = QHBoxLayout(self.control_panel)
        panel_layout.setContentsMargins(20, 15, 20, 15)
        
        # Instructions label
        instructions = QLabel("Draw a rectangle around the important area, then describe the step:")
        panel_layout.addWidget(instructions)
        
        panel_layout.addSpacing(20)
        
        # Step description input
        desc_label = QLabel("Description:")
        panel_layout.addWidget(desc_label)
        
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("e.g., Clicked 'Submit' button")
        self.description_input.setMinimumWidth(300)
        panel_layout.addWidget(self.description_input)
        
        panel_layout.addSpacing(20)
        
        # Result selector
        result_label = QLabel("Result:")
        panel_layout.addWidget(result_label)
        
        self.result_combo = QComboBox()
        self.result_combo.addItems(["Pass", "Fail", "Blocked"])
        self.result_combo.setMinimumWidth(120)
        panel_layout.addWidget(self.result_combo)
        
        panel_layout.addStretch()
        
        # Action buttons
        self.confirm_btn = QPushButton("Confirm")
        self.confirm_btn.clicked.connect(self._on_confirm)
        panel_layout.addWidget(self.confirm_btn)
        
        self.skip_btn = QPushButton("Skip")
        self.skip_btn.setObjectName("skipBtn")
        self.skip_btn.clicked.connect(self._on_skip)
        panel_layout.addWidget(self.skip_btn)
        
        # Add control panel to main layout (at bottom)
        main_layout.addStretch()
        main_layout.addWidget(self.control_panel)
    
    def show_for_manual_highlight(self, session) -> None:
        """
        Show highlighter in manual mode - captures screen and allows highlighting.
        ONLY TRIGGERED BY EXPLICIT "Highlight" BUTTON CLICK.
        Uses center popup dialog ONLY (no bottom toolbar).
        
        Args:
            session: Current TestSession to add the step to
        """
        self.manual_mode = True
        self.current_session = session
        
        try:
            # Capture the current screen
            self.screenshot = ImageGrab.grab()
            
            # Convert to QPixmap
            self._update_pixmap()
            
            # Reset state - IMPORTANT: Unlock drawing for new highlight
            self.highlight_rect = QRect()
            self.start_point = QPoint()
            self.end_point = QPoint()
            self.is_drawing = False
            self.drawing_locked = False  # Allow drawing of ONE rectangle
            
            # HIDE bottom control panel - use center dialog only
            self.control_panel.hide()
            
            # Show fullscreen using show() + window state instead of showFullScreen()
            self.setWindowState(Qt.WindowFullScreen)
            self.show()
            self.raise_()
            self.activateWindow()
            
        except Exception as e:
            print(f"Manual highlight error: {e}")
            import traceback
            traceback.print_exc()
    
    def _save_manual_highlight(self, description: str, result: str = "Pass") -> None:
        """Save the manually highlighted evidence as a test step."""
        if not self.current_session or not self.screenshot:
            return
        
        try:
            # Create new step number
            step_number = len(self.current_session.steps) + 1
            
            # Create temp session directory
            session_dir = f"./temp_sessions/session_{self.current_session.session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(session_dir, exist_ok=True)
            
            # Save original screenshot
            screenshot_path = os.path.join(session_dir, f"step_{step_number:03d}.png")
            self.screenshot.save(screenshot_path)
            
            # Create annotated version with highlight
            annotated = self.screenshot.copy()
            draw = ImageDraw.Draw(annotated, 'RGBA')
            
            x = self.highlight_rect.x()
            y = self.highlight_rect.y()
            w = self.highlight_rect.width()
            h = self.highlight_rect.height()
            
            rect_coords = [x, y, x + w, y + h]
            
            # Fill
            fill_color = (255, 0, 0, int(255 * 0.2))
            draw.rectangle(rect_coords, fill=fill_color, outline=None)
            
            # Outline
            outline_color = (255, 0, 0, 255)
            draw.rectangle(rect_coords, outline=outline_color, width=3)
            
            # Save annotated
            annotated_path = os.path.join(session_dir, f"step_{step_number:03d}_annotated.png")
            annotated.save(annotated_path)
            
            # Create TestStep
            step = TestStep(
                step_number=step_number,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                screenshot_path=screenshot_path,
                annotated_path=annotated_path,
                highlight_rect={"x": x, "y": y, "w": w, "h": h},
                active_window="Manual Highlight",
                description=description,
                result=result  # Use result from naming dialog
            )
            
            # Emit confirmed signal - main_window will add step to session
            # DO NOT add here to prevent duplicate evidence in report
            self.confirmed.emit(step)
            
            # Close the highlighter safely
            self.hide()
            
        except Exception as e:
            print(f"Failed to save manual highlight: {e}")
            import traceback
            traceback.print_exc()
    
    def _show_naming_dialog_for_manual_highlight(self) -> None:
        """Show naming dialog for manual highlight mode."""
        try:
            naming_dialog = HighlightNamingDialog(self)
            result = naming_dialog.exec_()
            
            if result == QDialog.Accepted:
                result_data = naming_dialog.get_result()
                
                if result_data["reselect"]:
                    # User wants to redraw - reset and continue
                    self.highlight_rect = QRect()
                    self.start_point = QPoint()
                    self.end_point = QPoint()
                    self.update()
                else:
                    # Save the highlight with description and result
                    self._save_manual_highlight(result_data["description"], result_data.get("result", "Pass"))
            else:
                # User cancelled - close highlighter safely
                self.hide()
        
        except Exception as e:
            print(f"Error showing naming dialog: {e}")
            import traceback
            traceback.print_exc()
            self.hide()
    
    def show_step(self, step: TestStep) -> None:
        """
        Display highlighter for a captured step (F8 manual capture).
        Shows bottom toolbar for annotation.
        
        Args:
            step: TestStep with raw screenshot attached as _raw_image
        """
        self.manual_mode = False
        self.step = step
        
        # Get screenshot from step (attached by recorder)
        if hasattr(step, '_raw_image'):
            self.screenshot = step._raw_image
        else:
            # Fallback: load from file
            try:
                self.screenshot = Image.open(step.screenshot_path)
            except Exception as e:
                print(f"Failed to load screenshot: {e}")
                return
        
        # Convert PIL Image to QPixmap
        self._update_pixmap()
        
        # Reset drawing state - IMPORTANT: Unlock drawing for new highlight
        self.highlight_rect = QRect()
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.is_drawing = False
        self.drawing_locked = False  # Allow drawing of ONE rectangle
        
        # Reset inputs
        self.description_input.clear()
        self.result_combo.setCurrentIndex(0)
        
        # SHOW bottom control panel for F8 captures
        self.control_panel.show()
        
        # Show fullscreen using show() + window state instead of showFullScreen()
        self.setWindowState(Qt.WindowFullScreen)
        self.show()
        self.raise_()
        self.activateWindow()
        self.description_input.setFocus()
    
    def _update_pixmap(self) -> None:
        """Convert PIL screenshot to QPixmap for display."""
        if not self.screenshot:
            return
        
        # Convert PIL Image to QImage
        img_data = self.screenshot.convert("RGB").tobytes()
        qimage = QImage(
            img_data,
            self.screenshot.width,
            self.screenshot.height,
            self.screenshot.width * 3,
            QImage.Format_RGB888
        )
        
        self.pixmap = QPixmap.fromImage(qimage)
    
    def paintEvent(self, event) -> None:
        """Draw screenshot and highlight rectangle."""
        painter = QPainter(self)
        
        # Draw screenshot as background
        if self.pixmap:
            # Scale to fit screen while maintaining aspect ratio
            scaled_pixmap = self.pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # Center the image
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
        
        # Draw manual mode overlay text
        if self.manual_mode and self.highlight_rect.isNull():
            # Semi-transparent overlay
            overlay_color = QColor(0, 0, 0, 180)
            painter.fillRect(self.rect(), overlay_color)
            
            # Instruction text
            painter.setPen(QColor(255, 255, 255))
            font = QFont("Arial", 24, QFont.Bold)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, "SNIPPING HIGHLIGHT TOOL ACTIVE\n\nClick and drag to select an area")
        
        # Draw highlight rectangle if being drawn or completed
        if not self.highlight_rect.isNull():
            # Semi-transparent red fill
            pen = QPen(QColor("#FF0000"), 3, Qt.SolidLine)
            painter.setPen(pen)
            
            brush_color = QColor("#FF0000")
            brush_color.setAlpha(int(255 * 0.2))  # 20% opacity
            brush = QBrush(brush_color)
            painter.setBrush(brush)
            
            painter.drawRect(self.highlight_rect)
    
    def mousePressEvent(self, event) -> None:
        """Start drawing highlight rectangle - SINGLE BOX ONLY."""
        if event.button() == Qt.LeftButton and not self.drawing_locked:
            self.is_drawing = True
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.highlight_rect = QRect()
    
    def mouseMoveEvent(self, event) -> None:
        """Update highlight rectangle while dragging."""
        if self.is_drawing:
            self.end_point = event.pos()
            self.highlight_rect = QRect(self.start_point, self.end_point).normalized()
            self.update()  # Trigger repaint
    
    def mouseReleaseEvent(self, event) -> None:
        """Finish drawing highlight rectangle - LOCK AFTER FIRST BOX."""
        if event.button() == Qt.LeftButton and self.is_drawing:
            self.is_drawing = False
            self.end_point = event.pos()
            self.highlight_rect = QRect(self.start_point, self.end_point).normalized()
            self.update()
            
            # LOCK DRAWING - prevent multiple rectangles
            self.drawing_locked = True
            
            # In manual mode, show naming dialog immediately
            if self.manual_mode and not self.highlight_rect.isNull():
                self._show_naming_dialog_for_manual_highlight()
    
    def keyPressEvent(self, event) -> None:
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key_Escape:
            self._on_skip()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if not self.description_input.hasFocus():
                self._on_confirm()
    
    def _on_confirm(self) -> None:
        """Save annotation and emit confirmed signal - SAFE CLOSE."""
        if self.manual_mode:
            # In manual mode, just close safely - SAFE CLOSE
            self.hide()
            return
        
        if not self.step or not self.screenshot:
            return
        
        # Get user inputs
        description = self.description_input.text().strip()
        result = self.result_combo.currentText()
        
        # Validate description
        if not description:
            description = f"Step {self.step.step_number}"
        
        # Update step data
        self.step.description = description
        self.step.result = result
        
        # Save highlight rectangle coordinates
        if not self.highlight_rect.isNull():
            self.step.highlight_rect = {
                "x": self.highlight_rect.x(),
                "y": self.highlight_rect.y(),
                "w": self.highlight_rect.width(),
                "h": self.highlight_rect.height()
            }
        
        # Apply highlight to screenshot and save annotated version
        self._save_annotated_screenshot()
        
        # Emit confirmed signal BEFORE closing
        self.confirmed.emit(self.step)
        
        # Close dialog safely using hide() instead of close()
        self.hide()
    
    def _on_skip(self) -> None:
        """Skip this capture without saving - SAFE CLOSE."""
        self.skipped.emit()
        self.hide()
    
    def _save_annotated_screenshot(self) -> None:
        """Draw highlight rectangle on screenshot and save."""
        if not self.screenshot or not self.step:
            return
        
        try:
            # Create a copy of the screenshot
            annotated = self.screenshot.copy()
            draw = ImageDraw.Draw(annotated, 'RGBA')
            
            # Draw highlight rectangle if exists
            if self.step.highlight_rect:
                x = self.step.highlight_rect["x"]
                y = self.step.highlight_rect["y"]
                w = self.step.highlight_rect["w"]
                h = self.step.highlight_rect["h"]
                
                # Draw rectangle with semi-transparent fill
                rect_coords = [x, y, x + w, y + h]
                
                # Fill
                fill_color = (255, 0, 0, int(255 * 0.2))  # Red with 20% opacity
                draw.rectangle(rect_coords, fill=fill_color, outline=None)
                
                # Outline
                outline_color = (255, 0, 0, 255)  # Solid red
                draw.rectangle(rect_coords, outline=outline_color, width=3)
            
            # Save annotated screenshot with error handling
            base_path = self.step.screenshot_path
            annotated_path = base_path.replace(".png", "_annotated.png")
            
            try:
                annotated.save(annotated_path)
                self.step.annotated_path = annotated_path
            except Exception as save_error:
                print(f"Failed to save annotated screenshot: {save_error}")
                # Use original screenshot if annotation save fails
                self.step.annotated_path = self.step.screenshot_path
            
        except Exception as e:
            print(f"Failed to create annotated screenshot: {e}")
            import traceback
            traceback.print_exc()
            # Use original screenshot if annotation fails
            self.step.annotated_path = self.step.screenshot_path
