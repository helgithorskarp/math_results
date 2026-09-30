"""Exact sparse-clause geometry and first-prefix phase checking; stdlib only."""
from pathlib import Path
from collections import Counter
import argparse
import copy
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
PINS={
 'heesch_polyomino_star_b_obstruction/check.py':'a17e23d38e0cd1f867610509069a0699042f834b2419a99db329a3039880b8f6',
 'heesch_polyomino_corner_obstruction/pairs.json':'52395c73e83ff3a1b023a1c50ebc43472caded160e4b0645c8fcbbbf905d4033',
 'heesch_polyomino_star_b_obstruction/positive_comparison.json':'f352747cf676d96f005e2c06c2d3b3997af2dab032f9d06c250838587607d5eb',
 'heesch_polyomino_first_prefix_reduction/patterns.json':'0e4dcd4e4fae96749b6850f012b834cca084be05c524da4a3b41731ecd78e4a7',
 'heesch_polyomino_first_prefix_reduction/expected.json':'f81806300341e1ae6ef7ea7835b35a2d0843fed56e478c25be48d89eeae9dc86',
 'heesch_polyomino_first_prefix_reduction/check.py':'99a8c1653290cd996625fe5813b129e164a8c1c8925e63bedd6ed26cea50f5b1'}
EXCLUDED=[32,33,60,61,63,137]
SURVIVING=[1,25,50,72,96,133,134]


def require(condition,message):
    if not condition:raise ValueError(message)


def pose(code):
    require(isinstance(code,list) and len(code)==3 and all(type(z) is int for z in code),'invalid integral pose')
    require(0<=code[0]<8,'invalid pose orientation')
    return tuple(code)


def cell(target):
    require(isinstance(target,list) and len(target)==2 and all(type(z) is int for z in target),'invalid cell coordinate')
    return tuple(target)


def dependencies(repository):
    for path,digest in PINS.items():
        require(hashlib.sha256((repository/path).read_bytes()).hexdigest()==digest,'changed dependency: '+path)
    spec=importlib.util.spec_from_file_location('literal_p17_geometry',repository/'heesch_polyomino_star_b_obstruction/check.py')
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    library=set(map(tuple,json.loads((repository/'heesch_polyomino_corner_obstruction/pairs.json').read_text())['forbidden_poses']))
    patterns=json.loads((repository/'heesch_polyomino_first_prefix_reduction/patterns.json').read_text())
    previous=json.loads((repository/'heesch_polyomino_first_prefix_reduction/expected.json').read_text())
    require(previous['three_corona_source_rows']==sorted(EXCLUDED+SURVIVING),'changed prior thirteen-subset conclusion')
    fixed={r['source_row']:r['required_codes'] for r in patterns['two_corona_patterns']}
    positive=json.loads((repository/'heesch_polyomino_star_b_obstruction/positive_comparison.json').read_text())
    return g,library,fixed,previous,positive


def halo(squares):
    return {(x+a,y+b) for x,y in squares for a in (-1,0,1) for b in (-1,0,1)}


