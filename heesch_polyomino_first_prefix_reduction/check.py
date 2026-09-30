"""Exact first-prefix subset reduction; CPython 3.11+, standard library only."""
from pathlib import Path
from collections import Counter
import argparse
import copy
import hashlib
import importlib.util
import itertools
import json

HERE=Path(__file__).resolve().parent
GEOMETRY_SHA='a17e23d38e0cd1f867610509069a0699042f834b2419a99db329a3039880b8f6'
PAIR_SHA='52395c73e83ff3a1b023a1c50ebc43472caded160e4b0645c8fcbbbf905d4033'
POSITIVE_SHA='f352747cf676d96f005e2c06c2d3b3997af2dab032f9d06c250838587607d5eb'


def require(condition,message):
    if not condition:raise ValueError(message)


def pinned(path,digest):
    raw=path.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==digest,'changed dependency bytes: '+path.name)
    return raw


def load_geometry(repo):
    path=repo/'heesch_polyomino_star_b_obstruction/check.py'
    pinned(path,GEOMETRY_SHA)
    spec=importlib.util.spec_from_file_location('published_literal_geometry',path)
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    return g


def census(g,shapes,library):
    root=(3,0,0);root_cells=g.moved(shapes,root);root_vertices=g.vertices(root_cells)
    cells={root:root_cells};pair_cache={}
    def footprint(code):
        if code not in cells:cells[code]=g.moved(shapes,code)
        return cells[code]
    def prohibited(a,b):
        key=tuple(sorted((a,b)))
        if key not in pair_cache:pair_cache[key]=g.forbidden(footprint(a),footprint(b),shapes,library)
        return pair_cache[key]
    targets=g.corner_targets(root_vertices,root_cells)
    require(len(targets)==5,'changed root isolated corners')
    codes=g.bound_candidates(shapes,targets,root_cells)
    allowed=[q for q in codes if not prohibited(root,q)]
    conflicts={frozenset((a,b)) for a,b in itertools.combinations(allowed,2)
               if footprint(a)&footprint(b) or prohibited(a,b)}
    masks={q:sum(1<<j for j,p in enumerate(targets) if p in footprint(q)) for q in allowed}
    goal=(1<<len(targets))-1;covers=[];examined=0
    # Each member of a minimal cover has a private target, hence size <= 5.
    # Full subset enumeration is different from discovery's pruned DFS.
    for size in range(1,len(targets)+1):
        for chosen in itertools.combinations(allowed,size):
            examined+=1
            if any(frozenset(p) in conflicts for p in itertools.combinations(chosen,2)):continue
            mask=0
            for q in chosen:mask|=masks[q]
            if mask!=goal:continue
            for omitted in chosen:
                other=0
                for q in chosen:
                    if q!=omitted:other|=masks[q]
                if other==goal:break
            else:covers.append(chosen)
    covers.sort()
    potential={(v[0]+dx,v[1]+dy) for v in root_vertices for dx,dy in g.LOWER}-root_cells
    complete=g.bound_candidates(shapes,potential,root_cells)
    complete=[q for q in complete if not prohibited(root,q)]
    by_target={p:[q for q in complete if p in footprint(q)] for p in potential}
    halo={(x+dx,y+dy) for x,y in root_cells for dx in (-1,0,1) for dy in (-1,0,1)}-root_cells
    rows=[];domain_count=0
    for chosen in covers:
        selected=list(chosen);steps=[]
        # Each forced footprint is new and covers a previously empty root
        # vertex cell. There are finitely many such owner poses; no guard
        # can be mistaken for a negative branch.
        for _ in range(len(complete)+1):
            occupied=set(root_cells).union(*(footprint(q) for q in selected))
            if halo<=occupied:status='full integer halo forced';break
            gaps=g.corner_targets(root_vertices,occupied);domains=[]
            for p in gaps:
                owners=[q for q in by_target[p] if not footprint(q)&occupied
                        and not any(prohibited(a,q) for a in selected)]
                domains.append((p,owners));domain_count+=1
            empty=next(((p,d) for p,d in domains if not d),None)
            if empty:
                status='empty isolated-gap domain';steps.append({'target':list(empty[0]),'owners':[]});break
            forced=next(((p,d) for p,d in domains if len(d)==1),None)
            if forced is None:status='unresolved root halo';break
            steps.append({'target':list(forced[0]),'unique_owner':list(forced[1][0])})
            selected.append(forced[1][0])
        else:raise ValueError('incomplete forced-owner propagation')
        fixed=[root]+selected
        require(not any(footprint(a)&footprint(b) for a,b in itertools.combinations(fixed,2)),
                'fixed footprints overlap')
        require(all(set(root_vertices)&set(g.vertices(footprint(q))) for q in selected),
                'a purported first-layer copy does not contact the root')
        rows.append({'initial_codes':list(chosen),'forced_steps':steps,'final_codes':selected,
                     'status':status,'uncovered_root_halo_cells':len(halo-occupied)})
    digest=hashlib.sha256(json.dumps(rows,separators=(',',':'),sort_keys=True).encode()).hexdigest()
    summary={'root_corner_candidates':len(codes),'allowed_after_old_pairs':len(allowed),
             'subsets_examined':examined,'minimal_covers':len(covers),
             'propagation_counts':dict(Counter(r['status'] for r in rows)),
             'propagation_domains_checked':domain_count,'root_vertex_owners_after_pairs':len(complete),
             'derivation_sha256':digest}
    return rows,summary


