# cwa-library
[View on GitHub](https://github.com/cmccormack/bookshelf/blob/main/CLAUDE.md)

## Project Overview
Self-hosted ebook library using Calibre-Web Automated (CWA) on a Synology DS918+ NAS.
Kobo e-reader syncs wirelessly via CWA's native Kobo sync protocol over a UniFi travel
router network — at home or at the beach.

## Repo
github.com/<your-username>/bookshelf

## Branch Strategy
- `main` — stable, tested, NAS-ready
- `local-test` — local Docker testing before NAS deploy (complete)
- `feature/*` — future additions (mobile upload UI, epub.js preview, etc.)

## Infrastructure
- NAS: Synology DS918+, DSM 7.1.1, Btrfs volume
- NAS volumes: `/volume1/` (primary)
- Networking: UDM Pro at home, UniFi travel router on the road
- Docker: docker-compose v1 (`/usr/local/bin/docker-compose`) — NOT v2 plugin
- SSH: `<user>@<nas-ip>`, public key auth
- Platform docs (SSH, Docker admin, DSM config, security): [MackNet NAS Docs](https://github.com/cmccormack/macknet/tree/main/docs/synology/)

## Architecture (Phase 1 — current)
Single CWA container. No custom code. No Flask. No Redis.

```
Phone / browser
    ↓ upload via CWA web UI or drop into ingest share (File Station → calibre → ingest)
/cwa-book-ingest  (watched folder, polling mode on NAS)
    ↓ polling → auto format detection → conversion → metadata fetch
/calibre-library  (Calibre database + EPUB files)
    ↓ native Kobo sync protocol (port 8083)
Kobo e-reader
```

## Volume Layout
### Local testing
Uses relative paths — everything lives in the project folder:
- `./config`        → CWA config + app database
- `./library`       → Calibre library (metadata.db + book files)
- `./ingest`        → drop books here to import

### NAS deployment
- `/volume1/docker/cwa-library/config`   → CWA config
- `/volume1/calibre/library`             → Calibre library
- `/volume1/calibre/ingest`              → ingest folder
- `/volume1/docker/cwa-library/bookshelf` → cloned repo (compose files + scripts)

## Key Technical Notes
- CWA auto-detects the Calibre library path from the `/calibre-library` mount — no manual config needed
- On NAS, inotify is unavailable — polling mode is enabled via `NETWORK_SHARE_MODE=true` and `WATCH_METHOD=polling` in `docker-compose.nas.yml`
- SQLite WAL mode disabled on NAS via `NETWORK_SHARE_MODE=true` — prevents lock errors on Btrfs
- Default credentials: admin / admin123 — `setup_cwa.py` changes this on first run
- PUID/PGID must match the owner of the library and ingest folders (get from `id $(whoami)` on the NAS)
- Kobo sync token is per-CWA-install — must regenerate after fresh deploy
- Kobo Beta Features sync menu absent on firmware 4.39+ — use `kobo_set_server.py` via USB

## Kobo Sync Notes
- Kobo proxy (`config_kobo_proxy=1`) must be enabled — without it the Kobo can't fetch
  resource definitions and shows "Retry sync" even though the library request gets through
- CWA converts EPUB → KEPUB on-the-fly during sync (via kepubify) — library stays as EPUB
- After metadata edits via `calibredb` inside the container, always fix permissions and restart

## Btrfs Gotcha (NAS)
Synology Btrfs volumes use subvolumes for shared folders. You cannot promote a regular
directory to a shared folder. Always create the `calibre` share via:
```bash
sudo /usr/syno/sbin/synoshare --add calibre 'Calibre ebook library' /volume1/calibre '' '' '' 1 0
```
If `/volume1/calibre` already exists as a regular directory, delete it first.

After any operation that creates files as root inside the container (e.g. `calibredb` via
`docker exec`), fix ownership:
```bash
sudo chown -R <user>:users /volume1/calibre/library/
```

## Tooling (Python, managed with uv)
- `setup_cwa.py` — password management + Kobo sync enable via Playwright (`--rotate-password`, `--update-password`, `--host` for NAS)
- `kobo_set_server.py` — patches Kobo eReader.conf via USB
- `make_test_pdf.py` — generates a valid test PDF for ingest testing

## Phase 2 (future branch: feature/mobile-upload)
Mobile upload UI with epub.js preview and conversion options.
Will share the same ingest folder — files dropped there get picked up by CWA automatically.
No changes to Phase 1 required.

