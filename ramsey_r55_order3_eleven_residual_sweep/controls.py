#!/usr/bin/env python3
"""Full-formula mutation controls for the residual cube bridge."""
import argparse
import json
from pathlib import Path
import audit
import cube


def run(parent, work):
    work.mkdir(parents=True, exist_ok=True)
    sample = cube.cases()[0]
    correct = work/'correct.cnf'
    cube.make(parent, correct, sample['bits'])
    audit.check(parent, correct, sample['bits'])
    raw = correct.read_bytes()
    header, body = raw.split(b'\n', 1)
    head, last, empty = body.rsplit(b'\n', 2)
    cube.require(empty == b'', 'canonical final newline')
    literal = int(last.split()[0])
    mutants = dict(missing_unit=header+b'\n'+head+b'\n',
                   wrong_polarity=header+b'\n'+head+b'\n'+f'{-literal} 0\n'.encode(),
                   empty_clause=header+b'\n'+head+b'\n0\n',
                   wrong_parent=header+b'\n0\n'+body.split(b'\n', 1)[1],
                   extra_clause=raw+b'1 0\n')
    rejected = []
    for name, data in mutants.items():
        path = work/(name+'.cnf')
        path.write_bytes(data)
        try:
            audit.check(parent, path, sample['bits'])
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted malformed cube '+name)
        finally:
            path.unlink()
    correct.unlink()
    result = dict(rejected=rejected, core_variables=[abs(v) for v in audit.units('0'*18)],
                  complete_primary_count=320, verified=True)
    (work/'controls.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--parent', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(run(a.parent, a.work), sort_keys=True))
