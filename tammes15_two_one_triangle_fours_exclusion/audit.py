"""Separate finite representation: binary original incidences and edge sets.
No production-code import. Same author, not independent mathematical review.
"""
from itertools import combinations, permutations, product
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib
import json

LABELS = ('U','V','F','G','A','D','B')+tuple('o'+str(i) for i in range(8))
DEGREES = (3,3,5,5,4,4,4)+(4,)*8
TRIANGLES = (0,0,3,3,1,1,0)+(2,)*8
ORD_MASK = sum(1 << i for i in range(7,15))
PLUS_G = ORD_MASK | 8


def need(b,m):
    if not b:
        raise ValueError(m)


def undirected_stars(names,t,rt=(),rq=(),qq=()):
    n=len(names)
    all_edges=list(combinations(range(n),2))
    index={v:i for i,v in enumerate(names)}
    required_t={all_edges.index(tuple(sorted((index[a],index[b])))) for a,b in rt}
    required_q={all_edges.index(tuple(sorted((index[a],index[b])))) for a,b in rq}
    out=[]
    cycle_count=0
    for chosen in combinations(range(len(all_edges)),n):
        adj=[set() for _ in range(n)]
        for k in chosen:
            a,b=all_edges[k];adj[a].add(b);adj[b].add(a)
        if any(len(a)!=2 for a in adj):
            continue
        seen={0};stack=[0]
        while stack:
            v=stack.pop()
            for w in adj[v]-seen:
                seen.add(w);stack.append(w)
        if len(seen)!=n:
            continue
        cycle_count+=1
        for selected_t in combinations(chosen,t):
            ts=set(selected_t);qs=set(chosen)-ts
            if not required_t<=ts or not required_q<=qs:
                continue
            if any(index[v] in all_edges[k] for v in qq for k in ts):
                continue
            for first in sorted(adj[0]):
                order=[0,first]
                while len(order)<n:
                    w=next(iter(adj[order[-1]]-{order[-2]}))
                    need(w not in order,'simple undirected-cycle traversal')
                    order.append(w)
                out.append({'cycle':[names[i] for i in order],
                    'T_pairs':sorted(sorted(names[i] for i in all_edges[k]) for k in ts),
                    'Q_pairs':sorted(sorted(names[i] for i in all_edges[k]) for k in qs)})
    need(cycle_count=={4:3,5:12}[n],'every undirected Hamiltonian cycle')
    return sorted(out,key=lambda x:(x['cycle'],x['T_pairs']))


def neighbor_entries():
    names=('A','B','D','F','G')
    role=(1,0,1,3,3)
    maps=[p for p in permutations(range(5)) if all(role[i]==role[p[i]] for i in range(5))]
    need(len(maps)==4,'all120 raw permutations screened for equal original roles')
    entries=[]
    for u,v in product(range(32),repeat=2):
        if u.bit_count()!=3 or v.bit_count()!=3 or u==v:
            continue
        if any(bool(u&(1<<i))+bool(v&(1<<i))>1 for i in (3,4)):
            continue
        orbit=[]
        for p in maps:
            a=tuple(sorted(names[p[i]] for i in range(5) if u>>i&1))
            b=tuple(sorted(names[p[i]] for i in range(5) if v>>i&1))
            orbit.append(tuple(sorted((a,b))))
        shared=u&v
        bad=[names[i] for i in (0,2) if shared==(1<<i)]
        entries.append({'ordered_triples':[[names[i] for i in range(5) if x>>i&1] for x in (u,v)],
                        'role_orbit':list(map(list,min(orbit))),
                        'shared_one_T_without_other_common_contact':bad})
    return sorted(entries,key=lambda e:e['ordered_triples'])


def fan_entries(case):
    out=[]
    masks=(1,2,4,8,0)
    for dpos,d in enumerate(masks):
        for gpos,g in enumerate(masks):
            if d&g:
                continue
            if d&6:
                reason='one_T_D_cannot_be_internal'
            elif case in ('C1','C7') and d&1:
                reason='D_B_contact_forbidden_by_three_star'
            elif case=='C1' and d&8:
                reason='D_A_contact_forbidden_by_three_star'
            elif case=='C5' and d&8:
                reason='A_side_endpoint_has_two_Ts'
            elif g&9:
                reason='adjacent_fives_in_Q'
            elif case=='C5' and not g:
                reason='single_D_cannot_cover_both_distinct_zero_B_endpoints'
            elif case=='C5' and g&4:
                reason='G_third_T_overloads_full_R_or_Z'
            elif not g&2:
                reason='ordinary_zero_B_endpoint_pair'
            elif case=='C5' and d&1:
                reason='G_third_T_overloads_one_T_X_equals_D'
            else:
                reason='RETAINED_G_R_D_'+('Z' if d&8 else 'outside')
            out.append({'D_position':dpos,'G_position':gpos,'reason':reason})
    return out


