> **Provenance.**  This note is reproduced verbatim from Paper~II of
> the A=1 Discrete Causal Lattice series
> ([doi:10.5281/zenodo.20240736](https://doi.org/10.5281/zenodo.20240736)).
> Cross-references to `paper/sections/audit_table.tex` below refer to
> **Paper~II's** audit table; this zoo has its own separate audit
> table.  Cross-references to other notes under `notes/` point at
> Paper~II's `notes/` directory.  Per the zoo's own audit row
> "Conjectural decoherence-channel labels" (STUB), the
> decoherence-as-projection hypothesis described here is reproduced
> as conjectural infrastructure; the zoo's catalogue records only
> the algebraic facts and tags physical-role readings clearly as
> DRAFT.

# The 59 extras as the A=1 accountant's ledger:
# decoherence as algebraic projection

**Status:** DRAFT (a structural hypothesis that upgrades the
decoherence framing of `notes/aut_centralizer_extras_commutators.md`
into a specific physical mechanism; not yet verified by a
calculation, but the calculation is sketched below).
**Purpose:** Articulate the hypothesis that the 59 extras of the
71-dim centralizer are the structural-level bookkeeping channels
through which probability flows during what an SM observer
identifies as "decoherence."  In this reading, $\mathcal{A}=1$ is
not violated during interference / measurement; the coherence
that appears lost has been algebraically projected out of the
SM-gauge-invariant sector into the extras subspace, where the
framework still tracks it.
**Cited by:** will land in Paper~II's eventual conclusion or in
a separate follow-up paper that develops the decoherence-as-
projection mechanism into a quantitative prediction.

---

## Three observations that converge

1. **Experiments throw away coherence.**  In a double-slit
   experiment with which-slit measurement, the interference
   pattern disappears.  Standard QM accounts for this via
   environment-induced decoherence: globally unitary evolution,
   with coherence transferred to environment modes that an
   observer traces out.  Locally, the visible system looks like
   a mixed state.

2. **$\mathcal{A}=1$ accounting has been informal.**  The
   framework asserts $\sum_\mathbf{x}(|\psi_R|^2 + |\psi_L|^2) = 1$
   on the lattice, but the prose has rarely tracked where
   probability flows during a specific decoherence-like event.
   Phase 3's discovery of a 71-dim centralizer (with the SM 12 +
   59 extras decomposition) suddenly makes this tractable:
   probability can flow between SM-visible and extras-hidden
   sectors while preserving $\mathcal{A}=1$ exactly.

3. **Minimum change in probability.**  If the lattice tick rule
   is reformulated so that each tick transfers a discrete
   quantum of probability (instead of a continuous
   $\sin^2(\delta\phi/2)$ / $\cos^2(\delta\phi/2)$ split), then
   $\mathcal{A}=1$ becomes an *integer-valued* bookkeeping
   property -- not a soft conservation but a hard quantum
   identity.  The framework would predict discrete decoherence
   events, each a specific number of tick-quanta transferred
   between sectors.

The hypothesis: the 59 extras are the *accounting categories*
that make this bookkeeping precise.  Decoherence is not
unitarity violation; it is **algebraic projection** from the
full 71-dim centralizer onto the SM 12-dim gauge-invariant
sub-algebra, with the "lost coherence" residing in the 59
extras directions that an SM observer cannot see.

## Decoherence as algebraic projection

Standard open-systems quantum theory uses Lindblad operators:
$$\dot{\rho} = -i[H, \rho] + \sum_k\bigl(L_k\,\rho\,L_k^\dagger - \tfrac{1}{2}\{L_k^\dagger L_k, \rho\}\bigr),$$
where $L_k$ are typically non-Hermitian operators describing
coupling to environment modes.  Probability flows from the
"system" to the "environment" in a way that looks non-unitary
on the system alone, but is unitary on the combined system +
environment.

The framework's setup is structurally cleaner.  All 71
centralizer generators are Hermitian; they commute with the
bipartite tick rule, so $\mathcal{A}=1$ is preserved on the
full $\mathbb{C}^{12}$ amplitude.  There is no actual
non-unitarity anywhere -- only a *projection* induced by
restricting attention to SM-gauge-invariant observables.

In this reading:

- **The "system"** is the SM-gauge-invariant 12-dim sector.
- **The "environment"** is the 59-dim extras sector.
- **The Lindblad operators** correspond to the 59 extras
  themselves, but acting *unitarily* on the full $\mathbb{C}^{12}$
  -- it is only the SM-projection that turns their effect into
  apparent decoherence.
- **The trace-out** is the SM-gauge-invariance projection,
  $\rho_{\text{SM}} = P_{\text{SM}}\,\rho_{\text{full}}\,P_{\text{SM}}$
  where $P_{\text{SM}}$ is the projector onto the SM-invariant
  subspace.

The mechanism: a coherent state in the full $\mathbb{C}^{12}$
that has support on both SM and extras subspaces, when projected
onto SM, gives a *mixed* state -- the "lost coherence" is the
extras-subspace content that the projection annihilates.  But
the full state was, and remains, a pure state in the full
71-dim sector.

## What the framework derives that the SM cannot

Standard decoherence theory imports the Lindblad operators
$\{L_k\}$ phenomenologically -- as a model of "how the
environment interacts with the system."  The framework derives
the analogous set from first principles: the 59 extras are
*exactly* the operators that commute with the bipartite tick
rule (i.e., preserve $\mathcal{A}=1$) but that the SM's
factor-product gauge invariance forbids.  Algebraically:

$$\{\text{decoherence channels}\} = \mathfrak{Aut}_{\text{cent}}(71) \setminus \mathfrak{Aut}_{\text{SM}}(12) = \text{59-dim extras subspace}.$$

The 59 extras decompose under $SU(3) \times SU(2)$ as

- $24 + 24 = 48$ generators in $(\mathbf{8}, \mathbf{3})$
  (colour-octet weak-triplet, "leptoquark-flavoured"), and
- $8 + 3 = 11$ generators of chirality-$\sigma_x$-twisted
  SM-flavoured channels.

These are the *structurally derived* decoherence channels of
the framework.  Each one carries a specific colour /
weak-isospin / chirality content, so the framework predicts
that decoherence in different gauge sectors should have
**anisotropic structure** -- the rate of coherence loss should
depend on which factor is being mixed.

## The minimum-probability-change formulation

If the lattice tick rule is reformulated to transfer a discrete
quantum $\Delta p$ of probability per tick (rather than the
continuous $\sin^2(\delta\phi/2)$ split currently in
`src/utilities/tick_rule_extended_consistency.py`), then:

- $\mathcal{A}=1$ becomes an *exact integer-valued* identity:
  total probability is conserved modulo the discrete quantum,
  with no rounding error.
- Each "decoherence event" is an integer number of tick-quanta
  transferred from SM-visible to extras-hidden channels.
- The decoherence rate becomes *quantized*: not a continuous
  $\Gamma$ but a discrete sequence $n \Delta p / \tau$ for tick
  duration $\tau$ and integer $n$.

This is a specific testable departure from standard QM
decoherence theory (which assumes continuous $\Gamma$).  The
prediction would be that high-precision interferometry should
see *discrete steps* in coherence-loss rates, rather than
continuous decay.  Whether existing experiments can distinguish
this from continuous decay depends on $\Delta p / \tau$ -- if
the quantum is small enough (Planck-scale), the discreteness
would be unobservable at current sensitivities; if it's larger,
this is already in tension with measurement.

## The concrete calculation to make this rigorous

A small follow-up script could compute the *rate* of probability
flow from SM-projected to extras-projected wavefunctions as a
function of the tick rule's $\delta\phi$ and the initial
coherence.

Sketch:

1. Define a density matrix $\rho_0$ on $\mathbb{C}^{12}$ with
   support on both SM and extras subspaces (a generic mixed
   state).
2. Evolve under the tick rule: $\rho(n) = T_{\text{ext}}^n\,\rho_0\,(T_{\text{ext}}^\dagger)^n$.
3. Project at each step: $\rho_{\text{SM}}(n) = P_{\text{SM}}\,\rho(n)\,P_{\text{SM}}$.
4. Measure the "coherence" of $\rho_{\text{SM}}(n)$ as the
   purity $\mathrm{Tr}(\rho_{\text{SM}}^2)$ or the off-diagonal
   element magnitudes.
5. Watch how coherence evolves with $n$.  If the framework's
   hypothesis is right, the rate of coherence loss should be
   determined by which extras directions $\rho_0$ has support
   on.

The script would be ~100-150 lines of sympy + numpy.  The
projector $P_{\text{SM}}$ is constructed from the 12 SM Hermitian
generators of the centralizer (already enumerated in
`automorphism_centralizer_extended.py`).  The outcome would be a
quantitative prediction for decoherence-rate ratios across the
$(\mathbf{8}, \mathbf{3})$ and chirality-shadow channels.

## What this hypothesis would change for Paper~II

If verified, Paper~II's "characterisation" outcome (Phase 1 +
Phase 3 + the 59 extras) gains a much sharper physical
interpretation:

