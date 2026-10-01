"""Exact local support for the two-ordinary-fives hand proof.
six-tammes-1, researcher. No complete contact-map or packing census.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

POINTS=('U','V','F','G','A','D','B','C')+tuple('o'+str(i) for i in range(7))
ORD=POINTS[8:]
DEG=dict(zip(POINTS,(3,3,5,5,4,4,4,4)+(4,)*7))
CAP=dict(zip(POINTS,(0,0,4,4,1,1,0,0)+(2,)*7))
DEF={'A','D','B','C'}


def need(b,m):
    if not b:
        raise ValueError(m)


def edge(a,b):
    return tuple(sorted((a,b)))


def qcanon(q):
    return min(x[i:]+x[:i] for x in (q,q[::-1]) for i in range(4))


def stars(names,t,rt=(),rq=(),zero=()):
    out=[]
    for p in permutations(names[1:]):
        cycle=names[:1]+p
        es=[edge(cycle[i],cycle[(i+1)%len(cycle)]) for i in range(len(cycle))]
        for slots in combinations(range(len(cycle)),t):
            ts=[es[i] for i in slots];qs=[es[i] for i in range(len(cycle)) if i not in slots]
            if Counter(rt)-Counter(ts) or Counter(rq)-Counter(qs):
                continue
            if any(v in e for v in zero for e in ts):
                continue
            out.append({'cycle':list(cycle),'T_pairs':sorted(map(list,ts)),'Q_pairs':sorted(map(list,qs))})
    return sorted(out,key=lambda x:(x['cycle'],x['T_pairs']))


def neighbor_cover():
    names=sorted(DEF);roles={'A':1,'D':1,'B':0,'C':0}
    relabel=[dict(zip(names,p)) for p in permutations(names) if all(roles[x]==roles[y] for x,y in zip(names,p))]
    need(len(relabel)==4,'all equal-role relabelings from24 raw permutations')
    entries=[]
    for u,v in product(combinations(names,3),repeat=2):
        if u==v:
            continue
        orbit=min(tuple(sorted(tuple(sorted(r[x] for x in t)) for t in (u,v))) for r in relabel)
        counts={x:int(x in u)+int(x in v) for x in names}
        need(all(counts.values()) and len(set(u)&set(v))==2,'every deficient four meets a three')
        entries.append({'U_neighbors':list(u),'V_neighbors':list(v),'shared_contacts':sorted(set(u)&set(v)),
                        'three_contact_counts':counts,'role_orbit':list(map(list,orbit)),
                        'common_Q_forced_by_shared_one_T_four':bool(set(u)&set(v)&{'A','D'})})
    counts=Counter(tuple(map(tuple,e['role_orbit'])) for e in entries)
    need(len(entries)==12 and len(counts)==3 and sorted(counts.values())==[2,2,8],'full12/3 cover')
    return {'ordered_entries':entries,'three_orbits':[{'pair':list(map(list,k)),'ordered_entries':v} for k,v in sorted(counts.items())]}


def shared_stars(other,names):
    out=[]
    for s in stars(names,4,rt=[edge(other,'X'),edge(other,'Z')]):
        q=s['Q_pairs'][0];tes={tuple(x) for x in s['T_pairs']};path=[q[0]]
        while len(path)<5:
            ns=[b if a==path[-1] else a for a,b in tes if path[-1] in (a,b)]
            ns=[v for v in ns if len(path)==1 or v!=path[-2]]
            need(len(ns)==1 and ns[0] not in path,'one full four-T neighbor path')
            path.append(ns[0])
        inc=Counter(v for e in s['T_pairs'] for v in e)
        out.append(dict(s,T_path=path,other_five_position=path.index(other),
                        shared_XZ_T_incidence={v:inc[v] for v in ('X','Z')}))
    need(len(out)==12,'all12 oriented shared stars')
    return out


def shared_pair_cover():
    fs=shared_stars('G',('G','X','Z','P','Q'))
    gs=shared_stars('F',('F','X','Z','M','N'));pairs=[]
    for i,j in product(range(12),repeat=2):
        a,b=fs[i],gs[j]
        counts={v:a['shared_XZ_T_incidence'][v]+b['shared_XZ_T_incidence'][v]-1 for v in ('X','Z')}
        if max(counts.values())<=2:
            need(set(counts.values())=={2},'both shared originals ordinary and full')
            ae=set(a['Q_pairs'][0])&{'X','Z'};be=set(b['Q_pairs'][0])&{'X','Z'}
            need(len(ae)==len(be)==1 and ae!=be,'opposed near-end assignments')
            need(a['other_five_position'] in (1,3) and b['other_five_position'] in (1,3),'no middle-five position')
            pairs.append({'F_index':i,'G_index':j,'shared_triangle_counts':counts})
    need(len(pairs)==32,'all144raw/32necessary shared charts')
    return {'F_stars':fs,'G_stars':gs,'raw_pairs':144,'permitted_pairs':pairs}


def opposite_five_alias_cover():
    # Shared Q endpoints are ordinary o0,o1; each fan has three other ordinary internals.
    triples=list(permutations(ORD[2:],3));matrix=[];hist=Counter();permitted=[]
    for a in triples:
        row=''
        for b in triples:
            common={'o0','o1'}|(set(a)&set(b));n=len(common)
            row+=str(n);hist[n]+=1
            if n<=2:
                permitted.append([list(a),list(b)])
        matrix.append(row)
    need(len(triples)==60 and not permitted and hist=={3:1080,4:2160,5:360},'complete3600opposite-five actual alias cover')
    return {'fixed_shared_ordinary_originals':['o0','o1'],'available_other_ordinary_originals':list(ORD[2:]),
            'ordered_internal_triples':list(map(list,triples)),'raw_original_assignments':3600,
            'common_contact_counts_by_F_G_triples':matrix,'common_contact_histogram':{str(k):v for k,v in sorted(hist.items())},
            'permitted_original_assignments':permitted,'necessary_distinct_ordinary_fours':8,'row_ordinary_fours':7}


def legal(tris,quads,fixed=(),capacity=None,ignore_links=False,ignore_three_contacts=False):
    if any(len(set(f))!=len(f) for f in tris+quads) or any(a==b for a,b in fixed):
        return False
    ts={tuple(sorted(t)) for t in tris};qs={qcanon(q) for q in quads}
    caps=CAP if capacity is None else dict(CAP,**capacity)
    ntri=Counter(v for t in ts for v in t)
    if any(ntri[v]>caps[v] for v in POINTS):
        return False
    adj={v:set() for v in POINTS};ecount=Counter();corners={v:[] for v in POINTS}
    for f in ts|qs:
        for i,v in enumerate(f):
            w=f[(i+1)%len(f)];adj[v].add(w);adj[w].add(v);ecount[edge(v,w)]+=1
            corners[v].append(edge(f[i-1],w))
    for a,b in fixed:
        adj[a].add(b);adj[b].add(a)
    if any(len(adj[v])>DEG[v] for v in POINTS) or any(n>2 for n in ecount.values()):
        return False
    if not ignore_three_contacts and any(adj[v]-DEF for v in ('U','V')):
        return False
    if any(q[2] in adj[q[0]] or q[3] in adj[q[1]] for q in qs):
        return False
    if any(len(adj[a]&adj[b])>2 for a,b in combinations(POINTS,2)):
        return False
    if not ignore_links:
        for v in POINTS:
            graph={u:[] for u in adj[v]}
            for a,b in corners[v]:
                graph[a].append(b);graph[b].append(a)
            if any(len(ns)>2 for ns in graph.values()):
                return False
            seen=set()
            for root in graph:
                if root in seen:
                    continue
                component={root};todo=[root]
                while todo:
                    u=todo.pop()
                    for w in graph[u]:
                        if w not in component:
                            component.add(w);todo.append(w)
                seen|=component
                if all(len(graph[u])==2 for u in component) and len(component)<DEG[v]:
                    return False
    return True


def full_F_prefix(h,y,m='o3'):
    # X=o0,Z=o1,L=o2. M may initially alias L or Y; separate prefix controls check both.
    return [('F','G','o0'),('F','G','o1'),('F','o1','o2'),('F','o2',y),('G','o0',m)], [('F','o0',h,y)]


def noncontact_frames(last_Q=True):
    alive=[]
    for y,j in product(POINTS,ORD):
        if y not in ORD:
            continue
        ts=[('F','A','o2'),('F','o2','o1'),('G',y,j)]
        qs=[('F','o0','D','A')]+([('G',y,'A','D')] if last_Q else [])
        if legal(ts,qs,fixed=[('A','U'),('D','V')]):
            alive.append([y,j])
    return {'raw_end_and_internal_aliases':105,'permitted_entries':alive}


def noncontact_link_at_A():
    out=stars(('F','L','D','U'),1,rt=[edge('F','L')],rq=[edge('F','D'),edge('L','D')],zero=('U',))
    need(not out,'forced Y=L sealsC3 at degree4 A')
    return out


def prefix_other_internal_aliases():
    out=[]
    for y in ('D','o4'):
        for m in ('o2',y):
            ts,qs=full_F_prefix('A',y,m)
            out.append({'Y_role':y,'M_original_alias':m,'permitted':legal(ts,qs)})
    need(not any(x['permitted'] for x in out),'M=L orY cannot survive triangle/diagonal/simplicity constraints')
    return out


def nonshared_fan_cross_aliases():
    # The two actual shared originals X,Z exhaust F/G common contacts.
    entries=[]
    for a,b in (('o2','o3'),('o2','o5'),('o4','o3'),('o4','o5')):
        ren={b:a}
        f={'o0','G','o1','o2','o4'}
        g={ren.get(x,x) for x in ('o1','F','o0','o3','o5')}
        common=sorted(f&g)
        need(len(common)==3,'any other fan cross-alias makes a third actual common contact')
        entries.append({'identified_originals':[a,b],'F_G_common_contacts':common,'permitted':False})
    return entries


def one_T_opposite_K_frames():
    result=[]
    for h,y in (('A','D'),('A','o4'),('D','A'),('D','o4')):
        ts,qs=full_F_prefix(h,y);prefix=[];permitted=[]
        for k in POINTS:
            qq=qs+[('o0','o3',k,h)]
            if not legal(ts,qq,fixed=[(h,'V')]):
                continue
            prefix.append(k)
            neigh=tuple(sorted({'o0',y,k,'V'}))
            need(len(neigh)==4,'all four actual H contacts after alias controls')
            if stars(neigh,1,rq=[edge('o0',y),edge('o0',k)],zero=('U','V')):
                permitted.append(k)
        need(not permitted,'all actual K choices excluded at one-T H')
        result.append({'H':h,'Y':y,'raw_K_aliases':15,'necessary_prefix_entries':prefix,'permitted_K_entries':permitted})
    return result


def zero_T_opposite_ordinary_end():
    out=[]
    for h in ('B','C'):
        ts,qs=full_F_prefix(h,'o4');permitted=[]
        for j in POINTS:
            if legal(ts+[('o4',h,j)],qs,fixed=[(h,'V')]):
                permitted.append(j)
        need(not permitted,'qualified ordinary Y,L forces forbidden T at zero-T H')
        out.append({'H':h,'raw_forced_T_original_aliases':15,'permitted_entries':permitted})
    return out


def zero_T_opposite_KO_frames(ignore_three_contacts=False):
    out=[]
    for h,y,assoc in product(('B','C'),('A','D'),('U','V')):
        ts,qs=full_F_prefix(h,y);rows=[];prefix=[]
        fixed=[(h,'V'),(y,assoc)]
        for k in POINTS:
            qq=qs+[('o0','o3',k,h)]
            if legal(ts,qq,fixed=fixed,ignore_three_contacts=ignore_three_contacts):
                prefix.append(k)
            mask=0
            for i,o in enumerate(POINTS):
                if legal(ts,qq+[(h,y,o,'V')],fixed=fixed,ignore_three_contacts=ignore_three_contacts):
                    mask|=1<<i
            rows.append(mask)
        out.append({'H':h,'Y':y,'Y_three_contact':assoc,'raw_KO_aliases':225,'necessary_prefix_K_entries':prefix,'permitted_O_bitmasks_by_original_K':rows})
    return out


def catalogue():
    root=Path(__file__).resolve().parent;deps=json.loads((root/'DEPENDENCIES.json').read_text())['files']
    for path,m in deps.items():
        need(hashlib.sha256((root.parent/path).read_bytes()).hexdigest()==m['sha256'],'public byte guard '+path)
    old=json.loads((root.parent/'tammes15_four_two_triangle_fives_exclusion/EXPECTED.json').read_text())['catalogue_corollary']
    rows=old['remaining_beta_profiles'];target=(2,2,2,[2,0,0])
    removed=[r for r in rows if (r['r'],r['a'],r['b'],r['five_counts_f0_f1_f2'])==target]
    need(len(rows)==19 and old['counts_r1_r2_r3']==[0,8,11] and len(removed)==1,'checked19 and exact unique target')
    left=[r for r in rows if r not in removed]
    return {'newly_excluded_row':removed[0],'remaining_beta_profiles':left,'counts_r1_r2_r3':[0,7,11],
            'remaining_profile_sha256':hashlib.sha256(json.dumps(left,separators=(',',':')).encode()).hexdigest(),
            'prior19_source_imported_not_regenerated':True,'prior_source_only_and_rejected_registrations_not_committed':True,
            'guarded_public_dependency_sha256':{p:m['sha256'] for p,m in deps.items()}}


def main():
    xlinks=stars(('F','G','M','H'),2,rt=[edge('F','G'),edge('G','M')],rq=[edge('F','H')])
    need(len(xlinks)==2 and all(['H','M'] in x['Q_pairs'] for x in xlinks),'last Q at full ordinary X')
    h1=stars(('X','Y','K','V'),1,rq=[edge('X','Y'),edge('X','K')],zero=('V',))
    h0=stars(('X','Y','K','V'),0,rq=[edge('X','Y'),edge('X','K')])
    released=stars(('X','Y','K','V'),1,rq=[edge('X','Y'),edge('X','K')])
    need(not h1 and len(h0)==2 and len(released)==4,'one/zero-T H stars and nonempty released-three control')
    duplicate=stars(('X','Y','P','V'),0,rq=[edge('X','Y'),edge('X','Y')])
    duplicate_release=stars(('X','Y','P','V'),0,rq=[edge('X','Y')])
    need(not duplicate and duplicate_release,'two distinct known Q corners cannot merge into one cycle edge')
    endpoint=stars(('F','L','H','J'),2,rt=[edge('F','L')],rq=[edge('F','H')])
    forced=[x for x in endpoint if not any('L' in e for e in x['T_pairs'] if e!=['F','L'])]
    need(len(endpoint)==4 and len(forced)==2 and all(['H','J'] in x['T_pairs'] for x in forced),'qualified ordinary end links')
    noncontact=noncontact_frames();noncontact_control=noncontact_frames(last_Q=False)
    need(not noncontact['permitted_entries'] and noncontact_control['permitted_entries'],'noncontact complete-contact prefix and nonempty pre-final-Q control')
    zeros=zero_T_opposite_KO_frames();zero_control=zero_T_opposite_KO_frames(ignore_three_contacts=True)
    need(all(not any(x['permitted_O_bitmasks_by_original_K']) for x in zeros),'all1800terminalKOoriginal frames excluded')
    need(any(any(x['permitted_O_bitmasks_by_original_K']) for x in zero_control),'three-neighbor restriction has a nonempty released control')
    lo,w=Fraction(1,2),Fraction(1,10);p0=1+lo-4*lo*lo;p1=w*(1-8*lo);p2=-4*w*w
    bernstein=list(map(str,(p0,p0+p1/2,p0+p1+p2)))
    need(bernstein==['1/2','7/20','4/25'],'credited full-interval corner margin')
    return {'agent':'six-tammes-1','role':'researcher','status':'conditional hand proof with small exact support; independent mathematical review pending',
            'scope':'actual fifteen-point complete connected degree3..5 contact graph, simple strictly convex hemispherical cellular T/Q faces,nine Qs',
            'new_row_interval':'FULL OPEN1/2<c<3/5,no beta/H premise','neighbor_cover':neighbor_cover(),'shared_five_pair_cover':shared_pair_cover(),
            'opposite_five_all_original_alias_cover':opposite_five_alias_cover(),
            'ordinary_X_forced_last_Q_links':xlinks,'one_T_opposite_H_links':h1,'zero_T_opposite_H_links':h0,
            'duplicate_K_equals_Y_known_corner_links':duplicate,'qualified_endpoint_all_links':endpoint,'qualified_endpoint_forced_links':forced,
            'noncontact_all_original_end_frames':noncontact,'noncontact_forced_alias_sealed_A_links':noncontact_link_at_A(),
            'nonshared_fan_cross_original_aliases':nonshared_fan_cross_aliases(),
            'other_G_internal_original_alias_controls':prefix_other_internal_aliases(),'one_T_opposite_all_K_frames':one_T_opposite_K_frames(),
            'zero_T_opposite_ordinary_Y_forced_T_frames':zero_T_opposite_ordinary_end(),'zero_T_opposite_all_KO_frames':zeros,
            'controls':{'not_sphere_packings':True,'H_one_T_released_three_quota_links':released,'released_duplicate_corner_links':duplicate_release,
                        'noncontact_before_final_Q':noncontact_control,'zero_KO_released_three_neighbor_restriction':zero_control},
            'credited_Bernstein_entries':bernstein,'catalogue_corollary':catalogue(),
            'written_geometric_bridges_unformalized':True,'global_numerical_Tammes15_bounds_unchanged':True}


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
