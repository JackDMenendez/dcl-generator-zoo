# data/

Data files produced and consumed by experiments, and the
machine-readable catalogue emitted by the generator zoo.

## What goes here

- **`generator_catalogue.json`** -- the canonical machine-readable
  catalogue of the 71-dim per-site automorphism algebra, written by
  `src/utilities/generator_zoo.py`.  Downstream tooling that
  consumes the zoo should read this file rather than scraping the
  `paper/sections/generator_zoo_table.tex` longtable.  Schema
  documented in the docstring of `generator_zoo.py`; current
  `schema_version` is `1`.  Tracked in git -- it is the
  human-citeable artifact of each catalogue release.
- `*.npy` -- NumPy arrays produced by experiment scripts.
- `*.log` -- stdout captures from long-running experiments.
- `*.csv` -- tabular results that downstream figures read.

## What does NOT go here

- Source code (lives in `src/`).
- Figures (live in `paper/figures/` or the repo-root `figures/`).
- Build artefacts (live in `build/`).

## Tracking in git

`.npy` files are tracked when small enough that the repo stays
manageable. For multi-gigabyte outputs, store them in Zenodo or a
data-archive service and refer to them by DOI from the experiment's
companion `.md` doc and from the audit-table evidence column.

`.log` files are tracked (the `.gitignore` has `!data/*.log`) so the
exact stdout of each PASS/FAIL run is part of the project history.

## Naming

`<exp_id>_<descriptor>.{npy,log}` -- e.g. `exp_00_example.npy`,
`exp_12c_grid_113.log`. The `<exp_id>` prefix lets you `ls data/exp_12*`
and see everything that experiment touched.
