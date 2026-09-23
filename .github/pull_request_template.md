## Why

What problem does this change solve?

## What changed

Summarize the implementation. Keep unrelated refactors out of the PR.

## Financial assumption or workflow affected

If this changes accounting, cash flow, ownership, policy, scenarios, providers or quantitative research, state the assumption/invariant explicitly.

Write `None` for documentation-only or unrelated changes.

## Evidence / data provenance

What fixtures, public sources or synthetic examples support the change?

Do not include private household data.

## Tests actually run

```text
[ ] python -m unittest discover -s tests -v
[ ] python scripts/ofo.py demo
[ ] python scripts/release_check.py
[ ] node tests/sandbox.test.cjs
[ ] npm run build
[ ] other:
```

## Screenshots

Required for meaningful UI/dashboard changes. Otherwise write `N/A`.

## Known limits / follow-ups

What remains intentionally out of scope?

## Checklist

- [ ] Uses only synthetic / authorized redistributable data.
- [ ] Does not add credentials or a private workspace.
- [ ] Keeps confirmed facts, assumptions and model outputs separate.
- [ ] Does not duplicate canonical financial rules in host-specific adapters.
- [ ] Keeps provider implementation / live-verification status honest.
- [ ] Adds or updates tests for user-visible behavioural changes.
- [ ] Updates docs / changelog when the public interface changes.
- [ ] Does not add trading, money movement or hidden network side effects.
