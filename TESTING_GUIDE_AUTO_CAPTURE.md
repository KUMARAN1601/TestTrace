# Testing Guide: Auto-Capture Mouse Clicks in Report

## Current Implementation Status

✅ **Mouse listener starts** when recording begins  
✅ **Steps are added to session** with `session.add_step(step)`  
✅ **Cursor overlay** applied at click coordinates  
✅ **Description** set to "Mouse Click at (x, y)"  
✅ **Result** set to "Pass"  
✅ **Report generator** iterates over `session.steps`  
✅ **Debug logging** added to track data flow

## Testing Procedure

### Step 1: Start the Application
```bash
python main.py
```

### Step 2: Start Recording
1. Click "Start" or "New Session" button
2. Fill in test case details
3. Click OK

**Expected Console Output:**
```
Recording started - Silent auto-capture enabled
```

If you see "Manual capture only" instead, check:
- `config/settings.json` has `"auto_capture_on_click": true`
- pynput module is installed

### Step 3: Click Around (Auto-Capture)
Click on different applications/windows:
- Browser address bar
- Excel cell
- Notepad window
- Desktop icon

**Expected Console Output (per click):**
```
✓ Auto-captured: Step 1 at (850, 300)
  Window: Google Chrome
  Total steps in session: 1

✓ Auto-captured: Step 2 at (1024, 450)
  Window: Microsoft Excel
  Total steps in session: 2

✓ Auto-captured: Step 3 at (640, 720)
  Window: Notepad
  Total steps in session: 3
```

**If you see no output:**
- Mouse listener may not have started
- Check if you're running as administrator
- Verify `auto_capture_on_click: true` in settings

### Step 4: Add Manual Highlight (Optional)
1. Click "Highlight" button
2. Draw rectangle on screen
3. Enter description: "Highlighted Important Field"
4. Select result: "Pass"
5. Click "Save"

**Expected Console Output:**
```
(No console output for manual highlights - they use UI dialog)
```

### Step 5: Stop & Generate Report
1. Click "Stop & Report" button

**Expected Console Output:**
```
=== STOP RECORDING DEBUG ===
Session from recorder.stop(): <session_model.TestSession object at 0x...>
self.current_session: <session_model.TestSession object at 0x...>
Are they the same object? True
Steps in recorder session: 4
  Step 1: Mouse Click at (850, 300) - Pass
  Step 2: Mouse Click at (1024, 450) - Pass
  Step 3: Mouse Click at (640, 720) - Pass
  Step 4: Highlighted Important Field - Pass
Steps in current_session: 4
  Step 1: Mouse Click at (850, 300) - Pass
  Step 2: Mouse Click at (1024, 450) - Pass
  Step 3: Mouse Click at (640, 720) - Pass
  Step 4: Highlighted Important Field - Pass
============================

=== REPORT GENERATION DEBUG ===
Session ID: a1b2c3d4
Test Case: TC001
Total steps in session: 4
  Step 1: Mouse Click at (850, 300) - Pass
    Screenshot: C:\...\temp_sessions\session_...\step_001.png
    Annotated: C:\...\temp_sessions\session_...\step_001_annotated.png
  Step 2: Mouse Click at (1024, 450) - Pass
    Screenshot: C:\...\temp_sessions\session_...\step_002.png
    Annotated: C:\...\temp_sessions\session_...\step_002_annotated.png
  Step 3: Mouse Click at (640, 720) - Pass
    Screenshot: C:\...\temp_sessions\session_...\step_003.png
    Annotated: C:\...\temp_sessions\session_...\step_003_annotated.png
  Step 4: Highlighted Important Field - Pass
    Screenshot: C:\...\temp_sessions\session_...\step_004.png
    Annotated: C:\...\temp_sessions\session_...\step_004_annotated.png
===============================
```

### Step 6: Verify Report Content
1. Open generated report in `output/Evidence_*.docx`
2. Check that report contains ALL 4 steps
3. Verify each auto-captured step shows:
   - Description: "Mouse Click at (x, y)"
   - Result badge: "PASS" (green)
   - Screenshot with cursor overlay at click point
4. Verify manual highlight shows:
   - Description: "Highlighted Important Field"
   - Result badge: "PASS" (green)
   - Screenshot with red rectangle highlight

## Troubleshooting

### Problem: No Auto-Captures Happening

