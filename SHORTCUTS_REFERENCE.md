# TestTrace Recorder - Keyboard Shortcuts & Controls Reference

## ⌨️ Global Hotkeys (Work Anywhere)

| Hotkey | Action | Available When |
|--------|--------|----------------|
| **F8** | Manual screenshot capture | Recording active |
| **F9** | Stop recording & open review | Recording active |
| **F10** | Pause / Resume toggle | Recording active |

> **Note**: Global hotkeys require Administrator privileges on Windows

---

## 🖱️ Control Panel Buttons

### When Idle
- **Start** - Begin new recording session

### When Recording
- **Pause** - Suspend capture (timer stops, yellow indicator)
- **Resume** - Continue capture (timer resumes, green indicator)
- **Capture (F8)** - Force screenshot at current moment
- **Stop (F9)** - End session and open step review

### Status Indicators
- **● Gray** - Idle (not recording)
- **● Green** - Recording active
- **● Yellow** - Paused

---

## 🎨 Highlighter Overlay Controls

### Mouse Actions
- **Click + Drag** - Draw highlight rectangle
- **Release** - Complete rectangle

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| **Esc** | Skip this capture (discard) |
| **Enter** | Confirm annotation (when not in description field) |
| **Tab** | Navigate between fields |

### Buttons
- **Confirm** - Save step with annotation
- **Skip** - Discard this capture

---

## 📝 Step Review Window

### Mouse Actions
- **Click in Description** - Edit step description
- **Drag Row** - Reorder steps

### Buttons (Per Step)
- **Edit** - Focus description field for editing
- **Delete** - Remove step from session

### Main Actions
- **Generate Report** - Create DOCX evidence document
- **Cancel** - Close without generating report

---

## 🔔 System Tray Icon

### Left Click
- Show/raise control panel

### Right Click Menu
- **Open Control Panel** - Show floating toolbar
- **New Session** - Start new recording
- **Exit** - Close application

---

## 💡 Tips & Tricks

### Efficient Recording
1. Use auto-capture for standard testing (every click captures)
2. Use F8 for precise control (only capture when you press F8)
3. Use F10 to pause when navigating away

### Annotation Speed
1. Draw highlight first, then type description
2. Tab through fields quickly
3. Enter to confirm (if not in text field)
4. Esc to skip unwanted captures

### Step Management
1. Edit descriptions inline during review
2. Delete accidental captures immediately
3. Reorder by dragging if steps are out of sequence

### Report Quality
1. Always add descriptive text ("Clicked Submit" better than "Step 1")
2. Use Pass/Fail/Blocked consistently
3. Review all steps before generating report
4. Keep highlights focused on important areas

---

## 🎯 Workflow Keyboard Flow

**Fast Recording Workflow (Keyboard-Only)**

```
1. Start app
2. Click Start → Fill form → Enter
3. Perform test (auto-capture on clicks)
4. For each capture:
   - Draw highlight
   - Type description
   - Tab to result
   - Space/Arrow to select
   - Enter to confirm
5. Press F9 when done
6. Review steps
7. Enter to generate report
```

**Manual Control Workflow**

```
1. Start app
2. Click Start → Fill form → Enter
3. Perform test action
4. Press F8 to capture
5. Annotate and confirm
6. Repeat steps 3-5
7. Press F9 when done
8. Review and generate
```

---

## 🚫 What Keys DON'T Work

These keys are **not** supported:
- ❌ Ctrl+C / Ctrl+V (use mouse for copy/paste in fields)
- ❌ Alt+F4 (use Exit from tray menu)
- ❌ Windows+D (may minimize control panel)
- ❌ Custom hotkey combinations (only F8/F9/F10)

---

## 🔧 Customizing Hotkeys

Currently, hotkeys are hardcoded to F8/F9/F10. To change them:

1. Edit `ui/main_window.py` in the `HotkeyThread` class:
```python
keyboard.add_hotkey('f8', ...)  # Change 'f8' to desired key
keyboard.add_hotkey('f9', ...)  # Change 'f9' to desired key
keyboard.add_hotkey('f10', ...) # Change 'f10' to desired key
```

2. Update labels in `ui/control_panel.py`:
```python
self.capture_btn = QPushButton("Capture (F8)")  # Update label
self.stop_btn = QPushButton("Stop (F9)")        # Update label
```

3. Update documentation (README.md, this file)

---

## 📱 Mouse-Only Operation

TestTrace can be operated entirely with mouse:
- Click "Start" instead of pressing hotkeys
- Click "Capture" instead of F8
- Click "Stop" instead of F9
- Click "Pause" instead of F10
- All features accessible via buttons

---

## 🎮 Advanced Controls

### Control Panel Movement
- **Click + Drag** anywhere on panel to move it
- Position is not saved between sessions

### Window Management
- Control panel is **always on top** (can't be covered)
- Highlighter overlay is **modal** (must complete or skip)
- Review window is **modal** (must complete or cancel)

### Multi-Monitor
- Screenshots capture **all monitors** as one image
- Control panel appears on **primary monitor**
- Highlighter overlay covers **all monitors**

---

## 🆘 Emergency Controls

### If Application Freezes
1. **Ctrl+Alt+Del** → Task Manager
2. End "TestTrace.exe" or "python.exe"
3. Restart application

### If Hotkeys Stop Working
1. Close application
2. Right-click TestTrace.exe
3. "Run as Administrator"
4. Hotkeys should work now

### If Can't Click Anything
- Highlighter overlay is probably active
- Press **Esc** to close it
- Or move mouse to bottom of screen to find control buttons

---

## 📖 Quick Reference Card

**Print this section for desk reference**

```
╔══════════════════════════════════════════════╗
║   TESTTRACE RECORDER - QUICK REFERENCE       ║
╠══════════════════════════════════════════════╣
║  HOTKEYS                                     ║
║  ├─ F8  : Manual Capture                    ║
║  ├─ F9  : Stop & Review                     ║
║  └─ F10 : Pause/Resume                      ║
║                                              ║
║  HIGHLIGHTER                                 ║
║  ├─ Click+Drag : Draw highlight             ║
║  ├─ Enter      : Confirm                    ║
║  └─ Esc        : Skip                       ║
║                                              ║
║  STATUS DOTS                                 ║
║  ├─ ● Gray   : Idle                         ║
║  ├─ ● Green  : Recording                    ║
║  └─ ● Yellow : Paused                       ║
║                                              ║
║  OUTPUTS                                     ║
║  └─ output/Evidence_[TC]_[Date]_[Name].docx ║
╚══════════════════════════════════════════════╝
```

---

**Need help?** See README.md for complete documentation
