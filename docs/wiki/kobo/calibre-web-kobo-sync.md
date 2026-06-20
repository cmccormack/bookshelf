# Calibre-Web Kobo Sync (upstream)
[View on GitHub](https://github.com/janeczku/calibre-web)

CWA is built on calibre-web, so these upstream instructions apply. CWA-specific differences are noted.

## Enable in Admin

1. Admin → Edit Basic Configuration → Feature Configuration
2. Check **Enable Kobo sync**
3. Check **Proxy unknown requests to Kobo Store**
4. Confirm **Server External Port** = 8083 (or your actual port)

## Generate Sync Token

User settings → **Kobo Sync Token** → Create/View

In CWA the path is: Admin → Edit Users → [user] → OAuth & API Integrations → Kobo Sync Token

The generated `api_endpoint` URL format:
```
http://<server-ip>:<port>/kobo/<sync-token>
```

Access calibre-web from the network IP (not localhost) before generating, so the URL is device-reachable.

## Configure Kobo Device

Connect Kobo via USB. Edit `.kobo/Kobo/Kobo eReader.conf`:

```ini
[OneStoreServices]
api_endpoint=http://<server-ip>:8083/kobo/<sync-token>
```

The default line is `api_endpoint=https://storeapi.kobo.com` — replace it entirely.

## Shelves / Collections

- By default the full library syncs
- Enable "Sync only books in selected shelves with Kobo" in user settings for selective sync
- Create/edit a shelf → check "Sync this shelf with Kobo device"
- Shelf name appears as a collection on the Kobo

## Format Support

Only EPUB and KEPUB sync to Kobo. Install kepubify for automatic EPUB→KEPUB conversion (better native Kobo experience). PDF and other formats do not sync.

## Reading Progress

Calibre-web tracks reading position, bookmarks, and last-read page. Progress syncs when the Kobo connects to WiFi or on manual sync (Settings → Sync and Share → Sync Now).

## Reverse Proxy Notes

- HTTPS with a reverse proxy can cause issues; local IP + HTTP is more reliable for initial setup
- If using a reverse proxy, set the external URL correctly in Basic Configuration
- Ports 80/443 may work better than 8083 through a proxy for cover images
