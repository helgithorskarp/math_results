#!/usr/bin/env python3
"""Solver-free regular-(4,4;15) obstruction and hard R55 profile corollary."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
import importlib.util
from itertools import combinations,permutations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import gluing
import literal_check

HERE=Path(__file__).resolve().parent
PROFILE='0,2,3,38,0,0,0'
PINS={
 'ramsey_r55_common_neighbor_squeeze/verify.py':'95e34f12c73fcbe93f4dea8da27bcf09e22185827efc4cdfb5aee1c37f6ec16d',
 'ramsey_r55_common_neighbor_squeeze/report.json':'2a09b4a391fb97f3a9ffcab0dfeb7f4c0924d0cb84154f249c90f1ec9fc4aecf',
 'ramsey_r55_ten_edge_cell_obstruction/verify.py':'e8b88da1b0c5d63877dd93636e99e9f3bdc8aa2f9e95cf8a6d00d66888e6de2f',
 'ramsey_r55_degree19_triangle_exclusion/verify.py':'69f3dfd46ced7ad162bce81c0e6ddda1baed94452b9f7e6eb6d25235e34d184c',
}


def require(ok,detail):
    if not ok:raise ValueError(detail)


def load(name,relative):
    spec=importlib.util.spec_from_file_location(name,HERE.parent/relative)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def from_code(n,mask):
    adj=[0]*n
    for k,(a,b) in enumerate(combinations(range(n),2)):
        if mask>>k&1:adj[a]|=1<<b;adj[b]|=1<<a
    return tuple(adj)


def encode(adj):
    return sum(1<<k for k,(a,b) in enumerate(combinations(range(len(adj)),2)) if adj[a]>>b&1)


def as_sets(adj):
    return [{j for j in range(len(adj)) if a>>j&1} for a in adj]


def complement(adj):
    full=(1<<len(adj))-1
    return tuple(full^(1<<i)^a for i,a in enumerate(adj))


def valid(adj,r,b):
    for k,red in ((r,True),(b,False)):
        for S in combinations(range(len(adj)),k):
            if all(bool(adj[a]>>bb&1)==red for a,bb in combinations(S,2)):return False
    return True


def six_census(ten):
    # Exhaust all 2^15 edge-bit assignments, independent of vertex augmentation.
    good={mask for mask in range(1<<15) if valid(from_code(6,mask),3,4)}
    augmented={encode(g) for g in ten.augment(6)}
    require(good==augmented and len(good)==2812,'complete independent six-vertex census')
    left=set(good);records=[];ranks={e:k for k,e in enumerate(combinations(range(6),2))}
    while left:
        key=min(left);adj=from_code(6,key)
        edges=[e for e in ranks if adj[e[0]]>>e[1]&1]
        orbit={sum(1<<ranks[tuple(sorted((p[a],p[b])))] for a,b in edges) for p in permutations(range(6))}
        require(orbit<=left,'complete disjoint six-vertex permutation orbit')
        left-=orbit
        records.append({'blue_side_complement_mask':key,'labeled_graphs':len(orbit),
                        'complement_edges':len(edges),'automorphisms':720//len(orbit)})
    require(len(records)==15 and sum(r['labeled_graphs'] for r in records)==2812,'fifteen classes')
    return records


def decode(H,B,rows):
    n=len(H);m=len(B);root=n+m;adj=[set() for _ in range(root+1)]
    for i in range(n):
        adj[i]|={j for j in range(n) if H[i]>>j&1}|{root}
        adj[i]|={n+b for b in range(m) if rows[i]>>b&1};adj[root].add(i)
    for b in range(m):
        adj[n+b]|={n+c for c in range(m) if B[b]>>c&1}
        adj[n+b]|={i for i in range(n) if rows[i]>>b&1}
    return adj


def check_graph(adj,degree):
    require(all(len(s)==degree for s in adj),'literal regularity')
    require(all(i not in adj[i] and all((j in adj[i])==(i in adj[j]) for j in range(len(adj)))
                for i in range(len(adj))),'literal simple graph')
    require(all(len({b in adj[a] for a,b in combinations(S,2)})>1
                for S in combinations(range(len(adj)),4)),'literal no monochromatic K4')


def controls():
    # Rook graph on a 3x3 board: degree four, clique/independence numbers three.
    rook=[{j for j in range(9) if i!=j and (i//3==j//3 or i%3==j%3)} for i in range(9)]
    check_graph(rook,4);hs=sorted(rook[0]);bs=sorted(set(range(1,9))-set(hs))
    H=tuple(sum(1<<j for j,w in enumerate(hs) if w in rook[v]) for v in hs)
    B=tuple(sum(1<<j for j,w in enumerate(bs) if w in rook[v]) for v in bs)
    actual=tuple(sum(1<<j for j,w in enumerate(bs) if w in rook[v]) for v in hs)
    first=gluing.search(H,B);second=literal_check.search(as_sets(H),as_sets(B))
    require(first['solutions']==second['solutions'] and actual in first['solutions'],'entry-level positive gluing agreement')
    for rows in first['solutions']:check_graph(decode(H,B,rows),4)
    negative=0
    changed=list(actual);changed[0]^=1
    try:check_graph(decode(H,B,changed),4)
    except ValueError:negative+=1
    else:raise ValueError('changed cross edge accepted')
    complete=[set(range(5))-{v} for v in range(5)]
    try:check_graph(complete,4)
    except ValueError as e:require(str(e)=='literal no monochromatic K4','negative wrong cause');negative+=1
    else:raise ValueError('regular complete graph accepted')
    return {'positive_order':9,'positive_degree':4,'complete_cross_matrix_count':len(first['solutions']),
            'all_positive_models_decoded':True,'negative_tests':negative}


def regular_obstruction(ten):
    eight=ten.classify_w()  # Complete augmentation/orbits plus its separate <=6 brute checks.
    require([r['lex_mask'] for r in eight['classes']]==[5388912,5404008,5683824],'three critical eight types')
    six=six_census(ten);cases=[];balanced=[]
    for h in eight['classes']:
        H=from_code(8,h['lex_mask']);eh=h['edges']
        for b in six:
            B=complement(from_code(6,b['blue_side_complement_mask']));eb=15-b['complement_edges']
            # Both sides must account for the same number of red cross edges.
            if 56-2*eh!=48-2*eb:continue
            require(eh-eb==4,'edge balance equivalence')
            balanced.append((h['lex_mask'],b['blue_side_complement_mask']))
            first=gluing.search(H,B);second=literal_check.search(as_sets(H),as_sets(B))
            require(first['solutions']==second['solutions']==[],'both complete gluing algorithms exclude case')
            cases.append({'H_mask':h['lex_mask'],'B_complement_mask':b['blue_side_complement_mask'],
                          'H_edges':eh,'B_edges':eb,'cross_edge_total':56-2*eh,
                          'row_domain':first['domain_sizes'],'search_order':first['row_order'],
                          'search_nodes':first['nodes_by_depth'],'literal_nodes':second['nodes_by_depth'],
                          'literal_attempted_rows':second['attempted_rows'],'completions':0})
    expected=[(5388912,4060),(5404008,2012),(5683824,954),(5683824,956),(5683824,1884)]
    require(balanced==expected,'all five balanced pairs among all 45 pair types')
    require(sum(sum(r['search_nodes']) for r in cases)==4261,'complete compact search count')
    return {'eight_vertex_classification':eight,'six_vertex_classes':six,'pair_types_before_balance':45,
            'balanced_pair_types':5,'cases':cases,'eight_regular_R44_order15_exists':False}


def campaign():
    # Recompute the immediately preceding profile reduction and its full parent chain.
    path=HERE.parent/'ramsey_r55_common_neighbor_squeeze/verify.py'
    with tempfile.TemporaryDirectory(prefix='r55-regular15-') as scratch:
        report=Path(scratch)/'parent.json'
        run=subprocess.run([sys.executable,'-O',str(path),'--report',str(report)],
                           check=True,capture_output=True,text=True)
        require(run.stdout==(path.parent/'EXPECTED_OUTPUT.txt').read_text(),'common-root complete replay')
        require(sha256(report.read_bytes()).hexdigest()==PINS['ramsey_r55_common_neighbor_squeeze/report.json'],
                'fresh common-root report')
        previous=json.loads(report.read_text())['campaign']
    require(previous['surviving_pattern']['A']==[4,2,8],'necessary parent pattern')
    # Its proof forces P union {4} to be eight-regular Ramsey(4,4;15), now impossible.
    require(14+1==15 and 2*52+2*8==15*8,'regular-side degree and edge identity')
    single=load('regular15_previous_exclusion','ramsey_r55_degree19_triangle_exclusion/verify.py')
    run=subprocess.run([sys.executable,str(single.HERE/'verify.py')],check=True,capture_output=True,text=True)
    require(run.stdout==(single.HERE/'EXPECTED_OUTPUT.txt').read_text(),'previous single-degree19 replay')
    old=single.cumulative_totals()
    require(old['global_candidates']==67 and old['anchored_split_candidates']==273,'previous cumulative totals')
    with (HERE.parent/'ramsey_r55_exceptional_degree_sieve/PROFILES.tsv').open() as stream:
        removed=[r for r in csv.DictReader(stream,delimiter='\t') if r['counts_18_to_24']==PROFILE]
    require(len(removed)==1 and removed[0]['status']=='feasible' and removed[0]['M']=='217'
            and removed[0]['split_count']=='2','exact new global and split target')
    # Check that this row survived all earlier screens and is distinct from the old deletion.
    for file,column in [('ramsey_r55_exceptional_signature_capacity/CENSUS.tsv','pass'),
                        ('ramsey_r55_coupled_signature_counts/SUMMARY.tsv','primal_cores'),
                        ('ramsey_r55_signature_union_cuts/SUMMARY.tsv','primal_cores')]:
        with (HERE.parent/file).open() as stream:rows=[r for r in csv.DictReader(stream,delimiter='\t') if r['counts_18_to_24']==PROFILE]
        require(len(rows)==1 and int(rows[0][column])>0,'target survived earlier screen')
    require(PROFILE!=single.COUNTS,'not double-counting previous profile exclusion')
    globals_by_M=old['global_M214_to_M220'].copy();splits_by_M=old['split_M214_to_M220'].copy()
    globals_by_M[3]-=1;splits_by_M[3]-=2
    require(sum(globals_by_M)==66 and sum(splits_by_M)==271,'new exact totals')
    return {'excluded_profile':PROFILE,'excluded_M':217,'global_candidates':66,'anchored_split_candidates':271,
            'global_M214_to_M220':globals_by_M,'split_M214_to_M220':splits_by_M,
            'hard_branch_only':True,'target_graph_found':False}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path);args=ap.parse_args()
    for name,digest in PINS.items():require(sha256((HERE.parent/name).read_bytes()).hexdigest()==digest,name)
    ten=load('regular15_critical_census','ramsey_r55_ten_edge_cell_obstruction/verify.py')
    report={'regular_obstruction':regular_obstruction(ten),'controls':controls(),'campaign':campaign(),
            'solver_used':False,'catalog_completeness_used':False}
    if args.report:args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('PASS complete small census: three (3,4;8) types and fifteen (3,4;6) types')
    print('PASS all 45 rooted type pairs reduce by degree balance to five cases')
    print('PASS all five cross-matrix cases excluded by two exact algorithms; 4261 production nodes')
    print('PASS positive regular-nine control: complete model sets agree and all decode to literal Ramsey graphs')
    print('PASS changed-edge and monochromatic-clique negative controls')
    print('PASS full common-root and previous profile-exclusion replay')
    print('THEOREM no eight-regular (4,4;15) graph; hard profile 19^2 20^3 21^38 excluded')
    print('CAMPAIGN 66 global profiles and 271 anchored splits remain; no target graph or new Ramsey lower bound')


if __name__=='__main__':main()