- The framework's prediction is not "Eq.~(137) holds at the
  factor-product level only" but the stronger claim
  "Eq.~(137) holds *exactly* as the SM-gauge-invariant projection
  of a 71-dim broken-symmetry algebra, with the 59 extras
  appearing in observable physics as the structural decoherence
  channels."
- This converts the 59 extras from "structural curiosities" to
  *predictive content*: a specific colour-weak-isospin anisotropy
  in decoherence rates that experiments could test.
- The "minimum probability change" angle would give the framework
  a falsifiable prediction at high-precision interferometric
  scales.

The two narrative framings of
`notes/aut_centralizer_extras_commutators.md` (high-energy
unification vs decoherence) collapse to a single sharper version:
*decoherence as algebraic projection through the 59 extras*.
The high-energy unification framing (extras as massive GUT-style
gauge bosons) is the *complementary* picture in which the
extras are gauge bosons that the lattice geometry has chosen to
suppress.  Both are simultaneously true: the 59 extras are both
GUT-style would-be gauge bosons AND the decoherence-bookkeeping
channels -- they are the same object viewed through different
physical lenses.

## Open structural questions

1. *Is the SM-projection $P_{\text{SM}}$ actually
   gauge-invariant?*  The 12 SM Hermitian generators form a
   subalgebra of the 71-dim centralizer; the SM-invariant
   subspace of $\mathbb{C}^{12}$ is the joint eigenspace of all
   12 SM generators with eigenvalue zero (or with their Casimirs
   at specific values).  The projector $P_{\text{SM}}$ onto this
   subspace is well-defined but may be smaller-dimensional than
   12.  Working out its rank is a small calculation.

