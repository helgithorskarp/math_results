"""Independent literal definition audit of the complete longest-run8..14 cover."""
import argparse
from collections import Counter
import json
from pathlib import Path
import resource
import sys
import time

from common import pins,require,sha


def main(work):
    began = time.monotonic()
    pins()
    subgroup = {pow(3,88*j,617) for j in range(7)}
    ids = {}
    for i in range(88):
        for h in subgroup:
            x = pow(57,i,617)*h % 617
            require(x not in ids,'overlapping literal cosets')
            ids[x] = i
    require(set(ids)==set(range(1,617)) and
            len({pow(57,i,617) for i in range(616)})==616,'invalid root/cosets')
    supports = set()
    retained = removed = 0
    for a in range(617):
        for d in range(1,617):
            terms = [(a+j*d)%617 for j in range(7)]
            if 0 in terms:removed+=1;continue
            retained+=1;supports.add(tuple(sorted({ids[x] for x in terms})))
    require((retained,removed,len(supports))==(375760,4312,26488),'wrong AP census')
    critical = [(494+j*287)%617 for j in range(7)]
    require([ids[x] for x in critical]==[1,2,0,12,0,14,4]
            and 0 not in critical,'missing explicit longest-run bound')
    for scalar in (pow(57,r,617) for r in range(88)):
        images = [x*scalar%617 for x in critical]
        shift = ids[scalar]
        require([ids[x] for x in images]==[(v+shift)%88 for v in [1,2,0,12,0,14,4]],
                'scalar run coverage fails')
    field = []
    for edge in supports:
        values = tuple(i+1 for i in edge)
        field.extend((values,tuple(sorted(-v for v in values))))
    color = []
    for end in range(88):
        point = pow(57,end,617)
        values = tuple(sorted(ids[point*pow(3,-j,617)%617]+1 for j in range(7)))
        color.extend((values,tuple(sorted(-v for v in values))))
    meta = json.loads((work/'models.json').read_text())
    require([r['L'] for r in meta['records']]==list(range(8,15)),
            'incomplete longest-run cover')
    require({p.name for p in work.glob('*.cnf')}=={f'run-{k}.cnf' for k in range(8,15)},
            'missing or extra longest-run model')
    refs = {r['L']:r for r in meta['records']}
    records = []
    for length in range(8,15):
        expected = list(field)+list(color)
        for end in range(88):
            values = tuple(sorted(ids[pow(57,end-j,617)]+1 for j in range(length+1)))
            expected.extend((values,tuple(sorted(-v for v in values))))
        expected.extend((-i,) for i in range(1,length+1))
        expected.extend(((88,),(length+1,)))
        cnf = work/f'run-{length}.cnf'
        lines = cnf.read_text().splitlines()
        require(lines[0].split()==['p','cnf','88',str(53330+length)],'wrong longest-run header')
        actual = []
        for line in lines[1:]:
            values = list(map(int,line.split()))
            require(values and values[-1]==0 and all(1<=abs(v)<=88 for v in values[:-1]),
                    'invalid literal')
            actual.append(tuple(sorted(values[:-1])))
        require(Counter(actual)==Counter(expected),'complete literal-field/run clauses differ')
        require(sha(cnf)==refs[length]['cnf_sha256'] and refs[length]['variables']==88
                and refs[length]['clauses']==len(actual), 'changed model metadata')
        records.append(dict(L=length,variables=88,clauses=len(actual),cnf_sha256=sha(cnf),
                            stem=f'run-{length}'))
    result = dict(agent='six-vdw-2',role='researcher',status='EXACT_ROOT57_RUN_COVER_AUDIT',
        records=records,critical_AP=critical,critical_labels=[ids[x] for x in critical],
        actual_APs=retained,removed_zero_APs=removed,
        source_sha256=sha(Path(__file__)),seconds=time.monotonic()-began,
        maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    destination = work/('audit-optimized.json' if not __debug__ else 'audit-normal.json')
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    main(parser.parse_args().work.absolute())
