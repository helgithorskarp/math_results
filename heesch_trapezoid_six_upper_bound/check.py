#!/usr/bin/env python3
"""Regenerate the complete neighborhood models proving the curved tile's upper6.

Standard library only. This reader uses relative exact geometry and bit-mask
arc consistency/direct frontier products, distinct from discovery's global
geometry, full Cartesian first-model census and MRV prefix DFS. Published
geometry and all earlier proof readers are disclosed byte-pinned reuse.
"""
import argparse
from collections import Counter
import copy
from functools import lru_cache
import hashlib
import importlib.util
import itertools
import json
from math import prod
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError('Pinned parents require assertions; -O is unsupported')
HERE=Path(__file__).resolve().parent
ROOT=(0,0,0,0)

def require(value,message):
    if not value:raise ValueError(message)

def canonical(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def context(repo):
    pins=json.loads((HERE/'dependency_pins.json').read_text())
    for path,digest in pins.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'Changed dependency: '+path)
    directory=repo/'heesch_trapezoid_prefix_rigidity'
    reader=load_module('published_fifteen_reader',directory/'check.py')
    ctx=reader.context(repo)
    data=json.loads((directory/'input.json').read_text())
    report=reader.run(data,json.loads((directory/'certificate.json').read_text()),ctx)
    require(reader.canonical(report)==reader.canonical(json.loads((directory/'expected.json').read_text())),
            'The fifteen-family proof does not replay')
    parent,g,base,_,_=ctx
    ids=tuple(data['remaining_subset_indices'])
    poses=tuple(map(tuple,base['candidate_poses']))
    families={i:frozenset((ROOT,)+tuple(poses[v-1] for v in base['necessary_subsets'][i])) for i in ids}
    return g,base,report,ids,families

