# Custom Sync Server Configuration (no Beta Features menu)

[View on GitHub](https://github.com/cmccormack/bookshelf/blob/main/docs/wiki/kobo/custom-sync-server.md)

Kobo devices on firmware 4.39+ (including the Libra Colour on 4.45) may not show a
Beta Features menu in Settings — it can be hidden by parental mode or absent on some
models. The direct USB config file edit works on all firmware versions and is the
primary recommended method.

---

## Method 1: Direct config file edit via USB (recommended)

Works on all Kobo firmware versions. Survives reboots. May revert after a firmware update
(see Gotchas).

### Prerequisites

- USB cable (data-capable, not charge-only)
- A text editor
- Calibre-Web running and Kobo sync enabled (Admin > Configuration > Feature Configuration)
- Your Kobo sync token URL from Calibre-Web (username > "Create/View Kobo Sync Token")

The token URL looks like: `https://yourserver/kobo/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Steps

1. Connect the Kobo to your computer via USB. It mounts as a USB drive.
2. Enable hidden file/folder display on your OS if needed (the `.kobo` directory is hidden).
3. Open the file:
   ```
   .kobo/Kobo/Kobo eReader.conf
   ```
   On Windows the path separator is `\`. The file may also appear as `Kobo.eReader.conf`
   depending on your OS's hidden-extension settings — it is the same file.
4. Make a backup copy before editing:
   ```
   .kobo/Kobo/Kobo eReader.conf.backup
   ```
5. Find the `[OneStoreServices]` section. Locate this line:
   ```
   api_endpoint=https://storeapi.kobo.com
   ```
6. Replace it with your Calibre-Web (or Komga/CWA) endpoint:
   ```
   api_endpoint=https://yourserver/kobo/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   For local network use, an IP address works:
   ```
   api_endpoint=http://192.168.1.100:8083/kobo/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
7. Save the file and safely eject the Kobo.
8. On the Kobo home screen tap the sync icon (circular arrow, top right) to sync.

### Firmware version compatibility

Confirmed working on firmware 4.25 through 4.45 by community reports. The file format
has not changed across these versions. No firmware version requires a different key name
or section.

### Gotchas

- **Setting may revert after a firmware update.** After every OTA update, re-check the
  `api_endpoint` line and re-apply if needed. Keep the `.backup` file around for reference
  on the original value.
- **Rare reversion bug (Clara 2E):** At least one user on firmware ~4.37 found the setting
  reverting after each sync. A full hardware reset (hold power while plugged in until device
  resets fully — not a software factory reset) resolved it. Cause unknown, appears to be a
  device-specific bug. [Source](https://www.mobileread.com/forums/showthread.php?t=357598)
- **Only EPUB is synced** by Calibre-Web's Kobo sync. PDFs and other formats are not.
- **Shelves required:** Books do not sync automatically. In Calibre-Web, create a shelf and
  enable "Sync this shelf with Kobo device". Enable "Sync only books in selected shelves
  with Kobo" in user settings.
- **Port in Calibre-Web admin must match.** The "Server External Port" setting in Calibre-Web
  Admin > Configuration must match the port your Kobo connects on. Default is 8083; if
  behind a reverse proxy on port 80/443, update this field accordingly.
- **Nginx Proxy Manager users** need extra buffer settings:
  ```nginx
  proxy_buffer_size 128k;
  proxy_buffers 4 256k;
  proxy_busy_buffers_size 256k;
  ```
- Local IP is more reliable than external URLs when behind Cloudflare tunnels or complex
  reverse proxies.

### Restoring original Kobo store

Rename `.backup` back to `Kobo eReader.conf`, or manually set:
```
api_endpoint=https://storeapi.kobo.com
```

---

## Method 2: Restore Beta Features menu access

The Beta Features menu (Settings > Beta Features) is the GUI path to set a custom sync
server on some Kobo devices. If it is missing, check these causes before assuming it's
been removed:

### Cause 1: Parental mode is enabled

Enabling parental controls hides the Beta Features submenu entirely. Go to Settings >
Parental Controls and disable it. The Beta Features entry should reappear.
[Source](https://www.mobileread.com/forums/showthread.php?t=354808)

### Cause 2: Developer mode is not enabled

On some models and firmware versions, Beta Features only appears after enabling developer
mode:

1. On the Kobo home screen, tap the magnifying glass (search icon, top right).
2. Type `devmodeon` — no confirmation message appears, but the mode activates.
3. Check Settings again; the Beta Features entry should now be visible.

[Source](https://goodereader.com/blog/electronic-readers/how-to-access-the-secret-kobo-developer-options)

### Note on firmware 4.45 (Libra Colour)

No confirmed reports of Beta Features being fully removed in 4.45. The absence is most
likely due to parental mode or developer mode not being active. If Method 2 fails, use
Method 1 (USB config edit) instead — it is more reliable and firmware-independent.

---

## Sources

- [My Kobo Customizations — Mendhak](https://code.mendhak.com/kobo-customizations/)
- [Setting up Kobo sync with Calibre Web — Jordan Palmer](https://jccpalmer.com/posts/setting-up-kobo-sync-with-calibre-web/)
- [Syncing Kobo and Calibre Web — yvn.no](https://devblog.yvn.no/posts/syncing-kobo-and-calibre-web/)
- [Synchronize Kobo eReader with Calibre-Web — Symalon](https://symalon.com/en/synchronize-kobo-ereader-with-calibre-web/)
- [Setting up Kobo synchronisation with Calibre-Web and Nginx — shadowandy (GitHub Gist)](https://gist.github.com/shadowandy/0112323b47d76ec77a58e769ac1efaf9)
- [Read with Kobo — Komga documentation](https://komga.org/docs/guides/kobo/)
- [Clara 2E api_endpoint keeps reverting — MobileRead](https://www.mobileread.com/forums/showthread.php?t=357598)
- [Kobo Clara HD missing beta features — MobileRead](https://www.mobileread.com/forums/showthread.php?t=354808)
- [How to access the secret Kobo developer options — Good e-Reader](https://goodereader.com/blog/electronic-readers/how-to-access-the-secret-kobo-developer-options)
- [About Beta Features — Rakuten Kobo help](https://help.kobo.com/hc/en-us/articles/360017763733-About-Beta-Features)
- [Calibre-Web & Kobo Sync Tutorial — MobileRead (Feb 2026)](https://www.mobileread.com/forums/showthread.php?t=372086)
