#!/usr/bin/env python3
"""Exact audit of the common-neighbor squeeze; no solver is imported."""
import argparse
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
PINS={
    'ramsey_r55_paired_neighborhood_budget/verify.py':
        '518a05072a726287628c57e8c9d9bc16aac4380dd800b4d807d00208b6b6e624',
    'ramsey_r55_ten_edge_cell_obstruction/verify.py':
        'e8b88da1b0c5d63877dd93636e99e9f3bdc8aa2f9e95cf8a6d00d66888e6de2f',
}
P=frozenset((5,9,17));Q=frozenset((6,10,18))


def require(ok,detail):
    if not ok:raise ValueError(detail)


def graph(n,edges):
    adj=[set() for _ in range(n)]
    for a,b in edges:
        require(0<=a<b<n,'simple edge')
        adj[a].add(b);adj[b].add(a)
    return adj


def monochromatic(adj,vs,red):
    return all((b in adj[a])==red for a,b in combinations(vs,2))


def has_clique(adj,vs,k,red):
    return any(monochromatic(adj,s,red) for s in combinations(vs,k))


def edge_count(adj,vs,ws=None):
    if ws is None:return sum(b in adj[a] for a,b in combinations(vs,2))
    require(not vs&ws,'disjoint cross sets')
    return sum(b in adj[a] for a in vs for b in ws)


def intersection_audit(adj,z,w,C,cap=8,check_types=False):
    """Literal graph audit of the lemma and the strengthened paired bound."""
    require(z!=w and not {z,w}&C,'distinct roots outside C')
    J=adj[z]&C;K=adj[w]&C;U=J&K;P0=J-K;Q0=K-J;W=C-(J|K)
    outside=set(range(len(adj)))-C-{z,w}
    Fz=(adj[z]-adj[w])&outside;Fw=(adj[w]-adj[z])&outside
    for u in U:
        for root,opposite,side in ((z,w,P0),(w,z,Q0)):
            pool=adj[u]&side
            require(len(pool)<=cap,'common-root degree cap')
            if check_types:
                require(u in adj[root] and u in adj[opposite],'common-neighbor hypothesis')
                require(not has_clique(adj,pool,3,True) and not has_clique(adj,pool,4,False),
                        'literal common pool has type (3,4)')
        require(len(adj[u]&W)>=len(adj[u]&C)-16-(len(U)-1),'leak lower bound')
    D=edge_count(adj,P0,Fz)+edge_count(adj,Q0,Fw)
    left=2*(edge_count(adj,J)+edge_count(adj,K))
    right=8*(len(P0)+len(Q0))-D+32*len(U)+2*len(U)*(len(U)-1)
    require(left<=right,'strengthened paired bound')
    return len(U),left,right


def literal_tests():
    small=overlap=0
    pairs=list(combinations(range(5),2))
    for mask in range(1024):
        adj=graph(5,[e for k,e in enumerate(pairs) if mask>>k&1])
        if any(monochromatic(adj,range(5),red) for red in (True,False)):continue
        for z,w in permutations(range(5),2):
            rest=sorted(set(range(5))-{z,w})
            for bits in range(8):
                C={v for k,v in enumerate(rest) if bits>>k&1}
                u,_,_=intersection_audit(adj,z,w,C,check_types=True)
                small+=1;overlap+=int(u>0)
    # A separate 19-vertex literal Ramsey fixture, from Paley(17) plus two roots.
    residues={x*x%17 for x in range(1,17)}
    large=graph(19,[(a,b) for a,b in combinations(range(17),2) if (b-a)%17 in residues]
                +[(v,17) for v in range(17)]+[(17,18)])
    require(not has_clique(large,range(19),5,True) and not has_clique(large,range(19),5,False),
            'literal 19-vertex fixture is Ramsey')
    checks=0
    for z,w in permutations(range(19),2):
        rest=set(range(19))-{z,w}
        for omitted in sorted(rest):
            intersection_audit(large,z,w,rest-{omitted},check_types=True);checks+=1
    # The cap eight is attained: two red roots over a critical (3,4;8) graph.
    edges=[(0,2),(0,3),(1,2),(1,3),(0,4),(1,5),(2,6),(3,7),(4,5),(6,7)]
    sharp=graph(11,edges+[(v,r) for v in range(8) for r in (8,9)]+[(8,9),(9,10)])
    require(not has_clique(sharp,range(11),5,True) and not has_clique(sharp,range(11),5,False),
            'sharp eight-cap fixture is Ramsey')
    intersection_audit(sharp,8,10,set(range(8))|{9},check_types=True)
    require(len(sharp[9]&set(range(8)))==8,'attained common-root capacity')
    negatives=0
    try:intersection_audit(sharp,8,10,set(range(8))|{9},cap=7)
    except ValueError as e:require(str(e)=='common-root degree cap','negative wrong cause');negatives+=1
    else:raise ValueError('false cap seven accepted')
    bad=graph(12,[(v,r) for v in range(9) for r in (9,10)]+[(9,10),(10,11)])
    try:intersection_audit(bad,9,11,set(range(9))|{10})
    except ValueError as e:require(str(e)=='common-root degree cap','negative wrong cause');negatives+=1
    else:raise ValueError('Ramsey hypothesis omitted')
    require((small,overlap,checks)==(163520,53940,5814),'literal test coverage')
    return {'small_graph_partitions':small,'small_nonempty_U':overlap,
            'large_graph_partitions':checks,'sharp_common_root_capacity':8},negatives


