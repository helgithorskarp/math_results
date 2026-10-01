"""Different same-author binary/edge-set audit; no production-code import.
six-tammes-1, researcher. Geometric and coverage bridges remain written.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

NAMES=('U','V','F','G','A','D','B','C')+tuple('o'+str(i) for i in range(7))
DEGREES=(3,3,5,5,4,4,4,4)+(4,)*7
TCAPS=(0,0,4,4,1,1,0,0)+(2,)*7
IDS={x:i for i,x in enumerate(NAMES)}
DEF_MASK=sum(1<<i for i in (4,5,6,7))


def need(b,m):
    if not b:
        raise ValueError(m)


def vertices(vs):
    return sum(1<<i for i in set(vs))


def ebit(a,b):
    return 1<<(15*min(a,b)+max(a,b))


def edge_stars(names,t,rt=(),rq=(),zero=()):
    n=len(names);edges=list(combinations(range(n),2));ids={v:i for i,v in enumerate(names)}
    index={e:i for i,e in enumerate(edges)}
    def requirements(es):
        return Counter(index[tuple(sorted((ids[a],ids[b])))] for a,b in es)
    tr,qr=requirements(rt),requirements(rq);zero_ids={ids[v] for v in zero if v in ids};out=[];cycles=0
    for chosen in combinations(range(len(edges)),n):
        adj=[set() for _ in names]
        for k in chosen:
            a,b=edges[k];adj[a].add(b);adj[b].add(a)
        if any(len(s)!=2 for s in adj):
            continue
        todo=[0];seen={0}
        while todo:
            a=todo.pop()
            for b in adj[a]-seen:
                seen.add(b);todo.append(b)
        if len(seen)!=n:
            continue
        cycles+=1
        for tt in combinations(chosen,t):
            ts=set(tt);qs=set(chosen)-ts
            if tr-Counter(ts) or qr-Counter(qs):
                continue
            if any(a in edges[k] for a in zero_ids for k in ts):
                continue
            for first in sorted(adj[0]):
                order=[0,first]
                while len(order)<n:
                    nxt=next(iter(adj[order[-1]]-{order[-2]}))
                    need(nxt not in order,'simple Hamiltonian traversal')
                    order.append(nxt)
                out.append({'cycle':[names[i] for i in order],
                            'T_pairs':sorted(sorted(names[i] for i in edges[k]) for k in ts),
                            'Q_pairs':sorted(sorted(names[i] for i in edges[k]) for k in qs)})
    need(cycles=={3:1,4:3,5:12}[n],'all undirected Hamiltonian edge sets')
    return sorted(out,key=lambda x:(x['cycle'],x['T_pairs']))


def neighbors():
    names=('A','B','C','D');roles=(1,0,0,1)
    perms=[p for p in permutations(range(4)) if all(roles[i]==roles[p[i]] for i in range(4))]
    need(len(perms)==4,'all24 raw permutations and four permitted renamings')
    entries=[]
    for u,v in product(range(16),repeat=2):
        if u.bit_count()!=3 or v.bit_count()!=3 or u==v:
            continue
        orbit=[]
        for p in perms:
            a=tuple(sorted(names[p[i]] for i in range(4) if u>>i&1))
            b=tuple(sorted(names[p[i]] for i in range(4) if v>>i&1));orbit.append(tuple(sorted((a,b))))
        entries.append({'U_neighbors':[names[i] for i in range(4) if u>>i&1],
                        'V_neighbors':[names[i] for i in range(4) if v>>i&1],
                        'shared_contacts':[names[i] for i in range(4) if (u&v)>>i&1],
                        'three_contact_counts':{names[i]:int(bool(u>>i&1))+int(bool(v>>i&1)) for i in range(4)},
                        'role_orbit':list(map(list,min(orbit))),
                        'common_Q_forced_by_shared_one_T_four':bool((u&v)&9)})
    entries.sort(key=lambda x:(x['U_neighbors'],x['V_neighbors']))
    c=Counter(tuple(map(tuple,x['role_orbit'])) for x in entries)
    return {'ordered_entries':entries,'three_orbits':[{'pair':list(map(list,k)),'ordered_entries':v} for k,v in sorted(c.items())]}


def shared_stars(other,names):
    out=[]
    for s in edge_stars(names,4,rt=[(other,'X'),(other,'Z')]):
        adj={x:set() for x in names}
        for a,b in s['T_pairs']:
            adj[a].add(b);adj[b].add(a)
        q=s['Q_pairs'][0];paths=[]
        for p in permutations(names):
            if p[0]==q[0] and p[-1]==q[1] and all(p[i+1] in adj[p[i]] for i in range(4)):
                paths.append(p)
        need(len(paths)==1,'one full path from all120 independent orders')
        path=paths[0];inc={v:sum(v in e for e in s['T_pairs']) for v in ('X','Z')}
        out.append(dict(s,T_path=list(path),other_five_position=path.index(other),shared_XZ_T_incidence=inc))
    return out


def shared_cover():
    a=shared_stars('G',('G','X','Z','P','Q'));b=shared_stars('F',('F','X','Z','M','N'));allowed=[]
    for i,j in product(range(len(a)),range(len(b))):
        # Rebuild actual triangle vertex sets for the shared endpoints rather than summing stored counts.
        ft={frozenset(('F',*e)) for e in a[i]['T_pairs']}
        gt={frozenset(('G',*e)) for e in b[j]['T_pairs']}
        counts={x:sum(x in t for t in ft|gt) for x in ('X','Z')}
        if max(counts.values())<=2:
            need(set(counts.values())=={2},'both shared vertices full ordinary fours')
            allowed.append({'F_index':i,'G_index':j,'shared_triangle_counts':counts})
    return {'F_stars':a,'G_stars':b,'raw_pairs':len(a)*len(b),'permitted_pairs':allowed}


def opposite_five_cover():
    # Independent five-bit subset pairs, each expanded through all six orders.
    names=NAMES[10:];subsets=[mask for mask in range(32) if mask.bit_count()==3]
    counts={};hist=Counter()
    for a,b in product(subsets,repeat=2):
        count=2+(a&b).bit_count()
        aa=[names[i] for i in range(5) if a>>i&1];bb=[names[i] for i in range(5) if b>>i&1]
        for ap,bp in product(permutations(aa),permutations(bb)):
            counts[(ap,bp)]=count;hist[count]+=1
    ordered=sorted({a for a,b in counts});matrix=[''.join(str(counts[(a,b)]) for b in ordered) for a in ordered]
    permitted=[[list(a),list(b)] for a in ordered for b in ordered if counts[(a,b)]<=2]
    need(len(counts)==3600 and len(ordered)==60,'all original order pairs from100bit-subset pairs')
    return {'fixed_shared_ordinary_originals':['o0','o1'],'available_other_ordinary_originals':list(names),
            'ordered_internal_triples':list(map(list,ordered)),'raw_original_assignments':3600,
            'common_contact_counts_by_F_G_triples':matrix,'common_contact_histogram':{str(k):v for k,v in sorted(hist.items())},
            'permitted_original_assignments':permitted,'necessary_distinct_ordinary_fours':8,'row_ordinary_fours':7}


def valid(tris,quads,fixed=(),caps=(),skip_links=False,skip_three=False):
    ts={vertices(t) for t in tris}
    if any(t.bit_count()!=3 for t in ts) or any(a==b for a,b in fixed):
        return False
    qs=set()
    for q in quads:
        mask=vertices(q)
        if mask.bit_count()!=4:
            return False
        qs.add((mask,sum(ebit(q[i],q[(i+1)%4]) for i in range(4))))
    cap=list(TCAPS)
    for i,n in caps:
        cap[i]=n
    if any(sum(bool(t>>i&1) for t in ts)>cap[i] for i in range(15)):
        return False
    adj=[0]*15;inc=Counter();corner=[[] for _ in range(15)]
    for t in ts:
        vs=[i for i in range(15) if t>>i&1]
        for a,b in combinations(vs,2):
            adj[a]|=1<<b;adj[b]|=1<<a;inc[(a,b)]+=1
        for i in vs:
            a,b=[v for v in vs if v!=i];corner[i].append((a,b))
    for mask,edges in qs:
        vs=[i for i in range(15) if mask>>i&1];local={i:[] for i in vs}
        for a,b in combinations(vs,2):
            if edges&ebit(a,b):
                adj[a]|=1<<b;adj[b]|=1<<a;inc[(a,b)]+=1;local[a].append(b);local[b].append(a)
        for i in vs:
            need(len(local[i])==2,'quadrilateral corner determined by its edge bits')
            corner[i].append(tuple(local[i]))
    for a,b in fixed:
        adj[a]|=1<<b;adj[b]|=1<<a
    if any(adj[i].bit_count()>DEGREES[i] for i in range(15)) or any(n>2 for n in inc.values()):
        return False
    if not skip_three and any(adj[i]&~DEF_MASK for i in (0,1)):
        return False
    for mask,edges in qs:
        vs=[i for i in range(15) if mask>>i&1]
        if any(not edges&ebit(a,b) and adj[a]>>b&1 for a,b in combinations(vs,2)):
            return False
    if any((adj[a]&adj[b]).bit_count()>2 for a,b in combinations(range(15),2)):
        return False
    if not skip_links:
        # Union/find components and multigraph degrees independently detect proper closed link cycles.
        for i in range(15):
            parent=list(range(15));degree=[0]*15
            def root(v):
                while parent[v]!=v:
                    parent[v]=parent[parent[v]];v=parent[v]
                return v
            for a,b in corner[i]:
                degree[a]+=1;degree[b]+=1;parent[root(a)]=root(b)
            if any(n>2 for n in degree):
                return False
            components={}
            for v in range(15):
                if degree[v]:
                    components.setdefault(root(v),[]).append(v)
            if any(len(vs)<DEGREES[i] and all(degree[v]==2 for v in vs) for vs in components.values()):
                return False
    return True


def ints(tris,quads,fixed=()):
    return ([tuple(IDS[v] for v in t) for t in tris],
            [tuple(IDS[v] for v in q) for q in quads],
            [tuple(IDS[v] for v in e) for e in fixed])


def prefix(h,y,m=11):
    # F=2,G=3,X=8,Z=9,L=10,M=11. No production constants or code are imported.
    return [(2,3,8),(2,3,9),(2,9,10),(2,10,y),(3,8,m)],[(2,8,h,y)]


def noncontact(last_Q=True):
    out=[]
    for y,j in product(range(15),range(8,15)):
        if y<8:
            continue
        ts=[(2,4,10),(2,10,9),(3,y,j)];qs=[(2,8,5,4)]+([(3,y,4,5)] if last_Q else [])
        if valid(ts,qs,fixed=[(4,0),(5,1)]):
            out.append([NAMES[y],NAMES[j]])
    return {'raw_end_and_internal_aliases':105,'permitted_entries':out}


def internal_aliases():
    out=[]
    for y in (5,12):
        for m in (10,y):
            ts,qs=prefix(4,y,m)
            out.append({'Y_role':NAMES[y],'M_original_alias':NAMES[m],'permitted':valid(ts,qs)})
    return out


def cross_aliases():
    out=[]
    for a,b in ((10,11),(10,13),(12,11),(12,13)):
        fm=vertices((8,3,9,10,12))
        gm=vertices(tuple(a if i==b else i for i in (9,2,8,11,13)))
        common=fm&gm
        need(common.bit_count()==3,'binary third-common-contact obstruction')
        out.append({'identified_originals':[NAMES[a],NAMES[b]],
                    'F_G_common_contacts':sorted(NAMES[i] for i in range(15) if common>>i&1),'permitted':False})
    return out


def one_T():
    out=[]
    for h,y in ((4,5),(4,12),(5,4),(5,12)):
        ts,qs=prefix(h,y);before=[];alive=[]
        for k in range(15):
            if not valid(ts,qs+[(8,11,k,h)],fixed=[(h,1)]):
                continue
            before.append(NAMES[k]);neighbors=tuple(sorted(NAMES[i] for i in {8,y,k,1}))
            if edge_stars(neighbors,1,rq=[('o0',NAMES[y]),('o0',NAMES[k])],zero=('U','V')):
                alive.append(NAMES[k])
        out.append({'H':NAMES[h],'Y':NAMES[y],'raw_K_aliases':15,'necessary_prefix_entries':before,'permitted_K_entries':alive})
    return out


def ordinary_end():
    out=[]
    for h in (6,7):
        ts,qs=prefix(h,12)
        alive=[NAMES[j] for j in range(15) if valid(ts+[(12,h,j)],qs,fixed=[(h,1)])]
        out.append({'H':NAMES[h],'raw_forced_T_original_aliases':15,'permitted_entries':alive})
    return out


def zero_T(skip_three=False):
    out=[]
    for h,y,assoc in product((6,7),(4,5),(0,1)):
        ts,qs=prefix(h,y);before=[];masks=[];fixed=[(h,1),(y,assoc)]
        for k in range(15):
            qq=qs+[(8,11,k,h)]
            if valid(ts,qq,fixed=fixed,skip_three=skip_three):
                before.append(NAMES[k])
            mask=sum(1<<o for o in range(15) if valid(ts,qq+[(h,y,o,1)],fixed=fixed,skip_three=skip_three))
            masks.append(mask)
        out.append({'H':NAMES[h],'Y':NAMES[y],'Y_three_contact':NAMES[assoc],'raw_KO_aliases':225,
                    'necessary_prefix_K_entries':before,'permitted_O_bitmasks_by_original_K':masks})
    return out


def main():
    folder=Path(__file__).resolve().parent;e=json.loads((folder/'EXPECTED.json').read_text())
    def compare(value,key):
        need(value==e[key],'every permitted entry in '+key)
    compare(neighbors(),'neighbor_cover');compare(shared_cover(),'shared_five_pair_cover')
    compare(opposite_five_cover(),'opposite_five_all_original_alias_cover')
    compare(edge_stars(('F','G','M','H'),2,rt=[('F','G'),('G','M')],rq=[('F','H')]),'ordinary_X_forced_last_Q_links')
    compare(edge_stars(('X','Y','K','V'),1,rq=[('X','Y'),('X','K')],zero=('V',)),'one_T_opposite_H_links')
    compare(edge_stars(('X','Y','K','V'),0,rq=[('X','Y'),('X','K')]),'zero_T_opposite_H_links')
    compare(edge_stars(('X','Y','P','V'),0,rq=[('X','Y'),('X','Y')]),'duplicate_K_equals_Y_known_corner_links')
    end=edge_stars(('F','L','H','J'),2,rt=[('F','L')],rq=[('F','H')]);compare(end,'qualified_endpoint_all_links')
    compare([s for s in end if not any('L' in p for p in s['T_pairs'] if p!=['F','L'])],'qualified_endpoint_forced_links')
    compare(noncontact(),'noncontact_all_original_end_frames')
    compare(edge_stars(('F','L','D','U'),1,rt=[('F','L')],rq=[('F','D'),('L','D')],zero=('U',)),'noncontact_forced_alias_sealed_A_links')
    compare(internal_aliases(),'other_G_internal_original_alias_controls');compare(one_T(),'one_T_opposite_all_K_frames')
    compare(cross_aliases(),'nonshared_fan_cross_original_aliases')
    compare(ordinary_end(),'zero_T_opposite_ordinary_Y_forced_T_frames');compare(zero_T(),'zero_T_opposite_all_KO_frames')
    c=e['controls']
    need(edge_stars(('X','Y','K','V'),1,rq=[('X','Y'),('X','K')])==c['H_one_T_released_three_quota_links'],'all released-three links')
    need(edge_stars(('X','Y','P','V'),0,rq=[('X','Y')])==c['released_duplicate_corner_links'],'all released duplicate-corner links')
    need(noncontact(False)==c['noncontact_before_final_Q'],'all pre-final-Q controls')
    need(zero_T(True)==c['zero_KO_released_three_neighbor_restriction'],'all released three-neighbor matrices')
    def p(x):
        return 1+x-4*x*x
    left,right=p(Fraction(1,2)),p(Fraction(3,5));middle=2*p(Fraction(11,20))-(left+right)/2
    compare(list(map(str,(left,middle,right))),'credited_Bernstein_entries')
    dep=json.loads((folder/'DEPENDENCIES.json').read_text())['files']
    for path,m in dep.items():
        need(hashlib.sha256((folder.parent/path).read_bytes()).hexdigest()==m['sha256'],'public guard '+path)
    old=json.loads((folder.parent/'tammes15_four_two_triangle_fives_exclusion/EXPECTED.json').read_text())['catalogue_corollary']['remaining_beta_profiles']
    left=[r for r in old if not(r['r']==2 and r['a']==2 and r['b']==2 and r['five_counts_f0_f1_f2']==[2,0,0])]
    need(len(old)==19 and len(left)==18 and left==e['catalogue_corollary']['remaining_beta_profiles'],'all18 imported rows compared entrywise')
    need([sum(r['r']==i for r in left) for i in (1,2,3)]==[0,7,11]==e['catalogue_corollary']['counts_r1_r2_r3'],'exact18 split')
    return {'agent':'six-tammes-1','role':'researcher','status':'different same-author exact audit; geometric/contact bridges unformalized; mathematical review pending',
            'binary_neighbor_pairs':256,'raw_role_permutations':24,'ordered_neighbor_entries':12,'role_orbits':3,
            'shared_four_T_stars_each':12,'raw_shared_star_pairs':144,'permitted_shared_star_pairs':32,
            'opposite_five_original_alias_assignments':3600,'opposite_five_bit_subset_pairs':100,
            'noncontact_original_frames':105,'one_T_opposite_K_original_frames':60,'zero_T_ordinary_endpoint_T_frames':30,
            'zero_T_opposite_KO_original_frames':1800,'other_internal_alias_controls':4,
            'nonshared_fan_cross_alias_entries':4,
            'pre_final_Q_permitted_controls':30,'released_three_neighbor_terminal_controls':20,
            'credited_Bernstein_entries':3,'guarded_public_files':len(dep),'remaining_profiles_compared_entrywise':len(left)}


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
