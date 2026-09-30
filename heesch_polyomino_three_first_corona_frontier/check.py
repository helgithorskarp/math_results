"""P17: three necessary complete first prefixes under three real coronas.

CPython 3.11+ standard library. Replays the published atlas and compact RUP
clauses using its byte-pinned literal geometry, with no discovery imports.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PINS = {'check.py': '8e483737baa95efa9c30932a888340689dd6fc84364ed7ac55d6136b3c552d29', 'atlas.json': 'ac2e2a33dec9192417b3251afd168c67320ad251018be9891bcb5a71b7e20fbb', 'certificates.json': 'd0d6fef89ad75b8ba4a6ff728f7f84acf6bbc68808bb643c73d7feaa8400ddf6', 'expected.json': '8c0b41eb8200e75128cb1cf0c7e424e6d5cb3b6de1b7eff1c6f97fba516bd7b4'}
EXCLUDED = [1,2,3,4,9,10]
CAP_EXCLUDED = [5,6]
SURVIVING = [0,7,8]


def require(condition,message):
    if not condition:
        raise ValueError(message)


def load(path,name):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dependencies(repository):
    require(len(PINS)==4,'missing parent source pins')
    parent = repository/'heesch_polyomino_four_corona_frontier'
    for name,digest in PINS.items():
        require(hashlib.sha256((parent/name).read_bytes()).hexdigest()==digest,'changed parent: '+name)
    result = subprocess.run([sys.executable,*(['-O'] if sys.flags.optimize else []),'-B',str(parent/'check.py'),
                             '--repository',str(repository),'--expected',str(parent/'expected.json')],
                            capture_output=True,text=True,timeout=55)
    require(result.returncode==0 and result.stdout==(parent/'expected.json').read_text(),
            'published atlas replay failed: '+result.stderr[:300])
    atlas_reader = load(parent/'check.py','p17_completed_atlas')
    prior = repository/'heesch_polyomino_third_prefix_reduction'
    require(hashlib.sha256((prior/'check.py').read_bytes()).hexdigest()==atlas_reader.PINS['check.py'],
            'changed sparse geometric reader')
    reader = load(prior/'check.py','p17_sparse_geometry')
    dep = reader.dependencies(repository)
    first = json.loads((parent/'atlas.json').read_text())['three_corona_first_prefixes']
    require(len(first)==11,'parent atlas size differs')
    caps = json.loads((parent/'certificates.json').read_text())['exclusions']
    return atlas_reader,reader,dep,first,caps


def cap_matches(first,caps,g):
    shapes = g.orientations()
    def cells(q):
        return g.moved(shapes,tuple(q))
    matches = []
    for cap in caps:
        fixed = cap['fixed_codes']
        required = {g.relative(cells(fixed[0]),cells(q),shapes) for q in fixed[1:]}
        for anchor in first:
            relative = {g.relative(cells(anchor),cells(q),shapes) for q in first if q!=anchor}
            if required<=relative:
                matches.append({'cap_second_prefix_id':cap['second_prefix_case'],'anchor':anchor,
                                'transported_support_copies':len(fixed)})
    return matches


def check(data,dependencies):
    _,reader,dep,first,caps = dependencies
    g,library,_,_,positive = dep
    require(data.get('schema')==1 and data.get('agent')=='six-heesch-1' and data.get('role')=='researcher',
            'invalid certificate provenance')
    certs = data['exclusions']
    require([c['first_prefix_id'] for c in certs]==EXCLUDED,'missing or changed exclusion branch')
    adapted_dep = (g,library,{i:p for i,p in enumerate(first)},None,None)
    negative = []
    for c in certs:
        require(type(c['first_prefix_id']) is int,'invalid first-prefix ID')
        adapted = copy.deepcopy(c)
        adapted['source_row'] = adapted.pop('first_prefix_id')
        require('conclusion_clause' not in adapted,'negative proof has an implication goal')
        report = reader.certificate(adapted,adapted_dep,'exclusion')
        report['first_prefix_id'] = report.pop('source_row')
        negative.append(report)
    cap_reports = []
    for i in CAP_EXCLUDED:
        matches = cap_matches(first[i],caps,g)
        require(matches and all(r['cap_second_prefix_id']==1 and r['transported_support_copies']==2 for r in matches),
                'published two-copy cap not transported into first prefix')
        cap_reports.append({'first_prefix_id':i,'cap_matches':matches})
    require(sorted(set(range(11))-set(EXCLUDED)-set(CAP_EXCLUDED))==SURVIVING,'necessary atlas coverage differs')
    control = sorted(r['code'] for r in positive['poses'] if r['level']<=1)
    require(control==first[8] and 8 in SURVIVING,'known three-corona construction was excluded')
    return {'agent':'six-heesch-1','role':'researcher',
            'status':'verified three necessary complete first prefixes under at least three real-motion coronas',
            'parent_atlas_checker_replayed':True,'parent_first_prefixes':11,
            'new_two_surround_exclusions':negative,'transported_published_caps':cap_reports,
            'necessary_first_prefix_ids':SURVIVING,
            'necessary_first_prefixes':[{'first_prefix_id':i,'copies':len(first[i]),'poses':first[i]} for i in SURVIVING],
            'total_new_core_clauses':sum(r['core_clauses'] for r in negative),
            'total_new_rup_additions':sum(r['rup_additions'] for r in negative),
            'positive_control':{'copies':36,'complete_disc_coronas':3,'first_prefix_id':8},
            'conclusion':'3 <= Hc(P17) <= Hh(P17) <= 4; no fourth-corona decision or new lower-bound construction'}


def controls(data,dep):
    variants = []
    bad = copy.deepcopy(data);bad['exclusions'].pop();variants.append(bad)
    bad = copy.deepcopy(data);bad['exclusions'][0]['first_prefix_id']=0;variants.append(bad)
    bad = copy.deepcopy(data);bad['exclusions'][0]['rup']=[];variants.append(bad)
    bad = copy.deepcopy(data)
    clause = next(c for c,r in zip(bad['exclusions'][0]['clauses'],bad['exclusions'][0]['reasons'])
                  if r['kind']=='cover' and len(c)>1)
    clause.pop();variants.append(bad)
    bad = copy.deepcopy(data)
    reason = next(r for r in bad['exclusions'][0]['reasons'] if r['kind']=='conditional_cover')
    reason['receiver']=len(bad['exclusions'][0]['poses'])+1;variants.append(bad)
    bad = copy.deepcopy(data);bad['exclusions'][0]['poses'][0]=[3,0,0];variants.append(bad)
    for i,bad in enumerate(variants):
        try:
            check(bad,dep)
        except (ValueError,KeyError,IndexError,TypeError):
            continue
        raise ValueError('malformed certificate accepted: '+str(i))
    return len(variants)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repository',type=Path,default=HERE.parent)
    p.add_argument('--certificates',type=Path,default=HERE/'certificates.json')
    p.add_argument('--expected',type=Path)
    p.add_argument('--controls',action='store_true')
    args = p.parse_args()
    dep = dependencies(args.repository)
    data = json.loads(args.certificates.read_text())
    result = check(data,dep)
    if args.controls:
        result['malformed_controls_rejected'] = controls(data,dep)
    output = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.expected:
        require(output==args.expected.read_text(),'expected result differs')
    print(output,end='')


if __name__=='__main__':
    main()
