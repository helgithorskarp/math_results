#!/usr/bin/env python3
"""Complete small signed-word controls and model/witness damage guards."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import check
import generate


def need(condition,message):
    if not condition:
        raise ValueError(message)


def write_rows(path,n,rows):
    path.write_text('p cnf '+str(n)+' '+str(len(rows))+'\n'+
                    ''.join(' '.join(map(str,row))+' 0\n' for row in rows))


def run(work,helper_path):
    work.mkdir(parents=True,exist_ok=True)
    common = check.helper(helper_path)
    records = []
    model_damages = pair_inputs = consistent_fixed = decoded_positives = 0
    for q,cases in ((7,(1,2)),(11,(1,2)),(13,(1,2,3))):
        for case in cases:
            path = work/('q'+str(q)+'-case'+str(case)+'.cnf')
            model = generate.generate(q,case,path)
            audited = check.audit(path,q,case,common)
            need(all(audited[key] == value for key,value in model.items()),
                 'Small independent audit differs from generator')
            _,core,opposite,regular,pairs,index = check.parameters(q,case)
            rows = common.parse(path,len(pairs))
            positives = []
            inputs = 0
            for tail in itertools.product((0,1),repeat=len(regular)-1):
                bits = (0,)+tail
                values = dict(zip(regular,bits))
                parities = [values[x]^values[y] for x,y in pairs]
                encoded = all(any(parities[abs(v)-1] == int(v>0) for v in row)
                              for row in rows)
                direct,_ = check.literal(q,case,bits)
                need(encoded == direct, 'Complete small model differs from literal cyclic condition')
                if direct:
                    positives.append(''.join(map(str,bits)))
                    signed = [(j+1) if b else -(j+1) for j,b in enumerate(parities)]
                    need(check.decode(signed,q,case) == bits, 'Positive coboundary decoder failed')
                    decoded_positives += 1
                inputs += 1
            need(positives, 'No positive small control')
            if q == 7:
                for parities in itertools.product((0,1),repeat=len(pairs)):
                    encoded = all(any(parities[abs(v)-1] == int(v>0) for v in row)
                                  for row in rows)
                    signed = [(j+1) if b else -(j+1) for j,b in enumerate(parities)]
                    try:
                        bits = check.decode(signed,q,case)
                        direct,_ = check.literal(q,case,bits)
                    except ValueError:
                        direct = False
                    need(encoded == direct, 'Complete pair-input control failed')
                    consistent_fixed += direct
                    pair_inputs += 1
            # Repairs keep a syntactically valid CNF wherever possible, so the
            # guard must recognize the changed mathematical instance.
            ordered = sorted(rows)
            unit = next(row for row in ordered if len(row)==1 and row[0]>0)
            cycle = next(row for row in ordered if len(row)==3)
            changed = set(rows)-{unit} | {(-unit[0],)}
            damages = [changed, set(rows)-{unit}, set(rows)-{cycle},
                       ordered+[ordered[0]], set(rows)|{(-index[(regular[0],core[1])],
                                                       -index[(regular[0],core[2])])}]
            ladder = next((row for row in ordered if len(row)==4),None)
            if ladder is not None:
                damages.append(set(rows)-{ladder})
            else:
                damages.append(set(rows)|{(len(pairs)+1,)})
            for j,damaged in enumerate(damages):
                broken = work/'damaged.cnf'
                write_rows(broken,len(pairs),list(damaged))
                try:
                    check.audit(broken,q,case,common)
                except ValueError:
                    model_damages += 1
                else:
                    raise ValueError('Damaged model accepted: '+str((q,case,j)))
            wrong = work/'wrong-domain.cnf'
            write_rows(wrong,len(pairs)+1,ordered)
            try:
                check.audit(wrong,q,case,common)
            except ValueError:
                model_damages += 1
            else:
                raise ValueError('Changed variable domain accepted')
            records.append({'q':q,'case':case,'anchored_inputs':inputs,
                            'positive_partial_words':len(positives),
                            'positive_fixtures':positives[:3],
                            'positive_words_sha256':hashlib.sha256(('\n'.join(positives)+'\n').encode()).hexdigest()})
    return {'status':'COMPLETE_GENERIC_SIGNED_WORD_CONTROLS',
            'cases':records,'anchored_orientation_inputs':sum(x['anchored_inputs'] for x in records),
            'positive_partial_words':decoded_positives,
            'model_damages_rejected':model_damages,
            'complete_q7_pair_inputs':pair_inputs,
            'q7_consistent_fixed_word_inputs':consistent_fixed,
            'global_density_lemma_proved':False,'native_solver_invoked':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--helper',type=Path,required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.work,args.helper)))
