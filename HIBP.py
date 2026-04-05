# -*- coding: utf-8 -*-
import requests
import time

# Your Have I Been Pwned API key
API_KEY = "Your API Key"

# HIBP API endpoint
BASE_URL = "https://haveibeenpwned.com/api/v3/breachedaccount/"

# List to store emails that were found in breaches
pwned_list = []

# Read emails from file
try:
    with open("emails.txt", "r") as file:
        emails = file.readlines()
except FileNotFoundError:
    print("[ERROR] emails.txt not found.")
    emails = []

for email in emails:
    email = email.strip()
    if not email:
        continue

    print(f"\nChecking: {email}")

    headers = {
        "hibp-api-key": API_KEY,
        "User-Agent": "Project"
    }

    url = BASE_URL + email
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        breaches = response.json()
        print(f"[BREACHED] {email} found in {len(breaches)} breach(es):")
        # Add to our list for the final report
        pwned_list.append(email)
        for breach in breaches:
            print(" -", breach["Name"])

    elif response.status_code == 404:
        print(f"[CLEAN] {email} not found in any breaches.")

    elif response.status_code == 401:
        print("[ERROR] Unauthorized. Check your API key.")
        break

    elif response.status_code == 429:
        print("[WARNING] Rate limit exceeded. Slowing down...")
        time.sleep(10)
    else:
        print(f"[ERROR] HTTP {response.status_code} for {email}")

    # Rate limiting
    time.sleep(6.2)

# --- NEW FUNCTIONALITY: Write results to file ---
if pwned_list:
    print(f"\n[INFO] Writing {len(pwned_list)} compromised emails to pwned_emails.txt...")
    with open("pwned_emails.txt", "w") as output_file:
        for pwned_email in pwned_list:
            output_file.write(pwned_email + "\n")
    print("[SUCCESS] Report generated.")
else:
    print("\n[INFO] No breached emails found. No file generated.")
