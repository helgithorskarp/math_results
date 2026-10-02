"""Malformed original APs and invalid RUP records must reject in both Python modes."""
import argparse
import copy
import json
from pathlib import Path
import tempfile
from check_kernel import derive, symbol
from strict_rup import verify


def need(ok, message):
    if not ok:
        raise ValueError(message)


def controls(source):
    original = json.loads((source / 'AP_KERNEL.json').read_text())
    rejected = []
    for name in ['pole_AP', 'zero_step', 'outside_start', 'wrong_palette', 'missing_leaf',
                 'duplicate_leaf', 'root_removed', 'pole_changed']:
        data = copy.deepcopy(original)
        if name == 'pole_AP': data['ap_records'][0][0] = 0
        elif name == 'zero_step': data['ap_records'][0][1] = 0
        elif name == 'outside_start': data['ap_records'][0][0] = 310
        elif name == 'wrong_palette': data['ap_records'][0][2] = 2
        elif name == 'missing_leaf': data['ap_records'].pop()
        elif name == 'duplicate_leaf': data['ap_records'][0] = data['ap_records'][1][:]
        elif name == 'root_removed': data['roots'] = [1,2]
        elif name == 'pole_changed': data['pole'] = 1
        failed = False
        try: derive(data)
        except (ValueError, KeyError, IndexError): failed = True
        need(failed, 'malformed original-AP evidence accepted: ' + name)
        rejected.append(name)
    lines = (source / 'kernel.lrat').read_text().splitlines()
    with tempfile.TemporaryDirectory(prefix='vdw310-controls-') as name:
        path = Path(name)
        cnf, _ = derive(original)
        (path / 'input.cnf').write_bytes(cnf)
        for damage in ['negative_hint', 'unknown_hint', 'nonfresh_addition', 'outside_variable', 'missing_empty']:
            changed = lines[:]
            words = list(map(int, changed[0].split()))
            cut = words.index(0)
            if damage == 'negative_hint': words[cut + 1] = -abs(words[cut + 1])
            elif damage == 'unknown_hint': words[cut + 1] = 999999999
            elif damage == 'nonfresh_addition': words[0] = 1
            elif damage == 'outside_variable': words[1] = 56
            elif damage == 'missing_empty': changed.pop()
            if damage != 'missing_empty': changed[0] = ' '.join(map(str, words))
            (path / 'bad.lrat').write_text('\n'.join(changed) + '\n')
            failed = False
            try: verify(path / 'input.cnf', path / 'bad.lrat')
            except (ValueError, KeyError, IndexError): failed = True
            need(failed, 'invalid strict proof accepted: ' + damage)
            rejected.append(damage)
    undefined = False
    try: symbol(0)
    except ValueError: undefined = True
    need(undefined, 'character zero must stay undefined')
    return {'author': 'six-vdw-1', 'role': 'researcher', 'status': 'ALL_ORIGINAL_AP_AND_STRICT_PROOF_DAMAGES_REJECTED',
            'damages': rejected, 'rejected': len(rejected), 'undefined_character_rejected': undefined}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=Path(__file__).resolve().parent)
    a = p.parse_args()
    print(json.dumps(controls(a.source), sort_keys=True))