def parent():
    for rel,digest in PINS.items():require(sha256((HERE.parent/rel).read_bytes()).hexdigest()==digest,rel)
    path=HERE.parent/'ramsey_r55_ten_edge_cell_obstruction/verify.py'
    replay=subprocess.run([sys.executable,'-O',str(path)],check=True,capture_output=True,text=True)
    require(replay.stdout==(path.parent/'EXPECTED_OUTPUT.txt').read_text(),'complete ten-edge and paired replay')
    path=HERE.parent/'ramsey_r55_paired_neighborhood_budget/verify.py'
    spec=importlib.util.spec_from_file_location('common_root_parent',path)
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    _,union=p.inputs();union.check_ramsey_table()
    require(union.RAMSEY[2][3]==9,'elementary R(3,4) upper bound')
    return p,union


def extra_rows(y,pairs,k):
    """Exactly eleven new equality rows; no individual edges are encoded."""
    rows=[]
    def add(name,row,value):rows.append((name,row,value,value))
    for cell in sorted(P|Q):
        side=P if cell in P else Q
        row=[int(a==cell and b in side)+int(b==cell and a in side) for a,b in pairs]
        add(('side_degree',cell),row,(7 if cell in (17,10) else 8)*y[cell])
    add(('U_internal',),[int((a,b)==(3,3)) for a,b in pairs],1)
    for name,side,value in [('P',P,16),('Q',Q,16),('W',{28},4)]:
        add(('U_cross',name),[int(a==3 and b in side) for a,b in pairs],value)
    add(('W_edges',),[int((a,b)==(28,28)) for a,b in pairs],k)
    return rows


def check_extra(y,pairs,e,k):
    for name,row,lo,hi in extra_rows(y,pairs,k):
        require(lo<=sum(v*c for v,c in zip(e,row))<=hi,('new equality',name))


