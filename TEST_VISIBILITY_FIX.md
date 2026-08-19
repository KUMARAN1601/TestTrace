# Quick Test Guide - Control Panel Visibility Fix

## What Was Fixed

The control panel was disappearing when you clicked "Start" button. This has been completely fixed with the following improvements:

1. **Control panel stays visible** during session dialog
2. **Control panel stays visible** after clicking Start Recording
3. **Timer runs continuously** after recording starts
4. **Control panel stays visible** during captures and highlights
5. **Proper cleanup** when stopping/completing recording

## Quick Test (5 Minutes)

### Test 1: Basic Start/Stop Flow

```bash
# Run the application
python main.py
```

**Expected Results:**
1. ✓ Control panel appears in top-right corner
2. ✓ "Start" button is enabled (blue)
3. ✓ Other buttons are disabled (gray)
4. ✓ Timer shows 00:00:00
5. ✓ Gray status dot
6. ✓ Steps: 0

**Now Click "Start" Button:**
1. ✓ Session dialog pops up
2. ✓ Control panel STILL VISIBLE behind dialog
3. Fill in:
   - Test Case ID: TEST_001
   - Test Case Name: Visibility Test
   - Module: UI
   - Environment: SIT
   - Tester Name: [Your name]
4. Click "Start Recording"

**After Clicking Start Recording:**
1. ✓ Control panel STILL VISIBLE
2. ✓ Timer STARTS counting (00:00:01, 00:00:02, 00:00:03...)
3. ✓ Green status dot appears
4. ✓ "Start" button becomes disabled (gray)
5. ✓ "Pause", "Highlight", "Stop & Report" become enabled (blue)

**SUCCESS!** If you see the timer running and the control panel is visible, the fix is working!

### Test 2: Capture and Highlight

**While Recording (timer running):**
1. Click anywhere on screen (desktop, browser, etc.)
2. ✓ Control panel should STAY VISIBLE during capture
3. ✓ Highlighter overlay appears with bottom panel
4. Type description: "Test capture"
5. Click "Confirm"
6. ✓ Control panel reappears immediately
7. ✓ Timer continues running
8. ✓ Step count increments to 1

**Click "Highlight" Button:**
1. ✓ Screen freezes with "SNIPPING HIGHLIGHT TOOL ACTIVE"
2. Click and drag to draw red rectangle
3. Type description: "Test highlight"
4. Click "Save Highlight & Evidence"
5. ✓ Control panel reappears immediately
6. ✓ Timer continues running
7. ✓ Step count increments to 2

### Test 3: Complete Recording

1. Click "Stop & Report" button
2. ✓ "Generating evidence report..." notification
3. ✓ Completion dialog appears
4. Click "Open Word Document"
5. ✓ Word document opens
6. Close Word
7. ✓ Control panel returns to initial state:
   - Gray dot
   - Timer: 00:00:00
   - Steps: 0
   - "Start" button enabled
   - Other buttons disabled

## Automated Monitoring Test

For detailed visibility monitoring during testing:

```bash
python test_control_panel_visibility.py
```

This will:
- Show control panel status every 2 seconds in console
- Display recording state, step count, timer
- Alert if panel becomes hidden (shouldn't happen!)

## Console Output to Look For

When you run the application, you should see:

```
Initial state: Control Panel visible = True
Window flags: ...
Position: (...)
Size: 650x90
Monitoring control panel visibility every 2 seconds...

✓ Control Panel VISIBLE - Recording: False, Paused: False, Steps: 0, Timer: 00:00:00
✓ Control Panel VISIBLE - Recording: True, Paused: False, Steps: 0, Timer: 00:00:01
✓ Control Panel VISIBLE - Recording: True, Paused: False, Steps: 1, Timer: 00:00:15
✓ Control Panel VISIBLE - Recording: True, Paused: False, Steps: 2, Timer: 00:00:32
```

You should NEVER see:
```
✗ Control Panel HIDDEN - This should NOT happen!
```

## What If Something Goes Wrong?

### Control Panel Not Appearing at All
```bash
# Check if Python dependencies are installed
pip install -r requirements.txt

# Run with verbose output
python main.py
```

### Control Panel Appears But Disappears After Start
This should be fixed now! But if it happens:
1. Check the console for error messages
2. Run the automated monitoring test: `python test_control_panel_visibility.py`
3. Report the exact step where it disappeared

### Timer Not Running
This should be fixed now! Timer should start immediately after "Start Recording" and count continuously every second.

### Mouse Captures Not Working
- Make sure you're clicking with LEFT mouse button
- Wait 200ms between clicks (prevents duplicates)
- Check console for "mouse listener" errors

## All Tests Passing?

If all tests pass, you should see:
- ✓ Control panel always visible
- ✓ Timer running continuously during recording
- ✓ Captures working (auto and manual)
- ✓ Highlights working
- ✓ Report generation working
- ✓ Clean return to initial state after stop

**The application is now fully functional!**

## Next Steps

Once visibility is confirmed working:
1. Test with real workflows (browser testing, app testing)
2. Test multi-monitor setup (drag panel between monitors)
3. Test pause/resume functionality
4. Generate full test reports

## Need Help?

If you encounter any issues:
1. Check console output for error messages
2. Run automated test: `python test_control_panel_visibility.py`
3. Review `CONTROL_PANEL_VISIBILITY_FIX.md` for technical details
4. Check other documentation: `QUICK_START_GUIDE.md`, `FINAL_COMPLETE_STATUS.md`