def check_certificate(g,shapes,library,fixed,cert):
    fixed_cells=[g.moved(shapes,q) for q in fixed]
    require(not any(a&b for a,b in itertools.combinations(fixed_cells,2)),'required copies overlap')
    if cert['kind']=='halo':
        codes,cells,targets,cover=g.halo_geometry(shapes,fixed,[])
    else:
        require(cert['kind'] in ('corner','inner_corner'),'unknown certificate kind')
        occupied=set().union(*fixed_cells)
        targets=g.corner_targets(g.vertices(occupied),occupied)
        codes=g.bound_candidates(shapes,targets,occupied)
        cells=[g.moved(shapes,q) for q in codes]
        cover={tuple(sorted(g.owners_at(p,cells))) for p in targets}
    require(len(codes)==cert['candidate_count'],'changed complete candidate inventory')
    reasons=Counter()
    for clause in cert['clauses']:
        g.validate_clause(clause,len(codes));key=tuple(sorted(clause))
        if key in cover:reasons['complete_cover']+=1;continue
        require(1<=len(clause)<=2 and all(z<0 for z in clause),'unjustified sparse clause')
        if len(clause)==1:
            require(cert['kind']=='inner_corner' and
                    any(g.forbidden(s,cells[-clause[0]-1],shapes,library) for s in fixed_cells),
                    'unjustified interior-pair unit')
            reasons['interior_pair_unit']+=1
        else:
            a,b=(-z-1 for z in clause)
            if cells[a]&cells[b]:reasons['whole_footprint_overlap']+=1
            else:
                require(cert['kind']=='inner_corner' and g.forbidden(cells[a],cells[b],shapes,library),
                        'unjustified interior-pair binary')
                reasons['interior_pair_binary']+=1
    additions=g.rup(cert['clauses'],cert['rup'],len(codes))
    return {'source_row':cert['source_row'],'kind':cert['kind'],'complete_candidates':len(codes),
            'complete_targets':len(targets),'core_clauses':len(cert['clauses']),
            'rup_additions':additions,'clause_reasons':dict(reasons)}


def positive_surround(g,shapes,fixed,selected):
    occupied=set().union(*(g.moved(shapes,q) for q in fixed));g.boundary_disc(occupied)
    doubled=tuple(tuple(sorted(g.doubled_cells(s))) for s in shapes)
    inner=g.doubled_cells(occupied);copies=[]
    require(len(selected)==len(set(map(tuple,selected))),'duplicate surround copy')
    for q in selected:
        require(isinstance(q,list) and len(q)==3 and all(type(z) is int for z in q)
                and 0<=q[0]<8,'invalid doubled pose')
        copies.append(g.moved(doubled,q))
    require(not any(s&inner for s in copies),'surround overlaps the fixed union')
    require(not any(a&b for a,b in itertools.combinations(copies,2)),'surround copies overlap')
    xmin,xmax=min(x for x,y in inner),max(x for x,y in inner)
    ymin,ymax=min(y for x,y in inner),max(y for x,y in inner)
    # Inverse Chebyshev distance rather than discovery's forward dilation.
    halo={(x,y) for x in range(xmin-1,xmax+2) for y in range(ymin-1,ymax+2)
          if (x,y) not in inner and any(abs(x-a)<=1 and abs(y-b)<=1 for a,b in inner)}
    require(halo<=set().union(*copies),'incomplete positive halo')
    require(all(s&halo for s in copies),'positive copy does not meet the fixed halo')
    return {'surround_copies':len(copies),'complete_halo_cells':len(halo)}


