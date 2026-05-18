# release_notes/

The dcl-generator-zoo is a **living document**: it accumulates
catalogue revisions as the per-site automorphism algebra is studied
in more depth (new naming conventions, new tags, new bracket
classifications, new structural notes, eventual generalisations
beyond $\mathbb{C}^{12}$).  Each release is a frozen snapshot of
the catalogue at a particular point in time, with its own Zenodo
DOI, so that downstream papers and external work can cite a
*specific* version that will not change under them.

This document is the **authoritative release procedure** for the
zoo.  A fresh Claude Code session (or any contributor) should be
able to execute a release end-to-end by following the steps below.

---

## Two files per release

For each released `vX.Y`, two files land in this directory:

- **`vX.Y.md`** -- the **change log**.  Long-form, internal: what
  changed, why, what's deferred, audit-row deltas, reproducibility
  instructions.  Use `TEMPLATE.md` as the starting point.
- **`vX.Y-release-message.md`** -- the **GitHub Release body**.
  Outward-facing: headline change, audit-status delta, what's
  out of scope.  Posted as the body of the GitHub Release
  alongside the `vX.Y` tag.  Use `TEMPLATE-release-message.md`.

---

## Versioning policy

Two version numbers move in lockstep at every release:

- **Repo version** -- `vX.Y` (the git tag, the `version:` field in
  `CITATION.cff`, the `\thanks{}` block on the paper's title page,
  the `VERSION` constant in `src/utilities/generator_zoo.py`, and
  the `catalogue_version` field in
  `data/generator_catalogue.json`).
- **Zenodo DOI** -- a fresh DOI is minted for every new version on
  Zenodo; the *concept DOI* (the version-less DOI Zenodo creates
  alongside the first deposit) stays the same across versions and
  always resolves to the latest.  Downstream papers should cite
  the *version DOI* of the snapshot they relied on, not the
  concept DOI.

One version field moves separately:

- **JSON `schema_version`** -- an integer (`1`, `2`, ...) inside
  `data/generator_catalogue.json`.  Bump *only* when the JSON
  shape changes in a way that breaks existing programmatic
  consumers.  Adding new generators, new bracket entries, or new
  notes does not bump the schema; renaming a field, removing a
  field, or changing a field's type does.

### When to release

The zoo is living, but not every commit deserves a release.  A
release is appropriate when *any* of the following has changed
since the last tag:

- An audit-table row's status flips (`STUB` $\to$ `PART`, `PART`
  $\to$ `PASS`, or anything $\to$ `FAIL`).
- The catalogue's algebraic content changes (new generators,
  re-numbering, new tags, new bracket classifications).
- A note moves from `DRAFT` to `STABLE`.
- A structural revision to the paper's appendix prose.
- A breaking change to the JSON schema (also bump `schema_version`).
- An external paper has cited the zoo and would benefit from a
  fresh frozen snapshot.

A release is NOT appropriate for:

- Pure typo fixes in prose (commit on `main`, no tag).
- Layout polish that doesn't change content.
- Dependency-version bumps that don't change catalogue output.
- Adding placeholder sections to be filled in later.

### Version-number conventions

- `v0.Y` -- the catalogue is still evolving; pre-stable.  Each
  bump is allowed to make breaking changes (rename fields, change
  ordering convention, ...).
- `v1.0` -- the first stable release, intended as the canonical
  long-lived reference.  After `v1.0`, the naming convention
  (`G_NN` ordering) and the JSON schema are considered frozen
  for downstream consumption; breaking changes require a `v2.0`.
- `vX.Y.Z` (patch) -- not used.  Patches in this project should
  produce a new minor version.

---

## Release procedure (step-by-step)

Each step's owner is annotated: **\[Claude\]** can be executed
autonomously by a Claude session; **\[User\]** requires a human
(typically because it touches an external service like Zenodo or
GitHub releases).  Before any **\[Action\]** that modifies shared
state (commits, tags, deposits, Releases), Claude should confirm
with the user.

### Phase 1 -- Prepare the release locally

1. **\[Claude\]** Confirm the release type with the user.  Pick
   the next version number (`vX.Y`).  Verify:
   - Working tree clean on `main`.
   - No uncommitted catalogue changes.
   - CI / `python audit_universe.py` green at the current HEAD.

