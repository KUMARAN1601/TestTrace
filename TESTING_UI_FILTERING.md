# Testing Guide: UI Click Filtering

## Quick Test Procedure

### Prerequisites
- Build or run TestTrace Recorder
- Have an external application open (e.g., Notepad, Chrome)

---

## Test Case 1: Control Panel Clicks Are Filtered

**Steps:**
1. Launch TestTrace Recorder
2. Click **Start** and create a new session
3. Once recording starts, click the **Highlight** button on the control panel
4. Click **Cancel** on the naming dialog
5. Click the control panel background area several times
6. Click **Stop & Report (F9)**

**Expected Result:**
- Report should contain **ZERO steps**
- Console should show "Ignored click on control panel at (x, y)" messages
- No control panel clicks appear in the Word document

---

## Test Case 2: Highlight Workflow Is Filtered

**Steps:**
1. Start recording session
2. Click **Highlight** button
3. Draw a rectangle on the screen (click, drag, release)
4. Type a description in the dialog
5. Select a result from the dropdown
6. Click **Save Highlight Evidence**
7. Stop recording

**Expected Result:**
- Report contains **ONLY ONE step** (the highlighted evidence)
- The click on "Highlight" button is NOT in the report
- The clicks on the naming dialog are NOT in the report
- Console shows "Mouse listener paused" when Highlight clicked
- Console shows "Mouse listener resumed" after saving

---

## Test Case 3: External Clicks Still Work

**Steps:**
1. Start recording session
2. Click on an external application (e.g., Notepad) 3 times
3. Stop recording

**Expected Result:**
- Report contains **3 auto-captured steps**
- Each step shows "Mouse Click at (x, y)"
- Each screenshot has white cursor overlay at click position
- All external clicks are captured normally

---

## Test Case 4: Mixed Workflow

**Steps:**
1. Start recording session
2. Click on Notepad → *Should capture*
3. Click **Highlight** button → *Should NOT capture*
4. Draw rectangle and save highlight → *Should NOT capture these interactions*
5. Click on Notepad again → *Should capture*
6. Click control panel → *Should NOT capture*
7. Click on Desktop → *Should capture*
8. Stop recording

**Expected Result:**
- Report contains **4 steps total:**
  1. Auto-captured: "Mouse Click at (x, y)" - Notepad click #1
  2. Manual Highlight: Your description
  3. Auto-captured: "Mouse Click at (x, y)" - Notepad click #2
  4. Auto-captured: "Mouse Click at (x, y)" - Desktop click
- Control panel and highlight dialog clicks are filtered out

---

## Test Case 5: Control Panel Dragging

**Steps:**
1. Start recording session
2. Drag the control panel to a different screen position
3. Click where the control panel WAS originally → *Should capture*
4. Click where the control panel IS now → *Should NOT capture*
5. Stop recording

**Expected Result:**
- Report contains **1 step** (click on original position)
- Click on new control panel position is filtered
- Console shows "Control panel bounds set: (new x, new y, 650, 90)"

---

## Debug Console Output Reference

When testing, watch the console for these messages:

```
# When recording starts
Recording started - Silent auto-capture enabled

# When Highlight button clicked
Mouse listener paused

# When control panel clicked during recording
Ignored click on control panel at (1500, 50)

# When highlight action completes
Mouse listener resumed
Control panel bounds set: (1250, 20, 650, 90)

# When external click captured
✓ Auto-captured: Step 1 at (500, 300)
  Window: Notepad
  Total steps in session: 1
```

---

## Common Issues & Solutions

### Issue: External clicks not capturing
**Solution:** Check that `auto_capture_on_click` is `true` in `config/settings.json`

### Issue: Control panel clicks still being captured
**Solution:** 
- Check console for "Control panel bounds set" message
- Verify bounds are updated after dragging panel
- Ensure `_update_control_panel_bounds()` is called in `_on_start_recording()`

### Issue: Listener doesn't resume after highlight
**Solution:**
- Verify `resume_listener()` is called in both `_on_step_confirmed()` and `_on_step_skipped()`
- Check that signal connections are working

