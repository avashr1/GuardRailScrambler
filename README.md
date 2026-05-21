# GuardRail PII Scrambler - Medical Data Masking Tool

A lightweight, offline-first POC for anonymizing sensitive medical data using regex patterns and NLP.

## Features

✅ **100% Offline** - No external APIs or cloud dependencies  
✅ **Regex + NLP** - Pattern matching + spaCy entity recognition  
✅ **Multiple Data Types** - SA IDs, phone numbers, emails, medical aid numbers, ICD-10 codes, names, locations  
✅ **Structure Preserved** - JSON, SQL, and text formatting intact  
✅ **Clean UI** - Dark mode, responsive design, copy-to-clipboard  

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Setup

1. **Create templates directory:**
   ```bash
   mkdir templates
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy NLP model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Run the Flask server:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   - Navigate to `http://localhost:5000`

## Masked Data Types

### Regex Patterns
- **Emails** → Random valid email
- **SA Phone Numbers** (082 XXX XXXX, +27X XXX XXXX) → Random SA number
- **13-digit SA IDs** → Random 13-digit string
- **Medical Aid Numbers** (MED + digits or 7-9 alphanumeric) → Random similar format
- **ICD-10 Codes** (A99, B99.99, etc.) → Random valid format

### NLP Entity Recognition (spaCy)
- **PERSON** → Random name
- **GPE, LOC, FAC** (locations/organizations) → Random city/address

## Example

**Input:**
```
Patient: John Smith, ID: 9201015800123
Email: john.smith@example.com
Phone: 082 555 1234
Medical Aid: MED12345678
Diagnosis: Type 2 Diabetes (E11.9)
Location: Johannesburg Hospital
```

**Output:**
```
Patient: Maria Garcia, ID: 4758921463027
Email: robert.brown@yahoo.com
Phone: 083 421 8765
Medical Aid: QWERTY789
Diagnosis: Type 2 Diabetes (M23.45)
Location: Cape Town
```

## Architecture

```
GuardRailScrambler/
├── app.py                 # Flask backend with scrambling logic
├── templates/
│   └── index.html         # Frontend UI (dark mode, responsive)
├── requirements.txt       # Python dependencies
└── setup.bat             # Windows setup helper
```

### Processing Pipeline

1. **Regex Pass** - Replaces patterns in order:
   - Emails, SA phones, SA IDs, medical aid numbers, ICD-10 codes

2. **NLP Pass** - Entity recognition and replacement:
   - PERSON → fake.name()
   - GPE/LOC/FAC → fake.city()

## API

**POST /scramble**
- Request: `{ "text": "sensitive data here" }`
- Response: `{ "output": "masked data here" }`

## Security Notes

- **No data persistence** - Input/output exists only in browser memory
- **No external calls** - All processing is local
- **No logs** - (Default Flask development mode; disable in production)

## Development

To modify masking rules, edit the corresponding functions in `app.py`:
- `scramble_emails()` - Email patterns
- `scramble_sa_phone()` - Phone number patterns
- `scramble_sa_id()` - ID patterns
- `scramble_medical_aid()` - Medical aid patterns
- `scramble_icd10()` - ICD-10 code patterns
- `apply_nlp_masking()` - NLP entity recognition

## Limitations

- spaCy model accuracy depends on text quality
- Regex patterns are SA-specific (phone, ID formats)
- Performance depends on text length (NLP processing slower on large texts)
- ICD-10 code generation is format-only (not clinically validated)

## License

This is a proof-of-concept tool. Use responsibly and test thoroughly before production use.

## Disclaimer

This tool is provided as-is for educational and development purposes. Always validate masked data compliance with your organization's privacy policies before using in production.