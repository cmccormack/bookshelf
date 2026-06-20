# Kobo eReader.conf

[View on MobileRead](https://wiki.mobileread.com/wiki/Kobo_eReader.conf)

> Note: The MobileRead wiki page for this topic was empty as of 2026-06-19. This document
> is compiled from calibre-web, CWA documentation, and community sources.

## File Location

```
<kobo-mount>/.kobo/Kobo/Kobo eReader.conf
```

Connect via USB; the file is in the hidden `.kobo/Kobo/` directory. Back it up before editing.

## Format

INI-style, section headers in `[brackets]`, key=value pairs.

## Key Sections

### [OneStoreServices]

Controls which sync server the device talks to. The critical field:

```ini
[OneStoreServices]
api_endpoint=https://storeapi.kobo.com
```

To redirect to a self-hosted CWA instance:

```ini
[OneStoreServices]
api_endpoint=https://<your-cwa-host>/kobo/<auth-token>
```

The auth token is generated in CWA under: User Profile → Kobo Sync → Create/View.
**Access CWA from a non-localhost address** when generating the token, or the resulting
URL will be unreachable from the device.

### [FeatureSettings]

```ini
[FeatureSettings]
ExcludeSyncFolders=\.(?!kobo|adobe).*?
```

Prevents the device from loading sideloaded files from non-Kobo directories as books.

## api_endpoint Field

- Default: `https://storeapi.kobo.com`
- Set to your CWA endpoint to redirect all library sync, book delivery, and metadata
  requests to your server.
- Format: `https://<host>/kobo/<token>` — token is unique per user account in CWA.
- If using a reverse proxy, ensure the endpoint uses `https://` and the proxy forwards
  `X-Scheme https` and `X-Forwarded-Proto`.
- Do not append a port number directly to a domain name (e.g., `domain.tld:8083`) — this
  causes the device to append the port to multiple other `[OneStoreServices]` entries and
  break them. Use an IP:port instead (`192.168.1.10:8083`) or a domain without a port via
  a reverse proxy.

## Firmware Overwrite Issue (Newer Devices)

On recent Kobo models including the **Libra Colour**, the device may restore the
`eReader.conf` file during sync, overwriting the custom `api_endpoint` back to
`https://storeapi.kobo.com`.

**Workaround options:**
1. Edit the file immediately before each sync session (impractical).
2. Use the alternative image server fields (limited — does not fully redirect sync):
   ```ini
   image_host=<server>
   image_url_quality_template=<template>
   image_url_template=<template>
   ```
3. Use a DNS-level intercept to redirect `storeapi.kobo.com` to your CWA host (advanced).
4. Check CWA issue trackers for firmware-specific patches — the CWA community actively
   works around this.

## Sync Limitations

- Only EPUB format syncs over the Kobo protocol. PDFs do not sync via this method.
- Device may display "Sync Failed" while still syncing book titles and firmware check —
  this is a known cosmetic issue with some CWA configurations.
- Signing into a Kobo account or factory resetting the device will overwrite `api_endpoint`
  back to the official store.

## Sources

- [Calibre-Web Kobo Integration wiki](https://github.com/janeczku/calibre-web/wiki/Kobo-Integration)
- [CWA Kobo Integration & Sync wiki](https://github.com/crocodilestick/Calibre-Web-Automated/wiki/Kobo-Integration-&-Sync)
- [CWA DeepWiki — Kobo Device Support](https://deepwiki.com/crocodilestick/Calibre-Web-Automated/5.2-kobo-device-support)
- [Kobo sync Nginx setup gist](https://gist.github.com/shadowandy/0112323b47d76ec77a58e769ac1efaf9)
- [Kobo sync setup walkthrough (Bubbu0129)](https://gist.github.com/Bubbu0129/92db9ad73ff32408cc41edaef1bbe130)
- [calibre-web issue #2690 — port appending bug](https://github.com/janeczku/calibre-web/issues/2690)
- [booklore issue #2083 — conf overwrite on sync](https://github.com/booklore-app/booklore/issues/2083)
