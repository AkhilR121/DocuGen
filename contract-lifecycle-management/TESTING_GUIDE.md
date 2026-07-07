# Testing Guide - Open-Source Contract Generation POC

## Current System Status ✅

### Pre-requisites Verification

| Component | Status | Version | Notes |
|-----------|--------|---------|-------|
| **Python** | ✅ Installed | 3.14.6 | Required: 3.11+ |
| **pip** | ✅ Installed | 26.1.2 | Package manager |
| **LibreOffice** | ✅ Installed | 26.2.4.2 | Path: `C:\Program Files\LibreOffice\program\soffice.com` |
| **docxtpl** | ✅ Installed | 0.17.0 | Template engine |
| **python-docx** | ✅ Installed | 1.2.0 | DOCX manipulation |
| **jinja2** | ✅ Installed | 3.1.2 | Template engine (required by docxtpl) |
| **Template File** | ✅ Present | - | `assets/templates/pc-template.docx` |
| **Output Directory** | ✅ Exists | - | `output/` |

---

## Dependency Conflict Resolution ⚠️

**Issue**: The original `requirements.txt` had a version conflict:
- `docxtpl==0.17.0` requires `python-docx>=1.1.1`
- But `requirements.txt` specified `python-docx==1.1.0` ❌

**Fix Applied**: Updated `requirements.txt` to use `python-docx>=1.1.1` ✅

**Current Status**: You already have `python-docx==1.2.0` installed, which satisfies the requirement.

### Install/Update Dependencies

```bash
# Install or update all requirements
pip install -r requirements.txt
```

---

## Commands for Version Checking

**IMPORTANT**: These commands are for **Git Bash** or **WSL Bash**.  
For **PowerShell** commands, see [POWERSHELL_COMMANDS.md](POWERSHELL_COMMANDS.md)

### 1. Check Python Version
```bash
python --version
```
**Expected**: Python 3.11 or higher ✅ (You have 3.14.6)

### 2. Check pip Version
```bash
pip --version
```

### 3. Check LibreOffice Version
```bash
# Method 1: Using soffice.com
"C:\Program Files\LibreOffice\program\soffice.com" --version

# Method 2: Using soffice.bin
"C:\Program Files\LibreOffice\program\soffice.bin" --version
```
**Your Version**: LibreOffice 26.2.4.2 ✅

### 4. Check Installed Python Packages
```bash
# List all packages
pip list

# Check specific packages
pip list | grep -E "docxtpl|python-docx|jinja2"

# Check detailed info for a package
pip show docxtpl
pip show python-docx
pip show jinja2
```

### 5. Verify Project Structure
```bash
# Check template exists
ls -la assets/templates/pc-template.docx

# Check output directory
ls -la output/

# Check scripts exist
ls -la scripts/
```

---

## Step-by-Step Testing Commands

### Step 1: Install Missing Dependencies (if any)

```bash
# Navigate to project directory
cd c:\Users\Technoidentity\Desktop\contract-lifecycle-management

# Install all requirements
pip install -r requirements.txt
```

**Expected Output** (if packages need installation):
```
Successfully installed docxtpl-0.17.0 python-docx-1.1.2 jinja2-3.1.2
```

**Or** (if already installed):
```
Requirement already satisfied: docxtpl==0.17.0
Requirement already satisfied: python-docx>=1.1.1
Requirement already satisfied: jinja2==3.1.2
```

### Step 2: Verify All Dependencies

```bash
pip list | grep -E "docxtpl|python-docx|jinja2"
```

**Expected Output**:
```
docxtpl           0.17.0
jinja2            3.1.2
python-docx       1.2.0 (or any version >= 1.1.1)
```

### Step 3: Run the Open-Source Script

```bash
python scripts/generate_contract_open_source.py
```

### Step 4: Monitor Output and Timing

The script will display:
1. **Template Loading Time**
2. **DOCX Generation Time** (including data population and table insertion)
3. **PDF Conversion Time** (LibreOffice headless conversion)
4. **Total Time**

**Example Expected Output**:
```
================================================================================
CLM POC - OPEN-SOURCE APPROACH
Library: docxtpl (Jinja2) + LibreOffice
================================================================================

[1/4] Loading template: assets/templates/pc-template.docx
[OK] Template loaded

[2/4] Populating data and generating DOCX...
      Customer: Test Customer One
      Location: Houston, Texas
      Period: 07/01/2026 - 06/30/2027
      Inserted sites table with 3 rows
[OK] DOCX generated: output/contract_opensource_20260707_HHMMSS.docx
      Time taken: X.XXX seconds

[3/4] Converting DOCX to PDF using LibreOffice...
      Executing LibreOffice conversion...
[OK] PDF generated: output/contract_opensource_20260707_HHMMSS.pdf
      Time taken: X.XXX seconds

================================================================================
GENERATION COMPLETE - OPEN-SOURCE APPROACH
================================================================================

Performance Metrics:
  DOCX Generation:    X.XXX seconds
  PDF Conversion:     X.XXX seconds
  Total Time:         X.XXX seconds

Generated Files:
  DOCX: C:\Users\Technoidentity\Desktop\contract-lifecycle-management\output\contract_opensource_YYYYMMDD_HHMMSS.docx
  PDF:  C:\Users\Technoidentity\Desktop\contract-lifecycle-management\output\contract_opensource_YYYYMMDD_HHMMSS.pdf
```

