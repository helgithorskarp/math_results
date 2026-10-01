"""Literal clauses and complete seven-level prefix-threshold truth checking."""
import argparse
from collections import Counter
import itertools
import json
import math
from pathlib import Path
import resource
import sys
import time

from common import pins,require,sha,endpoint_auditor
old = endpoint_auditor()
literal_field,expected_clauses,independent_fixed = old.literal_field,old.expected_clauses,old.independent_fixed


def counter_check(rows,n,background):
    base = 44+2*n
    cells = {(i,k):base+(i*(i-1)//2 if i<=7 else 7*(i-1)-21)+k
             for i in range(1,n+1) for k in range(1,min(i,7)+1)}
    end = base+7*n-21
    require(set(cells.values()) == set(range(base+1,end+1)),'incomplete counter cells')
    units = {(cells[n,6],),(-cells[n,7],)}
    require({row for row in rows if len(row)==1} == units,'wrong exact-six units')
    accounted = set(units)
    checked = 0
    for (i,k),output in cells.items():
        a = cells.get((i-1,k),False)
        b = True if k==1 else cells[i-1,k-1]
        value = (44+n+i)*(-1 if background else 1)
        local = {row for row in rows if len(row)>1 and max(map(abs,row))==output}
        domain = {abs(v) for v in (a,b,value,output) if not isinstance(v,bool)}
        require(local and all(set(map(abs,row))<=domain for row in local),
                'wrong gate domain or missing output')
        for bits in itertools.product((0,1),repeat=len(domain)):
            assignment = dict(zip(sorted(domain),bits))
            def ev(v):
                return v if isinstance(v,bool) else assignment[abs(v)]^int(v<0)
            relation = bool(assignment[output]) == bool(ev(a) or (ev(value) and ev(b)))
            require(all(any(ev(v) for v in row) for row in local)==relation,
                    'wrong seven-level gate truth relation')
            checked += 1
        accounted.update(local)
    require(accounted==rows,'unaccounted counter clause')
    return end,checked


def tiny_controls():
    thresholds = exact = 0
    for m in range(1,11):
        for bits in itertools.product((0,1),repeat=m):
            for flip in (0,1):
                cells = {}
                for i,value in enumerate(bits,1):
                    for k in range(1,min(i,7)+1):
                        a = cells.get((i-1,k),False)
                        b = True if k==1 else cells[i-1,k-1]
                        cells[i,k] = bool(a or ((value^flip) and b))
                        require(cells[i,k] == (sum(x^flip for x in bits[:i])>=k),
                                'tiny threshold differs')
                        thresholds += 1
                require((cells.get((m,6),False) and not cells.get((m,7),False))
                        == (sum(x^flip for x in bits)==6),'tiny exact-six differs')
                exact += 1
    return thresholds,exact


def main(work):
    began = time.monotonic()
    pins()
    models = json.loads((work/'models.json').read_text())
    expected = [(d,b) for d in range(4,2,-1) for b in (0,1)]
    require([r['stem'] for r in models['records']] ==
            [f'd-{d}-b-{b}' for d,b in expected],'incomplete closest-pair cover')
    require({p.name for p in work.glob('*.cnf')} ==
            {f'd-{d}-b-{b}.cnf' for d,b in expected},'missing or extra model file')
    slots,supports = literal_field()
    records = []
    for record,(distance,background) in zip(models['records'],expected):
        require(record['minimum_distance']==distance and record['background']==background
                and record['phase_K']==(36 if background else 8)
                and record['free_minority_count']==6,'changed branch semantics')
        fixed = independent_fixed(distance,background)
        free = [i for i in range(44) if i not in fixed]
        semantic,n = expected_clauses(slots,supports,fixed,distance)
        require(n==len(free)=={1:41,2:39,3:36,4:33}[distance] and
                record['free_phase_indices']==free,'wrong free phase domain')
        cnf = work/(record['stem']+'.cnf')
        text = cnf.read_text().splitlines()
        variables = 23+9*n
        require(text[0].split()==['p','cnf',str(variables),str(record['clauses'])]
                and record['variables']==variables,'wrong model dimension')
        rows = []
        for line in text[1:]:
            values = list(map(int,line.split()))
            require(values and values[-1]==0 and all(1<=abs(v)<=variables
                    for v in values[:-1]),'invalid DIMACS row')
            rows.append(tuple(sorted(values[:-1])))
        counters = {row for row in rows if any(abs(v)>44+2*n for v in row)}
        end,truth_rows = counter_check(counters,n,background)
        require(end==variables,'wrong analytic cell labeling')
        require(Counter(rows)==Counter(list(semantic|counters)+[(-1,)])
                and len(rows)==record['clauses'] and sha(cnf)==record['cnf_sha256'],
                'full actual-field model audit differs')
        records.append(dict(stem=record['stem'],variables=variables,
            clauses=len(rows),cnf_sha256=sha(cnf),counter_truth_rows=truth_rows,
            free_phase_inputs_before_cuts=math.comb(n,6)))
    thresholds,exact = tiny_controls()
    result = dict(agent='six-vdw-2',role='researcher',status='EXACT_ENDPOINT8_CLOSE_AUDIT',
        records=records,literal_APs=375760,removed_zero_APs=4312,signed_supports=26488,
        tiny_threshold_cells=thresholds,tiny_exact_counts=exact,
        seconds=time.monotonic()-began,maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path = work/('audit-optimized.json' if not __debug__ else 'audit-normal.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    main(parser.parse_args().work.absolute())
