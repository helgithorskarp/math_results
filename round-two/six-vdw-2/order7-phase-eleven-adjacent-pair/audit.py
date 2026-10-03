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

PAIR_STARTS=sorted(range(8,40),key=lambda j:(abs(j-22),j))+[7,40,5,42]
PARAMETERS=[(j,b) for j in PAIR_STARTS for b in (0,1)]

def stem_for(j,b):return f"eleven-gap4-pairs-j-{j}-b-{b}"

def head_fixed(j,b):
    require((j,b) in PARAMETERS,"unsupported conditional minimum-pair gap4 head")
    selected=(0,5,j,(j+2)%44)
    background=(1,2,3,4,6,43,(j-1)%44,(j+1)%44,(j+3)%44)
    require(set(selected).isdisjoint(background),'contradictory literal head')
    return {i:(1-b if i in selected else b) for i in range(44) if i in (*selected,*background)}

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
    j,b=record['minimum_pair_start'],record['background'];m=5;fixed=head_fixed(j,b)
    free=[i for i in range(44) if i not in fixed];n=len(free);known=sum(v!=b for v in fixed.values());exact=11-known
    variables=44+(exact+3)*n-exact*(exact+1)//2
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
    end,counter_truths=counter_check(counter,n,b,exact)
    require(end==variables and n in (31,32,34) and exact in (7,8),'wrong minimum-pair exact-count dimension')
    core=semantic|counter;isolation=conditional['isolation'];maxgap=conditional['maxgap']
    expected=dict(stem=stem_for(j,b),next_selected=m,maximum_background_gap=m-1,background=b,
        phase_K=33 if b else 11,selected_phase_count=11,free_selected_count=exact,
        selected_anchor_count=known,counter_levels=exact+1,
        minimum_pair_start=j,minimum_pair_selected_positions=[j,(j+2)%44],
        minimum_pair_background_positions=[(j-1)%44,(j+1)%44,(j+3)%44],
        conditional_minimum_pair_head=True,minimum_pair_rule_is_universal=False,
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
        gap_four_lemma_used_as_unconditional_native_cut=False,unpublished_exclusion_used_as_input=False,
        unrelated_family_cut=False,premise_ref=REF,source_commit=COMMIT,mathematical_exclusion=False)
    require(record==expected,'entire conditional exact-eleven head/count/rule/premise differs')
    require(len(isolation-core)>0 and (m==8 or len(maxgap-(core|isolation))>0),
            'missing distinct conditional restriction')
    require(Counter(rows)==Counter(list(core|isolation|maxgap)+[(-1,)]) and len(rows)==record['clauses'],
            'whole literal-field conditional maximum-gap CNF differs')
    return dict(stem=record['stem'],background=b,maximum_background_gap=m-1,phase_K=record['phase_K'],
        variables=variables,clauses=len(rows),cnf_sha256=sha(cnf),free_selected_count=exact,minimum_pair_start=j,
        counter_truth_rows=counter_truths,conditional_rule_truth_rows=truths,
        conditional_isolation_clauses=len(isolation),new_conditional_isolation_clauses=len(isolation-core),
        maximum_gap_clauses=len(maxgap),new_maximum_gap_clauses=len(maxgap-(core|isolation)))

