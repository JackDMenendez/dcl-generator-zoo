"""
generator_zoo.py  -- the dcl-generator-zoo catalogue script.

Extends the Paper II Phase 3 centralizer enumeration with the
zoo's value-add layer:

  - Stable per-generator name (G_01 .. G_71).  Names are preserved
    across catalogue revisions; downstream papers cite generators
    by name.
  - 3-bit tensor-factor action tag (chir, iso, col), one bit per
    factor, 1 iff that factor is non-identity.
  - (SU(3), SU(2)) irrep tag from the
    35 = (8,1) + (1,3) + (8,3) + (1,1) branching of su(6) under
    SU(3) x SU(2) (via 6 = (3, 2)).
  - chirality-block label ('I' vs 'X'): which of the two
    su(6) factors in the chirality eigenspace decomposition
    su(6)_+ (+) su(6)_- (+) u(1) the generator lives in.
  - SM classification: 'SM' (one of the 12 SM gauge generators
    plus J_1) or 'extras' (one of the 59 generators that commute
    with the tick rule but are not SM gauge).
  - Bracket-class classification for all C(71, 2) = 2485 unordered
    pairs (G_i, G_j) with i < j.  Each bracket [G_i, G_j] is
    classified as 'zero', 'in_SM', 'in_extras', or 'mixed'.

Emits:

  - data/generator_catalogue.json   -- machine-readable catalogue,
    one record per generator plus the full bracket-class table.
  - paper/sections/generator_zoo_table.tex  -- LaTeX longtable
    fragment that paper/sections/generator_zoo.tex \\input{}s.

Algebraic substance is inherited verbatim from Paper II Phase 3
(this script does no new derivation).  The 71-element centralizer,
the 12 + 59 SM/extras split, and the bracket-class classifier are
all imported from the upstream scripts:

  src/utilities/automorphism_centralizer_extended.py
  src/utilities/aut_centralizer_extras_commutators.py

Runtime: a few minutes on a modern laptop (2485 sympy commutators
with rank-based classification over the complex field).

Stable-name ordering convention:

    G_01           : J_1 = (1/2) sigma_x x I_2 x I_3  (central U(1))
    G_02 .. G_04   : SU(2)_W generators (I x sigma_a x I, a=X,Y,Z)
    G_05 .. G_12   : SU(3)_c Gell-Manns (I x I x lambda_a, a=1..8)
    G_13 .. G_36   : iso-col mixings (I x sigma_a x lambda_b), 24
    G_37 .. G_39   : chir-X x iso (sigma_x x sigma_a x I), 3
    G_40 .. G_47   : chir-X x col (sigma_x x I x lambda_a), 8
    G_48 .. G_71   : chir-X x iso x col (sigma_x x sigma_a x lambda_b), 24

Within each block, ordering is lexicographic by (iso_label,
col_label) using the map I=0, X=1, Y=2, Z=3 (Pauli) and I=0,
'1'=1..'8'=8 (Gell-Mann).  This ordering is stable across
catalogue revisions provided the underlying basis enumeration in
tensor_basis_su12() is not changed.
"""

import json
import os
from dataclasses import dataclass, asdict, field
from typing import List, Tuple, Dict

import sympy as sp

from src.utilities.automorphism_centralizer_extended import (
    pauli_matrices,
    gell_mann_matrices,
    kron,
    commutator,
    is_zero_matrix,
    tensor_basis_su12,
    commutes_with_tick,
)
from src.utilities.aut_centralizer_extras_commutators import (
    rank_of_matrices,
    is_in_span,
)


VERSION = "v0.1"
SCHEMA_VERSION = 1


# Pauli-label -> integer for stable lexicographic ordering.
PAULI_ORDER = {'I': 0, 'X': 1, 'Y': 2, 'Z': 3}


