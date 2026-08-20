================================
TestTrace Recorder v1.0
================================

Test Evidence Capture Tool for QA Engineers
Captures screenshots, highlights, and generates Word reports.

================================
QUICK START
================================

1. Double-click TestTrace.exe to launch
2. If Windows Defender blocks it, click "More info" then "Run anyway"
3. Control panel appears in top-right corner

================================
HOW TO USE
================================

STEP 1: Start Recording
-----------------------
- Click "Start" button
- Fill in test case details:
  * Test Case ID (e.g., TC_001)
  * Test Case Name (e.g., Login Test)
  * Module/Feature (e.g., Authorization)
  * Environment (e.g., SIT)
  * Tester Name (e.g., Kumaran)
- Click "Start Recording"
- Timer starts running

STEP 2: Capture Steps
---------------------
Method 1: Press F8
- Press F8 key at any time
- Toast notification: "Action Captured"
- Screen freezes with overlay

Method 2: Click Highlight Button
- Click "Highlight" button on control panel
- Screen freezes immediately

Then:
- Draw ONE rectangle around important area
- Enter step description
- Click "Save Highlight & Evidence"
- Repeat for each test step

STEP 3: Generate Report
-----------------------
- Click "Stop & Report (F9)" button
- Wait 2-3 seconds
- Success popup shows file location
- Click "OK"
- Choose action:
  * Open Word Document - Opens report
  * Open Export Folder - Opens Downloads
  * Close - Just close
- Application exits automatically

================================
KEYBOARD SHORTCUTS
================================

F8 = Manual capture (while recording)
F9 = Stop recording and generate report
ESC = Skip current highlight

================================
WHERE ARE REPORTS SAVED?
================================

Reports are saved automatically to your Downloads folder:

Windows: C:\Users\[YourName]\Downloads\
macOS: /Users/[YourName]/Downloads/
Linux: /home/[YourName]/Downloads/

File format: Evidence_[TC_ID]_[Date]_[Tester].docx

================================
SYSTEM REQUIREMENTS
================================

- Windows 10 or later
- Microsoft Word (for opening reports)
- Administrator privileges (recommended for global hotkeys)

================================
TROUBLESHOOTING
================================

Q: F8/F9 keys don't work
A: Run TestTrace.exe as Administrator

Q: Windows blocks the application
A: Right-click TestTrace.exe → Properties → Check "Unblock" → OK

Q: Application doesn't start
A: Check if antivirus is blocking it
   Add exclusion or temporarily disable

Q: Reports not in Downloads
A: Check success popup for actual location
   May have saved to Documents folder

Q: Can't draw second rectangle
A: This is normal - only ONE box per screenshot
   Click "Re-select Area" to redraw

Q: Application disappears during use
A: This has been fixed - should not happen
   Report if it occurs

================================
FEATURES
================================

✓ Floating control panel (always on top)
✓ Draggable panel (move anywhere)
✓ Manual capture only (F8 or button)
✓ Single-box highlighting
✓ Toast notifications
✓ Auto-save to Downloads folder
✓ Professional Word reports
✓ Auto-exit after report generation

================================
KNOWN BEHAVIORS
================================

- Only ONE rectangle per screenshot (by design)
- No auto-capture on clicks (manual only)
- No pause button (continuous recording)
- Application closes after report generation
- Reports always go to Downloads folder

================================
CONFIGURATION
================================

Edit config/settings.json to customize:

{
  "output_dir": null,           // Downloads folder
  "tester_name": "Your Name",   // Default name
  "last_module": "Auth",        // Last used module
  "last_environment": "SIT"     // Last environment
}

================================
FILE LOCATIONS
================================

TestTrace.exe       - Main application
config/             - Configuration files
  settings.json     - User preferences
assets/             - Icons and resources
Downloads/          - Generated reports

================================
SUPPORT
================================

For issues or questions:
1. Check this README
2. Run as Administrator
3. Check Windows Defender settings
4. Contact your IT department

================================
VERSION
================================

Version: 1.0 Complete
Date: 2026-08-19
Platform: Windows 10/11

================================
LICENSE
================================

[Add your license information here]

================================
© 2026 TestTrace. All rights reserved.
