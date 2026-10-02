#!/usr/bin/env python3
"""Audit all fifteen signed-core instances after a complete input-cover check."""
import argparse
import json
import time
from pathlib import Path
from generate import generate
from check import audit,need
from cover_check import audit as audit_cover


def run(cover_path,work):
    started = time.monotonic()
    work.mkdir(parents=True,exist_ok=True)
    cover = json.loads(cover_path.read_text())
    coverage = audit_cover(cover)
    hole_numbers = {(5,53,101):1,(5,53,102):2,(5,54,101):3}
    cases = []
    for number,record in enumerate(cover['cases'],1):
        h = tuple(record['holes'])
        need(h in hole_numbers,'Unexpected production hole representative')
        case,opposite = hole_numbers[h],record['unique_opposite_satellite']
        path = work/('case-'+str(case)+'-opposite-'+str(opposite)+'.cnf')
        model = generate(103,case,opposite,path)
        literal = audit(path,103,case,opposite)
        for key,value in model.items():
            need(literal[key] == value,'Full model/audit disagreement in '+key)
        need(model['fixed_core_bits'] == record['fixed_core_bits'] and model['regular_core'] == record['regular_core'],'Fixed-word model does not represent its input-cover class')
        need(model['other_regular_bits_free'] == 90 and model['fixed_core_units'] == 9,'Incorrect free/fixed domain')
        cases.append({'number':number,'case':case,'opposite':opposite,'path':str(path),'model':model,
                      'audit':{k:v for k,v in literal.items() if k != 'seconds'}})
    need(len(cases) == 15,'Incomplete production family')
    result = {'agent':'six-vdw-3','role':'researcher','status':'ALL_FIFTEEN_MODELS_AND_INPUT_COVER_LITERAL_AUDITED',
              'coverage':coverage,'cases':cases,'distinct_hole_bases_actually_enumerated':3,
              'actual_cyclic_pairs_enumerated_for_common_bases':3*381306,
              'fixed_word_cases_compared':15,'native_solver_invoked':False,'higher_density_lemma_proved':False,
              'seconds':time.monotonic()-started}
    (work/'family-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--workdir',type=Path,required=True)
    a = p.parse_args()
    r = run(a.cover,a.workdir)
    print(json.dumps({k:v for k,v in r.items() if k != 'cases'}))
