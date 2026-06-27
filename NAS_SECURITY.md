# NAS Security Hardening — DS918+ / CWA
[View on GitHub](https://github.com/cmccormack/bookshelf/blob/main/NAS_SECURITY.md)

CWA-specific security for the Synology DS918+.

> For platform-level security (SSH hardening, DSM firewall, 2FA, VPN, auto-block, Security Advisor), see [MackNet NAS Docs](https://github.com/cmccormack/macknet/tree/main/docs/synology/).

---

## Quick Wins (done)

- [x] `chmod 755 ~/.oh-my-zsh/custom` — world-writable dir was a local shell injection vector
- [x] `chmod 644 ~/.oh-my-zsh/custom/example.zsh` — world-writable executable zsh file
- [x] `chmod 755 ~/.oh-my-zsh/custom/themes` — world-writable themes dir
- [x] `chmod 600 /volume1/docker/cwa-library/bookshelf/.env` — CWA admin password readable by `users` group
- [x] Verified no `--privileged` flag in `docker-compose.nas.yml`
- [x] CWA admin password rotated to strong generated value

## DSM Platform Hardening (pending)

These are NAS platform items. See [MackNet NAS Docs](https://github.com/cmccormack/macknet/tree/main/docs/synology/) for step-by-step instructions.

- [ ] **Security → Protection** — enable DoS protection
- [ ] **Security → Account → Auto Block** — 5 failures / 10 min, block 30 days
- [ ] **Notification → Email** — enable auth alerts and auto-block notifications
- [ ] **User & Group → admin → Disable** — disable built-in `admin` account
- [ ] **Personal → Account → 2-Factor Authentication** — enable for your user account
- [ ] **SSH hardening** — non-default port, key-only auth, `sshd_config` via Task Scheduler boot script
- [ ] **VPN** — Tailscale or WireGuard; highest-leverage long project (moves SSH and DSM off public internet)

---

## CWA-Specific Security

### TLS on port 8083

Plain HTTP means the Kobo sync token and admin session cookie travel in cleartext on travel networks.

1. Get a domain — Synology DDNS (`yourname.synology.me`) is free and built-in
2. Issue Let's Encrypt cert: **Control Panel → Security → Certificate → Add → Let's Encrypt**
3. Configure reverse proxy: **Control Panel → Application Portal → Reverse Proxy**
   - External: HTTPS 8443 → Internal: HTTP localhost:8083
4. Re-run `kobo_set_server.py` with the `https://` URL

### Ingest folder permissions

The ingest folder is a file-parsing pipeline. Any write access allows dropping crafted files that exploit Calibre parser CVEs (documented history: CVE-2019-17163, CVE-2022-26888) for RCE inside the container.

```bash
chmod 750 /volume1/calibre/ingest
```

Verify the CWA container PUID can still read from it after the change.

### CWA login rate limiting

CWA Admin UI → Basic Configuration → Security → Enable Login Rate Limiting
Default 5/min — acceptable, or tighten to 3.

### Geo-IP firewall on port 8083

In UDM Pro: Firewall & Security → Firewall Rules → Internet In
Restrict port 8083 to countries you actually travel to. Cuts ~90% of internet scanner traffic while keeping Kobo sync working on the road.

### Btrfs snapshot schedule for calibre

Storage Manager → Snapshot Replication → calibre shared folder
- Hourly, retain 48 hours
- Daily, retain 30 days

Snapshots are not a backup (same volume). Pair with Hyper Backup to offsite storage.

> **Warning:** Btrfs snapshots preserve historical `.env` passwords. Even after password rotation, old credentials survive in `.snapshot/<date>/`. If a breach is suspected, purge snapshots explicitly.

### CWA Docker network isolation

Isolate the CWA container on a dedicated bridge to prevent a container compromise from pivoting to other containers or NAS services:

```yaml
# docker-compose.nas.yml addition
networks:
  cwa_net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/24

services:
  calibre-web-automated:
    networks:
      - cwa_net
    ports:
      - "8083:8083"
```

### CWA access log monitoring

Periodically review for unexpected access patterns (unexpected IPs fetching book lists or sync endpoints):

```bash
/usr/local/bin/docker exec cwa-library tail -n 100 /config/logs/cwa.log | grep -v "Kobo"
```

If you see unexpected IPs: rotate the Kobo sync token and CWA password.

---

## Threat Notes

### Kobo sync token

The token is static and stored in two places: Btrfs snapshots of the `.env`, and the CWA config database at `/volume1/docker/cwa-library/config/app.db`. Any attacker with read access to the config volume can extract it from `app.db` directly without cracking. Rotate via **CWA Admin UI → Kobo → Regenerate** then re-run `kobo_set_server.py`. Rotate if you suspect token capture (hotel network, lost device).

### Default credential window

Fresh CWA deploys start as `admin / admin123`. Port 8083 should not be reachable until `setup_cwa.py` has run. If the config volume is deleted and CWA is redeployed, the default window reappears.

### `calibredb` runs as root in container

`docker exec` + `calibredb` creates root-owned files (requiring the `chown` fix in NAS_SETUP.md). Container compromise via a malicious ingest file gives an attacker root within the container namespace — lowering the bar for any kernel-escape attempt.

### docker-compose v1 is EOL

docker-compose v1 (Python-based) reached end-of-life May 2023 with no further patches. DSM 7.2 Container Manager ships compose v2. Upgrade path is a DSM update.

### DSM QuickConnect

If enabled, routes DSM admin traffic through Synology relay servers. Disable if not actively used: **Control Panel → QuickConnect → Disable**.

---

## Priority Summary

| Control | Priority | Effort |
|---|---|---|
| chmod 600 .env | Critical (done) | 2 min |
| Verify no --privileged in compose | Critical (done) | 2 min |
| CWA login rate limiting | High | 5 min |
| Geo-IP / country firewall on 8083 | High | 15 min |
| Ingest folder permissions (chmod 750) | High | 5 min |
| Btrfs snapshots for calibre | Medium | 20 min |
| CWA Docker network isolation | Medium | 30 min |
| TLS reverse proxy for CWA | Medium | 2 hr |
| Kobo sync token rotation (6-month cadence) | Ongoing | 5 min |

For NAS platform items (SSH, DSM admin, VPN, 2FA, auto-block) see [MackNet NAS Docs](https://github.com/cmccormack/macknet/tree/main/docs/synology/).
