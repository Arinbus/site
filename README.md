# Arinbus field notes

Small, evidence-linked articles from AI-assisted technical work.

Public site: https://arinbus.github.io/site/

## Notes

- `notes/runx-receipts.html` — a real Runx 0.8.2 validation and receipt workflow.
- `notes/frantic-first-bounty.html` — a candid Sourcey/Frantic bounty field report.
- `evidence/*.json` — structured observations for delivery verification.
- `evidence/*-report.md` — bullet-based delivery reports consumed by Frantic preflight.

## Verification

```bash
python3 scripts/verify_site.py
```

The verifier checks local link targets, JSON evidence contracts, disclosure text, required external links, and accidental private-path/secret markers.