def certificate(cert,dep,goal_kind):
    g,library,required,_,_=dep;shapes=g.orientations();row=cert['source_row']
    require(type(row) is int and row in required,'unknown census row')
    require(cert['fixed_codes']==required[row],'fixed subset differs from normative census')
    fixed=list(map(pose,cert['fixed_codes']));fixed_cells=[g.moved(shapes,q) for q in fixed]
    require(len(fixed)==len(set(fixed)) and not any(a&b for a,b in itertools.combinations(fixed_cells,2)),'overlapping or duplicate fixed copies')
    occupied=set().union(*fixed_cells);codes=list(map(pose,cert['poses']));cells=[g.moved(shapes,q) for q in codes]
    require(len(codes)==len(set(codes)),'duplicate sparse pose')
    require(not any(s&occupied for s in cells),'sparse candidate overlaps fixed C')
    vertices=set(g.vertices(occupied));touch=[bool(vertices&set(g.vertices(s))) for s in cells]
    clauses=cert['clauses'];reasons=cert['reasons'];trace=cert['rup']
    require(isinstance(clauses,list) and isinstance(reasons,list) and len(reasons)==len(clauses),'missing clause explanation')
    counts=Counter()
    for clause,reason in zip(clauses,reasons):
        g.validate_clause(clause,len(codes));require(isinstance(reason,dict),'bad clause explanation');kind=reason['kind'];counts[kind]+=1
        if kind in ('cover','conditional_cover'):
            target=cell(reason['target'])
            if kind=='cover':
                require(target in g.corner_targets(g.vertices(occupied),occupied),'not a fixed isolated gap')
                positive=clause
            else:
                require(type(reason['receiver']) is int,'invalid receiver variable');r=reason['receiver']-1
                require(0<=r<len(codes) and touch[r],'receiver is not licensed interior')
                require(target in g.corner_targets(g.vertices(cells[r]),occupied|set(cells[r])),'not a conditional isolated gap')
                require(clause.count(-(r+1))==1,'conditional antecedent absent')
                positive=[z for z in clause if z!=-(r+1)]
            require(all(z>0 for z in positive),'bad cover signs')
            complete_owners=g.bound_candidates(shapes,[target],occupied)
            require(sorted(codes[z-1] for z in positive)==complete_owners,'incomplete target-owner clause')
        elif kind=='overlap':
            require(len(clause)==2 and all(z<0 for z in clause),'bad overlap clause')
            a,b=[-z-1 for z in clause];require(bool(cells[a]&cells[b]),'false whole-copy overlap')
        elif kind=='interior_pair':
            require(1<=len(clause)<=2 and all(z<0 for z in clause),'bad pair clause')
            ids=[-z-1 for z in clause];require(all(touch[i] for i in ids),'outer pose used as interior')
            if len(ids)==1:require(any(g.forbidden(cells[ids[0]],s,shapes,library) for s in fixed_cells),'false old pair unit')
            else:require(g.forbidden(cells[ids[0]],cells[ids[1]],shapes,library),'false old pair binary')
        else:raise ValueError('unknown clause reason')
    if goal_kind=='exclusion':
        require('conclusion_clause' not in cert,'unexpected exclusion conclusion')
        g.rup(clauses,trace,len(codes));conclusion=[]
    else:
        conclusion=cert['conclusion_clause'];g.validate_clause(conclusion,len(codes))
        require(bool(conclusion) and all(z>0 for z in conclusion),'invalid positive conclusion')
        conclusion_poses=list(map(pose,cert['conclusion_poses']))
        require([codes[z-1] for z in conclusion]==conclusion_poses,'conclusion pose mismatch')
        require(isinstance(trace,list) and bool(trace) and trace[-1]==conclusion,'proof must end in the exact positive goal')
        database=[list(c) for c in clauses]
        for j,c in enumerate(trace):
            g.validate_clause(c,len(codes))
            require(g.propagated_contradiction(database,[-z for z in c]),'non-RUP implication addition '+str(j))
            database.append(c)
        root=g.moved(shapes,(3,0,0));root_vertices=set(g.vertices(root))
        require(all(root_vertices&set(g.vertices(cells[z-1])) for z in conclusion),'conclusion copy does not touch root')
        if goal_kind=='forced':require(len(conclusion)==1,'forced-copy conclusion must be a unit')
        else:
            target=cell(cert['target']);require(target in halo(root)-occupied,'not an uncovered root halo cell')
            require(all(target in cells[z-1] for z in conclusion),'goal pose does not cover stated halo cell')
    result={'source_row':row,'sparse_poses':len(codes),'core_clauses':len(clauses),'rup_additions':len(trace),'reasons':dict(sorted(counts.items()))}
    if goal_kind=='forced':result['forced_pose']=cert['conclusion_poses'][0]
    if goal_kind=='halo':result.update({'target':cert['target'],'conclusion_poses':cert['conclusion_poses']})
    return result