def point_mask(vs):
    return sum(1<<i for i in set(vs))


def edge_bit(a,b):
    return 1<<(15*min(a,b)+max(a,b))


def legal(tris,quads,extra):
    """Binary necessary constraints, with original-face deduplication."""
    tset={point_mask(t) for t in tris}
    if any(t.bit_count()!=3 for t in tset):
        return False
    qset=set()
    for q in quads:
        vs=point_mask(q)
        if vs.bit_count()!=4:
            return False
        es=sum(edge_bit(q[i],q[(i+1)%4]) for i in range(4))
        qset.add((vs,es))
    adjacency=[0]*15
    face_edges=Counter()
    triangle_count=[0]*15
    for t in tset:
        points=[i for i in range(15) if t>>i&1]
        for i in points:
            triangle_count[i]+=1
        for a,b in combinations(points,2):
            adjacency[a]|=1<<b;adjacency[b]|=1<<a;face_edges[(a,b)]+=1
    for vs,es in qset:
        points=[i for i in range(15) if vs>>i&1]
        for a,b in combinations(points,2):
            if es&edge_bit(a,b):
                adjacency[a]|=1<<b;adjacency[b]|=1<<a;face_edges[(a,b)]+=1
    for a,b in extra:
        if a==b:
            return False
        adjacency[a]|=1<<b;adjacency[b]|=1<<a
    if any(adjacency[i].bit_count()>DEGREES[i] or triangle_count[i]>TRIANGLES[i] for i in range(15)):
        return False
    if any(x>2 for x in face_edges.values()):
        return False
    for vs,es in qset:
        vertices=[i for i in range(15) if vs>>i&1]
        if any(not es&edge_bit(a,b) and adjacency[a]>>b&1 for a,b in combinations(vertices,2)):
            return False
    if any((adjacency[a]&adjacency[b]).bit_count()>2 for a,b in combinations(range(15),2)):
        return False
    return True


def pack(values):
    return sum(v<<(4*(len(values)-i-1)) for i,v in enumerate(values))


def c1_frames(ys):
    accepted=[];terminal=[];raw=0
    for code in range(16**4):
        j,k,l,n=[code>>shift&15 for shift in (12,8,4,0)]
        if not (ORD_MASK>>j&1 and PLUS_G>>k&1 and PLUS_G>>l&1 and ORD_MASK>>n&1):
            continue
        ts=[(3,7,2),(3,8,2),(9,2,8),(j,4,9),(k,j,5),(n,3,7)]
        qs=[(2,1,6,7),(4,1,2,9),(4,0,6,1),(j,4,0,5),(5,0,6,l)]
        for y in ys:
            raw+=1
            if y in (2,7,8,n):
                continue
            if not legal(ts,qs,[(0,4),(0,6),(0,5),(1,4),(1,6),(1,2),(3,y)]):
                continue
            record=pack((j,k,l,n,y))
            if l==k:
                tmasks={point_mask(t) for t in ts}
                incident=[t for t in tmasks if t>>j&1]
                need(len(incident)==2 and k>=7,'terminal internal ordinary J is full')
                current=point_mask((j,5,k))
                others=[t for t in incident if t!=current]
                need(len(others)==1 and not others[0]>>k&1,'the other J triangle excludes endpoint K')
                terminal.append(record)
            else:
                accepted.append(record)
    return {'raw_assignments':raw,'slot_order':['J','K','L','N','Y'],
            'K_equals_L_prefixes_excluded_by_terminal_endpoint_rule':sorted(terminal),
            'accepted_encoded_original_assignments':sorted(accepted)}


def c7_frames():
    good=[]
    for code in range(16**3):
        j,l,m=[code>>shift&15 for shift in (8,4,0)]
        if any(not ORD_MASK>>i&1 for i in (j,l,m)):
            continue
        ts=[(3,7,2),(3,8,2),(9,2,8),(10,3,7),(j,4,9),(m,5,j)]
        for e in (3,6):
            qs=[(2,0,6,7),(4,0,2,9),(3,1,6,10),(5,1,3,8),(l,4,0,6),(j,5,8,9),(m,5,1,e)]
            if legal(ts,qs,[(0,4),(0,6),(0,2),(1,6),(1,5),(1,3)]):
                good.append(pack((j,l,m,e)))
    return {'raw_assignments':1024,'slot_order':['J','L','M','E'],'accepted_encoded_original_assignments':sorted(good)}


