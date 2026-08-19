"""
Quick verification script for the 5 sequential fixes.
Checks code for proper implementation without running the app.
"""
import os
import sys


def check_file_content(filepath, search_terms, should_exist=True):
    """Check if search terms exist or don't exist in file."""
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = []
    for term in search_terms:
        found = term in content
        if should_exist and not found:
            results.append(f"❌ Missing: {term}")
        elif not should_exist and found:
            results.append(f"❌ Should not exist: {term}")
        else:
            status = "✓" if should_exist else "✓ (correctly removed)"
            results.append(f"✅ {status}: {term}")
    
    return True, results


def main():
    print("="*70)
    print("VERIFICATION: 5 SEQUENTIAL FIXES")
    print("="*70)
    print()
    
    # TASK 1: Single Box Highlight
    print("TASK 1: SINGLE-BOX HIGHLIGHT & EXPLICIT TRIGGERS")
    print("-" * 70)
    
    exists, results = check_file_content(
        "highlighter.py",
        [
            "self.drawing_locked = False",
            "if event.button() == Qt.LeftButton and not self.drawing_locked:",
            "self.drawing_locked = True  # LOCK after first box",
        ],
        should_exist=True
    )
    
    if exists:
        for r in results:
            print(r)
    print()
    
    # TASK 2: Stop & Report Popup
    print("TASK 2: STOP & REPORT GENERATION & POPUP")
    print("-" * 70)
    
    exists, results = check_file_content(
        "ui/main_window.py",
        [
            "Report Generated Successfully",
            "if not os.path.exists(report_path):",
            "QMessageBox.information",
        ],
        should_exist=True
    )
    
    if exists:
        for r in results:
            print(r)
    print()
    
    # TASK 3: Pause Button Removed
    print("TASK 3: PAUSE BUTTON REMOVED")
    print("-" * 70)
    
    # Check that pause is removed
    exists, results = check_file_content(
        "ui/control_panel.py",
        [
            "pause_clicked = pyqtSignal()",
            "self.is_paused",
            "pause_btn",
            "def pause_recording",
            "def resume_recording",
        ],
        should_exist=False
    )
    
    if exists:
        for r in results:
            print(r)
    
    # Check recorder
    exists, results = check_file_content(
        "recorder.py",
        [
            "self.is_paused",
            "def pause(self)",
            "def resume(self)",
        ],
        should_exist=False
    )
    
    if exists:
        for r in results:
            print(r)
    print()
    
    # TASK 4: Safe Dialog Closing
    print("TASK 4: FIX CRASH ON HIGHLIGHT CONFIRM")
    print("-" * 70)
    
    exists, results = check_file_content(
        "highlighter.py",
        [
            "self.hide()",
            "# SAFE CLOSE",
        ],
        should_exist=True
    )
    
    if exists:
        for r in results:
            print(r)
    print()
    
    # TASK 5: Manual Capture Only + Toast
    print("TASK 5: MANUAL CAPTURE & TOAST NOTIFICATIONS")
    print("-" * 70)
    
    exists, results = check_file_content(
        "recorder.py",
        [
            "# DISABLED: Auto-capture on click",
            "Manual capture only",
        ],
        should_exist=True
    )
    
    if exists:
        for r in results:
            print(r)
    
    exists, results = check_file_content(
        "ui/main_window.py",
        [
            "✓ Action Captured",
            "showMessage",
            "1000  # 1 second duration",
        ],
        should_exist=True
    )
    
    if exists:
        for r in results:
            print(r)
    print()
    
    print("="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)
    print()
    print("Next steps:")
    print("1. Run the application: python main.py")
    print("2. Test each fix according to SEQUENTIAL_FIXES_APPLIED.md")
    print("3. Verify no regressions occurred")
    print()


if __name__ == "__main__":
    main()
