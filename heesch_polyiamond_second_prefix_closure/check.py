"""Exact centroid and bit-mask RUP replay of a local T214 obstruction.

six-heesch-2, researcher. No 48-copy fixed premise, discovery inventory,
extractor, native solver, dense formula or DRAT is used. Disclosed pinned
older geometry/pattern routines and the 38 pair lemmas remain dependencies.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

BASE=Path(__file__).resolve().parent
PUB=BASE.parent
PARENT=PUB/'heesch_polyiamond_third_prefix_closure'
PINS={
    'check.py':'13704f116b806d27922c6bebdeba0ea5a5f3c5a3e7fc3f41bb55b43b9436c661',
    'five-pattern.json':'3027469bb374bd8864d50b7c9facfdb221e1a37369c0229cb1de2075ec3b40b1',
    'corner-pattern.json':'f75a4703f555379a505d24e84895bcb12144ab2fe01ef76512fa66f602fe5887',
    'caps.json':'2e6d3e66fa7447a2ff22ad3433054d0c3eba156777ec779405954f47776d0f2f',
}


def need(ok,message):
    if not ok:raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def context():
    for name,digest in PINS.items():
        need(hashlib.sha256((PARENT/name).read_bytes()).hexdigest()==digest,('parent bytes',name))
    r=load(PARENT/'check.py','pinned_three_surround_geometry')
    for path,digest in r.PINS.items():
        # This old positive fixture is not a premise or input of the local proof.
        if path.endswith('escape-both-witness.json'):continue
        need(hashlib.sha256((PUB/path).read_bytes()).hexdigest()==digest,('older bytes',path))
    f=load(PUB/'heesch_polyiamond_six_copy_obstruction/check.py','pinned_six_helpers')
    h,c=f.helpers()
    data=read(PUB/'heesch_polyiamond_deficit_review1/input.json')
    g=c.Geometry(c.shape(data['side_signs']))
    need(len(g.fs)==214,'prototype size')
    catalogue,trials,gaps=g.anchor_pool(g.pockets)
    need(len(catalogue)==59 and len(set(data['retained_indices']))==21,'pair catalogue')
    excluded={q for i,q in enumerate(catalogue,1) if i not in data['retained_indices']}
    single=read(PUB/'heesch_polyiamond_fixed_fourth_extension/patterns.json')
    single.append(read(PUB/'heesch_polyiamond_fixed_third_extension/hole.json'))
    single.extend(read(PUB/'heesch_polyiamond_alternate_fourth/patterns.json'))
    single.append(read(PUB/'heesch_polyiamond_six_copy_obstruction/single-gap.json'))
    single.append(read(PARENT/'corner-pattern.json'))
    single_checks=r.verify_patterns(f,h,c,g,single)
    five=read(PARENT/'five-pattern.json')
    six=read(PUB/'heesch_polyiamond_six_copy_obstruction/pattern.json')
    two_checks={'five':r.local_two(f,h,c,g,excluded,single,five),
                'six':r.local_two(f,h,c,g,excluded,single,six)}
    caps,cap_check=r.cap_family(f,c,g,catalogue,excluded,read(PARENT/'caps.json'))
    tables=[('single_surround_pattern',single),('two_surround_five_pattern',[five]),
            ('two_surround_six_pattern',[six]),('two_surround_cap_pattern',caps)]
    return r,f,h,c,g,excluded,tables,{'single':single_checks,'two':two_checks,
                                    'cap_count':cap_check['retained_caps'],
                                    'old_pair_catalogue':[len(catalogue),len(excluded),trials,gaps]}


def encode(row,n):
    need(len(row)==len(set(row)) and all(type(v)is int and 1<=abs(v)<=n for v in row),'literal encoding')
    positive=negative=0
    for v in row:
        if v>0:positive|=1<<(v-1)
        else:negative|=1<<(-v-1)
    return positive,negative


def conflict(clauses):
    yes=no=0;steps=0
    while True:
        changed=False
        for i,(positive,negative) in enumerate(clauses):
            if positive&yes or negative&no:continue
            unknown=~(yes|no)
            p=positive&unknown;q=negative&unknown
            remaining=p|q
            if not remaining:return i,steps
            if remaining.bit_count()==1:
                if p:yes|=p
                else:no|=q
                changed=True;steps+=1
        if not changed:return None,steps


def rup(cert):
    n=len(cert['providers']);clauses=[encode(row,n) for row in cert['clauses']]
    need(cert['rup_lemmas'] and cert['rup_lemmas'][-1]==[],'no final empty lemma')
    report=[]
    for lemma in cert['rup_lemmas']:
        encoded=encode(lemma,n)
        assumptions=[encode([-v],n) for v in lemma]
        where,steps=conflict(clauses+assumptions)
        need(where is not None,('RUP implication fails',lemma))
        report.append({'clause':lemma,'unit_steps':steps,'conflict_clause':where})
        clauses.append(encoded)
    return report


def check(cert,ctx=None):
    need(cert['kind']=='three_surround_obstruction' and cert['tile']=='T214' and
         type(cert.get('surrounds'))is int and cert['surrounds']==3,'three-stage scope')
    r,f,h,c,g,excluded,tables,dependencies=ctx if ctx is not None else context()
    fixed=[r.pose(row) for row in cert['poses']]
    providers=[tuple(q) for q in cert['providers']]
    r.valid_poses(g,fixed);r.valid_poses(g,providers)
    for row in cert['cover_targets']:
        need(len(row['vertex'])==len(row['required_centroid'])==2 and
             all(type(v)is int for v in row['vertex']+row['required_centroid']),
             'integral local cover coordinates')
    need(fixed and fixed[0]==c.IDENTITY,'normalized fixed anchor')
    occupied=g.union(fixed)
    need(all(not g.footprint(q)&occupied for q in providers),'provider overlaps fixed premise')
    cover_ids,census=r.covers(f,c,g,fixed,providers,cert)
    counts=r.negative_clauses(h,c,g,fixed,providers,cert,cover_ids,excluded,tables)
    proof=rup(cert)
    return {'agent':'six-heesch-2','role':'researcher','fixed_copies':len(fixed),
            'fixed_faces':len(occupied),'providers':len(providers),'clauses':len(cert['clauses']),
            'complete_covers':census,'clause_counts':counts,'rup_lemmas':proof,
            'dependencies_rechecked':dependencies,'three_surround_contradiction_verified':True,
            'scope':'specified finite copy pattern has no three strict surrounds under arbitrary real motions and topology'}


def forward(cert):
    n=len(cert['providers']);clauses=[encode(row,n) for row in cert['clauses']]
    yes=no=0
    for step in cert['steps']:
        literal,reason=step['literal'],step['reason']
        need(type(literal)is int and 1<=abs(literal)<=n and type(reason)is int and
             0<=reason<len(clauses),'unit step encoding')
        bit=1<<(abs(literal)-1)
        need(not bit&(yes|no),'repeated forward assignment')
        positive,negative=clauses[reason]
        need(not positive&yes and not negative&no,'satisfied unit reason')
        remaining=(positive|negative)&~(yes|no)
        need(remaining==bit and bool(positive&bit)==(literal>0),'invalid forward unit')
        if literal>0:yes|=bit
        else:no|=bit
    targets=cert['forced_provider_indices']
    need(len(targets)==len(set(targets)) and all(type(i)is int and 1<=i<=n and
         yes&(1<<(i-1)) for i in targets),'unproved forced third copies')
    return yes,no


def rigidity(cert,local,ctx=None):
    """The caller checks the local three-surround proof first, as main does."""
    need(cert['kind']=='conditional_third_prefix_rigidity' and cert['tile']=='T214' and
         type(cert.get('future_surrounds_required'))is int and cert['future_surrounds_required']==2,
         'rigidity requires two future surrounds')
    r,f,h,c,g,excluded,tables,_=ctx if ctx is not None else context()
    fixed=[r.pose(row) for row in cert['fixed_poses']]
    providers=[tuple(q) for q in cert['providers']]
    r.valid_poses(g,fixed);r.valid_poses(g,providers)
    for row in cert['cover_targets']:
        need(len(row['vertex'])==len(row['required_centroid'])==2 and
             all(type(v)is int for v in row['vertex']+row['required_centroid']),
             'integral rigidity cover coordinates')
    need(len(fixed)==18 and fixed[0]==c.IDENTITY,'specified second-prefix normalization')
    occupied=g.union(fixed)
    need(all(not g.footprint(q)&occupied for q in providers),'rigidity provider overlaps premise')
    cover_ids,census=r.covers(f,c,g,fixed,providers,cert)
    # These copies have only one guaranteed surround after the new layer.
    single=[row for row in tables if row[0]=='single_surround_pattern']
    counts=r.negative_clauses(h,c,g,fixed,providers,cert,cover_ids,excluded,single)
    yes,no=forward(cert)
    forced=[providers[i-1] for i in cert['forced_provider_indices']]
    need(len(forced)==28,'28 first-stage forced copies')
    partial=g.union(fixed+forced)
    old_vertices={v for face in occupied for v in c.vertices(face)}
    terminal=[];added=[]
    for row in cert['terminal_targets']:
        vertex=tuple(row['vertex']);required=tuple(row['required_centroid'])
        need(len(vertex)==len(required)==2 and all(type(v)is int for v in vertex+required),
             'terminal coordinates')
        need(vertex in old_vertices,'terminal point belongs only to a selected copy')
        raw,allowed,joins,sectors=f.cover(c,g,partial,vertex,required)
        provider=tuple(row['provider']);r.valid_poses(g,[provider])
        need(sectors==5 and len(raw)==22 and allowed==[provider],'terminal list not complete/unique')
        added.append(provider)
        terminal.append({'vertex':list(vertex),'required_centroid':list(required),
                         'centroid_joins':joins,'raw_providers':len(raw),'provider':list(provider)})
    need(len(added)==2 and len(set(added))==2 and not set(added)&set(forced),'two new terminal copies')
    third=[tuple(q) for q in cert['forced_third_poses']]
    r.valid_poses(g,third)
    need(len(third)==30 and set(forced+added)==set(third),'forced third layer differs')
    whole=fixed+third;union=g.union(whole)
    need(all(set(c.star(v))<=union for v in old_vertices),'incomplete old full halo')
    second_mesh,_=c.mesh(occupied);third_mesh,_=c.mesh(union)
    relative_path='heesch_polyiamond_forced_pair/escape-both-witness.json'
    need(hashlib.sha256((PUB/relative_path).read_bytes()).hexdigest()==r.PINS[relative_path],
         'named positive prefix bytes')
    layers,positive=r.positive(c,g)
    need(set(fixed)==set(q for layer in layers[:3] for q in layer) and set(third)==set(layers[3]),
         'different named second/third prefixes')
    relative=[r.pose(row) for row in local['poses']]
    instances=[anchor for anchor in whole if all(c.compose(anchor,q) in set(whole) for q in relative)]
    need(instances,'forced third prefix misses the proved local obstruction')
    return {'fixed_second_copies':len(fixed),'providers':len(providers),'clauses':len(cert['clauses']),
            'unit_steps':len(cert['steps']),'true_units':yes.bit_count(),'false_units':no.bit_count(),
            'initial_forced_copies':len(forced),'terminal_forced_copies':len(added),
            'total_forced_third_copies':len(third),'complete_covers':census,'clause_counts':counts,
            'complete_terminal_censuses':terminal,'old_full_halo_verified':True,
            'second_mesh':second_mesh,'forced_third_mesh':third_mesh,
            'local_obstruction_anchors':[list(q) for q in instances],
            'positive_four_coronas':positive,'rigidity_verified':True,
            'all_sixth_continuations_excluded':True,
            'scope':'fixed alternative second prefix forces the specified third subset under two surrounds and has no four further real surrounds'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pattern',type=Path,default=BASE/'local-pattern.json')
    ap.add_argument('--expected',type=Path)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--controls',action='store_true')
    ap.add_argument('--rigidity',type=Path,default=BASE/'rigidity.json')
    args=ap.parse_args();start=time.monotonic()
    cert=read(args.pattern);ctx=context();out=check(cert,ctx)
    rigid=read(args.rigidity) if args.rigidity else None
    if rigid is not None:out['alternate_second_rigidity']=rigidity(rigid,cert,ctx)
    if args.controls:
        names=['shifted_fixed_blocker','omitted_provider','truncated_cover','false_rup_unit','wrong_future_stage']
        for name in names:
            bad=copy.deepcopy(cert)
            if name=='shifted_fixed_blocker':bad['poses'][-1]['translation'][0]+=40
            elif name=='omitted_provider':bad['providers'].pop()
            elif name=='truncated_cover':bad['clauses'][bad['cover_targets'][0]['clause']].pop()
            elif name=='false_rup_unit':bad['rup_lemmas'][0]=[2]
            else:bad['surrounds']=2
            try:check(bad,ctx)
            except ValueError:continue
            raise ValueError(('malformed control accepted',name))
        out['rejected_controls']=names
        if rigid is not None:
            names=['flipped_rigidity_unit','deleted_terminal_provider','selected_only_terminal_point','wrong_rigidity_stage']
            for name in names:
                bad=copy.deepcopy(rigid)
                if name=='flipped_rigidity_unit':bad['steps'][0]['literal']*=-1
                elif name=='deleted_terminal_provider':bad['forced_third_poses'].pop()
                elif name=='selected_only_terminal_point':
                    r,f,h,c,g,_,_,_=ctx
                    old=g.union([r.pose(row) for row in rigid['fixed_poses']])
                    old_vertices={v for face in old for v in c.vertices(face)}
                    fixed=[r.pose(row) for row in rigid['fixed_poses']]
                    forced=[tuple(rigid['providers'][i-1]) for i in rigid['forced_provider_indices']]
                    partial=g.union(fixed+forced)
                    new_vertices={v for face in partial for v in c.vertices(face)}-old_vertices
                    choices=[v for v in sorted(new_vertices) if sum(face in partial for face in c.star(v))==5]
                    need(choices,'no selected-only test vertex')
                    vertex=choices[0];required=next(face for face in c.star(vertex) if face not in partial)
                    bad['terminal_targets'][0]['vertex']=list(vertex)
                    bad['terminal_targets'][0]['required_centroid']=list(required)
                else:bad['future_surrounds_required']=1
                try:rigidity(bad,cert,ctx)
                except ValueError:continue
                raise ValueError(('malformed rigidity control accepted',name))
            out['rejected_rigidity_controls']=names
    if args.expected:need(out==read(args.expected),'expected output differs')
    text=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')
    print(json.dumps({'seconds':round(time.monotonic()-start,3),
                      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__=='__main__':main()
