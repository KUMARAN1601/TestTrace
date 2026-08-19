# TestTrace Recorder v1.0

**Automated Test Evidence Capture Desktop Tool for QA Engineers**

TestTrace Recorder is a Windows desktop application that automates the entire test evidence capture workflow. It runs alongside your application during testing, automatically captures screenshots on every interaction, lets you annotate and highlight important areas, then generates a professional Word document with complete step-by-step evidence.

---

## Features

✨ **Automatic Screenshot Capture** - Captures screen on every mouse click  
🎨 **Visual Annotation** - Draw highlight rectangles around important areas  
⚡ **Global Hotkeys** - F8 (capture), F9 (stop), F10 (pause/resume)  
📊 **Structured Reports** - Generate professional DOCX evidence documents  
🖥️ **Multi-Monitor Support** - Works seamlessly across multiple displays  
⏱️ **Session Timer** - Track test execution duration automatically  
🔄 **Step Review** - Edit, reorder, or delete steps before report generation  
🎯 **Always-on-Top Control Panel** - Floating toolbar that never gets in the way  

---

## System Requirements

- **Operating System**: Windows 10 or Windows 11
- **Python**: 3.11 or higher (for development)
- **RAM**: 4GB minimum, 8GB recommended
- **Display**: Any resolution, multi-monitor supported

---

## Installation

### For Development

