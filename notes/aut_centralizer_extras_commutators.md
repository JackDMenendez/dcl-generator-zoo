> **Provenance.**  This note is reproduced verbatim from Paper~II of
> the A=1 Discrete Causal Lattice series
> ([doi:10.5281/zenodo.20240736](https://doi.org/10.5281/zenodo.20240736)),
> as the textual companion to the like-named script under
> `src/utilities/`.  Cross-references to `paper/sections/audit_table.tex`
> below refer to **Paper~II's** audit table; this zoo has its own
> separate audit table.  Cross-references to other notes under
> `notes/` point at Paper~II's `notes/` directory, which is not
> fully reproduced in this zoo.

# Phase 3 extension: bracket structure between the 59 extras and 12 SM

**Status:** STABLE (verified by
`src/utilities/aut_centralizer_extras_commutators.py`, 2026-05-15).
**Purpose:** Make the algebraic shape of the symmetry-breaking
structure of Phase 3 explicit.  The 71-dim discrete-Hermitian
centralizer of the bipartite tick rule is structurally
$\mathfrak{su}(6)_+ \oplus \mathfrak{su}(6)_- \oplus \mathfrak{u}(1)$;
this note computes the brackets $[E, T]$ (and $[E_i, E_j]$) and
verifies that the 12-dim SM subalgebra acts on the 59-dim extras
as an invariant representation -- exactly the algebraic signature
of a broken-symmetry structure where SM is unbroken and extras
are "would-be massive" coset generators.
**Cited by:** the audit-table row "Exact equality vs containment
in $\mathrm{Aut}_\text{ext}$" in
`paper/sections/audit_table.tex` (already PART; this note sharpens
the structural reading).  Will be folded into Paper II's
conclusion together with the GUT-style symmetry-breaking
interpretation when Phase 5 lands.

---

## Background and motivation

Phase 3 established that the discrete-Hermitian centralizer of
$\sigma_x \otimes I_2 \otimes I_3$ in $\mathfrak{su}(12)$ has
dimension 71, and that this algebra has the explicit structure

$$\mathfrak{Aut}_{\text{centralizer}} \;=\; \mathfrak{su}(6)_+ \oplus \mathfrak{su}(6)_- \oplus \mathfrak{u}(1),$$

with the two $\mathfrak{su}(6)$ factors acting on the $\pm 1$
chirality eigenspaces and the $\mathfrak{u}(1)$ central (= $J_1$).
The SM gauge subalgebra $\mathfrak{su}(3) \oplus \mathfrak{su}(2)
\oplus \langle J_1 \rangle$ (dim 12 in $\mathfrak{su}(12)$) embeds
in the centralizer via the diagonal embedding of
$\mathfrak{su}(3) \times \mathfrak{su}(2)$ in each $\mathfrak{su}(6)$
factor (using $\mathbf{6} = (\mathbf{3}, \mathbf{2})$).  The
"extras" (59 generators) are the centralizer minus the SM.

The structural question this note settles: how does the SM
subalgebra act on the extras via the adjoint (commutator) action?

Three possibilities:

1. *SM is normal in the centralizer:* $[E, T] \in \mathrm{SM}$ for
   $E \in \mathrm{extras}, T \in \mathrm{SM}$.  Equivalently:
   extras would be an "irrelevant ideal."
2. *Extras invariant under SM (SM-module structure):* $[E, T] \in
   \mathrm{extras}$ for all such pairs.  Extras form an SM-module
   but possibly not a Lie ideal.
3. *Mixed:* $[E, T]$ has both SM and extras components, so neither
   subspace is invariant.

The script `aut_centralizer_extras_commutators.py` computes all
$59 \times 12 = 708$ brackets $[E, T]$ explicitly, classifies each
as zero / in_SM / in_extras / mixed, and reports counts.  It also
computes $\binom{59}{2} = 1711$ brackets $[E_i, E_j]$ within the
extras to check whether extras are themselves a Lie ideal
(closed under bracket) or only a module.

## Bracket-classification results

Script output:

| Bracket type | Zero | in SM | in extras | mixed | Total |
|---|---|---|---|---|---|
| $[E, T]$ (extras × SM) | 256 | 0 | 452 | 0 | 708 |
| $[E_i, E_j]$ (extras × extras, $i<j$) | 339 | 178 | 1146 | 48 | 1711 |

### Reading 1: $[SM, \text{extras}] \subseteq \text{extras}$ (the module structure)

Of the 708 SM × extras brackets:
- **256 vanish:** mostly because $J_1$ (the central $\mathfrak{u}(1)$
  of the centralizer) commutes with everything ($J_1$ contributes
  exactly $59$ trivial brackets); the rest are accidental zeros from
  factor-disjointness (e.g., $[I \otimes \sigma_a \otimes I_3,
  I \otimes I_2 \otimes \lambda_b] = 0$).
- **0 land in SM, 452 in extras:** every non-vanishing bracket
  $[E, T]$ stays inside the 59-dim extras subspace.

This proves: the 59 extras form an **invariant module** under the
SM adjoint action.  The SM subalgebra is a **structural subgroup**
of the 71-dim centralizer; extras transform as SM-irreducible
representations under SM's adjoint, but they never mix with SM
in the bracket.

### Reading 2: $[\text{extras}, \text{extras}]$ has SM components -- extras is NOT a Lie ideal

Of the 1711 extras × extras brackets:
- **339 vanish.**
- **178 land entirely in SM** (the 12-dim SM subspace).
- **1146 land entirely in extras** (the 59-dim extras subspace).
- **48 are mixed** (have both SM and extras components).

So $226 = 178 + 48$ brackets $[E_i, E_j]$ produce SM-component
output.  The extras subspace is therefore **not a Lie ideal** of
the centralizer.

This rules out the simplest semidirect-sum structure (where extras
would be an ideal).  The 71-dim centralizer's algebraic shape is
the standard structure of a simple Lie algebra (here
$\mathfrak{su}(6) \oplus \mathfrak{su}(6) \oplus \mathfrak{u}(1)$)
containing a non-normal subalgebra (the SM 12) with a complement
(the 59 extras) that is an SM-module under the adjoint but not
itself an ideal.

Equivalently, in representation-theoretic terms: the bracket of
two $(\mathbf{8}, \mathbf{3})$ generators decomposes under
$SU(3) \times SU(2)$ into $(\mathbf{8}, \mathbf{1}) \oplus
(\mathbf{1}, \mathbf{3}) \oplus (\mathbf{8}, \mathbf{3})$ -- the
first two are SM, the third is back into extras.  This is exactly
the standard branching rule of $\mathfrak{su}(6)$ adjoint under
the SM subgroup; the 178 + 48 "SM-producing" brackets are the
$SU(3) \times SU(2)$ adjoint pieces of the closure.

## SU(3) × SU(2) representation content of the extras

Under the SM gauge group's adjoint action, the 59 extras
decompose into SM-irreducible representations:

- **24 in $(\mathbf{8}, \mathbf{3})$ (internal block):**
  $I_2 \otimes \sigma_a \otimes \lambda_b$ -- leptoquark-flavoured
  generators (colour-octet, weak-triplet).  These transform like
  the leptoquark gauge bosons of standard GUTs.
- **24 in $(\mathbf{8}, \mathbf{3})$ ($\sigma_x$ block):**
  $\sigma_x \otimes \sigma_a \otimes \lambda_b$ -- the chirality-
  twisted partner of the above.
- **8 in $(\mathbf{8}, \mathbf{1})$ ($\sigma_x$ block):**
  $\sigma_x \otimes I_2 \otimes \lambda_a$ -- chirality-twisted
  SU(3)-colour generators.
- **3 in $(\mathbf{1}, \mathbf{3})$ ($\sigma_x$ block):**
  $\sigma_x \otimes \sigma_a \otimes I_3$ -- chirality-twisted
  SU(2)-weak generators.

Total: $24 + 24 + 8 + 3 = 59$ ✓.

Two-thirds of the extras (48 of 59) are leptoquark-flavoured;
the remaining 11 are "$\sigma_x$-shadow SM" -- they transform
like the SM gauge generators but live in the $\sigma_x$ chirality
block rather than the identity chirality block, so they are not
part of the SM gauge sector.

## Physical interpretation: a broken-symmetry shape

The shape *SM subalgebra + module of extras* is the **algebraic
signature of a broken gauge symmetry** with structure group $G$
and unbroken subgroup $H \subset G$.  Standard examples:

- $SU(5) \to SU(3) \times SU(2) \times U(1)$ with 12
  unbroken generators and $24 - 12 = 12$ broken (X/Y leptoquark)
  generators.
- $SO(10) \to SU(5)$, with 25 broken generators (or $SO(10) \to
  SU(3) \times SU(2) \times U(1)$ with $45 - 12 = 33$ broken).
- Pati-Salam $SU(4)_C \times SU(2)_L \times SU(2)_R$ ($\dim 21$)
  $\to$ SM, with 9 broken.

The framework's $\mathfrak{su}(6) \oplus \mathfrak{su}(6) \oplus
\mathfrak{u}(1) \to \mathrm{SM}$ has 59 broken generators -- larger
than these standard GUTs, but structurally the same kind of
pattern.  The 48 leptoquark-flavoured extras are *exactly* the
type of generator that would be a massive X/Y-like gauge boson
in a GUT-style breaking; the 11 $\sigma_x$-shadow SM generators
would be additional massive gauge bosons mediating chirality-
violating interactions.

## What the framework does and does not say

The framework's natural prediction is the **larger 71-dim algebra
at the discrete lattice scale**.  Whether the SM emerges as the
*effective* low-energy theory after some symmetry-breaking
mechanism (Higgs-like, or geometric / decoherence-driven on the
lattice) is the open structural question.

The framework's contribution:

1. *Identifies the larger symmetry algebraically:* not just "more
   than SM" but specifically $\mathfrak{su}(6) \oplus
   \mathfrak{su}(6) \oplus \mathfrak{u}(1)$ with explicit
   decomposition.
2. *Shows the SM subalgebra is a structural subgroup with
   well-defined coset module:* the 59 extras transform as
   SM-irreducible representations, not as random factor-mixings.
3. *Locates the breaking mechanism as the open follow-up:* what
   gives the 59 extras large masses (or otherwise decouples them)
   at observable energies is not addressed; the framework asks
   the question precisely without answering it.

## Two narrative framings for Paper II's conclusion

Both come from the same algebraic structure.  These match the
narrative options identified earlier in
`notes/mass_chirality_coupling.md` and `notes/debt_to_measurement.md`:

**The high-energy unification framing:** the 71-dim algebra is
the fundamental gauge symmetry at the lattice scale $1/a$ (which
might be the Planck scale, or some other UV scale set by lattice
physics).  The 59 extras correspond to heavy gauge bosons that
mediate factor-mixing interactions.  At lower energies, these
heavy bosons decouple, leaving only the 12-dim SM gauge sector
as the effective field theory.  This is structurally identical
to standard GUT symmetry breaking.

**The decoherence framing:** the 59 extras correspond to
operations that, in a discrete causal walk, induce rapid phase
decoherence between different tensor factors.  Only the
factor-product-preserving operations (the SM 12) maintain
coherence over macroscopic distances; the 59 mixings dephase
inside a single tick.  In this reading, the SM emerges as the
"coherence-preserving" sub-symmetry rather than as the
mass-suppressed unbroken subgroup.

The high-energy unification framing is more conventional and
maps onto known physics (mass-suppressed GUT gauge bosons).  The
decoherence framing is more specific to the framework's
discrete-walk structure and offers a potentially distinct
prediction (interaction strengths set by lattice walk geometry
rather than by VEV-dependent masses).  Both will be acknowledged
in Paper II's conclusion.

## Upstream-flow tags

- **Algebra:** the 71-dim centralizer is
  $\mathfrak{su}(6) \oplus \mathfrak{su}(6) \oplus \mathfrak{u}(1)$
  with SM as a "diagonal subgroup" containing 11 of 35 generators
  from each $\mathfrak{su}(6)$ factor (plus 1 from the U(1)).
  The 59 extras transform under SM as
  $(\mathbf{8}, \mathbf{3})_\text{internal} \oplus
  (\mathbf{8}, \mathbf{3})_{\sigma_x} \oplus
  (\mathbf{8}, \mathbf{1})_{\sigma_x} \oplus
  (\mathbf{1}, \mathbf{3})_{\sigma_x}$.
- **Topology / structure of the bipartition:** the chirality
  $\sigma_x$ bipartition is the L/R exchange that swaps the two
  $\mathfrak{su}(6)$ factors.  This is the discrete analogue of
  the left-right exchange in Pati-Salam, where the framework's
  bipartite parity plays the same role as Pati-Salam's
  $\mathbb{Z}_2$ exchange of $SU(2)_L$ and $SU(2)_R$.
- **Balanced equations:** a reaction-style $\mathcal{A}=1$
  equation involving the 59 extras would be SM-gauge-non-invariant
  in its raw form, but invariant under the larger
  $\mathfrak{su}(6) \oplus \mathfrak{su}(6) \oplus \mathfrak{u}(1)$.
  Decoherence or mass suppression of the extras turns this into
  the SM's gauge-invariant reaction algebra at observable energies.

## Pointers

- Script: `src/utilities/aut_centralizer_extras_commutators.py`
  (sympy; 708 $[E, T]$ brackets + 1711 $[E_i, E_j]$ brackets;
  rank-based linear-algebra classification over the complex field).
- Audit table: `paper/sections/audit_table.tex`, row "Exact equality
  vs containment in $\mathrm{Aut}_\text{ext}$" (PART; sharpened by
  this note with the SU(6)$\oplus$SU(6)$\oplus$U(1) identification).
- Work plan: `notes/work_plan.md`, Phase 3 closure (sharpened).
- Adjacent: `notes/aut_centralizer_enumeration.md` (the parent
  finding -- 71-dim centralizer + SM = 12 + extras = 59);
  `notes/mass_chirality_coupling.md` (the related observation that
  SM gauge structure is forced by clock-density preservation in
  the discrete tick rule);
  `notes/debt_to_measurement.md` (the methodological framing for
  Paper II's conclusion).
