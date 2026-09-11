"""Finite mathematics and complete orbit audit for the four-edge layer."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import argparse,copy,hashlib,json
from a0_inventory import profiles
from a0_independent import inventory
from four_edge_orbits import forest,components
from four_edge_sat import near_partitions,cases,proof_stage
from verify_four_edge_orbits import audit
from verify_a0_multi_quad import unit_controls

HERE=Path(__file__).resolve().parent
ORBIT_ROLES=((0,1,1),(0,2,0),(0,3,0),(0,4,0),(1,2,0),(1,3,0),(2,2,0),(3,2,0))

def need(test,why):
    if not test:raise ValueError(why)

def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def one_quad_frames():
    pairs=[{2*i,2*i+1} for i in range(4)]
    choices=[]
    for i in range(4):
        other=[j for j in range(4) if j!=i];row=[]
        for bits in product((0,1),repeat=2):
            word=(0,)+bits
            A={2*j+b for j,b in zip(other,word)}
            B={2*j+1-b for j,b in zip(other,word)}
            row.append((A,B))
        choices.append(row)
    good=[]
    for word in product(range(4),repeat=4):
        triples=[B for i,j in enumerate(word) for B in choices[i][j]]
        if any(len(A&B)>1 for A,B in combinations(triples,2)):continue
        covered=[tuple(sorted(e)) for B in pairs+triples for e in combinations(B,2)]
        need(len(covered)==28 and len(set(covered))==28,"four-bad pair coverage")
        good.append([list(word),[sorted(B) for B in triples]])
    need(bool(good),"positive linear frame control")
    return dict(choices_checked=256,linear_frames=len(good),frames_sha256=digest(good),covered_pairs=28)

def partition_controls():
    points=set(range(4))
    vertices=[(6,frozenset(),j) for j in range(3)]
    vertices += [(6,frozenset(B),0) for r in range(1,5) for B in combinations(range(4),r)]
    rows=[]
    for mask in range(16):
        R=frozenset(t for t in points if mask>>t&1)
        eligible=[i for i,(d,B,j) in enumerate(vertices) if B<=R]
        for count in range(1,4):
            generated=list(near_partitions(R,count,eligible,vertices))
            reference=set()
            for chosen in combinations(eligible,count):
                blocks=[vertices[i][1] for i in chosen]
                if any(A&B for A,B in combinations(blocks,2)):continue
                if set().union(*blocks)==R:reference.add(chosen)
            need(len(generated)==len(set(generated)),"duplicate unordered partition")
            need(set(generated)==reference,"incomplete partition generator")
            rows.append([mask,count,sorted(reference)])
    return dict(instances=len(rows),partitions=sum(len(r[2]) for r in rows),entry_sha256=digest(rows))

def witness(r):
    index,fid,orbit=r['case'];m,k,six,seven=list(profiles())[index];H=forest(fid)
    V={i:(d,set(B)) for i,d,B,j in r['vertices']}
    need(len(V)==42,"low vertex total")
    quads={i:B for i,(d,B) in V.items() if len(B)==4}
    N={t:set() for t in range(12)}
    for t,u in H:N[t].add(u);N[u].add(t)
    for d,counts in ((6,six),(7,seven)):
        need([sum(dd==d and len(B)==c for dd,B in V.values()) for c in range(len(counts))]==list(counts),"profile")
    for d,B in V.values():
        need(B<=set(range(12)),"point range")
        need(all(u not in N[t] and not N[u]&N[t] for t,u in combinations(B,2)),"H-square independence")
    need(all(len(A&B)<=1 for (d,A),(dd,B) in combinations(V.values(),2)),"high-set linearity")
    for t in range(12):
        need(sum(d==6 and t in B for d,B in V.values())==3+len(N[t]),"six point quota")
        need(sum(d==7 and t in B for d,B in V.values())==5-2*len(N[t]),"seven point quota")
        for u in range(t+1,12):
            need(int(u in N[t])+len(N[t]&N[u])+sum(t in B and u in B for d,B in V.values())==1,"high pair")
    near={q:set() for q in quads};far={q:set() for q in quads}
    for q,v in r['near']:need(q in quads and v in V and q!=v,"near endpoints");near[q].add(v)
    for u,v in r['far']:
        need(u in V and v in V and u!=v,"far endpoints")
        if u in quads:far[u].add(v)
        if v in quads:far[v].add(u)
    charge=0
    for q,Q in quads.items():
        d=V[q][0];eps=(d==7)+sum(V[v][0]==7 for v in near[q]);charge+=eps
        need(len(near[q])==d-4,"quad low degree")
        R=set(range(12))-Q-set().union(*(N[t] for t in Q))
        need(Counter(t for v in near[q] for t in V[v][1])==Counter(R),"quad near partition")
        need(len(far[q])==(9 if d==6 else 4)-eps,"quad far cardinality")
        need(not near[q]&far[q],"near far overlap")
        need(all(not Q&V[v][1] for v in far[q]),"own-set far avoidance")
        need(Counter(t for v in far[q] for t in V[v][1])==Counter({t:8-d for t in set(range(12))-Q}),"far multiplicity")
        for other in quads:need((other in near[q])==(q in near[other]),"quad adjacency symmetry")
    bad=set();helpers=[];helper6={q:set() for q in quads};weight=0
    for v,fs in r['covers']:
        need(v in V and v not in bad,"bad vertex distinct");bad.add(v);d,B=V[v]
        need(d==7 and len(B) in (1,2),"bad type")
        need(len(fs)==len(set(fs))==3 and v not in fs and all(u in V for u in fs),"far endpoints distinct")
        C=Counter(B)
        for u in fs:C.update(V[u][1])
        need(C==Counter(range(12)),"bad far partition")
        qs=[q for q in fs if q in quads]
        need(len(qs)>=1 and (len(B)!=1 or len(qs)==2),"quad cover type")
        for q in quads:need((v in far[q])==(q in fs),"quad far reciprocity")
        if len(qs)==1:
            hs=[u for u in fs if u not in quads];need(all(len(V[u][1])==3 for u in hs),"triple helpers")
            helpers.extend(hs);helper6[qs[0]].update(u for u in hs if V[u][0]==6)
        weight+=3-len(B)
    need(len(helpers)==len(set(helpers)),"single-quad helper reuse")
    need(weight>=4+charge+6*six[0]+2*six[1],"charge inequality")
    if r['stage']=='packing':
        for q,Q in quads.items():
            sigma=sum(len(N[t]) for t in Q);d=V[q][0]
            outside6=4-sigma+3*(d==6);outside7=6+2*sigma+3*(d==7)
            need(sum(v!=q and dd==6 and not B&Q for v,(dd,B) in V.items())==outside6,"outside six census")
            need(sum(v!=q and dd==7 and not B&Q for v,(dd,B) in V.items())==outside7,"outside seven census")
            small={u for u in near[q] if V[u][0]==6 and len(V[u][1])!=3}
            need(not helper6[q]&small and len(helper6[q])+len(small)<=outside6,"helper and near packing")
    return dict(case=r['case'],stage=r['stage'],bad_vertices=len(bad),weight=weight,quad_charge=charge)

def finite():
    census=list(profiles());need(sorted(census)==inventory(),"independent inventory")
    raw=[(i,*r) for i,r in enumerate(census) if r[0]==4 and not any(r[2][5:]) and not any(r[3][5:])]
    buckets={key:[] for key in ('zero','one_six','one_seven','multiple')}
    for row in raw:
        i,m,k,s,t=row;q=s[4]+t[4]
        category='zero' if q==0 else 'multiple' if q>=2 else 'one_six' if s[4] else 'one_seven'
        buckets[category].append(i)
        if category=='one_six':need(t[3]<=3,"seven-helper inventory bound")
    need({k:len(v) for k,v in buckets.items()}==dict(zero=33,one_six=20,one_seven=4,multiple=16),"raw layer cover")
    fixtures=json.loads((HERE/'four_edge_controls.json').read_text());positive=[witness(r) for r in fixtures]
    mutants=[]
    x=copy.deepcopy(fixtures[0]);x['covers'][0][1].pop();mutants.append(x)
    x=copy.deepcopy(fixtures[0]);x['near'].pop();mutants.append(x)
    for x in mutants:
        try:witness(x)
        except ValueError:pass
        else:raise ValueError('Malformed fixture accepted')
    root_rows=[]
    for d in (6,7):
        for seven_neighbors in range(d-3):
            neighbor_degree_sum=4*8+(d-4-seven_neighbors)*6+seven_neighbors*7
            far=53-neighbor_degree_sum
            need(far+seven_neighbors==(9 if d==6 else 3),"quad far row")
            root_rows.append([d,seven_neighbors,far])
    previous=json.loads((HERE/'a0_multi_quad_expected.json').read_text())['finite_controls']
    remaining=[r for r in previous['remaining_profiles'] if r[1]==3]
    forests=[r for r in previous['remaining_high_forests'] if r['m']==3]
    need(len(remaining)==23 and len(forests)==3,"campaign remainder")
    return dict(raw_profiles=raw,human_buckets=buckets,one_quad_frames=one_quad_frames(),
                partition_controls=partition_controls(),positive_relaxation_controls=positive,rejected_mutants=len(mutants),
                quad_far_rows=root_rows,unit_controls=unit_controls(),remaining_profiles=remaining,remaining_high_forests=forests)

def orbit_summary():
    rows=[]
    for args in ORBIT_ROLES:
        r=audit(*args);records=r.pop('records');r['orbit_records_sha256']=digest(records);rows.append(r)
    return rows

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--finite-only',action='store_true');args=parser.parse_args()
    out={'finite':finite()}
    if not args.finite_only:
        out['orbits']=orbit_summary()
        case_list=list(cases())
        need(len(case_list)==3721,"complete case count")
        out['cases']={'count':len(case_list),'stage_counts':dict(Counter(proof_stage(c) for c in case_list)),
                      'case_list_sha256':digest(case_list)}
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':main()
