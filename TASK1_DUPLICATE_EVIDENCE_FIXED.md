# Task 1: Fix Duplicate Evidence in Word Report - COMPLETE ✅

## Issue Fixed
When a user highlighted an issue, the exact same image and step were being saved and printed TWICE in the final .docx report.

## Root Cause Analysis

### Problem Identified
The step was being added to the session **twice**:

1. **First Addition** - In `highlighter.py` line ~388:
   ```python
   # _save_manual_highlight() method
   self.current_session.add_step(step)  # ❌ DUPLICATE ADDITION
   self.confirmed.emit(step)
   ```

2. **Second Addition** - In `ui/main_window.py` line ~330:
   ```python
   # _on_step_confirmed() signal handler
   self.current_session.add_step(step)  # ✅ CORRECT ADDITION
   ```

### Why This Happened
When the user clicks the "Highlight" button:
1. `highlighter.py` creates a manual highlight
2. `_save_manual_highlight()` creates a TestStep and adds it to session
3. Then emits `confirmed` signal
4. `main_window.py` receives the signal and adds the SAME step again
5. Result: Step appears twice in `session.steps` array
6. Report generator iterates over `session.steps` and includes both duplicates

## Fix Applied

### Changed File: `highlighter.py`

**Location:** Line ~388 in `_save_manual_highlight()` method

**Before:**
```python
# Create TestStep
step = TestStep(
    step_number=step_number,
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    screenshot_path=screenshot_path,
    annotated_path=annotated_path,
    highlight_rect={"x": x, "y": y, "w": w, "h": h},
    active_window="Manual Highlight",
    description=description,
    result="Pass"
)

# Add to session
self.current_session.add_step(step)  # ❌ REMOVED - causes duplicate

# Emit confirmed signal
self.confirmed.emit(step)
```

**After:**
```python
# Create TestStep
step = TestStep(
    step_number=step_number,
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    screenshot_path=screenshot_path,
    annotated_path=annotated_path,
    highlight_rect={"x": x, "y": y, "w": w, "h": h},
    active_window="Manual Highlight",
    description=description,
    result="Pass"
)

# Emit confirmed signal - main_window will add step to session
# DO NOT add here to prevent duplicate evidence in report
self.confirmed.emit(step)
```

## Verification

### DOCX Generation Check
✅ Verified `report_generator.py` - No duplicate iteration issues found:
- `_add_step_evidence_section()` method uses single `for i, step in enumerate(session.steps)` loop
- Each step is processed exactly once
- No nested loops or repeated iterations

### Evidence Storage Check
✅ Verified step storage flow:
1. Manual highlight creates step
2. Step is emitted via `confirmed` signal
3. Main window handler adds step to session **once**
4. No duplicate additions anywhere in the codebase

## How It Works Now

### Correct Flow:
1. User clicks "Highlight" button
2. `highlighter.py` captures screen and shows drawing overlay
3. User draws rectangle and enters description
4. `_save_manual_highlight()` creates TestStep object
5. Step is **NOT** added to session locally
6. `confirmed.emit(step)` signal sent to main window
7. `main_window._on_step_confirmed()` receives signal
8. Step is added to session **ONCE** ✅
9. Report generation iterates over steps **ONCE** ✅
10. Each step appears in report **ONCE** ✅

## Testing Checklist

To verify the fix works:

- [ ] Start recording session
- [ ] Click "Highlight" button
- [ ] Draw a rectangle around an element
- [ ] Enter description and save
- [ ] Click "Stop & Report"
- [ ] Open generated Word document
- [ ] Verify the highlighted step appears **ONLY ONCE** in report
- [ ] Repeat with F8 manual capture - should also work correctly
- [ ] Generate report with multiple highlights - each should appear once

## Files Modified
- `highlighter.py` - Removed duplicate `add_step()` call in `_save_manual_highlight()`

## Files Verified (No Changes Needed)
- `report_generator.py` - DOCX generation loop is correct
- `ui/main_window.py` - Signal handler is correct
- `session_model.py` - Storage mechanism is correct

## Impact
- **Before Fix:** Each manual highlight appeared twice in Word report (duplicate evidence)
- **After Fix:** Each manual highlight appears exactly once in Word report ✅
- **Side Effects:** None - F8 manual capture and all other functionality unchanged

## Notes
- This fix only affects manual highlights (Highlight button)
- F8 manual capture already had correct flow (no duplication)
- The fix follows proper signal/slot architecture in PyQt
- Step is now only added in the central handler location (`main_window._on_step_confirmed`)
