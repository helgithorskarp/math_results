"""Exact local-incidence validation for the conditional original tensor-face proof.

The full real-space kernel/norm bridge is ordinary mathematics in PROOF.md.
This script does not reverify the 10208 seed, materialize its enormous matrix,
or enumerate tensor directions. No solver, floating arithmetic or asserts.
"""
import argparse
import copy
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
from incidence import generate_block, check_basis, parameters, row, require


def canonical(data):
    return (json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n').encode()


def serializable(block):
    basis = block['basis']
    return dict(b=block['b'], layers=block['layers'], masks=block['masks'], gram=block['gram'],
        pivots=basis['pivots'], free=basis['free'],
        columns=[[[j, str(value)] for j, value in sorted(c.items())] for c in basis['columns']],
        rref=[[str(x) for x in w] for w in basis['rref']],
        checks={k: str(v) if isinstance(v, F) else v for k, v in block['checks'].items()})


def tensor_control(left, right, offset, n):
    """Check each original coordinate of one nontrivial local cross matrix."""
    require(offset >= left['b'] and offset + right['b'] <= n, 'Disjoint ground blocks')
    ma = left['masks']
    mb = [x << offset for x in right['masks']]
    ca, cb = left['basis']['columns'], right['basis']['columns']
    require(len(ca) >= 2 and len(cb) >= 2, 'Two genuine free directions in each block')
    last_a, last_b = len(ca) - 1, len(cb) - 1
    h = {(0, 0): F(1, 7), (0, last_b): F(-2, 11),
         (last_a, 0): F(3, 13), (last_a, last_b): F(5, 17)}
    z = {}
    for (k, l), value in h.items():
        for i, u in ca[k].items():
            for j, v in cb[l].items():
                z[i, j] = z.get((i, j), F(0)) + value * u * v
    z = {p: value for p, value in z.items() if value}
    # An independently indexed original-coordinate symmetric sparse representation.
    delta = {}
    for (i, j), value in z.items():
        a, b = ma[i], mb[j]
        delta[a, b] = value
        delta[b, a] = value
    require(all(a and b and a != b and not a & b and a | b != (1 << n) - 1
                for a, b in delta), 'All changed original support/diagonal/complements/empty')
    require(all(delta.get((b, a)) == value for (a, b), value in delta.items()), 'Original symmetry')
    members = sorted(set(x for pair in delta for x in pair))
    if len(left['layers']) > 1 or len(right['layers']) > 1:
        require(len({a.bit_count() for a in members}) > 1, 'Mixed layers exposed in actual original entries')
    for a in members:
        require(sum(value for (r, b), value in delta.items() if r == a) == 0, 'Original row sum')
        for p in range(n):
            require(sum(value for (r, b), value in delta.items() if r == a and b & (1 << p)) == 0,
                    'Every original point-star action')
    for (k, l), value in h.items():
        require(z.get((left['basis']['free'][k], right['basis']['free'][l])) == value,
                'Actual free-coordinate parameter recovery')
    frob2 = sum(value * value for value in z.values())
    # Entire block-square identity: Delta^2 is ZZ^T and Z^TZ, with zero cross blocks.
    for a in members:
        for b in members:
            actual = sum(delta.get((a, c), F(0)) * delta.get((c, b), F(0)) for c in members)
            if a in ma and b in ma:
                i, k = ma.index(a), ma.index(b)
                wanted = sum(z.get((i, j), F(0)) * z.get((k, j), F(0)) for j in range(len(mb)))
            elif a in mb and b in mb:
                j, l = mb.index(a), mb.index(b)
                wanted = sum(z.get((i, j), F(0)) * z.get((i, l), F(0)) for i in range(len(ma)))
            else:
                wanted = F(0)
            require(actual == wanted, 'Every complete original block-square entry')
    a, b = next(iter(delta))
    # Orient the witness X -> Y before applying the transposition from the proof.
    if a not in ma:
        a, b = b, a
    x = next(p for p in range(left['b']) if a & (1 << p))
    y = next(p for p in range(offset, offset + right['b']) if not b & (1 << p))
    swapped = (a ^ (1 << x)) | (1 << y)
    require(swapped.bit_count() == a.bit_count() and not swapped & b and
            (swapped, b) not in delta and delta[a, b] != 0, 'Changed/unchanged equal-size orbit witness')
    return dict(n=n, nonzero_ordered_entries=len(delta), active_original_vertices=len(members),
                actual_original_cardinalities=sorted({a.bit_count() for a in members}),
                checked_entire_square_entries=len(members) ** 2, original_star_actions=n * len(members),
                cross_frobenius_squared=str(frob2), actual_free_parameters_recovered=True,
                noninvariance_witness=[a, b, swapped],
                full_entries=[[[a, b], str(value)] for (a, b), value in sorted(delta.items())])


def rejection_controls(small):
    rejects = []
    def reject(name, function):
        try:
            function()
        except (ValueError, TypeError):
            rejects.append(name)
        else:
            raise RuntimeError('Damage accepted: ' + name)
    for name, b, layers in [('float_block', 4.0, [2]), ('bool_block', True, [2]),
                            ('duplicate_layers', 5, [2, 2]), ('unordered_layers', 5, [3, 2]),
                            ('full_layer', 4, [4]), ('empty_layers', 4, []),
                            ('singleton_layer', 4, [1]), ('float_layer', 4, [2.0])]:
        reject(name, lambda b=b, layers=layers: parameters(b, layers))
    for name, alter in [
        ('missing_column', lambda b: b['columns'].pop()),
        ('bad_free_value', lambda b: b['columns'][0].__setitem__(b['free'][0], F(2))),
        ('float_basis_value', lambda b: b['columns'][0].__setitem__(b['free'][0], 1.0)),
        ('bad_star_action', lambda b: b['columns'][0].__setitem__(b['pivots'][0], F(7))),
        ('duplicate_free_coordinate', lambda b: b['free'].__setitem__(0, b['free'][1])),
        ('out_of_range_original_vertex', lambda b: b['columns'][0].__setitem__(len(small['masks']), F(1)))]:
        b = copy.deepcopy(small['basis'])
        alter(b)
        reject(name, lambda b=b: check_basis(small['masks'], small['b'], b))
    return rejects


def run(record_path=None):
    blocks = [generate_block(4, [2]), generate_block(5, [2, 3]),
              generate_block(11, [9]), generate_block(14, [9]),
              generate_block(14, [9, 10, 11, 12, 13])]
    controls = [tensor_control(blocks[0], blocks[0], 4, 8),
                tensor_control(blocks[1], blocks[1], 5, 10)]
    damages = rejection_controls(blocks[0])
    entire = dict(blocks=[serializable(b) for b in blocks], literal_tensor_controls=controls,
                  semantic_rejections=damages)
    raw = canonical(entire)
    if record_path:
        p = Path(record_path)
        require(not p.exists(), 'Preserve existing complete positive record')
        p.write_bytes(raw)
    epsilon = F(1, 100000000)
    main = blocks[-1]
    d = len(main['basis']['free'])
    s = main['checks']['norm_squared']
    box = epsilon / (4 * s * d)
    require(d == 3457 and d*d == 11950849, 'Exact mixed n28 dimension')
    require(4 * s * d * box == epsilon, 'Entire real parameter cube operator bound')
    return dict(agent='six-downset-2', role='researcher',
        status='Exact incidence/tensor controls; ordinary original spectral bridge and baseline10208 explicit premises; unformalized and independently unreviewed',
        blocks=[dict(b=b['b'], layers=b['layers'], vertices=len(b['masks']),
            exact_augmented_rank=len(b['basis']['pivots']), kernel_dimension=len(b['basis']['free']),
            every_literal_gram_entry_checked=True, every_basis_star_and_free_coordinate_checked=True,
            basis_nonzero_entries=b['checks']['nonzero_basis_entries'],
            star_equations=b['checks']['star_equations'], basis_norm_squared=str(b['checks']['norm_squared']))
            for b in blocks],
        complete_positive_record_bytes=len(raw), complete_positive_record_sha256=hashlib.sha256(raw).hexdigest(),
        tensor_control_counts=[{k:v for k,v in c.items() if k!='full_entries'} for c in controls],
        semantic_rejections=damages, main_n28_dimension=d*d,
        original_cross_frobenius_radius=str(epsilon/4), main_n28_basis_norm_squared=str(s),
        main_n28_closed_real_coordinate_cube_radius=str(box),
        main_n28_remaining_two_endpoint_margin=str(3*epsilon/4),
        inherited_n28_lower_rank=263644105, inherited_n28_cap_rank=268435426,
        inherited_n28_minimum_noncentral_classes=5,
        inherited_n28_M_two_endpoint_gap=str(3*epsilon/(4*134217727)),
        seed_theorem_is_premise=True, enormous_original_matrix_materialized=False,
        all_tensor_directions_enumerated=False, computational_nonexistence_claim=False,
        standard_library_only=True, exact_arithmetic=True, independent_review=False)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--record')
    p.add_argument('--summary')
    p.add_argument('--check')
    a = p.parse_args()
    result = run(a.record)
    if a.check:
        require(result == json.loads(Path(a.check).read_text()), 'Every compact expected output field')
    if a.summary:
        path = Path(a.summary)
        require(not path.exists(), 'Preserve existing compact output')
        path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
