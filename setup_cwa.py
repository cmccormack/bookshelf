import argparse
import os
import secrets
import string
import sys
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


def generate_password(length=32):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    required = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()-_=+"),
    ]
    rest = [secrets.choice(alphabet) for _ in range(length - len(required))]
    pool = required + rest
    secrets.SystemRandom().shuffle(pool)
    return "".join(pool)


parser = argparse.ArgumentParser(description="CWA admin hardening and password management.")
parser.add_argument("--host", default="localhost", help="CWA host (default: localhost)")
parser.add_argument("--port", default="8083", help="CWA port (default: 8083)")
parser.add_argument("--env-file", default=".env", help="Path to .env file (default: .env)")
parser.add_argument(
    "--password", metavar="PASSWORD",
    help="Current admin password — overrides ADMIN_PASSWORD env var (default: admin123)",
)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--update-password", metavar="PASSWORD",
    help="Set admin password to this value",
)
group.add_argument(
    "--rotate-password", action="store_true",
    help="Generate a new strong random password, print it, then set it",
)
args = parser.parse_args()

load_dotenv(args.env_file)

# Current password: --password > ADMIN_PASSWORD env var > CWA factory default
OLD_PASS = args.password or os.environ.get("ADMIN_PASSWORD") or "admin123"

if args.rotate_password:
    NEW_PASS = generate_password()
    print(f"\nGenerated password: {NEW_PASS}")
    print("Save this in your password manager before continuing.")
    input("\nPress Enter to proceed...")
else:
    NEW_PASS = args.update_password

BASE = f"http://{args.host}:{args.port}"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    print(f"Logging in to {BASE}...")
    page.goto(f"{BASE}/login")
    page.fill("#username", "admin")
    page.fill("#password", OLD_PASS)
    page.click("[type=submit]")
    page.wait_for_url(f"{BASE}/")
    print("Logged in.")

    print("Changing password...")
    page.goto(f"{BASE}/admin/user/1")
    page.wait_for_load_state("networkidle")
    # Dismiss any active notification modal before interacting with the form
    modal = page.locator("#duplicate-notification-modal.active")
    if modal.is_visible():
        modal.locator("button").first.click()
        page.wait_for_load_state("networkidle")
    page.fill("#password", NEW_PASS)
    page.locator("#user_submit").click()
    page.wait_for_load_state("networkidle")
    print("Password changed.")

    print("Enabling Kobo sync...")
    page.goto(f"{BASE}/admin/config")
    page.wait_for_load_state("networkidle")
    cb = page.locator("#config_kobo_sync")
    if not cb.is_checked():
        cb.check()
    page.locator("#config_submit").click()
    page.wait_for_load_state("networkidle")
    print("Kobo sync enabled.")

    print("Verifying Kobo sync is on...")
    page.goto(f"{BASE}/admin/config")
    page.wait_for_load_state("networkidle")
    print(f"  config_kobo_sync checked: {page.locator('#config_kobo_sync').is_checked()}")

    print(f"\nKobo sync URL format: {BASE}/kobo/<user-token>")
    print("  (token visible per-user under Account Settings after login)")

    browser.close()
    print("\nSetup complete.")
