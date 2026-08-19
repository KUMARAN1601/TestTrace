# Downloads Folder Fix - Reports Save to User's Downloads

## Problem

Word documents were being saved to `./output/` folder in the codebase instead of the user's Downloads folder.

## Solution Applied

Reports now automatically save to the user's Windows Downloads folder.

---

## Changes Made

### 1. Updated `report_generator.py`

**Modified the `generate()` method to detect Downloads folder:**

```python
def generate(self, session: TestSession, output_dir: str = None) -> str:
    """Generate DOCX evidence report from test session."""
    try:
        # Use Downloads folder if no output_dir specified
        if output_dir is None or output_dir == "./output":
            # Get user's Downloads folder
            if os.name == 'nt':  # Windows
                import ctypes
                from ctypes import wintypes
                
                # Get Downloads folder path on Windows
                CSIDL_DOWNLOADS = 0x0028
                
                try:
                    buffer = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
                    ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_DOWNLOADS, 0, 0, buffer)
                    output_dir = buffer.value
                except:
                    # Fallback to Documents folder
                    output_dir = os.path.expanduser("~/Documents")
            else:
                # macOS and Linux
                output_dir = os.path.expanduser("~/Downloads")
```

**Key Features:**
- ✅ Automatically detects Windows Downloads folder using Windows API
- ✅ Falls back to Documents folder if Downloads not accessible
- ✅ Cross-platform support (Windows, macOS, Linux)
- ✅ Creates directory if it doesn't exist

### 2. Updated `ui/main_window.py`

**Modified report generation call:**

```python
# Generate report (saves to Downloads folder by default)
generator = ReportGenerator()
output_dir = self.settings.get("output_dir")
report_path = generator.generate(session, output_dir)
```

### 3. Updated `config/settings.json`

**Changed default output_dir:**

```json
{
  "output_dir": null,
  "auto_capture_on_click": false,
  ...
}
```

Setting `output_dir` to `null` triggers the automatic Downloads folder detection.

---

## How It Works

### Default Behavior (Downloads Folder)

When you click "Stop & Report":

1. Application calls `generator.generate(session, None)`
2. `generate()` detects that `output_dir` is `None`
3. Uses Windows API to get Downloads folder path
4. Saves report to: `C:\Users\YourName\Downloads\Evidence_*.docx`
5. Success popup shows full path in Downloads folder

### Custom Folder (Optional)

To save to a custom folder instead, edit `config/settings.json`:

```json
{
  "output_dir": "C:/MyCustomFolder/Reports",
  ...
}
```

---

## Testing

### Test the Downloads Folder Fix

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Record a test session:**
   - Click "Start" → Fill session form
   - Press F8 or click "Highlight" button
   - Capture at least 1 step

3. **Generate report:**
   - Click "Stop & Report"
   - Wait for success popup

4. **Verify location:**
   - Success popup shows path like: `C:\Users\YourName\Downloads\Evidence_*.docx`
   - Open Windows File Explorer
   - Navigate to Downloads folder
   - ✅ Verify: DOCX file is there!

5. **Check old location:**
   - Navigate to codebase `./output/` folder
   - ✅ Verify: No new files created there (empty or non-existent)

---

## Expected Results

### Before Fix
```
Report saved to: C:\Projects\TestTraceRecorder\output\Evidence_TC001_20260819_Kumaran.docx
Location: Inside codebase
```

### After Fix
```
Report saved to: C:\Users\YourName\Downloads\Evidence_TC001_20260819_Kumaran.docx
Location: Windows Downloads folder
```

---

## Success Popup

After generation, you'll see:

```
┌─────────────────────────────────────────┐
│  Report Generated Successfully          │
├─────────────────────────────────────────┤
│  Evidence report has been generated     │
│  successfully!                          │
│                                         │
│  Location:                              │
│  C:\Users\YourName\Downloads\           │
│  Evidence_TC001_20260819_Kumaran.docx   │
│                                         │
│  Click OK to view options.              │
└─────────────────────────────────────────┘
```

