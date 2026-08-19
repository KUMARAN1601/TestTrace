# TestTrace Recorder - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run Application

```bash
python main.py
```

### Step 3: Record Your First Test

1. Click **"Start"** in the floating control panel
2. Fill in test case details (TC ID, Name, Tester Name)
3. Click **"Start Recording"**
4. Perform your test - screenshots capture automatically
5. For each capture: draw highlight → add description → select Pass/Fail
6. Press **F9** or click **"Stop"** when done
7. Review steps and click **"Generate Report"**
8. Find your evidence report in the `output/` folder!

---

## 📋 Essential Hotkeys

- **F8** - Manual capture
- **F9** - Stop and review
- **F10** - Pause/Resume
- **Esc** - Skip annotation

---

## 🏗️ Build Standalone .exe

```bash
pyinstaller build.spec
```

Output: `dist/TestTrace.exe` (single file, ~50-80MB)

---

## ⚠️ Common Issues

**Hotkeys not working?**
→ Run as Administrator

**Can't capture screenshots?**
→ Check screen capture permissions

**Dependencies missing?**
→ `pip install -r requirements.txt`

---

## 📁 Where Files Are Saved

- **Evidence reports**: `output/` folder
- **Screenshots**: `temp_sessions/` (temporary)
- **Settings**: `config/settings.json`

---

**Need more help?** See full README.md
