# dcl-generator-zoo

A catalogue of the 71-dimensional per-site automorphism algebra of
the A=1 Discrete Causal Lattice.

Phase~3 of Paper~II of the A=1 Discrete Causal Lattice series
([doi:10.5281/zenodo.20240736](https://doi.org/10.5281/zenodo.20240736))
established that the discrete-Hermitian centralizer of the
bipartite tick rule on the per-site $\mathbb{C}^{12} =
\mathbb{C}^2_\text{chir} \otimes \mathbb{C}^2_\text{iso} \otimes
\mathbb{C}^3_\text{col}$ amplitude has dimension 71, structurally
$\mathfrak{su}(6)_+ \oplus \mathfrak{su}(6)_- \oplus \mathfrak{u}(1)$.
The 12-dimensional Standard Model gauge subalgebra sits inside
this centralizer as a non-normal subgroup, and the 59-generator
complement (the "extras") transforms under $SU(3) \times SU(2)$ as
$(\mathbf{8}, \mathbf{3})$ leptoquark-flavoured plus chirality-
$\sigma_x$-twisted SM-flavoured.

This zoo turns those 71 generators into a navigable catalogue:
each generator gets a stable name, an $(SU(3), SU(2))$ irrep tag,
a tensor-factor action tag, and a bracket-class classification
against every other generator.  The catalogue is emitted as
machine-readable JSON for downstream consumption and as a
printable \LaTeX{} longtable for human reference.

The intent is that follow-on papers in the A=1 series, and
external researchers building on the framework, can refer to
specific generators by name rather than re-deriving them.

## Status: v0.1-DRAFT (2026-05-16)

What is in place:

- The two load-bearing centralizer enumeration scripts are
  reproduced verbatim from Paper~II in `src/utilities/`.
- Four supporting notes from Paper~II are reproduced with
  Provenance prefixes in `notes/`.
- The zoo's catalogue extension layer
  (`src/utilities/generator_zoo.py`) is written and ready to run.
  It builds the 71-generator catalogue with stable names + irrep
  tags + factor-action tags, classifies all 2485 brackets, and
  emits `data/generator_catalogue.json` plus
  `paper/sections/generator_zoo_table.tex`.
- A paper skeleton (title page, abstract, introduction, audit
  table, generator-zoo appendix, references) is in place.  The
  conclusion and acknowledgements sections retain template
  placeholders pending v1.0.

What is pending (next session): user runs the catalogue script
end-to-end, commits the emitted JSON + LaTeX, flips the relevant
audit-table rows from `PART` to `PASS`, and deposits v1.0 on
Zenodo for a citeable DOI.  See `CLAUDE.md` for the full status
block.

## Upstream

This zoo builds on:

- **Paper~I, *Geometry First*** -- the bipartite octahedral
  lattice, the $\mathcal{A}=1$ conservation axiom, the per-site
  $\mathbb{C}^{12}$ extension.
  [doi:10.5281/zenodo.20078529](https://doi.org/10.5281/zenodo.20078529).
- **Paper~II, *Geometry Forces Physics*** -- the centralizer
  enumeration and bracket-classification that the zoo catalogues.
  [doi:10.5281/zenodo.20240736](https://doi.org/10.5281/zenodo.20240736).

Both deposits are in the
[`a1-discrete-causal-lattice`](https://zenodo.org/communities/a1-discrete-causal-lattice/)
Zenodo community, to which the zoo's v1.0 will also be added.

## What you get

```text
.
├── paper/                       (LaTeX paper: catalogue + introduction)
│   ├── main.tex
│   ├── macros/
│   ├── sections/                introduction.tex, audit_table.tex,
│   │                            abstract.tex, ... (catalogue appendix
│   │                            generator_zoo.tex pending Phase 2)
│   ├── figures/
│   └── paper-bib/references.bib
├── src/
│   ├── utilities/               automorphism_centralizer_extended.py,
│   │                            aut_centralizer_extras_commutators.py
│   │                            (inherited verbatim from Paper II),
│   │                            generator_zoo.py (catalogue extension)
│   ├── core/                    framework primitives (README only for now)
│   └── experiments/             (none yet; placeholder)
├── tests/                       pytest scaffolding
├── data/                        catalogue output (JSON) lands here
├── notes/                       four inherited Paper II notes, prefixed
│                                with Provenance blocks
├── release_notes/               per-version change log
├── .claude/agents/claim-auditor.md  read-only audit agent
├── audit_universe.py            master PASS/STUB/FAIL roll-up
├── audit_universe.md            audit-model documentation
├── virtual-env-requirements.txt sympy + numpy + matplotlib + pytest
├── CLAUDE.md                    project memory for Claude Code
├── CITATION.cff                 machine-readable citation
├── LICENSE                      MIT (code) / CC BY 4.0 (paper text)
├── makefile common.mak          root build (paper + tests + experiments)
├── build.{sh,cmd}               platform wrappers around make
└── setup.{sh,cmd}               create venv + install requirements
```

## Quickstart

```sh
# 1. Create the venv and install dependencies (sympy + numpy + ...)
./setup.sh                       # POSIX / MSYS2 UCRT64 on Windows
setup.cmd                        # Windows cmd / PowerShell

# 2. Sanity-check the toolchain
./build.sh tests                 # pytest against tests/
./build.sh paper                 # pdflatex 3-pass + bibtex

# 3. Reproduce the inherited Paper II Phase 3 results
python -m src.utilities.automorphism_centralizer_extended
python -m src.utilities.aut_centralizer_extras_commutators

# 4. Build the zoo catalogue (writes data/generator_catalogue.json
#    and paper/sections/generator_zoo_table.tex; ~5-15 min runtime)
python -m src.utilities.generator_zoo

# 5. Master audit roll-up
python audit_universe.py
```

## License

Paper text and figures: CC BY 4.0.
Source (the catalogue scripts and infrastructure): MIT
(see `LICENSE`).

## Citing this catalogue

See `CITATION.cff`.  Until the v1.0 Zenodo DOI is assigned, cite
as:

> Menendez, J. (2026).  *dcl-generator-zoo: A Catalogue of the
> 71-Dimensional Per-Site Automorphism Algebra of the A=1 Discrete
> Causal Lattice*, v0.1-DRAFT.  GitHub:
> `JackDMenendez/dcl-generator-zoo`.

Once v1.0 is deposited on Zenodo, the DOI will be added to
`CITATION.cff` and to `paper/main.tex`'s title-page `\thanks{}`
block.
