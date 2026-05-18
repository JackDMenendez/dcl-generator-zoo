<!-- markdownlint-disable MD022 MD025 MD033 MD060 -->
# CLAUDE.md -- Working Brief for Claude Code

> Project: dcl-generator-zoo -- A Catalogue of the 71-Dimensional
> Per-Site Automorphism Algebra of the A=1 Discrete Causal Lattice

This file is the project memory for Claude Code.  Keep it updated so
a new conversation can continue work without the full chat history.

---

## CURRENT STATUS (2026-05-16) -- v0.1-DRAFT (Phase~2 written, first run pending)

Repository freshly provisioned on 2026-05-16 from
`dcl-paper-experiment-template`.  The substantive algebraic results
that the zoo catalogues all come from Paper~II Phase~3, which is
already deposited on Zenodo at
[doi:10.5281/zenodo.20240736](https://doi.org/10.5281/zenodo.20240736).
This catalogue is the companion artifact that turns those results
into a citeable reference for downstream papers in the series and
for external work.

What is in place (v0.1-DRAFT):

- **Inherited evidence (PASS).**  The two load-bearing centralizer
  enumeration scripts are reproduced verbatim from Paper~II:
  - `src/utilities/automorphism_centralizer_extended.py` -- enumerates
    the 143-element Pauli$\otimes$Pauli$\otimes$Gell-Mann tensor
    basis of $\mathfrak{su}(12)$, filters to the 71 elements
    commuting with the bipartite tick rule, classifies into 7
    categories ($J_1$, SU(2)$_W$, SU(3)$_c$, 4 extras types).
  - `src/utilities/aut_centralizer_extras_commutators.py` -- computes
    708 $[\text{extras}, \text{SM}]$ brackets and 1711
    $[\text{extras}, \text{extras}]$ brackets, classifies each as
    zero / in_SM / in_extras / mixed.
- **Inherited textual context.**  Four notes copied from Paper~II
  with provenance prefixes (`aut_centralizer_enumeration.md`,
  `aut_centralizer_extras_commutators.md`, `extras_as_a1_accounting.md`,
  `su3_generation_from_colour_memory.md`).
- **Generator-zoo extension layer (PART; written, awaits first
  user-side run).**  `src/utilities/generator_zoo.py` builds the
  catalogue (71 generators with stable `G_01`..`G_71` names + 3-bit
  factor-action tags + $(SU(3), SU(2))$ irrep tags + chirality-block
  labels), classifies all $\binom{71}{2} = 2485$ brackets, and emits
  both `data/generator_catalogue.json` (machine-readable) and
  `paper/sections/generator_zoo_table.tex` (auto-generated LaTeX
  longtable for the appendix).
- **Paper skeleton.**  Title page, abstract, introduction, audit
  table, generator-zoo appendix (`paper/sections/generator_zoo.tex`),
  references all rewritten zoo-specific.  The auto-generated
  catalogue table is `\input`-included via `\IfFileExists`, so the
  paper builds even before the first script run (with a visible
  placeholder reminder).  Conclusion and acknowledgements appendices
  retain template `\placeholder{}` markers pending v1.0.

**Next concrete actions:**

1. Run `setup.cmd` to create `.venv` and install dependencies
   (notably the new sympy dependency).
2. Run the inherited scripts to reproduce Paper~II Phase~3
   evidence:

   ```text
   python -m src.utilities.automorphism_centralizer_extended
   python -m src.utilities.aut_centralizer_extras_commutators
   ```

3. Run the catalogue script (a few minutes):

   ```text
   python -m src.utilities.generator_zoo
   ```

   On success it writes `data/generator_catalogue.json` and
   `paper/sections/generator_zoo_table.tex`.  Commit both to git;
   the JSON is the canonical citeable artifact.
4. Build the paper with the auto-generated table in place
   (`build.cmd paper`).  Verify the appendix renders cleanly.
5. Flip the relevant audit-table rows from PART to PASS in
   `paper/sections/audit_table.tex` (rows 8-13 of the
   "Zoo-specific" block); the conjectural-decoherence-labels
   row stays STUB.
6. Tag v0.1 (optional baseline) or proceed to v1.0 deposit on
   Zenodo (request a DOI, add it to `CITATION.cff` and
   `paper/main.tex`'s `\thanks{}`, then tag).

---

## What This Project Is

A **living catalogue** of the 71-dimensional per-site automorphism
algebra of the A=1 Discrete Causal Lattice.  Phase~3 of Paper~II
established that the discrete-Hermitian centralizer of the
bipartite tick rule on the per-site $\mathbb{C}^{12} =
\mathbb{C}^2_\text{chir} \otimes \mathbb{C}^2_\text{iso} \otimes
\mathbb{C}^3_\text{col}$ amplitude has dimension 71, structurally
$\mathfrak{su}(6)_+ \oplus \mathfrak{su}(6)_- \oplus \mathfrak{u}(1)$,
with the 12-dimensional Standard Model gauge subalgebra inside as
a non-normal subgroup and a 59-generator complement (``extras'')
transforming under $SU(3) \times SU(2)$ as $(\mathbf{8}, \mathbf{3})$
leptoquark-flavoured plus chirality-$\sigma_x$-twisted
SM-flavoured.

That structure is the *result* this zoo catalogues.  The zoo's
value-add is giving each of the 71 generators a stable name, an
irrep tag, a tensor-factor action tag, and a bracket-class
classification against every other generator -- and emitting all
of this as machine-readable JSON plus a printable \LaTeX{} longtable.
The intent is that follow-on papers in the series (and external
work building on the framework's algebraic structure) can refer
to specific generators by name rather than re-deriving them.

**Living-document framing.**  The zoo is expected to accumulate
catalogue revisions over time -- new naming conventions, sharper
tags, additional structural notes, eventually a generalisation
beyond per-site $\mathbb{C}^{12}$ (a generation index would
extend the centralizer by adding additional tensor factors).
Each release is a frozen snapshot with its own Zenodo DOI, so
that downstream papers can cite a *specific* version that will
not change under them.  Stability guarantees:

- Within a `v0.Y` line: breaking changes (rename fields, change
  the `G_NN` ordering, change the JSON schema) are allowed; the
  catalogue is pre-stable.
- At `v1.0` and beyond: the `G_NN` naming convention and the
  JSON schema are frozen for downstream consumption.  Breaking
  changes require a `v2.0`.

See `release_notes/README.md` for the authoritative release
procedure.

---

## Paper Title and Theme

**Title:** The dcl-generator-zoo: A Catalogue of the 71-Dimensional
Per-Site Automorphism Algebra of the A=1 Discrete Causal Lattice.

**Series:** Companion artifact to the A=1 Discrete Causal Lattice
series.  Not itself a numbered paper (Paper~I, Paper~II, ...);
intended to be cited from those papers and from external work.

**Anchor:** Phase~3 of Paper~II
([doi:10.5281/zenodo.20240736](https://doi.org/10.5281/zenodo.20240736)).

**Core framing:** the zoo is *infrastructure*, not new theoretical
content.  All algebraic claims are inherited from Paper~II Phase~3
and reproduced verbatim via the scripts under `src/utilities/`.
The zoo adds naming, tagging, and machine-readable emit so that
the 71 generators become navigable rather than just countable.

---

## Audit Table Status (mirrors `paper/sections/audit_table.tex`)

The audit table is split into two blocks.

**Inherited from Paper~II Phase~3 (PASS):**

| Row | Status | What it claims |
|---|---|---|
| Centralizer dimension is 71 | PASS | `automorphism_centralizer_extended.py` Step~1 |
| SM subalgebra has dim 12 inside the centralizer | PASS | Same script, Step~2 |
| Extras count is 59, breakdown 24+3+8+24 | PASS | Same script, Step~3 |
| 71-dim centralizer is $\mathfrak{su}(6)_+ \oplus \mathfrak{su}(6)_- \oplus \mathfrak{u}(1)$ | PASS | `notes/aut_centralizer_enumeration.md` |
| $(\mathbf{8}, \mathbf{3})$ + chirality-shadow SM decomposition | PASS | Same note |
| $[\text{extras}, \text{SM}]$ never lands in SM | PASS | `aut_centralizer_extras_commutators.py`; 256 zero, 0 in_SM, 452 in_extras |
| $[\text{extras}, \text{extras}]$ has SM components | PASS | Same script; 178 in_SM, 1146 in_extras, 48 mixed |

**Zoo-specific (STUB in v0.1, to flip in Phase~2):**

| Row | Status | What it claims |
|---|---|---|
| Stable name per generator | STUB | `generator_zoo.py` not yet written |
| 3-bit tensor-factor action tag per generator | STUB | Same |
| $(SU(3), SU(2))$ irrep tag per generator | STUB | Same |
| Bracket-class lookup for all $\binom{71}{2}$ pairs | STUB | Extension of Paper~II's $59 \times 12$ + $\binom{59}{2}$ |
| JSON catalogue emit | STUB | Same |
| \LaTeX{} longtable renderer | STUB | Same; appendix not yet written |
| Conjectural decoherence-channel labels | STUB | DRAFT per `notes/extras_as_a1_accounting.md` |

The claim auditor agent
(`.claude/agents/claim-auditor.md`) treats `audit_table.tex` as the
authority; this section is for quick orientation only.

---

## Conventions

- **Status legend.** `PASS` / `PART` / `STUB` / `FAIL` (defined in
  the front-matter of `paper/main.tex`).
- **File naming.** Sections: `paper/sections/<topic>.tex`.  Figures:
  `paper/figures/<name>.{tex,pdf,png}` with `.tex` fragment + binary
  pair.  Notes: `notes/<topic>.md`.  Utilities:
  `src/utilities/<topic>.py`.  Experiments (if any):
  `src/experiments/exp_NN_<name>.{py,md}`.
- **Cross-references.** Always `\label{}` + `\ref{}` / `\autoref{}`,
  never hard-coded numbers.  Section labels: `sec:<name>`.  Subsection:
  `subsec:<name>`.  Equation: `eq:<name>`.  Figure: `fig:<name>`.
  Table: `tab:<name>`.  Theorem: `thm:<name>`.
- **Bibliography.** All cites flow through
  `paper/paper-bib/references.bib`.  Style:
  `\bibliographystyle{unsrt}` (numeric, in citation order).
- **LaTeX layout idioms.** `\nolinkurl{}` for paths, `\url{}` for URLs
  inside `\href{}`.  `longtable` for tables that may span pages.
  `\scriptsize` for long verbatim Python.
- **Inherited scripts.**  The two `src/utilities/*centralizer*.py`
  scripts are pinned copies of the Paper~II v1.0 versions and
  should NOT be edited.  Edit `generator_zoo.py` (the zoo's
  extension layer) instead, which `import`s from them.

## Documentation convention for code

Every non-trivial line of framework code should say what it **is**
in the theory, not just what it does in the program.  Name the
mathematical object, cite the paper section/equation, and use "IS"
for exact correspondences, "approximates" for continuum limits.
This convention is inherited from Paper~I and Paper~II.

---

## Release flow

**The authoritative procedure is `release_notes/README.md`.**  A
Claude session asked to "make a release" or "cut vX.Y" should
read that file end-to-end before doing anything; it has 19
numbered steps split across 5 phases, with each step annotated
`[Claude]` (autonomous) or `[User]` (requires a human, typically
because it touches Zenodo or GitHub Releases).

The short version, sufficient to orient before reading the
detailed procedure:

**Phase~1 -- Prepare locally (`[Claude]`).**  Bump the repo
version in four files in lockstep -- `CITATION.cff`,
`src/utilities/generator_zoo.py` (the `VERSION` constant),
`paper/main.tex` (the `\thanks{}` block, DOI placeholder), and
`CLAUDE.md`'s `CURRENT STATUS` header.  Run `python -m
src.utilities.generator_zoo` to regenerate
`data/generator_catalogue.json` and
`paper/sections/generator_zoo_table.tex` with the new
`catalogue_version` field.  Run `python audit_universe.py` to
verify no regressions.  Draft `release_notes/vX.Y.md` and
`release_notes/vX.Y-release-message.md` from the templates.
Build a candidate PDF (`build.cmd paper`), commit as
"Prepare vX.Y release (DOI pending)" -- but **do not tag yet**.

**Phase~2 -- Zenodo deposit (`[User]`).**  Upload the candidate
PDF + source-tree archive to Zenodo as a new version, selecting
the `a1-discrete-causal-lattice` community.  Zenodo mints a new
version DOI.

**Phase~3 -- Lock in the DOI (`[Claude]`).**  Fill in the DOI in
the four files where it landed as a placeholder (`CITATION.cff`,
`paper/main.tex`, both `release_notes/vX.Y*.md`).  Rebuild the
PDF; snapshot to `.stage/dcl-generator-zoo_vX.Y.pdf` (gitignored,
durable per-version archive).  Commit "vX.Y: fill DOI
placeholders post-Zenodo deposit", tag `vX.Y`, push the tag.

**Phase~4 -- Publish (`[Claude]` for GitHub Release, `[User]` for
community curation).**  `gh release create vX.Y --notes-file
release_notes/vX.Y-release-message.md`.  Confirm Zenodo deposit
is listed in the community.

**Phase~5 -- Post-release sanity (`[Claude]`).**  Verify tag is
on `origin`, `gh release view` shows the right body, the DOI
resolves to the new deposit, the community lists it.  Bump
`CLAUDE.md`'s `CURRENT STATUS` to the next planned increment.

Versioning policy summary (full version in
`release_notes/README.md`):
- **Repo version** (`vX.Y`) moves at every release.
- **Zenodo DOI** is fresh per version; the concept DOI stays the
  same and resolves to the latest.
- **JSON `schema_version`** (integer) bumps only when the JSON
  shape changes in a breaking way; adding generators or brackets
  does not bump it.
- Pre-`v1.0` (`v0.Y`): breaking changes allowed.  Post-`v1.0`:
  the `G_NN` naming convention and the JSON schema are frozen;
  breaking changes require a `v2.0`.

For Zenodo curation context (the broader A=1 community
structure, communities Paper~I and Paper~II are in,
`fbt-framework` / `osqgr` cross-listings), see Paper~II's
`notes/arxiv_endorsement_candidates.md`.

---

## What NOT to Change

- **`src/utilities/automorphism_centralizer_extended.py`** and
  **`src/utilities/aut_centralizer_extras_commutators.py`:** copies
  of the Paper~II v1.0-released versions.  The whole zoo is built
  on these being identical to their upstream; edit *only* if
  extending the calculation, and even then prefer a new file
  (`generator_zoo.py`) that imports from them.  Both files carry
  a "Provenance" block in their docstring documenting this.
- **The four Paper~II notes under `notes/`:** copies prefixed with
  a Provenance block.  Edit only to add zoo-specific commentary at
  the bottom; never edit the inherited content.
- **`paper/sections/audit_table.tex`:** once the zoo's v1.0 is
  deposited on Zenodo, the audit table is part of the released
  artifact.  External tooling that consumes it must work read-only
  against it.

---

## Cross-references to Paper~I

The dcl repo is the upstream of record for Paper~I (v1.0 at
[doi:10.5281/zenodo.20078529](https://doi.org/10.5281/zenodo.20078529)).
For local Claude/agent work, expose it as a directory junction:

```text
external/dcl  ->  C:\dev\dcl
```

To (re)create the junction on Windows:

```bat
mkdir external
mklink /J external\dcl C:\dev\dcl
```

The zoo does not strictly depend on the dcl checkout for build /
test (the inherited centralizer scripts and their docstrings are
self-contained), but having dcl available locally lets Claude /
agents cross-reference the framework's origin notes.

---

## Cross-references to Paper~II (dcl-sm-derivation)

The dcl-sm-derivation repo is the upstream of record for Paper~II
(v1.0 at
[doi:10.5281/zenodo.20240736](https://doi.org/10.5281/zenodo.20240736)).
Expose as a junction:

```text
external/dcl-sm-derivation  ->  C:\dev\dcl-sm-derivation
```

The zoo's load-bearing scripts in `src/utilities/` were originally
introduced in Paper~II's `src/utilities/` and are reproduced here
verbatim with a Provenance block.  Having dcl-sm-derivation
available locally lets a reviewer compare the two copies and
confirm they are identical at the v1.0 cut.

---

## Cross-references to physics-research (notation / formalization)

The parallel formalization effort (notation, algebra, topology,
balanced $\mathcal{A}=1$ equations) lives in the physics-research
repo.  Expose as a junction:

```text
external/research  ->  C:\dev\physics-research
```

Highlights for zoo work:

- `external/research/Notes/balanced_equations/` -- symbol-meaning
  catalogues and `Diagrammatic_Map.md`.  The zoo's stable-name
  scheme for the 71 generators should align with the symbol
  catalogue conventions where it overlaps.
- `external/research/Notes/color_and_emergent_forces.md` -- the
  formalization-side view of the $(\mathbf{8}, \mathbf{3})$
  leptoquark-flavoured content.

**Upstream flow rule.** Findings during zoo work that touch
notation, algebra, topology, or balanced $\mathcal{A}=1$ equations
should be captured as notes in this repo's `notes/` directory (per
`notes/README.md`) so they can flow upstream to physics-research's
Notes/.

---

## Notes Index

- `notes/README.md` -- conventions for notes/
- `notes/aut_centralizer_enumeration.md` -- inherited from
  Paper~II Phase~3.  Discrete-Hermitian centralizer of the
  bipartite tick rule on $\mathbb{C}^{12}$ is dim 71, structurally
  $\mathfrak{su}(6)_+ \oplus \mathfrak{su}(6)_- \oplus \mathfrak{u}(1)$.
  SM 12 + extras 59 breakdown; $(\mathbf{8}, \mathbf{3})$ + shadow
  SM irrep decomposition.
- `notes/aut_centralizer_extras_commutators.md` -- inherited from
  Paper~II.  Bracket structure: 708 $[\text{extras}, \text{SM}]$
  brackets (256 zero, 0 in_SM, 452 in_extras: extras is an
  SM-invariant module) and 1711 $[\text{extras}, \text{extras}]$
  brackets (extras is NOT a Lie ideal).  Algebraic signature of a
  broken-symmetry pattern.
- `notes/extras_as_a1_accounting.md` (DRAFT) -- inherited from
  Paper~II.  Structural hypothesis: the 59 extras are the
  bookkeeping channels through which probability flows during
  decoherence; decoherence as algebraic projection from the
  71-dim centralizer onto the SM-gauge-invariant 12-dim
  subalgebra.  Reproduced as conjectural infrastructure; the
  zoo's catalogue tags physical-role labels clearly as DRAFT
  per `feedback_let_formalism_mature` in cross-conversation
  memory.
- `notes/su3_generation_from_colour_memory.md` -- inherited from
  Paper~II Phase~2.  Real-symmetric colour-memory tick rule
  closes to full $\mathfrak{su}(3)$ under Lie brackets; structural
  upstream of the zoo's $(\mathbf{8}, \mathbf{1}) / (\mathbf{8},
  \mathbf{3})$ irrep tagging.

(List additional notes here as they accumulate.  Zoo-specific
notes -- naming-scheme rationale, irrep-tagging algorithm, JSON
schema -- are expected to land here as Phase~2 develops.)
