"""Optional entrywise comparison with the pinned producer's public record.

This comparison is attribution evidence, not a hypothesis of the proof.
No producer module executes. Supply the original expected.json as a local file.
"""
import argparse
import hashlib
import json
from pathlib import Path
from audit import scalar, need

EXPECTED_SHA256 = 'a1e2f9849e8377b132264620a21a159d41261d5c32aa8825e856e5051d257e9b'
HERE = Path(__file__).resolve().parent


def compare(producer_bytes):
    need(hashlib.sha256(producer_bytes).hexdigest() == EXPECTED_SHA256,
         'pinned producer record bytes')
    producer = json.loads(producer_bytes)
    independent = json.loads((HERE/'expected.json').read_text())
    need(len(producer['profiles']) == len(independent['profiles']) == 3,
         'three representative profiles')
    count = 0
    for p, q in zip(producer['profiles'], independent['profiles']):
        need(p['axis'] == q['axis'], 'actual marked profile')
        need(len(p['physical_moment_matrix']) == len(q['moment']) == 3,
             'three physical moment rows')
        for a, b in zip(p['physical_moment_matrix'], q['moment']):
            need(len(a) == len(b) == 3, 'three physical moment columns')
            for x, y in zip(a, b):
                need(scalar(x) == scalar(y), 'physical moment entry')
                count += 1
        need(scalar(p['bilinear_planar_determinant']) == scalar(q['planar_det']),
             'physical planar determinant')
        count += 1
        need(len(p['fans']) == len(q['fans']), 'all closed receiving fans')
        for a, b in zip(p['fans'], q['fans']):
            need(a['fan'] == b['fan'], 'marked closed fan')
            for key, own_key, n in [('bilinear_corners', 'corners', 4), ('B', 'B', 3)]:
                need(len(a[key]) == len(b[own_key]) == n, 'complete physical entries')
                for x, y in zip(a[key], b[own_key]):
                    need(scalar(x) == scalar(y), 'literal physical fan scalar')
                    count += 1
            need(scalar(a['Kc']) == scalar(b['Kc']), 'retained translation drift')
            count += 1
    need(count == 398, 'complete comparison count')
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('producer_record', type=Path)
    args = parser.parse_args()
    print('PASS', compare(args.producer_record.read_bytes()), 'exact scalar comparisons')
