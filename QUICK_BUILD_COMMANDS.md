# Quick Build Commands Reference

## One-Command Build

```bash
# Just run this:
BUILD.bat
```

The script will:
1. Check prerequisites
2. Install dependencies
3. Create necessary folders
4. Clean previous build
5. Build the executable
6. Offer to open dist folder

---

## Manual Build Steps

If you prefer manual control:

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Install dependencies
pip install -r requirements.txt

# 3. Build executable
pyinstaller build.spec

# 4. Test executable
cd dist
TestTrace.exe
```

---

## Clean Build

Remove all build artifacts and rebuild:

```bash
# Clean
rmdir /s /q build dist

# Rebuild
pyinstaller build.spec
```

---

## Test Before Building

Always test the Python version first:

```bash
python main.py
```

Test all features, then build.

---

## Verify Build Success

After building, verify:

```bash
# Check file exists
dir dist\TestTrace.exe

# Run it
cd dist
TestTrace.exe
```

---

## Distribution Steps

After successful build:

```bash
# 1. Create distribution folder
mkdir TestTrace_v1.0

# 2. Copy executable
copy dist\TestTrace.exe TestTrace_v1.0\

# 3. Copy README
copy USER_README.txt TestTrace_v1.0\README.txt

# 4. Create config folder
mkdir TestTrace_v1.0\config

# 5. Zip it
# Right-click → Send to → Compressed folder
```

---

## Expected Build Time

- Build time: 1-3 minutes
- Output size: 50-80 MB
- Single file: dist\TestTrace.exe

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| PyInstaller not found | `pip install pyinstaller` |
| Permission denied | Run as Administrator |
| Missing module | `pip install -r requirements.txt` |
| Build fails | Check error message, add to hiddenimports |
| File too large | Normal for Python apps (50-80 MB) |
| Antivirus blocks | Add exclusion or sign the exe |

---

## Build Command Options

### Standard Build (use build.spec)
```bash
pyinstaller build.spec
```

### Alternative: Command Line Build
```bash
pyinstaller --onefile --noconsole --name=TestTrace --add-data="config;config" main.py
```

### Debug Build (with console)
```bash
pyinstaller --onefile --console --name=TestTrace_Debug main.py
```

---

## Output Location

```
dist/
└── TestTrace.exe  ← Your executable here!
```

---

## Ready to Distribute!

After building:
1. Test TestTrace.exe
2. Copy to distribution folder
3. Add README.txt
4. Zip and share!

---

## Need Help?

See: BUILD_EXE_GUIDE.md (detailed guide)
