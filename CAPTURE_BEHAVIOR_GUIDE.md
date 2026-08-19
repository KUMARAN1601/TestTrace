# TestTrace Recorder - Capture Behavior Guide

**Last Updated:** August 19, 2026  
**Version:** 1.1

---

## What Gets Captured Automatically

### ✅ Mouse Click Events (LEFT BUTTON ONLY)

The recorder automatically captures screenshots when you **LEFT-CLICK** on:

1. **Buttons** - Submit, Cancel, OK, etc.
2. **Links** - Hyperlinks, navigation links
3. **Menu Items** - Dropdown menus, context menus
4. **Input Fields** - Text boxes (when clicking to focus)
5. **Checkboxes** - Select/deselect
6. **Radio Buttons** - Option selection
7. **Tabs** - Switching between tabs
8. **Icons** - Application icons, toolbar icons
9. **List Items** - Selecting items in lists
10. **Dropdowns** - Opening dropdown menus

### ❌ What is NOT Captured Automatically

These actions do NOT trigger automatic capture:

1. **Mouse Hover** - Moving mouse over elements (no click)
2. **Right Click** - Right button clicks
3. **Middle Click** - Scroll wheel clicks  
4. **Keyboard Input** - Typing in fields
5. **Scrolling** - Mouse wheel scrolling
6. **Drag and Drop** - Click-and-drag operations (only captures the initial click)
7. **Double Click** - Captures only the first click
8. **Window Resize** - Moving/resizing windows

### 🔄 How to Capture Non-Click Actions

For actions that don't automatically capture, use:

**Method 1: Manual Capture (F8)**
- Press **F8** key after performing the action
- Or click **"Capture (F8)"** button on control panel

**Method 2: Highlight Tool**
- Click **"Highlight"** button on control panel
- Screen freezes
- Draw rectangle around relevant area
- Enter description
- Creates evidence with annotation

---

## Capture Behavior Details

### Automatic Click Capture Flow:

1. **User clicks** anywhere on screen (left button)
2. **Delay check** - Must be >200ms since last capture (prevents duplicates)
3. **Recorder checks** - Is recording active? Not paused?
4. **Screenshot taken** - Full screen capture using mss library
5. **Metadata captured:**
   - Click coordinates (x, y)
   - Active window title
   - Timestamp
   - Step number (auto-incremented)
6. **Highlighter appears** - Full-screen overlay with screenshot
7. **User annotates:**
   - Draws red rectangle around important area
   - Enters step description
   - Selects result (Pass/Fail/Blocked)
8. **Step saved** - Added to session with annotated screenshot

### Manual Capture Flow (F8):

1. **User presses F8** or clicks "Capture" button
2. **Check** - Is recording active? Not paused?
3. **Screenshot taken** - Full screen capture
4. **Metadata captured:**
   - No click coordinates (manual)
   - Active window title
   - Timestamp
   - Step number
5. **Highlighter appears** - Same annotation flow as automatic
6. **Step saved** - Added to session

### Highlight Tool Flow:

1. **User clicks "Highlight"** button during recording
2. **Screen freezes** - Current screen captured with ImageGrab
3. **Overlay shown** - "SNIPPING HIGHLIGHT TOOL ACTIVE"
4. **User draws** rectangle by click-and-drag
5. **Naming dialog appears** immediately after drawing
6. **User enters** description (required)
7. **Options:**
   - **Re-select Area** - Redraw rectangle
   - **Cancel** - Discard highlight
   - **Save Highlight & Evidence** - Save and continue recording
8. **Step saved** - Annotated screenshot added to session
9. **Recording continues** - Control panel still active

---

## Capture Delay Explained

**Default:** 200ms between captures

**Why?** Prevents duplicate captures when:
- User double-clicks
- Application opens a dialog (click registers on both windows)
- Click triggers multiple events

**Can be changed** in `config/settings.json`:
```json
{
  "capture_delay_ms": 200
}
```

**Recommended values:**
- **100ms** - Fast clicking, may capture duplicates
- **200ms** - Default, good balance
- **500ms** - Slow clicking, prevents all duplicates

---

## Common Scenarios

### Scenario 1: Form Fill-Out
**Actions:**
1. Click in "Name" field → **CAPTURED** (click)
2. Type "John Smith" → **NOT CAPTURED** (typing)
3. Click in "Email" field → **CAPTURED** (click)
4. Type "john@example.com" → **NOT CAPTURED** (typing)
5. Click "Submit" button → **CAPTURED** (click)

**Result:** 3 automatic captures (field clicks + submit)

**To capture typed data:** Use "Highlight" tool to show the filled form

### Scenario 2: Navigation
**Actions:**
1. Click "Products" menu → **CAPTURED**
2. Hover over submenu items → **NOT CAPTURED** (hover)
3. Click "Electronics" → **CAPTURED**
4. Scroll down page → **NOT CAPTURED** (scroll)
5. Click product image → **CAPTURED**

**Result:** 3 automatic captures

**To capture page after scroll:** Press F8 to manually capture

### Scenario 3: Data Validation
**Actions:**
1. Click "Amount" field → **CAPTURED**
2. Type "invalid text" → **NOT CAPTURED**
3. Click "Save" → **CAPTURED**
4. Error message appears → **NOT CAPTURED** (automatic display)

**Result:** 2 automatic captures, but error message NOT shown

**To capture error:** 
- **Option A:** Click anywhere on the error message → **CAPTURED**
- **Option B:** Press F8 → **CAPTURED**
- **Option C:** Use "Highlight" tool to highlight the error

### Scenario 4: Dropdown Selection
**Actions:**
1. Click dropdown arrow → **CAPTURED** (dropdown opens)
2. Hover over options → **NOT CAPTURED** (hover)
3. Click "Option 2" → **CAPTURED** (selection made)