def c5_quad_frames():
    good=[]
    for w,k in product(range(7,15),(2,3)):
        ts=[(3,7,2),(3,8,2),(9,2,8),(w,3,7),(w,4,9)]
        qs=[(2,0,6,7),(4,0,2,9),(3,1,6,8),(4,1,3,w),(4,0,6,1),(k,7,6,8)]
        if legal(ts,qs,[]):
            good.append(pack((w,k)))
    return {'raw_assignments':16,'slot_order':['W','last_Q_opposite'],'accepted_encoded_original_assignments':good}


def c2_stars():
    out=[]
    for s in undirected_stars(('F','X','S','Z','H'),3,rt=[('F','X'),('F','S'),('Z','H')]):
        sector_sets=[set(p) for p in s['Q_pairs']]
        if {'S','Z'} in sector_sets:
            reason,domain='S_Z_contact_Q_diagonal',None
        else:
            need({'H','S'} in sector_sets,'remaining sector requires S/H quadrilateral')
            # Intersection of H's full neighbor mask U,V,Z,G with the
            # ordinary-S non-three contact domain, excluding the center G.
            full_h={'U','V','Z','G'}
            domain=sorted(full_h-{'U','V','G'})
            reason='forced_Z_creates_G_Z_contact_Q_diagonal'
        out.append(dict(s,reason=reason,opposite_domain=domain))
    return out


def c8_record():
    ts=[(2,7,8),(2,8,9),(2,9,10),(3,11,12),(3,12,13),(3,13,14),(4,7,11),(5,10,14)]
    qs=[(0,2,7,4),(0,5,10,2),(1,3,11,4),(1,5,14,3),(0,4,1,5)]
    tmask={point_mask(t) for t in ts}
    counts=[sum(bool(t>>v&1) for t in tmask) for v in range(15)]
    adj=[0]*15
    for f in ts+qs:
        for i in range(len(f)):
            a,b=f[i],f[(i+1)%len(f)];adj[a]|=1<<b;adj[b]|=1<<a
    candidates=sorted(LABELS[v] for v in range(15) if v!=6 and adj[v].bit_count()<DEGREES[v])
    entries=[]
    rr=undirected_stars(('F','X','S','B'),2,rt=[('F','X'),('F','S')])
    ss=undirected_stars(('F','R','Z','B'),2,rt=[('F','R'),('F','Z')])
    for r,s in product(rr,ss):
        def other(c,p):
            es={frozenset((c[i],c[(i+1)%4])) for i in range(4)}
            return next(x for x in set().union(*[e for e in es if p in e])-{p,'F'})
        b1=other(r['cycle'],'S');b2=other(s['cycle'],'R')
        need(b1==b2=='B','both original face positions coincide at B')
        entries.append({'R_cycle':r['cycle'],'S_cycle':s['cycle'],'forced_Q':['R','S',b2,b1],'simple':False})
    controls=undirected_stars(('F','R','Z','Bp'),2,rt=[('F','R'),('F','Z')])
    need(len(rr)*len(controls)==4 and len({'R','S','B','Bp'})==4,'four simple fourth-neighbor controls')
    return {'all_15_original_triangle_counts':dict(zip(LABELS,counts)),
            'only_B_contact_candidates':candidates,'last_Q_all_four_entries':entries,
            'relaxing_one_fourth_neighbor_to_Bp_gives_four_simple_local_Qs':4}


