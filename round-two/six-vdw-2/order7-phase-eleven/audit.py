"""Independent literal-field and whole eight-case maximum-gap encoding audit."""
import argparse
from collections import Counter
import itertools
import json
import math
from pathlib import Path
import resource
import time
from common import COMMIT, REF, pins, require, sha

PARAMETERS=[(m,b) for m in range(8,4,-1) for b in (0,1)]

def stem_for(m,b):return f'singleton8-maxgap-{m-1}-b-{b}'

def head_fixed(m,b):
    require((m,b) in PARAMETERS,'unsupported largest-gap head')
    return {i:(1-b if i in (0,m) else b) for i in [*range(m+2),43]}

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

def rules(fixed,free,background,m):
    names={i:45+len(free)+j for j,i in enumerate(free)}
    kinds={k:set() for k in ('two','fourth','singleton','maxgap')}
    truths={k:0 for k in kinds}
    schemes=[('two',(-1,0,1,2),(1-background,background,background,1-background)),
             ('fourth',(-1,0,1,3,4),(1-background,background,background,1-background,1-background)),
             ('singleton',(0,1),(background,background)),
             ('maxgap',tuple(range(m)),(1-background,)*m)]
    for origin in range(44):
        for kind,offsets,wanted in schemes:
            points=[(origin+j)%44 for j in offsets]
            satisfied=any(i in fixed and fixed[i]==v for i,v in zip(points,wanted))
            row=None if satisfied else tuple(sorted({names[i]*(1 if v else -1)
                        for i,v in zip(points,wanted) if i not in fixed}))
            if row is not None:kinds[kind].add(row)
            domain=sorted({names[i] for i in points if i not in fixed})
            for values in itertools.product((0,1),repeat=len(domain)):
                assignment=dict(zip(domain,values))
                selected=[(fixed[i] if i in fixed else assignment[names[i]])!=background for i in points]
                if kind=='singleton':correct=not(selected[0] and selected[1])
                elif kind=='maxgap':correct=any(selected)
                else:correct=selected[0] or not selected[1] or not selected[2] or any(selected[3:])
                actual=row is None or any(assignment[abs(v)]==(v>0) for v in row)
                require(actual==correct,'substituted '+kind+' rule differs from literal phase definition')
                truths[kind]+=1
    return kinds,truths

def audit_case(record,cnf,slots,supports):
    m,b=record['next_singleton'],record['background']
    fixed=head_fixed(m,b);free=[i for i in range(44) if i not in fixed];n=len(free);exact=8;levels=9
    require(record['stem']==stem_for(m,b) and record['fixed_phase_positions']=={str(i):v for i,v in fixed.items()}
            and record['free_phase_indices']==free and n==41-m and record['maximum_background_gap']==m-1
            and record['phase_K']==(34 if b else 10) and record['selected_phase_count']==10
            and record['free_selected_count']==exact and record['selected_anchor_count']==2
            and record['counter_levels']==levels and record['minimum_distance']==1
            and all(record[name] is True for name in ('root57_color_cut','only_global_y0_zero',
                'next_phase_after_singleton_fixed_background','actual_TWO_cut','actual_FOURTH4_cut',
                'actual_all_selected_singletons_cut','maximum_gap_normalization'))
            and all(record[name] is False for name in ('maximum_gap_rule_is_global_phase_restriction',
                'proposed_phase_TEN_exclusion','unpublished_exclusion_used_as_input','unrelated_family_cut'))
            and record['premise_ref']==REF and record['source_commit']==COMMIT,
            'changed largest-gap/count semantics or false premise')
    semantic=semantic_rows(slots,supports,fixed,free)
    conditional,truths=rules(fixed,free,b,m)
    semantic.update(conditional['two']|conditional['fourth'])
    variables=8+11*n
    lines=cnf.read_text().splitlines()
    require(record['variables']==variables and lines[0].split()==['p','cnf',str(variables),str(record['clauses'])],
            'wrong largest-gap counter dimension')
    rows=[]
    for line in lines[1:]:
        row=list(map(int,line.split()))
        require(row and row[-1]==0 and all(1<=abs(v)<=variables for v in row[:-1]),'invalid DIMACS row')
        rows.append(tuple(sorted(row[:-1])))
    counters={row for row in rows if any(abs(v)>44+2*n for v in row)}
    end,counter_truths=counter_check(counters,n,b,exact)
    require(end==variables and record['singleton_clauses']==len(conditional['singleton'])
            and record['new_singleton_clauses']==len(conditional['singleton']-(semantic|counters))>0,
            'wrong or omitted actual singleton clauses')
    core=semantic|counters|conditional['singleton']
    require(record['maximum_gap_clauses']==len(conditional['maxgap'])
            and record['new_maximum_gap_clauses']==len(conditional['maxgap']-core)
            and (m==8 or record['new_maximum_gap_clauses']>0),'wrong conditional maximum-gap window census')
    semantic.update(conditional['singleton']|conditional['maxgap'])
    require(Counter(rows)==Counter(list(semantic|counters)+[(-1,)]) and len(rows)==record['clauses']
            and sha(cnf)==record['cnf_sha256'],'full literal-field largest-gap CNF differs')
    return dict(stem=record['stem'],variables=variables,clauses=len(rows),cnf_sha256=sha(cnf),
                free_selected_count=exact,counter_truth_rows=counter_truths,rule_truth_rows=truths,
                singleton_clauses=len(conditional['singleton']),maximum_gap_clauses=len(conditional['maxgap']),
                new_singleton_clauses=record['new_singleton_clauses'],
                new_maximum_gap_clauses=record['new_maximum_gap_clauses'])

