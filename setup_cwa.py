import argparse
import os
import re
import secrets
import string
import sys
from pathlib import Path
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


def update_env_file(env_file: str, new_password: str) -> None:
    path = Path(env_file)
    if not path.exists():
        return
    text = path.read_text()
    text = re.sub(r"^ADMIN_PASSWORD=.*$", f"ADMIN_PASSWORD='{new_password}'", text, flags=re.MULTILINE)
    text = re.sub(r"^ADMIN_REFRESH_PASSWORD=.*$", "ADMIN_REFRESH_PASSWORD=", text, flags=re.MULTILINE)
    path.write_text(text)


def confirm(prompt: str, auto_yes: bool) -> bool:
    if auto_yes:
        print(f"{prompt} [auto-yes]")
        return True
    return input(f"{prompt} [y/N] ").strip().lower() == "y"


parser = argparse.ArgumentParser(description="CWA admin hardening and password management.")
parser.add_argument("--host", default="localhost", help="CWA host (default: localhost)")
parser.add_argument("--port", default="8083", help="CWA port (default: 8083)")
parser.add_argument("--env-file", default=".env", help="Path to .env file (default: .env)")
parser.add_argument(
    "--password", metavar="PASSWORD", default="admin123",
    help="Current admin password (default: admin123)",
)
parser.add_argument(
    "--yes", "-y", action="store_true",
    help="Skip all confirmation prompts and proceed automatically",
)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--update-password", nargs="?", const=None, metavar="PASSWORD",
    help="Set admin password to PASSWORD, or to ADMIN_PASSWORD from .env if no value given",
)
group.add_argument(
    "--rotate-password", action="store_true",
    help=(
        "Rotate admin password: reads current from ADMIN_PASSWORD, "
        "new from ADMIN_REFRESH_PASSWORD (or generates one), then optionally updates .env"
    ),
)
args = parser.parse_args()

load_dotenv(args.env_file)

OLD_PASS = args.password

if args.rotate_password:
    if OLD_PASS == "admin123":
        OLD_PASS = os.environ.get("ADMIN_PASSWORD") or "admin123"
    NEW_PASS = os.environ.get("ADMIN_REFRESH_PASSWORD") or generate_password()
    print(f"\nNew password: {NEW_PASS}")
    if not os.environ.get("ADMIN_REFRESH_PASSWORD"):
        print("Save this in your password manager.")
    if not args.yes:
        input("\nPress Enter to proceed...")
else:
    NEW_PASS = args.update_password or os.environ.get("ADMIN_PASSWORD")
    if not NEW_PASS:
        sys.exit("Error: --update-password requires a value or ADMIN_PASSWORD set in .env")

BASE = f"http://{args.host}:{args.port}"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    print(f"\nLogging in to {BASE}...")
    page.goto(f"{BASE}/login")
    page.fill("#username", "admin")
    page.fill("#password", OLD_PASS)
    page.click("[type=submit]")
    page.wait_for_url(f"{BASE}/")
    print("Logged in.")

    print("Changing password...")
    page.goto(f"{BASE}/admin/user/1")
    page.wait_for_load_state("networkidle")
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

if args.rotate_password:
    if confirm(f"\nUpdate {args.env_file} with new password?", args.yes):
        update_env_file(args.env_file, NEW_PASS)
        print(f"Updated: ADMIN_PASSWORD set to new value, ADMIN_REFRESH_PASSWORD cleared.")

print("\nSetup complete.")
