# Debug: Auto-Capture Steps Not Appearing in Report

## Issue
Mouse clicks are being captured but not appearing in the generated Word report.

## Debug Logging Added

I've added comprehensive debug logging to track the data flow from mouse click to report generation:

### 1. Recorder Debug Output (recorder.py)

When auto-capture occurs, you'll now see:
```
✓ Auto-captured: Step 1 at (850, 300)
  Window: Google Chrome - Login Page
  Total steps in session: 1
```

This confirms:
- Step was captured
- Cursor position recorded
- Window title captured
- Step added to session

### 2. Stop Recording Debug Output (ui/main_window.py)

When you click "Stop & Report", you'll see:
```
=== STOP RECORDING DEBUG ===
Session from recorder.stop(): <session_model.TestSession object at 0x...>
self.current_session: <session_model.TestSession object at 0x...>
Are they the same object? True
Steps in recorder session: 5
  Step 1: Step 1 - Pass
  Step 2: Step 2 - Pass
  Step 3: Manual Highlight Evidence - Pass
  Step 4: Step 4 - Pass
  Step 5: Step 5 - Pass
Steps in current_session: 5
  Step 1: Step 1 - Pass
  ...
============================
```

This confirms:
- Session object is consistent
- All steps are in the session
- Step descriptions and results are set

### 3. Report Generator Debug Output (report_generator.py)

When generating the report, you'll see:
```
=== REPORT GENERATION DEBUG ===
Session ID: a1b2c3d4
Test Case: TC001
Total steps in session: 5
  Step 1: Step 1 - Pass
    Screenshot: C:\...\temp_sessions\session_...\step_001.png
    Annotated: C:\...\temp_sessions\session_...\step_001_annotated.png
  Step 2: Step 2 - Pass
    Screenshot: C:\...\temp_sessions\session_...\step_002.png
    Annotated: C:\...\temp_sessions\session_...\step_002_annotated.png
  ...
===============================
```

This confirms:
- Report generator received all steps
- Screenshot paths are correct
- Annotated paths are set for auto-captures

## How to Use Debug Logging

### Testing Procedure:

1. **Start the Application**
   ```bash
   python main.py
   ```

2. **Start Recording**
   - Click "Start" or "New Session"
   - Console should show: "Recording started - Silent auto-capture enabled"

3. **Click Around Screen**
   - Click on browser, applications, buttons
   - Watch console for auto-capture confirmations:
     ```
     ✓ Auto-captured: Step 1 at (850, 300)
       Window: Google Chrome
       Total steps in session: 1
     ✓ Auto-captured: Step 2 at (1024, 450)
       Window: Microsoft Excel
       Total steps in session: 2
     ```

4. **Add a Manual Highlight (Optional)**
   - Click "Highlight" button
   - Draw rectangle and add description
   - Watch console for confirmation

5. **Stop & Generate Report**
   - Click "Stop & Report"
   - Console shows all debug output sections
   - Check that step counts match in all three sections

6. **Open Generated Report**
   - Check `output/Evidence_*.docx`
   - Verify all steps appear
   - Verify screenshots show cursor overlay at click points

## Expected Behavior

### Auto-Captured Steps:
- Description: "Step 1", "Step 2", etc.
- Result: "Pass"
- Screenshot: Has cursor overlay at click point
- Annotated path: Same as screenshot path (already overlaid)

### Manual Highlight Steps:
- Description: User-provided text
- Result: User-selected (Pass/Fail/Blocked)
- Screenshot: Raw screenshot
- Annotated path: Screenshot with red highlight rectangle

### Report:
- ALL steps should appear in sequential order
- Each step has screenshot
- Auto-captured steps show cursor at click location
- Manual highlights show red rectangle overlay

## Troubleshooting

### If auto-capture is not working:

1. **Check settings.json**
   ```json
   {
     "auto_capture_on_click": true,
     "capture_delay_ms": 200
   }
   ```
   Must be `true`, not `false`

2. **Check console for mouse listener startup**
   Should see: "Recording started - Silent auto-capture enabled"
   If you see: "Manual capture only" - listener didn't start

3. **Check for permission issues**
   - pynput may require admin privileges on some systems
   - Try running as administrator

### If steps are captured but not in report:

1. **Check step count matching**
   - Compare "Total steps in session" across all three debug sections
   - If numbers differ, there's a data flow issue

2. **Check session object identity**
   - Verify "Are they the same object? True"
   - If False, recorder and main_window have different session objects

3. **Check screenshot paths**
   - Verify paths exist and are accessible
   - Check that `temp_sessions/session_*/` folder has all screenshots

### If report is empty:

1. **Check report generator received steps**
   - Look for "Total steps in session: 0" in report generator debug
   - If 0, session is empty when passed to generator

2. **Check for exceptions**
   - Look for error messages in console
   - Check "Report Generation Failed" dialog

## Code Changes Made

### recorder.py
```python
# Added detailed logging in silent mode
if silent:
    if self.session:
        self.session.add_step(step)
        print(f"✓ Auto-captured: Step {self.step_counter} at ({x}, {y})")
        print(f"  Window: {window_title}")
        print(f"  Total steps in session: {len(self.session.steps)}")
    else:
        print(f"ERROR: No active session to add step to!")
```

### ui/main_window.py
```python
# Added debug output in _on_stop_recording
print(f"\n=== STOP RECORDING DEBUG ===")
print(f"Session from recorder.stop(): {session}")
print(f"Steps in recorder session: {len(session.steps)}")
for step in session.steps:
    print(f"  Step {i+1}: {step.description} - {step.result}")
print(f"============================\n")
```

### report_generator.py
```python
# Added debug output in generate()
print(f"\n=== REPORT GENERATION DEBUG ===")
print(f"Total steps in session: {len(session.steps)}")
for step in session.steps:
    print(f"  Step {i+1}: {step.description} - {step.result}")
    print(f"    Screenshot: {step.screenshot_path}")
    print(f"    Annotated: {step.annotated_path}")
print(f"===============================\n")
```

## Next Steps

1. Run the application with these debug logs
2. Perform a full test cycle (start, click, highlight, stop)
3. Review console output to identify where the data flow breaks
4. Share console output if issue persists

The debug logs will show exactly where steps are being lost in the pipeline.