2. *What is the minimum quantum $\Delta p$?*  If the lattice
   has a natural smallest unit of probability transfer, it
   should be expressible in terms of $\sin(\delta\phi/2)$ for
   the smallest meaningful $\delta\phi$ (perhaps $\delta\phi =
   2\pi/N$ for some integer $N$ related to the lattice scale).
   This connects to Paper~I's mass-as-clock-density
   identification: the smallest $\delta\phi$ corresponds to the
   smallest fermion mass, and $\Delta p$ would scale with mass.

3. *Does the decoherence rate match measured rates?*  The
   framework predicts specific colour-weak-isospin anisotropies.
   Comparing to measured decoherence rates in interferometric
   experiments (atomic, molecular, photonic) would test the
   hypothesis.

## Upstream-flow tags

- **Notation:** the framework's $\mathcal{A}=1$ conservation
  applies to the full 71-dim centralizer's action on $\mathbb{C}^{12}$;
  the 59 extras are the algebraic ledger entries for probability
  flowing out of the SM-gauge-invariant sector.  The notation
  catalogue in
  `external/research/Notes/balanced_equations/` should record
  the SM-projection as the natural restriction operation linking
  fundamental ($\mathcal{A}=1$) and observable (SM-gauge-invariant)
  amplitudes.
- **Topology / structure of the bipartition:** the chirality
  $\sigma_x$ block structure of the centralizer (35 internal +
  36 $\sigma_x$ extras) gives the framework's distinction between
  "in-block" and "across-block" decoherence channels -- a
  topological feature of how probability can flow across the
  bipartite RGB/CMY exchange.