1. **Clone or extract the project**
   ```bash
   cd testtrace
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # Windows Command Prompt
   venv\Scripts\activate
   
   # Windows PowerShell
   venv\Scripts\Activate.ps1
   
   # Windows Git Bash
   source venv/Scripts/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

---

## Building Standalone Executable

To create a single-file `.exe` that can run on any Windows PC without Python installed:

1. **Ensure PyInstaller is installed**
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**
   ```bash
   pyinstaller build.spec
   ```

3. **Find the executable**
   - Built executable: `dist/TestTrace.exe`
   - Size: ~50-80 MB (single file, no dependencies)

4. **Distribute**
   - Copy `TestTrace.exe` to any Windows PC
   - No Python installation required on target machine
   - Double-click to run

---

## Usage Guide

### 1. Launch Application
- Double-click `TestTrace.exe` or run `python main.py`
- Floating control panel appears in top-right corner
- System tray icon appears in Windows taskbar

### 2. Start New Session
- Click **"Start"** on control panel (or right-click tray icon → New Session)
- Fill in test case metadata:
  - **Test Case ID** * (required) - e.g., TC_VISA_AUTH_001
  - **Test Case Name** * (required) - e.g., VISA Authorization Flow
  - **Module** * (required) - Select from dropdown
  - **Environment** * (required) - SIT / UAT / PROD / Dev
  - **Tester Name** * (required) - Your name
  - **Build Version** (optional) - e.g., v3.2.1
  - **Expected Result** (optional) - Brief description
- Click **"Start Recording"**

### 3. Execute Test
- Perform your test steps normally in the application
- Every mouse click automatically triggers a screenshot capture
- **Or** press **F8** to manually capture at any moment

### 4. Annotate Each Step
- After each capture, a full-screen overlay appears
- **Draw a highlight rectangle** - Click and drag to highlight important area
- **Add description** - Type what action you performed (e.g., "Clicked Submit button")
- **Select result** - Pass / Fail / Blocked
- Click **"Confirm"** to save (or **"Skip"** to discard)

### 5. Stop Recording
- Click **"Stop"** button or press **F9**
- Step Review window opens automatically

### 6. Review Steps
- View all captured steps with thumbnails
- **Edit** descriptions by clicking in Description column
- **Delete** unwanted steps with Delete button
- **Reorder** steps by dragging rows
- Click **"Generate Report"** when ready

### 7. Get Your Evidence Report
- Word document automatically generated
- Saved to `output/` folder
- Filename format: `Evidence_TC_VISA_AUTH_001_20260818_Kumaran.docx`
- Output folder opens automatically

---

## Hotkey Reference

| Hotkey | Action | When Available |
|--------|--------|----------------|
| **F8** | Manual screenshot capture | During recording |
| **F9** | Stop recording & open review | During recording |
| **F10** | Pause / Resume toggle | During recording |
| **Esc** | Skip current annotation | In highlighter overlay |

---

## Project Structure

```
testtrace/
├── main.py                    # Application entry point
├── session_model.py           # Data models (TestSession, TestStep)
├── recorder.py                # Core recording logic (mss, pynput)
├── highlighter.py             # Screenshot annotation overlay
├── report_generator.py        # DOCX report builder (python-docx)
├── ui/
│   ├── __init__.py
│   ├── main_window.py         # Main application controller
│   ├── control_panel.py       # Floating control toolbar
│   ├── session_dialog.py      # Test session setup form
│   └── step_review.py         # Pre-export step review screen
├── assets/
│   └── icon.ico               # Application icon (add your own)
├── config/
│   └── settings.json          # User preferences
├── output/                    # Generated DOCX reports saved here
├── temp_sessions/             # Temporary screenshot storage
├── requirements.txt           # Python dependencies
├── build.spec                 # PyInstaller build configuration
└── README.md                  # This file
```

---

## Configuration

Settings are stored in `config/settings.json`:

```json
{
  "output_dir": "./output",
  "auto_capture_on_click": true,
  "capture_delay_ms": 200,
  "hotkey_capture": "F8",
  "hotkey_stop": "F9",
  "hotkey_pause": "F10",
  "highlight_color": "#FF0000",
  "highlight_opacity": 0.3,
  "tester_name": "",
  "last_module": "Authorization",
  "last_environment": "SIT"
}
```

You can manually edit this file to customize:
- Output directory path
- Auto-capture behavior
- Capture delay (ms between clicks)
- Hotkey assignments (limited support)
- Highlight color and opacity
- Default tester name and preferences

---

## Generated Report Structure

The DOCX evidence report includes:

1. **Cover Page**
   - Test Case ID, Name, Module, Environment
   - Tester name, execution date/time, duration
   - Overall test status (PASS/FAIL/BLOCKED)

2. **Test Execution Summary**
   - Total steps executed
   - Pass/Fail/Blocked counts
   - Expected result description

3. **Step-by-Step Evidence**
   - For each step:
     - Step number, timestamp, active window
     - Action description
     - Annotated screenshot with highlight
     - Result badge (color-coded)

4. **Sign-Off Section**
   - Tester signature block
   - Reviewer signature block

---

## Troubleshooting

### Global hotkeys not working
**Solution**: Run as Administrator
- Right-click `TestTrace.exe`
- Select "Run as administrator"
- Windows security may block global hooks without admin rights

### Screenshot capture fails
**Solution**: Check permissions
- Ensure application has screen capture permissions
- Some secured applications block screenshots
- Try running as Administrator

### Report generation fails
**Solution**: Check file paths
- Ensure screenshots exist in `temp_sessions/`
- Check write permissions to `output/` folder
- Verify python-docx is installed correctly

### Application won't start
**Solution**: Check dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### "Not running as Administrator" warning
- This is a warning, not an error
- Application will work, but global hotkeys may not function
- Run as Administrator for full functionality

---

## Dependencies

- **PyQt5** (5.15.10) - GUI framework
- **mss** (9.0.1) - Fast screenshot capture
- **Pillow** (10.4.0) - Image processing
- **pynput** (1.7.6) - Global mouse/keyboard hooks
- **keyboard** (0.13.5) - Global hotkey support
- **python-docx** (1.1.0) - Word document generation
- **pyinstaller** (6.6.0) - Executable packaging
- **pywin32** (306) - Windows API integration

---

## Limitations

- **Windows only** - Uses Windows-specific APIs (ctypes, pywin32)
- **Screenshot protection** - Some applications block screenshots (DRM content)
- **Admin rights** - Global hotkeys require administrator privileges
- **Single session** - One recording session at a time

---

## Future Enhancements (Roadmap)

- [ ] Video recording alongside screenshots
- [ ] JIRA integration (auto-upload evidence)
- [ ] TestRail integration (update test run results)
- [ ] PDF export option
- [ ] AI-powered step description generation
- [ ] Custom report templates
- [ ] Team collaboration dashboard
- [ ] Defect linking

---

## Support

For issues, feature requests, or questions:
- Check the Troubleshooting section above
- Review console output for error messages
- Ensure all dependencies are correctly installed

---

## License

Copyright © 2026 Kumaran - QA Engineer

---

## Version History

**v1.0.0** (August 2026) - Initial Release
- Core recording functionality
- Screenshot capture with annotation
- DOCX report generation
- Global hotkey support
- Step review and editing
- System tray integration

---

**Built with ❤️ for QA Engineers everywhere**
