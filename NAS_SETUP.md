# NAS Setup Guide
[View on GitHub](https://github.com/cmccormack/bookshelf/blob/main/NAS_SETUP.md)

Deploying CWA on a Synology DS918+ (DSM 7.1.1, Btrfs volume).

> For Synology DS918+ platform docs (SSH hardening, Docker administration, DSM configuration, security), see [MackNet NAS Docs](https://github.com/cmccormack/macknet/tree/main/docs/synology/).

## Prerequisites

- SSH access to the NAS
- Docker installed via Container Manager (Package Center)
- `git` installed via Package Center

## Environment

| Item | Value |
|------|-------|
| Docker binary | `/usr/local/bin/docker` (not in default SSH PATH — use full path) |
| docker-compose | v1 at `/usr/local/bin/docker-compose` — use `docker-compose`, not `docker compose` |
| git binary | `/var/packages/git/target/bin/git` (not in PATH) |
| PUID/PGID | Get from `id $(whoami)` on the NAS |

## Step 1: Clone the repo

```bash
ssh <user>@<nas-ip>
/var/packages/git/target/bin/git clone https://github.com/<your-username>/bookshelf.git /volume1/docker/cwa-library/bookshelf
```

## Step 2: Create .env

```bash
cat > /volume1/docker/cwa-library/bookshelf/.env << 'EOF'
PUID=<uid>
PGID=<gid>
TZ=America/New_York
PORT=8083

ADMIN_USER=admin
ADMIN_PASSWORD='<strong-password>'
EOF
chmod 600 /volume1/docker/cwa-library/bookshelf/.env
```

Get your PUID/PGID with `id $(whoami)` on the NAS.

## Step 3: Create the calibre shared folder

> **Btrfs gotcha:** The NAS volume is Btrfs-formatted. Shared folders on Btrfs are subvolumes — you cannot promote an existing regular directory to a shared folder. If you pre-created `/volume1/calibre` via `mkdir`, delete it first.

```bash
# Remove if it already exists as a regular directory
sudo rm -rf /volume1/calibre

# Create as a proper Btrfs subvolume via DSM
sudo /usr/syno/sbin/synoshare --add calibre 'Calibre ebook library' /volume1/calibre '' '' '' 1 0

# Create subdirectories and set ownership
sudo mkdir -p /volume1/calibre/library /volume1/calibre/ingest
sudo chown -R <user>:users /volume1/calibre/library /volume1/calibre/ingest
```

The `calibre` share will now appear in File Station.

## Step 4: Create the config directory

```bash
sudo mkdir -p /volume1/docker/cwa-library/config
sudo chown -R <user>:users /volume1/docker/cwa-library/config
```

## Step 5: Deploy

```bash
cd /volume1/docker/cwa-library/bookshelf
/usr/local/bin/docker-compose -f docker-compose.yml -f docker-compose.nas.yml up -d
```

The NAS overlay (`docker-compose.nas.yml`) enables:
- `WATCH_METHOD=polling` — inotify is not available on Synology over network shares
- `NETWORK_SHARE_MODE=true` — disables SQLite WAL mode to prevent lock errors on Btrfs

## Step 6: Harden CWA (run from your Mac)

```bash
uv run python setup_cwa.py --host <nas-ip>
```

Changes the default admin password and enables Kobo sync.

## Step 7: Set up Kobo sync

1. Log into CWA at `http://<nas-ip>:8083`
2. Go to **User Profile → Kobo Sync → Create token** — copy the token
3. Connect Kobo via USB, then from your Mac:

```bash
uv run python kobo_set_server.py /Volumes/KOBOeReader <nas-ip> 8083 <token>
```

4. Eject Kobo and sync

> Note: the Kobo sync token is per-CWA-install. If you re-deploy from scratch, generate a new token and re-run `kobo_set_server.py`.

See `KOBO_SETUP.md` for full Kobo troubleshooting.

## Adding books

Drop files into `/volume1/calibre/ingest/` via **File Station → calibre → ingest**.

CWA polls the folder and auto-imports. Files are removed from ingest once processed. EPUBs are imported directly; PDFs and MOBIs are converted to EPUB first.

## Troubleshooting

### "Troubleshooting your DB" page on first launch

CWA can't find `metadata.db`. Usually a permissions issue after recreating the library directory.

Fix:
```bash
# Initialize the library DB from inside the container
/usr/local/bin/docker exec cwa-library calibredb check_library --library-path /calibre-library

# Fix ownership and permissions — calibredb creates files as root,
# and Btrfs ACLs don't pass through to Docker containers
sudo chown -R <user>:users /volume1/calibre/library/
sudo chmod -R u+rwX,g+rX /volume1/calibre/library/

# Restart
/usr/local/bin/docker restart cwa-library
```

After the restart, log out and back into the CWA web UI — the browser session caches the error state and won't clear until you re-authenticate.

### Files in library have no permissions in container

Btrfs shared folders use ACLs (shown as `+` in `ls -la`). Docker does not inherit these ACLs —
the container sees only the raw Unix permissions, which may be `----------`.

Fix — set explicit Unix permissions and correct ownership:

```bash
sudo chown -R <user>:users /volume1/calibre/library/
sudo chmod -R u+rwX,g+rX /volume1/calibre/library/
/usr/local/bin/docker restart cwa-library
```

This is required after:
- Initial library creation (new files are owned by root)
- Running `calibredb` inside the container via `docker exec` (also creates root-owned files)

### Fix duplicate/corrupted author metadata

If `calibredb` or a bad ingest creates a duplicated author name (e.g. `Wilson, Robert Charles Charles`):

```bash
# Fix author name and sort
/usr/local/bin/docker exec cwa-library calibredb set_metadata \
  --field authors:'Correct Author Name' \
  --field author_sort:'Last, First' \
  --library-path /calibre-library <book-id>

# Fix permissions after (calibredb runs as root)
sudo chown -R <user>:users /volume1/calibre/library/
sudo chmod -R u+rwX,g+rX /volume1/calibre/library/

# Restart to pick up changes
/usr/local/bin/docker restart cwa-library
```

### Kobo sync fails with "Retry sync"

Check CWA logs. If you see `Using fallback Kobo resource definitions` and `Received unproxied request`, the Kobo proxy is disabled. Enable it:

```bash
sqlite3 /volume1/docker/cwa-library/config/app.db 'UPDATE settings SET config_kobo_proxy=1;'
/usr/local/bin/docker restart cwa-library
```

The proxy allows non-library requests (firmware checks, resource definitions) to pass through to Kobo's servers while CWA handles library sync.

### Enable DEBUG logging

```bash
sqlite3 /volume1/docker/cwa-library/config/app.db 'UPDATE settings SET config_log_level=10;'
/usr/local/bin/docker restart cwa-library
# Check logs:
/usr/local/bin/docker logs cwa-library -f
# Restore INFO after troubleshooting:
sqlite3 /volume1/docker/cwa-library/config/app.db 'UPDATE settings SET config_log_level=20;'
```

### Update to latest CWA image

```bash
cd /volume1/docker/cwa-library/bookshelf
/usr/local/bin/docker-compose -f docker-compose.yml -f docker-compose.nas.yml pull
/usr/local/bin/docker-compose -f docker-compose.yml -f docker-compose.nas.yml up -d
```

## Verified on

- Synology DS918+, DSM 7.1.1-42962
- Docker 20.10.3, docker-compose 1.28.5
- CWA v2.2.1, Calibre 9.1
