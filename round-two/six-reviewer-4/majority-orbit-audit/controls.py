"""Explicit semantic rejection controls, active under Python -O."""
import json
import tempfile
from pathlib import Path
from independent import audit, check_pack, color, legendre_bit, load_csv, require


def rejected(label, operation):
    try:
        operation()
    except ValueError:
        return label
    raise RuntimeError('damage accepted: ' + label)


def controls(groups):
    z = min(groups)
    pack = list(groups[z])
    labels = []
    for label, changed in (
        ('short-pack', pack[:-1]),
        ('zero-step', [(pack[0][0], 0)] + pack[1:]),
        ('step-out-of-range', [(pack[0][0], 618)] + pack[1:]),
        ('start-out-of-range', [(618, pack[0][1])] + pack[1:]),
        ('negative-start', [(-1, pack[0][1])] + pack[1:]),
        ('repeated-field-columns', [(pack[0][0], 103)] + pack[1:]),
        ('duplicate-support', [pack[0], pack[0]] + pack[2:]),
        ('free-root-entered', [(0, pack[0][1])] + pack[1:]),
    ):
        labels.append(rejected(label, lambda changed=changed: check_pack(z, changed)))
    incomplete = dict(groups)
    incomplete.pop(z)
    labels.append(rejected('missing-orbit', lambda: audit(incomplete)))
    extra = dict(groups)
    extra[(103, 0, 0)] = tuple(pack)
    labels.append(rejected('invalid-state', lambda: audit(extra)))
    labels.append(rejected('character-zero', lambda: legendre_bit(0)))
    labels.append(rejected('root-color', lambda: color(z, z[0])))
    # A complete but mixed pack: find a root-free replacement for the first AP.
    for start in range(618):
        points = [(start + i * pack[0][1]) % 618 for i in range(7)]
        if {x % 103 for x in points}.intersection((0, 1, z[0])):
            continue
        if len({color(z, x % 103, x % 6) for x in points}) > 1:
            changed = [(start, pack[0][1])] + pack[1:]
            labels.append(rejected('mixed-colors', lambda: check_pack(z, changed)))
            break
    else:
        raise RuntimeError('mixed damage construction failed')
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'damage.csv'
        for label, text in (
            ('wrong-schema', 't,a,b,slot,start,step,extra\n2,0,0,0,3,4,5\n'),
            ('duplicate-slot', 't,a,b,slot,start,step\n2,0,0,0,3,4\n2,0,0,0,5,6\n'),
            ('missing-slot', 't,a,b,slot,start,step\n2,0,0,1,3,4\n'),
            ('noninteger-input', 't,a,b,slot,start,step\n2,0,0,0,x,4\n'),
        ):
            path.write_text(text)
            labels.append(rejected(label, lambda: load_csv(path)))
    require(len(labels) == 17 and len(set(labels)) == 17, 'complete damages')
    return labels


if __name__ == '__main__':
    import sys
    labels = controls(load_csv(Path(sys.argv[1])))
    print(json.dumps({'status': 'ALL_SEMANTIC_DAMAGES_REJECTED', 'labels': labels}, sort_keys=True))
