# How to Build TestTrace Recorder as .EXE

## Complete Step-by-Step Guide

This guide will walk you through converting your TestTrace Recorder Python application into a standalone Windows executable (.exe) file that can be distributed to users.

---

## Prerequisites

Before building the .exe, ensure you have:

1. **Python 3.7+ installed**
2. **All dependencies installed** (from requirements.txt)
3. **Windows operating system** (the .exe will only work on Windows)
4. **Administrator access** (for PyInstaller)

---

## Step 1: Install PyInstaller

PyInstaller is the tool that converts Python applications to executables.

### Option A: Install via pip (Recommended)

```bash
pip install pyinstaller
```

### Option B: Install specific version (if needed)

```bash
pip install pyinstaller==6.1.0
```

### Verify Installation

```bash
pyinstaller --version
```

Expected output: `6.x.x` (or similar version number)

---

## Step 2: Prepare Your Application

### 2.1 Ensure All Dependencies Are Listed

Check your `requirements.txt`:

```bash
cat requirements.txt
```

Should contain:
```
PyQt5>=5.15.0
mss>=9.0.0
Pillow>=10.0.0
pynput>=1.7.0
keyboard>=0.13.0
python-docx>=1.0.0
pywin32>=305.1
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

### 2.2 Create Required Folders

Ensure these folders exist:

```bash
# Create folders if they don't exist
mkdir config
mkdir assets
mkdir output
mkdir temp_sessions
```

### 2.3 Create Default Settings File

Create `config/settings.json` with default values:

```json
{
  "output_dir": null,
  "auto_capture_on_click": false,
  "capture_delay_ms": 200,
  "hotkey_capture": "F8",
  "hotkey_stop": "F9",
  "highlight_color": "#FF0000",
  "highlight_opacity": 0.3,
  "tester_name": "",
  "last_module": "",
  "last_environment": ""
}
```

### 2.4 Add Application Icon (Optional)

If you want a custom icon for your .exe:

1. Create or download an icon file
2. Save it as `assets/icon.ico`
3. Recommended size: 256x256 pixels
4. Must be .ico format (not .png or .jpg)

**To convert PNG to ICO:**
- Use online tool: https://convertico.com/
- Or use ImageMagick: `convert icon.png icon.ico`

---

## Step 3: Test Application Before Building

**Important:** Always test that your application runs correctly before building the .exe.

```bash
# Run the application
python main.py
```

**Test Checklist:**
- [ ] Application launches successfully
- [ ] Control panel appears
- [ ] Can start recording
- [ ] Can capture steps (F8)
- [ ] Can generate report
- [ ] Application exits cleanly

If any test fails, fix the issues before building the .exe.

---

## Step 4: Build the Executable

### Method 1: Using the Provided build.spec (Recommended)

Your application already has a `build.spec` file configured. Use it for a professional build.

```bash
# Build using the spec file
pyinstaller build.spec
```

This will:
- ✅ Create a single .exe file
- ✅ Include all dependencies
- ✅ Bundle config and assets folders
- ✅ Add custom icon (if present)
- ✅ Request admin privileges (for global hooks)
- ✅ Run without console window

### Method 2: Using Command Line (Alternative)

If you want to customize the build:

```bash
# Single file, no console, with icon
pyinstaller --onefile --noconsole --icon=assets/icon.ico --name=TestTrace --add-data="config;config" --add-data="assets;assets" --uac-admin main.py
```

**Parameters explained:**
- `--onefile`: Creates a single .exe file
- `--noconsole`: Hides the console window
- `--icon=assets/icon.ico`: Sets custom icon
- `--name=TestTrace`: Names the output file
- `--add-data="config;config"`: Includes config folder
- `--add-data="assets;assets"`: Includes assets folder
- `--uac-admin`: Requests admin privileges
- `main.py`: Entry point script

---

## Step 5: Monitor the Build Process

### What You'll See

The build process takes 1-3 minutes. You'll see:

```
 Building EXE from EXE-00.toc completed successfully.
