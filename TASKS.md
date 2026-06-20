# Tasks

## Status: NAS deploy complete ✅

All local test and NAS deployment tasks are done. See `NAS_SETUP.md` for the full deployment guide.

---

## Completed Tasks

### Task 1: Environment check ✅
Docker (OrbStack 28.2.2), Compose v2.36.2 confirmed. PUID=501, PGID=20 (chris:staff). Port 8083 free.

### Task 2: Local setup ✅
Copied `.env`, set PUID=501/PGID=20. Created `config/`, `library/`, `ingest/` with correct ownership.

### Task 3: Deploy locally ✅
`docker compose up -d` — container healthy at http://localhost:8083. CWA + Calibre 9.1.

### Task 4: First login + hardening ✅
Password changed (stored in `.env` as ADMIN_PASSWORD). Kobo sync enabled via Playwright automation (`setup_cwa.py`). Library path auto-configured by CWA from Docker volume mount — no manual config needed.

### Task 5: Ingest test ✅
EPUB: Alice's Adventures in Wonderland imported within seconds, kindle-epub-fixer applied.
PDF: Valid PDF converted to EPUB via Calibre in 1.19s and imported. (Note: Gutenberg PDFs are malformed — use `make_test_pdf.py` to generate a clean test PDF.)

### Task 6: Kobo connection test ✅
Patched via USB with `kobo_set_server.py` (Beta Features menu absent on 4.45.23697). Synced over LAN — both Alice in Wonderland books arrived on device. URL format: `http://<ip>:8083/kobo/<token>`.

### Task 7: Document results ✅
KOBO_SETUP.md updated with exact steps, working URL format, and verified firmware/version. Local-test phase complete.

### Task 8: NAS deploy ✅
Deployed on DS918+ (DSM 7.1.1, Btrfs). Key gotchas: docker binary not in SSH PATH; docker-compose v1 only; Btrfs volumes require shared folders be created via `synoshare` not `mkdir`. Full steps in `NAS_SETUP.md`.

---

## Notes
- inotify not available on NAS — polling mode active via `docker-compose.nas.yml` override
- Library path at `/calibre-library` is auto-detected by CWA; no manual config needed
- Kobo sync token is per-CWA-install — re-generate on new installs
- Default admin password changed — see `.env` for ADMIN_PASSWORD
- To add books: drop files into `/volume1/calibre/ingest/` via File Station (calibre → ingest)
