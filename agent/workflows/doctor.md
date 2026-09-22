# ofo-doctor

## Goal

Inspect the real environment before financial tooling.

## Procedure and controls

Run `python scripts/ofo.py doctor` and `python scripts/ofo.py providers`. Report installed versions, missing native packages and missing variable NAMES, not values. Distinguish source existence, local execution, SDK installation and live validation. Never paste credentials. Offer the authorized setup command only when installation is requested; it is not needed to view prebuilt HTML. Do not silently execute paid or live calls. Store any diagnostic report outside the repository after review.

## Completion

Return the actual calculation/output location, the methods executed and their limitations. Do not claim installation, live connection or host validation merely because source code exists.