2. **\[Claude\]** Bump the version in **four files** in lockstep:
   - `CITATION.cff` -- update `version: vX.Y` and
     `date-released: YYYY-MM-DD` (use today).
   - `src/utilities/generator_zoo.py` -- update the
     `VERSION = "vX.Y"` module-level constant.
   - `paper/main.tex` -- update the `Version X.Y` line inside the
     title-page `\thanks{}` block.  Leave the DOI line as
     `TBD` / placeholder for now.
   - `CLAUDE.md` -- update the `CURRENT STATUS (YYYY-MM-DD) -- vX.Y`
     header line.

3. **\[Claude\]** Regenerate the catalogue so the JSON and the
   auto-generated LaTeX longtable carry the new version:
   ```text
   python -m src.utilities.generator_zoo
   ```
   This rewrites `data/generator_catalogue.json` (with
   `"catalogue_version": "vX.Y"`) and
   `paper/sections/generator_zoo_table.tex`.  Verify:
   - 71 generators reported, 2485 brackets classified.
   - The bracket-count totals match the prior release (`zero`,
     `in_SM`, `in_extras`, `mixed` should be stable unless a
     structural change is the explicit point of this release).

4. **\[Claude\]** Run the master audit roll-up to confirm no
   regressions:
   ```text
   python audit_universe.py
   ```
   Any `FAIL` or unexpected `STUB` flip is a release-blocker --
   investigate before continuing.

5. **\[Claude\]** Draft the change log
   `release_notes/vX.Y.md` from `TEMPLATE.md`.  Fill in:
   - `Why vX.Y` (the purpose, one paragraph).
   - `Summary of changes since vX.Y-1` (audit-row flips, new
     notes, schema changes if any).
   - `What is not in vX.Y` (explicit out-of-scope, with pointers
     to where it might land).
   - Bibliography additions (if any).
   - Reproducibility paragraph (which scripts to run from a
     fresh clone of the tag).

6. **\[Claude\]** Draft the GitHub Release body
   `release_notes/vX.Y-release-message.md` from
   `TEMPLATE-release-message.md`.  Headline, audit-status delta,
   reproducibility -- shorter and more outward-facing than the
   change log.

7. **\[Claude\]** Build the candidate PDF:
   ```text
   build.cmd paper      REM Windows
   ./build.sh paper     # POSIX / MSYS2
   ```
   This writes `build/<DOC_TITLE>.pdf`.  Open it and verify:
   - Title page shows the right version.
   - `\thanks{}` shows DOI placeholder (the real DOI lands in
     Phase 3).
   - Generator-zoo appendix renders (the `\IfFileExists` branch
     should *not* fire; the auto-generated table should be there).
   - Audit table renders without missing rows.

8. **\[Claude\]** Commit the candidate state (DOI still pending).
   Use a HEREDOC commit message; include the regenerated catalogue
   files and the release-notes drafts.  Suggested message:
   ```text
   Prepare vX.Y release (DOI pending)

   - Bump VERSION / CITATION.cff / main.tex \thanks{} to vX.Y.
   - Regenerate data/generator_catalogue.json and
     paper/sections/generator_zoo_table.tex with vX.Y metadata.
   - Draft release_notes/vX.Y.md and vX.Y-release-message.md
     with DOI placeholders.
   ```
   **Do not tag yet.**  Tagging happens in Phase 3 after the DOI
   is in hand.

### Phase 2 -- Deposit on Zenodo (User-led, external)

9. **\[User\]** Upload the candidate PDF (`build/<DOC_TITLE>.pdf`)
   and a source-tree archive (the `vX.Y` candidate commit's
   tarball, downloadable from GitHub after pushing the candidate
   commit) to Zenodo as a *new version* of the existing zoo
   deposit (or, for the first release, as a new deposit).

   Use the `a1-discrete-causal-lattice` community when filling
   the deposit form (the deposit appears in the community's
   record list and inherits the community curation).

   Zenodo mints a new version DOI.  Note it down -- it has the
   form `10.5281/zenodo.NNNNNNNN`.

   Claude can help prepare the upload metadata (title, author,
   description, keywords, related identifiers pointing at Paper~I
   and Paper~II) but cannot perform the upload itself.

### Phase 3 -- Lock in the DOI and tag the release

