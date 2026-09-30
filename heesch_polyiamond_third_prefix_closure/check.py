"""Exact geometry and ten elementary RUP checks for the T214 C3 branch.

six-heesch-2, researcher. No solver, dense CNF, DRAT, discovery inventory or
extractor is loaded. Old excluded interior pairs remain mathematical premises.
Centroid geometry, small-pattern matching and local unit logic are reused
from byte-pinned public predecessors; the new geometric covers are regenerated.
"""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

BASE = Path(__file__).resolve().parent
PUB = BASE.parent
PINS = {
    'heesch_polyiamond_six_copy_obstruction/check.py':
        '4116830b1dfe1bd2714b66891bd94a28894b5b30c815251a1a8aa7f032cce3c3',
    'heesch_polyiamond_six_copy_obstruction/pattern.json':
        '9a6bdd8df8484a7ffd28e32a2042325c66035564085c4e8c9b29e93782b35799',
    'heesch_polyiamond_six_copy_obstruction/single-gap.json':
        '802db54ea515f82278c97436629734a739580371a6168aa8a6caab9ca5d7f59a',
    'heesch_polyiamond_forced_pair/escape-both-witness.json':
        'b949b4b8c4b0c738ccd54742356ddf803e82e63759683f138449221dc3daceae',
    'heesch_polyiamond_alternate_fourth/patterns.json':
        'f5970193b1657dfdcdfe6b0e345dc8293a2053ef8721c73afab762147d46b1be',
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def pose(row):
    return tuple(row['matrix']) + tuple(row['translation'])


def context():
    for relative, digest in PINS.items():
        need(hashlib.sha256((PUB/relative).read_bytes()).hexdigest() == digest,
             ('changed dependency', relative))
    path = PUB/'heesch_polyiamond_six_copy_obstruction/check.py'
    spec = importlib.util.spec_from_file_location('pinned_six_copy_helpers', path)
    f = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(f)
    h, c = f.helpers()
    data = read(PUB/'heesch_polyiamond_deficit_review1/input.json')
    g = c.Geometry(c.shape(data['side_signs']))
    need(len(g.fs) == 214, 'prototype size')
    c.mesh(g.fs)
    catalogue, trials, gaps = g.anchor_pool(g.pockets)
    need(len(catalogue) == 59 and len(set(data['retained_indices'])) == 21,
         'old interior-pair catalogue')
    excluded = {q for i, q in enumerate(catalogue,1) if i not in data['retained_indices']}
    patterns = read(PUB/'heesch_polyiamond_fixed_fourth_extension/patterns.json')
    patterns.append(read(PUB/'heesch_polyiamond_fixed_third_extension/hole.json'))
    patterns.extend(read(PUB/'heesch_polyiamond_alternate_fourth/patterns.json'))
    patterns.append(read(PUB/'heesch_polyiamond_six_copy_obstruction/single-gap.json'))
    return f, h, c, g, catalogue, excluded, patterns, trials, gaps


def valid_poses(g, rows):
    need(len(rows) == len(set(rows)), 'duplicate physical poses')
    need(all(len(p) == 6 and all(type(t) is int for t in p) and p[:4] in g.ms
             for p in rows), 'invalid integral pose')


def verify_patterns(f, h, c, g, patterns):
    """Face joins check small gaps; exact edge enclosure checks small holes."""
    reports = []
    for row in patterns:
        fixed = [pose(p) for p in row['poses']]
        valid_poses(g, fixed)
        need(c.IDENTITY in fixed, 'pattern normalization')
        occupied = g.union(fixed)
        if row['kind'] == 'small_hole':
            hole = {h.cell(p) for p in row['hole_cells']}
            need(0 < len(hole) < len(g.fs) and not hole & occupied, 'hole size/overlap')
            for face in hole:
                vertices = c.vertices(face)
                for u,v in combinations(vertices,2):
                    w = next(t for t in vertices if t not in (u,v))
                    across = c.triangle((u,v,(u[0]+v[0]-w[0],u[1]+v[1]-w[1])))
                    need(across in hole or across in occupied, 'unenclosed hole edge')
            reports.append({'kind':row['kind'],'copies':len(fixed),'hole_faces':len(hole)})
            continue
        targets = row['targets'] if row['kind'] == 'forced_clash' else [
            {'vertex':row['target'],'cell':row['missing_cell']}]
        available, counts = [], []
        for target in targets:
            raw, allowed, _, _ = f.cover(c,g,occupied,tuple(target['vertex']),h.cell(target['cell']))
            counts.append(len(raw))
            available.append(allowed)
        if row['kind'] == 'empty_corner':
            need(len(available) == 1 and not available[0], 'false empty corner')
        else:
            need(row['kind'] == 'forced_clash' and len(available) == 2 and all(available),
                 'false forced-clash target')
            need(all(g.footprint(p) & g.footprint(q) for p in available[0] for q in available[1]),
                 'compatible alleged clash providers')
        reports.append({'kind':row['kind'],'copies':len(fixed),'raw_providers':counts,
                        'available_counts':[len(a) for a in available]})
    return reports


def covers(f,c,g,fixed,providers,certificate):
    occupied = g.union(fixed)
    lookup = {p:i for i,p in enumerate(providers,1)}
    reports, indices = [], set()
    for row in certificate['cover_targets']:
        i = row['clause']
        need(type(i) is int and 0 <= i < len(certificate['clauses']) and i not in indices,
             'invalid/repeated complete cover')
        raw, allowed, joins, sectors = f.cover(c,g,occupied,tuple(row['vertex']),tuple(row['required_centroid']))
        need(all(p in lookup for p in allowed), 'geometric provider omitted from certificate')
        ids = sorted(lookup[p] for p in allowed)
        need(ids and ids == sorted(certificate['clauses'][i]) and len(raw) == row['raw_providers'],
             'truncated or false complete cover')
        indices.add(i)
        reports.append({'clause':i,'vertex':row['vertex'],'required_centroid':row['required_centroid'],
                        'filled_sectors':sectors,'centroid_joins':joins,'raw_providers':len(raw),
                        'allowed_provider_ids':ids})
    return indices, reports


def negative_clauses(h,c,g,fixed,providers,certificate,cover_ids,excluded,tables):
    matches = [(name,h.pattern_clauses(c,fixed,providers,rows)) for name,rows in tables]
    counts = Counter(complete_cover=len(cover_ids))
    for i,clause in enumerate(certificate['clauses']):
        need(clause and len(clause) == len(set(clause)) and
             all(type(v) is int and 1 <= abs(v) <= len(providers) for v in clause), 'clause encoding')
        if i in cover_ids:
            need(all(v > 0 for v in clause), 'nonpositive cover')
            continue
        need(all(v < 0 for v in clause), 'unproved positive clause')
        ps = [providers[-v-1] for v in clause]
        if len(ps) == 1 and any(g.bad(ps[0],p,excluded) for p in fixed):
            counts['old_interior_pair_unit'] += 1
        elif len(ps) == 2 and g.footprint(ps[0]) & g.footprint(ps[1]):
            counts['whole_overlap_binary'] += 1
        elif len(ps) == 2 and g.bad(ps[0],ps[1],excluded):
            counts['old_interior_pair_binary'] += 1
        else:
            normalized = tuple(sorted(clause,key=abs))
            found = next((name for name,allowed in matches if normalized in allowed),None)
            need(found is not None, ('unsupported geometric clause',i,clause))
            counts[found] += 1
    return dict(sorted(counts.items()))


def local_two(f,h,c,g,excluded,patterns,certificate):
    need(certificate['kind'] == 'two_surround_obstruction' and certificate['tile'] == 'T214', 'local scope')
    fixed, providers = [pose(row) for row in certificate['poses']], [tuple(p) for p in certificate['providers']]
    valid_poses(g,fixed);valid_poses(g,providers)
    need(fixed[0] == c.IDENTITY, 'two-surround normalization')
    occupied = g.union(fixed)
    need(all(not g.footprint(p) & occupied for p in providers), 'local provider overlaps premise')
    ids, census = covers(f,c,g,fixed,providers,certificate)
    counts = negative_clauses(h,c,g,fixed,providers,certificate,ids,excluded,[('single_surround_pattern',patterns)])
    steps = f.logic(certificate)
    return {'fixed_copies':len(fixed),'providers':len(providers),'clauses':len(certificate['clauses']),
            'unit_steps':steps,'clause_counts':counts,'complete_covers':census,'contradiction_verified':True}


def cap_family(f,c,g,catalogue,excluded,listed):
    base = [c.IDENTITY,(1,0,0,1,-6,3)]
    occupied = g.union(base)
    raw, allowed, joins, sectors = f.cover(c,g,occupied,(-2,0),(-7,-1))
    q = (1,0,-1,-1,-3,-3)
    need(sectors == 5 and len(raw) == 22 and allowed == [q], 'base filler is not uniquely forced')
    possible = sorted({c.compose(q,e) for e in excluded} | {c.compose(q,c.inverse(e)) for e in excluded})
    caps, witnesses = [], []
    for cap in possible:
        foot = g.footprint(cap)
        if foot & occupied or sum(t in occupied|foot for t in c.star((-2,0))) != 5:
            continue
        need(not foot & g.footprint(q), 'cap blocks Q directly')
        need(not any(g.bad(cap,p,excluded) for p in base), 'already forbidden base-cap pair')
        cases = []
        for direction,a,b in [('Q_to_cap',q,cap),('cap_to_Q',cap,q)]:
            relative = c.compose(c.inverse(a),b)
            if relative in excluded:
                cases.append({'direction':direction,'attachment':catalogue.index(relative)+1})
        need(cases, 'cap has no forbidden Q pair')
        caps.append(cap);witnesses.append({'cap':list(cap),'pair_witnesses':cases})
    supplied = [tuple(p) for p in listed]
    valid_poses(g,supplied)
    need(supplied == caps and len(possible) == 75 and len(caps) == 48, 'incomplete or false cap catalogue')
    census = []
    for p in raw:
        blocked=[]
        for i,old in enumerate(base,1):
            overlap=g.footprint(p)&g.footprint(old)
            if overlap:blocked.append({'base_copy':i,'overlap_faces':len(overlap),'example_centroid':list(min(overlap))})
        census.append({'pose':list(p),'blockers':blocked})
    patterns = [{'poses':[{'matrix':list(p[:4]),'translation':list(p[4:])} for p in base+[cap]]}
                for cap in caps]
    return patterns, {'derived_caps':len(possible),'retained_caps':len(caps),'centroid_joins':joins,
                      'base_provider_census':census,'unique_Q':list(q),'cap_pair_witnesses':witnesses}


def propagate(clauses):
    assigned, steps = {}, 0
    while True:
        changed = False
        for i,clause in enumerate(clauses):
            remaining=[]
            for v in clause:
                if abs(v) not in assigned:remaining.append(v)
                elif assigned[abs(v)] == (v > 0):break
            else:
                if not remaining:return steps,i
                if len(remaining) == 1:
                    v=remaining[0];assigned[abs(v)]=v>0;steps+=1;changed=True
        if not changed:return steps,None


def rup(certificate):
    clauses = copy.deepcopy(certificate['clauses'])
    out=[]
    need(certificate['rup_lemmas'] and certificate['rup_lemmas'][-1] == [], 'no terminal empty lemma')
    for row in certificate['rup_lemmas']:
        need(len(row) == len(set(row)) and all(type(v) is int and 1 <= abs(v) <= len(certificate['providers']) for v in row),
             'RUP lemma encoding')
        steps,conflict=propagate(clauses+[[-v] for v in row])
        need(conflict is not None, ('not an elementary RUP lemma',row))
        out.append({'clause':row,'unit_steps':steps,'conflict_clause':conflict})
        clauses.append(row)
    return out


def positive(c,g):
    witness=read(PUB/'heesch_polyiamond_forced_pair/escape-both-witness.json')
    need(witness['tile']=='T214' and witness['depth']==4,'positive scope')
    layers=[[pose(row) for row in witness['placements'] if row['level']==level] for level in range(5)]
    need([len(row) for row in layers]==[1,5,12,30,41] and layers[0]==[c.IDENTITY], 'positive layer counts')
    previous_vertices, previous_layer, fixed, reports=set(),set(),[],[]
    for level,layer in enumerate(layers):
        fixed.extend(layer);occupied=g.union(fixed);mesh,vertices=c.mesh(occupied)
        if level:
            need(all(set(c.star(v))<=occupied for v in previous_vertices),'incomplete positive surround')
            need(all(previous_layer&{c.point(p,v) for v in g.vs} for p in layer),'missing preceding-layer contact')
        mesh.update(level=level,layer_copies=len(layer),cumulative_copies=len(fixed));reports.append(mesh)
        previous_vertices=vertices;previous_layer={c.point(p,v) for p in layer for v in g.vs}
    return layers, reports


def check(certificate,five,corner,caps):
    f,h,c,g,catalogue,excluded,patterns,trials,gaps=context()
    patterns.append(corner)
    pattern_checks=verify_patterns(f,h,c,g,patterns)
    five_check=local_two(f,h,c,g,excluded,patterns,five)
    six=read(PUB/'heesch_polyiamond_six_copy_obstruction/pattern.json')
    six_check=local_two(f,h,c,g,excluded,patterns,six)
    cap_patterns, cap_report=cap_family(f,c,g,catalogue,excluded,caps)
    layers,positive_report=positive(c,g)
    fixed=[p for layer in layers[:4] for p in layer]
    need(certificate['kind']=='three_surround_obstruction' and certificate['tile']=='T214' and
         certificate['prefix_level']==3, 'three-surround scope')
    providers=[tuple(p) for p in certificate['providers']]
    valid_poses(g,providers)
    occupied=g.union(fixed)
    need(all(not g.footprint(p)&occupied for p in providers),'branch provider overlaps fixed prefix')
    ids,census=covers(f,c,g,fixed,providers,certificate)
    tables=[('single_surround_pattern',patterns),('two_surround_five_pattern',[five]),
            ('two_surround_six_pattern',[six]),('two_surround_cap_pattern',cap_patterns)]
    counts=negative_clauses(h,c,g,fixed,providers,certificate,ids,excluded,tables)
    lemmas=rup(certificate)
    return {'agent':'six-heesch-2','role':'researcher','fixed_prefix_level':3,'fixed_copies':len(fixed),
            'providers':len(providers),'clauses':len(certificate['clauses']),'rup_lemmas':lemmas,
            'complete_covers':census,'clause_counts':counts,'old_pair_catalogue':
            {'poses':len(catalogue),'excluded':len(excluded),'centroid_joins':trials,'target_faces':gaps},
            'single_surround_pattern_checks':pattern_checks,'five_copy_lemma':five_check,
            'six_copy_dependency_replay':six_check,'cap_family':cap_report,
            'positive_four_coronas':positive_report,'three_surround_contradiction_verified':True,
            'scope':'the specified C3 prefix cannot have C4,C5,C6 under arbitrary real motions and topology'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--expected',type=Path)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--controls',action='store_true')
    args=ap.parse_args();start=time.monotonic()
    inputs=[read(BASE/name) for name in ['certificate.json','five-pattern.json','corner-pattern.json','caps.json']]
    report=check(*inputs)
    if args.controls:
        names=['truncated_cover','deleted_cap','shifted_five_blocker','false_rup_unit']
        for name in names:
            bad=copy.deepcopy(inputs)
            if name=='truncated_cover':bad[0]['clauses'][bad[0]['cover_targets'][0]['clause']].pop()
            elif name=='deleted_cap':bad[3].pop()
            elif name=='shifted_five_blocker':bad[1]['poses'][-1]['translation'][0]+=40
            else:bad[0]['rup_lemmas'][0]=[2]
            try:check(*bad)
            except ValueError:continue
            raise ValueError(('malformed control accepted',name))
        report['rejected_controls']=names
    if args.expected:
        need(report==read(args.expected),'expected output differs')
    text=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')
    print(json.dumps({'seconds':round(time.monotonic()-start,3),
                      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__=='__main__':
    main()
