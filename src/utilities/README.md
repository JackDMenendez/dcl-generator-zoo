# src/utilities/

Helper scripts that support the paper.  In this repository, the
utilities are the load-bearing evidence base (not just build steps);
each one is cited from `paper/sections/audit_table.tex`.

## Inherited from Paper II (do not edit)

- **`automorphism_centralizer_extended.py`** -- the 71-element
  per-site centralizer enumeration.  Builds the 143-element
  Pauli$\otimes$Pauli$\otimes$Gell-Mann tensor basis of
  $\mathfrak{su}(12)$, filters to the 71 elements commuting with
  the bipartite tick rule, classifies into 7 categories.  Each
  audit-table row that begins "Centralizer dimension is 71",
  "Extras count is 59", or similar is reproduced by this script.
- **`aut_centralizer_extras_commutators.py`** -- the bracket-
  classification script.  Computes the 708 $[\text{extras},
  \text{SM}]$ brackets and 1711 $[\text{extras}, \text{extras}]$
  brackets and classifies each as `zero` / `in_SM` / `in_extras` /
  `mixed`.

Both files carry a `Provenance` docstring documenting their
identity with the Paper~II v1.0 deposit; they should not be
edited here.

## Zoo-specific (the extension layer)

- **`generator_zoo.py`** -- the catalogue script.  Imports the
  enumeration and rank/span helpers from the two scripts above,
  adds:
  - stable per-generator names (`G_01` .. `G_71`),
  - a 3-bit tensor-factor action tag,
  - $(SU(3), SU(2))$ irrep tagging,
  - chirality-block ($I$ vs $\sigma_x$) labelling,
  - SM-classification subgroup labelling (`J_1`, `SU(2)_W`,
    `SU(3)_c`, `iso_col_mixing`, `sigmaX_iso`, `sigmaX_col`,
    `sigmaX_iso_col`),
  - full bracket-class classification for all $\binom{71}{2} =
    2485$ pairs,

  and emits two artifacts in lockstep:
  - `data/generator_catalogue.json` (machine-readable),
  - `paper/sections/generator_zoo_table.tex` (auto-generated
    LaTeX longtable that the appendix `\input`s).

  Regenerate via:

  ```text
  python -m src.utilities.generator_zoo
  ```

  Runtime: a few minutes on a modern laptop.  The script is
  deterministic; the JSON output is the canonical citeable
  artifact and should be committed.

## Conventions

A utility script in this repo IS evidence (cited from the audit
table), not just a build step.  If a script's output flips an
audit-table row from `STUB` / `PART` to `PASS`, that script and
its companion notes are part of the paper's reproducibility
contract.  Reproducibility is documented in
`paper/sections/reproducibility.tex`.
