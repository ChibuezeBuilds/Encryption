# app.py
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import csv
import os
import random
import string
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets

app = Flask(__name__)
CORS(app)

# Generate a key from a password
def generate_key(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

# Encrypt data
def encrypt_data(data, password):
    salt = secrets.token_bytes(16)
    key, salt = generate_key(password, salt)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    return base64.urlsafe_b64encode(salt + encrypted).decode()

# Decrypt data
def decrypt_data(encrypted_data, password):
    decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
    salt = decoded_data[:16]
    encrypted = decoded_data[16:]
    key, _ = generate_key(password, salt)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted)
    return decrypted.decode()

# Generate a secure password
def generate_password(length=12, use_upper=True, use_digits=True, use_special=True):
    characters = string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    
    # Ensure at least one character from each selected set
    password = []
    if use_upper:
        password.append(random.choice(string.ascii_uppercase))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice(string.punctuation))
    
    # Fill the rest with random characters
    remaining_length = length - len(password)
    if remaining_length > 0:
        password.extend(random.choice(characters) for _ in range(remaining_length))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

# Save passwords to CSV
def save_to_csv(passwords, filename, encryption_password=None):
    fieldnames = ['website', 'username', 'password', 'notes']
    
    if encryption_password:
        # Encrypt each password entry
        encrypted_data = []
        for pwd in passwords:
            encrypted_pwd = {
                'website': encrypt_data(pwd.get('website', ''), encryption_password),
                'username': encrypt_data(pwd.get('username', ''), encryption_password),
                'password': encrypt_data(pwd.get('password', ''), encryption_password),
                'notes': encrypt_data(pwd.get('notes', ''), encryption_password)
            }
            encrypted_data.append(encrypted_pwd)
        passwords = encrypted_data
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(passwords)
    
    return filename

# Load passwords from CSV
def load_from_csv(filename, decryption_password=None):
    passwords = []
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if decryption_password:
                    # Decrypt each field
                    decrypted_row = {
                        'website': decrypt_data(row['website'], decryption_password),
                        'username': decrypt_data(row['username'], decryption_password),
                        'password': decrypt_data(row['password'], decryption_password),
                        'notes': decrypt_data(row['notes'], decryption_password)
                    }
                    passwords.append(decrypted_row)
                else:
                    passwords.append(row)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error loading CSV: {e}")
    return passwords

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_password', methods=['POST'])
def generate_password_route():
    data = request.json
    length = data.get('length', 12)
    use_upper = data.get('use_upper', True)
    use_digits = data.get('use_digits', True)
    use_special = data.get('use_special', True)
    
    password = generate_password(length, use_upper, use_digits, use_special)
    return jsonify({'password': password})

@app.route('/save_passwords', methods=['POST'])
def save_passwords():
    data = request.json
    passwords = data.get('passwords', [])
    filename = data.get('filename', 'passwords.csv')
    encryption_password = data.get('encryption_password')
    
    try:
        saved_filename = save_to_csv(passwords, filename, encryption_password)
        return jsonify({'success': True, 'filename': saved_filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/load_passwords', methods=['POST'])
def load_passwords():
    data = request.json
    filename = data.get('filename', 'passwords.csv')
    decryption_password = data.get('decryption_password')
    
    try:
        passwords = load_from_csv(filename, decryption_password)
        return jsonify({'success': True, 'passwords': passwords})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download_csv/<filename>')
def download_csv(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)