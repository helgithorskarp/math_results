"""Independent actual-field, conditional all-isolated maximum-gap, threshold and whole-CNF audit."""
import argparse
from collections import Counter
import itertools
import json
import math
from pathlib import Path
import resource
import time
from common import COMMIT, REF, ROOT, pins, require, sha

PARAMETERS=[(m,b) for m in range(8,4,-1) for b in (0,1)]

def stem_for(m,b):return f"eleven-singletons-maxgap-{m-1}-b-{b}"

def head_fixed(m,b):
    require((m,b) in PARAMETERS,"unsupported conditional maximum-gap head")
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

def rules(fixed,free,background,m):
    names={i:45+len(free)+j for j,i in enumerate(free)}
    kinds={k:set() for k in ('isolation','maxgap')};truths={k:0 for k in kinds}
    schemes=[('isolation',(0,1),(background,background)),
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
                correct=not all(selected) if kind=='isolation' else any(selected)
                actual=row is None or any(assignment[abs(v)]==(v>0) for v in row)
                require(actual==correct,'conditional '+kind+' sign/substitution differs');truths[kind]+=1
    return kinds,truths

def audit_case(record,cnf,slots,supports):
    m,b=record['next_selected'],record['background'];fixed=head_fixed(m,b)
    free=[i for i in range(44) if i not in fixed];n=len(free);variables=12*n-1
    semantic=semantic_rows(slots,supports,fixed,free)
    conditional,truths=rules(fixed,free,b,m)
    lines=cnf.read_text().splitlines()
    require(lines[0].split()==['p','cnf',str(variables),str(record['clauses'])],
            'wrong conditional exact-eleven maximum-gap dimension')
    rows=[]
    for line in lines[1:]:
        values=list(map(int,line.split()))
        require(values and values[-1]==0 and all(1<=abs(v)<=variables for v in values[:-1]),'invalid CNF row')
        rows.append(tuple(sorted(values[:-1])))
    counter={row for row in rows if any(abs(v)>44+2*n for v in row)}
    end,counter_truths=counter_check(counter,n,b,9)
    require(n==41-m and end==variables,'wrong conditional exact-nine prefix dimension')
    core=semantic|counter;isolation=conditional['isolation'];maxgap=conditional['maxgap']
    expected=dict(stem=stem_for(m,b),next_selected=m,maximum_background_gap=m-1,background=b,
        phase_K=33 if b else 11,selected_phase_count=11,free_selected_count=9,
        selected_anchor_count=2,counter_levels=10,
        fixed_phase_positions={str(i):v for i,v in fixed.items()},free_phase_indices=free,
        lower_orientation_variables=44,minimum_selected_distance_at_least=2,
        normalized_selected_pair=[0,m],variables=variables,clauses=len(core|isolation|maxgap)+1,cnf_sha256=sha(cnf),
        conditional_isolation_clauses=len(isolation),new_conditional_isolation_clauses=len(isolation-core),
        maximum_gap_clauses=len(maxgap),new_maximum_gap_clauses=len(maxgap-(core|isolation)),
        conditional_all_selected_isolated=True,isolation_rule_is_universal=False,
        maximum_gap_normalization=True,maximum_gap_rule_is_global_phase_restriction=False,
        next_phase_after_selected_fixed_background=True,only_global_y0_zero=True,
        root3_color_cut=True,root57_color_cut=True,nonconstant_phase8_cut=True,
        exact_TEN_rules_used=False,proposed_ELEVEN_exclusion_used=False,
        close_pair_lemma_used_as_native_cut=False,unpublished_exclusion_used_as_input=False,
        unrelated_family_cut=False,premise_ref=REF,source_commit=COMMIT,mathematical_exclusion=False)
    require(record==expected,'entire conditional exact-eleven head/count/rule/premise differs')
    require(len(isolation-core)>0 and (m==8 or len(maxgap-(core|isolation))>0),
            'missing distinct conditional restriction')
    require(Counter(rows)==Counter(list(core|isolation|maxgap)+[(-1,)]) and len(rows)==record['clauses'],
            'whole literal-field conditional maximum-gap CNF differs')
    return dict(stem=record['stem'],background=b,maximum_background_gap=m-1,phase_K=record['phase_K'],
        variables=variables,clauses=len(rows),cnf_sha256=sha(cnf),free_selected_count=9,
        counter_truth_rows=counter_truths,conditional_rule_truth_rows=truths,
        conditional_isolation_clauses=len(isolation),new_conditional_isolation_clauses=len(isolation-core),
        maximum_gap_clauses=len(maxgap),new_maximum_gap_clauses=len(maxgap-(core|isolation)))

def ordinary_head_controls():
    records=[];labeled_total=marked_total=0
    require(composition_dp(11,33,3)==composition_ie(11,33,3)==1,
            'wrong unique regular-gap boundary coefficient')
    for gap in range(4,8):
        bounded=composition_dp(11,33,gap);previous=composition_dp(11,33,gap-1)
        anchored=composition_dp(10,33-gap,gap)
        require(bounded==composition_ie(11,33,gap) and previous==composition_ie(11,33,gap-1)
                and anchored==composition_ie(10,33-gap,gap)>0,'independent maximum-gap coefficients differ')
        numerator=44*(bounded-previous)
        require(numerator%11==0,'nonintegral necessary labeled phase count')
        labeled=numerator//11;marked=44*anchored
        labeled_total+=labeled;marked_total+=marked
        records.append(dict(maximum_background_gap=gap,anchored_max_gap_words_per_background=anchored,
            labeled_phase_words_per_background=labeled,marked_max_gap_words_per_background=marked))
    require(labeled_total==4*(composition_ie(11,33,7)-1),'incomplete maximum-gap count cover')
    return dict(records=records,labeled_necessary_phase_words_per_background=labeled_total,
        marked_max_gap_words_per_background=marked_total,selected_positive_gaps=11,background_gap_sum=33,
        maximum_at_most_three_forces_regular_distance_four=True,close_pair_parent_eliminates_regular_boundary=True,
        coverage_uses_ordinary_normalization_not_enumeration=True,multiple_maxima_retained=True,
        free_rotation_orbit_division=False,counts_are_not_feasible_field_colorings=True,
        min_distance_two_existence_not_imposed_on_head_models=True,exact_TEN_rules_used=False)

def tiny_controls():
    cells=counts=pair_truths=window_truths=0
    for n in range(1,11):
        for bits in itertools.product((0,1),repeat=n):
            for flip in (0,1):
                prior={}
                for i,value in enumerate(bits,1):
                    for k in range(1,min(i,10)+1):
                        a=prior.get((i-1,k),False);b=True if k==1 else prior[i-1,k-1]
                        prior[i,k]=bool(a or ((value^flip) and b))
                        require(prior[i,k]==(sum(x^flip for x in bits[:i])>=k),'tiny threshold mismatch');cells+=1
                require((prior.get((n,9),False) and not prior.get((n,10),False))
                        ==(sum(x^flip for x in bits)==9),'tiny exact-nine mismatch');counts+=1
    word_counts=Counter();marked_counts=Counter();normalizations=literal_words=0
    for n in range(5,13):
        for word in itertools.product((0,1),repeat=n):
            starts=[i for i,x in enumerate(word) if x]
            if len(starts)<2:continue
            distances=[(starts[(j+1)%len(starts)]-p)%n for j,p in enumerate(starts)]
            isolated=all(not(word[i] and word[(i+1)%n]) for i in range(n))
            require(isolated==(min(distances)>=2),'tiny conditional isolation equivalence failed');pair_truths+=1
            gaps=[d-1 for d in distances];largest=max(gaps)
            for m in range(1,min(n,8)+1):
                windows=all(any(word[(i+j)%n] for j in range(m)) for i in range(n))
                require(windows==(largest<m),'tiny all-origin maximum-gap equivalence failed');window_truths+=1
            if not isolated or largest>7:continue
            k=len(starts);word_counts[n,k,largest]+=1;literal_words+=1
            for j,origin in enumerate(starts):
                if gaps[j]!=largest:continue
                m=largest+1;marked_counts[n,k,largest]+=1
                rotated=[word[(i+origin)%n] for i in range(n)]
                require(rotated[0]==rotated[m]==1 and all(rotated[i]==0 for i in range(1,m))
                        and rotated[m+1]==rotated[-1]==0,'tiny maximum-gap head misses a word')
                for background in (0,1):
                    phase=[x^background for x in rotated]
                    fixed={0:1-background,m:1-background}|{i:background for i in (*range(1,m),m+1,n-1)}
                    require(all(phase[i]==v for i,v in fixed.items())
                            and sum(phase[i]!=background for i in range(n) if i not in fixed)==k-2,
                            'tiny both-background normalized head/count differs');normalizations+=1
    coefficients=0
    for n in range(5,13):
        for k in range(2,n//2+1):
            for gap in range(1,8):
                total=n-k;a=composition_dp(k,total,gap);b=composition_dp(k,total,gap-1)
                c=composition_dp(k-1,total-gap,gap) if total>=gap else 0
                require(a==composition_ie(k,total,gap) and b==composition_ie(k,total,gap-1)
                        and c==(composition_ie(k-1,total-gap,gap) if total>=gap else 0),
                        'tiny independent coefficient methods differ')
                require(k*word_counts[n,k,gap]==n*(a-b) and marked_counts[n,k,gap]==n*c,
                        'complete tiny cyclic/marked gap census differs');coefficients+=1
    gauge=0
    for n in range(2,7):
        for bits in itertools.product((0,1),repeat=2*n):
            phase=[bits[i]^bits[i+n] for i in range(n)]
            for offset in range(2*n):
                values=[bits[(j+offset)%(2*n)]^bits[offset] for j in range(2*n)]
                require(values[0]==0 and all(values[i+n]==values[i]^phase[(i+offset)%n] for i in range(n)),
                        'scalar/global gauge mismatch');gauge+=1
    return dict(threshold_cells=cells,exact_nine_counts=counts,all_origin_isolation_truths=pair_truths,
        all_origin_max_gap_truths=window_truths,literal_cyclic_words=literal_words,
        both_background_max_gap_normalizations=normalizations,coefficient_checks=coefficients,
        signed_rotation_controls=gauge)

def actual_scalar_controls():
    truths=normalizations=independence=0
    for gap in range(4,8):
        parts=[gap];remaining=33-gap
        for j in range(10):
            value=min(gap,remaining-(9-j));require(value>=1,'sample positive gap cover failed')
            parts.append(value);remaining-=value
        require(remaining==0 and len(parts)==11 and sum(parts)==33 and max(parts)==gap,'wrong actual gap control')
        starts=[0]
        for g in parts[:-1]:starts.append(starts[-1]+g+1)
        require(starts[-1]+parts[-1]+1==44,'actual gap circle does not close')
        for background in (0,1):
            phases=[background^int(i in starts) for i in range(44)]
            for origin in range(88):
                require({(i+origin)%44 for i in range(44)}==set(range(44)),'scalar identifies lower colors')
                for i in range(44):
                    for bit in (0,1):
                        def literal(e):
                            e%=88;return bit^(phases[e%44] if e>=44 else 0)
                        require(literal(i+origin)^literal(i+origin+44)==phases[(i+origin)%44],
                                'actual scalar transport loses an antipodal exchange');truths+=1
                anchor=origin%44
                if anchor in starts and parts[starts.index(anchor)]==gap:
                    fixed=head_fixed(gap+1,background)
                    require(all(phases[(i+origin)%44]==v for i,v in fixed.items()),
                            'actual tied-maximum normalized head fails');normalizations+=1
            lower=[0]*44;lower[1]=1;upper=[v^f for v,f in zip(lower,phases)]
            require([v^w for v,w in zip(lower,upper)]==phases
                    and [(1-v)^(1-w) for v,w in zip(lower,upper)]==phases
                    and lower[0]!=lower[1],'unjustified lower-color identification');independence+=1
    return dict(actual_scalar_phase_truth_rows=truths,actual_tied_maximum_anchor_normalizations_including_side=normalizations,
        actual_lower_orientation_controls=independence,all44_lower_orientations_remain_independent=True)

def main(work):
    began=time.monotonic();pins();models=json.loads((work/'models.json').read_text())
    require(models['producer_sha256']==sha(ROOT/'generate.py'),'changed producer')
    require([r['stem'] for r in models['records']]==[stem_for(*p) for p in PARAMETERS]
            and {p.name for p in work.glob('*.cnf')}=={stem_for(*p)+'.cnf' for p in PARAMETERS},
            'incomplete eight-head conditional exact-eleven maximum-gap cover')
    slots,supports=literal_field()
    records=[audit_case(r,work/(r['stem']+'.cnf'),slots,supports) for r in models['records']]
    out=dict(agent='six-vdw-2',role='researcher',status='EXACT_H7_ELEVEN_SINGLETONS_DEFINITION_AUDIT',
        literal_APs=375760,removed_zero_APs=4312,signed_supports=26488,records=records,
        tiny_controls=tiny_controls(),ordinary_max_gap_controls=ordinary_head_controls(),
        actual_scalar_controls=actual_scalar_controls(),ordinary_coverage_not_proved_by_tiny_controls=True,
        conditional_isolation_premise=True,isolation_is_universal=False,exact_TEN_rules_used=False,
        proposed_ELEVEN_exclusion_used=False,close_pair_lemma_used_as_native_cut=False,
        unpublished_exclusion_used_as_input=False,seconds=time.monotonic()-began,
        maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    mode='normal' if __debug__ else 'optimized'
    (work/('audit-'+mode+'.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','tiny_controls','ordinary_max_gap_controls','actual_scalar_controls')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);main(p.parse_args().work.absolute())
