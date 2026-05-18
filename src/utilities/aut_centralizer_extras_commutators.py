"""
aut_centralizer_extras_commutators.py

Phase 3 extension: compute the bracket structure between the 59
"extra" generators of the discrete-Hermitian centralizer (from
automorphism_centralizer_extended.py) and the 12 Hermitian SM
gauge generators that sit inside the centralizer.  The structural
question this resolves:

  Is the 12-dim SM subalgebra a NORMALISER of the 59 extras
  inside the 71-dim centralizer?  Equivalently: do brackets
  [E, T] with E in extras and T in SM produce more SM generators,
  or do they stay within the extras?

The answer determines the algebraic shape of the symmetry breaking
needed to recover Eq.~(137) as exact equality.

Background.

The 71-dim centralizer of $\\sigma_x \\otimes I_2 \\otimes I_3$ in
su(12) is structurally su(6)_+ (+) su(6)_- (+) u(1), with the two
su(6) factors acting on the +/- 1 chirality eigenspaces.  Under
SU(3) x SU(2) (the SM gauge subgroup), each su(6) factor branches
as

    35 = (8, 1) (+) (1, 3) (+) (8, 3)

where (8, 1) is su(3)_c, (1, 3) is su(2)_W, and (8, 3) is the
"leptoquark-flavoured" colour-octet weak-triplet representation
that contains the factor-mixing extras.

If the SM subalgebra were an IDEAL of the 71-dim centralizer, then
brackets [extras, SM] would land in extras only (the complement of
SM would be invariant under SM action) -- this would make the
71-dim algebra a *semidirect sum* with SM as the structural
subalgebra and extras as the module.

If brackets [extras, SM] land partly in SM, the SM subalgebra is
NOT a normaliser, and the 71/12 structure is more entangled.

This script computes all 59 x 12 = 708 brackets and classifies
each as:
  - zero (the bracket vanishes),
  - in_SM (the bracket lies in the 12-dim SM subalgebra),
  - in_extras (the bracket lies in the 59-dim extras complement),
  - or mixed (has components in both).

Predicted outcome (by representation theory).

The su(6) adjoint under SU(3) x SU(2) is (8,1) + (1,3) + (8,3).  The
SM corresponds to (8,1) + (1,3); the extras correspond to (8,3) in
each chirality block (plus 11 more from $\\sigma_x$-twisted
SM-flavoured generators in the $\\sigma_x$ block).  Brackets:

  - [(8, 1), (8, 3)] = (8, 3) + (1, 3) + ... (Lie-algebra closure
    on the colour index, but the weak-triplet index is just
    acted on)
    Color brackets give (8 x 8 -> 1 + 8 + ...) but only (8, 3)
    survives because the iso-triplet doesn't mix.
  - [(1, 3), (8, 3)] = (8, 3) similarly.

So [(SM in (8,1)+(1,3)), (extras in (8,3))] = (8, 3) -> stays in
extras.  This confirms: extras are SU(3)xSU(2)-irreducible
representation, and SM brackets with them stay within extras.

For the chirality-$\\sigma_x$ extras (35 of 59), the chirality
factor is $\\sigma_x$, but the chirality factor of SM is either I
or $\\sigma_x$ (for $J_1$ only).  Since $J_1$ is central (commutes
with everything in the centralizer), [J_1, extras] = 0.  For other
SM (chirality = I), brackets with $\\sigma_x$-extras have the same
SU(3)xSU(2) representation content as their non-$\\sigma_x$
counterparts, so they stay in extras.

Conclusion: [extras, SM] should land entirely in extras, with no
SM component.  The SM subalgebra is a STRUCTURAL SUBALGEBRA of
the 71-dim centralizer (closed under inner brackets) but the
extras form a SUBALGEBRA-COMPLEMENT that is INVARIANT under
inner derivation by SM (i.e., extras form a module under the
adjoint action of SM).

This is exactly the algebraic shape of a broken symmetry: a
larger algebra G' (here su(6) (+) su(6) (+) u(1)) with a
structural subgroup G (here SM = su(3)xsu(2)xu(1)_{J_1}) and a
complement m = G'/G that transforms as a G-representation.

This script verifies the prediction by enumeration.

Provenance.

This file is reproduced verbatim from Paper II
(doi:10.5281/zenodo.20240736).  It is reproduced in the
dcl-generator-zoo as inherited evidence; downstream zoo tooling
extends but does not modify it.  The import path
'src.utilities.automorphism_centralizer_extended' is identical in
the two repositories, so no edit is needed.
"""

