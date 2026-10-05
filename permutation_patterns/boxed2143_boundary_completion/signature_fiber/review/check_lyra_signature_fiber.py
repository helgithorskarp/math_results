"""Sage's independent all-interval controls of Lyra's separate guard fiber."""

from pathlib import Path
import argparse
import hashlib
import importlib.util
import itertools
import json
import platform
import resource
import sys
import time

from check_lyra_boundary import file_record, occurrences, require


def image_by_residues(p, k):
    stride = 2 * k + 1
    end = stride * len(p) - 2 * k
    targets = tuple(range(1, end + 1, stride))
    front = tuple(x for x in range(1, end + 1) if (x - 1) % stride > k)
    back = tuple(x for x in range(1, end + 1) if 1 <= (x - 1) % stride <= k)
    return front + tuple(targets[i-1] for i in p) + back


def signature_by_positions(word, k):
    rows = []
    for low in range(1, len(word) + 1):
        for high in range(low, len(word) + 1):
            indices = tuple(i for i, x in enumerate(word) if low <= x <= high)
            rows.append((tuple(word[i] for i in indices[:k]), tuple(word[i] for i in indices[-k:])))
    return tuple(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.author_dir.resolve()
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    before = {row['path']: file_record(root / row['path']) for row in manifest['files']}
    require(all(before[row['path']] == {'size': row['size'], 'sha256': row['sha256']}
                for row in manifest['files']), 'Author packet changed')
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location('reviewed_lyra_guard_map', root / 'check_boundary_fiber.py')
    require(spec is not None and spec.loader is not None, 'Cannot load author map functions')
    author = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    began = time.perf_counter()
    digest = hashlib.sha256()
    inputs = intervals = 0
    rows = []
    for k in (1, 2, 3):
        for m in range(1, 6):
            common = signature_by_positions(image_by_residues(tuple(range(1, m + 1)), k), k)
            count = avoiders = total_occ = 0
            seen = set()
            for p in itertools.permutations(range(1, m + 1)):
                word = image_by_residues(p, k)
                require(word == author.guard_map(p, k), 'Actual author map differs')
                require(sorted(word) == list(range(1, len(word) + 1)), 'Image alphabet differs')
                require(word not in seen, 'Recoverable image repeated')
                seen.add(word)
                offset = k * (m-1)
                require(tuple((x - 1)//(2*k+1)+1 for x in word[offset:offset+m]) == p,
                        'Middle decoder differs')
                actual = occurrences(word)
                expected = tuple(tuple(i+offset for i in entry) for entry in occurrences(p))
                require(actual == expected, 'Complete occurrence correspondence differs')
                signature = signature_by_positions(word, k)
                require(signature == common == author.interval_signature(word, k), 'Global signature differs')
                inputs += 1
                intervals += len(signature)
                count += 1
                avoiders += not actual
                total_occ += len(actual)
                digest.update((json.dumps([k, p, word, actual], separators=(',', ':'))+'\n').encode())
            rows.append({'k': k, 'm': m, 'output_length': (2*k+1)*m-2*k,
                         'inputs': count, 'avoiding_outputs': avoiders,
                         'total_occurrences': total_occ, 'common_signature_count': 1})
    expected_report = json.loads((root/'boundary_fiber_reproduction.json').read_text())
    require(rows == expected_report['rows'] and inputs == expected_report['inputs_k_m'] and
            intervals == expected_report['all_interval_entries_compared'] and
            digest.hexdigest() == expected_report['ordered_occurrence_map_sha256'],
            'Author complete map stream differs')
    pair = (image_by_residues((1, 2), 3), image_by_residues((2, 1), 3))
    require(pair[0] != pair[1] and not any(occurrences(w) for w in pair) and
            signature_by_positions(pair[0], 3) == signature_by_positions(pair[1], 3),
            'Two-avoider signature collision differs')
    require({name: file_record(root/name) for name in before} == before, 'Source changed during review')
    report = {'author': 'literature-researcher-2', 'checker': 'literature-researcher-1',
              'proof_sha256': before['BOUNDARY_FIBER_ENTROPY.md']['sha256'],
              'author_manifest_sha256': file_record(root/'MANIFEST.json')['sha256'],
              'source_files': before, 'full_target_solved': False,
              'inputs_k_m': inputs, 'all_interval_entries_compared': intervals,
              'rows': rows, 'ordered_occurrence_map_sha256': digest.hexdigest(),
              'two_avoiders_one_signature': pair, 'python': platform.python_version(),
              'seconds': time.perf_counter()-began,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('source_files','rows')}, indent=2))


if __name__ == '__main__':
    main()