def run(g,patterns,certificates,repo):
    require(patterns['schema']==1,'unknown pattern schema')
    require(patterns['geometry_sha256']==GEOMETRY_SHA and patterns['pair_data_sha256']==PAIR_SHA
            and patterns['positive_fixture_sha256']==POSITIVE_SHA,'changed dependency declaration')
    pair=json.loads(pinned(repo/'heesch_polyomino_corner_obstruction/pairs.json',PAIR_SHA))
    library=set(map(tuple,pair['forbidden_poses']));shapes=g.orientations()
    rows,summary=census(g,shapes,library)
    cert_keys={(q['source_row'],q['kind']) for q in certificates}
    require(cert_keys=={(51,'corner'),(197,'halo'),(230,'halo'),(294,'inner_corner')}
            and len(certificates)==4,'missing or repeated subsidiary proof')
    reports=[];cut_two=set();cut_three=set()
    for cert in certificates:
        index=cert['source_row'];row=rows[index]
        require(row['status']!='empty isolated-gap domain','subsidiary proof addresses an already empty branch')
        fixed=[(3,0,0)]+list(map(tuple,row['final_codes']))
        reports.append(check_certificate(g,shapes,library,fixed,cert))
        if cert['kind']=='inner_corner':cut_three.add(index)
        else:cut_two.add(index)
    surviving={i for i,r in enumerate(rows) if r['status']!='empty isolated-gap domain'}-cut_two
    require(surviving=={r['source_row'] for r in patterns['two_corona_patterns']}
            and len(surviving)==len(patterns['two_corona_patterns']),'missing or duplicated necessary pattern')
    positives=[]
    for p in patterns['two_corona_patterns']:
        index=p['source_row'];fixed=[(3,0,0)]+list(map(tuple,rows[index]['final_codes']))
        require(list(map(tuple,p['required_codes']))==fixed,'required subset changed')
        positive=positive_surround(g,shapes,fixed,p['selected_codes_doubled'])
        positives.append({'source_row':index,'required_copies':len(fixed),
                          'uncovered_root_unit_halo_cells':rows[index]['uncovered_root_halo_cells'],**positive})
    incoming=set(g.incoming(shapes,(3,0,0)))
    require({(q['source_row'],q['premise_directory']) for q in patterns['imported_third_cuts']}==
            {(54,'heesch_polyomino_star_c_obstruction'),(142,'heesch_polyomino_star_b_obstruction')}
            and len(patterns['imported_third_cuts'])==2,'changed imported star cuts')
    for cut in patterns['imported_third_cuts']:
        data=json.loads(pinned(repo/cut['premise_directory']/'certificates.json',cut['certificate_sha256']))
        star=list(map(tuple,data['fixed_codes']))
        require(star==list(map(tuple,cut['fixed_codes'])) and star[0]==(3,0,0),'changed imported placement')
        require(set(star[1:])<=incoming,'imported provider is not incoming to the root')
        require(set(star)<=set([(3,0,0)]+list(map(tuple,rows[cut['source_row']]['final_codes']))),
                'excluded root star is absent from the required subset')
        cut_three.add(cut['source_row'])
    surviving_three=surviving-cut_three
    original=json.loads(pinned(repo/'heesch_polyomino_star_b_obstruction/positive_comparison.json',POSITIVE_SHA))
    comparison=g.positive_comparison(original)
    first={tuple(q['code']) for q in original['poses'] if q['level']<=1}
    actual=[i for i in surviving_three if {(3,0,0),*map(tuple,rows[i]['final_codes'])}<=first]
    require(actual==[133],'known three-corona first prefix does not meet the reduction')
    return {'agent':'six-heesch-1','role':'researcher','status':'verified necessary first-prefix subsets under arbitrary real motions',
            **summary,'subsidiary_certificates':reports,'two_corona_source_rows':sorted(surviving),
            'three_corona_source_rows':sorted(surviving_three),'two_corona_necessary_patterns':len(surviving),
            'three_corona_necessary_patterns':len(surviving_three),'positive_fixed_disc_surrounds':positives,
            'closed_root_halo_survivors':[i for i in surviving if not rows[i]['uncovered_root_halo_cells']],
            'positive_control':{'source_row':133,'first_prefix_copies':len(first),
                                'complete_disc_coronas':comparison['complete_disc_coronas']}}