import sympy as sp
from sympy import I, Matrix, eye, sqrt, simplify, Rational

# Reuse the tensor basis from automorphism_centralizer_extended.py
from src.utilities.automorphism_centralizer_extended import (
    pauli_matrices,
    gell_mann_matrices,
    kron,
    commutator,
    is_zero_matrix,
    tensor_basis_su12,
    classify_element,
    commutes_with_tick,
)


def matrix_to_vec(M, n=12):
    """Flatten an n x n complex matrix to a complex n*n column vector
    for linear-algebra checks (rank, span over the complex field).

    Note: commutators of Hermitian generators are anti-Hermitian (= $i$
    times Hermitian).  We compute rank over the complex field so that
    $iH$ lies in the complex span of $H$, regardless of (anti-)Hermitian
    status."""
    return Matrix([M[i, j] for i in range(n) for j in range(n)])


def rank_of_matrices(mats, n=12):
    """Dimension of the linear span of a list of n x n matrices."""
    if not mats:
        return 0
    vecs = [matrix_to_vec(m, n) for m in mats]
    big = sp.Matrix.hstack(*vecs)
    return big.rank()


def is_in_span(M, basis_set, basis_rank=None, n=12):
    """Whether M is in the linear span of the basis_set matrices."""
    if basis_rank is None:
        basis_rank = rank_of_matrices(basis_set, n)
    return rank_of_matrices(basis_set + [M], n) == basis_rank


def classify_bracket(bracket, sm_basis, sm_rank, extras_basis, extras_rank, n=12):
    """Classify the bracket [E, T] as:
      - 'zero' if it vanishes,
      - 'in_SM' if it lies entirely in the SM subspace,
      - 'in_extras' if it lies entirely in the extras subspace,
      - 'mixed' if it has components in both (this should not
        occur for centralizer elements since SM (+) extras span
        the full centralizer)."""
    if is_zero_matrix(bracket):
        return 'zero'
    in_sm = is_in_span(bracket, sm_basis, basis_rank=sm_rank, n=n)
    in_extras = is_in_span(bracket, extras_basis, basis_rank=extras_rank, n=n)
    if in_sm and in_extras:
        # Both: this means the bracket is zero (caught above) or
        # the basis sets overlap (they shouldn't).
        return 'in_SM_and_extras_inconsistent'
    if in_sm:
        return 'in_SM'
    if in_extras:
        return 'in_extras'
    # Neither: would mean the bracket is outside the centralizer,
    # which contradicts the Jacobi identity if E and T both commute
    # with the tick rule.
    return 'OUTSIDE_centralizer_inconsistent'


