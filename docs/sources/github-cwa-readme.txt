# Calibre-Web Automated: Overview

**Calibre-Web Automated (CWA)** is a free, open-source self-hosted digital library solution designed as an all-in-one alternative to running Calibre and Calibre-Web separately.

## Core Purpose

The project aims to combine "the modern lightweight web UI from Calibre-Web with the robust, versatile feature set of Calibre, with a slew of extra features and automations thrown in on top."

## Key Features

**Stock Calibre-Web capabilities include:**
- Modern Bootstrap 3 interface with user management
- OPDS feed support for e-readers
- Metadata editing and OAuth 2.0/OIDC authentication
- In-browser e-book reading across multiple formats

**CWA-specific additions:**
- Automatic book ingest (27 supported formats)
- Multi-format conversion (EPUB, MOBI, AZW3, KEPUB, PDF)
- Intelligent duplicate detection and management
- Automated metadata fetching and enforcement
- EPUB fixing service for Amazon compatibility
- KOReader sync functionality
- Deep analytics and statistics dashboard
- Batch editing and deletion tools
- Smart "Magic Shelves" with dynamic rules
- Auto-send to e-readers after processing

## Installation

CWA is deployed via Docker with three essential volume binds:
- `/config` - Application data and logs
- `/cwa-book-ingest` - Temporary ingest folder (files deleted after processing)
- `/calibre-library` - Persistent library location

**Default login:** admin / admin123

## Special Considerations

The project explicitly states: "CWA does not approve of or support piracy of copyrighted materials and is not responsible for user behaviour."

Network share deployments require setting `NETWORK_SHARE_MODE=true` to disable SQLite WAL and use polling-based file watching for reliability.

---
SOURCE: https://raw.githubusercontent.com/crocodilestick/Calibre-Web-Automated/main/README.md
FETCHED: 2026-06-19