```

### Build Output Location

After successful build:

```
dist/
└── TestTrace.exe    ← Your executable!
```

### Build Artifacts (Can Delete Later)

```
build/               ← Temporary build files (can delete)
dist/                ← Contains your .exe
*.spec               ← Build specification (keep)
```

---

## Step 6: Test the Executable

### 6.1 Navigate to dist folder

```bash
cd dist
```

### 6.2 Run the executable

```bash
TestTrace.exe
```

**Or double-click `TestTrace.exe` in File Explorer**

### 6.3 Verify Functionality

Test all features work in the .exe:

- [ ] Application launches
- [ ] Control panel visible
- [ ] Can start recording
- [ ] F8 capture works
- [ ] Highlight button works
- [ ] Stop & Report works
- [ ] Report saves to Downloads
- [ ] Application exits cleanly

**Important:** Test on a different machine to ensure portability.

---

## Step 7: Distribution

### Create Distribution Package

Create a folder for distribution:

```bash
# Create distribution folder
mkdir TestTrace_v1.0

# Copy executable
copy dist\TestTrace.exe TestTrace_v1.0\

# Create necessary folders
mkdir TestTrace_v1.0\config
mkdir TestTrace_v1.0\assets

# Create default config
echo {
  "output_dir": null,
  "auto_capture_on_click": false,
  "capture_delay_ms": 200,
  "hotkey_capture": "F8",
  "hotkey_stop": "F9",
  "highlight_color": "#FF0000",
  "highlight_opacity": 0.3,
  "tester_name": "",
  "last_module": "",
  "last_environment": ""
} > TestTrace_v1.0\config\settings.json

# Create README for users
echo TestTrace Recorder v1.0 > TestTrace_v1.0\README.txt
echo. >> TestTrace_v1.0\README.txt
echo Usage: >> TestTrace_v1.0\README.txt
echo 1. Double-click TestTrace.exe to launch >> TestTrace_v1.0\README.txt
echo 2. Click "Start" to begin recording >> TestTrace_v1.0\README.txt
echo 3. Press F8 or click "Highlight" to capture steps >> TestTrace_v1.0\README.txt
echo 4. Click "Stop & Report" to generate Word document >> TestTrace_v1.0\README.txt
echo. >> TestTrace_v1.0\README.txt
echo Reports are saved to your Downloads folder. >> TestTrace_v1.0\README.txt
```

### Zip the Distribution

```bash
# Compress for distribution
tar -a -c -f TestTrace_v1.0.zip TestTrace_v1.0
```

**Or right-click → Send to → Compressed (zipped) folder**

---

## Step 8: User Installation Instructions

Create an `INSTALL.txt` file for your users:

```
TestTrace Recorder - Installation Guide
========================================

Installation Steps:
-------------------
1. Extract TestTrace_v1.0.zip to any folder (e.g., C:\TestTrace)
2. Double-click TestTrace.exe to launch
3. If prompted by Windows Defender, click "More info" → "Run anyway"
4. The application will start with a floating control panel

System Requirements:
--------------------
- Windows 10 or later
- Microsoft Word installed (for opening reports)
- Administrator privileges (for global hotkeys)

First Run:
----------
1. Click "Start" button
2. Fill in test case details
3. Click "Start Recording"
4. Press F8 to capture steps
5. Click "Stop & Report" when done
6. Reports will be in your Downloads folder

Troubleshooting:
----------------
- If F8/F9 don't work: Run as Administrator
- If Windows blocks the app: Right-click → Properties → Unblock
- If no reports generated: Check Downloads folder