def controls(g,patterns,certificates,repo):
    shapes=g.orientations();library=set(map(tuple,json.loads(pinned(
        repo/'heesch_polyomino_corner_obstruction/pairs.json',PAIR_SHA))['forbidden_poses']))
    rows,_=census(g,shapes,library);count=0
    cert=certificates[0];fixed=[(3,0,0)]+list(map(tuple,rows[cert['source_row']]['final_codes']))
    variants=[]
    bad=copy.deepcopy(cert);bad['candidate_count']+=1;variants.append(bad)
    bad=copy.deepcopy(cert);bad['rup']=bad['rup'][:-1];variants.append(bad)
    bad=copy.deepcopy(cert)
    clause=next(c for c in bad['clauses'] if len(c)>1 and all(z>0 for z in c));clause.pop();variants.append(bad)
    for bad in variants:
        try:check_certificate(g,shapes,library,fixed,bad)
        except (ValueError,KeyError,IndexError):count+=1
        else:raise ValueError('malformed subsidiary certificate accepted')
    halo=next(c for c in certificates if c['kind']=='halo');bad=copy.deepcopy(halo)
    clause=next(c for c in bad['clauses'] if c and all(z>0 for z in c));clause.pop()
    halo_fixed=[(3,0,0)]+list(map(tuple,rows[halo['source_row']]['final_codes']))
    try:check_certificate(g,shapes,library,halo_fixed,bad)
    except (ValueError,KeyError,IndexError):count+=1
    else:raise ValueError('incomplete halo-owner clause accepted')
    third=next(c for c in certificates if c['kind']=='inner_corner')
    third_fixed=[(3,0,0)]+list(map(tuple,rows[third['source_row']]['final_codes']))
    occupied=set().union(*(g.moved(shapes,q) for q in third_fixed))
    candidates=g.bound_candidates(shapes,g.corner_targets(g.vertices(occupied),occupied),occupied)
    valid=next(i for i,q in enumerate(candidates,1) if not any(g.forbidden(
        g.moved(shapes,s),g.moved(shapes,q),shapes,library) for s in third_fixed))
    bad=copy.deepcopy(third);next(c for c in bad['clauses'] if len(c)==1 and c[0]<0)[0]=-valid
    try:check_certificate(g,shapes,library,third_fixed,bad)
    except (ValueError,KeyError,IndexError):count+=1
    else:raise ValueError('false interior-pair unit accepted')
    bad=copy.deepcopy(patterns);bad['two_corona_patterns'].pop()
    try:run(g,bad,certificates,repo)
    except (ValueError,KeyError,IndexError):count+=1
    else:raise ValueError('missing necessary pattern accepted')
    p=patterns['two_corona_patterns'][0];bad=copy.deepcopy(p['selected_codes_doubled']);bad.append(bad[0])
    try:positive_surround(g,shapes,list(map(tuple,p['required_codes'])),bad)
    except (ValueError,KeyError,IndexError):count+=1
    else:raise ValueError('duplicate positive copy accepted')
    bad=copy.deepcopy(patterns);bad['geometry_sha256']='0'*64
    try:run(g,bad,certificates,repo)
    except (ValueError,KeyError,IndexError):count+=1
    else:raise ValueError('changed dependency pin accepted')
    return count


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=HERE.parent)
    parser.add_argument('--patterns',type=Path,default=HERE/'patterns.json')
    parser.add_argument('--certificates',type=Path,default=HERE/'certificates.json')
    parser.add_argument('--expected',type=Path)
    parser.add_argument('--controls',action='store_true')
    a=parser.parse_args();g=load_geometry(a.repository)
    patterns=json.loads(a.patterns.read_text());certificates=json.loads(a.certificates.read_text())
    report=run(g,patterns,certificates,a.repository)
    if a.expected:require(report==json.loads(a.expected.read_text()),'expected report differs')
    if a.controls:report['malformed_controls_rejected']=controls(g,patterns,certificates,a.repository)
    print(json.dumps(report,sort_keys=True,indent=2))


if __name__=='__main__':main()
