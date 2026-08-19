# Highlight Tool User Guide

**Quick reference for using the manual highlight evidence feature**

---

## How to Use the Highlight Tool

### Step 1: Start Recording
1. Click **Start** button on the control panel
2. Fill in your test case details in the session dialog
3. Click **OK** to begin recording

### Step 2: Perform Your Test
- Perform your test steps as normal
- Screenshots are automatically captured on mouse clicks
- Or use **F8** to manually capture screens

### Step 3: Add Manual Highlight Evidence
When you want to highlight a specific UI element or data field:

1. **Click the "Highlight" button** on the control panel
   - Button is between "Pause" and "Capture"
   - Only enabled while recording (not paused)

2. **Your screen will freeze immediately**
   - You'll see: "SNIPPING HIGHLIGHT TOOL ACTIVE"
   - Instruction: "Click and drag to select an area"

3. **Click and drag** to draw a rectangle around the area you want to highlight
   - Red rectangle appears as you drag
   - Release mouse button when done

4. **Naming Dialog appears automatically**
   - **Description field:** Describe what you highlighted
     - Example: "Highlighted Customer Name Field 'John Smith'"
     - Example: "Highlighted Error Message 'Invalid credentials'"
   - **Re-select Area:** Click if you want to redraw the rectangle
   - **Cancel:** Discard this highlight
   - **Save Highlight & Evidence:** Save the annotated screenshot

5. **Evidence is saved and added to your test session**
   - Step counter increments
   - You can continue recording or highlight more areas

### Step 4: Stop and Generate Report
1. Click **Stop (F9)** button when testing is complete
2. Report generates automatically
3. Dialog appears: "Would you like to open the report now?"
4. Click **Yes** to open the Word document immediately

---

## Tips & Tricks

### Best Practices:
- ✅ Use descriptive names: Include the field name and actual value
- ✅ Highlight data fields to show what was entered
- ✅ Highlight error messages to document failures
- ✅ Highlight confirmation messages to document success
- ✅ Re-select if your rectangle isn't quite right

### Common Use Cases:
- **Data Entry:** Highlight fields to show entered values
- **Error Validation:** Capture error messages with context
- **Confirmation:** Document success messages and status changes
- **UI Elements:** Highlight buttons, menus, or options selected
- **Before/After:** Capture state changes in the application

### Keyboard Shortcuts:
- **F8:** Manual screenshot capture (during recording)
- **F9:** Stop recording and generate report
- **F10:** Pause/Resume recording
- **Escape:** Cancel highlight or annotation (when in overlay)

---

## Example Descriptions

### Good Descriptions:
✅ "Highlighted Customer Name field showing 'John Smith'"  
✅ "Error message displayed: 'Invalid email format'"  
✅ "Submit button enabled after form completion"  
✅ "Balance updated from $100.00 to $150.00"  
✅ "Success notification: 'Transaction completed successfully'"

### Avoid:
❌ "Highlighted something"  
❌ "Field"  
❌ "Button clicked"  
❌ "Step 5"

---

## Workflow Comparison

### Without Highlight Tool:
1. Stop recording
2. Take screenshot manually (Print Screen)
3. Paste into image editor
4. Draw rectangle manually
5. Save image
6. Resume recording
7. Describe step later

### With Highlight Tool:
1. **Click "Highlight"**
2. **Draw rectangle**
3. **Type description**
4. **Click "Save"**
5. Continue recording ✨

**Time saved: ~90 seconds per highlight**

---

## Troubleshooting

### Highlight button is grayed out:
- ✅ Make sure recording is active (green status indicator)
- ✅ If paused (yellow indicator), click "Resume" first

### Screen doesn't freeze when I click Highlight:
- ✅ Ensure recording is not paused
- ✅ Try clicking the button again
- ✅ Check that the application has focus

### Naming dialog doesn't appear after drawing:
- ✅ Make sure you released the mouse button
- ✅ Try drawing a larger rectangle (at least 10x10 pixels)
- ✅ Dialog may be behind other windows - check taskbar

### Can't enter description:
- ✅ Click inside the description text field
- ✅ Description is required - field will turn red if empty

---

## Report Output

### Generated Report Includes:
- Cover page with test metadata
- Execution summary with result counts
- **Step-by-step evidence with screenshots**
- Each screenshot shows your red highlight rectangle
- Your descriptions appear above each screenshot
- Sign-off section for tester and reviewer

### Report Location:
- **Default:** `./output/Evidence_{TC_ID}_{Date}_{Tester}.docx`
- **Example:** `./output/Evidence_TC001_20260819_JohnDoe.docx`

### Opening the Report:
- Click "Yes" when prompted after stopping
- Or navigate to `./output` folder manually
- Double-click to open in Microsoft Word

---

## Advanced Usage

### Multiple Highlights in One Test:
1. Click "Highlight" button multiple times during recording
2. Each highlight creates a separate test step
3. All highlights appear in sequence in the final report

### Combining with Automatic Captures:
- Automatic captures (on click): Show actions performed
- Manual highlights: Show specific data or UI elements
- Together: Complete evidence trail with detailed annotations

### Re-selecting Area:
1. Draw your first rectangle
2. In naming dialog, click "Re-select Area"
3. Draw a new rectangle (previous one discarded)
4. Enter description and save

---

## Questions?

For more help, refer to:
- `README.md` - Full application documentation
- `QUICKSTART.md` - Getting started guide
- `SHORTCUTS_REFERENCE.md` - All keyboard shortcuts

**Happy Testing! 🎯**
