"""Small exact original-face checks, six-tammes-1, researcher.
The hand proof supplies the geometric/face bridges; no packing census.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

ORIGINALS=('U','V','F','G','A','D','B')+tuple('o'+str(i) for i in range(8))
ORD=ORIGINALS[7:]
DEG=dict(zip(ORIGINALS,(3,3,5,5,4,4,4)+(4,)*8))
CAP=dict(zip(ORIGINALS,(0,0,4,2,1,1,0)+(2,)*8))


def need(b,m):
    if not b:
        raise ValueError(m)


def edge(a,b):
    return tuple(sorted((a,b)))


def stars(names,t,rt=(),rq=(),zero=(),qq_exact=None):
    out=[]
    for p in permutations(names[1:]):
        cycle=names[:1]+p
        es=[edge(cycle[i],cycle[(i+1)%len(cycle)]) for i in range(len(cycle))]
        for ids in combinations(range(len(cycle)),t):
            ts={es[i] for i in ids};qs=set(es)-ts
            if not set(rt)<=ts or not set(rq)<=qs or any(v in e for v in zero for e in ts):
                continue
            qq={v for v in names if not any(v in e for e in ts)}
            if qq_exact is not None and qq!=set(qq_exact):
                continue
            out.append({'cycle':list(cycle),'T_pairs':sorted(map(list,ts)),'Q_pairs':sorted(map(list,qs))})
    return sorted(out,key=lambda s:(s['cycle'],s['T_pairs']))


def neighbor_cover():
    triples=list(combinations(('A','B','D','G'),3))
    def canonical(u,v):
        choices=[]
        for swap in (False,True):
            ren={'A':'D','D':'A'} if swap else {}
            choices.append(tuple(sorted(tuple(sorted(ren.get(x,x) for x in t)) for t in (u,v))))
        return min(choices)
    entries=[]
    for u,v in product(triples,repeat=2):
        if u==v:
            continue
        shared=sorted(set(u)&set(v))
        need(len(shared)==2,'two actual common contacts')
        entries.append({'U_neighbors':list(u),'V_neighbors':list(v),'role_orbit':list(map(list,canonical(u,v))),
                        'shared_contacts':shared,'forced_Q':['U',shared[0],'V',shared[1]],
                        'mechanism':'one_T_shared_four' if set(shared)&{'A','D'} else 'G_double_three_star'})
    counts=Counter(tuple(map(tuple,e['role_orbit'])) for e in entries)
    need(len(entries)==12 and len(counts)==4,'full12/4 cover')
    return {'all_twelve_entries':entries,'four_orbits':[{'pair':list(map(list,k)),'ordered_entries':v} for k,v in sorted(counts.items())]}


def f_shared_stars():
    out=[]
    for s in stars(('G','X','Z','P','Q'),4,rt=[edge('G','X'),edge('G','Z')]):
        q=s['Q_pairs'][0]
        es={tuple(e) for e in s['T_pairs']}
        path=[q[0]]
        while len(path)<5:
            nxt=[b if a==path[-1] else a for a,b in es if path[-1] in (a,b)]
            nxt=[x for x in nxt if len(path)==1 or x!=path[-2]]
            need(len(nxt)==1 and nxt[0] not in path,'simple complete F triangle path')
            path.append(nxt[0])
        need(path[-1]==q[1] and path.index('G') in (1,2,3),'G is a F internal')
        out.append(dict(s,F_T_path=path,G_internal_position=path.index('G'),
                        Z_shared_opposite_obstruction='sealed_C3_at_Z' if 'Z' in q else 'H_quota_forces_contact_Q_diagonal'))
    need(len(out)==12,'all oriented F/G shared stars')
    return out


def quad(q):
    return min(x[i:]+x[:i] for x in (q,q[::-1]) for i in range(4))


def legal(ts,qs,capacity=None,ignore_diagonal=False):
    if any(len(set(f))!=len(f) for f in ts+qs):
        return False
    ts={tuple(sorted(t)) for t in ts};qs={quad(q) for q in qs}
    counts=Counter(v for t in ts for v in t)
    cap=CAP if capacity is None else dict(CAP,**capacity)
    if any(counts[v]>cap[v] for v in ORIGINALS):
        return False
    adj={v:set() for v in ORIGINALS};incidence=Counter()
    for f in ts|qs:
        for i in range(len(f)):
            a,b=f[i],f[(i+1)%len(f)];adj[a].add(b);adj[b].add(a);incidence[edge(a,b)]+=1
    if any(len(adj[v])>DEG[v] for v in ORIGINALS) or any(x>2 for x in incidence.values()):
        return False
    if not ignore_diagonal and any(q[2] in adj[q[0]] or q[3] in adj[q[1]] for q in qs):
        return False
    if any(len(adj[a]&adj[b])>2 for a,b in combinations(ORIGINALS,2)):
        return False
    return True


def opposite_pair_frames(h,capacity=None,ignore_diagonal=False):
    survivors=[]
    for j,k in product(ORIGINALS,repeat=2):
        if legal([(h,ORD[0],j),(h,ORD[1],k)],[('F',ORD[0],h,ORD[1])],capacity,ignore_diagonal):
            survivors.append([j,k])
    return {'opposite':h,'raw_assignments':225,'surviving_original_assignments':survivors}


def c3_zero_opposite_cases():
    out=[]
    for gpos,dend in product((1,2,3),('absent','left','right')):
        if (gpos==1 and dend=='left') or (gpos==3 and dend=='right'):
            reason='D_G_contact_forbidden_by_G_Q_opposite'
        elif (gpos==1 and dend=='right') or (gpos==3 and dend=='left'):
            reason='D_four_contacts_F_L_B_V_plus_one_G_endpoint'
        else:
            reason='ordinary_endpoint_internal_pair_forces_T_at_B'
        out.append({'G_F_internal_position':gpos,'D_F_endpoint':dend,'reason':reason})
    return out


def c3_last_contacts():
    # Y,G,W,L,D are five distinct original F neighbors.
    return [{'G_D_side_endpoint':v,'D_forced_contacts':sorted(('F','o2','B','V',v)),
             'distinct_contacts':5,'degree_cap':4} for v in ('o0','o1')]


def c4_one_T_F_contact_frames():
    out=[]
    for h in ('A','D'):
        entries=[]
        controls=[]
        for p in ORD[1:]:
            ts=[('G',ORD[0],ORD[1]),('F',h,ORD[0]),('F',ORD[0],p)]
            count=Counter(v for t in {tuple(sorted(t)) for t in ts} for v in t)[ORD[0]]
            need(count==3,'three distinct Ts at actual ordinary G endpoint')
            entries.append({'other_F_internal':p,'ordinary_endpoint_triangle_count':count,'permitted':legal(ts,[])})
            if legal(ts,[],capacity={ORD[0]:3}):
                controls.append(p)
        need(not any(x['permitted'] for x in entries) and controls,'endpoint quota obstruction with nonempty release')
        out.append({'one_T_F_contact':h,'all_seven_other_internal_aliases':entries,'released_endpoint_quota_controls':controls})
    return out


def catalogue():
    root=Path(__file__).resolve().parent
    deps=json.loads((root/'DEPENDENCIES.json').read_text())['files']
    for n,m in deps.items():
        need(hashlib.sha256((root.parent/n).read_bytes()).hexdigest()==m['sha256'],'public dependency '+n)
    old=json.loads((root.parent/'tammes15_two_one_triangle_fours_exclusion/EXPECTED.json').read_text())['catalogue_corollary']
    rows=old['remaining_beta_profiles']
    removed=[r for r in rows if (r['r'],r['a'],r['b'],r['five_counts_f0_f1_f2'])==(2,2,1,[1,0,1])]
    need(len(rows)==20 and old['counts_r1_r2_r3']==[0,9,11] and len(removed)==1,'preceding20 and unique new row')
    left=[r for r in rows if r not in removed]
    return {'newly_excluded_row':removed[0],'remaining_beta_profiles':left,'counts_r1_r2_r3':[0,8,11],
            'remaining_profile_sha256':hashlib.sha256(json.dumps(left,separators=(',',':')).encode()).hexdigest(),
            'prior_catalogue_imported_not_regenerated':True,'prior20_source_graph_attempt_rejected_not_committed':True,
            'guarded_dependency_sha256':{n:m['sha256'] for n,m in deps.items()}}


def main():
    one_T_shared=stars(('U','V','P','Q'),1,zero=('U','V'))
    need(len(one_T_shared)==4 and all(['U','V'] in s['Q_pairs'] for s in one_T_shared),'all one-T shared-three Q stars')
    single=stars(('U','X','R','S','Z'),2,zero=('U',),qq_exact=('U',))
    double=stars(('U','V','X','R','Z'),2,zero=('U','V'),qq_exact=('U','V'))
    need(len(single)==24 and len(double)==12,'all one/double-three G stars')
    for s in single:
        incidence=Counter(v for e in s['T_pairs'] for v in e)
        need(all(incidence[v]==1 for v in ('X','R','S','Z')),'single-three G has only TQ other contacts')
    for s in double:
        need(['U','V'] in s['Q_pairs'],'double-three shared Q')
    full=stars(('a','b','c','d','e'),4)
    for s in full:
        inc=Counter(v for e in s['T_pairs'] for v in e)
        need(sorted(inc.values())==[1,1,2,2,2] and {v for v in inc if inc[v]==1}==set(s['Q_pairs'][0]),'F one-T neighbors only Q endpoints,no QQ')
    hcontrol=stars(('V','Z','P','Q'),1,rq=[edge('P','Q'),edge('Z','V')],zero=('V',))
    hsaturated=[x for x in hcontrol if not any('Z' in e for e in x['T_pairs'])]
    need(len(hcontrol)==4 and not hsaturated,'shared opposite full internal leaves no H T')
    sealed=stars(('F','G','H','N'),2,rt=[edge('F','G')],rq=[edge('F','H'),edge('G','H')])
    need(not sealed,'sealed C3 at ordinary Z cannot have degree4')
    degree_control=stars(('F','G','H'),1,rt=[edge('F','G')],rq=[edge('F','H'),edge('G','H')])
    need(len(degree_control)==2,'two abstract degree3 link controls')
    both_three=stars(('U','V','P','Q'),1,rq=[edge('P','Q')],zero=('U','V'))
    need(not both_three,'one-T four with two threes cannot be F Q opposite')
    endpoint=stars(('H','R','C','J'),2,rt=[edge('H','R')],rq=[edge('H','C')])
    forced=[x for x in endpoint if not any('R' in e for e in x['T_pairs'] if e!=['H','R'])]
    need(len(endpoint)==4 and len(forced)==2,'qualified endpoint links')
    one,zero=opposite_pair_frames('A'),opposite_pair_frames('B')
    relaxed_diag=opposite_pair_frames('A',ignore_diagonal=True)
    relaxed_quota=opposite_pair_frames('A',capacity={'A':2})
    need(not one['surviving_original_assignments'] and not zero['surviving_original_assignments'],'all actual opposite aliases excluded')
    need(relaxed_diag['surviving_original_assignments']==[['o1','o0']] and relaxed_quota['surviving_original_assignments'],'nonempty opposite controls')
    lo,w=Fraction(1,2),Fraction(1,10)
    b0=1+lo-4*lo*lo;b1=w*(1-8*lo);b2=-4*w*w
    bernstein=list(map(str,(b0,b0+b1/2,b0+b1+b2)))
    need(bernstein==['1/2','7/20','4/25'],'credited strict margin')
    return {'agent':'six-tammes-1','role':'researcher','status':'conditional hand proof with small exact local checks; independent mathematical review pending',
            'scope':'actual N15 complete connected degree3..5,simple strictly convex hemispherical cellular T/Q,nine Qs',
            'new_row_interval':'FULL OPEN1/2<c<3/5,no beta/H premise','neighbor_cover':neighbor_cover(),
            'one_T_shared_three_stars':one_T_shared,
            'G_all_single_three_stars':single,'G_all_double_three_stars':double,'F_four_T_raw_oriented_stars':len(full),
            'F_G_shared_stars':f_shared_stars(),'shared_opposite_released_internal_H_stars':hcontrol,
            'shared_opposite_saturated_internal_H_stars':hsaturated,'shared_opposite_sealed_degree4_stars':sealed,
            'shared_opposite_degree3_abstract_control':degree_control,'one_T_opposite_with_two_threes_stars':both_three,
            'qualified_endpoint_all_links':endpoint,'qualified_endpoint_forced_links':forced,
            'all_ordinary_one_T_opposite_frames':one,'all_ordinary_zero_T_opposite_frames':zero,
            'C3_F_Q_zero_opposite_all_nine_cases':c3_zero_opposite_cases(),'C3_last_D_contact_entries':c3_last_contacts(),
            'C4_one_T_F_contact_original_aliases':c4_one_T_F_contact_frames(),
            'C4_F_Q_B_G_positions':[{'G_position':i,'reason':'both endpoints ordinary,one pair remains ordinary,forces_T_B'} for i in (1,2,3)],
            'controls':{'released_Q_diagonal':relaxed_diag,'released_opposite_T_quota':relaxed_quota,'not_sphere_packings':True},
            'credited_Bernstein_entries':bernstein,'catalogue_corollary':catalogue(),
            'written_geometric_bridges_unformalized':True,'global_numerical_Tammes15_bounds_unchanged':True}


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
