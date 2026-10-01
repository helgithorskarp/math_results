"""Separate binary/edge-set representation; no production-code import.
six-tammes-1, researcher. Not independent mathematical peer review.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

LABELS=('U','V','F','G','A','D','B')+tuple('o'+str(i) for i in range(8))
DEGREES=(3,3,5,5,4,4,4)+(4,)*8
TRIANGLES=(0,0,4,2,1,1,0)+(2,)*8


def need(b,m):
    if not b:
        raise ValueError(m)


def edge_stars(names,t,rt=(),rq=(),zero=(),qq_exact=None):
    n=len(names);edges=list(combinations(range(n),2));ids={x:i for i,x in enumerate(names)}
    tt={edges.index(tuple(sorted((ids[a],ids[b])))) for a,b in rt}
    qreq={edges.index(tuple(sorted((ids[a],ids[b])))) for a,b in rq}
    zero_ids={ids[x] for x in zero}
    exact=None if qq_exact is None else {ids[x] for x in qq_exact}
    out=[];cycles=0
    for chosen in combinations(range(len(edges)),n):
        adj=[set() for _ in range(n)]
        for k in chosen:
            a,b=edges[k];adj[a].add(b);adj[b].add(a)
        if any(len(s)!=2 for s in adj):
            continue
        seen={0};todo=[0]
        while todo:
            v=todo.pop()
            for x in adj[v]-seen:
                seen.add(x);todo.append(x)
        if len(seen)!=n:
            continue
        cycles+=1
        for t_indices in combinations(chosen,t):
            ts=set(t_indices);qs=set(chosen)-ts
            if not tt<=ts or not qreq<=qs or any(i in edges[k] for i in zero_ids for k in ts):
                continue
            covered=set().union(*(set(edges[k]) for k in ts)) if ts else set()
            if exact is not None and set(range(n))-covered!=exact:
                continue
            for first in sorted(adj[0]):
                order=[0,first]
                while len(order)<n:
                    nxt=next(iter(adj[order[-1]]-{order[-2]}))
                    need(nxt not in order,'Hamiltonian traversal remains simple')
                    order.append(nxt)
                out.append({'cycle':[names[i] for i in order],
                            'T_pairs':sorted(sorted(names[i] for i in edges[k]) for k in ts),
                            'Q_pairs':sorted(sorted(names[i] for i in edges[k]) for k in qs)})
    need(cycles=={3:1,4:3,5:12}[n],'all undirected Hamiltonian cycles covered')
    return sorted(out,key=lambda x:(x['cycle'],x['T_pairs']))


def neighbors():
    names=('A','B','D','G');roles=(1,0,1,2)
    renamings=[p for p in permutations(range(4)) if all(roles[i]==roles[p[i]] for i in range(4))]
    need(len(renamings)==2,'all24 raw role permutations,only two allowed')
    out=[]
    for u,v in product(range(16),repeat=2):
        if u.bit_count()!=3 or v.bit_count()!=3 or u==v:
            continue
        possibilities=[]
        for p in renamings:
            a=tuple(sorted(names[p[i]] for i in range(4) if u>>i&1))
            b=tuple(sorted(names[p[i]] for i in range(4) if v>>i&1))
            possibilities.append(tuple(sorted((a,b))))
        shared=[names[i] for i in range(4) if (u&v)>>i&1]
        out.append({'U_neighbors':[names[i] for i in range(4) if u>>i&1],
                    'V_neighbors':[names[i] for i in range(4) if v>>i&1],
                    'role_orbit':list(map(list,min(possibilities))),'shared_contacts':shared,
                    'forced_Q':['U',shared[0],'V',shared[1]],
                    'mechanism':'one_T_shared_four' if (u&v)&5 else 'G_double_three_star'})
    out.sort(key=lambda x:(x['U_neighbors'],x['V_neighbors']))
    counts=Counter(tuple(map(tuple,e['role_orbit'])) for e in out)
    return {'all_twelve_entries':out,'four_orbits':[{'pair':list(map(list,k)),'ordered_entries':v} for k,v in sorted(counts.items())]}


def shared():
    out=[]
    for s in edge_stars(('G','X','Z','P','Q'),4,rt=[('G','X'),('G','Z')]):
        q=s['Q_pairs'][0]
        adj={v:set() for v in ('G','X','Z','P','Q')}
        for a,b in s['T_pairs']:
            adj[a].add(b);adj[b].add(a)
        paths=[]
        for order in permutations(adj):
            if order[0]==q[0] and order[-1]==q[1] and all(order[i+1] in adj[order[i]] for i in range(4)):
                paths.append(order)
        need(len(paths)==1,'one complete triangle path from edge-set definition')
        p=paths[0]
        out.append(dict(s,F_T_path=list(p),G_internal_position=p.index('G'),
                        Z_shared_opposite_obstruction='sealed_C3_at_Z' if 'Z' in q else 'H_quota_forces_contact_Q_diagonal'))
    return out


def points(vs):
    return sum(1<<i for i in set(vs))


def edge_bit(a,b):
    return 1<<(15*min(a,b)+max(a,b))


def frame_legal(tris,quads,capacity=(),ignore_diagonal=False):
    ts={points(t) for t in tris}
    if any(t.bit_count()!=3 for t in ts):
        return False
    qs=set()
    for q in quads:
        vs=points(q)
        if vs.bit_count()!=4:
            return False
        es=sum(edge_bit(q[i],q[(i+1)%4]) for i in range(4))
        qs.add((vs,es))
    count=[sum(bool(t>>i&1) for t in ts) for i in range(15)]
    caps=list(TRIANGLES)
    for i,v in capacity:
        caps[i]=v
    if any(count[i]>caps[i] for i in range(15)):
        return False
    adj=[0]*15;face_edges=Counter()
    for t in ts:
        vertices=[i for i in range(15) if t>>i&1]
        for a,b in combinations(vertices,2):
            adj[a]|=1<<b;adj[b]|=1<<a;face_edges[(a,b)]+=1
    for vs,es in qs:
        vertices=[i for i in range(15) if vs>>i&1]
        for a,b in combinations(vertices,2):
            if es&edge_bit(a,b):
                adj[a]|=1<<b;adj[b]|=1<<a;face_edges[(a,b)]+=1
    if any(adj[i].bit_count()>DEGREES[i] for i in range(15)) or any(n>2 for n in face_edges.values()):
        return False
    if not ignore_diagonal:
        for vs,es in qs:
            vertices=[i for i in range(15) if vs>>i&1]
            if any(not es&edge_bit(a,b) and adj[a]>>b&1 for a,b in combinations(vertices,2)):
                return False
    if any((adj[a]&adj[b]).bit_count()>2 for a,b in combinations(range(15),2)):
        return False
    return True


def opposite(h,capacity=(),ignore_diagonal=False):
    surviving=[]
    for j,k in product(range(15),repeat=2):
        if frame_legal([(h,7,j),(h,8,k)],[(8,h,7,2)],capacity,ignore_diagonal):
            surviving.append([LABELS[j],LABELS[k]])
    return {'opposite':LABELS[h],'raw_assignments':225,'surviving_original_assignments':surviving}


def c3_cases():
    out=[]
    for gpos,side in product((1,2,3),(('absent',0),('left',1),('right',16))):
        name,mask=side
        if mask&((1<<(gpos-1))|(1<<(gpos+1))):
            reason='D_G_contact_forbidden_by_G_Q_opposite'
        elif gpos==2 or mask==0:
            reason='ordinary_endpoint_internal_pair_forces_T_at_B'
        else:
            reason='D_four_contacts_F_L_B_V_plus_one_G_endpoint'
        out.append({'G_F_internal_position':gpos,'D_F_endpoint':name,'reason':reason})
    return out


def last_contacts():
    old=(1<<2)|(1<<9)|(1<<6)|(1<<1)
    out=[]
    for v in (7,8):
        full=old|(1<<v)
        out.append({'G_D_side_endpoint':LABELS[v],
                    'D_forced_contacts':sorted(LABELS[i] for i in range(15) if full>>i&1),
                    'distinct_contacts':full.bit_count(),'degree_cap':DEGREES[5]})
    return out


def one_T_F_contacts():
    out=[]
    for h in (4,5):
        entries=[];controls=[]
        for p in range(8,15):
            ts=[(3,7,8),(2,h,7),(2,7,p)]
            tm={points(t) for t in ts}
            count=sum(bool(t&(1<<7)) for t in tm)
            entries.append({'other_F_internal':LABELS[p],'ordinary_endpoint_triangle_count':count,'permitted':frame_legal(ts,[])})
            if frame_legal(ts,[],capacity=[(7,3)]):
                controls.append(LABELS[p])
        out.append({'one_T_F_contact':LABELS[h],'all_seven_other_internal_aliases':entries,'released_endpoint_quota_controls':controls})
    return out


def main():
    root=Path(__file__).resolve().parent;e=json.loads((root/'EXPECTED.json').read_text())
    def compare(got,key):
        need(got==e[key],'every entry in '+key)
    cover=neighbors();compare(cover,'neighbor_cover')
    compare(edge_stars(('U','V','P','Q'),1,zero=('U','V')),'one_T_shared_three_stars')
    single=edge_stars(('U','X','R','S','Z'),2,zero=('U',),qq_exact=('U',))
    double=edge_stars(('U','V','X','R','Z'),2,zero=('U','V'),qq_exact=('U','V'))
    compare(single,'G_all_single_three_stars');compare(double,'G_all_double_three_stars')
    full=edge_stars(('a','b','c','d','e'),4)
    for star in full:
        tdegree=Counter(v for p in star['T_pairs'] for v in p)
        need(sorted(tdegree.values())==[1,1,2,2,2]
             and {v for v,n in tdegree.items() if n==1}==set(star['Q_pairs'][0]),
             'independent F four-T incidence degrees and endpoint roles')
    compare(len(full),'F_four_T_raw_oriented_stars');compare(shared(),'F_G_shared_stars')
    relaxed=edge_stars(('V','Z','P','Q'),1,rq=[('P','Q'),('Z','V')],zero=('V',))
    saturated=[x for x in relaxed if not any('Z' in p for p in x['T_pairs'])]
    compare(relaxed,'shared_opposite_released_internal_H_stars');compare(saturated,'shared_opposite_saturated_internal_H_stars')
    compare(edge_stars(('F','G','H','N'),2,rt=[('F','G')],rq=[('F','H'),('G','H')]),'shared_opposite_sealed_degree4_stars')
    compare(edge_stars(('F','G','H'),1,rt=[('F','G')],rq=[('F','H'),('G','H')]),'shared_opposite_degree3_abstract_control')
    compare(edge_stars(('U','V','P','Q'),1,rq=[('P','Q')],zero=('U','V')),'one_T_opposite_with_two_threes_stars')
    endpoint=edge_stars(('H','R','C','J'),2,rt=[('H','R')],rq=[('H','C')])
    compare(endpoint,'qualified_endpoint_all_links')
    compare([x for x in endpoint if not any('R' in p for p in x['T_pairs'] if p!=['H','R'])],'qualified_endpoint_forced_links')
    compare(opposite(4),'all_ordinary_one_T_opposite_frames');compare(opposite(6),'all_ordinary_zero_T_opposite_frames')
    need(opposite(4,ignore_diagonal=True)==e['controls']['released_Q_diagonal'],'all released diagonal controls')
    need(opposite(4,capacity=[(4,2)])==e['controls']['released_opposite_T_quota'],'all released quota controls')
    compare(c3_cases(),'C3_F_Q_zero_opposite_all_nine_cases');compare(last_contacts(),'C3_last_D_contact_entries')
    compare(one_T_F_contacts(),'C4_one_T_F_contact_original_aliases')
    compare([{'G_position':i,'reason':'both endpoints ordinary,one pair remains ordinary,forces_T_B'} for i in (1,2,3)],'C4_F_Q_B_G_positions')
    def polynomial(c):
        return 1+c-4*c*c
    left,right=polynomial(Fraction(1,2)),polynomial(Fraction(3,5))
    middle=2*polynomial(Fraction(11,20))-(left+right)/2
    compare(list(map(str,(left,middle,right))),'credited_Bernstein_entries')
    deps=json.loads((root/'DEPENDENCIES.json').read_text())['files']
    for n,m in deps.items():
        need(hashlib.sha256((root.parent/n).read_bytes()).hexdigest()==m['sha256'],'public guard '+n)
    old=json.loads((root.parent/'tammes15_two_one_triangle_fours_exclusion/EXPECTED.json').read_text())['catalogue_corollary']['remaining_beta_profiles']
    remaining=[r for r in old if not(r['r']==2 and r['a']==2 and r['b']==1 and r['five_counts_f0_f1_f2']==[1,0,1])]
    need(len(old)==20 and len(remaining)==19 and remaining==e['catalogue_corollary']['remaining_beta_profiles'],'all19 imported rows individually')
    counts=[sum(r['r']==k for r in remaining) for k in (1,2,3)]
    need(counts==[0,8,11]==e['catalogue_corollary']['counts_r1_r2_r3'],'exact19 count split')
    return {'agent':'six-tammes-1','role':'researcher','status':'different same-author exact representation; written geometric bridges unformalized',
            'binary_neighbor_pairs':256,'raw_role_permutations':24,'ordered_neighbor_entries':12,'role_orbits':4,
            'G_single_three_stars':len(single),'G_double_three_stars':len(double),'F_four_T_stars':len(full),
            'F_G_shared_stars_compared':12,'shared_opposite_internal_saturated_stars':len(saturated),
            'released_internal_stars':len(relaxed),'degree3_abstract_controls':2,'opposite_frames_compared':450,
            'C3_zero_opposite_cases':9,'C3_last_D_contacts':2,'C4_one_T_endpoint_aliases':14,
            'credited_Bernstein_entries':3,'public_guarded_files':len(deps),'remaining_profiles_compared_entrywise':len(remaining)}


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
