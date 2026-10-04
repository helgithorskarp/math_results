"""Exact serial entry-flow reader. The full physical bridge is separate."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import resource
import time
from model import (TAU_MAX, budget_record, canonical, check_literal_budgets, digest,
                   coefficient_input, comparison, exact_ldl, literal_point,
                   q19_candidate, require, sector_forms, type_budgets, type_of)


def entry_audit(point, old, b, tau):
    N,s,h=point['N'],point['s'],point['h']
    M=[[a-s*int(i==j) for j,a in enumerate(row)] for i,row in enumerate(point['L'])]
    bad=[];minimum=None;allowed=0
    sets=list(map(frozenset,point['members']))
    for i in range(N):
        require(sum(M[i])==h,'each original M row in h units')
        for j in range(N):
            if sets[i].isdisjoint(sets[j]):
                allowed+=1
                minimum=M[i][j] if minimum is None else min(minimum,M[i][j])
                if M[i][j]<tau:
                    bad.append(dict(i=i,j=j,v=point['members'][i],w=point['members'][j],
                                    actual_entry_h_units=str(M[i][j])))
    B=[i for i,v in enumerate(point['members']) if i>0 and 0 not in v]
    K={i for i in B if b['ell'][type_of(point['members'][i],b['k'])]<0}
    P=F(0);decrease=F(0);counts={'KK':0,'KG':0,'GG':0}
    equality_defects=[]
    for a,i in enumerate(B):
        for j in B[a+1:]:
            if not sets[i].isdisjoint(sets[j]):
                continue
            change=point['L'][i][j]-old['L'][i][j]
            tag='KK' if i in K and j in K else 'KG' if i in K or j in K else 'GG'
            counts[tag]+=1;P+=max(change,0);decrease+=max(-change,0)
            if (tag=='KK' and change>0) or (tag=='KG' and change!=0) or (tag=='GG' and change<0):
                equality_defects.append(dict(i=i,j=j,kind=tag,change=str(change)))
    require(all(point['L'][0][i]==tau for i in K),'all fresh bad nonstar floors')
    require(M[0][0]==tau,'actual empty loop floor')
    require(P==b['P0']+F(len(K)+1,2)*tau and
            decrease==b['D']/2+F(len(K),2)*tau and not equality_defects,
            'individual-edge mass identity/equality signs')
    return dict(tau=str(tau),minimum_original_M=str(minimum/h),minimum_h_units=str(minimum),
                allowed_positions=allowed,floor_violations=bad,bad_vertex_count=len(K),
                actual_NN_counts=counts,actual_positive_NN_mass=str(P),
                actual_negative_NN_mass=str(decrease),all_mass_equality_signs=True,
                all_entry_inequalities_paid=not bad,
                original_L_rational_sha256=digest([[str(a) for a in row] for row in point['L']]),
                original_T_rational_sha256=digest([[str(a) for a in row] for row in point['T']]))


def certificates(table,k,m):
    forms=sector_forms(table,k,m)
    records={}
    for tag,block in forms.items():
        test=exact_ldl(block['matrix'],block['metric'],F(1,1024))
        if not test['positive_definite']:
            test['unshifted_test']=exact_ldl(block['matrix'],block['metric'],F(0))
        records[tag]=dict(types=block['types'],metric=block['metric'],
                          multiplicity=block['multiplicity'],exact_block_test=test)
    return records


def largest_entry_interval(zero,maximum):
    limits=[];permanent=0;positions=0
    for i,v in enumerate(zero['members']):
        for j,w in enumerate(zero['members']):
            if not set(v).isdisjoint(w):continue
            positions+=1
            initial=zero['L'][i][j]-zero['s']*int(i==j)
            slope=(maximum['L'][i][j]-zero['L'][i][j])/TAU_MAX-1
            require(initial>=0 and (initial>0 or slope>=0),'every original affine surplus')
            if initial==slope==0:permanent+=1
            if slope<0:limits.append((initial/(-slope),i,j,v,w))
    bound=min(a[0] for a in limits)
    critical=[a for a in limits if a[0]==bound]
    require(bound==TAU_MAX and len(critical)==18 and all(
            (v==() and type_of(w,9)==(0,1,0)) or (w==() and type_of(v,9)==(0,1,0))
            for value,i,j,v,w in critical),'entire exact boundary is all18 actual empty/X-singleton entries')
    require(permanent==211,'all declared permanent loop/bad/30 chosen star floor positions')
    return dict(all_original_allowed_affine_inequalities=positions,
                declared_recipe_largest_entry_feasible_tau=str(bound),
                original_epsilon_interval=['0',str(bound/zero['h'])],
                permanent_floor_positions=permanent,critical_ordered_empty_X_singleton_positions=18,
                critical_individual_positions_sha256=digest([(i,j,v,w) for value,i,j,v,w in critical]),
                no_global_maximum_entry_floor_claim=True)


def run(path):
    raw=coefficient_input(path)
    start=time.monotonic()
    bases=[];q19=None
    for k,m in [(8,9),(9,9),(9,10)]:
        table=comparison(raw,k,m)
        b=type_budgets(table,k,m)
        point=literal_point(table,k,m)
        bases.append(dict(budgets=budget_record(b),literal_original=check_literal_budgets(point,b)))
        if (k,m)==(9,10):
            q19=(point,b)
    attempts=[];points=[]
    for tau in [F(0),TAU_MAX]:
        table,recipe=q19_candidate(raw,tau)
        point=literal_point(table,9,10)
        points.append(point)
        attempts.append(dict(recipe=recipe,entry_audit=entry_audit(point,q19[0],q19[1],tau),
                             block_diagnostics=certificates(table,9,10)))
    return dict(agent='six-downset-2',role='researcher',baseline_actual_checks=bases,
                entire_affine_entry_interval=largest_entry_interval(*points),
                q19_trials=attempts,generic_basis_proof_ordinary_unformalized='STRUCTURAL.md',
                real_q19_interpolation_proof_ordinary_unformalized='PROOF.md',
                no_other_count_H_certificate_or_general_H_claim=True,
                observed_seconds=time.monotonic()-start,
                peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--coefficients',required=True);p.add_argument('--out',required=True)
    args=p.parse_args();result=run(args.coefficients)
    raw=canonical(result)+b'\n';Path(args.out).write_bytes(raw)
    import hashlib
    print(json.dumps(dict(record_bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                          observed_seconds=result['observed_seconds'],peak_RSS_KiB=result['peak_RSS_KiB'])))
    for r in result['q19_trials']:
        print(json.dumps(dict(tau=r['recipe']['tau'],entry_floor_paid=r['entry_audit']['all_entry_inequalities_paid'],
                              floor_violations=r['entry_audit']['floor_violations'],
                              blocks={tag:rec['exact_block_test']['positive_definite'] for tag,rec in r['block_diagnostics'].items()})))
