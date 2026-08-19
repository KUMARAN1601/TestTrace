# TestTrace Recorder - Quick Start Guide

**Get started in 2 minutes! 🚀**

---

## Step 1: Launch Application

```bash
python main.py
```

**What you'll see:**
- Floating control panel in top-right corner
- Buttons: Start, Pause, Highlight, Capture (F8), Stop & Report (F9)

---

## Step 2: Start Recording

1. **Click "Start" button**
2. **Fill in test details:**
   - Test Case ID: `TC_001`
   - Test Case Name: `User Login Test`
   - Module / Feature: `Authentication`
   - Environment: `SIT`
   - Tester Name: `Your Name`
3. **Click "Start Recording"**

**What happens:**
- Control panel turns GREEN ●
- Timer starts counting
- Recording is active!

---

## Step 3: Perform Your Test

### 🖱️ Automatic Capture (Recommended)
**Just click normally!** Every left-click is captured automatically.

**Example:**
1. Click "Username" field → **Screenshot captured!**
2. Type username
3. Click "Password" field → **Screenshot captured!**
4. Type password
5. Click "Login" button → **Screenshot captured!**

**After each click:**
- Highlighter appears with your screenshot
- Draw a red box around the important area
- Enter description: *"Clicked Login button"*
- Select result: Pass / Fail / Blocked
- Click "Confirm"
- Recording continues!

### ✨ Manual Highlight (For Special Evidence)
**Use when you need to highlight specific data:**

1. **Click "Highlight" button**
2. Screen freezes (shows current state)
3. **Click & drag** to draw rectangle
4. **Enter description:** *"Customer ID showing 12345"*
5. **Click "Save Highlight & Evidence"**
6. Recording continues!

**Perfect for:**
- Data fields (show values entered)
- Error messages
- Success notifications
- Before/after states

---

## Step 4: Stop & Get Your Report

1. **Click "Stop & Report (F9)"** when done
2. **Report generates automatically**
3. **Custom dialog appears:**

```
┌─────────────────────────────────────────────┐
│  ✅ Evidence report generated successfully! │
│                                             │
│  Location:                                  │
│  ./output/Evidence_TC001_20260819.docx      │
│                                             │
│  [📄 Open Word Document]                    │
│  [📁 Open Export Folder]  [Close]           │
└─────────────────────────────────────────────┘
```

4. **Click "📄 Open Word Document"** → Opens in Microsoft Word
5. **Or click "📁 Open Export Folder"** → Opens folder with file selected

---

## What You Get

### Professional Word Report Contains:
✅ Cover page with test metadata  
✅ Execution summary (Pass/Fail counts)  
✅ Step-by-step evidence with screenshots  
✅ Red highlight boxes showing important areas  
✅ Your descriptions for each step  
✅ Timestamps and active window info  
✅ Sign-off section for approval  

### File Location:
```
./output/Evidence_{TC_ID}_{Date}_{TesterName}.docx
```
**Example:** `Evidence_TC001_20260819_JohnDoe.docx`

---

## Tips & Tricks

### 💡 Auto-Capture Best Practices:
- **Let it work for you** - Just click normally, don't overthink it
- **Describe each step clearly** - Future you will thank you
- **Use Pass/Fail/Blocked** - Accurate results matter
- **Don't click too fast** - Wait 200ms between clicks to avoid duplicates

### 💡 When to Use Manual Highlight:
- Showing **specific data values** (IDs, names, amounts)
- Highlighting **error messages**
- Capturing **confirmation messages**
- Documenting **before/after states**

### 💡 Keyboard Shortcuts:
- **F8** - Manual capture (screenshot without click)
- **F9** - Stop & Report
- **F10** - Pause/Resume
- **Escape** - Cancel highlighter

---

## Common Scenarios

### Scenario 1: Form Fill-Out
```
1. Click "Name" field       → Auto-captured ✓
2. Type "John Smith"        → (not captured)
3. Click "Email" field      → Auto-captured ✓
4. Type "john@test.com"     → (not captured)
5. Click "Submit"           → Auto-captured ✓
6. Success message shows    → Press F8 to capture
```
**Total:** 4 captures (3 auto + 1 manual)

### Scenario 2: Data Validation
```
1. Click "Amount" field     → Auto-captured ✓
2. Type "invalid"           → (not captured)
3. Click "Save"             → Auto-captured ✓
4. Error appears            → Click "Highlight" button
5. Draw box around error    → Enter description
6. Save highlight           → ✓
```
**Total:** 3 captures (2 auto + 1 highlight)

---

## Troubleshooting

### ❓ Control panel disappeared after step?
**Fixed!** Control panel now always stays visible.

### ❓ Clicks not being captured?
**Check:**
- Is status GREEN? (recording active)
- Not YELLOW? (if paused, click "Resume")
- Are you LEFT-clicking? (right clicks don't capture)

**Workaround:** Use F8 for manual capture

### ❓ Can't open report?
**Check:**
- Is Microsoft Word installed?
- Try "Open Export Folder" button instead

### ❓ Typed text not captured?
**Expected!** Typing doesn't auto-capture.
**Solution:** 
- Click next field (captures with typed text visible)
- Or use Highlight tool to show the filled field

---

## Example Test: User Login

### Execution:
1. **Start recording** → Enter test details
2. **Open browser** (no capture needed)
3. **Navigate to login page** → Press F8
4. **Click Username field** → Auto-captured ✓
5. Type username
6. **Click Password field** → Auto-captured ✓
7. Type password
8. **Click Login button** → Auto-captured ✓
9. Dashboard appears → Press F8
10. **Stop & Report** → F9

### Result:
- **5 total captures** (3 auto + 2 manual)
- **Professional Word report** generated
- **Opens in Word** with one click
- **All evidence documented** with screenshots

---

## Configuration (Optional)

### `config/settings.json`:
```json
{
  "auto_capture_on_click": true,      // Auto-capture enabled
  "capture_delay_ms": 200,            // 200ms delay (default)
  "highlight_color": "#FF0000",       // Red highlights
  "highlight_opacity": 0.3            // 30% opacity
}
```

**Change delay if needed:**
- `100ms` - Fast clicking (may get duplicates)
- `200ms` - Default (recommended)
- `500ms` - Slow clicking (no duplicates)

---

## That's It! 🎉

**You're ready to record your first test!**

**Remember:**
1. **Start** → Fill test details
2. **Perform test** → Auto-capture on clicks
3. **Use Highlight** → For special evidence
4. **Stop & Report** → Get Word document

**Happy Testing!** ✨

---

## Need More Help?

- **Full Documentation:** `README.md`
- **Capture Behavior:** `CAPTURE_BEHAVIOR_GUIDE.md`
- **Highlight Tool Guide:** `HIGHLIGHT_TOOL_USER_GUIDE.md`
- **Troubleshooting:** `FINAL_FIXES_SUMMARY.md`

---

**Questions? Check the documentation or open an issue on GitHub.**
