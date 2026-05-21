# Quick Start Guide - GuardRail PII Scrambler

## 🚀 Installation & Setup

### Step 1: Create Project Structure
Run the setup script to create the required directories and files:

**Option A (Recommended - Python):**
```bash
python init_project.py
```

**Option B (Manual - Windows):**
```bash
mkdir templates
mkdir static
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download spaCy NLP Model
```bash
python -m spacy download en_core_web_sm
```

### Step 4: Start the Server
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 5: Open in Browser
Navigate to: **http://localhost:5000**

---

## 📝 Usage

### Basic Workflow
1. **Paste sensitive data** in the left textarea
2. **Click "🔐 Scramble Data"** button
3. **Copy the output** using "📋 Copy Output" button
4. **Clear** with "🗑️ Clear All" when done

### Example Input
```
PATIENT RECORD
==============
Name: Dr. Sarah Johnson
Patient ID: 8905021234567
Email: sarah.johnson@healthcare.com
Phone: 082 123 4567
Medical Aid: MED20240515
Insurance ID: SA123456
Diagnosis: E11.9 (Type 2 Diabetes)
Location: Sandton Medical Center
```

### Example Output
```
PATIENT RECORD
==============
Name: Michael Chen
Patient ID: 5627394812065
Email: marcus.williams@gmail.com
Phone: 083 876 2341
Medical Aid: RXVWQP234
Insurance ID: ZA987654
Diagnosis: T15.42 (Corneal foreign body)
Location: Durban
```

---

## 🔧 Masked Data Types

### Regex Patterns (First Pass)
- ✉️ **Emails** → `faker.email()`
- 📱 **SA Phone Numbers** → `082 XXX XXXX` format
- 🆔 **13-digit SA IDs** → Random 13-digit string
- 🏥 **Medical Aid Numbers** → Random alphanumeric (7-9 chars)
- 📋 **ICD-10 Codes** → Random valid format (e.g., E11.9)

### NLP Entity Recognition (Second Pass - spaCy)
- 👤 **PERSON** → Random first/last name
- 📍 **GPE, LOC, FAC** → Random city/location

---

## ⚙️ Configuration

### Modify Regex Patterns
Edit these functions in `app.py`:
```python
def scramble_emails(text):          # Lines ~80-82
def scramble_sa_phone(text):        # Lines ~84-86
def scramble_sa_id(text):           # Lines ~88-90
def scramble_medical_aid(text):     # Lines ~92-94
def scramble_icd10(text):           # Lines ~96-99
```

### Modify NLP Behavior
Edit `apply_nlp_masking()` function (lines ~101-120):
```python
if ent.label_ == 'PERSON':
    # Change fake.name() to something else
    replacement = fake.name()
```

### Adjust Faker Locale
Currently set to South African (en_ZA). Change in `app.py` line 11:
```python
fake = Faker('en_ZA')  # Change to 'en_US', 'en_GB', etc.
```

---

## 🔒 Security & Privacy

✅ **100% Offline** - No external API calls  
✅ **No Data Storage** - Everything processed in memory  
✅ **No Logs** - Disable Flask debug in production  
✅ **Browser Only** - Data never leaves your machine  

### For Production Use
1. Disable Flask debug mode
2. Use HTTPS
3. Add authentication if needed
4. Consider data retention policies
5. Test thoroughly before production

---

## 🐛 Troubleshooting

### spaCy Model Not Found
```
OSError: [E050] Can't find model 'en_core_web_sm'
```
**Fix:** Run `python -m spacy download en_core_web_sm`

### Port 5000 Already in Use
```
Address already in use
```
**Fix:** Edit `app.py` line 238, change port:
```python
app.run(debug=True, port=5001)  # Use 5001 instead
```

### Module Not Found (Flask, Faker, spacy)
```
ModuleNotFoundError: No module named 'flask'
```
**Fix:** Install dependencies: `pip install -r requirements.txt`

### HTML File Not Found
```
jinja2.exceptions.TemplateNotFound: index.html
```
**Fix:** Run `python init_project.py` to create `templates/index.html`

---

## 📊 Performance Tips

- **Large Texts** - NLP processing slows with text size (100KB+ may take seconds)
- **Batch Processing** - Consider splitting very large files
- **Local SSD** - Faster spaCy model loading on SSD

---

## 📚 Architecture Overview

```
GuardRailScrambler/
├── app.py                 # Flask backend (231 lines)
│   ├── Regex scrambling (5 patterns)
│   ├── NLP masking (spaCy)
│   └── /scramble endpoint
│
├── templates/
│   └── index.html         # Frontend UI (HTML + CSS + JS)
│       ├── Flexbox layout (dark mode)
│       ├── Textarea inputs
│       └── Copy/Clear buttons
│
├── requirements.txt       # Dependencies
├── init_project.py        # Setup script
├── create_html.py         # HTML generator
├── setup.py              # Alternative setup
└── README.md             # Full documentation
```

### Data Flow
```
User Input (Textarea)
    ↓
JavaScript (Fetch API)
    ↓
Flask Backend (/scramble)
    ↓
Regex Scrambling (Step 1)
    ↓
spaCy NLP Processing (Step 2)
    ↓
Return Masked Output
    ↓
Display in Output Textarea
```

---

## 💡 Tips & Tricks

### Batch Multiple Entries
Paste multiple patient records separated by `---` and process together

### Preserve Formatting
JSON and SQL structures are preserved - only values are changed

### Test with Examples
Use the placeholder text to test basic functionality first

### Export Results
Use Copy button or select all (`Ctrl+A`) and copy manually

---

## 📞 Support

For issues, check:
1. README.md - Full documentation
2. Dependencies installed? `pip list | grep -E "Flask|Faker|spacy"`
3. spaCy model? `python -c "import spacy; spacy.load('en_core_web_sm')"`
4. Port available? Try a different port (5001, 5002, etc.)

---

## 🎯 Next Steps

- [ ] Run `python init_project.py`
- [ ] Install `pip install -r requirements.txt`
- [ ] Download model `python -m spacy download en_core_web_sm`
- [ ] Start server `python app.py`
- [ ] Test at `http://localhost:5000`

Happy masking! 🛡️
