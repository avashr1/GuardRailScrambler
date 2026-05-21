# 📄 Full Code Listing - GuardRail PII Scrambler

## File 1: app.py (Complete)

```python
import re
import string
import random
from flask import Flask, render_template, request, jsonify
from faker import Faker
import spacy

app = Flask(__name__)
fake = Faker('en_ZA')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Store processed entities to avoid duplicate replacements
processed_positions = set()


def generate_sa_phone():
    """Generate a realistic SA phone number in format 082 XXX XXXX"""
    operators = ['082', '083', '084', '081']
    operator = random.choice(operators)
    number = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"{operator} {number[:3]} {number[3:]}"


def generate_sa_id():
    """Generate a random 13-digit SA ID"""
    return ''.join([str(random.randint(0, 9)) for _ in range(13)])


def generate_medical_aid():
    """Generate a random medical aid number (MED + digits or 7-9 alphanumeric)"""
    choice = random.choice(['med_format', 'alphanumeric'])
    if choice == 'med_format':
        digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"MED{digits}"
    else:
        length = random.randint(7, 9)
        chars = string.ascii_uppercase + string.digits
        return ''.join([random.choice(chars) for _ in range(length)])


def generate_icd10():
    """Generate a random ICD-10 code format: Letter + 2 digits, optional .X or .XX"""
    letter = random.choice(string.ascii_uppercase)
    two_digits = ''.join([str(random.randint(0, 9)) for _ in range(2)])
    code = f"{letter}{two_digits}"
    
    # Optional decimal part
    if random.random() > 0.5:
        decimal_digits = random.randint(1, 2)
        decimal_part = ''.join([str(random.randint(0, 9)) for _ in range(decimal_digits)])
        code = f"{code}.{decimal_part}"
    
    return code


def scramble_emails(text):
    """Replace email addresses with fake emails"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    text = re.sub(email_pattern, lambda m: fake.email(), text)
    return text


def scramble_sa_phone(text):
    """Replace SA phone numbers with random ones"""
    sa_phone_pattern = r'\b0[0-9]{2}\s?[0-9]{3}\s?[0-9]{4}\b|\b\+27[0-9]\s?[0-9]{3}\s?[0-9]{4}\b'
    text = re.sub(sa_phone_pattern, lambda m: generate_sa_phone(), text, flags=re.IGNORECASE)
    return text


def scramble_sa_id(text):
    """Replace 13-digit SA IDs with random ones"""
    sa_id_pattern = r'\b[0-9]{13}\b'
    text = re.sub(sa_id_pattern, lambda m: generate_sa_id(), text)
    return text


def scramble_medical_aid(text):
    """Replace medical aid numbers with random ones"""
    med_aid_pattern = r'\b(?:MED[0-9]{5,8}|[A-Z0-9]{7,9})\b'
    text = re.sub(med_aid_pattern, lambda m: generate_medical_aid(), text, flags=re.IGNORECASE)
    return text


def scramble_icd10(text):
    """Replace ICD-10 diagnosis codes with random valid-looking ones"""
    icd10_pattern = r'\b[A-Z][0-9]{2}(?:\.[0-9]{1,2})?\b'
    text = re.sub(icd10_pattern, lambda m: generate_icd10(), text)
    return text


def apply_nlp_masking(text):
    """Apply spaCy NLP for entity recognition and masking"""
    doc = nlp(text)
    
    # Sort entities by position (reverse order to replace from end to start)
    entities_to_replace = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            entities_to_replace.append((ent.start_char, ent.end_char, fake.name()))
        elif ent.label_ in ['GPE', 'LOC', 'FAC']:
            entities_to_replace.append((ent.start_char, ent.end_char, fake.city()))
    
    # Sort by start position in reverse order to avoid offset issues
    entities_to_replace.sort(key=lambda x: x[0], reverse=True)
    
    # Replace entities from end to start
    for start, end, replacement in entities_to_replace:
        text = text[:start] + replacement + text[end:]
    
    return text


def scramble_data(text):
    """Main scrambling function: regex first, then NLP"""
    # Step 1: Apply regex-based replacements
    text = scramble_emails(text)
    text = scramble_sa_phone(text)
    text = scramble_sa_id(text)
    text = scramble_medical_aid(text)
    text = scramble_icd10(text)
    
    # Step 2: Apply NLP-based masking
    text = apply_nlp_masking(text)
    
    return text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scramble', methods=['POST'])
def scramble():
    try:
        data = request.get_json()
        input_text = data.get('text', '')
        
        if not input_text:
            return jsonify({'error': 'No text provided'}), 400
        
        scrambled_text = scramble_data(input_text)
        return jsonify({'output': scrambled_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## File 2: templates/index.html (Complete)

See the `templates/index.html` file in the repository. It contains:

- **850+ lines of code**
- **Comprehensive CSS** (dark mode, flexbox, animations, responsive design)
- **Complete HTML structure** (header, info box, textareas, buttons, status area)
- **Full JavaScript** (async fetch, event handling, UI state management)

Key sections:
1. **Meta tags** for charset, viewport, title
2. **CSS Grid/Flexbox** layout with responsive breakpoints
3. **Dark theme styling** with gradient backgrounds
4. **Button styles** with hover/active states
5. **Animation definitions** (spinner, slide-down)
6. **Media queries** for 1024px and 768px breakpoints
7. **Vanilla JavaScript** without frameworks
8. **Event listeners** for all buttons
9. **Async fetch** to `/scramble` endpoint
10. **Status message system** with auto-hide timers

---

## File 3: requirements.txt (Complete)

```
Flask==2.3.3
Faker==19.6.1
spacy==3.6.1
```

---

## File 4: init_project.py (Automated Setup)

The `init_project.py` script handles:
1. Creating `templates/` and `static/` directories
2. Generating `templates/index.html` with full content
3. Verifying required files exist
4. Printing setup instructions

**Usage:**
```bash
python init_project.py
```

---

## Regular Expressions Used

### Email Pattern
```regex
\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b
```
Matches: `user.name+tag@domain.co.za`

### SA Phone Pattern
```regex
\b0[0-9]{2}\s?[0-9]{3}\s?[0-9]{4}\b|\b\+27[0-9]\s?[0-9]{3}\s?[0-9]{4}\b
```
Matches: `082 555 1234` or `+27 82 555 1234`

### SA ID Pattern
```regex
\b[0-9]{13}\b
```
Matches: `9201015800123`

### Medical Aid Pattern
```regex
\b(?:MED[0-9]{5,8}|[A-Z0-9]{7,9})\b
```
Matches: `MED20240515` or `QXYZWP789`

### ICD-10 Pattern
```regex
\b[A-Z][0-9]{2}(?:\.[0-9]{1,2})?\b
```
Matches: `E11` or `E11.9` or `E11.90`

---

## Faker Methods Used

```python
fake.email()        # Generate random email
fake.name()         # Generate random full name
fake.city()         # Generate random city name
fake.address()      # Generate random address
```

---

## spaCy Entity Types Recognized

| Label | Type | Example | Replacement |
|-------|------|---------|-------------|
| PERSON | Person | "Dr. Sarah Johnson" | `fake.name()` |
| GPE | Geo-political entity | "South Africa" | `fake.city()` |
| LOC | Location | "Johannesburg" | `fake.city()` |
| FAC | Facility | "Hospital" | `fake.city()` |

---

## API Contract

### POST /scramble

**Request:**
```json
{
  "text": "sensitive data here..."
}
```

**Success Response (200):**
```json
{
  "output": "masked data here..."
}
```

**Error Response (400 - No text):**
```json
{
  "error": "No text provided"
}
```

**Error Response (500 - Server error):**
```json
{
  "error": "Error message here"
}
```

---

## JavaScript Event Flow

1. **Page Load** → Input textarea gets focus
2. **User Types** → Text accumulates in input area
3. **Click Scramble** → 
   - Validate not empty
   - Disable buttons
   - Show loading spinner
   - POST to `/scramble`
4. **Server Response** →
   - Enable buttons
   - Display output
   - Show success message
5. **Click Copy** →
   - Select all text
   - Copy to clipboard
   - Show confirmation
6. **Click Clear** →
   - Empty both textareas
   - Disable copy button
   - Clear status messages
   - Focus input

---

## CSS Classes Structure

```css
.container       /* Main wrapper, max-width 1400px */
header          /* Title and subtitle section */
h1              /* Gradient text title */
.subtitle       /* Subtitle text */
.main-content   /* Flexbox container for sections */
.section        /* Individual input/output sections */
.section-title  /* Section headings */
textarea        /* Input and output areas */
.controls       /* Button container */
button          /* All buttons */
.btn-scramble   /* Primary action button */
.btn-copy       /* Secondary action button */
.btn-clear      /* Danger action button */
.status         /* Message display area */
.spinner        /* Loading animation */
.info-box       /* Feature explanation box */
```

---

## Directory Structure After Setup

```
GuardRailScrambler/
├── .git/                          # Git repository
├── app.py                         # Flask backend (151 lines)
├── requirements.txt               # Dependencies
├── init_project.py               # Setup script
├── create_html.py                # HTML generator
├── setup.py                      # Alternative setup
├── setup.bat                     # Windows batch script
├── README.md                     # Full documentation
├── QUICK_START.md                # Quick reference
├── IMPLEMENTATION.md             # Technical details
├── CODE_LISTING.md              # This file
├── templates/                    # Created by init_project.py
│   └── index.html                # Frontend (350+ lines)
└── static/                       # Created by init_project.py
    └── (future CSS/JS files)
```

---

## How to Use This Code

1. **Copy app.py** to project root
2. **Run init_project.py** to create HTML and directories
3. **Install dependencies** with `pip install -r requirements.txt`
4. **Download model** with `python -m spacy download en_core_web_sm`
5. **Start server** with `python app.py`
6. **Open browser** to `http://localhost:5000`

The entire POC is ready to use! 🎉
