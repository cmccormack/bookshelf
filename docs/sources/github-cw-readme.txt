# Calibre-Web Overview

**Purpose**: Calibre-Web is a web application that provides "a clean and intuitive interface for browsing, reading, and downloading eBooks using a valid Calibre database."

**Key Capabilities**:
The platform offers extensive features including responsive Bootstrap interface, comprehensive user management, multilingual support (20+ languages), OPDS feed compatibility, advanced search functionality, metadata editing, eBook conversion, in-browser reading across multiple formats, and authentication via LDAP, OAuth, or proxy methods.

**Installation Method**:
The recommended approach involves creating a Python virtual environment, then installing via pip with the command `pip install calibreweb`, followed by launching the application using `cps`.

**System Requirements**:
Users need Python 3.7 or newer, ImageMagick for cover extraction, and optionally the Calibre desktop application for conversion features or Kepubify for Kobo device synchronization.

**Getting Started**:
After installation, users access the interface at localhost:8083, log in with default credentials (admin/admin123), configure the Calibre database location through the admin panel, and customize their instance settings.

**Deployment Options**:
Pre-built Docker images are available through LinuxServer for both x64 and ARM architectures, with optional Calibre binary integration available via environment variables.

**Support & Community**:
The project maintains comprehensive wiki documentation, active Discord community, and welcomes bug reports and feature requests through its GitHub repository.

---
SOURCE: https://raw.githubusercontent.com/janeczku/calibre-web/master/README.md
FETCHED: 2026-06-19