10. **\[Claude\]** Fill in the DOI in **four files** (the same
    four as step 2, except now the DOI is the moving part):
    - `CITATION.cff` -- add `doi: 10.5281/zenodo.NNNNNNNN`.
    - `paper/main.tex` -- replace the placeholder DOI in the
      `\thanks{}` block with the real DOI; uncomment the
      commented-out URL line if applicable.
    - `release_notes/vX.Y.md` -- fill in the DOI in the header
      block.
    - `release_notes/vX.Y-release-message.md` -- fill in the DOI
      at the bottom.

    The catalogue JSON does NOT carry the DOI (the DOI is a
    deposit identifier, not a catalogue field), so the JSON does
    not need to be regenerated.

11. **\[Claude\]** Rebuild the PDF with the DOI in place:
    ```text
    build.cmd paper
    ```
    Open and confirm the title page now shows the real DOI.

12. **\[Claude\]** Snapshot the DOI'd PDF to `.stage/`:
    ```text
    mkdir .stage 2>NUL
    copy build\<DOC_TITLE>.pdf .stage\dcl-generator-zoo_vX.Y.pdf
    ```
    `.stage/` is gitignored; it is the durable per-version
    archive that survives `make clean`.

13. **\[Claude\]** Commit the DOI fill-in.  Suggested message:
    ```text
    vX.Y: fill DOI placeholders post-Zenodo deposit

    - DOI 10.5281/zenodo.NNNNNNNN added to CITATION.cff,
      paper/main.tex \thanks{}, release_notes/vX.Y*.md.
    - Rebuilt PDF with the DOI in place; snapshotted to
      .stage/dcl-generator-zoo_vX.Y.pdf (gitignored, durable
      per-version archive).
    ```

14. **\[Claude\]** Tag the release:
    ```text
    git tag vX.Y
    git push origin vX.Y
    ```
    Confirm with the user before pushing the tag (tags are
    public and immutable once pushed).

### Phase 4 -- Publish on GitHub and curate

15. **\[Claude\]** Create the GitHub Release using the `gh` CLI:
    ```text
    gh release create vX.Y \
        --title "vX.Y -- <one-line headline>" \
        --notes-file release_notes/vX.Y-release-message.md
    ```
    Confirm with the user before creating (Releases are public
    and notify watchers).

16. **\[User\]** Confirm the new Zenodo deposit is in the
    `a1-discrete-causal-lattice` Zenodo community
    ([communities/a1-discrete-causal-lattice](https://zenodo.org/communities/a1-discrete-causal-lattice/)).
    If Zenodo did not auto-add it (because the community was
    not selected during upload), add it via the deposit's
    "Communities" tab.

17. **\[Claude\]** Update `CLAUDE.md`'s `CURRENT STATUS` block to
    reflect the released state and the next planned increment.
    Commit:
    ```text
    Post-vX.Y: bump CLAUDE.md status to next planned increment
    ```

### Phase 5 -- Post-release sanity

18. **\[Claude\]** Verify the release is discoverable:
    - `git tag` shows `vX.Y` locally and on `origin`.
    - `gh release view vX.Y` shows the Release with the right body.
    - The Zenodo DOI resolves to the new deposit.
    - The deposit is listed in the `a1-discrete-causal-lattice`
      community.

19. **\[Claude\]** If any audit-table rows that this release
    addressed are now stable enough to flip from `PART` to `PASS`
    (or to add new `PASS` rows for new content), do so in a
    follow-up commit on `main`.  Do NOT amend the tagged commit.

---

## What to do when a step fails

- **Catalogue regeneration fails (step 3).**  The script raises
  an `AssertionError` if the centralizer dimension is not 71 or
  the per-group counts do not match.  This is a release-blocker:
  the inherited Paper II scripts have changed unexpectedly, or
  the import path is broken.  Investigate before continuing.
- **PDF build fails (step 7 or 11).**  Common causes:
  `paper/sections/generator_zoo_table.tex` does not exist
  (rerun step 3), or a hand-edited section has a syntax error.
  The `\IfFileExists` placeholder branch ensures the build can
  succeed even without the auto-generated table; if it fires,
  step 3 was skipped.
- **Zenodo deposit fails (step 9).**  User must resolve with
  Zenodo support.  Claude cannot help.
- **`gh release create` fails (step 15).**  Common cause: tag
  not yet pushed.  Confirm step 14 succeeded.

---

## Pointers

- `TEMPLATE.md` -- change-log scaffold
- `TEMPLATE-release-message.md` -- GitHub Release body scaffold
- `CLAUDE.md` (repo root) -- the Release Flow section
  cross-references this README as authoritative
- Paper~I and Paper~II followed an essentially identical flow;
  their respective `release_notes/` directories are the worked
  precedents
