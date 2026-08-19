"""
Step review window for editing and reordering captured steps before report generation.
"""
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QLabel, QMessageBox, QProgressDialog, QAbstractItemView,
                             QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon

from session_model import TestSession
from report_generator import ReportGenerator


class StepReviewWindow(QDialog):
    """Review and edit captured steps before generating report."""
    
    report_generated = pyqtSignal(str)  # Signal with report path
    
    def __init__(self, session: TestSession, parent=None):
        """
        Initialize step review window.
        
        Args:
            session: TestSession with captured steps
            parent: Parent widget
        """
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Step Review - TestTrace Recorder")
        self.setModal(True)
        self.resize(1000, 600)
        
        self._setup_ui()
        self._apply_styles()
        self._populate_table()
    
    def _setup_ui(self) -> None:
        """Setup UI components."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Review Captured Steps")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2563EB;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Session info
        info_text = f"TC: {self.session.tc_id} | Steps: {len(self.session.steps)}"
        info_label = QLabel(info_text)
        info_label.setStyleSheet("font-size: 10pt; color: #9CA3AF;")
        header_layout.addWidget(info_label)
        
        main_layout.addLayout(header_layout)
        
        # Instructions
        instructions = QLabel(
            "Review your captured steps below. You can edit descriptions, change results, "
            "reorder steps by dragging rows, or delete unwanted steps."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #D1D5DB; font-size: 9pt;")
        main_layout.addWidget(instructions)
        
        # Steps table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Step", "Timestamp", "Description", "Result", "Actions", "Preview"
        ])
        
        # Table settings
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setDragDropMode(QAbstractItemView.InternalMove)
        self.table.setDragEnabled(True)
        self.table.setDropIndicatorShown(True)
        self.table.verticalHeader().setVisible(False)
        
        # Column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.setColumnWidth(5, 120)
        
        main_layout.addWidget(self.table)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.generate_btn = QPushButton("Generate Report")
        self.generate_btn.clicked.connect(self._on_generate_report)
        button_layout.addWidget(self.generate_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(button_layout)
    
    def _apply_styles(self) -> None:
        """Apply custom stylesheet."""
        self.setStyleSheet("""
            QDialog {
                background-color: #1B2333;
            }
            QLabel {
                color: white;
            }
            QTableWidget {
                background-color: #232D3F;
                color: white;
                gridline-color: #374151;
                border: 1px solid #2563EB;
                border-radius: 4px;
                font-size: 9pt;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #2563EB;
            }
            QHeaderView::section {
                background-color: #1B3A6B;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 10pt;
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
            QPushButton#deleteBtn {
                background-color: #DC2626;
                min-width: 60px;
                padding: 6px 12px;
            }
            QPushButton#deleteBtn:hover {
                background-color: #B91C1C;
            }
            QPushButton#editBtn {
                background-color: #F59E0B;
                min-width: 60px;
                padding: 6px 12px;
            }
            QPushButton#editBtn:hover {
                background-color: #D97706;
            }
        """)
    
    def _populate_table(self) -> None:
        """Populate table with session steps."""
        self.table.setRowCount(len(self.session.steps))
        
        for i, step in enumerate(self.session.steps):
            # Step number
            step_item = QTableWidgetItem(str(step.step_number))
            step_item.setTextAlignment(Qt.AlignCenter)
            step_item.setFlags(step_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 0, step_item)
            
            # Timestamp
            time_item = QTableWidgetItem(step.timestamp)
            time_item.setTextAlignment(Qt.AlignCenter)
            time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 1, time_item)
            
            # Description (editable)
            desc_item = QTableWidgetItem(step.description)
            self.table.setItem(i, 2, desc_item)
            
            # Result badge (editable)
            result_item = QTableWidgetItem(step.result)
            result_item.setTextAlignment(Qt.AlignCenter)
            
            # Color-code result
            if step.result == "Pass":
                result_item.setBackground(Qt.green)
                result_item.setForeground(Qt.white)
            elif step.result == "Fail":
                result_item.setBackground(Qt.red)
                result_item.setForeground(Qt.white)
            elif step.result == "Blocked":
                result_item.setBackground(Qt.yellow)
                result_item.setForeground(Qt.black)
            
            self.table.setItem(i, 3, result_item)
            
            # Action buttons
            action_widget = self._create_action_buttons(i)
            self.table.setCellWidget(i, 4, action_widget)
            
            # Preview thumbnail
            preview_widget = self._create_preview(step)
            self.table.setCellWidget(i, 5, preview_widget)
            
            # Set row height
            self.table.setRowHeight(i, 80)
    
    def _create_action_buttons(self, row: int) -> QWidget:
        """Create action buttons for a row."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("editBtn")
        edit_btn.clicked.connect(lambda: self._edit_step(row))
        layout.addWidget(edit_btn)
        
        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setObjectName("deleteBtn")
        delete_btn.clicked.connect(lambda: self._delete_step(row))
        layout.addWidget(delete_btn)
        
        return widget
    
    def _create_preview(self, step) -> QLabel:
        """Create thumbnail preview of step screenshot."""
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("border: 1px solid #374151; background-color: #1F2937;")
        
        screenshot_path = step.annotated_path or step.screenshot_path
        
        if os.path.exists(screenshot_path):
            pixmap = QPixmap(screenshot_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(100, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label.setPixmap(scaled)
            else:
                label.setText("No preview")
        else:
            label.setText("Missing")
        
        return label
    
    def _edit_step(self, row: int) -> None:
        """Open edit dialog for a step."""
        # For now, just focus on description cell for inline editing
        self.table.setCurrentCell(row, 2)
        self.table.editItem(self.table.item(row, 2))
    
    def _delete_step(self, row: int) -> None:
        """Delete a step from the session."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete Step {row + 1}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Remove from session
            self.session.steps.pop(row)
            self.session._renumber_steps()
            
            # Refresh table
            self._populate_table()
    
    def _on_generate_report(self) -> None:
        """Generate DOCX report from session."""
        # Update step descriptions from table
        for i in range(self.table.rowCount()):
            desc_item = self.table.item(i, 2)
            if desc_item and i < len(self.session.steps):
                self.session.steps[i].description = desc_item.text()
        
        # Show progress dialog
        progress = QProgressDialog("Generating report...", None, 0, 0, self)
        progress.setWindowTitle("TestTrace Recorder")
        progress.setWindowModality(Qt.WindowModal)
        progress.setCancelButton(None)
        progress.show()
        
        try:
            # Generate report
            generator = ReportGenerator()
            output_path = generator.generate(self.session)
            
            progress.close()
            
            # Show success message
            QMessageBox.information(
                self,
                "Report Generated",
                f"Evidence report generated successfully!\n\nSaved to:\n{output_path}"
            )
            
            # Emit signal and close
            self.report_generated.emit(output_path)
            self.accept()
            
        except Exception as e:
            progress.close()
            QMessageBox.critical(
                self,
                "Report Generation Failed",
                f"Failed to generate report:\n\n{str(e)}"
            )
