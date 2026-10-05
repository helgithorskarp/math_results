"""Sage's separate exact controls of Lyra's uniform root-only obstruction."""

from pathlib import Path
import argparse
import hashlib
import itertools
import json
import platform
import resource
import time

from check_lyra_boundary import file_record, interleave, occurrences, require, scaffolds


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
    began = time.perf_counter()
    digest = hashlib.sha256()
    p = (2, 1, 4, 3, 7, 8, 5, 6)
    old = tuple(2 * x - 1 for x in p)
    counts = {'before': 0, 'after': 0}
    complete_stream = hashlib.sha256()
    for zero_rho in scaffolds(7):
        rho = tuple(x + 1 for x in zero_rho)
        gap = rho.index(7)
        if gap not in (4, 5):
            continue
        word = interleave(old, tuple(2 * x for x in rho))
        occ = occurrences(word)
        require(occ, 'Adjacent full root has an avoiding completion')
        counts['before' if gap == 4 else 'after'] += 1
        digest.update((json.dumps([rho, occ[0]], separators=(',', ':')) + '\n').encode())
        complete_stream.update((json.dumps([rho, occ], separators=(',', ':')) + '\n').encode())
    left = after = 0
    for m in range(8, 21):
        pi = (2, 1, 4, 3, m - 1, m) + tuple(range(5, m - 1))
        require(sorted(pi) == list(range(1, m + 1)), 'Family is not a permutation')
        band = tuple(2 * x for x in range(m - 5, m - 1))
        for markers in itertools.permutations(band):
            word = interleave((3, 1, 7, 5, 2 * m - 3), markers)
            occ = occurrences(word)
            require(occ, 'Before-case band certificate failed')
            left += 1
            digest.update((json.dumps([m, markers, occ[0]], separators=(',', ':')) + '\n').encode())
        for y in range(2, 2 * m - 3, 2):
            word = (2 * m - 3, y, 2 * m - 1, 2 * m - 2)
            require(occurrences(word) == ((0, 1, 2, 3),), 'After-case exact consecutive certificate failed')
            after += 1
    full = interleave(old, tuple(range(2, 15, 2)))
    require(full == (3, 2, 1, 4, 7, 6, 5, 8, 13, 10, 15, 12, 9, 14, 11), 'Named full witness differs')
    require(not occurrences(full), 'Named nonadjacent witness fails')
    require(tuple((x + 1) // 2 for x in full[::2]) == p, 'Recovery fails')
    require(tuple(x // 2 for x in full[1::2]) == tuple(range(1, 8)), 'Increasing scaffold differs')
    require(full[13] == 14 and full[9] != 14 and full[11] != 14, 'Largest even is not nonadjacent')
    expected = json.loads((root / 'root_adjacency_reproduction.json').read_text())
    require(counts == expected['adjacent_root_candidates_checked_at_m8'] and
            left == expected['before_arbitrary_left_orderings_m8_20'] and
            after == expected['after_possible_even_labels_m8_20'] and
            digest.hexdigest() == expected['ordered_witness_stream_sha256'], 'Author certificate stream differs')
    require({name: file_record(root / name) for name in before} == before, 'Source changed during check')
    report = {'author': 'literature-researcher-2', 'checker': 'literature-researcher-1',
              'proof_sha256': before['ROOT_ADJACENCY_OBSTRUCTION.md']['sha256'],
              'author_manifest_sha256': file_record(root / 'MANIFEST.json')['sha256'],
              'source_files': before, 'full_target_solved': False,
              'all_132_scaffolds_at_m8': len(scaffolds(7)),
              'adjacent_root_candidates': counts, 'arbitrary_before_cases': left, 'after_cases': after,
              'ordered_author_certificate_sha256': digest.hexdigest(),
              'complete_adjacent_occurrence_stream_sha256': complete_stream.hexdigest(),
              'valid_nonadjacent_full_word': full, 'rho': tuple(range(1, 8)),
              'python': platform.python_version(), 'seconds': time.perf_counter() - began,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'source_files'}, indent=2))


if __name__ == '__main__':
    main()