def campaign(p,union):
    patterns=[]
    E=graph(5,[(0,1),(0,2),(0,4),(1,2),(1,3),(2,3),(2,4)])
    for a in range(3,6):
        for b in range(2,5):
            if not 6<=a+b<=8:continue
            y=p.normal_form(a,b);D=y[17]+y[10]
            # Sum of the two exceptional local edge counts is 154-D.
            local_sum=154-D
            direct_local=[]
            for root in (0,1):
                fixed=edge_count(E,E[root])
                fixed+=sum(v*sum((x>>j)&1 for j in E[root]) for x,v in enumerate(y) if x>>root&1)
                direct_local.append(85-fixed)
            require(direct_local==[67+b,63+a+b] and sum(direct_local)==local_sum,
                    'literal exceptional-neighborhood decomposition')
            require(sum(y)==38 and y[3]==2 and 21-(3).bit_count()==19,'central U degree data')
            pairs,_,_=p.edge_rows(y,E,union)
            # Coefficient-level check: (e(J)+e(K))-sum_U d_C=e(P)+e(Q)-e(U,W).
            for x,z in pairs:
                local=int(bool(x&z&1))+int(bool(x&z&2))
                udegree=int(x==3)+int(z==3)
                side=int(x in P and z in P)+int(x in Q and z in Q)
                leak=int((x,z)==(3,28))
                require(local-udegree==side-leak,'slack identity coefficients')
            require(224-D-2*(local_sum-38)==D-8,'slack identity constant')
            # Old side degree caps plus the two common-root degree caps and |U|=2.
            upper_twice=8*28-D+32*2+2*2*(2-1)
            leak_max=(D-8)//2
            keep=2*local_sum<=upper_twice
            require(keep==(leak_max>=4),'independent squeeze formulations agree')
            patterns.append({'A':[a,b,14-a-b],'B':[8-a,10-b,a+b-4],
                             'D':D,'old_U_W_upper':leak_max,'U_W_lower':4,
                             'paired_lhs':2*local_sum,'paired_rhs':upper_twice,'retained':keep})
    retained=[r for r in patterns if r['retained']]
    require(len(patterns)==7 and len(retained)==1 and retained[0]['A']==[4,2,8], 'sole cell pattern')
    # All five nonnegative slack terms in the equality case vanish.
    require(2*138==8*28-16+64+4,'exact equality in strengthened bound')
    require(2*52+8==8*14 and 2*52+8==8*14,'saturated side degrees')
    require(2*1+16+16+4==2*19,'U degree budget')
    require(14+1==15 and (14*8+8)//2==60,'two eight-regular 15-vertex rooted sides')
    y=p.normal_form(4,2);near=p.adjacency(443,5)
    pairs,caps,oldrows=p.edge_rows(y,near,union)
    records=json.loads((HERE/'EDGE_WITNESSES.json').read_text())
    require([r['W_edges'] for r in records]==[11,12],'two separate edge-count witnesses')
    summaries=[]
    for r in records:
        require(r['a']==[4,2,8],'witness pattern')
        e=r['edge_counts'];k=r['W_edges'];p.check_edge_witness(y,e,near,union)
        check_extra(y,pairs,e,k)
        values={pair:v for pair,v in zip(pairs,e)}
        internal=lambda side:sum(v for (a,b),v in values.items() if a in side and b in side)
        cross=lambda left,right:sum(v for (a,b),v in values.items() if (a in left and b in right) or (a in right and b in left))
        require(internal(P)==internal(Q)==52,'two side edge counts')
        require(cross(P,{28})==cross(Q,{28})==70-k,'side-to-W edge counts')
        require(cross(P,Q)==76+k,'P-Q edge count')
        require(sum(e)==357,'central total')
        summaries.append({'W_edges':k,'P_edges':52,'Q_edges':52,'P_W':70-k,'Q_W':70-k,
                          'P_Q':76+k,'old_rows':len(oldrows),'new_rows':len(extra_rows(y,pairs,k)),
                          'edge_variables':len(e)})
    negatives=0
    changed=records[0]['edge_counts'].copy();changed[pairs.index((3,3))]=0
    try:check_extra(y,pairs,changed,11)
    except ValueError:negatives+=1
    else:raise ValueError('missing U edge accepted')
    old=json.loads((HERE.parent/'ramsey_r55_ten_edge_cell_obstruction/EDGE_WITNESSES.json').read_text())
    old=next(r['edge_counts'] for r in old if r['a']==[4,2,8])
    try:check_extra(y,pairs,old,old[pairs.index((28,28))])
    except ValueError:negatives+=1
    else:raise ValueError('old weaker witness accepted')
    return {'patterns':patterns,'surviving_pattern':retained[0],
            'aggregate_witnesses':summaries,'pattern_W_templates_before':14,'pattern_W_templates_after':2,
            'global_profiles':67,'anchored_splits':273,'target_graph_found':False},negatives


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--report',type=Path);args=ap.parse_args()
    p,union=parent();tests,n1=literal_tests();result,n2=campaign(p,union)
    report={'literal_tests':tests,'campaign':result,'negative_tests':n1+n2,
            'proof_uses_solver':False,'aggregate_witnesses_are_graphs':False}
    require(n1+n2==4,'four negative tests')
    if args.report:args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('PASS complete paired and ten-edge parent replay')
    print('PASS common-root degree cap eight; literal small/large graph tests and sharp fixture')
    print('PASS seven patterns reduced to A=(4,2,8), B=(4,8,2), for either remaining W type')
    print('PASS U is a red edge; each endpoint has P/Q/W red degrees 8/8/2')
    print('PASS both 15-vertex rooted sides must be eight-regular (4,4) graphs')
    print('PASS two exact aggregate witnesses: W edges 11 and 12; 153 old plus 11 new rows each')
    print('PASS four negative tests; solver-free verifier')
    print('SCOPE two pattern/W templates remain; no whole-profile exclusion or target; totals 67/273 unchanged')


if __name__=='__main__':main()
