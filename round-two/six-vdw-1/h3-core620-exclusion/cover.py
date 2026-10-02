"""Whole preserving six-case H3 normalization and all original cut truth tables; no solver."""
import argparse
import hashlib
import json
from math import gcd
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def run(model,out):
    require(not out.exists(),'fresh private next-plan output')
    require(hashlib.sha256(model.read_bytes()).hexdigest()=='af8d6618bcdc7880103a2fe4ae3418b609d8443115d791c4ce83f88e3137013d','canonical audited NEW row34 physical model')
    outer=json.loads(model.read_text());d=outer['base_model']
    require(outer['cut_premise']['artifact_ref']=='bafkreig4gyqfrxg7brwukbp7jbrfbj2bkzv6sctzy2ba6lgbt55qkbykme','actual cut premise')
    require((d['field_prime'],d['row_half'],d['AP_length'],d['subgroup'],d['fixed_first_coset_row'],d['variables'])==(31,10,7,[1,5,25],34,100),'full chosen physical input family')
    H={1,5,25};classes=sorted({tuple(r for r in range(1,31) if r*pow(a,-1,31)%31 in H) for a in range(1,31)},key=lambda c:c[0])
    lookup={r:g for g,c in enumerate(classes) for r in c}
    points=[None if x%31==0 else (1 if x%20<10 else -1)*(10*lookup[x%31]+x%10+1) for x in range(620)]
    require(points==d['point_literals'] and d['cosets']==[list(c) for c in classes],'whole independent actual unchanged point-input table')
    row=lambda m,s:((m>>((s%20)%10))&1)^((s%20)//10)
    units=[v for v in range(20) if gcd(v,20)==1]
    crt={(r,s):next(x for x in range(620) if x%31==r and x%20==s) for r in range(31) for s in range(20)}
    actions=set();identities=maps=0
    for v in units:
        A=crt[1,v];require(gcd(A,620)==1,'actual phase multiplier is a CRT unit')
        for z in range(20):
            B=crt[0,z]
            require({(A*x+B)%620 for x in range(620)}==set(range(620)),'whole physical phase-affine bijection')
            substitution=[points[(A*crt[c[0],j]+B)%620] for c in classes for j in range(10)]
            require({abs(s) for s in substitution}==set(range(1,101)),'whole absolute-input signed permutation')
            for x,l in enumerate(points):
                y=(A*x+B)%620
                require(y%31==x%31 and y%20==(v*(x%20)+z)%20,'all actual CRT coordinates')
                if l is None:require(points[y] is None,'whole modular pole set retained');continue
                require(points[y]==(1 if l>0 else -1)*substitution[abs(l)-1],'every actual regular signed input action');identities+=1
            actions.add(tuple(substitution));maps+=1
    require(maps==160 and len(actions)==160 and identities==96000,'full physical phase-affine action domain')
    local=[[(a+j*h)%20 for j in range(7)] for a in range(20) for h in range(1,20)]
    admissible={m for m in range(1024) if all(any(row(m,s)!=row(m,pos[0]) for s in pos[1:]) for pos in local)}
    orbits={};pending=set(admissible)
    while pending:
        rep=min(pending)
        orbit={sum(row(rep,v*s+z)<<s for s in range(10)) for v in units for z in range(20)}
        require(orbit<=pending,'full distinct admissible affine-class partition')
        orbits[rep]=sorted(orbit);pending-=orbit
    require([(r,len(o)) for r,o in orbits.items()]==[(8,160),(10,40),(12,80),(16,160),(20,40),(34,80),(72,20)],'entire known seven-orbit inventory')
    forbidden=set(orbits[16]);remaining=admissible-forbidden;reps=[8,10,12,20,34,72]
    cover=[];transport_checks=0
    for m in sorted(remaining):
        matches=[(rep,v,z) for rep in reps for v in units for z in range(20)
                 if all(row(m,v*s+z)==row(rep,s) for s in range(20))]
        require(matches,'every one of420 remaining original rows has a normalized representative')
        rep,v,z=matches[0]
        require(rep==next(r for r in reps if m in orbits[r]),'normalization belongs to its unique row class')
        transported={sum(row(f,v*s+z)<<s for s in range(10)) for f in forbidden}
        require(transported==forbidden,'chosen whole-core phase normalization preserves ALL orbit16 bans')
        transport_checks+=len(forbidden);cover.append([m,rep,v,z])
    cuts=[];truths=0
    for g in range(10):
        block=[]
        for m in sorted(forbidden):
            clause=[-(10*g+j+1) if(m>>j)&1 else 10*g+j+1 for j in range(10)]
            require(len({abs(v) for v in clause})==10,'ten independent absolute row inputs')
            for raw in range(1024):
                encoded=any(((raw>>j)&1)==int(v>0) for j,v in enumerate(clause))
                require(encoded==(raw!=m),'whole original row-mask exclusion truth table');truths+=1
            block.append(clause)
        accepted=[m for m in sorted(admissible) if all(any(((m>>j)&1)==int(v>0) for j,v in enumerate(c)) for c in block)]
        require(accepted==sorted(remaining),'all420 local rows survive exactly, at each actual coset')
        cuts+=block
    require(len(cuts)==len({tuple(c) for c in cuts})==1600,'complete distinct necessary row-cut inventory')
    first_units=[j+1 if(34>>j)&1 else -(j+1) for j in range(10)]
    require(first_units==[-1,2,-3,-4,-5,6,-7,-8,-9,-10] and 34 in remaining,'absolute unresolved first-coset34')
    result={'author':'six-vdw-1','role':'researcher','status':'COMPLETE_H3_REMAINING_SIX_CASE_NORMALIZATION_AND_CUT_TRUTHS',
            'proved_cut_graph_height':9576,'proved_cut_artifact_ref':'bafkreig4gyqfrxg7brwukbp7jbrfbj2bkzv6sctzy2ba6lgbt55qkbykme',
            'source_commit':'99b8f2cf222afd483784a41cdfbb94221158acae','cosets':[list(c) for c in classes],
            'point_input_table':points,'variables':100,'local_masks':580,'forbidden_masks':sorted(forbidden),
            'remaining_masks':sorted(remaining),'first_row_representatives':reps,
            'first_row_class_sizes':[len(orbits[r]) for r in reps],'first_row_normalization_cover':cover,
            'normalizing_phase_actions_preserve_forbidden_masks':transport_checks,
            'necessary_cut_clauses':cuts,'cut_original_row_truths':truths,'selected_first_row':34,
            'selected_absolute_units':first_units,'free_point_inputs_after_first_units':90,'actual_CRT_phase_maps':maps,'distinct_signed_input_permutations':len(actions),'all_actual_regular_signed_point_identities':identities,
            'scope':'Complete physical cut-preserving six-case normalization. IF all six audited formulas are strictly refuted, ACTUAL9576 implies no H3-invariant AP7-free regular620 core. This script alone asserts no refutation, interval witness or W bound.'}
    out.write_text(json.dumps(result,sort_keys=True)+'\n')
    return {k:v for k,v in result.items() if k not in ['point_input_table','forbidden_masks','remaining_masks','first_row_normalization_cover','necessary_cut_clauses']}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    print(json.dumps(run(a.model,a.output),sort_keys=True),flush=True)
