# Password Manager with Encryption

A secure password manager with encryption, password generation, and CSV export functionality. Built with a Python Flask backend and a web-based frontend using Tailwind CSS.

## Project Structure

```
password-manager/
├── app.py                 # Flask backend
├── templates/
│   └── index.html        # Frontend interface
├── static/
│   └── style.css         # Tailwind CSS
└── requirements.txt      # Python dependencies
```

## Features

- **Password Generator**: Generate secure passwords with customizable options (length, uppercase, digits, special characters).
- **Password Manager**: Store and manage multiple password entries with fields for website, username, password, and notes.
- **CSV Export/Import**: Save passwords to and load from CSV files for backup.
- **Encryption**: Optional encryption of password data using a master password with PBKDF2 key derivation.
- **User-Friendly Interface**: Responsive and clean design powered by Tailwind CSS.

## Installation

1. Clone the repository or download the project files.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`.

## Usage

1. **Generate Passwords**:
   - Configure password length and character types (uppercase, digits, special characters).
   - Click "Generate Password" to create a secure password.
   - Copy the generated password to the clipboard or use it in a password entry.

2. **Manage Passwords**:
   - Add new password entries with details for website, username, password, and notes.
   - Toggle password visibility or use a generated password for an entry.
   - Remove entries as needed (minimum one entry required).

3. **Save/Load Passwords**:
   - Save passwords to a CSV file, optionally encrypting them with a master password.
   - Load passwords from a CSV file, providing the decryption password if encrypted.
   - Download the saved CSV file for backup.

## Security Notes

- **Encryption**: Uses PBKDF2 with 100,000 iterations for key derivation and Fernet for symmetric encryption. Each encrypted file includes a unique salt.
- **Data Security**: Without the correct encryption password, encrypted data cannot be recovered.
- **Best Practices**: Keep your encryption password secure and never share it. Always back up your CSV files in a safe location.

## Requirements

The following dependencies are listed in `requirements.txt`:

```
Flask==2.3.3
Flask-CORS==4.0.0
cryptography==41.0.3
```

## Running the Application

1. Ensure Python 3.8+ is installed.
2. Install dependencies using `pip install -r requirements.txt`.
3. Start the Flask server with `python app.py`.
4. Access the application at `http://localhost:5000`.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for bug reports or feature requests.

## License

This project is licensed under the MIT License.