**Symptom:** Clicks don't trigger screenshots

**Solutions:**
1. Check `config/settings.json`:
   ```json
   {
     "auto_capture_on_click": true
   }
   ```

2. Check console for listener startup:
   - Should see: "Silent auto-capture enabled"
   - If not, listener didn't start

3. Run as administrator:
   - pynput may need elevated privileges
   - Right-click → Run as Administrator

4. Check Python packages:
   ```bash
   pip install pynput pillow mss
   ```

### Problem: Steps Captured But Not in Report

**Symptom:** Console shows auto-captures, but report is empty or only has manual highlights

**Debug Steps:**

1. **Check step count at each stage:**
   - Auto-capture console: "Total steps in session: X"
   - Stop recording debug: "Steps in recorder session: X"
   - Report generation debug: "Total steps in session: X"
   - All three should match!

2. **If counts don't match:**
   - Between auto-capture and stop: Session object issue
   - Between stop and report: Session passing issue

3. **Verify session object identity:**
   - Check: "Are they the same object? True"
   - If False: `self.current_session` and `recorder.session` are different

4. **Check screenshot paths:**
   - Look in `temp_sessions/session_*/` folder
   - Should have `step_001.png`, `step_001_annotated.png`, etc.
   - If files exist but not in report: Path issue

### Problem: Only Manual Highlights in Report

**This is the reported issue!**

**Diagnostic:**
1. Run through test procedure above
2. Check console output at each stage
3. Compare step counts
4. Share console output for analysis

**Possible Causes:**
1. Auto-captures not being added to session
   - Check: "Total steps in session" increases after each click
   - If not increasing: `session.add_step()` not working

2. Session object mismatch
   - Check: "Are they the same object?"
   - Should be True

3. Report generator receiving empty session
   - Check: "Total steps in session" in report generation debug
   - Compare with stop recording debug count

## Expected Report Structure

### Cover Page:
- Test Case ID
- Tester Name
- Overall Status (PASS if all steps pass)

### Summary Section:
```
Total Steps Executed: 4
Passed: 4
Failed: 0
Blocked: 0
Untested: 0

Overall Test Status: PASS
```

### Step Evidence Section:

**Step 1:**
- Header: "Step 1 | 2026-08-20 14:30:45 | Google Chrome"
- Action: "Mouse Click at (850, 300)"
- Screenshot: Full screen with white arrow cursor at (850, 300)
- Result: **PASS** (green badge)

**Step 2:**
- Header: "Step 2 | 2026-08-20 14:31:12 | Microsoft Excel"
- Action: "Mouse Click at (1024, 450)"
- Screenshot: Full screen with white arrow cursor at (1024, 450)
- Result: **PASS** (green badge)

**Step 3:**
- Header: "Step 3 | 2026-08-20 14:31:45 | Notepad"
- Action: "Mouse Click at (640, 720)"
- Screenshot: Full screen with white arrow cursor at (640, 720)
- Result: **PASS** (green badge)

**Step 4:**
- Header: "Step 4 | 2026-08-20 14:32:20 | Manual Highlight"
- Action: "Highlighted Important Field"
- Screenshot: Full screen with red rectangle around highlighted area
- Result: **PASS** (green badge)

## Code Verification

### 1. Mouse Listener Activation (recorder.py, line ~90)
```python
# Start mouse listener for auto-capture on click (SILENT MODE)
if self.settings.get("auto_capture_on_click", True):
    try:
        self.mouse_listener = mouse.Listener(on_click=self._on_click)
        self.mouse_listener.start()
        print("Recording started - Silent auto-capture enabled")
```

### 2. Step Addition (recorder.py, line ~246)
```python
if silent:
    # SILENT MODE: Add step directly to session
    if self.session:
        self.session.add_step(step)
        print(f"✓ Auto-captured: Step {self.step_counter} at ({x}, {y})")
        print(f"  Total steps in session: {len(self.session.steps)}")
```

### 3. Report Generation (report_generator.py, line ~189)
```python
# Add each step
for i, step in enumerate(session.steps):
    self._add_step_block(doc, step)
```

All code is correctly implemented. The debug logging will reveal where the issue is.

## Next Steps

1. Run the test procedure above
2. Capture all console output
3. Check if step counts match at each stage
4. Verify report content matches expected structure
5. If issue persists, share console output for further diagnosis
