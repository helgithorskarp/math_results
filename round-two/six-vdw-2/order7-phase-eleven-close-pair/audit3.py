"""Independent actual-field, conditional spacing-three, threshold and whole-CNF audit."""
import argparse
from collections import Counter
import itertools
import json
import math
from pathlib import Path
import resource
import time
from common import COMMIT, REF, ROOT, pins, require, sha

PARAMETERS=[0,1]
def stem_for(background):return f'eleven3-mindistance-3-b-{background}'
def head_fixed(background):
    require(background in PARAMETERS,'unsupported conditional background')
    return {i:(1-background if i in (0,3) else background) for i in [0,1,2,3,4,5,42,43]}

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

def spacing_rows(fixed,free,background):
    names={i:45+len(free)+j for j,i in enumerate(free)};rows=set();truths=0
    for origin in range(44):
        for distance in (1,2):
            points=[origin,(origin+distance)%44]
            satisfied=any(i in fixed and fixed[i]==background for i in points)
            row=None if satisfied else tuple(sorted(names[i]*(1 if background else -1) for i in points if i not in fixed))
            if row is not None:rows.add(row)
            domain=[names[i] for i in points if i not in fixed]
            for bits in itertools.product((0,1),repeat=len(domain)):
                assignment=dict(zip(domain,bits))
                selected=[(fixed[i] if i in fixed else assignment[names[i]])!=background for i in points]
                correct=not all(selected)
                actual=row is None or any(assignment[abs(v)]==(v>0) for v in row)
                require(actual==correct,'conditional spacing-three sign/substitution differs');truths+=1
    return rows,truths

def audit_case(record,cnf,slots,supports):
    background=record['background'];fixed=head_fixed(background)
    free=[i for i in range(44) if i not in fixed];n=len(free);variables=431
    semantic=semantic_rows(slots,supports,fixed,free)
    spacing,rule_truths=spacing_rows(fixed,free,background)
    lines=cnf.read_text().splitlines()
    require(lines[0].split()==['p','cnf','431',str(record['clauses'])],'wrong conditional branch dimensions')
    rows=[]
    for line in lines[1:]:
        values=list(map(int,line.split()))
        require(values and values[-1]==0 and all(1<=abs(v)<=variables for v in values[:-1]),'invalid conditional CNF row')
        rows.append(tuple(sorted(values[:-1])))
    counter={row for row in rows if any(abs(v)>44+2*n for v in row)}
    end,counter_truths=counter_check(counter,n,background,9)
    require(n==36 and end==431,'wrong conditional exact-nine counter dimension')
    core=semantic|counter
    expected=dict(stem=stem_for(background),background=background,phase_K=33 if background else 11,
        selected_phase_count=11,free_selected_count=9,selected_anchor_count=2,counter_levels=10,
        fixed_phase_positions={str(i):v for i,v in fixed.items()},free_phase_indices=free,
        minimum_selected_distance=3,normalized_selected_pair=[0,3],lower_orientation_variables=44,
        variables=variables,clauses=len(core|spacing)+1,cnf_sha256=sha(cnf),
        conditional_spacing_clauses=len(spacing),new_conditional_spacing_clauses=len(spacing-core),
        conditional_minimum_distance_rule=True,minimum_distance_rule_is_universal=False,
        only_global_y0_zero=True,root3_color_cut=True,root57_color_cut=True,nonconstant_phase8_cut=True,
        exact_TEN_rules_used=False,unpublished_exclusion_used_as_input=False,
        proposed_ELEVEN_exclusion_used=False,regular_spacing_exclusion_used_as_input=False,
        unrelated_family_cut=False,premise_ref=REF,source_commit=COMMIT,mathematical_exclusion=False)
    require(record==expected,'entire exact-eleven conditional phase/count/head/premise differs')
    require(Counter(rows)==Counter(list(core|spacing)+[(-1,)]) and len(rows)==record['clauses'],
            'whole literal-field conditional spacing-three CNF differs')
    return dict(stem=record['stem'],background=background,phase_K=record['phase_K'],variables=variables,
        clauses=len(rows),cnf_sha256=sha(cnf),free_selected_count=9,counter_truth_rows=counter_truths,
        conditional_spacing_truth_rows=rule_truths,conditional_spacing_clauses=len(spacing),
        new_conditional_spacing_clauses=len(spacing-core))

