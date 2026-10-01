"""Truth-classified checker controls and damaged real encoding/proof rejection."""
import argparse
from itertools import product
import json
from pathlib import Path

import field
from rup import need, verify


def write_cnf(path, n, rows):
    path.write_text(f'p cnf {n} {len(rows)}\n'+
                    ''.join(' '.join(map(str,row))+' 0\n' for row in rows))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--case-dir',type=Path,required=True)
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args()
    args.work.mkdir(parents=True,exist_ok=False)
    clauses=[(1,),(-1,),(2,),(-2,)]+list(product([1,-1],[2,-2]))
    accepted=rejected=0
    cnf,proof=args.work/'tiny.cnf',args.work/'tiny.lrat'
    for mask in range(256):
        rows=[clauses[k] for k in range(8) if mask>>k&1]
        write_cnf(cnf,2,rows)
        assignments=list(product([False,True],repeat=2))
        satisfied=lambda row,a:any(a[abs(z)-1]==(z>0) for z in row)
        sat=any(all(satisfied(row,a) for row in rows) for a in assignments)
        if sat:
            proof.write_text(f'{len(rows)+1} 0 1 0\n')
            try:verify(cnf,proof)
            except ValueError:rejected+=1
            else:raise ValueError('SAT formula accepted an empty-clause proof')
            continue
        records=[];next_id=len(rows)
        leaves={}
        for a in assignments:
            hint=next(i for i,row in enumerate(rows,1) if not satisfied(row,a))
            next_id+=1
            block=tuple(-i if value else i for i,value in enumerate(a,1))
            records.append(f'{next_id} '+ ' '.join(map(str,block))+f' 0 {hint} 0')
            leaves[a]=next_id
        parents=[]
        for first in [False,True]:
            next_id+=1
            literal=-1 if first else 1
            records.append(f'{next_id} {literal} 0 {leaves[first,False]} {leaves[first,True]} 0')
            parents.append(next_id)
        next_id+=1
        records.append(f'{next_id} 0 {parents[0]} {parents[1]} 0')
        proof.write_text('\n'.join(records)+'\n')
        verify(cnf,proof);accepted+=1
    need((accepted,rejected)==(161,95),'Truth-classified two-variable coverage')
    cycle_words=normalizations=window_checks=0
    for size in [3,5,7,9,11]:
        for word in product([0,1],repeat=size):
            cycle_words+=1
            boundaries=[i for i in range(size) if word[i]!=word[i-1]]
            if boundaries:
                gaps=[((boundaries[(j+1)%len(boundaries)]-start)%size,start)
                      for j,start in enumerate(boundaries)]
                length,start=max(gaps)
                need(2<=length<size,'Odd nonconstant cycle longest-run domain')
                normalized=[word[(start+j)%size]^word[start] for j in range(size)]
                need(normalized[:length]==[0]*length and normalized[-1]==normalized[length]==1,
                     'Complete longest-run normalization')
                normalizations+=1
            else:
                length=size
            for bound in range(1,size):
                mixed=all(len({word[(i+j)%size] for j in range(bound+1)})==2
                          for i in range(size))
                need(mixed==(length<=bound),'Independent cyclic-window equivalence')
                window_checks+=1
    supports,_=field.reconstruct()
    source=args.case_dir/'run-3.cnf'
    _,rows=field.clauses(source)
    corruptions=0
    def reject_cnf(changed):
        nonlocal corruptions
        write_cnf(cnf,77,changed)
        try:field.compare(3,cnf,supports)
        except ValueError:corruptions+=1
        else:raise ValueError('Altered complete case accepted')
    reject_cnf(rows[1:])
    reject_cnf(rows[:-1])
    reject_cnf(rows[:-1]+[(-77,)])
    changed=list(rows);changed[2*23177]=changed[2*23177+1]
    reject_cnf(changed)
    lines=(args.case_dir/'run-3.lrat').read_text().splitlines()
    index=next(i for i,line in enumerate(lines) if line.split()[1]!='d')
    words=lines[index].split();split=words.index('0')
    changes=[]
    for position,replacement in [(split+1,'999999999'),(split+1,'-'+words[split+1]),(1,'78')]:
        new=words.copy();new[position]=replacement
        altered=lines.copy();altered[index]=' '.join(new);changes.append(altered)
    changes += [lines[:-1], ['1 d 999999999 0']+lines,
                lines+[f'{int(lines[-1].split()[0])+1} 0 1 0']]
    for changed in changes:
        proof.write_text('\n'.join(changed)+'\n')
        try:verify(source,proof)
        except ValueError:corruptions+=1
        else:raise ValueError('Altered production proof accepted')
    need(corruptions==10,'Complete production corruption coverage')
    print(json.dumps({'agent':'six-reviewer-5','role':'independent reviewer',
                      'status':'INDEPENDENT_TRUTH_COVER_AND_CORRUPTION_CONTROLS_PASS',
                      'two_variable_families':256,'UNSAT_refutations_checked':accepted,
                      'SAT_forged_refutations_rejected':rejected,'odd_cycle_words':cycle_words,
                      'nonconstant_normalizations':normalizations,'window_equivalences':window_checks,
                      'production_corruptions_rejected':corruptions},indent=2))


if __name__=='__main__':
    main()
