# Kobo Setup

Connect your Kobo to Calibre-Web Automated for wireless book sync.

## Prerequisites
- CWA running and accessible on your network
- Kobo sync enabled in CWA admin (Admin → Basic Configuration → "Enable Kobo sync")

## Step 1: Get your Kobo sync token

1. Log into CWA as the user whose Kobo you're setting up
2. Go to **User Profile → Kobo Sync → Create/View token**
3. Copy the token

## Step 2: Patch the Kobo config via USB

The Beta Features menu on firmware 4.39+ no longer includes a sync server option.
Edit the config file directly instead.

Connect the Kobo via USB, then run:

```bash
uv run python kobo_set_server.py /Volumes/KOBOeReader <host-ip> 8083 <token>
```

**Important:** use an IP address, not a hostname with port (e.g. `192.168.1.100`, not `mynas.local:8083`).
Using `hostname:port` causes the Kobo to append the port number to unrelated URLs.

This writes a backup (`.conf.bak`) before modifying. Safe to re-run when the IP changes (e.g. NAS deploy).

## Step 3: Eject and sync

Eject the Kobo from Finder, then on the device: **Home → Sync**.

Books from your CWA library will appear after the first sync.

## Sync URL format

```
http://<host-ip>:8083/kobo/<token>
```

- Local test: `http://<local-ip>:8083/kobo/<token>`
- NAS deploy: `http://<nas-ip>:8083/kobo/<token>` (re-run script with new IP after NAS deploy)

## Why does CWA convert books during sync?

CWA automatically converts EPUB → KEPUB on-the-fly when syncing to a Kobo. KEPUB is Kobo's
enhanced format with better typography and reading stats. Conversion happens in a temp
directory — the library files stay as EPUB. This is expected, normal behavior.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| "Retry sync" / sync fails | Enable Kobo proxy — see below |
| Kobo can't reach server | Use LAN IP not hostname; confirm port 8083 is not firewalled |
| Books don't appear after sync | Check CWA logs: `docker logs cwa-library -f` |
| Sync works at home, not on travel router | Ensure Kobo and server are on the same VLAN/subnet |
| Need to update server IP | Re-run `kobo_set_server.py` with new IP, re-sync |

### Kobo proxy

If sync fails with a generic error, enable the Kobo proxy in CWA. This allows the Kobo to
fetch resource definitions and firmware info from Kobo's servers, while CWA handles library sync:

```bash
sqlite3 /volume1/docker/cwa-library/config/app.db 'UPDATE settings SET config_kobo_proxy=1;'
/usr/local/bin/docker restart cwa-library
```

Or enable via CWA web UI: **Admin → Basic Configuration → "Proxy unknown requests to Kobo Store"**.

## Verified on

- Kobo Libra Colour, firmware 4.45.23697
- CWA v2.2.1, Calibre 9.1