def ordinary_head_controls():
    # Shift distances3..8 by2 to positive compositions1..6.
    bounded=composition_dp(11,22,6);regular=composition_dp(11,11,5)
    anchored=composition_dp(10,21,6)
    require(bounded==composition_ie(11,22,6)==319683
            and regular==composition_ie(11,11,5)==1
            and anchored==composition_ie(10,21,6)==147940,'independent conditional spacing coefficients differ')
    labeled=44*(bounded-regular)//11
    require(44*(bounded-regular)%11==0 and labeled==1278728,'wrong exact-minimum-three labeled count')
    return dict(anchored_minimum_three_necessary_phase_words_per_background=anchored,
        labeled_minimum_three_necessary_phase_words_per_background=labeled,
        marked_distance_three_words_per_background=44*anchored,
        ordinary_cover_uses_selected_pair_at_a_minimum_distance=True,
        all_tied_minima_retained=True,no_free_rotation_orbit_division=True,
        counts_are_not_feasible_field_colorings=True,regular_spacing_exclusion_used_as_input=False)

def tiny_controls():
    cells=counts=words=normalizations=pair_truths=0
    for n in range(1,11):
        for bits in itertools.product((0,1),repeat=n):
            for background in (0,1):
                prior={}
                for i,value in enumerate(bits,1):
                    for k in range(1,min(i,10)+1):
                        a=prior.get((i-1,k),False);b=True if k==1 else prior[i-1,k-1]
                        prior[i,k]=bool(a or ((value^background) and b))
                        require(prior[i,k]==(sum(x^background for x in bits[:i])>=k),'tiny threshold recurrence failed');cells+=1
                require((prior.get((n,9),False) and not prior.get((n,10),False))
                        ==(sum(x^background for x in bits)==9),'tiny exact-nine count failed');counts+=1
    for n in range(6,13):
        for word in itertools.product((0,1),repeat=n):
            starts=[i for i,x in enumerate(word) if x]
            if len(starts)<2:continue
            distances=[(starts[(j+1)%len(starts)]-i)%n for j,i in enumerate(starts)]
            pairs=all(not(word[i] and word[(i+d)%n]) for i in range(n) for d in (1,2))
            require(pairs==(min(distances)>=3),'tiny all-origin pair rule is not minimum distance at least three');pair_truths+=1
            if min(distances)!=3 or max(distances)>8:continue
            words+=1
            for j,origin in enumerate(starts):
                if distances[j]!=3:continue
                rotated=[word[(i+origin)%n] for i in range(n)]
                fixed={i:int(i in (0,3)) for i in (*range(6),n-2,n-1)}
                require(all(rotated[i]==v for i,v in fixed.items()),'tiny minimum-pair head misses a phase')
                for background in (0,1):
                    phase=[value^background for value in rotated]
                    require(all(phase[i]==(v^background) for i,v in fixed.items())
                            and sum(phase[i]!=background for i in range(n) if i not in fixed)==len(starts)-2,
                            'tiny fixed head/free count loses a background');normalizations+=1
    return dict(threshold_cells=cells,exact_nine_counts=counts,all_origin_pair_truths=pair_truths,
        small_cyclic_minimum_three_words=words,both_background_minimum_pair_normalizations=normalizations)

def main(work):
    began=time.monotonic();pins();models=json.loads((work/'models.json').read_text())
    require(models['producer_sha256']==sha(ROOT/'generate3.py')
            and [r['stem'] for r in models['records']]==[stem_for(b) for b in PARAMETERS],
            'incomplete two-background minimum-distance-three cover')
    slots,supports=literal_field()
    records=[audit_case(record,work/(record['stem']+'.cnf'),slots,supports) for record in models['records']]
    out=dict(agent='six-vdw-2',role='researcher',status='EXACT_H7_ELEVEN3_DEFINITION_AUDIT',
        literal_field_APs=375760,omitted_zero_APs=4312,distinct_signed_supports=26488,
        records=records,ordinary_head_controls=ordinary_head_controls(),tiny_controls=tiny_controls(),
        seconds=time.monotonic()-began,maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    mode='normal' if __debug__ else 'optimized'
    (work/('audit-'+mode+'.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','ordinary_head_controls','tiny_controls')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    main(p.parse_args().work.absolute())