@dataclass
class Generator:
    """One generator of the 71-dim per-site centralizer."""
    name: str                       # 'G_01' .. 'G_71'
    chir_label: str                 # 'I' or 'X'
    iso_label: str                  # 'I' or 'X'/'Y'/'Z'
    col_label: str                  # 'I' or '1'..'8'
    factor_tag: Tuple[int, int, int]   # 3-bit action tag
    su3_irrep: str                  # '8' (adjoint) or '1' (trivial)
    su2_irrep: str                  # '3' (adjoint) or '1' (trivial)
    chirality_block: str            # 'I' (eigenvalue +1 block) or 'X' (eigenvalue -1 block sigma_x mixed)
    sm_class: str                   # 'SM' (one of 12) or 'extras' (one of 59)
    sm_subgroup: str                # 'J_1' / 'SU(2)_W' / 'SU(3)_c' / 'iso_col_mixing' / 'sigmaX_iso' / 'sigmaX_col' / 'sigmaX_iso_col'
    description: str                # human-readable
    matrix: object = field(default=None, repr=False, compare=False)

    def to_serializable(self) -> dict:
        d = asdict(self)
        d.pop('matrix', None)
        d['factor_tag'] = list(self.factor_tag)
        return d


def derive_factor_tag(chir: str, iso: str, col: str) -> Tuple[int, int, int]:
    """3-bit tag: 1 if the factor is non-identity, 0 if identity."""
    return (
        0 if chir == 'I' else 1,
        0 if iso == 'I' else 1,
        0 if col == 'I' else 1,
    )


def derive_irrep(chir: str, iso: str, col: str) -> Dict[str, str]:
    """Return the (SU(3), SU(2)) irrep tag plus the SM classification.

    All operators in the centralizer either touch only the colour
    (SU(3) generators -> (8, 1)), only the isospin (SU(2) -> (1, 3)),
    both (leptoquark-flavoured -> (8, 3)), or neither (J_1 -> (1, 1)).
    The chirality factor is independent (gives the chirality block)."""
    if chir == 'X' and iso == 'I' and col == 'I':
        # J_1 = (1/2) sigma_x x I x I -- central U(1), in SM
        return dict(
            su3_irrep='1', su2_irrep='1', chirality_block='X',
            sm_class='SM', sm_subgroup='J_1',
            description='J_1 = sigma_x x I_2 x I_3  (central U(1), in SM)',
        )
    if chir == 'I' and iso != 'I' and col == 'I':
        return dict(
            su3_irrep='1', su2_irrep='3', chirality_block='I',
            sm_class='SM', sm_subgroup='SU(2)_W',
            description=f'SU(2)_W generator  I x sigma_{iso.lower()} x I_3',
        )
    if chir == 'I' and iso == 'I' and col != 'I':
        return dict(
            su3_irrep='8', su2_irrep='1', chirality_block='I',
            sm_class='SM', sm_subgroup='SU(3)_c',
            description=f'SU(3)_c Gell-Mann  I x I x lambda_{col}',
        )
    if chir == 'I' and iso != 'I' and col != 'I':
        return dict(
            su3_irrep='8', su2_irrep='3', chirality_block='I',
            sm_class='extras', sm_subgroup='iso_col_mixing',
            description=f'iso-col mixing (leptoquark-flavoured)  I x sigma_{iso.lower()} x lambda_{col}',
        )
    if chir == 'X' and iso != 'I' and col == 'I':
        return dict(
            su3_irrep='1', su2_irrep='3', chirality_block='X',
            sm_class='extras', sm_subgroup='sigmaX_iso',
            description=f'chirality-shadow SU(2)_W  sigma_x x sigma_{iso.lower()} x I',
        )
    if chir == 'X' and iso == 'I' and col != 'I':
        return dict(
            su3_irrep='8', su2_irrep='1', chirality_block='X',
            sm_class='extras', sm_subgroup='sigmaX_col',
            description=f'chirality-shadow SU(3)_c  sigma_x x I x lambda_{col}',
        )
    if chir == 'X' and iso != 'I' and col != 'I':
        return dict(
            su3_irrep='8', su2_irrep='3', chirality_block='X',
            sm_class='extras', sm_subgroup='sigmaX_iso_col',
            description=f'chirality-shadow leptoquark  sigma_x x sigma_{iso.lower()} x lambda_{col}',
        )
    raise ValueError(f"Unexpected signature: ({chir}, {iso}, {col})")


# Stable ordering of the seven groups: SM first, then extras in the
# order they appear in the documentation.
GROUP_ORDER = [
    'J_1',
    'SU(2)_W',
    'SU(3)_c',
    'iso_col_mixing',
    'sigmaX_iso',
    'sigmaX_col',
    'sigmaX_iso_col',
]


