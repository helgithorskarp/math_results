#!/usr/bin/env python3
"""Exact, solver-free reader for the nonflat small-bow classification.

Author: six-heesch-3; role: researcher. Python 3.11, standard library.
No timeout, intermediate-hole prune, numerical tolerance or external atlas.
"""
import argparse
from collections import Counter,defaultdict
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import geometry as e

HERE=Path(__file__).resolve().parent
EXCLUDED=set()

def independent_orient(angle,flip,p):
    # Complex multiplication, rather than repeated use of rot30.
    x=p[:2];y=p[2:]
    if flip:y=tuple(-v for v in y)
    c=e.DIRECTIONS[angle][:2];s=e.DIRECTIONS[angle][2:]
    xx=e.qsub(e.qmul(c,x),e.qmul(s,y));yy=e.qadd(e.qmul(s,x),e.qmul(c,y))
    e.require(all(v%2==0 for v in xx+yy),'independent rotation module')
    return tuple(v//2 for v in xx+yy)

def prototype_checks():
    e.require(len(set(e.VERTICES))==14,'repeated prototype vertex')
    e.require(e.twice_area(e.VERTICES)==(24,24),'prototype area')
    for i,a in enumerate(e.VERTICES):
        b=e.VERTICES[(i+1)%14]
        for j,c in enumerate(e.VERTICES):
            if j==i or (j-i)%14 in (1,13):continue
            d=e.VERTICES[(j+1)%14]
            s1=e.qsign(e.cross(e.sub(b,a),e.sub(c,a)))
            s2=e.qsign(e.cross(e.sub(b,a),e.sub(d,a)))
            s3=e.qsign(e.cross(e.sub(d,c),e.sub(a,c)))
            s4=e.qsign(e.cross(e.sub(d,c),e.sub(b,c)))
            e.require(not(s1*s2<0 and s3*s4<0),'proper prototype crossing')
            e.require(not any((e.on_segment(a,c,d),e.on_segment(b,c,d),
                               e.on_segment(c,a,b),e.on_segment(d,a,b))),'prototype nonadjacent contact')
    for a in range(12):
        for f in (0,1):
            for p in e.VERTICES:e.require(independent_orient(a,f,p)==e.orient(a,f,p),'rotation disagreement')
    e.require(e.geometry(e.IDENTITY,e.IDENTITY) is None,'positive overlap control')

def make_inventory():
    raw=set();control=set()
    for a in range(12):
        for f in (0,1):
            turned=[e.orient(a,f,v) for v in e.VERTICES]
            for p in e.VERTICES:
                for q in turned:raw.add((a,f)+e.sub(p,q))
            for i in range(14):
                for j in range(14):
                    q=independent_orient(a,f,e.VERTICES[j])
                    control.add((a,f)+tuple(e.VERTICES[i][k]-q[k] for k in range(4)))
    raw.discard(e.IDENTITY);control.discard(e.IDENTITY)
    e.require(raw==control,'vertex-anchor generation disagreement')
    records=[]
    for p in sorted(raw):
        r=e.geometry(e.IDENTITY,p)
        if r is None:continue
        m=e.coverage(p);e.require(m!=0,'empty neighbour coverage')
        e.require(e.compose(p,e.inverse(p))==e.IDENTITY,'pose inverse')
        e.require(tuple(sorted((j,i,v) for i,j,v in r))==e.geometry(p,e.IDENTITY),'reciprocal ports')
        records.append((p,m,r))
    return records,len(raw)

def edge_graph(rel):
    return sum(1<<k for k in {14*i+j for i,j,r in rel}|{14*j+i for i,j,r in rel})

@lru_cache(40000)
def components(g):
    todo=16383;cc=[]
    while todo:
        p=todo&-todo;todo^=p;A=p;B=0;front=[(p.bit_length()-1,0)]
        while front:
            v,col=front.pop();adj=(g>>(14*v))&16383
            if adj&(A if col==0 else B):return None
            new=adj&todo
            if col==0:B|=new
            else:A|=new
            todo^=new
            while new:
                bit=new&-new;new^=bit;front.append((bit.bit_length()-1,1-col))
        cc.append((A,B))
    return tuple(cc)

@lru_cache(40000)
def all_graph_words(g):
    cc=components(g)
    if cc is None:return ()
    result=[0]
    for a,b in cc:result=[w|c for w in result for c in (a,b)]
    return tuple(sorted(w for w in result if w.bit_count()==7))

@lru_cache(40000)
def graph_words(g):return tuple(w for w in all_graph_words(g) if w<8192)

def positive(g):return bool(graph_words(g))

def positive_overlap(p,q):
    pp,tp,bp=e.shape(p);qq,tq,bq=e.shape(q)
    return e.bbox_overlap(bp,bq) and any(e.triangle_overlap(t,u) for t in tp for u in tq)

def periodic_packings(fixtures):
    words=set();stats=[];classes=[]
    e.require(len(fixtures)==3,'three periodic fixtures required')
    for row in fixtures:
        pp=tuple(tuple(p) for p in row['poses']);u=tuple(row['u']);v=tuple(row['v'])
        e.require(len(pp) in (2,4) and e.IDENTITY in pp,'bad periodic bases')
        e.require(len(u)==len(v)==4,'bad lattice vector')
        det=e.cross(u,v);e.require(e.qsign(det)>0,'singular/reversed lattice')
        e.require(tuple(2*x for x in det)==tuple(len(pp)*x for x in e.twice_area(e.VERTICES)),'wrong lattice covolume')
        polygons=[e.shape(p)[0] for p in pp]
        # All interacting integer lattice coordinates have absolute value <2.
        limit=tuple(2*x for x in det)
        for a in polygons:
            for b in polygons:
                for x in a:
                    for y in b:
                        d=e.sub(x,y)
                        for c in (e.cross(d,v),e.cross(u,d)):
                            e.require(e.qsign(e.qsub(limit,c))>0 and e.qsign(e.qadd(limit,c))>0,'incomplete periodic collision window')
        graph=0;tests=0;partners={};expanded=[]
        for q in pp:
            for n in (-1,0,1):
                for m in (-1,0,1):
                    t=tuple(n*x+m*y for x,y in zip(u,v));expanded.append(q[:2]+e.add(q[2:],t))
        e.require(len(set(expanded))==len(expanded),'repeated periodic copy')
        for i,p in enumerate(pp):
            for j,q in enumerate(pp):
                for n in (-1,0,1):
                    for m in (-1,0,1):
                        if i==j and n==m==0:continue
                        t=tuple(n*x+m*y for x,y in zip(u,v));r=q[:2]+e.add(q[2:],t)
                        rel=e.geometry(p,r);tests+=1;e.require(rel is not None,'periodic reference collision or T contact')
                        graph|=edge_graph(rel)
                        for a,b,rev in rel:
                            key=(i,a);value=(j,n,m,b,rev)
                            e.require(key not in partners or partners[key]==value,'duplicate periodic partner')
                            partners[key]=value
        e.require(len(partners)==14*len(pp),'exposed periodic port')
        stars=occupied_stars(expanded)
        e.require(all(stars[x]==4095 for poly in polygons for x in poly),'unfilled periodic vertex')
        ww=all_graph_words(graph);e.require(len(ww)==128,'periodic profile count changed')
        cc=components(graph)
        e.require(len(cc)==7 and all(a.bit_count()==b.bit_count()==1 for a,b in cc),'periodic port graph not seven opposite pairs')
        pairs=[[a.bit_length()-1,b.bit_length()-1] for a,b in cc]
        words.update(ww);classes.append(set(ww));stats.append({'base_copies':len(pp),'pair_checks':tests,'port_partners':len(partners),'words':len(ww),'port_pairs':pairs})
    e.require(len(words)==320,'periodic word union changed')
    e.require(not words&{0x1555,0x2aaa},'periodic/Spectre calibration overlap')
    return words,stats,classes

def inventory_pairs(records):
    cache={};tests=[0]
    def pair(i,j):
        key=tuple(sorted((i,j)))
        if key not in cache:
            tests[0]+=1;cache[key]=e.geometry(records[key[0]][0],records[key[1]][0])
        r=cache[key]
        return r if i<=j or r is None else tuple(sorted((b,a,v) for a,b,v in r))
    return pair,tests

def graph_search(records,pair):
    masks=[r[1] for r in records];gg=[edge_graph(r[2]) for r in records]
    users={k:[i for i,m in enumerate(masks) if m&(1<<k) and positive(gg[i])]
           for k in range(168) if e.GOAL&(1<<k)}
    nodes=0;solutions={};graphs={}
    def visit(taken,chosen,graph):
        nonlocal nodes
        nodes+=1;remaining=e.GOAL&~taken
        if not remaining:
            pp=tuple(sorted((e.IDENTITY,)+tuple(records[i][0] for i in chosen)))
            e.require(pp not in solutions,'graph-search duplicate')
            solutions[pp]=graph_words(graph);graphs[pp]=graph;return
        bit=remaining&-remaining;k=bit.bit_length()-1
        for i in reversed(users[k]):
            if masks[i]&taken:continue
            g=graph|gg[i]
            if not positive(g):continue
            for j in chosen:
                rel=pair(i,j)
                if rel is None:break
                g|=edge_graph(rel)
                if not positive(g):break
            else:visit(taken|masks[i],chosen+(i,),g)
    visit(0,(),0);return solutions,nodes,graphs

def word_search(records,pair,only_words=None,first_only=False):
    # Independent domain representation and recursion order.
    words=only_words if only_words is not None else [w for w in range(8192) if w.bit_count()==7]
    ALL=(1<<len(words))-1;masks=[r[1] for r in records];rules_cache={}
    def rules(rel):
        key=tuple(sorted({tuple(sorted((i,j))) for i,j,v in rel}))
        if key not in rules_cache:
            rules_cache[key]=sum(1<<k for k,w in enumerate(words)
                if all(((w>>i)^(w>>j))&1 for i,j in key))
        return rules_cache[key]
    initial=[rules(r[2]) for r in records]
    users={k:[i for i,m in enumerate(masks) if m&(1<<k) and initial[i]]
           for k in range(168) if e.GOAL&(1<<k)}
    solutions={};nodes=0
    class Found(Exception):pass
    def admissible(i,chosen,domain):
        d=domain&initial[i]
        for j in chosen:
            if not d or masks[i]&masks[j]:return 0
            rel=pair(i,j)
            if rel is None:return 0
            d&=rules(rel)
        return d
    def visit(taken,chosen,domain):
        nonlocal nodes
        nodes+=1;remaining=e.GOAL&~taken
        if not remaining:
            pp=tuple(sorted((e.IDENTITY,)+tuple(records[i][0] for i in chosen)))
            e.require(pp not in solutions,'word-search duplicate')
            solutions[pp]=tuple(w for k,w in enumerate(words) if domain&(1<<k))
            if first_only:raise Found
            return
        best=None
        while remaining:
            bit=remaining&-remaining;k=bit.bit_length()-1;remaining^=bit;allowed=[]
            for i in users[k]:
                if masks[i]&taken:continue
                d=admissible(i,chosen,domain)
                if d:allowed.append((i,d))
            if not allowed:return
            if best is None or len(allowed)<len(best):best=allowed
        for i,d in best:visit(taken|masks[i],chosen+(i,),d)
    try:visit(0,(),ALL)
    except Found:pass
    return solutions,nodes

def occupied_stars(poses):
    occupied={}
    for p in poses:
        for j,v in enumerate(e.shape(p)[0]):
            mask=e.star_image(e.SECTORS[j],p[0],p[1]);old=occupied.get(v,0)
            e.require(not old&mask,'star overlap');occupied[v]=old|mask
    return occupied

def disk_boundary(poses):
    directed=Counter()
    for p in poses:
        poly=e.shape(p)[0]
        if p[1]:poly=tuple(reversed(poly))
        for i,a in enumerate(poly):
            b=poly[(i+1)%14]
            if directed[b,a]:directed[b,a]-=1
            else:directed[a,b]+=1
    edges=[edge for edge,n in directed.items() if n];succ=defaultdict(list);pred=defaultdict(list)
    for a,b in edges:succ[a].append(b);pred[b].append(a)
    if set(succ)!=set(pred) or any(len(succ[p])!=1 or len(pred[p])!=1 for p in succ):return False
    p=start=min(succ);visited=set()
    while p not in visited:visited.add(p);p=succ[p][0]
    return p==start and len(visited)==len(edges)

@lru_cache(40000)
def relative_geometry(p):return e.geometry(e.IDENTITY,p)

def check_branch_tree(tree,poses,w,chosen=(),stats=None):
    if stats is None:stats=Counter()
    old=occupied_stars(poses);occupied=dict(old)
    for p in chosen:
        for j,v in enumerate(e.shape(p)[0]):
            if v not in old:continue
            mask=e.star_image(e.SECTORS[j],p[0],p[1])
            e.require(not occupied[v]&mask,'branch chosen-star overlap');occupied[v]|=mask
    v=tuple(tree['vertex']);k=tree['sector']
    e.require(v in old and 0<=k<12 and not occupied[v]&(1<<k),'branch sector not missing')
    candidates={};allowed=set();stats['nodes']+=1
    for a in range(12):
        for flip in (0,1):
            for j,x in enumerate(e.VERTICES):
                p=(a,flip)+e.sub(v,independent_orient(a,flip,x))
                e.require(p not in candidates,'duplicate branch anchor')
                candidates[p]=e.star_image(e.SECTORS[j],a,flip)
    e.require(len(candidates)==336,'incomplete branch anchor list')
    stats['anchor_tests']+=len(candidates)
    for p,mask in candidates.items():
        if not mask&(1<<k) or mask&occupied[v]:continue
        stats['anchors_covering_missing_sector']+=1
        for inner in poses:
            rel=relative_geometry(e.compose(e.inverse(inner),p))
            if rel is None or not all(((w>>i)^(w>>j))&1 for i,j,rev in rel):break
        else:
            # Deliberately no outer/outer T or matching test: gaps, partial
            # contacts, pinches and holes at the final layer remain allowed.
            if any(positive_overlap(p,q) for q in chosen):continue
            if any(e.star_image(e.SECTORS[j],p[0],p[1])&occupied[x]
                   for j,x in enumerate(e.shape(p)[0]) if x in old):continue
            allowed.add(p)
    declared={tuple(row['pose']):row['child'] for row in tree['branches']}
    e.require(len(declared)==len(tree['branches']),'duplicate branch choice')
    e.require(set(declared)==allowed,'missing or extraneous branch option')
    for p,child in declared.items():check_branch_tree(child,poses,w,chosen+(p,),stats)
    return dict(stats)

def check_certificate(cert,found):
    declared={}
    for row in cert['first_surrounds']:
        poses=tuple(sorted(tuple(p) for p in row['poses']));ww=tuple(row['words'])
        e.require(poses not in declared,'duplicate first fixture');declared[poses]=ww
        e.require(e.IDENTITY in poses,'missing root')
        e.require(disk_boundary(poses),'first reference union is not a disk')
        stars=occupied_stars(poses)
        e.require(all(stars[v]==4095 for v in e.VERTICES),'root star not filled')
    e.require(declared==found,'incomplete or altered first-surround list')
    needed={(i,w) for i,r in enumerate(cert['first_surrounds']) for w in r['words']}
    seen=set();cut_candidates=0;cut_failures=Counter()
    for cut in cert['local_cuts']:
        k,w=cut['surround'],cut['word'];key=(k,w)
        e.require(key in needed and key not in seen,'duplicate or extraneous local cut');seen.add(key)
        poses=tuple(tuple(p) for p in cert['first_surrounds'][k]['poses'])
        vertex=tuple(cut['vertex']);sector=cut['sector'];stars=occupied_stars(poses)
        e.require(vertex in stars and 0<=sector<12,'bad cut vertex or sector')
        e.require(not(stars[vertex]&(1<<sector)),'cut sector already occupied')
        candidates={}
        for a in range(12):
            for f in (0,1):
                for j,v in enumerate(e.VERTICES):
                    pose=(a,f)+e.sub(vertex,independent_orient(a,f,v))
                    e.require(pose not in candidates,'duplicated vertex anchor')
                    candidates[pose]=e.star_image(e.SECTORS[j],a,f)
        e.require(len(candidates)==336,'missing anchored pose')
        for p,mask in candidates.items():
            if not mask&(1<<sector):continue
            cut_candidates+=1
            if mask&stars[vertex]:cut_failures['angle_overlap']+=1;continue
            for inner in poses:
                rel=relative_geometry(e.compose(e.inverse(inner),p))
                if rel is None:cut_failures['reference_overlap_or_T']+=1;break
                if not all(((w>>i)^(w>>j))&1 for i,j,v in rel):
                    cut_failures['profile_mismatch']+=1;break
            else:raise ValueError('local cut admits a covering tile')
    branches=[]
    for row in cert['branch_obstructions']:
        k,w=row['surround'],row['word'];key=(k,w)
        e.require(key in needed and key not in seen,'duplicate or extraneous branch obstruction');seen.add(key)
        poses=tuple(tuple(p) for p in cert['first_surrounds'][k]['poses'])
        branches.append(check_branch_tree(row['tree'],poses,w))
    e.require(seen==needed,'missing obstruction')
    return len(seen),cut_candidates,dict(sorted(cut_failures.items())),branches

def malformed_controls(cert,found):
    variants=[]
    c=deepcopy(cert);c['first_surrounds'].pop();variants.append(c)
    c=deepcopy(cert);c['first_surrounds'][0]['poses'][1][2]+=1;variants.append(c)
    c=deepcopy(cert);c['first_surrounds'][0]['words'][0]^=1;variants.append(c)
    c=deepcopy(cert);c['local_cuts'].pop();variants.append(c)
    c=deepcopy(cert);c['local_cuts'].append(deepcopy(c['local_cuts'][0]));variants.append(c)
    c=deepcopy(cert);c['local_cuts'][0]['vertex'][0]+=1;variants.append(c)
    c=deepcopy(cert);cut=c['local_cuts'][0]
    stars=occupied_stars(tuple(tuple(p) for p in c['first_surrounds'][cut['surround']]['poses']))
    occupied=stars[tuple(cut['vertex'])];cut['sector']=(occupied&-occupied).bit_length()-1;variants.append(c)
    c=deepcopy(cert);c['branch_obstructions'].clear();variants.append(c)
    c=deepcopy(cert);c['branch_obstructions'][0]['tree']['branches'].clear();variants.append(c)
    c=deepcopy(cert);c['branch_obstructions'][0]['tree']['branches'][0]['pose'][2]+=1;variants.append(c)
    for c in variants:
        try:check_certificate(c,found)
        except (ValueError,KeyError,IndexError):continue
        raise ValueError('malformed certificate accepted')
    return len(variants)

def refinement_frontier(graphs,classes):
    """All balanced coarsenings of old components not implying one tiler."""
    plane=set().union(*classes);frontier={};nodes=0;empty=0;direct=0
    for poses,g in sorted(graphs.items()):
        domain=set(all_graph_words(g))&plane
        if not domain:empty+=1;continue
        if any(domain<=c for c in classes):direct+=1;continue
        original=components(g);e.require(original is not None,'odd old graph')
        signatures={}
        def visit(base,remaining,cube,blocks):
            nonlocal nodes
            nodes+=1
            if not remaining:
                if any(set(cube)<=c for c in classes):return
                sig=tuple(sorted(tuple(sorted((mask&base,mask&(16383^base)))) for mask in blocks))
                signatures[sig]=tuple(sorted(cube));return
            bit=remaining&-remaining
            for w in sorted(domain):
                mask=base^w
                if not mask&bit or mask&~remaining:continue
                e.require(all(not mask&(a|b) or mask&(a|b)==(a|b) for a,b in original),'coarsening splits an old component')
                doubled=tuple(x^mask for x in cube)
                if any(x not in domain for x in doubled):continue
                visit(base,remaining^mask,cube+doubled,blocks+(mask,))
        for base in sorted(domain):
            if base<8192:visit(base,16383,(base,),())
        if signatures:
            old=tuple(sorted(tuple(sorted((a,b))) for a,b in original))
            e.require(set(signatures)=={old},'new nontrivial refinement case')
            e.require(len(old)==2 and sorted(a.bit_count() for a,b in old)==[3,4]
                      and all(a.bit_count()==b.bit_count() for a,b in old),'unexpected critical component sizes')
            e.require(set(all_graph_words(g))=={0xccb,0x1555,0x2aaa,0x3334},'unexpected critical colours')
            frontier[poses]=g
    e.require(len(frontier)==4,'critical prefix count changed')
    return frontier,{'refinement_nodes':nodes,'critical_prefixes':len(frontier),'empty_plane_domains':empty,'direct_class_domains':direct}

def refinement_cuts(cert,graphs,classes):
    frontier,stats=refinement_frontier(graphs,classes);seen=set();reasons=Counter();anchors=0
    for row in cert['refinement_cuts']:
        poses=tuple(sorted(tuple(p) for p in row['poses']))
        e.require(poses in frontier and poses not in seen,'missing/duplicate/extraneous refinement prefix');seen.add(poses)
        cc=components(frontier[poses]);implied=0
        for a,b in cc:
            for i in range(14):
                if a&(1<<i):implied|=b<<(14*i)
                if b&(1<<i):implied|=a<<(14*i)
        stars=occupied_stars(poses);v=tuple(row['vertex']);k=row['sector']
        e.require(v in stars and 0<=k<12 and not stars[v]&(1<<k),'refinement sector not missing')
        candidates={}
        for angle in range(12):
            for flip in (0,1):
                for j,x in enumerate(e.VERTICES):
                    p=(angle,flip)+e.sub(v,independent_orient(angle,flip,x))
                    e.require(p not in candidates,'duplicate refinement anchor')
                    candidates[p]=e.star_image(e.SECTORS[j],angle,flip)
        e.require(len(candidates)==336,'incomplete refinement anchors')
        for p,mask in candidates.items():
            if not mask&(1<<k):continue
            anchors+=1
            if mask&stars[v]:reasons['angle_overlap']+=1;continue
            for q in poses:
                rel=relative_geometry(e.compose(e.inverse(q),p))
                if rel is None:reasons['reference_overlap_or_T']+=1;break
                if edge_graph(rel)&~implied:reasons['forces_new_port_relation']+=1;break
            else:raise ValueError('critical graph admits a sector cover without a new relation')
    e.require(seen==set(frontier),'missing component-joining cut')
    stats.update({'sector_covering_anchors':anchors,'rejections':dict(sorted(reasons.items()))})
    return stats

def refinement_damage_controls(cert,graphs,classes):
    variants=[]
    c=deepcopy(cert);c['refinement_cuts'].pop();variants.append(c)
    c=deepcopy(cert);c['refinement_cuts'][0]['poses'][1][2]+=1;variants.append(c)
    c=deepcopy(cert);row=c['refinement_cuts'][0]
    stars=occupied_stars(tuple(tuple(p) for p in row['poses']))
    occupied=stars[tuple(row['vertex'])];row['sector']=(occupied&-occupied).bit_length()-1;variants.append(c)
    for c in variants:
        try:refinement_cuts(c,graphs,classes)
        except (ValueError,KeyError,IndexError):continue
        raise ValueError('damaged refinement certificate accepted')
    return len(variants)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected',action='store_true');args=parser.parse_args()
    cert=json.loads((HERE/'certificate.json').read_text())
    periodic,periodic_stats,classes=periodic_packings(cert['periodic_packings'])
    classes.append({0x1555,0x2aaa})
    EXCLUDED.update(periodic|{0x1555,0x2aaa})
    prototype_checks();records,raw=make_inventory();pair,tests=inventory_pairs(records)
    all_found,graph_nodes,graphs=graph_search(records,pair);graph_pair_tests=tests[0]
    control,word_nodes=word_search(records,pair);e.require(all_found==control,'independent searches differ')
    found={p:tuple(w for w in ww if w not in EXCLUDED) for p,ww in all_found.items() if set(ww)-EXCLUDED}
    cuts,anchors,reasons,branches=check_certificate(cert,found)
    balanced,_=word_search(records,pair,[0x1555],True)
    e.require(len(balanced)==1,'balanced Spectre calibration failed')
    balanced_poses=next(iter(balanced));e.require(disk_boundary(balanced_poses),'balanced calibration not a disk')
    malformed=malformed_controls(cert,found)
    refine=refinement_cuts(cert,graphs,classes)
    refined_damage=refinement_damage_controls(cert,graphs,classes)
    surviving=sorted({w for ww in found.values() for w in ww})
    result={'raw_vertex_poses':raw,'reference_neighbours':len(records),'root_missing_sectors':e.GOAL.bit_count(),
            'balanced_words':3432,'complement_representatives':1716,
            'all_balanced_first_prefixes':len(all_found),'all_balanced_first_word_count':len({w for ww in all_found.values() for w in ww}),
            'periodic_words':len(periodic),'periodic_packings':periodic_stats,'prior_plane_Spectre_words':2,
            'tested_non_tiling_representatives':1555,'first_surrounds':len(found),'surround_word_pairs':cuts,
            'surviving_words':surviving,'first_size_histogram':sorted(Counter(len(p) for p in found).items()),
            'graph_search_nodes':graph_nodes,'graph_search_pair_tests':graph_pair_tests,'word_search_nodes':word_nodes,
            'cut_anchored_candidates_covering_sector':anchors,'cut_rejection_counts':reasons,
            'local_cut_count':len(cert['local_cuts']),'branch_obstruction_stats':branches,
            'amplitude_refinement':refine,'refinement_damage_controls_rejected':refined_damage,
            'balanced_calibration_copies':len(balanced_poses),'malformed_controls_rejected':malformed,
            'certificate_sha256':hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest()}
    encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.expected:e.require(json.loads(encoded)==json.loads((HERE/'expected.json').read_text()),'expected result differs')
    print(encoded,end='')

if __name__=='__main__':main()
