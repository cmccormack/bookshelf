# cwa-library

Self-hosted ebook library using [Calibre-Web Automated](https://github.com/crocodilestick/Calibre-Web-Automated).
Kobo e-reader syncs wirelessly via CWA's native Kobo sync protocol.

## Flow

```
Drop file into ingest/ → auto-converted + metadata fetched → Calibre library → Kobo sync
```

## Quick Start (local testing)

```bash
cp .env.example .env          # set PUID/PGID
mkdir -p config library ingest
docker compose up -d
uv run python setup_cwa.py --rotate-password   # set strong password + enable Kobo sync
```

Open http://localhost:8083

## NAS Deployment

See **[NAS_SETUP.md](NAS_SETUP.md)** for the full guide. Key differences from local:

- Docker binary is at `/usr/local/bin/docker` (not in SSH PATH)
- Uses `docker-compose` v1, not `docker compose` v2
- Volume is Btrfs — shared folders must be created via `synoshare`, not `mkdir`
- Deploy with the NAS overlay: `docker-compose -f docker-compose.yml -f docker-compose.nas.yml up -d`

## Kobo Setup

See **[KOBO_SETUP.md](KOBO_SETUP.md)**. Short version:

```bash
# Get token from CWA: User Profile → Kobo Sync → Create token
uv run python kobo_set_server.py /Volumes/KOBOeReader <host-ip> 8083 <token>
```

Beta Features sync menu is absent on firmware 4.39+ — USB config patch is required.

## Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Base config (local testing) |
| `docker-compose.nas.yml` | NAS overrides — polling watcher, network share mode, NAS volume paths |
| `.env.example` | Environment variable template |
| `setup_cwa.py` | Admin password management + Kobo sync enable via Playwright (`--rotate-password` / `--update-password`) |
| `kobo_set_server.py` | Patches Kobo eReader.conf via USB to point at CWA sync server |
| `make_test_pdf.py` | Generates a valid test PDF for ingest/conversion testing |
| `NAS_SETUP.md` | Full NAS deployment guide (Synology DS918+, DSM 7, Btrfs) |
| `KOBO_SETUP.md` | Kobo connection instructions |
| `TASKS.md` | Setup task log |
| `CLAUDE.md` | Project context for Claude Code sessions |

## Ports

| Service | Port |
|---------|------|
| CWA Web UI + Kobo sync | 8083 |

## Phase 2
See `CLAUDE.md` for planned mobile upload + preview branch.
