"""Independent gap census and complete forced endpoint phase-orbit audit."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import resource
import sys
import time
from common import pins,require,sha,endpoint_auditor
old = endpoint_auditor()

def main(work):
    began=time.monotonic();pins()
    # Independent bounded census: u_j=6-g_j, sum u=12 and0<=u<=6.
    # Every maximum gap6 must be followed by gap0.
    rooted=[];candidates=0
    for extras in itertools.combinations_with_replacement(range(8),12):
        deficits=tuple(extras.count(j) for j in range(8))
        if max(deficits)>6:continue
        candidates+=1
        gaps=tuple(6-u for u in deficits)
        if 6 not in gaps:continue
        if all(gaps[(j+1)%8]==0 for j,g in enumerate(gaps) if g==6):
            rooted.append(gaps)
    expected_gaps=(6,0,5,5,5,5,5,5)
    require(candidates==44052 and len(rooted)==8 and
            set(rooted)=={expected_gaps[j:]+expected_gaps[:j] for j in range(8)},
            'complete forced-gap census differs')
    positions=(0,7,8,14,20,26,32,38)
    orbit={tuple(sorted((x+r)%44 for x in positions)) for r in range(44)}
    require(len(orbit)==44,'wrong forced phase orbit')
    for word in orbit:
        gaps=tuple((word[(j+1)%8]-word[j])%44-1 for j in range(8))
        require(sum(gaps)==36 and sum(x*x for x in gaps)==186 and
                any(gaps[j:]+gaps[:j]==expected_gaps for j in range(8)),
                'wrong literal forced phase orbit')
    data=json.loads((work/'models.json').read_text())
    stems=['forced-b-0','forced-b-1']
    require([r['stem'] for r in data['records']]==stems and
            {p.name for p in work.glob('*.cnf')}=={s+'.cnf' for s in stems},
            'incomplete signed equality cover')
    slots,supports=old.literal_field();records=[]
    for b,record in enumerate(data['records']):
        require(record['background']==b and record['phase_K']==(36 if b else 8)
                and record['minority_positions']==list(positions)
                and record['majority_gaps']==list(expected_gaps)
                and record['gap_square_sum']==186,'changed phase semantics')
        fixed={i:b^int(i in positions) for i in range(44)}
        require(sum(fixed.values())==record['phase_K'] and all(
            len({fixed[(i+j)%44] for j in range(8)})==2 for i in range(44)),
            'phase cut positive control failed')
        semantic,n=old.expected_clauses(slots,supports,fixed)
        require(n==0,'phase is not fully fixed')
        extra=set()
        for exponent in range(88):
            origin=pow(3,exponent,617)
            values=set()
            for j in range(8):
                i,side=slots[origin*pow(57,j,617)%617]
                values.add((i+1)*(-1 if side and fixed[i] else 1))
            if not any(-v in values for v in values):
                extra.add(tuple(sorted(values)))
                extra.add(tuple(sorted(-v for v in values)))
        cnf=work/(record['stem']+'.cnf');lines=cnf.read_text().splitlines()
        require(lines[0].split()==['p','cnf','44',str(record['clauses'])]
                and record['variables']==44,'orientation dimensions changed')
        rows=[]
        for line in lines[1:]:
            values=list(map(int,line.split()))
            require(values and values[-1]==0 and all(1<=abs(v)<=44
                    for v in values[:-1]),'malformed DIMACS row')
            rows.append(tuple(sorted(values[:-1])))
        require(Counter(rows)==Counter(list(semantic|extra)+[(-1,)]) and
                len(rows)==record['clauses'] and sha(cnf)==record['cnf_sha256'],
                'entire literal model differs')
        records.append(dict(stem=record['stem'],variables=44,clauses=len(rows),
                            cnf_sha256=sha(cnf)))
    result=dict(agent='six-vdw-2',role='researcher',status='EXACT_FORCED_PHASE_ORBIT_AUDIT',
        records=records,gap_census_candidates=44052,forced_rooted_gaps=8,
        labeled_phase_words_per_background=44,signed_phase_cover=88,
        literal_APs=375760,removed_zero_APs=4312,signed_supports=26488,
        seconds=time.monotonic()-began,maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/('audit-optimized.json' if not __debug__ else 'audit-normal.json')).write_text(
        json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    main(p.parse_args().work.absolute())
