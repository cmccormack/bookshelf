import argparse
import os
import sys
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

OLD_PASS = "admin123"

parser = argparse.ArgumentParser(description="First-run CWA hardening via Playwright.")
parser.add_argument("--host", default="localhost", help="CWA host (default: localhost)")
parser.add_argument("--port", default="8083", help="CWA port (default: 8083)")
parser.add_argument("--password", help="New admin password (overrides ADMIN_PASSWORD in .env)")
parser.add_argument("--env-file", default=".env", help="Path to .env file (default: .env)")
args = parser.parse_args()

load_dotenv(args.env_file)
NEW_PASS = args.password or os.environ.get("ADMIN_PASSWORD")

if not NEW_PASS:
    sys.exit("Error: provide --password, set ADMIN_PASSWORD env var, or add ADMIN_PASSWORD to .env")

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