def report():
    print("=" * 70)
    print("Phase 3 extension: bracket structure of the 59 extras vs SM")
    print("=" * 70)
    print()

    # -- Step 1: get the centralizer basis ----------------------------
    print("Loading the 71-dim centralizer basis from")
    print("automorphism_centralizer_extended.py...")
    print()

    sx, _, _ = pauli_matrices()
    Y = kron(sx, eye(2), eye(3))
    all_basis = tensor_basis_su12()
    centralizer = [e for e in all_basis if commutes_with_tick(e, Y)]
    print(f"  Centralizer size: {len(centralizer)} generators (expected 71).")
    print()

    # Split centralizer into SM and extras
    sm_elements = []
    extras_elements = []
    for elt in centralizer:
        cls = classify_element(elt)
        if (cls.startswith('J_1') or
                cls.startswith('SU(2)_W') or
                cls.startswith('SU(3)')):
            sm_elements.append(elt)
        else:
            extras_elements.append(elt)
    print(f"  SM-aligned     : {len(sm_elements)} generators (expected 12).")
    print(f"  Extras         : {len(extras_elements)} generators (expected 59).")
    print()

    sm_basis = [e['matrix'] for e in sm_elements]
    extras_basis = [e['matrix'] for e in extras_elements]
    sm_rank = rank_of_matrices(sm_basis)
    extras_rank = rank_of_matrices(extras_basis)
    print(f"  Rank check:  SM basis rank = {sm_rank}, extras basis rank = "
          f"{extras_rank}.")
    print(f"  Total rank   = {sm_rank + extras_rank} (expected 71).")
    print()

    # -- Step 2: compute all 59 x 12 brackets -------------------------
    print("-" * 70)
    print("Step 2: computing 59 * 12 = 708 brackets [E, T]")
    print("-" * 70)
    print()

    counts = {
        'zero': 0,
        'in_SM': 0,
        'in_extras': 0,
        'in_SM_and_extras_inconsistent': 0,
        'OUTSIDE_centralizer_inconsistent': 0,
    }
    sample_in_SM = []
    sample_in_extras = []

    print(f"  Iterating through 708 (E in extras, T in SM) pairs...")
    print(f"  (each bracket is a 12x12 sympy commutator + classification)")
    print()

    for i, E_elt in enumerate(extras_elements):
        for j, T_elt in enumerate(sm_elements):
            br = commutator(E_elt['matrix'], T_elt['matrix'])
            cls = classify_bracket(br, sm_basis, sm_rank,
                                   extras_basis, extras_rank)
            counts[cls] += 1
            if cls == 'in_SM' and len(sample_in_SM) < 3:
                sample_in_SM.append((E_elt, T_elt, br))
            elif cls == 'in_extras' and len(sample_in_extras) < 3:
                sample_in_extras.append((E_elt, T_elt, br))

    print(f"  Bracket classification counts:")
    print(f"    zero            : {counts['zero']:>4d}")
    print(f"    in_SM           : {counts['in_SM']:>4d}")
    print(f"    in_extras       : {counts['in_extras']:>4d}")
    inconsistent_total = (counts['in_SM_and_extras_inconsistent']
                          + counts['OUTSIDE_centralizer_inconsistent'])
    print(f"    inconsistent    : {inconsistent_total:>4d}")
    print(f"    total           : {sum(counts.values()):>4d}  (expected 708)")
    print()

    # -- Step 3: interpret the result --------------------------------
    print("-" * 70)
    print("Step 3: structural interpretation")
    print("-" * 70)
    print()
    if counts['in_SM'] == 0 and counts['in_extras'] > 0:
        print("  RESULT: zero brackets land in SM.  The 59-dim extras")
        print("  subspace is INVARIANT under the adjoint action of the")
        print("  12-dim SM subalgebra.")
        print()
        print("  Algebraically: the 71-dim centralizer is a SPLIT")
        print("  EXTENSION (semidirect sum) of the form")
        print()
        print("    71-dim centralizer = 12-dim SM (+) 59-dim extras")
        print()
        print("  where:")
        print("    - SM = (8, 1) (colour) (+) (1, 3) (isospin) (+)"
              " 1-dim <J_1>")
        print("    - extras = 24 * 2 = 48 in (8, 3) (leptoquark-")
        print("      flavoured) plus 11 chirality-sigma_x SM-flavoured")
        print()
        print("  This is exactly the structure of a BROKEN SYMMETRY:")
        print("  a larger algebra (su(6) (+) su(6) (+) u(1)) with a")
        print("  structural subgroup (SM) and a complementary module")
        print("  (extras) that transforms as SU(3) x SU(2) reps under")
        print("  the SM adjoint action.")
    elif counts['in_SM'] > 0:
        print("  RESULT: some brackets land in SM ({counts['in_SM']}/708).")
        print("  The SM subalgebra is NOT a normaliser of the extras.")
        print("  The 71-dim algebra has a more entangled structure than")
        print("  a clean semidirect sum.")
    else:
        print("  RESULT: all brackets are zero.  The SM and extras")
        print("  commute entirely.  Unexpected; investigate.")
    print()

    # -- Step 4: sample brackets --------------------------------------
    print("-" * 70)
    print("Step 4: sample brackets (illustrative)")
    print("-" * 70)
    print()
    if sample_in_extras:
        print(f"  Three sample brackets that land in extras:")
        for E_elt, T_elt, br in sample_in_extras:
            E_label = (f"{E_elt['chir_label']} (x) {E_elt['iso_label']}"
                       f" (x) {E_elt['col_label']}")
            T_label = (f"{T_elt['chir_label']} (x) {T_elt['iso_label']}"
                       f" (x) {T_elt['col_label']}")
            non_zero = not is_zero_matrix(br)
            print(f"    [E={E_label}, T={T_label}] {'non-zero' if non_zero else 'zero'}")
    print()

    # -- Step 4b: [extras, extras] check -----------------------------
    print("-" * 70)
    print("Step 4b: [extras, extras] bracket structure")
    print("-" * 70)
    print()
    print("  If [extras, extras] is contained in extras, the 71-dim")
    print("  centralizer is a SEMIDIRECT SUM (extras is an ideal).")
    print("  If [extras, extras] has SM components, the structure is")
    print("  a SYMMETRIC PAIR-like decomposition where extras is a")
    print("  Lie-algebra-module but not an ideal.")
    print()
    extras_extras_counts = {
        'zero': 0,
        'in_SM': 0,
        'in_extras': 0,
        'mixed': 0,
    }
    n_pairs = len(extras_elements) * (len(extras_elements) - 1) // 2
    print(f"  Computing {n_pairs} = C(59, 2) brackets [E_i, E_j] for i < j...")

    for i in range(len(extras_elements)):
        for j in range(i + 1, len(extras_elements)):
            br = commutator(extras_elements[i]['matrix'],
                            extras_elements[j]['matrix'])
            if is_zero_matrix(br):
                extras_extras_counts['zero'] += 1
            else:
                in_sm = is_in_span(br, sm_basis, basis_rank=sm_rank)
                in_ex = is_in_span(br, extras_basis, basis_rank=extras_rank)
                if in_sm and not in_ex:
                    extras_extras_counts['in_SM'] += 1
                elif in_ex and not in_sm:
                    extras_extras_counts['in_extras'] += 1
                else:
                    extras_extras_counts['mixed'] += 1

    print()
    print(f"  [E_i, E_j] for i < j counts:")
    print(f"    zero        : {extras_extras_counts['zero']:>5d}")
    print(f"    in_SM       : {extras_extras_counts['in_SM']:>5d}")
    print(f"    in_extras   : {extras_extras_counts['in_extras']:>5d}")
    print(f"    mixed       : {extras_extras_counts['mixed']:>5d}")
    print(f"    total       : {sum(extras_extras_counts.values()):>5d}")
    print(f"               (expected {n_pairs})")
    print()
    if extras_extras_counts['in_SM'] > 0 or extras_extras_counts['mixed'] > 0:
        print("  The [extras, extras] bracket has SM components: extras is")
        print("  NOT a Lie ideal of the centralizer.  Structurally, the 71-dim")
        print("  algebra is su(6) (+) su(6) (+) u(1) with SM as a non-normal")
        print("  subalgebra; extras is the coset space modulo SM, not an")
        print("  invariant submodule under bracketing within itself.")
    else:
        print("  All [extras, extras] land in extras: the 71-dim centralizer")
        print("  is a true semidirect sum SM (x) extras.")
    print()

    # -- Step 5: physical implications --------------------------------
    print("-" * 70)
    print("Step 5: physical implications")
    print("-" * 70)
    print()
    print("  The structure 'SM acts on extras as a module' is the algebraic")
    print("  signature of a symmetry-breaking pattern G' -> G with broken")
    print("  generators m = G'/G.  In standard symmetry breaking:")
    print()
    print("    - G' = larger gauge symmetry (here su(6) (+) su(6) (+) u(1))")
    print("    - G  = unbroken subgroup (here the SM su(3) x su(2) x u(1))")
    print("    - m  = coset generators that become MASSIVE gauge bosons")
    print("           after spontaneous breaking (here the 59 extras)")
    print()
    print("  The framework's natural prediction: at the lattice scale 1/a,")
    print("  the 71-dim symmetry is unbroken; the 59 extras are gauge")
    print("  bosons that mediate factor-mixing interactions.  At lower")
    print("  energies (after some breaking mechanism), the 59 extras")
    print("  acquire large masses and decouple, leaving only the 12-dim")
    print("  SM gauge sector as the effective theory.")
    print()
    print("  This is the same shape as standard GUT symmetry breaking")
    print("  (SU(5) -> SM, with X/Y leptoquarks getting heavy masses),")
    print("  except the framework gets there from $\\mathcal{A}=1$ on the")
    print("  bipartite lattice rather than from postulated gauge content.")
    print()
    print("  Implication for Eq.~(137):  the conjecture's equality $=$ is")
    print("  recovered at the EFFECTIVE level after the 59 extras")
    print("  decouple.  At the fundamental (lattice) level, the algebra")
    print("  is 71-dim, not 18-dim.  Whether the SM is recovered as the")
    print("  EFFECTIVE algebra requires a mass-generation mechanism for")
    print("  the 59 extras -- a question the framework does not yet")
    print("  settle but now poses precisely.")


if __name__ == '__main__':
    report()
