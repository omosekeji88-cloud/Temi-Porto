# Password Breach Checker

A Python command-line tool that checks whether a password appears in known data breaches using the Have I Been Pwned Pwned Passwords API.

## Key skills

- Python scripting
- API requests
- SHA-1 hashing
- Privacy-aware k-anonymity lookup
- Command-line arguments

## How it works

The password is converted to a SHA-1 hash locally. Only the first five hash characters are sent to the API, and the returned hash suffixes are checked locally. This avoids sending the original password or full hash.

## Run

```bash
python password_checker.py password123 anotherPassword
```
