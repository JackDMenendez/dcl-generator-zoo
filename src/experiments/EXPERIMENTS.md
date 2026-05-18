# Experiment Index

The dcl-generator-zoo is built primarily on the load-bearing
centralizer-enumeration scripts under `src/utilities/`, not on
runtime experiments.  No `src/experiments/exp_NN_*.py` scripts are
required for the v0.1 audit table.

If Phase~2 or later phases introduce runtime experiments (for
example, sympy stress-tests on the catalogue emit, or numerical
checks of the bracket-class lookup), add them here as a markdown
table with columns: `ID`, `Status`, `What it claims`,
`Audit row`, `Companion doc`.  No rows exist at v0.1.

## Status legend

- `STUB` -- audit row added, experiment script not yet written or
  not yet producing a clean signal.
- `PART` -- experiment runs and demonstrates the mechanism but the
  quantitative match is incomplete; specific gap noted in the
  companion doc.
- `PASS` -- experiment confirms the audit row to stated precision.
- `FAIL` -- experiment disconfirms the audit row.  Keep the row;
  failure is evidence too.

Status here should equal status in `audit_table.tex`.  If they
disagree, the audit table is the authority and this file is wrong.
The `audit_universe.py` master roll-up uses `audit_table.tex` as
its authority and parses each experiment's most recent
`data/*.log` for the actual cached PASS/FAIL marker -- see
`../../audit_universe.md` for the full model.

The v0.1 audit table's `PASS` rows are evidenced by analytical /
script output cited as `src/utilities/<script>.py`, not by
`exp_NN_*.log` files.  `audit_universe.py` reports them as-is
without trying to parse logs.
