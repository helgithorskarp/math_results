#!/usr/bin/env python3
"""Exhaustive small positives and signed-unit/model damage checks."""
import argparse
import itertools
import json
from pathlib import Path
from generate import generate
from check import audit,small,parameters,parse,need


def controls(q,work):
    work.mkdir(parents=True,exist_ok=True)
    records = []
    damages = pair_inputs = valid_pairs = 0
    for case in ((1,2) if q in (7,11) else (1,2,3)):
        core = tuple(x for x in range(q) if x not in (0,1,case+1))[:3]
        for opposite in core[1:]:
            path = work/('case-'+str(case)+'-opposite-'+str(opposite)+'.cnf')
            model = generate(q,case,opposite,path)
            checked = audit(path,q,case,opposite)
            for key,value in model.items():need(checked[key] == value,'Small audit mismatch')
            enumeration = small(path,q,case,opposite)
            records.append({'model':model,'enumeration':enumeration})
            if q == 7:
                _,fixed,regular,pairs,index = parameters(q,case,opposite)
                rows = parse(path,len(pairs))
                for assignment in itertools.product((0,1),repeat=len(pairs)):
                    encoded = all(any(assignment[abs(x)-1] == int(x>0) for x in row) for row in rows)
                    values = {regular[0]:0}
                    for x in regular[1:]:values[x] = assignment[index[(regular[0],x)]-1]
                    consistent = all(assignment[index[(x,y)]-1] == values[x]^values[y] for x,y in pairs)
                    word_matches = all(values[x] == int(x==opposite) for x in fixed)
                    need(encoded == (consistent and word_matches),'Complete q7 signed-word/cycle truth mismatch')
                    pair_inputs += 1
                    valid_pairs += int(encoded)
            lines = path.read_text().splitlines()
            header = lines[0].split()
            variants = []
            parity = next(i for i,line in enumerate(lines[1:],1) if len(line.split()) == 4)
            damaged = lines[:parity]+lines[parity+1:]
            damaged[0] = 'p cnf '+header[2]+' '+str(int(header[3])-1)
            variants.append('\n'.join(damaged)+'\n')
            unit = next(i for i,line in enumerate(lines[1:],1) if len(line.split()) == 2 and int(line.split()[0]) > 0)
            damaged = lines[:unit]+lines[unit+1:]
            damaged[0] = 'p cnf '+header[2]+' '+str(int(header[3])-1)
            variants.append('\n'.join(damaged)+'\n')
            damaged = list(lines)
            damaged[unit] = '-'+damaged[unit]
            variants.append('\n'.join(damaged)+'\n')
            unit_variables = {abs(int(line.split()[0])) for line in lines[1:] if len(line.split()) == 2}
            extra = next(x for x in range(1,int(header[2])+1) if x not in unit_variables)
            variants.append('p cnf '+header[2]+' '+str(int(header[3])+1)+'\n'+'\n'.join(lines[1:])+'\n'+str(extra)+' 0\n')
            variants.append('p cnf '+str(int(header[2])+1)+' '+header[3]+'\n'+'\n'.join(lines[1:])+'\n')
            if any(len(line.split()) == 5 for line in lines[1:]):
                position = next(i for i,line in enumerate(lines[1:],1) if len(line.split()) == 5)
                tokens = lines[position].split()
                tokens[0] = str(-int(tokens[0]))
                damaged = list(lines)
                damaged[position] = ' '.join(tokens)
                variants.append('\n'.join(damaged)+'\n')
            for text in variants:
                bad = work/'damaged.cnf'
                bad.write_text(text)
                try:audit(bad,q,case,opposite)
                except ValueError:damages += 1
                else:raise ValueError('Damaged signed-core model accepted')
    return {'q':q,'cases':records,'anchored_orientation_inputs':sum(x['enumeration']['anchored_inputs'] for x in records),
            'positive_partial_words':sum(x['enumeration']['valid_partial_words'] for x in records),
            'small_models':len(records),'model_damages_rejected':damages,
            'complete_q7_pair_inputs':pair_inputs,'consistent_q7_fixed_word_inputs':valid_pairs,
            'general_prime_density_lemma_assumed':False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--q',type=int,choices=(7,11,13),required=True)
    p.add_argument('--workdir',type=Path,required=True)
    a = p.parse_args()
    print(json.dumps(controls(a.q,a.workdir)))