def check(data,dep):
    g,_,fixed,previous,positive=dep
    require(data['schema']==1 and data['agent']=='six-heesch-1' and data['role']=='researcher','changed certificate provenance')
    exclusions=data['exclusions'];forced=data['forced_copies'];coverage=data['halo_coverage']
    require([c['source_row'] for c in exclusions]==EXCLUDED,'missing or changed exclusion family')
    negative=[certificate(c,dep,'exclusion') for c in exclusions]
    require(all(c['source_row'] in SURVIVING for c in forced+coverage),'claim about an eliminated branch')
    implications=[certificate(c,dep,'forced') for c in forced];covers=[certificate(c,dep,'halo') for c in coverage]
    forced_keys=[(r['source_row'],tuple(r['forced_pose'])) for r in implications]
    cover_keys=[(r['source_row'],tuple(r['target'])) for r in covers]
    require(len(forced_keys)==len(set(forced_keys)) and len(cover_keys)==len(set(cover_keys)),'duplicate conclusion')
    shapes=g.orientations();root=g.moved(shapes,(3,0,0));root_vertices=set(g.vertices(root));required_halo=halo(root)
    prefixes=[];missing=[]
    for row in SURVIVING:
        codes=list(map(tuple,fixed[row]))+[q for r,q in forced_keys if r==row]
        squares=[g.moved(shapes,q) for q in codes]
        require(len(codes)==len(set(codes)) and not any(a&b for a,b in itertools.combinations(squares,2)),'forced copies conflict')
        require(all(q==(3,0,0) or root_vertices&set(g.vertices(s)) for q,s in zip(codes,squares)),'guaranteed first copy does not touch root')
        occupied=set().union(*squares);unfilled=required_halo-occupied
        require(all((row,p) in cover_keys for p in unfilled),'unproved integer root-halo coverage')
        if not unfilled:
            g.boundary_disc(occupied)
            prefixes.append({'source_row':row,'complete_first_prefix_codes':[list(q) for q in sorted(codes)],'copies':len(codes),'disc':True})
        else:missing.append({'source_row':row,'guaranteed_first_prefix_copies':len(codes),'coverage_targets_needed':[list(p) for p in sorted(unfilled)]})
    control=g.positive_comparison(positive)
    first=sorted(tuple(r['code']) for r in positive['poses'] if r['level']<=1)
    require(next(r['complete_first_prefix_codes'] for r in prefixes if r['source_row']==133)==[list(q) for q in first],'known positive first prefix differs')
    all_reports=negative+implications+covers
    return {'agent':'six-heesch-1','role':'researcher','status':'verified necessary seven subsets and integral first prefixes under at least three coronas',
            'prior_three_corona_source_rows':previous['three_corona_source_rows'],'excluded_source_rows':EXCLUDED,'necessary_source_rows':SURVIVING,
            'exclusions':negative,'forced_copies':implications,'halo_coverage':covers,'unique_complete_first_prefixes':prefixes,'other_integral_first_prefix_branches':missing,
            'total_core_clauses':sum(r['core_clauses'] for r in all_reports),'total_rup_additions':sum(r['rup_additions'] for r in all_reports),
            'positive_control':{'copies':control['copies'],'complete_disc_coronas':control['complete_disc_coronas'],'first_prefix_source_row':133,'first_prefix_copies':len(first)}}


def controls(data,dep):
    variants=[]
    bad=copy.deepcopy(data);bad['exclusions'].pop();variants.append(bad)
    bad=copy.deepcopy(data);bad['exclusions'][0]['poses'][0][0]=-1;variants.append(bad)
    bad=copy.deepcopy(data);bad['exclusions'][0]['rup']=[];variants.append(bad)
    bad=copy.deepcopy(data)
    c=next(c for c,r in zip(bad['exclusions'][0]['clauses'],bad['exclusions'][0]['reasons']) if r['kind']=='cover' and len(c)>1)
    c.pop();variants.append(bad)
    bad=copy.deepcopy(data);bad['forced_copies'][0]['conclusion_clause'][0]*=-1;variants.append(bad)
    bad=copy.deepcopy(data);bad['forced_copies'][0]['rup'][-1]=[];variants.append(bad)
    bad=copy.deepcopy(data);bad['halo_coverage'][0]['target']=[999,999];variants.append(bad)
    bad=copy.deepcopy(data);bad['halo_coverage']=[c for c in bad['halo_coverage'] if not (c['source_row']==72 and c['target']==[-1,1])];variants.append(bad)
    for i,bad in enumerate(variants):
        try:check(bad,dep)
        except (ValueError,KeyError,IndexError,TypeError):continue
        raise ValueError('malformed certificate accepted: '+str(i))
    return len(variants)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repository',type=Path,default=HERE.parent)
    p.add_argument('--certificates',type=Path,default=HERE/'certificates.json');p.add_argument('--expected',type=Path)
    p.add_argument('--controls',action='store_true');a=p.parse_args();dep=dependencies(a.repository)
    prior=subprocess.run([sys.executable,*(['-O'] if sys.flags.optimize else []),'-B',str(a.repository/'heesch_polyomino_first_prefix_reduction/check.py'),
                          '--repository',str(a.repository),'--expected',str(a.repository/'heesch_polyomino_first_prefix_reduction/expected.json')],
                         capture_output=True,text=True,timeout=55)
    require(prior.returncode==0 and prior.stdout==(a.repository/'heesch_polyomino_first_prefix_reduction/expected.json').read_text(),'prior thirteen-subset checker failed: '+prior.stderr[:500])
    data=json.loads(a.certificates.read_text());result=check(data,dep);result['prior_thirteen_subset_checker_replayed']=True
    if a.controls:result['malformed_controls_rejected']=controls(data,dep)
    output=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.expected:require(output==a.expected.read_text(),'expected result differs')
    print(output,end='')


if __name__=='__main__':main()
