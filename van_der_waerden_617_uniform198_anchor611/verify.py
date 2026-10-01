"""Exact single-class611 anchor completion; no numerical proposer imports."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).parent
N,P,C=3704,617,1852
OLD_ROOTS={45,1165,1725,2285,2845}
NEW_ROOTS={605,3405}
BASE_SHA='8bad4b3e7ce7dcbe8c8f7334ab5969930cc506ab697e4a5576c866363b2daa43'
PROFILE_SHA='142578449837532e9a154c00681287983a3a83c94c96a6938ea60c7c460f0e93'

def need(ok,message):
    if not ok:raise ValueError(message)

def actual_ap(a,d):
    need(type(a) is int and type(d) is int and d>0 and 0<=a<a+6*d<N,'Actual nonconstant integer seven-AP')
    return {a+j*d for j in range(7)}

def domain_sha(V):
    return hashlib.sha256((','.join(map(str,sorted(V)))+'\n').encode()).hexdigest()

def context(directory=HERE):
    prior=directory/'prior';path=prior/'base/phase-611.json'
    need(hashlib.sha256(path.read_bytes()).hexdigest()==BASE_SHA,'Exact selected base bytes')
    spec=importlib.util.spec_from_file_location('attributed_uniform611_exact',prior/'verify.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    colors,V,summary=old.base_premise(path)
    need(summary['phase']==611 and summary['key']==[611,7,1],'Actual611 reflection reference')
    need(summary['base_denominator']==1000000 and summary['base_weight_numerator']==196012413,'Checked original611 coefficients')
    need(summary['cap197_defect_numerator']==987587,'Exact one-class197 defect budget')
    need(colors.count(0)==colors.count(1)==1849 and colors.count(-1)==6,'Actual class sizes and free poles')
    need(all(colors[N-1-x]==(-1 if colors[x]<0 else 1-colors[x]) for x in range(N)),'Reference antisymmetry without candidate symmetry')
    K=[{x for x in range(N) if colors[x]==c}-V[c] for c in (0,1)]
    need([len(k) for k in K]==[82,82] and [len(v) for v in V]==[1767,1767],'FULL single-class197 base screens')
    anchor=actual_ap(45,560)
    need(all(colors[x]==0 for x in anchor) and anchor&K[0]==NEW_ROOTS,'Actual original0 anchor; K0 is NOT fixed here')
    cover=json.loads((prior/'covers/phase-611.json').read_text())
    need(type(cover) is dict and set(cover)=={'format','phase','caps','anchor','chains'},'Historical cover schema')
    need(cover['format']=='QR617_BASESCREEN_ANCHOR_COVER_1' and type(cover['phase']) is int and cover['phase']==611,'Historical611 identity')
    need(cover['anchor']==[45,560] and all(type(v) is int for v in cover['anchor']),'Exact historical anchor')
    need(cover['caps']==[197,197] and all(type(v) is int for v in cover['caps']),'Legacy metadata; NO original0 cap is assumed')
    chains=cover['chains'];need(type(chains) is list and len(chains)==5,'All five inherited roots')
    old_roots={}
    for chain in chains:
        need(type(chain) is dict and set(chain)=={'root','certificates'} and type(chain['root']) is int,'Explicit native historical root')
        root=chain['root'];files=chain['certificates']
        need(root in OLD_ROOTS and root not in old_roots and type(files) is list and files,'Distinct old root and complete nonempty chain')
        need(all(type(f) is str and not Path(f).is_absolute() and '..' not in Path(f).parts for f in files),'Local historical stage files')
        old_roots[root]=files
    need(set(old_roots)==OLD_ROOTS and OLD_ROOTS|NEW_ROOTS==anchor,'Every actual anchor position covered exactly once')
    return {'old':old,'prior':prior,'base':path,'colors':colors,'V':V[1],'anchor':anchor,'old_roots':old_roots,'summary':summary}

def check_new_root(data,ctx,require_exclusion=True):
    fields={'format','phase','root','capped_original_class','capped_class_cap','base_sha256','denominator','AP_weights'}
    need(type(data) is dict and set(data)==fields,'Single-cap root schema without hidden states or other-class bounds')
    need(data['format']=='QR617_SINGLECAP611_AP_PACK_1' and type(data['phase']) is int and data['phase']==611,'Exact611 root format')
    root=data['root'];D=data['denominator'];V=ctx['V'];colors=ctx['colors']
    need(type(root) is int and root in NEW_ROOTS and root in ctx['anchor'] and colors[root]==0,'One of the two omitted actual original0 anchor edits')
    need(type(data['capped_original_class']) is int and data['capped_original_class']==1,'Only original1 capped')
    need(type(data['capped_class_cap']) is int and data['capped_class_cap']==197,'Exact197 cap, other class uncapped')
    need(data['base_sha256']==BASE_SHA and hashlib.sha256(ctx['base'].read_bytes()).hexdigest()==BASE_SHA,'Actually checked base premise')
    need(type(D) is int and D>0 and type(data['AP_weights']) is list,'Positive native denominator and weight list')
    loads={x:0 for x in V};W=activated=0;seen=set()
    for row in data['AP_weights']:
        need(type(row) is list and len(row)==3 and all(type(v) is int for v in row),'Native integer AP row')
        a,d,w=row;need(w>0 and (a,d) not in seen,'Unique positively weighted AP');seen.add((a,d))
        A=actual_ap(a,d)
        mono=all(colors[x]==1 for x in A)
        active=root in A and all(colors[x]==1 for x in A-{root})
        need(mono or active,'Original1 AP or exactly root plus six original1 positions, with no unknown poles')
        petal=A&V;need(petal,'Nonempty FULL inherited-domain petal')
        W+=w;activated+=int(active)
        for x in petal:loads[x]+=w
    need(all(0<=L<=D for L in loads.values()),'Capacity at EVERY full-domain point')
    gap=W-197*D
    if require_exclusion:need(gap>0,'Strict single-class197 packing contradiction')
    return {'root':root,'capped_original_class':1,'other_class_cap':None,'denominator':D,'weighted_numerator':W,
            'strict_gap_numerator':gap,'strict_gap':str(Fraction(gap,D)),'excluded':gap>0,
            'full_domain_size':len(V),'full_domain_sha256':domain_sha(V),'maximum_load':max(loads.values()),
            'positive_AP_weights':len(data['AP_weights']),'activated_AP_occurrences':activated,'native_solver_trusted':False}

def check_old_root(root,ctx):
    V=set(ctx['V']);stages=[]
    for filename in ctx['old_roots'][root]:
        need(not stages or not stages[-1]['exclusion'],'No stage after a contradiction')
        data=json.loads((ctx['prior']/filename).read_text())
        row=ctx['old'].check_stage(data,ctx['colors'],V,611,root)
        V=set(row['next_domain']);stages.append({k:v for k,v in row.items() if k!='next_domain'})
    need(stages[-1]['exclusion'],'Each old root ends in a strict contradiction')
    return {'root':root,'other_class_cap':None,'stages':stages}

def check_family():
    need(all(P%d for d in range(2,25)),'Prime617 by full trial division')
    q=[-1]+[int(pow(r,308,P)==P-1) for r in range(1,P)]
    need(all(pow(r,308,P) in (1,P-1) for r in range(1,P)),'Actual Euler characters')
    hist=Counter()
    for s in range(P):
        colors=[]
        for x in range(N):
            r=(x-C+(s if x<C else (1-s)%P))%P
            colors.append(-1 if not r else q[r]^int(x>=C))
        need(all(colors[N-1-x]==(-1 if colors[x]<0 else 1-colors[x]) for x in range(N)),'Reference reflection at all617 phases')
        size=1848 if s==1 else 1849
        need(colors.count(0)==colors.count(1)==size,'Complete actual original-class counts')
        hist[size]+=1
    return {'phases_checked':617,'original_class_size_histogram':{str(k):v for k,v in sorted(hist.items())},'candidate_symmetry_assumed':False}

def check_complete(directory=HERE,documents=None):
    manifest=json.loads((directory/'manifest.json').read_text())
    expected={'format':'QR617_COMPLETE_SINGLECAP611_ANCHOR_1','phase':611,'anchor':[45,560],
              'capped_original_class':1,'capped_class_cap':197,'old_roots':sorted(OLD_ROOTS),'new_roots':sorted(NEW_ROOTS)}
    need(type(manifest) is dict and set(manifest)==set(expected) and manifest==expected,'Exact complete611 manifest with only one cap')
    need(all(type(manifest[k]) is int for k in ('phase','capped_original_class','capped_class_cap')),'Native manifest hypothesis integers')
    need(all(type(x) is int for k in ('anchor','old_roots','new_roots') for x in manifest[k]),'Native complete manifest coordinates')
    ctx=context(directory)
    if documents is None:documents={r:json.loads((directory/f'certificates/root-{r}.json').read_text()) for r in NEW_ROOTS}
    need(type(documents) is dict and set(documents)==NEW_ROOTS and all(type(r) is int for r in documents),'BOTH missing roots, no omitted or extra alternative')
    old=[check_old_root(r,ctx) for r in sorted(OLD_ROOTS)];new=[]
    for r in sorted(NEW_ROOTS):
        need(documents[r]['root']==r,'Root document identity')
        new.append(check_new_root(documents[r],ctx))
    need({row['root'] for row in old+new}==ctx['anchor'] and len(old)+len(new)==7,'ALL seven anchor positions excluded under only e1<=197')
    raw=(directory/'imported_profile.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PROFILE_SHA,'Byte-pinned published other-phase mathematical profile')
    prior=json.loads(raw)['combined_profile']
    need(prior['individual198_or_stronger_count']==616 and prior['remaining_individual197_phases']==[611],'Precisely the sole remaining individual197 phase')
    need(prior['total396_or_stronger_count']==617 and prior['remaining_total395_phases']==[],'Earlier uniform total396 profile')
    need(sum(prior['total_floor_histogram'].values())==617,'Complete imported profile partition')
    return {'agent':'six-vdw-3','role':'researcher','status':'EXACT_QR617_UNIFORM_INDIVIDUAL198_ANCHOR611',
            'phase611':{'key':[611,7,1],'base_premise':ctx['summary'],'anchor':[45,560],'anchor_points':sorted(ctx['anchor']),
                        'old_roots':old,'new_roots':new,'old_root_count':5,'new_root_count':2,'all_anchor_roots_checked':7,
                        'old_stage_count':sum(len(row['stages']) for row in old),'only_capped_class':1,'cap':197,
                        'other_class_uncapped':True,'individual_interval_each_colour':[198,1651],'total_interval':[396,3302]},
            'family':check_family(),'combined_profile':{'uniform_individual_lower_bound':198,'uniform_individual_upper_bound':1651,
                       'individual198_or_stronger_count':617,'remaining_individual197_phases':[],
                       'uniform_total_lower_bound':396,'uniform_total_upper_bound':3302,
                       'total396_or_stronger_count':617,'total_floor_histogram':prior['total_floor_histogram'],
                       'prior_other_phase_proofs_replayed_here':False},
            'arbitrary_AP_free_candidates':True,'free_poles_unrestricted_and_uncounted':True,'candidate_symmetry_assumed':False,
            'native_solver_trusted':False,'new_W_bound':False,'length3704_witness':False,'attainment_claimed':False,
            'external_independent_review_claimed':False,'proof_assistant_formalization_claimed':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE);p.add_argument('--output',type=Path)
    p.add_argument('--expected',type=Path);p.add_argument('--new-root-dir',type=Path);a=p.parse_args()
    docs=None if a.new_root_dir is None else {r:json.loads((a.new_root_dir/f'root-{r}/packing.json').read_text()) for r in NEW_ROOTS}
    out=check_complete(a.directory,docs)
    if a.expected:need(out==json.loads(a.expected.read_text()),'Expected complete exact result')
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    compact={k:v for k,v in out.items() if k!='phase611'}
    compact['phase611']={k:v for k,v in out['phase611'].items() if k not in ('old_roots','base_premise')}
    print(json.dumps(compact),flush=True)

if __name__=='__main__':main()