def ordinary_head_controls():
    import hashlib
    forbidden={1,2,3,4,6,43}
    allowed=[j for j in range(44) if j not in forbidden and (j+2)%44 not in forbidden]
    require(allowed==[5,*range(7,41),42] and set(PAIR_STARTS)==set(allowed),'incomplete literal 36-pair domain')
    head_counts=Counter(); normalized_words=pair_markings=0; digest=hashlib.sha256()
    def tails(length,total):
        if not length:
            if total==0:yield ()
            return
        for value in range(1,5):
            remainder=total-value
            if length-1<=remainder<=4*(length-1):
                for rest in tails(length-1,remainder):yield (value,*rest)
    for tail in tails(10,29):
        gaps=(4,*tail)
        if min(gaps)!=1:continue
        positions=[0]
        for g in gaps[:-1]:positions.append(positions[-1]+g+1)
        require(positions[-1]+gaps[-1]+1==44,'literal gap word failed to close')
        selected=set(positions);word=[int(i in selected) for i in range(44)]
        require(word[0]==word[5]==1 and not any(word[i] for i in forbidden),'literal normalized maximum head failed')
        pairs=[j for j in positions if (j+2)%44 in selected]
        require(pairs and set(pairs)<=set(allowed),'literal minimum-pair cover missed normalized word')
        digest.update(bytes(word));normalized_words+=1
        for j in pairs:
            for b in (0,1):
                fixed=head_fixed(j,b);phase=[v^b for v in word]
                require(all(phase[i]==v for i,v in fixed.items())
                        and sum(phase[i]!=b for i in range(44) if i not in fixed)==11-sum(v!=b for v in fixed.values()),
                        'literal both-background minimum head/free count differs')
            head_counts[j]+=1;pair_markings+=1
    expected=composition_dp(10,29,4)-composition_dp(10,19,3)
    require(expected==composition_ie(10,29,4)-composition_ie(10,19,3)==normalized_words,'full normalized gap4 coefficient mismatch')
    unmarked=composition_dp(11,33,4)-composition_dp(11,22,3)
    require(unmarked==composition_ie(11,33,4)-composition_ie(11,22,3)==128865
            and 44*unmarked//11==515460,'full necessary labeled phase count mismatch')
    require(set(head_counts)==set(allowed),'empty or omitted pair head in literal necessary domain')
    return dict(allowed_pair_start_indices=allowed,heads_per_background=36,total_heads=72,
        normalized_max4_min1_words_per_background=normalized_words,marked_max_gap_words_per_background=44*normalized_words,
        minimum_pair_markings_per_normalized_background=pair_markings,full_ordered_normalized_word_sha256=digest.hexdigest(),
        head_counts_per_background=[dict(j=j,words=head_counts[j]) for j in allowed],
        necessary_labeled_phase_words_per_background=515460,both_backgrounds_checked=True,
        all_tied_maxima_and_minima_retained=True,ordinary_scalar_cover=True,free_orbit_division=False,
        counts_are_not_feasible_field_colorings=True,exact_TEN_rules_used=False)

def tiny_controls():
    cells=counts=literal_words=normalizations=0
    for exact in (7,8):
        for n in range(1,10):
            for bits in itertools.product((0,1),repeat=n):
                for flip in (0,1):
                    prior={}
                    for i,value in enumerate(bits,1):
                        for k in range(1,min(i,exact+1)+1):
                            a=prior.get((i-1,k),False);b=True if k==1 else prior[i-1,k-1]
                            prior[i,k]=bool(a or ((value^flip) and b))
                            require(prior[i,k]==(sum(x^flip for x in bits[:i])>=k),'tiny threshold mismatch');cells+=1
                    require((prior.get((n,exact),False) and not prior.get((n,exact+1),False))
                            ==(sum(x^flip for x in bits)==exact),'tiny exact-seven/eight mismatch');counts+=1
    for n in range(5,13):
        for word in itertools.product((0,1),repeat=n):
            starts=[i for i,x in enumerate(word) if x]
            if len(starts)<2:continue
            gaps=[(starts[(k+1)%len(starts)]-a)%n-1 for k,a in enumerate(starts)]
            if min(gaps)!=1 or max(gaps)>4:continue
            require(all(not(word[i] and word[(i+1)%n]) for i in range(n)),'tiny isolation mismatch')
            literal_words+=1;gap=max(gaps);m=gap+1
            require(all(any(word[(i+k)%n] for k in range(m)) for i in range(n)),'tiny gap windows mismatch')
            for k,a in enumerate(starts):
                if gaps[k]!=gap:continue
                rotated=[word[(i+a)%n] for i in range(n)]
                for j in range(n):
                    if not(rotated[j] and rotated[(j+2)%n]):continue
                    selected={0,m,j,(j+2)%n};background={*range(1,m),m+1,n-1,(j-1)%n,(j+1)%n,(j+3)%n}
                    require(not(selected & background),'tiny tied max/min head collides')
                    for b in (0,1):
                        phase=[v^b for v in rotated]
                        require(all(phase[i]==1-b for i in selected) and all(phase[i]==b for i in background),
                                'tiny both-background tied max/min normalization failed');normalizations+=1
    gauge=0
    for n in range(2,7):
        for bits in itertools.product((0,1),repeat=2*n):
            phase=[bits[i]^bits[i+n] for i in range(n)]
            for offset in range(2*n):
                values=[bits[(j+offset)%(2*n)]^bits[offset] for j in range(2*n)]
                require(values[0]==0 and all(values[i+n]==values[i]^phase[(i+offset)%n] for i in range(n)),
                        'scalar/global gauge mismatch');gauge+=1
    return dict(threshold_cells=cells,exact_seven_eight_counts=counts,literal_cyclic_words=literal_words,
        both_background_tied_max_min_normalizations=normalizations,signed_rotation_controls=gauge)

def actual_scalar_controls():
    truths=normalizations=independence=0
    parts=[4,1,4,4,4,4,4,2,2,2,2];require(sum(parts)==33 and len(parts)==11,'actual sample parts invalid')
    starts=[0]
    for g in parts[:-1]:starts.append(starts[-1]+g+1)
    for background in (0,1):
        phases=[background^int(i in starts) for i in range(44)]
        for origin in range(88):
            require({(i+origin)%44 for i in range(44)}==set(range(44)),'scalar identifies lower colors')
            for i in range(44):
                for bit in (0,1):
                    def literal(e):
                        e%=88;return bit^(phases[e%44] if e>=44 else 0)
                    require(literal(i+origin)^literal(i+origin+44)==phases[(i+origin)%44],
                            'actual scalar transport loses antipodal exchange');truths+=1
            anchor=origin%44
            if anchor in starts and parts[starts.index(anchor)]==4:
                phase=[phases[(i+origin)%44] for i in range(44)]
                pairs=[j for j in range(44) if phase[j]!=background and phase[(j+2)%44]!=background]
                require(pairs and set(pairs)<=set(PAIR_STARTS),'actual shortest-pair cover failed')
                for j in pairs:
                    require(all(phase[i]==v for i,v in head_fixed(j,background).items()),'actual tied-max/min normalized head failed');normalizations+=1
        lower=[0]*44;lower[1]=1;upper=[v^f for v,f in zip(lower,phases)]
        require([v^w for v,w in zip(lower,upper)]==phases and [(1-v)^(1-w) for v,w in zip(lower,upper)]==phases
                and lower[0]!=lower[1],'unjustified lower-color identification');independence+=1
    return dict(actual_scalar_phase_truth_rows=truths,actual_tied_max_min_normalizations_including_side=normalizations,
        actual_lower_orientation_controls=independence,all44_lower_orientations_remain_independent=True)

def main(work,batch=None,controls=False):
    began=time.monotonic();pins();models=json.loads((work/'models.json').read_text())
    require(models['producer_sha256']==sha(ROOT/'generate.py'),'changed producer')
    require([r['stem'] for r in models['records']]==[stem_for(*p) for p in PARAMETERS]
            and {p.name for p in work.glob('*.cnf')}=={stem_for(*p)+'.cnf' for p in PARAMETERS},
            'incomplete seventy-two conditional max4/min2 pair heads')
    if controls:
        selected=[]
    elif batch is not None:
        require(0<=batch<9,'unsupported bounded definition batch')
        selected=models['records'][8*batch:8*(batch+1)]
    else:selected=models['records']
    slots,supports=literal_field() if selected else ({},set())
    records=[audit_case(r,work/(r['stem']+'.cnf'),slots,supports) for r in selected]
    out=dict(agent='six-vdw-2',role='researcher',status='EXACT_H7_ELEVEN_GAP4_PAIRS_DEFINITION_AUDIT',
        literal_APs=375760,removed_zero_APs=4312,signed_supports=26488,records=records,
        tiny_controls=tiny_controls() if controls or batch is None else None,
        ordinary_pair_cover_controls=ordinary_head_controls() if controls or batch is None else None,
        actual_scalar_controls=actual_scalar_controls() if controls or batch is None else None,
        literal_field_reconstructed=bool(selected),bounded_batch=batch,ordinary_coverage_not_proved_by_tiny_controls=True,
        conditional_isolation_premise=True,isolation_is_universal=False,exact_TEN_rules_used=False,
        proposed_ELEVEN_exclusion_used=False,gap_four_lemma_used_as_unconditional_native_cut=False,
        unpublished_exclusion_used_as_input=False,seconds=time.monotonic()-began,
        maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    mode='normal' if __debug__ else 'optimized'
    suffix='-controls' if controls else '-batch-'+str(batch) if batch is not None else ''
    (work/('audit-'+mode+suffix+'.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','tiny_controls','ordinary_max_gap_controls','actual_scalar_controls')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--batch',type=int);p.add_argument('--controls',action='store_true');args=p.parse_args()
    main(args.work.absolute(),args.batch,args.controls)
