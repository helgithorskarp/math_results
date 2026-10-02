#!/usr/bin/env python3
"""Focused exact positive controls and repaired-artifact/proof damages."""
import argparse
import copy
import itertools
import json
from pathlib import Path

import check
import check_extension
import check_witness


def require(condition,message):
    if not condition:
        raise ValueError(message)


def rejected(call,contains):
    try:
        call()
    except (ValueError,KeyError) as error:
        require(contains in str(error),'Damage failed for an unexpected reason: '+str(error))
        return
    raise ValueError('Damaged mathematical artifact accepted')


def generic(checker,work):
    kernel = check_extension.load_checker(checker)
    work.mkdir(parents=True,exist_ok=True)
    damaged_helper = work/'changed-checker.py'
    damaged_helper.write_bytes(checker.read_bytes()+b'\n')
    rejected(lambda:check_extension.load_checker(damaged_helper),'Changed credited strict checker pin')
    active = {}
    row_id = {}
    for x,y,p in ((1,2,4),(1,3,5),(2,3,6)):
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2:
                row = tuple(sorted(v if b == 0 else -v for v,b in zip((x,y,p),bits)))
                row_id[row] = len(active)+1
                active[len(active)+1] = row
    t = (-6,4,5)
    pos = tuple(sorted((*t,1)))
    neg = tuple(sorted((*t,-1)))
    hp = [row_id[tuple(sorted(r))] for r in ((1,-2,4),(1,-3,5),(2,3,-6))]
    hn = [row_id[tuple(sorted(r))] for r in ((-1,2,4),(-1,3,5),(-2,-3,-6))]
    kernel.check_addition(pos,hp,active)
    active[13] = pos
    kernel.check_addition(neg,hn,active)
    active[14] = neg
    kernel.check_addition(t,[13,14],active)
    inputs = consistent = 0
    for bits in itertools.product((0,1),repeat=6):
        inputs += 1
        valid = all(any(bits[abs(v)-1] == int(v > 0) for v in row) for row in list(active.values())[:12])
        if valid:
            consistent += 1
            require(any(bits[abs(v)-1] == int(v > 0) for v in t),'False triangle transport')
    require(consistent == 8,'Rooted triangle toy count')
    rejected(lambda:kernel.check_addition(pos,hp[:-1],active),'no checked propagation contradiction')
    rejected(lambda:kernel.check_addition(pos,[-hp[0]],active),'RAT hints')
    rejected(lambda:kernel.check_addition(t,[13],active),'no checked propagation contradiction')
    rejected(lambda:kernel.check_addition(t,[99999],active),'unknown or deleted hint')
    return {'complete_six_parity_inputs':inputs,'consistent_rooted_inputs':consistent,
            'explicit_triangle_additions_checked':3,'generic_proof_damages_rejected':4,
            'changed_checker_pin_rejected':1}


def census(source):
    data = json.loads((source/'census.json').read_text())
    damaged = copy.deepcopy(data)
    damaged['classes'] = damaged['classes'][:-1]
    damaged['representatives'] = damaged['representatives'][:-1]
    for key in ('eligible_seed_supports','distinct_regular_cores','locally_covered_cores','cores_without_field_seven'):
        damaged['total_'+key] = sum(c[key] for c in damaged['classes'])
    rejected(lambda:check.audit(damaged),'Affine quotient fails total count')
    damaged = copy.deepcopy(data)
    case = next(c for c in damaged['classes'] if c['lambda'] == 9)
    case['exceptional_cores'] = []
    case['cores_without_field_seven'] = 0
    case['locally_covered_cores'] += 1
    damaged['total_cores_without_field_seven'] -= 1
    damaged['total_locally_covered_cores'] += 1
    rejected(lambda:check.audit(damaged),'different complete record')
    return {'repaired_census_damages_rejected':2}


def witness(source):
    fixtures = json.loads((source/'witnesses.json').read_text())
    data = json.loads((source/'census.json').read_text())
    wanted = {(c['lambda'],tuple(row['core'])) for c in data['classes'] for row in c['exceptional_cores']}
    actual = {(w['lambda'],tuple(w['target_core'])) for w in fixtures}
    require(len(fixtures) == len(actual) == 4 and wanted == actual,'Incomplete constructive kernel coverage')
    damaged = copy.deepcopy(fixtures[0])
    damaged['orientation'] = '0'*100
    rejected(lambda:check_witness.audit(damaged),'constant field seven')
    damaged = copy.deepcopy(fixtures[0])
    damaged['regular_point_order'] = damaged['regular_point_order'][::-1]
    rejected(lambda:check_witness.audit(damaged),'Changed point order')
    damaged = copy.deepcopy(fixtures[0])
    damaged['orientation'] = damaged['orientation'][:-1]
    rejected(lambda:check_witness.audit(damaged),'Malformed orientation')
    return {'distinct_constructive_targets_covered':4,'witness_damages_rejected':3}


def extension(directory,work,checker):
    work.mkdir(parents=True,exist_ok=True)
    for name in ('compressed.cnf','full.cnf'):
        (work/name).write_bytes((directory/name).read_bytes())
    proof_lines = (directory/'extension.lrat').read_text().splitlines()
    # Remove the final target addition. All earlier additions stay sound.
    (work/'extension.lrat').write_text('\n'.join(proof_lines[:-1])+'\n')
    rejected(lambda:check_extension.check_extension(work,2,checker),'target clauses are not derived')
    # A positive-only proof cannot accept a RAT hint.
    tokens = proof_lines[0].split()
    zero = tokens.index('0')
    tokens[zero+1] = '-'+tokens[zero+1]
    (work/'extension.lrat').write_text(' '.join(tokens)+'\n'+'\n'.join(proof_lines[1:])+'\n')
    rejected(lambda:check_extension.check_extension(work,2,checker),'Nonpositive/empty proof hint')
    (work/'extension.lrat').write_text('\n'.join(proof_lines)+'\n')
    lines = (work/'compressed.cnf').read_text().splitlines()
    remove = next(i for i,line in enumerate(lines[1:],1) if len(line.split()) == 10)
    del lines[remove]
    header = lines[0].split()
    header[3] = str(int(header[3])-1)
    lines[0] = ' '.join(header)
    (work/'compressed.cnf').write_text('\n'.join(lines)+'\n')
    rejected(lambda:check_extension.check_extension(work,2,checker),'Compressed model differs')
    return {'production_extension_damages_rejected':3}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--category',choices=('generic','census','witness','extension'),required=True)
    parser.add_argument('--source',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--checker',type=Path,required=True)
    parser.add_argument('--directory',type=Path)
    parser.add_argument('--workdir',type=Path,required=True)
    args = parser.parse_args()
    if args.category == 'generic':
        result = generic(args.checker,args.workdir)
    elif args.category == 'census':
        result = census(args.source)
    elif args.category == 'witness':
        result = witness(args.source)
    else:
        require(args.directory is not None,'Extension control needs the valid harmonic model')
        result = extension(args.directory,args.workdir,args.checker)
    print(json.dumps(result))