### Step 5: Verify Generated Files

```bash
# List files in output directory
ls -la output/

# Check file sizes
ls -lh output/contract_opensource_*.docx
ls -lh output/contract_opensource_*.pdf

# View the latest generated files
ls -lt output/ | head -5
```

### Step 6: Open and Verify Documents

```bash
# Open DOCX file (Windows)
start output/contract_opensource_<timestamp>.docx

# Open PDF file (Windows)
start output/contract_opensource_<timestamp>.pdf
```

---

## Performance Benchmarking Commands

### Run Multiple Tests to Get Average Timing

Create a test script or run manually 3 times:

```bash
# Test 1
python scripts/generate_contract_open_source.py > test_run_1.log 2>&1

# Test 2
python scripts/generate_contract_open_source.py > test_run_2.log 2>&1

# Test 3
python scripts/generate_contract_open_source.py > test_run_3.log 2>&1

# Extract timing data
grep "Time taken:" test_run_*.log
grep "Total Time:" test_run_*.log
```

### Expected Performance (Based on POC Design)

| Operation | Expected Time Range |
|-----------|-------------------|
| **Template Loading** | < 0.1 seconds |
| **DOCX Generation** | 1-2 seconds |
| **Sites Table Insertion** | < 0.5 seconds |
| **PDF Conversion (LibreOffice)** | 3-5 seconds |
| **Total Pipeline** | **4-7 seconds** |

---

## Troubleshooting Commands

### Issue 1: LibreOffice Not Found

```bash
# Find LibreOffice installation
where soffice 2>nul || dir "C:\Program Files\LibreOffice" /s /b | findstr soffice.exe

# Test LibreOffice headless conversion manually
"C:\Program Files\LibreOffice\program\soffice.com" --headless --convert-to pdf --outdir output/ output/test.docx
```

### Issue 2: Template Not Found

```bash
# Check if template exists
ls -la assets/templates/pc-template.docx

# If missing, check alternate locations
find . -name "pc-template.docx" 2>/dev/null
```

### Issue 3: Import Errors

```bash
# Test imports interactively
python -c "from docxtpl import DocxTemplate; print('docxtpl OK')"
python -c "from docx import Document; print('python-docx OK')"
python -c "import jinja2; print('jinja2 OK')"
```

### Issue 4: PDF Conversion Fails

```bash
# Check LibreOffice process
tasklist | findstr soffice

# Kill hung LibreOffice processes (if any)
taskkill /F /IM soffice.bin /T 2>nul
taskkill /F /IM soffice.exe /T 2>nul

# Retry conversion
python scripts/generate_contract_open_source.py
```

---

## Testing Checklist

Before running the test:
- [ ] Python 3.11+ installed and verified
- [ ] LibreOffice installed and version checked
- [ ] All Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Template file exists at `assets/templates/pc-template.docx`
- [ ] Output directory exists or will be auto-created
- [ ] No hung LibreOffice processes running

During the test:
- [ ] Script starts without errors
- [ ] Template loads successfully
- [ ] DOCX file is generated
- [ ] Sites table is inserted (3 rows expected)
- [ ] PDF conversion completes successfully
- [ ] Performance metrics are displayed

After the test:
- [ ] Both DOCX and PDF files exist in `output/` directory
- [ ] Files can be opened without corruption
- [ ] Document contains all placeholder data populated
- [ ] Sites table is properly formatted
- [ ] Record the timing metrics for comparison

---

## Recording Test Results

### Template for Test Notes

```
Test Date: _____________
Test Run: #_____
LibreOffice Version: 26.2.4.2
Python Version: 3.14.6

Performance Results:
- DOCX Generation Time: _______ seconds
- PDF Conversion Time: _______ seconds
- Total Time: _______ seconds

File Sizes:
- DOCX: _______ KB
- PDF: _______ KB

Quality Check:
- [ ] All placeholders replaced correctly
- [ ] Sites table formatted properly
- [ ] PDF matches DOCX content
- [ ] No errors or warnings

Notes:
_________________________________________________
_________________________________________________
```

---

## Next Steps After Testing

1. **Compare with Aspose approach** (if needed):
   ```bash
   pip install -r requirements-aspose.txt
   python scripts/generate_contract_aspose.py
   ```

2. **Test API server**:
   ```bash
   pip install -r server/requirements.txt
   python server/app.py
   ```

3. **Document findings** in TODO.md or create a separate `TEST_RESULTS.md`

---

## Quick Reference - All Commands in Sequence

```bash
# 1. Verify environment
python --version
"C:\Program Files\LibreOffice\program\soffice.com" --version
pip list | grep -E "docxtpl|python-docx|jinja2"

# 2. Install dependencies (if needed)
pip install -r requirements.txt

# 3. Run test
python scripts/generate_contract_open_source.py

# 4. Verify outputs
ls -la output/
start output/contract_opensource_*.docx
start output/contract_opensource_*.pdf
```

---

**Ready to Test!** 🚀

All prerequisites are satisfied. You can now run:
```bash
python scripts/generate_contract_open_source.py
```