**Result:** 2 automatic captures

### Scenario 5: Drag and Drop
**Actions:**
1. Click and hold item → **CAPTURED** (initial click only)
2. Drag item → **NOT CAPTURED** (movement)
3. Release item → **NOT CAPTURED** (mouse release)

**Result:** 1 automatic capture (start of drag)

**To capture final state:** 
- Press F8 after drop
- Or use "Highlight" tool to show final position

---

## Mouse Click Detection

### Detected Clicks:
- **Left button press** ✅
- **Left button release** ❌ (only press)

### Mouse Listener:
- Uses `pynput` library
- Global mouse hook (works across all applications)
- Requires application to run (gracefully degrades if no admin rights)

### Why Only Left Click?
- **Right click** typically opens context menus (no action taken)
- **Middle click** usually for scrolling/opening in new tab
- **Left click** is primary action button (buttons, links, inputs)

---

## Keyboard Hotkeys for Manual Capture

| Hotkey | Action | When Available |
|--------|--------|----------------|
| **F8** | Manual capture | While recording (not paused) |
| **F9** | Stop & Report | While recording |
| **F10** | Pause/Resume | While recording |
| **Escape** | Cancel highlight | While in highlighter overlay |

**Note:** Hotkeys require admin rights. If not available, use control panel buttons.

---

## Best Practices

### ✅ DO:
- **Click to capture** standard actions (buttons, links)
- **Use F8** for state changes that don't involve clicks
- **Use Highlight tool** to show data fields, error messages, or specific UI elements
- **Let automatic capture work** - don't manually capture every step
- **Describe each step** clearly in the highlighter

### ❌ DON'T:
- **Don't rely on hover** to capture - always click or use F8
- **Don't expect typing** to auto-capture - highlight the result instead
- **Don't skip annotation** - blank descriptions aren't useful
- **Don't capture duplicates** - wait 200ms between clicks
- **Don't forget to highlight errors** - they won't auto-capture

---

## Troubleshooting Capture Issues

### "Clicks aren't being captured"
**Check:**
1. Is recording active? (Green status indicator)
2. Is recording paused? (Yellow indicator - click "Resume")
3. Are you left-clicking? (Right/middle clicks don't capture)
4. Are you clicking too fast? (Wait 200ms between clicks)
5. Is mouse listener running? (Check console for errors)

**Solution:** Use manual capture (F8) if automatic fails

### "Highlighter doesn't appear after click"
**Check:**
1. Is recorder running? (Check console for errors)
2. Did screenshot capture fail? (Check console)
3. Is highlighter stuck behind other windows? (Check taskbar)

**Solution:** Press Escape, try manual capture (F8)

### "Can't capture hover states"
**This is expected behavior.** Mouse hover does NOT trigger capture.

**Solution:**
1. Click on the hovered element (if clickable)
2. Press F8 while hovering
3. Use Highlight tool to capture the hover state

### "Typed data not captured"
**This is expected behavior.** Keyboard input does NOT trigger capture.

**Solution:**
1. Click somewhere after typing (next field, submit button)
2. Press F8 after typing
3. Use Highlight tool to show the filled field

---

## Technical Implementation

### Libraries Used:
- **mss** - Fast screenshot capture (multi-monitor support)
- **pynput.mouse** - Global mouse listener
- **PIL/Pillow** - Image processing and saving
- **PyQt5** - UI overlays and annotations

### Capture Pipeline:
```
User Action (Left Click)
    ↓
pynput.mouse.Listener detects click
    ↓
Recorder._on_click(x, y, button, pressed)
    ↓
Check: Recording? Not paused? Delay passed?
    ↓
Recorder._perform_capture(x, y, is_manual=False)
    ↓
Screenshot captured with mss
    ↓
Active window title retrieved (Windows API)
    ↓
TestStep created with metadata
    ↓
Signal emitted: step_captured(TestStep)
    ↓
MainWindow._on_step_captured(step)
    ↓
Highlighter.show_step(step)
    ↓
User annotates (draw rectangle, describe)
    ↓
Highlighter._on_confirm()
    ↓
Annotated screenshot saved
    ↓
Signal emitted: confirmed(TestStep)
    ↓
MainWindow._on_step_confirmed(step)
    ↓
Step added to session
    ↓
Control panel step counter increments
```

---

## Examples with Expected Captures

### Test Case: User Login

| Step | Action | Captured? | How? |
|------|--------|-----------|------|
| 1 | Open browser | NO | No click |
| 2 | Navigate to URL | NO | Typing |
| 3 | Click "Username" field | ✅ YES | Auto (click) |
| 4 | Type username | NO | Typing |
| 5 | Click "Password" field | ✅ YES | Auto (click) |
| 6 | Type password | NO | Typing |
| 7 | Click "Login" button | ✅ YES | Auto (click) |
| 8 | Dashboard appears | NO | Automatic |
| 9 | Press F8 to capture dashboard | ✅ YES | Manual (F8) |

**Total Automatic Captures:** 3  
**Total Manual Captures:** 1  
**Total Highlights Needed:** 0 (but could highlight username/password fields)

---

## Summary

**Automatic capture works for:** Left-button mouse clicks  
**Manual capture needed for:** Everything else (hover, typing, scrolling, etc.)  
**Highlight tool for:** Showing specific data, errors, or UI elements  

**Recording workflow:**
1. Start recording → Control panel appears
2. Perform test → Clicks auto-capture, annotate each
3. Use F8/Highlight for non-click evidence
4. Stop & Report → DOCX generated automatically
5. Open report in Word

**That's it! The recorder does the heavy lifting for you.** 🎉

---

**End of Guide**
