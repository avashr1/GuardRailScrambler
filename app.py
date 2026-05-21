import re
import string
import random
from flask import Flask, render_template, request, jsonify
from faker import Faker
import spacy

app = Flask(__name__)
fake = Faker('en_US')

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
    # Only match explicit MED + digits format, not random uppercase sequences
    med_aid_pattern = r'\bMED[0-9]{6,10}\b'
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