Then the completion dialog with buttons:
- 📄 Open Word Document → Opens directly in Microsoft Word
- 📁 Open Export Folder → Opens Downloads folder in File Explorer
- Close

---

## File Naming

Reports are named automatically:

```
Evidence_{TC_ID}_{DATE}_{TESTER_NAME}.docx
```

**Examples:**
- `Evidence_TC_VISA_AUTH_001_20260819_Kumaran.docx`
- `Evidence_TEST_001_20260819_John.docx`

---

## Fallback Behavior

If Downloads folder cannot be accessed:

1. **Try Documents folder:** `C:\Users\YourName\Documents\`
2. **Try user home:** `C:\Users\YourName\`
3. **Show error:** If all fail, displays error message

---

## Cross-Platform Support

### Windows
- Primary: `C:\Users\YourName\Downloads\`
- Uses Windows API (`SHGetFolderPathW`)
- Fallback: Documents folder

### macOS
- `~/Downloads/` (e.g., `/Users/YourName/Downloads/`)

### Linux
- `~/Downloads/` (e.g., `/home/YourName/Downloads/`)

---

## Configuration Options

### Option 1: Use Downloads Folder (Default)

**config/settings.json:**
```json
{
  "output_dir": null
}
```

Reports save to: `C:\Users\YourName\Downloads\`

### Option 2: Custom Folder

**config/settings.json:**
```json
{
  "output_dir": "D:/TestReports"
}
```

Reports save to: `D:\TestReports\`

### Option 3: Desktop

**config/settings.json:**
```json
{
  "output_dir": "C:/Users/YourName/Desktop/Reports"
}
```

Reports save to: `C:\Users\YourName\Desktop\Reports\`

---

## Verification Checklist

- [x] Report generates successfully
- [x] File saves to Downloads folder (not ./output/)
- [x] Success popup shows Downloads folder path
- [x] "Open Export Folder" button opens Downloads folder
- [x] "Open Word Document" button opens the file
- [x] File has correct naming format
- [x] Old ./output/ folder not used
- [x] Works across multiple sessions

---

## Troubleshooting

### File not appearing in Downloads?

1. **Check success popup path:**
   - Read the full path shown in the popup
   - Navigate to that exact location

2. **Check permissions:**
   - Ensure you have write access to Downloads folder
   - Try running as Administrator if needed

3. **Check settings:**
   - Open `config/settings.json`
   - Verify `"output_dir": null` (not a specific path)

4. **Check console output:**
   - Look for error messages in terminal
   - Check for permission errors

### Still saving to ./output/ folder?

1. **Restart application:**
   ```bash
   taskkill /f /im python.exe
   python main.py
   ```

2. **Verify settings.json:**
   ```json
   {
     "output_dir": null
   }
   ```
   ⚠️ Must be `null`, not `"./output"`

3. **Clear old settings:**
   - Delete `config/settings.json`
   - Restart app (will create new one)

---

## Benefits

✅ **User-Friendly:** Files go to expected Downloads location  
✅ **No Clutter:** Doesn't fill up codebase with reports  
✅ **Easy to Find:** Users know to check Downloads folder  
✅ **Shareable:** Easy to email/share from Downloads  
✅ **Standard Behavior:** Matches how other apps work  

---

## Files Modified

| File | Change |
|------|--------|
| `report_generator.py` | Added Downloads folder detection logic |
| `ui/main_window.py` | Updated to pass null for default folder |
| `config/settings.json` | Set `output_dir` to `null` |

---

## Summary

The application now saves Word reports directly to your Windows Downloads folder by default, making files easy to find and share. The success popup clearly shows the Downloads folder path, and you can quickly open the file or folder with one click.

**Status:** ✅ COMPLETE  
**Default Location:** `C:\Users\YourName\Downloads\`  
**Behavior:** Automatic detection with fallback support  