def _sort_key(e):
    """Stable lexicographic sort within a group."""
    iso_key = PAULI_ORDER.get(e['iso_label'], 99)
    col_key = 0 if e['col_label'] == 'I' else int(e['col_label'])
    return (iso_key, col_key)


def build_catalogue() -> List[Generator]:
    """Build the 71-generator catalogue in stable G_NN order."""
    basis = tensor_basis_su12()
    sx, _, _ = pauli_matrices()
    Y = kron(sx, sp.eye(2), sp.eye(3))
    centralizer = [e for e in basis if commutes_with_tick(e, Y)]
    if len(centralizer) != 71:
        raise AssertionError(
            f"Expected 71 centralizer elements, got {len(centralizer)} "
            "-- inherited centralizer enumeration is inconsistent."
        )

    # Group by SM subgroup (uses same signature -> irrep mapping).
    groups: Dict[str, List[dict]] = {g: [] for g in GROUP_ORDER}
    for e in centralizer:
        sig = (e['chir_label'], e['iso_label'], e['col_label'])
        irrep_info = derive_irrep(*sig)
        groups[irrep_info['sm_subgroup']].append(e)

    # Sort within each group; assemble in stable order.
    catalogue: List[Generator] = []
    idx = 0
    for group_name in GROUP_ORDER:
        for e in sorted(groups[group_name], key=_sort_key):
            idx += 1
            sig = (e['chir_label'], e['iso_label'], e['col_label'])
            irrep_info = derive_irrep(*sig)
            tag = derive_factor_tag(*sig)
            catalogue.append(Generator(
                name=f"G_{idx:02d}",
                chir_label=e['chir_label'],
                iso_label=e['iso_label'],
                col_label=e['col_label'],
                factor_tag=tag,
                matrix=e['matrix'],
                **irrep_info,
            ))

    if len(catalogue) != 71:
        raise AssertionError(f"Catalogue size {len(catalogue)} != 71")

    # Sanity: stable per-group counts
    expected_counts = {
        'J_1': 1, 'SU(2)_W': 3, 'SU(3)_c': 8,
        'iso_col_mixing': 24, 'sigmaX_iso': 3,
        'sigmaX_col': 8, 'sigmaX_iso_col': 24,
    }
    actual_counts: Dict[str, int] = {}
    for g in catalogue:
        actual_counts[g.sm_subgroup] = actual_counts.get(g.sm_subgroup, 0) + 1
    if actual_counts != expected_counts:
        raise AssertionError(
            f"Per-group counts mismatch.  Expected {expected_counts}, "
            f"got {actual_counts}."
        )

    return catalogue


def classify_all_brackets(catalogue: List[Generator]) -> List[Dict]:
    """Compute and classify all C(71, 2) = 2485 brackets [G_i, G_j], i < j."""
    sm_matrices = [g.matrix for g in catalogue if g.sm_class == 'SM']
    extras_matrices = [g.matrix for g in catalogue if g.sm_class == 'extras']
    sm_rank = rank_of_matrices(sm_matrices)
    extras_rank = rank_of_matrices(extras_matrices)
    if sm_rank != 12:
        raise AssertionError(f"SM basis rank {sm_rank}, expected 12")
    if extras_rank != 59:
        raise AssertionError(f"Extras basis rank {extras_rank}, expected 59")

    n = len(catalogue)
    total_pairs = n * (n - 1) // 2
    print(f"  Computing {total_pairs} brackets [G_i, G_j] for i < j ...")
    print(f"  (each is a 12x12 sympy commutator + rank-based class check)")
    print()

    results: List[Dict] = []
    pair_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            pair_count += 1
            if pair_count % 250 == 0 or pair_count == total_pairs:
                print(f"    progress: {pair_count}/{total_pairs}")
            G_i = catalogue[i]
            G_j = catalogue[j]
            br = commutator(G_i.matrix, G_j.matrix)
            if is_zero_matrix(br):
                cls = 'zero'
            else:
                in_sm = is_in_span(br, sm_matrices, basis_rank=sm_rank)
                in_ex = is_in_span(br, extras_matrices, basis_rank=extras_rank)
                if in_sm and not in_ex:
                    cls = 'in_SM'
                elif in_ex and not in_sm:
                    cls = 'in_extras'
                else:
                    cls = 'mixed'
            results.append({
                'i': G_i.name,
                'j': G_j.name,
                'class': cls,
            })

    return results


