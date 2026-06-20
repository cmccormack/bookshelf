#!/usr/bin/env python3
"""
Set api_endpoint in Kobo eReader.conf to point at a CWA server.

Usage:
    uv run python kobo_set_server.py <mount> <host> <port> <token>

    mount  — Kobo USB mount point, e.g. /Volumes/KOBOeReader
    host   — CWA server IP (use IP, not hostname+port — Kobo appends port to
              other URLs if a domain:port combo is used)
    port   — CWA port, typically 8083
    token  — Kobo sync token from CWA: User Profile → Kobo Sync → Create/View token

Example (local test):
    uv run python kobo_set_server.py /Volumes/KOBOeReader <local-ip> 8083 <token>

Example (NAS):
    uv run python kobo_set_server.py /Volumes/KOBOeReader <nas-ip> 8083 <token>

Writes a .conf.bak backup before modifying. Safe to re-run.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

CONF_RELATIVE = Path(".kobo/Kobo/Kobo eReader.conf")
SECTION = "[OneStoreServices]"
KEY = "api_endpoint"


def find_conf(mount: Path) -> Path:
    conf = mount / CONF_RELATIVE
    if not conf.exists():
        sys.exit(f"Config not found: {conf}\nIs the Kobo mounted at {mount}?")
    return conf


def update_conf(conf: Path, endpoint: str) -> None:
    text = conf.read_text(encoding="utf-8")

    # Replace existing key under [OneStoreServices]
    pattern = re.compile(
        r"(\[OneStoreServices\][^\[]*?)"   # capture section header + body
        r"(api_endpoint\s*=\s*[^\n]*)",    # capture existing key=value
        re.DOTALL,
    )
    if pattern.search(text):
        new_text = pattern.sub(
            lambda m: m.group(1) + f"{KEY}={endpoint}",
            text,
        )
    else:
        # Key absent — append it under the section header
        new_text = text.replace(
            SECTION,
            f"{SECTION}\n{KEY}={endpoint}",
        )
        if new_text == text:
            # Section itself is absent — append both
            new_text = text.rstrip() + f"\n\n{SECTION}\n{KEY}={endpoint}\n"

    shutil.copy2(conf, conf.with_suffix(".conf.bak"))
    conf.write_text(new_text, encoding="utf-8")
    print(f"Updated: {conf}")
    print(f"   {KEY}={endpoint}")
    print(f"Backup:  {conf.with_suffix('.conf.bak')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Point Kobo at a CWA sync server.")
    parser.add_argument("mount", help="Kobo mount point (e.g. /Volumes/KOBOeReader)")
    parser.add_argument("host", help="CWA host IP or hostname (e.g. 192.168.1.100)")
    parser.add_argument("port", help="CWA port (e.g. 8083)")
    parser.add_argument("token", help="Kobo sync token from CWA user profile")
    args = parser.parse_args()

    endpoint = f"http://{args.host}:{args.port}/kobo/{args.token}"
    conf = find_conf(Path(args.mount))
    update_conf(conf, endpoint)


if __name__ == "__main__":
    main()
