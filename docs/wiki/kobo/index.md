# Kobo Sync Reference Index

| File | Topic | Summary |
|------|-------|---------|
| [kobo-ereader-conf.md](kobo-ereader-conf.md) | Device config file | `.kobo/Kobo/Kobo eReader.conf` format, `[OneStoreServices]` / `api_endpoint` field, port-appending bug, config-overwrite gotcha |
| [firmware-changelog.md](firmware-changelog.md) | Firmware 4.39–4.45 changelog | Key changes per version; no sync-breaking changes found; 4.44 added BT/Remote toggle |
| [cwa-kobo-sync.md](cwa-kobo-sync.md) | CWA Kobo sync setup | Sync URL format, token location in CWA UI, KEPUB conversion, Libra Colour cover image fix |
| [calibre-web-kobo-sync.md](calibre-web-kobo-sync.md) | Calibre-Web upstream Kobo sync | Upstream setup steps that CWA inherits; enables KEPUB conversion via kepubify |
| [custom-sync-server.md](custom-sync-server.md) | Custom server config (no Beta Features) | USB config file edit method for 4.45; `devmodeon` search trick to re-enable Beta Features |

## Failed / skipped sources

| URL | Reason |
|-----|--------|
| `https://wiki.mobileread.com/wiki/Kobo_eReader.conf` | Page exists but has no community content |
| `https://wiki.mobileread.com/wiki/Kobo_Wifi` | Page exists but has no community content |
| `https://raw.githubusercontent.com/wiki/crocodilestick/Calibre-Web-Automated/Kobo-Sync.md` | Wrong slug — actual page is `Kobo-Integration-&-Sync` |
| `https://github.com/janeczku/calibre-web/wiki/Kobo-Sync-Feature` | Wiki returned edit UI, not readable content |