def composition_dp(length,total,bound):
    values=[1]+[0]*total
    for _ in range(length):
        values=[sum(values[t-g] for g in range(1,bound+1) if t>=g) for t in range(total+1)]
    return values[total]

def composition_ie(length,total,bound):
    if bound<1:return int(length==0 and total==0)
    if length==0:return int(total==0)
    excess=total-length
    if excess<0:return 0
    return sum((-1)**j*math.comb(length,j)*math.comb(excess-j*bound+length-1,length-1)
               for j in range(min(length,excess//bound)+1))

def ordinary_head_controls():
    """Coefficient checks supplement the ordinary cover; no enumeration of all field colorings."""
    records=[];labeled_total=0;marked_total=0
    for gap in range(4,8):
        bounded=composition_dp(10,34,gap);previous=composition_dp(10,34,gap-1)
        anchored=composition_dp(9,34-gap,gap)
        require(bounded==composition_ie(10,34,gap) and previous==composition_ie(10,34,gap-1)
                and anchored==composition_ie(9,34-gap,gap)>0,'independent largest-gap coefficients differ')
        numerator=44*(bounded-previous)
        require(numerator%10==0,'nonintegral necessary labeled phase count')
        labeled=numerator//10;marked=44*anchored
        labeled_total+=labeled;marked_total+=marked
        records.append(dict(maximum_background_gap=gap,anchored_max_gap_words_per_background=anchored,
                            labeled_phase_words_per_background=labeled,marked_max_gap_words_per_background=marked))
    require(composition_dp(10,34,3)==0 and labeled_total==50389724,'incomplete ordinary largest-gap catalogue')
    return dict(records=records,labeled_necessary_phase_words_per_background=labeled_total,
                marked_max_gap_words_per_background=marked_total,
                coverage_uses_ordinary_normalization_not_enumeration=True,
                multiple_maxima_retained=True,free_rotation_orbit_division=False,
                counts_are_not_feasible_field_colorings=True)

def tiny_controls():
    cells=counts=0
    for n in range(1,11):
        for bits in itertools.product((0,1),repeat=n):
            for flip in (0,1):
                prior={}
                for i,value in enumerate(bits,1):
                    for k in range(1,min(i,9)+1):
                        a=prior.get((i-1,k),False);b=True if k==1 else prior[i-1,k-1]
                        prior[i,k]=bool(a or ((value^flip) and b))
                        require(prior[i,k]==(sum(x^flip for x in bits[:i])>=k),'tiny threshold mismatch');cells+=1
                require((prior.get((n,8),False) and not prior.get((n,9),False))
                        ==(sum(x^flip for x in bits)==8),'tiny exact-eight count mismatch');counts+=1
    word_counts=Counter();marked_counts=Counter();normalizations=0;literal_words=0
    for n in range(5,13):
        for word in itertools.product((0,1),repeat=n):
            starts=[i for i,x in enumerate(word) if x]
            if len(starts)<2 or any(word[i] and word[(i+1)%n] for i in range(n)):continue
            gaps=[(starts[(j+1)%len(starts)]-p)%n-1 for j,p in enumerate(starts)]
            largest=max(gaps)
            if largest>7:continue
            k=len(starts);word_counts[n,k,largest]+=1;literal_words+=1
            for j,origin in enumerate(starts):
                if gaps[j]!=largest:continue
                m=largest+1;marked_counts[n,k,largest]+=1
                rotated=[word[(i+origin)%n] for i in range(n)]
                require(rotated[0]==rotated[m]==1 and all(rotated[i]==0 for i in range(1,m))
                        and rotated[m+1]==rotated[-1]==0,'tiny largest-gap head misses a word')
                windows=all(any(rotated[(i+j)%n] for j in range(m)) for i in range(n))
                require(windows and max(gaps)==m-1,'tiny maximum-gap window rule differs')
                for background in (0,1):
                    phase=[x^background for x in rotated]
                    fixed={0:1-background,m:1-background}|{i:background for i in (*range(1,m),m+1,n-1)}
                    require(all(phase[i]==v for i,v in fixed.items())
                            and sum(phase[i]!=background for i in range(n) if i not in fixed)==k-2,
                            'tiny both-background count/head normalization differs');normalizations+=1
    coefficient_checks=0
    for n in range(5,13):
        for k in range(2,n//2+1):
            for gap in range(1,8):
                total=n-k
                a=composition_dp(k,total,gap);b=composition_dp(k,total,gap-1)
                c=composition_dp(k-1,total-gap,gap) if total>=gap else 0
                require(a==composition_ie(k,total,gap) and b==composition_ie(k,total,gap-1)
                        and c==(composition_ie(k-1,total-gap,gap) if total>=gap else 0),
                        'tiny coefficient methods differ')
                require(k*word_counts[n,k,gap]==n*(a-b) and marked_counts[n,k,gap]==n*c,
                        'complete tiny cyclic/marked gap census differs');coefficient_checks+=1
    gauge=0
    for n in range(2,7):
        for bits in itertools.product((0,1),repeat=2*n):
            phase=[bits[i]^bits[i+n] for i in range(n)]
            for offset in range(2*n):
                values=[bits[(j+offset)%(2*n)]^bits[offset] for j in range(2*n)]
                require(values[0]==0 and all(values[i+n]==values[i]^phase[(i+offset)%n] for i in range(n)),
                        'scalar/global gauge mismatch');gauge+=1
    return dict(threshold_cells=cells,exact_counts=counts,literal_cyclic_words=literal_words,
                both_background_max_gap_normalizations=normalizations,coefficient_checks=coefficient_checks,
                signed_rotation_controls=gauge)

def main(work):
    began=time.monotonic();pins();models=json.loads((work/'models.json').read_text())
    require(models['producer_sha256']==sha(Path(__file__).with_name('generate.py')),'changed producer')
    require([r['stem'] for r in models['records']]==[stem_for(*p) for p in PARAMETERS]
            and {p.name for p in work.glob('*.cnf')}=={stem_for(*p)+'.cnf' for p in PARAMETERS},
            'incomplete eight-head maximum-gap cover')
    slots,supports=literal_field();records=[audit_case(r,work/(r['stem']+'.cnf'),slots,supports) for r in models['records']]
    tiny=tiny_controls();cover=ordinary_head_controls()
    out=dict(agent='six-vdw-2',role='researcher',status='EXACT_H7_SINGLETON8_DEFINITION_AUDIT',records=records,
        literal_APs=375760,removed_zero_APs=4312,signed_supports=26488,tiny_controls=tiny,
        ordinary_coverage_not_proved_by_tiny_controls=True,ordinary_max_gap_controls=cover,
        actual_singleton_premise=True,proposed_phase_TEN_exclusion_used=False,
        unpublished_exclusion_used_as_input=False,seconds=time.monotonic()-began,
        maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (work/('audit-normal.json' if __debug__ else 'audit-optimized.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);main(p.parse_args().work.absolute())
