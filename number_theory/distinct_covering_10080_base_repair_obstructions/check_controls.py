"""Definition-level controls for integer phase sums and input validation.

Actual author six-covering-1, researcher. Exhaust all phase/omission choices
in three toy families, including actual covers and positive obstructions.
"""
from copy import deepcopy
import itertools
import json
from pathlib import Path
import tempfile
from check import load, physical_tables


def main():
    families = [(12, 4, 3, [2, 3, 4, 6, 12], [0, 1, 2, 0]),
                (24, 8, 3, [2, 3, 4, 6, 8], [1, 0, 3, 1, 2, 0, 0, 4]),
                (30, 10, 3, [2, 3, 5, 6, 10], [0, 1, 0, 2, 0, 1, 3, 0, 2, 0])]
    tested = covering = positive = 0
    for N, B, C, moduli, f in families:
        coefs, totals = physical_tables(N, B, C, moduli, f)
        for m in moduli:
            direct = [sum(f[x % B] for x in range(a, N, m)) for a in range(m)]
            if m % C and coefs[m] != direct:
                raise ValueError('Toy literal phase sums differ')
        options = [[None]+list(range(m)) for m in moduli]
        for phases in itertools.product(*options):
            tested += 1
            selected = [(a, m) for a, m in zip(phases, moduli) if a is not None]
            counts = [sum(x % m == a for a, m in selected) for x in range(N)]
            holes = [x for x in range(N) if not counts[x]]
            base_weight = sum(coefs[m][a] for a, m in selected if m % C)
            deficit = max(0, totals['weighted_gap']-base_weight)
            if (sum(f[x % B] for x in holes) < deficit
                    or len(holes) < (deficit+max(f)-1)//max(f)):
                raise ValueError('Toy weighted union bound failed')
            positive += deficit > 0
            covering += not holes
    if tested != 14784 or not covering or not positive:
        raise ValueError('Incomplete or vacuous toy controls')
    here = Path(__file__).resolve().parent
    obj = json.loads((here/'weights.json').read_text())
    malformed = []
    bad = deepcopy(obj); bad['vectors'][0]['nonzero_weights'][0][1] = True; malformed.append(bad)
    bad = deepcopy(obj); bad['vectors'][0]['nonzero_weights'][0][1] = -1; malformed.append(bad)
    bad = deepcopy(obj); bad['vectors'][0]['nonzero_weights'].insert(0, bad['vectors'][0]['nonzero_weights'][0]); malformed.append(bad)
    bad = deepcopy(obj); bad['vectors'][0]['expected']['tail_capacity'] += 1; malformed.append(bad)
    bad = deepcopy(obj); bad['vectors'][1] = deepcopy(bad['vectors'][2]); malformed.append(bad)
    bad = deepcopy(obj); bad['vectors'][1]['target'] = [80, 59]; malformed.append(bad)
    bad = deepcopy(obj); bad['vectors'].pop(); malformed.append(bad)
    bad = deepcopy(obj); bad['assignment_sha256'] = '0'*64; malformed.append(bad)
    rejected = 0
    with tempfile.TemporaryDirectory(prefix='covering-weight-controls-') as directory:
        path = Path(directory)/'invalid.json'
        for bad in malformed:
            path.write_text(json.dumps(bad))
            try:
                load(here/'near_cover.tsv', path)
            except ValueError:
                rejected += 1
            else:
                raise ValueError('Malformed certificate accepted')
    if rejected != 8:
        raise ValueError('Malformed input control count differs')
    print(json.dumps(dict(agent='six-covering-1', role='researcher',
                          status='COMPLETE_TOY_AND_MALFORMED_INPUT_CONTROLS_PASSED',
                          toy_families=3, phase_or_omission_vectors=tested,
                          actual_toy_covers=covering, positive_obstruction_vectors=positive,
                          malformed_certificates_rejected=rejected)))


if __name__ == '__main__':
    main()
