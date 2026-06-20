# Kobo Firmware Changelog (4.39–4.45)

Covers the Kobo Libra Colour and related devices (Clara Colour, Clara BW) across the
firmware range relevant to CWA sync setup.

## Version Summary

| Version     | Date        | Highlight                                      |
|-------------|-------------|------------------------------------------------|
| 4.39.22801  | ~Oct 2024   | Buggy release; caused boot loops; pulled/reverted by some users |
| 4.42.23296  | May 30 2025 | Unremarkable; no notable features documented   |
| 4.44.23552  | ~Nov 2025   | Kobo Remote support; Bluetooth status bar toggle |
| 4.45.23640  | Feb 2026    | Bug fixes; stability; revised model update support |

Versions 4.40, 4.41, 4.43 exist but no notable changelog entries were found for these.

## Detailed Notes

### 4.39.22801

- Flagged as suspicious by developer geek1011 (unusual changes to pickle, font handling,
  Nickel components; described as "obviously still for testing").
- Caused boot loops on some Kobo Touch and other devices.
- The release package labeled for Libra 2 (Freescale) contained Mediatek files — wrong
  hardware target in the download.
- Community recommendation: revert to 4.38.23038 if problems occur.
- No documented changes to api_endpoint, sync settings, or OneStoreServices.

### 4.42.23296 (May 30 2025)

- No notable features documented publicly.
- MobileRead forum thread exists but no technical changelog extracted.

### 4.44.23552 (~Nov 2025)

Official release notes:
1. Added support for **Kobo Remote** (page-turning peripheral accessory)
2. Added **Bluetooth toggle** to the top status bar

No changes to Beta Features, sync settings, api_endpoint, or OneStoreServices.

### 4.45.23640 (Feb 2026) — Current firmware for Libra Colour 23697 build

Official release notes:
- Various bug fixes
- Stability improvements

Beta tester notes:
- Ensures update installation works correctly on revised device models (different internal
  components from the original production run)
- Translation fixes

No changes to sync server behavior, api_endpoint handling, or Beta Features menu.

## Beta Features / Sync Server History

No public changelog entry documents the removal of a Beta Features menu or changes to
how the `api_endpoint` is handled across firmware 4.39–4.45. The config-overwrite behavior
(device restoring `eReader.conf` to defaults on sync) is reported by community users on
newer devices including the Libra Colour, but the exact firmware version that introduced
this behavior has not been pinpointed in available sources.

The `api_endpoint` field in `[OneStoreServices]` has been a supported customization point
since at least firmware 4.x. Its overwrite on sync appears to be a server-side sync
behavior rather than a firmware change — Kobo's sync API pushes device settings back to
the device during initial handshake.

## Sources

- [MobileRead: New Kobo Firmware 4.39.22801](https://www.mobileread.com/forums/showthread.php?t=360326)
- [MobileRead: Firmware 4.42.23296](https://www.mobileread.com/forums/showthread.php?t=368758)
- [eWritable: Kobo Firmware 4.44](https://ewritable.net/brands/kobo/firmware/4-44/)
- [The eBook Reader: Firmware 4.45](https://blog.the-ebook-reader.com/2026/02/26/software-update-4-45-released-for-latest-kobo-ereaders/)
- [MobileRead Wiki: Kobo Firmware Releases](https://wiki.mobileread.com/wiki/Kobo_Firmware_Releases)
- [Patrick Gaskin's Kobo Firmware Downloads](https://pgaskin.net/KoboStuff/kobofirmware.html)
- [eReadersForum: Firmware 4.45 thread](https://www.ereadersforum.com/threads/kobo-firmware-4-45-rolling-out-to-select-colour-and-bw-models.12050/)
