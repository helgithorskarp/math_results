"""Adversarial certificate controls and small definition-level logical models."""
import argparse
from copy import deepcopy
import itertools
import json
from pathlib import Path
import sys
import check_all
import verify

HERE=Path(__file__).parent


def run(work):
    work.mkdir(parents=True,exist_ok=True)
    rejected=[]
    def reject(label,fn):
        try:fn()
        except ValueError:rejected.append(label)
        else:raise RuntimeError('Unsound control accepted: '+label)
    manifest=json.loads((HERE/'manifest.json').read_text())
    full=check_all.replay();cases=full['new_cases']
    imports=check_all.dependencies(manifest)
    base=HERE/'base/phase-170.json';rawbase=json.loads(base.read_text())
    colors,V,_=verify.base_premise(base)
    cover=json.loads((HERE/'covers/phase-170.json').read_text())
    root=cover['chains'][0]['root']
    stage=json.loads((HERE/cover['chains'][0]['certificates'][0]).read_text())
    def badbase(label,change):
        data=deepcopy(rawbase);change(data);path=work/'bad-base.json';path.write_text(json.dumps(data)+'\n')
        reject(label,lambda:verify.base_premise(path))
    for key,value in [('N',3705),('terms',6),('seam',1851),('g',2),('denominator',True),('denominator',0),('s',True),('t',447)]:
        badbase('base '+key+'='+str(value),lambda d,k=key,v=value:d.__setitem__(k,v))
    badbase('base hidden candidate restriction',lambda d:d.__setitem__('forced',[]))
    badbase('base duplicate AP',lambda d:d['color0_APs'].append(d['color0_APs'][0]))
    for index,value in [(0,True),(1,0),(1,-1),(2,0),(2,True),(2,1.0),(2,-1)]:
        badbase('base row '+str((index,value)),lambda d,i=index,v=value:d['color0_APs'][0].__setitem__(i,v))
    badbase('base full point capacity violation',lambda d:d['color0_APs'][0].__setitem__(2,d['denominator']+1))
    def badstage(label,change):
        d=deepcopy(stage);change(d)
        reject(label,lambda:verify.check_stage(d,colors,V[1],170,root))
    for key,value in [('phase',171),('phase',170.0),('root',True),('root',root+1),
                      ('denominator',0),('denominator',True),('domain_sha256','0'*64),('format','bad')]:
        badstage('stage '+key+'='+str(value),lambda d,k=key,v=value:d.__setitem__(k,v))
    for key,value in [('forced',[]),('permitted_screen',sorted(V[1])[:-1]),('trial_opposite',1853)]:
        badstage('stage hidden '+key,lambda d,k=key,v=value:d.__setitem__(k,v))
    badstage('stage duplicate AP',lambda d:d['AP_weights'].append(d['AP_weights'][0]))
    for index,value in [(0,False),(1,0),(2,0),(2,True),(2,0.5)]:
        badstage('stage row '+str((index,value)),lambda d,i=index,v=value:d['AP_weights'][0].__setitem__(i,v))
    badstage('stage original0 AP as opposite mandatory AP',lambda d:d['AP_weights'].__setitem__(0,rawbase['color0_APs'][0]))
    badstage('stage full inherited point capacity violation',lambda d:d['AP_weights'][0].__setitem__(2,2*d['denominator']))
    badstage('stage forbidden-point surcharge',lambda d:d['surcharges'].append([next(x for x in range(3704) if colors[x]!=1),1]))
    badstage('stage boolean surcharge',lambda d:d['surcharges'].append([min(V[1]),True]))
    ap=stage['AP_weights'][0][:2]
    badstage('stage duplicate triple APs',lambda d:d['bundle_weights'].append([[ap,ap,ap],1]))
    common={}
    for a,d,w in stage['AP_weights']:
        for x in verify.actual_ap(a,d)&V[1]:common.setdefault(x,[]).append([a,d])
    triple=next(t[:3] for t in common.values() if len(t)>=3)
    badstage('stage false cover2 triple with common point',lambda d:d['bundle_weights'].append([triple,1]))
    empty={'format':'QR617_ACTIVATED_EMPTY_PETAL_1','phase':170,'root':root,
           'domain_sha256':verify.domain_sha(V[1]),'AP':ap}
    reject('false empty mandatory petal',lambda:verify.check_stage(empty,colors,V[1],170,root))

    def badcover(label,s,change,docchange=None,nozero=False):
        c=json.loads((HERE/f'covers/phase-{s}.json').read_text())
        docs={ch['root']:[json.loads((HERE/fn).read_text()) for fn in ch['certificates']] for ch in c['chains']}
        change(c)
        if docchange:docchange(docs)
        tree=HERE/f'old-trees/phase-{s}.json' if s in [184,205] and not nozero else None
        reject(label,lambda:verify.check_cover(HERE/f'base/phase-{s}.json',c,HERE,docs,tree))
    badcover('cover missing anchor root',170,lambda c:c['chains'].pop())
    badcover('cover duplicate anchor root',170,lambda c:c['chains'].append(deepcopy(c['chains'][0])))
    badcover('cover wrong anchor',170,lambda c:c.__setitem__('anchor',[198,552]))
    badcover('cover wrong class caps',170,lambda c:c.__setitem__('caps',[197,198]))
    badcover('cover floating caps',170,lambda c:c.__setitem__('caps',[197.0,197]))
    badcover('cover hidden fixed point',170,lambda c:c.__setitem__('forced',[197]))
    low=deepcopy(stage);low.update(AP_weights=[],bundle_weights=[],surcharges=[])
    verify.need(not verify.check_stage(low,colors,V[1],170,root)['exclusion'], 'Valid zero-weight packing is inconclusive')
    badcover('valid nonpositive final stage is not a completed proof',170,lambda c:None,
             lambda docs:docs[root].__setitem__(0,low))
    badcover('cover omitted refinement stage',174,
             lambda c:next(ch for ch in c['chains'] if ch['root']==1964)['certificates'].pop(1),
             lambda docs:docs[1964].pop(1))
    badcover('cover reversed refinement stages',174,
             lambda c:next(ch for ch in c['chains'] if ch['root']==1964)['certificates'].reverse(),
             lambda docs:docs[1964].reverse())
    badcover('cover extra stage after contradiction',170,
             lambda c:c['chains'][0]['certificates'].append(c['chains'][0]['certificates'][0]),
             lambda docs:docs[root].append(deepcopy(docs[root][0])))
    badcover('phase184 omitted zero-loss premise',184,lambda c:None,nozero=True)

    tree0=json.loads((HERE/'old-trees/phase-184.json').read_text())
    def badtree(label,change):
        data=deepcopy(tree0);change(data);p=work/'bad-tree.json';p.write_text(json.dumps(data)+'\n')
        reject(label,lambda:verify.base_premise(HERE/'base/phase-184.json',p))
    badtree('old tree missing complete branch',lambda t:t['tree'].pop('edited'))
    badtree('old tree wrong base hash',lambda t:t.__setitem__('base_certificate_sha256','0'*64))
    badtree('old tree wrong cap',lambda t:t.__setitem__('class_cap',197))
    badtree('old tree hidden state',lambda t:t['tree'].__setitem__('forced',[]))
    r184=next(r for r in cases if r['phase']==184)
    k0=min(r184['zero_loss_premise']['fixed_positions'][0])
    badtree('old tree split outside necessary screen',lambda t:t['tree'].__setitem__('split',k0))
    badtree('old tree repeated inherited split',lambda t:t['tree']['edited'].__setitem__('split',t['tree']['split']))
    badtree('old leaf boolean AP weight',lambda t:t['tree']['unchanged']['leaf']['color0_APs'][0].__setitem__(2,True))
    leaf=r184['zero_loss_premise']['leaves'][0]['colors'][0]
    increase=leaf['strict_gap_numerator']//196+1
    verify.need(leaf['old_gap_numerator']-196*increase>0, 'Damaged leaf still excludes the old cap196 case')
    badtree('old cap196 proof insufficient after a removed zero edit',
            lambda t:t['tree']['unchanged']['leaf'].__setitem__('denominator',leaf['denominator']+increase))

    def badcombine(label,change_imports=lambda d:None,change_cases=lambda d:None):
        d=deepcopy(imports);r=deepcopy(cases);change_imports(d);change_cases(r)
        reject(label,lambda:check_all.combine(d,r))
    badcombine('global missing new phase',change_cases=lambda r:r.pop())
    badcombine('global duplicated new phase',change_cases=lambda r:r.__setitem__(-1,deepcopy(r[0])))
    badcombine('global incomplete old profile',lambda d:d['base_profile'].__setitem__('complete',False))
    badcombine('global missing strong phase',lambda d:d['base_profile']['per_phase_lower_bound_each_color'].__setitem__(0,197))
    badcombine('global boolean old floor',lambda d:d['base_profile']['per_phase_lower_bound_each_color'].__setitem__(0,True))
    badcombine('global wrong prior197 upgrade set',lambda d:d['individual197'].__setitem__('phases',[184,201,205]))
    badcombine('global prior269 box has wrong caps',lambda d:d['joint269'].__setitem__('excluded_original_class_caps',[197,198]))
    badcombine('global prior201 assumed candidate symmetry',lambda d:d['joint201'].__setitem__('candidate_symmetry_assumed',True))
    badcombine('global new case has wrong old base floor',change_cases=lambda r:r[0].__setitem__('base_floor_per_class',198))
    badcombine('global new case has no individual197 floor',change_cases=lambda r:r[0].__setitem__('proved_individual_floor_per_class',196))
    badcombine('global new case has candidate symmetry',change_cases=lambda r:r[0].__setitem__('candidate_symmetry_assumed',True))
    badmanifest=deepcopy(manifest);badmanifest['dependencies'][0]['sha256']='0'*64
    reject('global replaced dependency digest',lambda:check_all.dependencies(badmanifest))

    activation=0
    for flags in itertools.product((0,1),repeat=6):
        final=[1]+[1-b for b in flags]
        verify.need((len(set(final))==1)==(sum(flags)==0), 'Exact sole-root activation requires a compensating opposite edit')
        activation+=1
    anchor_models=0
    for c in manifest['cases']:
        tree=HERE/c['zero_tree'] if c['zero_tree'] else None
        cc,VV,_=verify.base_premise(HERE/c['base'],tree)
        cv=json.loads((HERE/c['cover']).read_text());A=verify.actual_ap(*cv['anchor']);roots=sorted(A&VV[0])
        for bits in itertools.product((0,1),repeat=len(roots)):
            E={x for x,b in zip(roots,bits) if b}
            verify.need((all(int(x in E)==0 for x in A))==(not E), 'Actual anchor needs at least one permitted edit')
            anchor_models+=1
    clipping=0
    for loads in itertools.product(range(5),repeat=3):
        D=2;gamma=sum(max(0,L-D) for L in loads)
        for bits in itertools.product((0,1),repeat=3):
            E=[i for i,b in enumerate(bits) if b]
            for cap in range(len(E),4):
                for W in range(sum(loads[i] for i in E)+1):
                    clipped=sum(min(loads[i],D) for i in E)
                    verify.need(clipped>=W-gamma, 'Surcharged clipped load inequality')
                    delta=cap*D-(W-gamma)
                    verify.need(delta>=0 and all(D-min(loads[i],D)<=delta for i in E), 'Each edited point lies in the safe clipped screen')
                    clipping+=1
    zero_models=0
    sets=[{i for i,b in enumerate(bits) if b} for bits in itertools.product((0,1),repeat=3) if any(bits)]
    for petals in itertools.product(sets,repeat=3):
        if set.intersection(*petals):continue
        U=set.union(*petals)
        for zbits in itertools.product((0,1),repeat=3):
            k=sum(zbits);ell=2 if k==3 else int(k>0)
            for H in [set()]+sets:
                if any(not z and not(p&H) for p,z in zip(petals,zbits)):continue
                for T in [set()]+sets:
                    if not T<=H:continue
                    b=max(0,2-len(U&T))
                    verify.need(len((H-T)&U)>=b-min(b,ell), 'Removed-zero residual triple RHS loss')
                    zero_models+=1
    return {'success':True,'python_optimization':sys.flags.optimize,'corruptions_rejected':len(rejected),
            'rejected_controls':rejected,'sole_root_activation_models':activation,
            'actual_anchor_models':anchor_models,'clipped_capacity_models':clipping,
            'removed_zero_triple_models':zero_models}


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--output',type=Path)
    a=p.parse_args();out=run(a.work)
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':main()
