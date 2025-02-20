"""
Project: Password Generator
Author: Ryan Brinkman
Date: February 13, 2025

Description:
Generates secure passwords and evaluates password strength
based on length, complexity, and entropy.

GitHub Repository: https://github.com/RyanBrin/python/tree/main/vs-code/password-generator/
"""

import string, secrets, os, pathlib, hashlib
import math

def pick_choice():
    """Prompts the user to choose a password generation method."""
    print("Select an option:")
    print("1. Generate Password")
    print("2. Password Strength Checker")
    print("3. Quit")
    choice = input("Enter your choice: ").strip()
    return choice

def generate_password():
    """Generates a secure password and saves it to a file."""
    if not os.path.exists("generated-passwords"):
        os.mkdir("generated-passwords")

    length = int(input("Enter the desired password length: "))

    # Define character set based on strong password recommendations
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for _ in range(length))

    print(f"Generated Password: {password}")

    # Hash filename to prevent revealing passwords
    extension_hash = hashlib.md5(password.encode()).hexdigest()
    file_path = pathlib.Path("password-generator", "generated-passwords", f"password_{extension_hash}.txt")

    print(f"Password saved to: {file_path}")

    with open(file_path, "w") as file:
        file.write("Generated Password:\n")
        file.write(password)

def check_password_strength():
    """Evaluates the strength of a given password based on realistic criteria."""
    password = input("Enter the password to check: ").strip()

    length = len(password)
    score = 0

    # Length-based scoring
    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    # Complexity-based scoring
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)

    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1

    # Additional Checks
    common_passwords = ["password", "123456", "qwerty", "admin", "letmein"]
    if password.lower() in common_passwords:
        print("⚠️ This password is commonly used and very weak!")
        score = 0

    if password.isalpha() or password.isdigit():
        print("⚠️ Avoid using only letters or only numbers!")
        score -= 1

    if len(set(password)) < len(password) / 2:  # Checks for repeated characters
        print("⚠️ Your password contains too many repeated characters!")
        score -= 1

    # Entropy Calculation (Measures randomness)
    entropy = length * math.log2(len(set(password)))

    print("\n🔹 Password Strength Analysis 🔹")
    print(f"🔢 Length: {length} characters")
    print(f"🔑 Complexity: {'Uppercase' if has_upper else ''} {'Lowercase' if has_lower else ''} {'Digits' if has_digit else ''} {'Special Characters' if has_special else ''}")
    print(f"📊 Estimated Entropy: {entropy:.2f} bits")

    # Final Rating
    if score <= 2:
        print("❌ Very Weak Password! Change immediately.")
    elif score == 3 or entropy < 40:
        print("⚠️ Weak Password! Consider making it longer and more complex.")
    elif score == 4 or entropy < 60:
        print("✅ Moderate Password. Could be stronger.")
    elif score == 5 or entropy >= 70:
        print("💪 Strong Password! Good job.")
    else:
        print("🔥 Extremely Secure Password! Well done.")

while True:
    choice = pick_choice()

    if choice == "1":
        generate_password()
    elif choice == "2":
        check_password_strength()
    elif choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")