def emit_json(catalogue: List[Generator],
              brackets: List[Dict],
              output_path: str) -> None:
    """Write the machine-readable catalogue + bracket table."""
    counts: Dict[str, int] = {}
    for br in brackets:
        counts[br['class']] = counts.get(br['class'], 0) + 1
    payload = {
        'schema_version': SCHEMA_VERSION,
        'catalogue_version': VERSION,
        'description': (
            'dcl-generator-zoo: catalogue of the 71-dim per-site '
            'automorphism algebra of the A=1 Discrete Causal Lattice.  '
            'Inherited from Paper II Phase 3 '
            '(doi:10.5281/zenodo.20240736).'
        ),
        'centralizer_dim': 71,
        'sm_dim': 12,
        'extras_dim': 59,
        'bracket_counts': counts,
        'bracket_total': sum(counts.values()),
        'generators': [g.to_serializable() for g in catalogue],
        'brackets': brackets,
    }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(payload, f, indent=2)
    print(f"  Wrote {output_path} ({len(catalogue)} generators, "
          f"{len(brackets)} brackets).")


def _tex_chir(label: str) -> str:
    return r'$I$' if label == 'I' else r'$\sigma_x$'


def _tex_iso(label: str) -> str:
    if label == 'I':
        return r'$I$'
    return fr'$\sigma_{{{label.lower()}}}$'


def _tex_col(label: str) -> str:
    if label == 'I':
        return r'$I$'
    return fr'$\lambda_{{{label}}}$'


def _tex_class(subgroup: str) -> str:
    # Match the audit-table conventions: \texttt{...} with escaped underscores.
    return r'\texttt{' + subgroup.replace('_', r'\_') + r'}'


def emit_latex_longtable(catalogue: List[Generator],
                         output_path: str) -> None:
    """Write the catalogue longtable that the appendix \\input{}s."""
    lines: List[str] = []
    lines.append(
        '% AUTOGENERATED by src/utilities/generator_zoo.py'
        ' -- do not edit by hand.'
    )
    lines.append(
        '% Regenerate via:  python -m src.utilities.generator_zoo'
    )
    lines.append('% Source of truth: data/generator_catalogue.json')
    lines.append('')
    lines.append(r'\label{tab:generator_zoo}')
    lines.append('')
    lines.append(r'{\scriptsize')
    lines.append(r'\setlength{\tabcolsep}{4pt}')
    lines.append(r'\renewcommand{\arraystretch}{0.9}')
    lines.append(
        r'\begin{longtable}{@{}lcccccccc@{}}'
    )
    lines.append(
        r'\caption{\small Generator zoo: stable catalogue of the '
        r'71-dim per-site automorphism algebra.  '
        r'\textbf{Chir} / \textbf{Iso} / \textbf{Col}: tensor-signature '
        r'factor on $\mathbb{C}^2_{\text{chir}} \otimes '
        r'\mathbb{C}^2_{\text{iso}} \otimes \mathbb{C}^3_{\text{col}}$. '
        r'\textbf{Tag}: 3-bit factor-action tag (1 if non-identity). '
        r'$\mathbf{SU(3)}$ / $\mathbf{SU(2)}$: '
        r'$(\mathbf{8}, \mathbf{3})$ branching irrep under the SM '
        r'adjoint action.  \textbf{Block}: chirality eigenspace '
        r'($I$ or $\sigma_x$).  \textbf{Class}: SM gauge subgroup '
        r'or extras subgroup.} \\'
    )
    lines.append(r'\label{tab:generator_zoo_cap} \\')
    lines.append(r'\toprule')
    lines.append(
        r'\textbf{Name} & \textbf{Chir} & \textbf{Iso} & \textbf{Col} & '
        r'\textbf{Tag} & $\mathbf{SU(3)}$ & $\mathbf{SU(2)}$ & '
        r'\textbf{Block} & \textbf{Class} \\'
    )
    lines.append(r'\midrule')
    lines.append(r'\endfirsthead')
    lines.append(
        r'\multicolumn{9}{l}{\textit{(Table~\ref{tab:generator_zoo}, '
        r'continued)}} \\'
    )
    lines.append(r'\toprule')
    lines.append(
        r'\textbf{Name} & \textbf{Chir} & \textbf{Iso} & \textbf{Col} & '
        r'\textbf{Tag} & $\mathbf{SU(3)}$ & $\mathbf{SU(2)}$ & '
        r'\textbf{Block} & \textbf{Class} \\'
    )
    lines.append(r'\midrule')
    lines.append(r'\endhead')
    lines.append(r'\midrule')
    lines.append(
        r'\multicolumn{9}{r}{\textit{(continued on next page)}} \\'
    )
    lines.append(r'\endfoot')
    lines.append(r'\bottomrule')
    lines.append(r'\endlastfoot')

    current_class = None
    for g in catalogue:
        # Insert a horizontal rule when the SM-subgroup changes,
        # to visually separate the seven blocks.
        if g.sm_subgroup != current_class:
            if current_class is not None:
                lines.append(r'\midrule')
            current_class = g.sm_subgroup
        tag_str = ''.join(str(b) for b in g.factor_tag)
        row = (
            fr'\texttt{{{g.name}}} & '
            f'{_tex_chir(g.chir_label)} & '
            f'{_tex_iso(g.iso_label)} & '
            f'{_tex_col(g.col_label)} & '
            fr'\texttt{{{tag_str}}} & '
            fr'$\mathbf{{{g.su3_irrep}}}$ & '
            fr'$\mathbf{{{g.su2_irrep}}}$ & '
            f'{_tex_chir(g.chirality_block)} & '
            fr'{_tex_class(g.sm_subgroup)} \\'
        )
        lines.append(row)

    lines.append(r'\end{longtable}')
    lines.append(r'}')
    lines.append('')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f"  Wrote {output_path} ({len(catalogue)} rows).")


