"""Independent normalization and toy minimum-factorization scope controls.

Author: six-sorting-2, researcher. Imports no SAT solver or generator.
Finite controls complement the written general proof; they do not prove
the general transfer lemma or import an unproved K18 witness.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'fixture.json'


def columns(n):
    return tuple(sum(((mask >> i) & 1) << mask for mask in range(1 << n)) for i in range(n))


def sorted_columns(n):
    return tuple(sum((mask.bit_count() >= n - i) << mask for mask in range(1 << n)) for i in range(n))


def compare(values, pair):
    a, b = pair
    result = list(values)
    result[a], result[b] = values[a] & values[b], values[a] | values[b]
    return tuple(result)


def run(values, word):
    for pair in word:
        values = compare(values, pair)
    return values


def normalize(n, sections, permutation_after_first):
    frame = list(range(n))
    normalized = []
    end_frames = []
    for section, word in enumerate(sections):
        kept = []
        for a, b in word:
            x, y = frame[a], frame[b]
            kept.append((min(x, y), max(x, y)))
            frame[a], frame[b] = min(x, y), max(x, y)
        if section == 0:
            frame = [frame[i] for i in permutation_after_first]
        normalized.append(kept)
        end_frames.append(tuple(frame))
    return normalized, end_frames


def suffix_components_are_intervals(n, word):
    parents = list(range(n))
    def root(i):
        while parents[i] != i:
            i = parents[i]
        return i
    for a, b in reversed(word):
        parents[root(a)] = root(b)
        groups = {}
        for i in range(n):
            groups.setdefault(root(i), []).append(i)
        if any(group != list(range(min(group), max(group) + 1)) for group in groups.values()):
            return False
    return True


def toy_factorizations(size):
    n = 3
    input_columns, target = columns(n), sorted_columns(n)
    ordinary = tuple(itertools.combinations(range(n), 2))
    oriented = tuple(itertools.permutations(range(n), 2))
    permutations = tuple(itertools.permutations(range(n)))
    cases = correct = nonempty_suffixes = 0
    by_prefix_size = {}
    for prefix_size in range(size + 1):
        total_here = correct_here = 0
        for prefix in itertools.product(oriented, repeat=prefix_size):
            before_permutation = run(input_columns, prefix)
            for order in permutations:
                permuted = tuple(before_permutation[i] for i in order)
                for suffix in itertools.product(ordinary, repeat=size - prefix_size):
                    cases += 1
                    total_here += 1
                    if run(permuted, suffix) != target:
                        continue
                    correct += 1
                    correct_here += 1
                    if size == 3:
                        normalized, frames = normalize(n, (prefix, suffix), order)
                        all_gates = normalized[0] + normalized[1]
                        assert frames[-1] == tuple(range(n))
                        assert run(input_columns, all_gates) == target
                        live = input_columns
                        for gate in all_gates:
                            assert compare(live, gate) != live, 'A minimum normalized comparator was redundant'
                            live = compare(live, gate)
                        assert suffix_components_are_intervals(n, suffix)
                        nonempty_suffixes += bool(suffix)
        by_prefix_size[str(prefix_size)] = dict(factorizations=total_here, correct_sorters=correct_here)
    assert cases == (378 if size == 2 else 2430)
    if size == 2:
        assert correct == 0
    else:
        assert correct > 0 and nonempty_suffixes > 0
    return dict(comparators=size, factorizations=cases, correct_sorters=correct,
                nonempty_suffix_controls=nonempty_suffixes, by_prefix_size=by_prefix_size)


def audit():
    if not __debug__:
        raise RuntimeError('Run without Python optimization')
    start = time.monotonic()
    f = json.loads(SOURCE.read_text())
    assert f['known_eleven_input_lower_bound'] == 35 and f['tested_K_budget'] == 18
    assert len(f['prefix']) == 14 and len(f['after']) == 3 and len(f['K_control20']) == 20
    norm, frames = normalize(11, (f['prefix'], f['after'], f['K_control20']), f['prefix_output_order'])
    assert frames[1] == (0, 1, 4, 2, 3, 7, 8, 5, 6, 9, 10)
    assert frames[2] == tuple(range(11))
    assert list(frames[1]) == f['initial_frame']
    assert norm[0] + norm[1] == list(map(tuple, f['normalized_prefix']))
    prefix = norm[0] + norm[1]
    assert len(prefix) == 17 and all(a < b for a, b in prefix + norm[2])
    inputs = columns(11)
    actual = run(inputs, f['prefix'])
    actual = tuple(actual[i] for i in f['prefix_output_order'])
    actual = run(actual, f['after'])
    standard = run(inputs, prefix)
    assert actual == tuple(standard[i] for i in frames[1])
    image = set()
    for mask in range(2048):
        values = [(column >> mask) & 1 for column in actual]
        assert values[10] == bool(mask)
        image.add(sum(v << i for i, v in enumerate(values[:10])))
    assert image == set(f['K_states']) and len(image) == 127
    actual_final = run(actual, f['K_control20'])
    normalized_final = run(standard, norm[2])
    assert actual_final == normalized_final == sorted_columns(11)
    assert suffix_components_are_intervals(11, f['K_control20'])
    small2, small3 = toy_factorizations(2), toy_factorizations(3)
    # Dropping the minimum-size hypothesis invalidates the general claim.
    prefix3, reverse, last = ((0, 1), (1, 2), (0, 1)), (2, 1, 0), ((0, 2),)
    sorted3 = run(columns(3), prefix3)
    assert sorted3 == sorted_columns(3)
    assert run(tuple(sorted3[i] for i in reverse), last) == sorted_columns(3)
    assert not suffix_components_are_intervals(3, last)
    negative_norm, negative_frames = normalize(3, (prefix3, last), reverse)
    assert negative_frames[-1] == (0, 1, 2)
    before_last = run(columns(3), negative_norm[0])
    assert run(before_last, negative_norm[1]) == before_last
    result = dict(agent='six-sorting-2', role='researcher',
                  status='TRANSFER_APPLICATION_FIXTURE_AND_TOY_SCOPE_CONTROLS_VERIFIED',
                  original_prefix_boolean_inputs=2048, original_K_control20_boolean_inputs=2048,
                  K_states=127, prefix_comparators=17, K18_full_comparators=35,
                  imported_S11=35, initial_frame=list(frames[1]), normalized_prefix=prefix,
                  normalized_control20=norm[2], positive_control_final_frame_identity=True,
                  positive_K20_suffix_intervals=True,
                  toy_lower_control=small2, toy_minimum_controls=small3,
                  nonminimum_counterexample_checked=True,
                  fixture_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  seconds=time.monotonic() - start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  trust_boundary='Written frame induction; imported S11=35 and published2015 terminal-block theorem. Toy checks are not the general proof.')
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    result = audit()
    certificate = json.loads((HERE / 'certificate.json').read_text())
    assert result['fixture_sha256'] == certificate['fixture_sha256']
    assert hashlib.sha256((HERE / 'interval_blocks.py').read_bytes()).hexdigest() == certificate['encoder_sha256']
    for key, value in certificate['fixture_controls'].items():
        assert result[key] == value, key
    if args.out:
        args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