class Geometry:
    def __init__(self,g,families):
        self.g=g;self.families=families
        self.root_vertices=frozenset(g.V)
        self.root_positive=self.positives(ROOT)

    @lru_cache(maxsize=20000)
    def inverse(self,p):
        a,b=self.g.MATRICES[p[:2]]
        det=a[0]*b[1]-a[1]*b[0]
        require(det in (-1,1),'Nonunimodular orientation')
        columns=((b[1]//det,-a[1]//det),(-b[0]//det,a[0]//det))
        keys=[k for k,v in self.g.MATRICES.items() if v==columns]
        require(len(keys)==1,'Missing inverse D6 orientation')
        t=((b[0]*p[3]-b[1]*p[2])//det,(a[1]*p[2]-a[0]*p[3])//det)
        q=(*keys[0],*t)
        require(self.g.compose(q,p)==self.g.compose(p,q)==ROOT,'Wrong inverse pose')
        return q

    @lru_cache(maxsize=100000)
    def relative(self,a,b):return self.g.compose(self.inverse(a),b)

    @lru_cache(maxsize=20000)
    def positives(self,p):
        return frozenset(tuple(sorted((a,b))) for a,b,j,s in self.g.chords(p) if s==1)

    @lru_cache(maxsize=20000)
    def relative_contact(self,p):
        return bool(self.root_vertices & frozenset(self.g.image(v,p) for v in self.g.V))

    def contact(self,a,b):return self.relative_contact(self.relative(a,b))

    @lru_cache(maxsize=20000)
    def relative_conflict(self,p):
        if p==ROOT:return False
        if self.g.overlap(self.g.quad(ROOT),self.g.quad(p),True):return True
        return bool(self.root_positive & self.positives(p))

    def conflict(self,a,b):return self.relative_conflict(self.relative(a,b))

    @lru_cache(maxsize=20000)
    def family(self,a,i):return frozenset(self.g.compose(a,p) for p in self.families[i])

    def domain(self,c,a,allowed):
        answer=[]
        for i in allowed:
            f=self.family(a,i)
            if any(self.contact(a,p) for p in c-f):continue
            if any(self.contact(ROOT,p) for p in f-c):continue
            if any(self.conflict(p,q) for p in f for q in c):continue
            answer.append(i)
        return tuple(answer)

    @lru_cache(maxsize=100000)
    def compatible(self,a,i,b,j):
        f=self.family(a,i);h=self.family(b,j)
        if any(self.contact(b,p) for p in f-h):return False
        if any(self.contact(a,p) for p in h-f):return False
        return not any(self.conflict(p,q) for p in f for q in h)

def bit_values(mask):
    while mask:
        low=mask&-mask
        yield low.bit_length()-1
        mask-=low

def first_models(geom,ids):
    """Finite binary CSP using bit-mask arc consistency and lexical branching."""
    result=[];domain_reports=[]
    for root_type in ids:
        c=geom.families[root_type];anchors=tuple(sorted(c))
        domains=tuple(geom.domain(c,a,ids) for a in anchors)
        supports={}
        for a in range(len(anchors)):
            for b in range(len(anchors)):
                if a==b:continue
                supports[a,b]=tuple(sum(1<<j for j,v in enumerate(domains[b])
                    if geom.compatible(anchors[a],u,anchors[b],v)) for u in domains[a])
        masks=tuple((1<<len(d))-1 for d in domains)
        def consistent(values):
            current=list(values);changed=True
            while changed:
                changed=False
                for a in range(len(anchors)):
                    keep=current[a]
                    for x in bit_values(current[a]):
                        if any(not(supports[a,b][x]&current[b]) for b in range(len(anchors)) if a!=b):
                            keep&=~(1<<x)
                    if not keep:return None
                    if keep!=current[a]:current[a]=keep;changed=True
            return tuple(current)
        answers=[]
        def enumerate_masks(values):
            current=consistent(values)
            if current is None:return
            branch=next((a for a,v in enumerate(current) if v&(v-1)),None)
            if branch is None:
                answers.append(tuple(domains[a][next(bit_values(v))] for a,v in enumerate(current)))
                return
            for bit in bit_values(current[branch]):
                child=list(current);child[branch]=1<<bit;enumerate_masks(tuple(child))
        enumerate_masks(masks)
        require(len(set(answers))==len(answers),'Duplicate neighborhood assignment')
        result.extend((root_type,v) for v in sorted(answers))
        domain_reports.append({'first_index':root_type,'receivers':len(anchors),
            'domain_sizes':[len(d) for d in domains],'prepropagation_products':prod(len(d) for d in domains),
            'models':len(answers)})
    return tuple(sorted(result)),domain_reports

def height5_third(geom,models,k4):
    """Direct frontier products after checking every fixed-neighborhood choice."""
    catalog=[];second_states=[];third_reports=[]
    for root_type,vector in models:
        if not set(vector)<=set(k4):continue
        anchors=tuple(sorted(geom.families[root_type]))
        fixed=dict(zip(anchors,vector))
        second=frozenset(q for a,i in fixed.items() for q in geom.family(a,i))
        second_states.append((root_type,tuple(sorted(second)),tuple(sorted(fixed.items()))))
        new=tuple(sorted(second-set(anchors)))
        domains=[]
        for a in new:
            candidates=geom.domain(second,a,tuple(geom.families))
            domains.append(tuple(i for i in candidates if all(geom.compatible(a,i,b,j) for b,j in fixed.items())))
        bad_pairs={}
        for a,b in itertools.combinations(range(len(new)),2):
            bad_pairs[a,b]=frozenset((i,j) for i in domains[a] for j in domains[b]
                                    if not geom.compatible(new[a],i,new[b],j))
        checked=0;survivors=[];families=[]
        for choices in itertools.product(*domains):
            checked+=1
            if any((choices[a],choices[b]) in bad for (a,b),bad in bad_pairs.items()):continue
            assignments=tuple(sorted(tuple(fixed.items())+tuple(zip(new,choices))))
            third=frozenset(q for a,i in assignments for q in geom.family(a,i))
            survivors.append(assignments);families.append(tuple(sorted(third)))
            catalog.append((root_type,tuple(sorted(third))))
        require(checked==prod(len(d) for d in domains),'Incomplete frontier Cartesian product')
        # Keep every assignment before comparing pose catalogs. No state is lost
        # by trusting discovery's deduplication or arbitrary representative.
        third_reports.append({'first_index':root_type,'second_sha256':canonical(sorted(second)),
            'second_copies':len(second),'new_receivers':len(new),
            'products_after_fixed_constraints':checked,'assignment_models':len(survivors),
            'distinct_third_families':len(set(families))})
    require(len(set(second_states))==len(second_states),'Duplicate second state')
    require(len(set(catalog))==len(catalog),'Different frontier assignments have the same third family')
    return tuple(sorted(catalog)),third_reports

def refined_types(models,allowed):
    return tuple(sorted({i for i,v in models if i in allowed and set(v)<=set(allowed)}))

def run(data,certificate,ctx):
    g,base,parent_report,ids,families=ctx
    require(tuple(data['root'])==ROOT,'Wrong normalized root')
    require(data['required_local_surrounds']==3,'Three further surrounds are required for the local theorem')
    require(data['height_five']==5 and data['classified_prefix']==3 and data['two_outer_prefixes_remaining']==2,
            'Incorrect future-depth guard for the third-prefix census')
    require(data['claimed_upper']==6,'Wrong claimed numerical bound')
    require(tuple(data['local_type_indices'])==ids,'Missing or altered local neighborhood type')
    geom=Geometry(g,families)
    models,domains=first_models(geom,ids)
    require(canonical(models)==canonical(certificate['first_neighborhood_models']),'The full first-neighborhood model catalog differs')
    k4=refined_types(models,ids)
    k5_coarse=refined_types(models,k4)
    third,third_reports=height5_third(geom,models,k4)
    require(canonical(third)==canonical(certificate['height5_third_prefixes']),'The complete height-five third-prefix catalog differs')
    k5=tuple(sorted({i for i,c in third}))
    k6=refined_types(models,k5)
    k7=refined_types(models,k6)
    derived={'3':ids,'4':k4,'5_coarse':k5_coarse,'5':k5,'6':k6,'7':k7}
    require(canonical(derived)==canonical(certificate['types_at_depth']),'Unsupported local-type elimination')
    require(not k7,'Seven-corona obstruction was not established')
    witness=base['positive_four_corona_witness']
    packed=frozenset(tuple(r['pose']) for r in witness)
    known_first=frozenset(tuple(r['pose']) for r in witness if r['level']<=1)
    known_second=frozenset(tuple(r['pose']) for r in witness if r['level']<=2)
    known_third=tuple(sorted(tuple(r['pose']) for r in witness if r['level']<=3))
    require(known_first==families[0],'Known positive first family changed')
    a=tuple(sorted(known_first));positive=[]
    for i in a:
        selected=[j for j in ids if geom.family(i,j)<=packed]
        require(len(selected)==1,'Known positive neighborhood is not unique')
        positive.append(selected[0])
    require((0,tuple(positive)) in models,'Known four-corona control pruned')
    require(frozenset(q for i,j in zip(a,positive) for q in geom.family(i,j))==known_second,
            'Known second control not reproduced')
    require((0,known_third) in third,'Known third positive control omitted from the necessary height-five catalog')
    first_counts=Counter(i for i,v in models)
    third_counts=Counter(i for i,c in third)
    return {'agent':'six-heesch-3','role':'researcher',
        'claim':'The identical unmarked curved Euclidean Jordan disc has4<=Hc<=Hh<=6; no arbitrary-topology seven-corona chain exists.',
        'types_at_depth':derived,'first_neighborhood_models':len(models),'first_model_counts':dict(first_counts),
        'first_domain_census':domains,'height5_second_states':len(third_reports),
        'height5_third_models':len(third),'height5_third_first_counts':dict(third_counts),
        'third_model_census':third_reports,'first_raw_products':sum(r['prepropagation_products'] for r in domains),
        'third_products_after_fixed_constraints':sum(r['products_after_fixed_constraints'] for r in third_reports),
        'positive_control':{'first_index':0,'second_copies':len(known_second),'third_copies':len(known_third),
            'entire_four_coronas_replayed':parent_report['parent_replay']['positive_four_coronas']},
        'catalogs_sha256':canonical({'first':models,'third':third}),
        'input_sha256':canonical(data),'certificate_sha256':canonical(certificate),
        'trust_boundary':'Written contact-interiority/contact-graph-ball re-rooting and finite model necessity, exact Python, and byte-pinned prior geometry/certificates. No native solver, grid-window assumption, formalization, independent peer verdict or new lower construction.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,default=HERE.parent)
    parser.add_argument('--expected',type=Path);parser.add_argument('--controls',action='store_true')
    args=parser.parse_args();ctx=context(args.repo_root)
    data=json.loads((HERE/'input.json').read_text());certificate=json.loads((HERE/'certificate.json').read_text())
    answer=run(data,certificate,ctx)
    if args.expected:require(canonical(answer)==canonical(json.loads(args.expected.read_text())),'Expected output differs')
    print(json.dumps(answer,indent=2))
    if args.controls:
        tests=[]
        bad=copy.deepcopy(data);bad['local_type_indices'].pop();tests.append(('omitted_local_type',bad,certificate))
        bad=copy.deepcopy(data);bad['required_local_surrounds']=2;tests.append(('discarded_future_surround',bad,certificate))
        bad=copy.deepcopy(certificate);bad['first_neighborhood_models'].pop();tests.append(('omitted_first_model',data,bad))
        bad=copy.deepcopy(certificate);bad['height5_third_prefixes'].pop();tests.append(('omitted_third_model',data,bad))
        bad=copy.deepcopy(certificate);bad['height5_third_prefixes'][0][1][0][2]+=1;tests.append(('changed_whole_pose',data,bad))
        bad=copy.deepcopy(certificate);bad['types_at_depth']['6']=[17];tests.append(('false_type_elimination',data,bad))
        for name,bad_data,bad_certificate in tests:
            try:run(bad_data,bad_certificate,ctx)
            except (ValueError,AssertionError):print(json.dumps({'control':name,'status':'rejected'}))
            else:raise ValueError('Malformed control accepted: '+name)

if __name__=='__main__':main()
