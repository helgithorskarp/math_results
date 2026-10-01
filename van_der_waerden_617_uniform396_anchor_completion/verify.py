"""Complete single-class anchor exclusions, using actual APs and exact integers.

Only the opposite original class is capped197. The historical per-root domain
proofs are replayed before the nine new packings. All seven anchor positions
are covered, including positions that were fixed only in the older joint box.
No generator, solver, floating arithmetic or candidate symmetry is imported.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).parent
N,P,C=3704,617,1852
ANCHORS={184:(286,561),201:(957,235),205:(19,438),269:(35,323)}
NEW_ROOTS={184:{286,3652},201:{957,1192},205:{19,457},269:{35,358,681}}
PROFILE_SHA='d0506494b7a74b8121d4621aeb7b5f64e621cc810cb1b2436c22944b1b9a0de8'


def need(ok,message):
    if not ok:raise ValueError(message)


def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def actual_ap(a,d):
    need(type(a) is int and type(d) is int and d>0 and 0<=a<a+6*d<N,'Actual nonconstant integer seven-AP')
    return {a+j*d for j in range(7)}


def domain_sha(V):
    return hashlib.sha256((','.join(map(str,sorted(V)))+'\n').encode()).hexdigest()


def premise(phase,directory=HERE):
    need(type(phase) is int and phase in ANCHORS,'One of the four selected phases')
    if phase in (184,205):
        prior=directory/'prior_uniform';module=load_module(prior/'verify.py','old_uniform_exact')
        base=prior/f'base/phase-{phase}.json';rigidity=prior/f'old-trees/phase-{phase}.json'
        colors,V,summary=module.base_premise(base,rigidity)
        K=[set(v) for v in summary['zero_loss_premise']['fixed_positions']]
        need(V[1]=={x for x in range(N) if colors[x]==1 and x not in K[1]},'Full single-class197 domain after the checked rigidity lemma')
        cover=json.loads((prior/f'covers/phase-{phase}.json').read_text())
        need(type(cover) is dict and set(cover)=={'format','phase','caps','anchor','chains'},'Historical cover schema')
        need(cover['format']=='QR617_BASESCREEN_ANCHOR_COVER_1' and cover['phase']==phase and type(cover['phase']) is int,'Historical phase')
        need(cover['anchor']==list(ANCHORS[phase]) and cover['caps']==[197,197],'Historical anchor identity, without assuming its first cap')
        chains=cover['chains'];need(type(chains) is list,'Historical root chains')
        need(all(type(t) is dict and set(t)=={'root','certificates'} and type(t['root']) is int for t in chains),'Explicit historical root chains')
        old={t['root']:t['certificates'] for t in chains};need(len(old)==len(chains),'No repeated old root')
    elif phase==201:
        prior=directory/'prior201';module=load_module(prior/'verify.py','old_phase201_exact')
        colors,K,_,_=module.premise(prior,root=1662)
        base=prior/'parent/zero/base/phase-201.json';rigidity=prior/'parent/zero/tree.json'
        old={r:['certificates/'+f for f in names] for r,names in module.ROOT_FILES.items()}
    else:
        prior=directory/'prior269';module=load_module(prior/'verify.py','old_phase269_exact')
        colors,K,_=module.premise(prior)
        base=prior/'low/base/phase-269.json';rigidity=prior/'low/certificate.json'
        old={r:[f'roots/{r}.json'] for r in (1004,1327,1650,1973)}
    need(colors.count(-1)==6 and colors.count(0)==colors.count(1)==1849,'Original class counts and six uncounted poles')
    need(all(colors[N-1-x]==(-1 if colors[x]<0 else 1-colors[x]) for x in range(N)),'Actual reference antisymmetry')
    need(all(colors[x]==c for c in (0,1) for x in K[c]),'Rigidity sets in the actual original classes')
    anchor=actual_ap(*ANCHORS[phase])
    need(all(colors[x]==0 for x in anchor),'Actual original0 monochromatic anchor')
    need(set(old)|NEW_ROOTS[phase]==anchor and not set(old)&NEW_ROOTS[phase],'All seven anchor positions exactly once')
    need(NEW_ROOTS[phase]<=K[0],'Previously omitted anchor positions are in the opposite rigidity set; that set is NOT fixed in this proof')
    return {'phase':phase,'colors':colors,'K':K,'base':base,'rigidity':rigidity,
            'prior':prior,'module':module,'old_roots':old,'anchor':anchor,
            'V':{x for x in range(N) if colors[x]==1 and x not in K[1]}}


def check_root(data,ctx,require_exclusion=True):
    fields={'format','phase','root','capped_original_class','capped_class_cap',
            'base_sha256','rigidity_sha256','denominator','AP_weights','triple_weights'}
    need(type(data) is dict and set(data)==fields,'Root packing schema has exactly one capped class')
    need(data['format']=='QR617_ANCHOR_COMPLETION_PACK_1','Root packing format')
    need(type(data['phase']) is int and data['phase']==ctx['phase'],'Actual reference phase')
    root=data['root'];colors=ctx['colors'];V=ctx['V'];D=data['denominator']
    need(type(root) is int and root in ctx['anchor'] and colors[root]==0,'An actual original0 anchor edit')
    need(type(data['capped_original_class']) is int and data['capped_original_class']==1,'Only the opposite original class is capped')
    need(type(data['capped_class_cap']) is int and data['capped_class_cap']==197,'Exact single-class cap197')
    need(data['base_sha256']==hashlib.sha256(ctx['base'].read_bytes()).hexdigest(),'Exact checked base dependency')
    need(data['rigidity_sha256']==hashlib.sha256(ctx['rigidity'].read_bytes()).hexdigest(),'Exact checked class197 rigidity dependency')
    need(type(D) is int and D>0,'Positive native integer denominator')
    need(type(data['AP_weights']) is list and type(data['triple_weights']) is list,'Exact weight lists')
    loads={x:0 for x in V};W=checked=activated=0

    def petal(ap):
        nonlocal checked,activated
        need(type(ap) is list and len(ap)==2,'Actual AP coordinate pair')
        A=actual_ap(*ap)
        mono=all(colors[x]==1 for x in A)
        active=root in A and all(colors[x]==1 for x in A-{root})
        need(mono or active,'Original1 AP or exactly the assumed root plus six original1 terms; no poles or extra antecedents')
        ps=A&V;need(ps,'Nonempty full inherited petal')
        checked+=1;activated+=int(active)
        return ps
    seen=set()
    for row in data['AP_weights']:
        need(type(row) is list and len(row)==3 and all(type(v) is int for v in row),'Native integer AP row')
        a,d,w=row;need(w>0 and (a,d) not in seen,'Distinct positive AP rows');seen.add((a,d))
        ps=petal([a,d]);W+=w
        for x in ps:loads[x]+=w
    seen=set()
    for row in data['triple_weights']:
        need(type(row) is list and len(row)==2,'Triple row schema')
        aps,w=row;need(type(aps) is list and len(aps)==3 and type(w) is int and w>0,'Three actual APs with a positive native weight')
        need(all(type(ap) is list and len(ap)==2 and all(type(v) is int for v in ap) for ap in aps),'Native triple coordinates')
        key=tuple(sorted(tuple(ap) for ap in aps));need(len(set(key))==3 and key not in seen,'Distinct APs and no repeated triple');seen.add(key)
        ps=[petal(ap) for ap in aps];need(not set.intersection(*ps),'No single permitted edit hits all three required APs')
        U=set.union(*ps);W+=2*w
        for x in U:loads[x]+=w
    need(all(0<=L<=D for L in loads.values()),'Capacity at EVERY point of the full permitted original1 domain')
    gap=W-197*D
    if require_exclusion:need(gap>0,'Strict weighted contradiction of the single-class197 cap')
    return {'root':root,'capped_original_class':1,'other_class_cap':None,'denominator':D,
            'weighted_numerator':W,'strict_gap_numerator':gap,'strict_gap':str(Fraction(gap,D)),
            'excluded':gap>0,'full_domain_size':len(V),'full_domain_sha256':domain_sha(V),
            'maximum_load':max(loads.values()),'positive_AP_weights':len(data['AP_weights']),
            'positive_triple_weights':len(data['triple_weights']),'actual_AP_occurrences_checked':checked,
            'activated_AP_occurrences_checked':activated,'solver_trusted':False}


def check_old_root(root,ctx):
    phase=ctx['phase'];module=ctx['module'];files=ctx['old_roots'][root]
    need(root in ctx['anchor'] and ctx['colors'][root]==0 and files,'Actual old root and nonempty chain')
    need(all(type(f) is str and not Path(f).is_absolute() and '..' not in Path(f).parts for f in files),'Local historical proof files')
    if phase==269:
        old=json.loads((ctx['prior']/files[0]).read_text())
        need(len(files)==1 and set(old)=={'format','phase','root','caps','denominator','low_certificate_sha256','AP_weights','cover2_weights','surcharges'},'Old269 frozen row schema')
        need(old['format']=='QR617_PHASE269_JOINT197_ROOT_1' and type(old['phase']) is int and old['phase']==269,'Old269 identity')
        need(type(old['root']) is int and old['root']==root and old['caps']==[197,197] and all(type(c) is int for c in old['caps']),'Historical metadata, no new first-class cap assumption')
        need(old['surcharges']==[] and old['low_certificate_sha256']==hashlib.sha256(ctx['rigidity'].read_bytes()).hexdigest(),'Unchanged low premise and no dropped point surcharges')
        # Recheck the historical coefficients with the NEW single-class
        # checker. The old first-class cap and K0 do not enter any row.
        translated={'format':'QR617_ANCHOR_COMPLETION_PACK_1','phase':phase,'root':root,
                    'capped_original_class':1,'capped_class_cap':197,
                    'base_sha256':hashlib.sha256(ctx['base'].read_bytes()).hexdigest(),
                    'rigidity_sha256':hashlib.sha256(ctx['rigidity'].read_bytes()).hexdigest(),
                    'denominator':old['denominator'],'AP_weights':old['AP_weights'],'triple_weights':old['cover2_weights']}
        result=check_root(translated,ctx)
        return {'root':root,'other_class_cap':None,'stages':[result],'inherited_prefix_stages':0}
    if phase==201:
        colors,K,V,prefix=module.premise(ctx['prior'],root=root)
        need(colors==ctx['colors'] and K==ctx['K'],'Consistent checked201 premise')
    else:V=set(ctx['V']);prefix=None
    stages=[]
    for filename in files:
        need(not stages or not stages[-1]['exclusion'],'No stage after a contradiction')
        data=json.loads((ctx['prior']/filename).read_text())
        row=(module.check_stage(data,ctx['colors'],V,root=root,cap=197) if phase==201
             else module.check_stage(data,ctx['colors'],V,phase,root))
        stages.append(row);V=set(row['next_domain'])
    need(stages[-1]['exclusion'],'Every historical root chain ends in a strict contradiction')
    compact=[{k:v for k,v in row.items() if k not in ('next_domain','newly_forbidden_positions')} for row in stages]
    return {'root':root,'other_class_cap':None,'stages':compact,'inherited_prefix_stages':int(prefix is not None)}


def check_family():
    q=[-1]+[int(pow(r,308,P)==P-1) for r in range(1,P)];hist=Counter()
    need(all(pow(r,308,P) in (1,P-1) for r in range(1,P)),'Euler characters modulo617')
    need(all(P%d for d in range(2,25)),'Complete prime617 trial division')
    for s in range(P):
        colors=[]
        for x in range(N):
            r=(x-C+(s if x<C else (1-s)%P))%P
            colors.append(-1 if r==0 else q[r]^int(x>=C))
        need(all(colors[N-1-x]==(-1 if colors[x]<0 else 1-colors[x]) for x in range(N)),'Actual antisymmetry at every phase')
        size=1848 if s==1 else 1849
        need(colors.count(0)==colors.count(1)==size,'All617 actual class-size identities')
        hist[size]+=1
    return {'phases_checked':617,'original_class_size_histogram':{str(k):v for k,v in sorted(hist.items())},
            'candidate_symmetry_assumed':False}


def check_complete(directory=HERE,documents=None):
    manifest=json.loads((directory/'manifest.json').read_text())
    need(type(manifest) is dict and set(manifest)=={'format','phases'} and manifest['format']=='QR617_COMPLETE_ANCHORS_1','Complete manifest schema')
    need(type(manifest['phases']) is list and len(manifest['phases'])==4,'Exactly four selected phases')
    entries={}
    for e in manifest['phases']:
        need(type(e) is dict and set(e)=={'phase','anchor','new_roots'} and type(e['phase']) is int and e['phase'] in ANCHORS,'Native manifest phase')
        phase=e['phase'];need(phase not in entries and e['anchor']==list(ANCHORS[phase]) and all(type(v) is int for v in e['anchor']),'Exact distinct anchor')
        need(type(e['new_roots']) is list and all(type(v) is int for v in e['new_roots']) and len(set(e['new_roots']))==len(e['new_roots']) and set(e['new_roots'])==NEW_ROOTS[phase],'All new anchor positions exactly once')
        entries[phase]=e
    if documents is None:
        documents={s:{r:json.loads((directory/f'certificates/phase-{s}-root-{r}.json').read_text()) for r in NEW_ROOTS[s]} for s in ANCHORS}
    need(type(documents) is dict and set(documents)==set(ANCHORS),'No omitted or extra phase proof')
    results=[];old_count=new_count=0
    for phase in sorted(ANCHORS):
        ctx=premise(phase,directory);docs=documents[phase]
        need(type(docs) is dict and set(docs)==NEW_ROOTS[phase] and all(type(r) is int for r in docs),'Every new root proof, no omitted alternative')
        old=[check_old_root(r,ctx) for r in sorted(ctx['old_roots'])]
        new=[]
        for root in sorted(NEW_ROOTS[phase]):
            need(docs[root]['root']==root,'New document belongs to the required root')
            new.append(check_root(docs[root],ctx))
        covered={r['root'] for r in old+new}
        need(covered==ctx['anchor'] and len(old)+len(new)==7,'ALL seven original0 anchor edits excluded under only e1<=197')
        old_count+=len(old);new_count+=len(new)
        results.append({'phase':phase,'key':[phase,(1-phase)%P,1],'anchor':list(ANCHORS[phase]),
                        'anchor_points':sorted(ctx['anchor']),'old_roots':old,'new_roots':new,
                        'opposite_class_cap_only':197,'other_class_uncapped':True,
                        'all_anchor_roots_excluded':True,'individual_lower_bound_each_color':198,
                        'individual_upper_bound_each_color':1651,'total_lower_bound':396,'total_upper_bound':3302,
                        'rigidity_positions_per_class':len(ctx['K'][1]),'initial_full_domain_size':len(ctx['V'])})
    raw=(directory/'imported_profile.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PROFILE_SHA,'Byte-pinned published profile, explicitly imported as a mathematical result')
    prior=json.loads(raw)['combined_imported_context']
    need(prior['individual198_or_stronger_count']==612 and prior['total396_or_stronger_count']==613,'Published profile counts')
    need(set(prior['remaining_total395_phases'])==set(ANCHORS) and set(ANCHORS)<=set(prior['remaining_individual197_phases']),'Disjoint complete remaining-phase coverage')
    histogram=dict(prior['total_floor_histogram']);need(histogram.pop('395')==4,'Four old total395 phases')
    histogram['396']+=4;need(sum(histogram.values())==617,'Complete617-phase profile partition')
    return {'agent':'six-vdw-3','role':'researcher','status':'EXACT_QR617_UNIFORM396_ANCHOR_COMPLETION',
            'new_phases':results,'old_anchor_roots_rechecked':old_count,'new_anchor_roots_checked':new_count,
            'all_anchor_roots_checked':old_count+new_count,'complete_anchors':4,'family':check_family(),
            'combined_profile':{'uniform_total_lower_bound':396,'uniform_total_upper_bound':3302,
                                'total396_or_stronger_count':617,'individual198_or_stronger_count':616,
                                'remaining_individual197_phases':[611],'remaining_total395_phases':[],
                                'total_floor_histogram':histogram,'prior_other_phase_proofs_replayed_here':False},
            'arbitrary_AP_free_candidates':True,'free_poles_unrestricted_and_uncounted':True,
            'candidate_symmetry_assumed':False,'native_solver_trusted':False,'new_W_bound':False,
            'length3704_witness':False,'attainment_claimed':False,'external_independent_review_claimed':False,
            'proof_assistant_formalization_claimed':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE)
    p.add_argument('--output',type=Path);p.add_argument('--expected',type=Path)
    p.add_argument('--new-root-dir',type=Path);a=p.parse_args()
    documents=None if a.new_root_dir is None else {s:{r:json.loads((a.new_root_dir/f'phase-{s}-root-{r}/packing.json').read_text()) for r in NEW_ROOTS[s]} for s in ANCHORS}
    out=check_complete(a.directory,documents)
    if a.expected:need(out==json.loads(a.expected.read_text()),'Expected exact result')
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    compact={k:v for k,v in out.items() if k!='new_phases'}
    compact['new_phases']=[{'phase':r['phase'],'old_roots':[v['root'] for v in r['old_roots']],
                           'new_roots':[{'root':v['root'],'W':v['weighted_numerator'],'D':v['denominator'],
                                         'gap':v['strict_gap_numerator']} for v in r['new_roots']]} for r in out['new_phases']]
    print(json.dumps(compact),flush=True)


if __name__=='__main__':main()
