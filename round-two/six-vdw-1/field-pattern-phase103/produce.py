"""Generate positive five-packs; a failed proposal proves no absence."""
import argparse
import hashlib
import json
from pathlib import Path


def generate():
    q = 103
    bits = {r: int(pow(r, 51, q) != 1) for r in range(1, q)}
    labels = {r: sum(bits[(r-a) % q] << (2-j) for j, a in enumerate([1, 2, 4]))
              for r in range(1, q) if r not in [1, 2, 4]}
    supports = {}
    for start in range(q):
        for step in range(1, 52):
            points = tuple((start+j*step) % q for j in range(7))
            if any(r not in labels for r in points):
                continue
            physical = sum(1 << r for r in points)
            types = sum(1 << k for k in set(labels[r] for r in points))
            supports.setdefault(physical, (start, step, types))
    lines = []
    for word in range(0, 256, 2):
        candidates = [(mask, a, d) for mask, (a, d, types) in supports.items()
                      if word & types in [0, types]]
        chosen = None
        for variant in range(64):
            if variant == 0:
                ordered = sorted(candidates, key=lambda z: (z[2], z[1]))
            elif variant == 1:
                ordered = sorted(candidates, key=lambda z: (z[1]+6*z[2], z[2], z[1]))
            else:
                ordered = sorted(candidates, key=lambda z: hashlib.sha256(
                    (str(variant)+':'+str(z[0])).encode()).digest())
            occupied, pack = 0, []
            for mask, a, d in ordered:
                if mask & occupied:
                    continue
                pack.append((a, d))
                occupied |= mask
                if len(pack) == 5:
                    chosen = pack
                    break
            if chosen is not None:
                break
        if chosen is None:
            raise RuntimeError('positive proposal incomplete; no exclusion or optimum follows')
        lines.append(','.join(map(str, [word]+[x for pair in chosen for x in pair]))+'\n')
    return ''.join(lines).encode()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('output', type=Path)
    a = p.parse_args()
    if a.output.exists():
        raise ValueError('fresh output required')
    data = generate()
    a.output.write_bytes(data)
    print(json.dumps({'author': 'six-vdw-1', 'role': 'researcher',
                      'status': 'POSITIVE_FIVE_PACKS_GENERATED_NOT_CHECKED',
                      'cases': 128, 'APs': 640, 'bytes': len(data),
                      'sha256': hashlib.sha256(data).hexdigest()}, sort_keys=True))
