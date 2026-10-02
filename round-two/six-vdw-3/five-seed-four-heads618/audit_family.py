#!/usr/bin/env python3
"""Audit every changed model against actual cyclic colors and literal units."""
import argparse
import itertools
import json
import time
from pathlib import Path
import check
import cover_check
import generate


def need(condition, message):
    if not condition:
        raise ValueError(message)


def audit(cover_path, work, helper_path):
    started = time.monotonic()
    work.mkdir(parents=True, exist_ok=True)
    coverage = cover_check.verify(cover_path)
    proposed = json.loads(cover_path.read_text())
    initial = dict(proposed['parent_relative_bits'])
    common = check.helper(helper_path)
    records, unit_inputs, unit_positives, damages_rejected = [], 0, 0, 0
    for entry in proposed['heads']:
        case = entry['number']
        wanted = dict(initial)
        added = dict(entry['additional_relative_bits'])
        need(not set(added).intersection(initial), 'New head overwrites a premise')
        wanted.update(added)
        path = work / ('case-'+str(case)+'.cnf')
        model = generate.generate(103,case,path)
        actual = check.audit(path,103,case,common)
        actual.pop('seconds',None)
        need(all(actual[k] == v for k,v in model.items()), 'Actual-cyclic audit differs')
        need(dict(model['fixed_core_bits']) == wanted and
             model['other_regular_bits_free'] == entry['other_orientation_bits_free'] and
             model['clauses'] == (27887 if case in (1,2) else 27889),
             'Changed head domain or extra restriction')
        _,core,_,_,_,index = check.parameters(103,case)
        rows = common.parse(path,4950)
        units = [row for row in rows if len(row) == 1]
        need(len(units) == len(wanted)-1, 'Wrong signed-unit count')
        for tail in itertools.product((0,1),repeat=len(core)-1):
            word = dict(zip(core,(0,)+tail))
            root_pairs = {index[(0,x)]:word[x] for x in core if x != 0}
            encoded = all(root_pairs[abs(row[0])] == int(row[0]>0) for row in units)
            literal = word == wanted
            need(encoded == literal, 'Literal signed-unit domain differs')
            unit_inputs += 1
            unit_positives += literal
        # Each repaired production damage remains parseable where possible.
        positive = next(row for row in rows if len(row) == 1 and row[0] > 0)
        triangle = next(row for row in rows if len(row) == 3)
        damaged = [set(rows)-{positive}|{(-positive[0],)},set(rows)-{positive},
                   set(rows)-{triangle},set(rows)|{(1,2)},sorted(rows)+[positive]]
        target = work/'damaged.cnf'
        for clauses in damaged:
            target.write_text('p cnf 4950 '+str(len(clauses))+'\n'+
                              ''.join(' '.join(map(str,row))+' 0\n' for row in clauses))
            try:
                check.audit(target,103,case,common)
            except ValueError:
                damages_rejected += 1
            else:
                raise ValueError('Damaged production model accepted')
        records.append({'number':case,'model':model,'audit':actual})
    need(len(records) == 4 and unit_inputs == 20480 and unit_positives == 4 and
         damages_rejected == 20, 'Incomplete production audit')
    result = {'coverage':coverage,'cases':records,'literal_unit_inputs_checked':unit_inputs,
              'positive_literal_unit_words':unit_positives,
              'common_actual_cyclic_pairs_checked':381306,
              'all_models_free_bits':[r['model']['other_regular_bits_free'] for r in records],
              'production_damages_rejected':damages_rejected,'seconds':time.monotonic()-started}
    (work/'family-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--helper',type=Path,required=True)
    a=p.parse_args()
    r=audit(a.cover,a.work,a.helper)
    print(json.dumps({k:v for k,v in r.items() if k != 'cases'}))
