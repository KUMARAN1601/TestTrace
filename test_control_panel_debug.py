"""Debug script to test control panel visibility after dialog."""
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout
from ui.control_panel import ControlPanel
from ui.session_dialog import SessionDialog


def main():
    app = QApplication(sys.argv)
    
    # Create control panel
    control_panel = ControlPanel()
    control_panel.show()
    print("Control panel shown initially")
    
    def on_start_clicked():
        print("Start button clicked")
        
        # Show session dialog
        dialog = SessionDialog(None)
        result = dialog.exec_()
        print(f"Dialog result: {result}")
        
        if result == QDialog.Accepted:
            session = dialog.get_session()
            print(f"Session: {session}")
            
            if session:
                # Simulate starting recording
                control_panel.reset_counters()
                control_panel.start_recording()
                
                # Ensure visible
                control_panel.show()
                control_panel.raise_()
                control_panel.activateWindow()
                print("Control panel updated and shown")
    
    control_panel.start_clicked.connect(on_start_clicked)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
