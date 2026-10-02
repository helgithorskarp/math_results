"""Independent full literal-field, heterogeneous counter and unique-exterior audits."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import resource
import time
from common import COMMIT, REF, pins, require, sha

PARAMETERS=[(t,m,b) for t in (5,4) for m in (range(t+7,t,-1) if t!=3 else (4,)) for b in (0,1)]

def stem_for(t,m,b):return f'run45-t-{t}-next-{m}-b-{b}'

def head_fixed(t,m,b):
    require((t,m,b) in PARAMETERS,'unsupported unique-run head')
    return {i:(1-b if i<t or i==m else b) for i in [*range(m+2),43]}

def literal_field():
    require(all(617 % d for d in range(2,25)),'617 must be prime')
    require(len({pow(3,e,617) for e in range(616)})==616,'3 not primitive')
    h={pow(3,88*j,617) for j in range(7)}
    require(len(h)==7 and {pow(3,44,617)*v%617 for v in h}=={-v%617 for v in h},'wrong antipodal H7')
    slots={}
    for i in range(44):
        for side in (0,1):
            for v in h:
                x=(-1 if side else 1)*pow(3,i,617)*v%617
                require(x not in slots,'overlapping actual cosets');slots[x]=(i,side)
    require(set(slots)==set(range(1,617)),'incomplete actual field')
    supports=set();kept=removed=0
    for a in range(617):
        for d in range(1,617):
            points=[(a+j*d)%617 for j in range(7)]
            if 0 in points:removed+=1;continue
            kept+=1;edge=tuple(sorted({slots[x] for x in points}))
            require(len({i%2 for i,side in edge})==2,'QR control failed');supports.add(edge)
    require((kept,removed,len(supports))==(375760,4312,26488),'incomplete literal field AP census')
    return slots,supports

def rules(fixed,free,background,t):
    names={i:45+len(free)+j for j,i in enumerate(free)}
    rows=set();truths=0;outside=set();outside_truths=0
    for origin in range(44):
        for offsets,wanted,kind in [((-1,0,1,2),(1-background,background,background,1-background),'two'),
                                    ((-1,0,1,3,4),(1-background,background,background,1-background,1-background),'fourth'),
                                    ((0,1),(background,background),'outside')]:
            if kind=='outside' and origin in range(t-1):continue
            points=[(origin+j)%44 for j in offsets]
            true_constant=any(i in fixed and fixed[i]==v for i,v in zip(points,wanted))
            row=None if true_constant else tuple(sorted({names[i]*(1 if v else -1)
                for i,v in zip(points,wanted) if i not in fixed}))
            if row is not None:(outside if kind=='outside' else rows).add(row)
            domain=sorted({names[i] for i in points if i not in fixed})
            for values in itertools.product((0,1),repeat=len(domain)):
                assignment=dict(zip(domain,values))
                bits=[(fixed[i] if i in fixed else assignment[names[i]])!=background for i in points]
                correct=(not bits[0] or not bits[1]) if kind=='outside' else bits[0] or not bits[1] or not bits[2] or any(bits[3:])
                actual=row is None or any(assignment[abs(v)]==(v>0) for v in row)
                require(actual==correct,'substituted actual conditional/singleton rule differs')
                if kind=='outside':outside_truths+=1
                else:truths+=1
    return rows,outside,truths,outside_truths

def semantic_rows(slots,supports,fixed,free):
    n=len(free);index={i:j for j,i in enumerate(free)}
    def signed(i,side):
        return i+1 if not side else (i+1)*(-1 if fixed[i] else 1) if i in fixed else 45+index[i]
    rows=set()
    def both(values):
        values=set(values)
        if not any(-v in values for v in values):
            rows.add(tuple(sorted(values)));rows.add(tuple(sorted(-v for v in values)))
    for edge in supports:both([signed(i,side) for i,side in edge])
    for end in range(88):
        both([signed(*slots[pow(3,end-j,617)]) for j in range(7)])
        point=pow(3,end,617);both([signed(*slots[point*pow(57,j,617)%617]) for j in range(8)])
    for end in range(44):
        points=[(end-j)%44 for j in range(8)]
        for wanted in (0,1):
            if not any(i in fixed and fixed[i]==wanted for i in points):
                rows.add(tuple(sorted((45+n+index[i])*(1 if wanted else -1) for i in points if i not in fixed)))
    for i in free:
        variables=(i+1,45+index[i],45+n+index[i])
        for bits in itertools.product((0,1),repeat=3):
            if bits[2]!=(bits[0]^bits[1]):
                rows.add(tuple(sorted(-v if bit else v for v,bit in zip(variables,bits))))
    return rows

def counter_check(rows,n,background,exact):
    levels=exact+1;base=44+2*n
    cells={(i,k):base+(i*(i-1)//2 if i<=levels else levels*(i-1)-levels*(levels-1)//2)+k
           for i in range(1,n+1) for k in range(1,min(i,levels)+1)}
    end=base+levels*n-levels*(levels-1)//2
    require(set(cells.values())==set(range(base+1,end+1)),'incomplete analytic threshold labels')
    units={(cells[n,exact],),(-cells[n,levels],)}
    require({row for row in rows if len(row)==1}==units,'wrong heterogeneous exact-count units')
    accounted=set(units);truths=0
    for (i,k),output in cells.items():
        a=cells.get((i-1,k),False);b=True if k==1 else cells[i-1,k-1]
        value=(44+n+i)*(-1 if background else 1)
        local={row for row in rows if len(row)>1 and max(map(abs,row))==output}
        domain={abs(v) for v in (a,b,value,output) if not isinstance(v,bool)}
        require(local and all(set(map(abs,row))<=domain for row in local),'wrong gate domain/missing output')
        for bits in itertools.product((0,1),repeat=len(domain)):
            assignment=dict(zip(sorted(domain),bits))
            ev=lambda v:v if isinstance(v,bool) else assignment[abs(v)]^int(v<0)
            correct=bool(assignment[output])==bool(ev(a) or (ev(value) and ev(b)))
            require(all(any(ev(v) for v in row) for row in local)==correct,'wrong threshold recurrence gate')
            truths+=1
        accounted.update(local)
    require(accounted==rows,'unaccounted counter clause')
    return end,truths

def audit_case(record,cnf,slots,supports):
    t,m,b=record['long_run_length'],record['next_singleton'],record['background']
    fixed=head_fixed(t,m,b);free=[i for i in range(44) if i not in fixed];n=len(free);exact=9-t;levels=10-t
    require(record['stem']==stem_for(t,m,b) and record['fixed_phase_positions']=={str(i):v for i,v in fixed.items()}
            and record['free_phase_indices']==free and n==41-m and record['phase_K']==(34 if b else 10)
            and record['selected_phase_count']==10 and record['free_selected_count']==exact
            and record['selected_anchor_count']==t+1 and record['counter_levels']==levels
            and record['minimum_distance']==1 and record['root57_color_cut'] is True
            and record['only_global_y0_zero'] is True and record['next_phase_after_singleton_fixed_background'] is True
            and all(record[name] is True for name in ('actual_TWO_cut','actual_FOURTH4_cut','actual_at_most_one_long_run_cut'))
            and all(record[name] is False for name in ('proposed_global_no_adjacency_cut','proposed_no_run45_cut',
                'new_length6_exclusion_used_as_input','unrelated_family_cut'))
            and record['premise_ref']==REF and record['source_commit']==COMMIT,
            'changed ordinary unique-run semantics or false premise')
    semantic=semantic_rows(slots,supports,fixed,free)
    conditionals,outside,conditional_truths,outside_truths=rules(fixed,free,b,t)
    semantic.update(conditionals)
    variables=44+(2+levels)*n-levels*(levels-1)//2
    lines=cnf.read_text().splitlines()
    require(record['variables']==variables and lines[0].split()==['p','cnf',str(variables),str(record['clauses'])],
            'wrong heterogeneous variable dimension')
    rows=[]
    for line in lines[1:]:
        row=list(map(int,line.split()))
        require(row and row[-1]==0 and all(1<=abs(v)<=variables for v in row[:-1]),'invalid DIMACS row')
        rows.append(tuple(sorted(row[:-1])))
    counters={row for row in rows if any(abs(v)>44+2*n for v in row)}
    end,counter_truths=counter_check(counters,n,b,exact)
    require(end==variables and record['outside_singleton_clauses']==len(outside)
            and record['new_outside_singleton_clauses']==len(outside-(semantic|counters))>0,
            'wrong or omitted outside-singleton constraints')
    semantic.update(outside)
    require(Counter(rows)==Counter(list(semantic|counters)+[(-1,)]) and len(rows)==record['clauses']
            and sha(cnf)==record['cnf_sha256'],'full literal-field unique-run CNF differs')
    return dict(stem=record['stem'],variables=variables,clauses=len(rows),cnf_sha256=sha(cnf),
                free_selected_count=exact,counter_truth_rows=counter_truths,conditional_truth_rows=conditional_truths,
                outside_truth_rows=outside_truths,outside_singleton_clauses=len(outside),
                new_outside_singleton_clauses=record['new_outside_singleton_clauses'])

def tiny_controls():
    cells=counts=0
    for exact in (4,5,6):
        for n in range(1,11):
            for bits in itertools.product((0,1),repeat=n):
                for flip in (0,1):
                    prior={}
                    for i,value in enumerate(bits,1):
                        for k in range(1,min(i,exact+1)+1):
                            a=prior.get((i-1,k),False);b=True if k==1 else prior[i-1,k-1]
                            prior[i,k]=bool(a or ((value^flip) and b))
                            require(prior[i,k]==(sum(x^flip for x in bits[:i])>=k),'tiny threshold mismatch');cells+=1
                    require((prior.get((n,exact),False) and not prior.get((n,exact+1),False))
                            ==(sum(x^flip for x in bits)==exact),'tiny heterogeneous count mismatch');counts+=1
    exterior=0
    for n in range(8,14):
        for t in (3,4,5):
            for rest in itertools.product((0,1),repeat=n-t-2):
                word=[1]*t+[0]+list(rest)+[0]
                starts=[i for i in range(n) if word[i] and not word[(i-1)%n]]
                lengths=[]
                for i in starts:
                    length=0
                    while word[(i+length)%n]:length+=1
                    lengths.append(length)
                q=sum(length>=2 for length in lengths)
                direct=all(not(word[i] and word[(i+1)%n]) for i in range(n) if i not in range(t-1))
                require(direct==(q==1),'singleton exterior differs from unique prescribed long run');exterior+=1
    gauge=0
    for n in range(2,7):
        for bits in itertools.product((0,1),repeat=2*n):
            phase=[bits[i]^bits[i+n] for i in range(n)]
            for offset in range(2*n):
                values=[bits[(j+offset)%(2*n)]^bits[offset] for j in range(2*n)]
                require(values[0]==0 and all(values[i+n]==values[i]^phase[(i+offset)%n] for i in range(n)),
                        'scalar/global gauge mismatch');gauge+=1
    return cells,counts,exterior,gauge

def main(work):
    began=time.monotonic();pins();models=json.loads((work/'models.json').read_text())
    require(models['producer_sha256']==sha(Path(__file__).with_name('long_generate.py')),'changed producer')
    require([r['stem'] for r in models['records']]==[stem_for(*p) for p in PARAMETERS]
            and {p.name for p in work.glob('*.cnf')}=={stem_for(*p)+'.cnf' for p in PARAMETERS},'incomplete twenty-eight-head cover')
    slots,supports=literal_field();records=[audit_case(r,work/(r['stem']+'.cnf'),slots,supports) for r in models['records']]
    cells,counts,exterior,gauge=tiny_controls()
    out=dict(agent='six-vdw-2',role='researcher',status='EXACT_H7_RUN45_UNIQUE28_DEFINITION_AUDIT',records=records,
        literal_APs=375760,removed_zero_APs=4312,signed_supports=26488,tiny_threshold_cells=cells,
        tiny_exact_counts=counts,tiny_unique_exterior_controls=exterior,signed_rotation_controls=gauge,
        ordinary_coverage_not_proved_by_tiny_controls=True,proposed_global_no_adjacency_cut=False,
        proposed_no_run45_cut=False,new_length6_exclusion_used_as_input=False,
        seconds=time.monotonic()-began,maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/('audit-normal.json' if __debug__ else 'audit-optimized.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);main(p.parse_args().work.absolute())