Contact: [Your contact information]
```

---

## Step 9: Advanced Build Options

### 9.1 Reduce File Size

If the .exe is too large (100+ MB), exclude unnecessary modules:

Create `build-minimal.spec`:

```python
a = Analysis(
    ['main.py'],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'pytest',
    ],
    # ... rest of config
)
```

Build with:
```bash
pyinstaller build-minimal.spec
```

### 9.2 Add Version Information

Create `version.txt`:

```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'Your Company'),
           StringStruct(u'FileDescription', u'TestTrace Recorder'),
           StringStruct(u'FileVersion', u'1.0.0.0'),
           StringStruct(u'ProductName', u'TestTrace'),
           StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]
    )
  ]
)
```

Build with version:
```bash
pyinstaller --version-file=version.txt build.spec
```

### 9.3 Sign the Executable (Professional)

For professional distribution, sign the .exe:

```bash
# Install signtool (part of Windows SDK)
# Then sign:
signtool sign /f certificate.pfx /p password TestTrace.exe
```

---

## Step 10: Troubleshooting Build Issues

### Issue 1: Missing Module Errors

**Error:**
```
ModuleNotFoundError: No module named 'xxx'
```

**Solution:**
Add to `hiddenimports` in build.spec:

```python
hiddenimports=[
    'pynput.keyboard._win32',
    'pynput.mouse._win32',
    'missing_module_name',  # Add here
],
```

### Issue 2: Permission Denied

**Error:**
```
PermissionError: [WinError 5] Access is denied
```

**Solution:**
Run command prompt as Administrator:
- Right-click CMD → Run as administrator
- Navigate to your project
- Run pyinstaller command

### Issue 3: File Too Large

**If .exe > 100 MB:**

**Solution 1:** Exclude tests
```python
excludes=['tests', 'pytest', 'unittest'],
```

**Solution 2:** Use UPX compression
```python
upx=True,  # Already in build.spec
```

**Solution 3:** Build without --onefile (creates folder)

```bash
pyinstaller --noonefile build.spec
```

### Issue 4: Antivirus Blocking

**Error:** Windows Defender blocks .exe

**Solution:**
1. Add exclusion in Windows Defender
2. Or sign the executable (see Step 9.3)
3. Or submit to Microsoft for whitelisting

### Issue 5: Icon Not Showing

**Issue:** Custom icon doesn't appear

**Solution:**
- Ensure icon is .ico format
- Check file exists: `assets/icon.ico`
- Verify path in build.spec
- Clear build cache: `rmdir /s /q build dist`

---

## Complete Build Script

Create `BUILD.bat` for easy building:

```batch
@echo off
echo ========================================
echo TestTrace Recorder Build Script
echo ========================================
echo.

echo [1/5] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo Clean complete.

echo.
echo [2/5] Checking dependencies...
pip install -r requirements.txt
echo Dependencies installed.

echo.
echo [3/5] Creating necessary folders...
if not exist config mkdir config
if not exist assets mkdir assets
if not exist output mkdir output
if not exist temp_sessions mkdir temp_sessions

echo.
echo [4/5] Building executable...
pyinstaller build.spec
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Build failed!
    ========================================
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo [5/5] Build successful!
echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable location: dist\TestTrace.exe
echo.
echo Test it by running:
echo   cd dist
echo   TestTrace.exe
echo.
pause
```

Run with:
```bash
BUILD.bat
```

---

## Distribution Checklist

Before distributing to users:

- [ ] Build completed successfully
- [ ] Executable tested on your machine
- [ ] Executable tested on different machine
- [ ] All features work (Start, Capture, Report)
- [ ] Reports save to Downloads correctly
- [ ] Application exits cleanly
- [ ] No error messages
- [ ] Created README.txt
- [ ] Created INSTALL.txt
- [ ] Zipped distribution package
- [ ] Tested unzip and run

---

## File Size Expectations

Expected .exe file size:
- **Minimum:** 30-50 MB (with minimal dependencies)
- **Typical:** 50-80 MB (all features)
- **Maximum:** 100-150 MB (includes everything)

This is normal for Python applications with GUI frameworks.

---

## Quick Build Commands

```bash
# Clean previous builds
rmdir /s /q build dist

# Install dependencies
pip install -r requirements.txt

# Build executable
pyinstaller build.spec

# Test executable
cd dist
TestTrace.exe
```

---

## What Happens During Build

PyInstaller performs these steps:

1. **Analysis:** Scans your code for imports
2. **Collecting:** Gathers all Python modules
3. **Bundling:** Packages everything into .exe
4. **Optimization:** Reduces size with UPX
5. **Finalizing:** Creates executable in dist/

---

## Summary

**Build Command:**
```bash
pyinstaller build.spec
```

**Output:**
```
dist/TestTrace.exe
```

**Distribute:**
1. Create distribution folder
2. Add README.txt
3. Zip and share with users

**User runs:**
- Extract zip
- Double-click TestTrace.exe
- Application starts!

---

## Need Help?

If build fails:
1. Check error messages
2. Verify all dependencies installed
3. Try cleaning build: `rmdir /s /q build dist`
4. Run as Administrator
5. Check PyInstaller docs: https://pyinstaller.org/

---

## Final Notes

- **Build time:** 1-3 minutes
- **File size:** 50-80 MB typical
- **Compatibility:** Windows 10/11
- **Dependencies:** None required on user's machine
- **Installation:** Just run the .exe!

Your TestTrace Recorder is ready for distribution! 🎉