def main():
    root=Path(__file__).resolve().parent
    expected=json.loads((root/'EXPECTED.json').read_text())
    need(list(LABELS)==expected['original_encoding'],'fixed fifteen-original encoding')
    entries=neighbor_entries()
    need(entries==expected['neighbor_cover']['all_36_entries'],'all36 original neighbor pairs entrywise')
    orbits=sorted({tuple(map(tuple,x['role_orbit'])) for x in entries})
    need(list(map(lambda x:list(map(list,x)),orbits))==expected['neighbor_cover']['eight_full_interval_orbits'],'all8 full-interval role orbits')
    beta=[x for x in entries if all(not {'F','G'}<=set(t) for t in x['ordered_triples'])]
    need(len(beta)==30 and len({tuple(map(tuple,x['role_orbit'])) for x in beta})==6,'beta30/6 cover kept within beta')
    one=undirected_stars(('U','V','P','Q'),1,qq=('U','V'))
    need(one==expected['one_T_four_two_three_contact_stars'],'all one-T-four stars')
    relax=[x for x in undirected_stars(('U','V','P','Q'),0) if ['U','V'] not in x['Q_pairs']]
    need(relax==expected['controls']['zero_T_four_nonadjacent_threes'],'nonempty zero-T-four control')
    endpoint=undirected_stars(('H','R','C','J'),2,rt=[('H','R')],rq=[('H','C')])
    saturated=[x for x in endpoint if not any('R' in p for p in x['T_pairs'] if p!=['H','R'])]
    need(endpoint==expected['ordinary_endpoint_all_links'] and saturated==expected['ordinary_endpoint_saturated_links'],'qualified endpoint links entrywise')
    extension=undirected_stars(('F','P','Q','N','V'),3,rt=[('F','P'),('F','Q')],qq=('V',))
    need(extension==expected['three_T_five_all_third_extensions'],'all third-five-triangle extensions')
    contiguous=undirected_stars(('F','X','S','N','Y'),3,rt=[('F','X'),('F','S'),('X','N')])
    need(contiguous==expected['C1_contiguous_known_G_stars'],'fifth G neighbor necessarily Q-Q')
    for k in ('C1','C5','C7'):
        need(fan_entries(k)==expected['fan_placement_entries'][k],'all21 original fan placements '+k)
    need(c2_stars()==expected['C2_and_C1_G_alias_three_T_star_obstructions'],'all4 oriented three-T G aliases')
    c1=c1_frames((4,5,6));c1control=c1_frames(range(7,15));c7=c7_frames();c5=c5_quad_frames()
    for got,key in [(c1,'C1_all_original_alias_frames'),(c7,'C7_all_original_alias_frames'),(c5,'C5_last_Q_frames')]:
        need(got==expected[key],'every permitted original alias frame and terminal prefix '+key)
    need(c1control==expected['controls']['ordinary_QQ_neighbor_C1_relaxed_frames'],'all nonempty relaxed C1 original assignments')
    need(c8_record()==expected['C8_original_budget_and_nonsimple_Q'],'all15 original quotas,only B slots and all4 nonsimple Q entries')
    lo,width=Fraction(1,2),Fraction(1,10)
    a,b,c=1+lo-4*lo*lo,width*(1-8*lo),-4*width*width
    need(list(map(str,(a,a+b/2,a+b+c)))==expected['credited_Bernstein_margin'],'credited Bernstein coefficients rebuilt')
    deps=json.loads((root/'DEPENDENCIES.json').read_text())['files']
    for n,m in deps.items():
        need(hashlib.sha256((root.parent/n).read_bytes()).hexdigest()==m['sha256'],'public dependency '+n)
    old=json.loads((root.parent/'tammes15_one_triangle_four_exclusion/EXPECTED.json').read_text())['catalogue_corollary']['remaining_beta_profiles']
    remaining=[r for r in old if not(r['r']==2 and r['a']==2 and r['b']==1 and r['five_counts_f0_f1_f2']==[0,2,0])]
    need(len(old)==21 and len(remaining)==20 and remaining==expected['catalogue_corollary']['remaining_beta_profiles'],'every20 imported profile entry')
    return {'agent':'six-tammes-1','role':'researcher','status':'separate same-author exact finite representation; geometric bridges unformalized',
            'binary_neighbor_mask_pairs':1024,'raw_role_permutations':120,'full_neighbor_entries':len(entries),'full_role_orbits':len(orbits),
            'beta_neighbor_entries':len(beta),'beta_role_orbits':6,'fan_entries_per_case':21,
            'one_T_four_stars':len(one),'three_T_five_third_extensions':len(extension),'three_T_G_alias_stars':4,
            'C1_raw_original_alias_frames':c1['raw_assignments'],'C1_terminal_same_opposite_prefixes':len(c1['K_equals_L_prefixes_excluded_by_terminal_endpoint_rule']),
            'C1_survivors':len(c1['accepted_encoded_original_assignments']),'C7_raw_original_alias_frames':c7['raw_assignments'],
            'C7_survivors':len(c7['accepted_encoded_original_assignments']),'C5_last_Q_frames':16,'C5_survivors':len(c5['accepted_encoded_original_assignments']),
            'C1_relaxed_ordinary_QQ_frames':len(c1control['accepted_encoded_original_assignments']),
            'C8_original_quota_entries':15,'C8_nonsimple_Q_entries':4,'credited_Bernstein_entries':3,
            'guarded_public_files':len(deps),'remaining_profiles_compared_entrywise':len(remaining)}


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