def _print_breakdown(catalogue: List[Generator]) -> None:
    by_subgroup: Dict[str, List[str]] = {}
    for g in catalogue:
        by_subgroup.setdefault(g.sm_subgroup, []).append(g.name)
    print('  Breakdown by SM-classification subgroup:')
    for sub in GROUP_ORDER:
        names = by_subgroup.get(sub, [])
        if names:
            line = (f"    {sub:<20s}: {len(names):>2d}  "
                    f"({names[0]} .. {names[-1]})")
        else:
            line = f"    {sub:<20s}:  0"
        print(line)


def report() -> None:
    print('=' * 70)
    print(f'dcl-generator-zoo catalogue ({VERSION}): build, classify, emit')
    print('=' * 70)
    print()

    print('-' * 70)
    print('Step 1: build catalogue (71 generators with stable names)')
    print('-' * 70)
    catalogue = build_catalogue()
    print(f"  Catalogue size: {len(catalogue)} (expected 71)")
    print()
    _print_breakdown(catalogue)
    print()

    print('-' * 70)
    print('Step 2: classify all C(71, 2) = 2485 brackets')
    print('-' * 70)
    brackets = classify_all_brackets(catalogue)
    counts: Dict[str, int] = {}
    for br in brackets:
        counts[br['class']] = counts.get(br['class'], 0) + 1
    print()
    print('  Bracket-class counts:')
    for cls in ('zero', 'in_SM', 'in_extras', 'mixed'):
        print(f"    {cls:<12s}: {counts.get(cls, 0):>5d}")
    print(f"    {'total':<12s}: {sum(counts.values()):>5d}  (expected 2485)")
    print()

    print('-' * 70)
    print('Step 3: emit JSON catalogue and LaTeX longtable')
    print('-' * 70)
    repo_root = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..'
    ))
    json_path = os.path.join(repo_root, 'data', 'generator_catalogue.json')
    latex_path = os.path.join(
        repo_root, 'paper', 'sections', 'generator_zoo_table.tex'
    )
    emit_json(catalogue, brackets, json_path)
    emit_latex_longtable(catalogue, latex_path)
    print()

    print('=' * 70)
    print('generator_zoo PASS  (71 generators enumerated and named, '
          '2485 brackets')
    print('                    classified, JSON + LaTeX emitted)')
    print('=' * 70)


if __name__ == '__main__':
    report()
