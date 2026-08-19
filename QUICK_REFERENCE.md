# Quick Reference - TestTrace Recorder (All Fixes Applied)

## Launch
```bash
python main.py
```

## Control Panel Buttons

| Button | Function | Keyboard |
|--------|----------|----------|
| **Start** | Begin new recording session | - |
| **Highlight** | Capture with manual highlight | - |
| **Stop & Report** | Generate Word document | F9 |

**Note:** Pause button has been REMOVED (continuous recording only)

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **F8** | Manual capture (shows highlighter) |
| **F9** | Stop recording & generate report |
| **ESC** | Skip current highlight (while in highlighter) |

## Status Indicators

| Color | Meaning |
|-------|---------|
| **Gray ●** | Idle (not recording) |
| **Green ●** | Recording active |

## How to Capture Steps

### Method 1: Manual Capture (F8)
1. Press **F8** while recording
2. Toast notification: "✓ Action Captured"
3. Highlighter overlay appears
4. Draw ONE rectangle (optional)
5. Enter description
6. Click "Confirm"

### Method 2: Highlight Button
1. Click **"Highlight"** button on control panel
2. Screen freezes with overlay message
3. Draw ONE rectangle
4. Enter description in naming dialog
5. Click "Save Highlight & Evidence"

**Important:** Auto-capture on clicks is DISABLED (prevents issues)

## Single-Box Rule

- You can draw EXACTLY ONE rectangle per screenshot
- After first rectangle, drawing is locked
- To redraw: Click "Re-select Area" in naming dialog

## Recording Workflow

1. **Start**
   - Click "Start" → Fill session form → Start Recording
   - Timer starts, green dot appears

2. **Capture Steps**
   - Press F8 or click "Highlight" button
   - Draw box → Enter description → Confirm
   - Repeat for each test step

3. **Stop**
   - Click "Stop & Report (F9)"
   - Success popup shows file path
   - Click "Open Word Document" to view

## Important Behaviors

### ✅ What Works
- Control panel ALWAYS visible (stays on top)
- Drag panel anywhere on screen
- Timer runs continuously
- Manual capture via F8 or button
- Toast notifications (brief, non-blocking)
- Single rectangle per screenshot

### ❌ What's Disabled
- Auto-capture on clicks (no longer automatic)
- Pause/Resume (removed for simplicity)
- Multiple rectangles (single box only)
- Background triggers (explicit only)

## Troubleshooting

### Control panel disappeared?
- Check top-right corner of screen
- Drag it if behind other windows
- Restart: `taskkill /f /im python.exe` then `python main.py`

### Can't draw in highlighter?
- Only ONE box allowed per screenshot
- If already drawn, click "Re-select Area"

### No captures happening?
- Auto-capture is disabled
- Use F8 or "Highlight" button manually

### Report not generating?
- Ensure at least 1 step captured
- Check ./output/ folder exists
- Check console for errors

## File Locations

| Item | Location |
|------|----------|
| Reports | `./output/Evidence_*.docx` |
| Screenshots | `./temp_sessions/session_*/` |
| Config | `./config/settings.json` |
| Logs | Console output |

## Quick Test

```bash
python main.py
# 1. Start → Fill form → Start Recording (timer runs)
# 2. Press F8 → Draw box → Enter "Test" → Confirm (no crash!)
# 3. Stop & Report → Success popup shows (see file path)
# 4. Verify: 3 buttons only (no pause)
```

## Success Indicators

✓ Control panel visible at all times  
✓ Timer counting continuously  
✓ Green dot during recording  
✓ Toast appears on capture  
✓ No crashes on confirm  
✓ Success popup after generation  

## Need Help?

- **Full Testing:** See `FINAL_TEST_GUIDE.md`
- **Technical Details:** See `SEQUENTIAL_FIXES_APPLIED.md`
- **Verification:** Run `python verify_fixes.py`

---

**Status:** All 5 sequential fixes applied ✅  
**Version:** Production Ready  
**Date:** 2026-08-19
