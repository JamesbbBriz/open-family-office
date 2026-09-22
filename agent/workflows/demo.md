# Run and explain the public synthetic demonstration

Read `AGENTS.md` first. Canonical workflow; do not duplicate its business rules in runtime adapters.


## Procedure
1. Read `examples/README.md`; confirm `synthetic: true` on the selected fixture.
2. Run `python scripts/ofo.py demo`. No network, keys or paid agent is necessary for the numerical demo.
3. Run the recession and business-sale scenarios as documented in `docs/QUICKSTART.md`.
4. Explain why net worth differs from spendable cash, why pension is a wrapper, and why a sale is not recurring income.
5. Open `public/demo.html` for a precomputed interactive walkthrough. It is not a general-purpose hosted app.
6. For report files use `demo --out <new-directory-outside-repo>`.

## Public output
Use only bundled synthetic outputs and the checked-in demonstration. Never swap in a user's profile for a recording.
Runtime skill behaviour must be tested separately; passing Python tests does not prove model compliance.