- **Balanced equations:** an $\mathcal{A}=1$-conserving reaction
  in the framework's algebra can include flow into 59-extras
  channels without violating $\mathcal{A}=1$.  This extends the
  balanced-equation formalism upstream
  (`external/research/Notes/balanced_equations/`) with an
  "extras column" that tracks probability flow into the
  SM-gauge-violating bookkeeping sector.

## Pointers

- Adjacent: `notes/aut_centralizer_extras_commutators.md` -- the
  algebraic finding that the 59 extras are an SM-module under
  adjoint action, not a Lie ideal.  This note upgrades the
  interpretation to "decoherence channels with specific
  structure."
- Adjacent: `notes/aut_centralizer_enumeration.md` -- the
  parent finding of the 71-dim centralizer and its
  $\mathfrak{su}(6) \oplus \mathfrak{su}(6) \oplus \mathfrak{u}(1)$
  decomposition.
- Adjacent: `notes/mass_chirality_coupling.md` -- the related
  observation that the lattice's clock-density preservation
  forces vector-like gauge coupling.  The decoherence-as-
  projection mechanism may also explain why apparent chirality
  is recovered in observable physics: chirality coupling lives
  in the chirality-$\sigma_x$ extras subspace, which is hidden
  from SM-projected observers.
- Adjacent: `notes/debt_to_measurement.md` -- the framing that
  framework predictions are measurement-anchored.  The
  decoherence-as-projection mechanism is a specific instance:
  what observers measure is the SM-projection, and the
  framework's prediction is that the projection loses
  information that the full lattice carries.
- Adjacent: `notes/no_spacetime_torsion.md` -- the framework's
  geometric primitives are flat substrate + scalar density +
  tick operator, not curved spacetime.  The decoherence-as-
  projection mechanism extends this: what observers measure as
  "decoherence" is the projection from the framework's full
  geometric structure onto the SM-gauge-invariant sector, not
  a spacetime-curvature or environment-coupling effect.

## What the follow-up script should look like

```python
# src/utilities/decoherence_as_projection.py (sketch)
#
# 1. Define SM projector P_SM on C^12 (using 12 Hermitian SM
#    generators from automorphism_centralizer_extended.py).
# 2. Define a generic density matrix rho_0 with support on
#    both SM and extras subspaces.
# 3. Evolve under the bipartite tick rule for n ticks:
#    rho(n) = T^n rho_0 (T^dagger)^n.
# 4. Project at each step: rho_SM(n) = P_SM rho(n) P_SM.
# 5. Measure coherence loss: Tr(rho_SM(n)^2) or specific
#    off-diagonal magnitudes.
# 6. Compare across initial conditions with support on
#    different extras-irrep directions ((8,3) vs
#    chirality-sigma_x-twisted vs ...).
# 7. Report: rate of coherence loss as a function of which
#    extras irrep the initial state has support on.
#
# Expected outcome: anisotropic decoherence -- different rates
# for different extras-irrep directions, exactly matching the
# framework's SU(3) x SU(2) representation decomposition.
```

This is the concrete next step that would convert the
hypothesis into a quantitative prediction.  It is not done in
this note; the note records the structural reading and the
calculation sketch for future work.
