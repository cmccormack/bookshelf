# CWA Kobo Sync Setup
[View on GitHub](https://github.com/crocodilestick/Calibre-Web-Automated)

## Prerequisites

- Kobo e-reader (Clara HD, Libra 2, Libra Colour, Sage, etc.)
- CWA accessible on your network (not via localhost)
- Books in EPUB or KEPUB format — only these sync to Kobo
- Admin access to CWA

## Step 1: Enable Kobo Sync in CWA Admin

1. Admin → Basic Configuration → Feature Configuration
2. Check **Enable Kobo sync**
3. Check **Proxy unknown requests to Kobo Store** (recommended — allows store browsing)
4. Verify **Server External Port** matches CWA's port (default: 8083)
5. Ensure users have **Download** permission

## Step 2: Generate Kobo Auth Token (per user)

Admin → Edit Users → [user] → OAuth & API Integrations → **Kobo Sync Token** → Create/View

Or via user's own settings page: look for "Generate Kobo Auth URL".

**Important:** Access CWA from its network IP (not `localhost`) before generating the token, so the generated URL contains the correct reachable address.

The generated URL looks like:
```
http://192.168.1.x:8083/kobo/<your-auth-token>
```

This full URL is the `api_endpoint` value you'll paste into the Kobo config file.

## Step 3: Configure the Kobo Device

Connect the Kobo via USB. On the device prompt, choose to connect as storage.

Navigate to the hidden `.kobo/Kobo/` folder and open `Kobo eReader.conf` in a text editor. Backup this file first.

Find the `[OneStoreServices]` section and replace the `api_endpoint` line:

```ini
[OneStoreServices]
api_endpoint=http://192.168.1.x:8083/kobo/<your-auth-token>
```

### Libra Colour / newer devices — cover image URLs

Newer devices (including Libra Colour) also need image host entries for cover art. Add to the same section:

```ini
image_host=http://192.168.1.x:8083
image_url_quality_template=http://192.168.1.x:8083/kobo/<token>/{ImageId}/{width}/{height}/{Quality}/isGreyscale/image.jpg
image_url_template=http://192.168.1.x:8083/kobo/<token>/{ImageId}/{width}/{height}/false/image.jpg
```

## Step 4: Initial Sync

Safely eject the Kobo. On the home screen, tap the sync icon (top toolbar) or let it auto-sync on WiFi. The first sync builds the database and may take a minute.

## Sync Modes

**Full library sync (default):** every EPUB/KEPUB in CWA syncs to the device.

**Shelf-only sync (recommended for large libraries):**
1. Enable "Sync only books in selected shelves" in User Settings
2. Create a shelf → check "Sync this shelf with Kobo device"
3. Add books to that shelf

## KEPUB Conversion

CWA auto-converts EPUB → KEPUB when `kepubify` is configured. KEPUB integrates better with Kobo (chapter progress, font controls, etc.).

## Reading Progress Sync

Position, bookmarks, and statistics sync automatically on page turns, book close, and WiFi connection. Manual sync: Settings → Sync and Share → Sync Now.

## Key API Endpoints (for diagnostics)

```
/kobo/<token>/v1/library/sync          — main sync
/kobo/<token>/v1/initialization        — test reachability
/kobo/<token>/v1/library/<uuid>/state  — reading state
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| Books not appearing | Verify Download permission; confirm EPUB/KEPUB format |
| Auth errors | Regenerate token; access CWA from network IP not localhost |
| Cover images broken | Add `image_host` / `image_url_template` entries; try Force Full Sync |
| Sync timeouts | Test Kobo browser can reach `/v1/initialization`; check firewall |
| Local-only sync | For remote access, expose CWA via reverse proxy + HTTPS; use port 80/443 |

## Docker / Network Notes

- On NAS with NFS/SMB: set `NETWORK_SHARE_MODE=true` (disables SQLite WAL, enables polling)
- CWA v3.0.0+ does not support NFS-mounted library paths officially
- PUID/PGID in the container must match host folder ownership