### Issue: ALL clicks ignored after using Highlight
**Symptom:** `listener_paused` flag stuck at `True`
**Solution:** 
- Ensure highlight dialog ALWAYS calls either confirmed or skipped signal
- Add fallback `resume_listener()` in dialog close event

---

## Verification Checklist

Use this checklist during testing:

- [ ] Control panel Start button click → NOT captured ❌
- [ ] Control panel Highlight button click → NOT captured ❌
- [ ] Control panel Stop button click → NOT captured ❌
- [ ] Control panel drag → NOT captured ❌
- [ ] Highlight rectangle draw → NOT captured ❌
- [ ] Highlight dialog typing → NOT captured ❌
- [ ] Highlight dialog Save click → NOT captured ❌
- [ ] Highlight dialog Cancel click → NOT captured ❌
- [ ] External application clicks → CAPTURED ✅
- [ ] Desktop clicks → CAPTURED ✅
- [ ] Clicks after control panel drag → Still filtered correctly ❌
- [ ] Clicks after highlight complete → Resume capturing ✅

---

## Success Criteria

The implementation is working correctly when:

1. ✅ **Zero** TestTrace UI clicks appear in reports
2. ✅ External application clicks are captured normally
3. ✅ Listener pauses during highlight workflow
4. ✅ Listener resumes after highlight completes or cancels
5. ✅ Control panel clicks filtered regardless of panel position
6. ✅ Console shows appropriate debug messages
7. ✅ No crashes or freezes during UI interactions

---

## Report Validation

After testing, open the generated Word report and verify:

**Each step should be either:**
- "Mouse Click at (x, y)" with external window title (auto-capture)
- Custom description with "Manual Highlight" window (manual highlight)

**NEVER:**
- "Mouse Click at (x, y)" with "TestTrace Recorder" window
- Steps with coordinates matching control panel position
- Empty or untitled steps from UI interactions

---

## Performance Testing

Test with rapid clicking:

1. Start recording
2. Rapidly click control panel 10 times (as fast as possible)
3. Rapidly click external app 10 times (as fast as possible)
4. Stop recording

**Expected:**
- Control panel clicks: ALL filtered (0 in report)
- External clicks: Captured with respect to delay (8-10 in report due to 200ms delay)
- No system freezing or lag
- Smooth UI responsiveness

---

## Edge Cases

### Edge Case 1: Control Panel at Screen Edge
- Drag panel to screen edge (top, left, right)
- Verify clicks still filtered correctly
- Bounds should handle edge positions

### Edge Case 2: Multi-Monitor Setup
- Move control panel to secondary monitor
- Verify filtering works across monitors
- Bounds use absolute screen coordinates

### Edge Case 3: Rapid Highlight Open/Close
- Click Highlight, immediately Cancel
- Click Highlight, immediately Cancel again
- Repeat 5 times quickly
- Verify listener pause/resume handles rapid toggling

### Edge Case 4: Click During Dialog Transition
- Click Highlight button
- Immediately click elsewhere while dialog is opening
- Verify click is filtered (paused before dialog shows)

---

## Automation (Future)

For automated testing, create test script that:

```python
# Pseudo-code for future automated tests
def test_control_panel_filtering():
    recorder = start_recording()
    
    # Simulate click on control panel
    simulate_click(control_panel_x, control_panel_y)
    
    # Stop and check report
    session = recorder.stop()
    assert len(session.steps) == 0, "Control panel click was captured!"

def test_external_capture():
    recorder = start_recording()
    
    # Simulate click on external window
    simulate_click(external_window_x, external_window_y)
    
    # Stop and check report
    session = recorder.stop()
    assert len(session.steps) == 1, "External click not captured!"
    assert "Mouse Click at" in session.steps[0].description
```

---

## Contact for Issues

If filtering doesn't work as expected:
1. Check console output for error messages
2. Verify all code changes were applied
3. Confirm `listener_paused` flag is working
4. Review `control_panel_rect` bounds values
5. Test with simple scenario first before complex workflows
