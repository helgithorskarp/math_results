"""Whole entrywise replay with compact expected hashes; six-code-1 researcher."""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
import time
import producer as p
import oracle as o

HERE=Path(__file__).resolve().parent


def need(ok,msg):
    if not ok:raise ValueError(msg)


def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()


def reject(call):
    try:call()
    except (ValueError,KeyError,IndexError,TypeError):return True
    raise ValueError('semantic damage accepted')


def run(first):
    oldp=p.frozen('producer');oldo=p.frozen('oracle')
    raw=(p.PARENT/'fixtures.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7','frozen complete23 literal stars')
    literal=json.loads(raw);marks,_=oldp.rows_and_physical_bridge(literal)
    other,_=oldo.physical_rows(literal);need(marks==other,'every raw HIGH mark independently decoded')
    physical,types=p.actual_marks(oldp,literal)
    need(len(physical)==426 and len(types)==43,'full cap6/cap5 physical projection')
    pair_records=p.pair_carrier()
    for r in pair_records:r['columns']=p.column_carrier(r)
    need(enc(pair_records)==enc(o.independently_derive()),'every labelled HH/HHH and ordered D/N record agrees')
    cases=p.full_cases();need(cases==o.scalar_cases(),'all68 cases including tau2')
    pools={}
    for r in pair_records:
        if r['pattern'].startswith('T2'):
            for c in r['columns']:pools.setdefault(c['K'],[]).append((r,c))
    branch_summaries=[];cuts=Counter();post=[];matching_calls=0;maximum=[0,0];controls=[]
    for case in cases:
        vectors,s=oldp.produce(types,case);other,t=oldo.coefficient_vectors(types,case)
        need(vectors==other,'every full43-entry necessary population agrees')
        maximum=[max(maximum[0],s),max(maximum[1],t)];rows=[]
        for vector in vectors:
            p.check_vector(types,case,vector)
            cert=p.prior_certificate(types,vector,oldp)
            need(cert==o.prior_certificate(types,vector,oldo),'every endpoint, root and B2 certificate independently agrees')
            if cert['reason']=='OPEN':
                full=hashlib.sha256();pool=pools.get(case['K'],[]);begin=time.monotonic()
                for index,(r,c) in enumerate(pool):
                    need(index<100000 and time.monotonic()-begin<=10,'INCOMPLETE fixed100000-column/10s guard')
                    a=p.slot_matching(types,vector,r,c);b=o.hall_check(types,vector,r,c)
                    need(a==b,'each actual role-aware slot matching agrees with grouped Hall')
                    need(not a,'necessary support remains OPEN; no T2 absence')
                    full.update(enc([r['pattern'],r['mode'],r['lam'],r['D'],c['N'],a])+b'\n')
                    if not controls and case['K']==13 and r['D']==(5,5,4,4,1) and c['N']==(3,3,3,3,1):
                        relaxed=p.slot_matching(types,vector,r,c,False)
                        need(relaxed==o.hall_check(types,vector,r,c,False),'relaxed control checked independently')
                        if relaxed:controls.append(dict(case=case,vector=vector,pattern=r['pattern'],mode=r['mode'],lam=r['lam'],D=r['D'],N=c['N'],
                            ordinary_covered_pair_requirement=False,scope='abstract necessary allocation, not a packing'))
                matching_calls+=len(pool)
                cert=dict(reason='ACTUAL_ROLE_AWARE_HEAVY_SUPPORT',column_candidates=len(pool),every_candidate_sha256=full.hexdigest())
                post.append(dict(case=case,vector=vector,certificate=cert))
            cuts[cert['reason']]+=1;rows.append(dict(vector=vector,certificate=cert))
        branch_summaries.append(dict(case=case,vectors=len(rows),cuts=dict(Counter(r['certificate']['reason'] for r in rows)),
                                     full_vector_certificates_sha256=hashlib.sha256(enc(rows)).hexdigest()))
    need(len(post)==52 and matching_calls==112452 and controls,'all post-prior residues and essential positive control')
    case=post[0]['case'];v=post[0]['vector'];bad=list(v);bad[0]=-1
    damages=[dict(name='NEGATIVE_POPULATION',rejected=reject(lambda:p.check_vector(types,case,bad))),
             dict(name='SHORT_POPULATION',rejected=reject(lambda:p.check_vector(types,case,v[:-1]))),
             dict(name='WRONG_SUPPORT_K',rejected=reject(lambda:p.check_vector(types,dict(case,K=case['K']+1),v))),
             dict(name='WRONG_EXCESS_X',rejected=reject(lambda:p.check_vector(types,dict(case,X=case['X']+1),v))),
             dict(name='WRONG_HH_CHARGE_Q',rejected=reject(lambda:p.check_vector(types,dict(case,Q=case['Q']+1),v))),
             dict(name='BOOLEAN_COUNT',rejected=reject(lambda:p.check_vector(types,case,[True]+list(v[1:]))))]
    pair_summary=[]
    for pattern,mode in [('T1','all_le4'),('T2_shared_one','all_le4'),('T2_shared_pair','all_le4'),('T2_shared_pair','common_pair5')]:
        rs=[r for r in pair_records if (r['pattern'],r['mode'])==(pattern,mode)]
        pair_summary.append(dict(pattern=pattern,mode=mode,raw=len(rs),pair_feasible=sum(r['reason']=='PAIR_FEASIBLE' for r in rs),
                                 ordered_columns=sum(len(r['columns']) for r in rs)))
    summary=dict(actual_agent='six-code-1',role='researcher',status='COMPLETE_CONDITIONAL_P37_SINGLE_HHH_TRIPLE',
        raw_HIGH_marks=426,positive_HIGH_marks=sum(bool(r['cap6_LOW_completions']) for r in physical),
        physical_LOW_completions=sum(r['cap6_LOW_completions'] for r in physical),types=types,
        physical_every_mark_sha256=hashlib.sha256(enc(physical)).hexdigest(),
        pair_summary=pair_summary,every_labelled_HH_column_record_sha256=hashlib.sha256(enc(pair_records)).hexdigest(),
        scalar_cases=len(cases),population_vectors=sum(b['vectors'] for b in branch_summaries),cut_counts=dict(cuts),
        branch_records=branch_summaries,post_prior_residues=post,all_matching_candidates=matching_calls,
        relaxed_positive_control=controls,semantic_damages=damages,
        private_N5_exclusion_used=False,unconditional_surcharge_used=False,
        ordinary_bridges_formalized=False,external_independent_review=False)
    whole=hashlib.sha256(enc(summary)).hexdigest()
    if first:need(not (HERE/'EXPECTED.json').exists(),'first replay precedes expected output')
    else:need(enc(summary)==enc(json.loads((HERE/'EXPECTED.json').read_text())),'whole expected record changed')
    print(json.dumps(dict(summary=summary,mathematical_sha256=whole,diagnostics=dict(max_coefficient_states=maximum)),indent=2,sort_keys=True))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--first-run',action='store_true');run(parser.parse_args().first_run)
