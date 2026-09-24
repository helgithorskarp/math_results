"""Definition-level exact author audits; no imported design theorem is tested.

Run: python3 check.py > /tmp/bounded-type-audit.json
All sizable literal witnesses are regenerated in memory, not published data.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from math import comb
import random

from constructions import (affine_classes, balanced_roles, edge, exterior_fixture,
                           pendant_tag, type_balanced_coloring)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def ceil(x):
    return -(-x.numerator//x.denominator)


def checked_coloring(types, edges, palette, cert):
    """Replay only swaps and definition-level incidence/color counts."""
    n = len(types)
    need(len(cert['initial']) == len(edges) == len(cert['colors']), 'color length')
    need(all(type(c) is int and 0 <= c < palette for c in cert['initial']), 'color range')
    colors = list(cert['initial'])
    endpoint_type = [tuple(sorted((types[a],types[b]))) for a,b in edges]
    original = Counter((t,c) for t,c in zip(endpoint_type, colors))
    sizes = Counter(endpoint_type)
    for t, m in sizes.items():
        low, rem = divmod(m,palette)
        need(all(low <= original[t,c] <= low+bool(rem) for c in range(palette)), 'type quota')
    at = [Counter() for _ in range(n)]
    for (a,b),c in zip(edges,colors):
        at[a][c] += 1
        at[b][c] += 1
    potential = sum(comb(v,2) for row in at for v in row.values())
    need(cert['initial_potential'] == potential, 'initial potential')
    for x,y,before,after in cert['trace']:
        need(0 <= x < len(edges) and 0 <= y < len(edges) and x != y, 'swap index')
        need(endpoint_type[x] == endpoint_type[y], 'swap changes type')
        need(len(set(edges[x]+edges[y])) == 4, 'swap endpoints intersect')
        affected = set(edges[x]+edges[y])
        local_before = sum(comb(k,2) for v in affected for k in at[v].values())
        for idx in (x,y):
            for v in edges[idx]:
                at[v][colors[idx]] -= 1
        colors[x],colors[y] = colors[y],colors[x]
        for idx in (x,y):
            for v in edges[idx]:
                at[v][colors[idx]] += 1
        local_after = sum(comb(k,2) for v in affected for k in at[v].values())
        need(before == potential and after == potential+local_after-local_before and after < before,
             'bad potential trace')
        potential = after
    need(colors == cert['colors'], 'trace endpoint')
    need(Counter((t,c) for t,c in zip(endpoint_type,colors)) == original, 'changed type/color counts')
    need(potential == 0 and all(k <= 1 for row in at for k in row.values()), 'improper coloring')
    return len(cert['trace'])


def tag_audit():
    records = []
    for n in range(1,25):
        for k in (1,2,3):
            for m in range(1,65):
                total = k*m
                roles = balanced_roles(n,total)
                tag = pendant_tag(roles)
                a, omitted = tag['columns'], set(map(tuple,tag['missing']))
                need(len(omitted) == len(tag['missing']), 'duplicate omission')
                row = Counter(x for x,y in omitted)
                col = Counter(y for x,y in omitted)
                need(all(0 <= x < n and 0 <= y < a for x,y in omitted), 'tag endpoint')
                need(all(a-row[x] == roles[x] for x in range(n)), 'wrong pendant role')
                need(sum(roles) == total and n*a-len(omitted) == total, 'tag total')
                need(max(row.values(),default=0) <= 1 and
                     max(col.values(),default=0) <= ceil(F(n,a)), 'tag deletion degree')
                need(max(col.values(),default=0)-min([col[y] for y in range(a)]) <= 1, 'column balance')
                records.append([n,k,m,a,len(omitted)])
    return {'instances': len(records), 'records_sha256': digest(records)}


def embedding_audit():
    """Enumerate labeled role injections, including repeated original types."""
    cases = [([7],(0,0,0),7), ([7],(0,0,0),8),
             ([5,5],(0,0,1),6), ([3,4,5],(0,1,2),7),
             ([6],(0,0),8), ([4,5],(0,1),7)]
    records = []
    for sizes, pat, m in cases:
        k = Counter(pat)
        offsets, total = [],0
        for n in sizes:
            offsets.append(total); total += n
        tag_sizes, missing, tag_offsets = {},set(),{}
        for h in sorted(k):
            roles = balanced_roles(sizes[h],k[h]*m)
            tag = pendant_tag(roles)
            tag_sizes[h] = tag['columns']
            tag_offsets[h] = total
            missing.update(edge(offsets[h]+x,total+y) for x,y in tag['missing'])
            total += tag['columns']
        choices = []
        keys = []
        for h in sorted(k):
            choices.append(list(permutations(range(offsets[h],offsets[h]+sizes[h]),k[h])))
            keys.append(('original',h))
            choices.append(list(permutations(range(tag_offsets[h],tag_offsets[h]+tag_sizes[h]),k[h])))
            keys.append(('tag',h))
        full, valid, charged = Counter(),Counter(),Counter()
        count = survived = 0
        for selected in product(*choices):
            chosen = dict(zip(keys,selected))
            used = Counter()
            originals, pendants = [],[]
            for h in pat:
                a = used[h]; used[h] += 1
                originals.append(chosen['original',h][a])
                pendants.append(chosen['tag',h][a])
            edges = [edge(a,b) for a,b in combinations(originals,2)]
            edges += [edge(a,b) for a,b in zip(originals,pendants)]
            need(len(set(edges)) == len(edges), 'augmented copy not simple')
            full.update(edges)
            bad = len(set(edges)&missing)
            if not bad:
                valid.update(edges); survived += 1
            else:
                for e in edges:
                    if e not in missing:
                        charged[e] += bad
            count += 1
        expected = 1
        for choice in choices:
            expected *= len(choice)
        need(count == expected and count > 0, 'embedding normalization')
        mult = Counter(tuple(sorted((pat[a],pat[b]))) for a,b in combinations(range(len(pat)),2))
        for (h,j),a_e in mult.items():
            pairs = combinations(range(sizes[h]),2) if h == j else product(range(sizes[h]),range(sizes[j]))
            capacity = comb(sizes[h],2) if h == j else sizes[h]*sizes[j]
            for a,b in pairs:
                e = edge(offsets[h]+a,offsets[j]+b)
                need(F(m*full[e],count) == F(m*a_e,capacity), 'original full load')
        for h in k:
            for x in range(sizes[h]):
                for y in range(tag_sizes[h]):
                    e = edge(offsets[h]+x,tag_offsets[h]+y)
                    need(F(m*full[e],count) == F(k[h]*m,sizes[h]*tag_sizes[h]), 'tag full load')
        for e in full:
            if e in missing:
                need(valid[e] == 0, 'missing tag used')
            else:
                need(0 <= full[e]-valid[e] <= charged[e], 'restriction charge')
        records.append({'parts':sizes, 'pattern':list(pat), 'count':m,
                        'embeddings':count, 'surviving':survived,
                        'loads_sha256':digest([[list(e),full[e],valid[e]] for e in sorted(full)])})
    return {'cases':records, 'total_embeddings':sum(x['embeddings'] for x in records)}


def augmented_fano():
    triples = [t for t in combinations(range(1,8),3) if t[0]^t[1]^t[2] == 0]
    used = [set() for _ in range(8)]
    assignment = []
    def search(j):
        if j == len(triples):
            return True
        for colors in permutations(range(3)):
            if all(c not in used[v] for v,c in zip(triples[j],colors)):
                for v,c in zip(triples[j],colors): used[v].add(c)
                assignment.append(colors)
                if search(j+1): return True
                assignment.pop()
                for v,c in zip(triples[j],colors): used[v].remove(c)
        return False
    need(search(0), 'Fano pendant lift failed')
    copies = []
    for tri,cols in zip(triples,assignment):
        copies.append([edge(a,b) for a,b in combinations(tri,2)]+
                      [edge(v,8+c) for v,c in zip(tri,cols)])
    counts = Counter(e for copy in copies for e in copy)
    host = set(combinations(range(1,8),2))|{(v,8+c) for v in range(1,8) for c in range(3)}
    need(set(counts) == host and set(counts.values()) == {1}, 'augmented decomposition')
    for v in range(1,8):
        need(sum(v in t for t in triples) == sum(v in e for e in host if max(e)>=8) == 3,
             'local decoding')
    return {'original_triangles':7,'augmented_edges':len(host),'certificate_sha256':digest(copies)}


def coloring_audit():
    rng = random.Random(20260924)
    records, swaps = [],0
    # Exhaust every graph through five vertices with an arbitrary two-part cut.
    # Distinct initial colors make these domain/decoding tests; they do not
    # exercise the repair theorem below.
    for n in range(1,6):
        pairs = list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            edges = [e for j,e in enumerate(pairs) if mask>>j&1]
            types = [int(v>=n//2) for v in range(n)]
            palette = max(1,len(edges))
            initial = list(range(len(edges)))
            cert = type_balanced_coloring(types,edges,palette,initial)
            checked_coloring(types,edges,palette,cert)
            records.append([n,mask,digest(cert['colors'])])
    random_records = []
    for n in (24,32,48,64):
        for r in (1,2,3):
            for rep in range(5):
                types = [min(r-1,v*r//n) for v in range(n)]
                edges = [e for e in combinations(range(n),2) if rng.randrange(5)>0]
                rng.shuffle(edges)
                cert = type_balanced_coloring(types,edges,4*n)
                swaps += checked_coloring(types,edges,4*n,cert)
                random_records.append([n,r,rep,len(edges),len(cert['trace']),digest(cert['colors'])])
    # This literal case meets every sufficient hypothesis (7), not merely
    # the successful finite-witness conditions.
    s,beta,E,N = 384,F(1,2),3,49152
    types = [0]*192+[1]*192
    edges = list(combinations(range(s),2))
    cert = type_balanced_coloring(types,edges,N)
    swaps += checked_coloring(types,edges,N,cert)
    sizes = Counter(tuple(sorted((types[a],types[b]))) for a,b in edges)
    need(min(Counter(types).values())>=64*(2+1) and N>=64*s and
         min(sizes.values())>=32*s, 'color theorem domain')
    for t,m in sizes.items():
        deg = Counter(v for e in edges if tuple(sorted(types[x] for x in e))==t for v in e)
        need(max(deg.values())<=2*F(m,beta*s)+1, 'type degree bound')
    # A second fixture has unequal classes and no comparability parameter.
    unequal_types=[0]*192+[1]*1000
    unequal_edges=list(product(range(192),range(192,1192)))
    rng.shuffle(unequal_edges)
    uc=type_balanced_coloring(unequal_types,unequal_edges,64*1192)
    swaps+=checked_coloring(unequal_types,unequal_edges,64*1192,uc)
    need(192>=64*3 and len(unequal_edges)>=32*1192,'unequal color domain')
    return {'exhaustive_domain_instances':len(records), 'exhaustive_sha256':digest(records),
            'seeded_repair_instances':len(random_records), 'seed':20260924,
            'seeded_sha256':digest(random_records), 'replayed_swaps':swaps,
            'universal_hypotheses_fixture':{'vertices':s,'edges':len(edges),'colors':N,
                'swaps':len(cert['trace']),'certificate_sha256':digest(cert)},
            'unequal_classes_fixture':{'parts':[192,1000], 'edges':len(unequal_edges),
                'colors':64*1192,'swaps':len(uc['trace']),'certificate_sha256':digest(uc)}}


def profile_audit():
    records, intervals = [],0
    for r in (1,2,3):
        potential_edges = list(combinations_with_replacement(range(r),2))
        for bits in range(1<<len(potential_edges)):
            supported = {e for j,e in enumerate(potential_edges) if bits>>j&1}
            tris = [t for t in combinations_with_replacement(range(r),3)
                    if all(tuple(e) in supported for e in combinations(t,2))]
            for scale in (10**6,10**12):
                sizes = [(h+1)*scale for h in range(r)]
                s=sum(sizes); beta=F(min(sizes),s); d=2
                M=comb(r+2,3)+(d+1)*comb(r+1,2)
                lam=8*M/beta; theta=1-lam/s; B0=M*(6/beta+2); U=ceil(lam+B0)
                cap={e:(comb(sizes[e[0]],2) if e[0]==e[1] else sizes[e[0]]*sizes[e[1]])
                     for e in supported}
                patterns=[]
                remaining={e:F(b) for e,b in cap.items()}
                for j,t in enumerate(tris):
                    ae=Counter(tuple(e) for e in combinations(t,2))
                    y=min(F(cap[e],a) for e,a in ae.items())/(4*M)
                    if j%3==0: y=min(y,F(s,3))
                    elif j%3==1: y=min(y,F(3*s,2))
                    patterns.append((t,'triangle',y))
                    for e,a in ae.items():remaining[e]-=a*y
                for e in sorted(supported):
                    for i in range(d):
                        y=remaining[e]/(4*(d+1))
                        if (sum(e)+i)%3==0:y=F(0)
                        patterns.append((e,str(i),y));remaining[e]-=y
                    patterns.append((e,'spare',remaining[e]))
                data=[]
                for p,label,y in patterns:
                    m=(theta*y).__floor__()
                    m=m if m>=s else 0
                    need(0<=theta*y-m<s, 'profile cutoff')
                    roles={h:divmod(p.count(h)*m,sizes[h]) for h in set(p)}
                    data.append((p,label,y,m,roles))
                total_complement=Counter()
                for h,nh in enumerate(sizes):
                    breaks={0,nh}|{roles[h][1] for p,label,y,m,roles in data if h in roles}
                    ordered=sorted(breaks)
                    for lo,hi in zip(ordered,ordered[1:]):
                        if hi==lo:continue
                        intervals+=1
                        request=Counter();by_label=Counter();label_mean=Counter()
                        for p,label,y,m,roles in data:
                            if h not in roles:continue
                            q,extra=roles[h];rv=q+(lo<extra)
                            for j in range(r):
                                degree=p.count(j)-(j==h)
                                if degree:request[tuple(sorted((h,j)))]+=rv*degree
                            if len(p)==2 and label in ('0','1'):
                                by_label[label]+=rv
                                label_mean[label]+=F(p.count(h)*m,nh)
                        for e in supported:
                            if h not in e:continue
                            other=e[1] if e[0]==h else e[0]
                            pdeg=sizes[other]-(other==h)
                            need(theta*pdeg-B0<=request[e]<=theta*pdeg+2*M, 'role-vector bound')
                            comp=pdeg-request[e]
                            need(1<=comp<=U,'complement degree')
                            total_complement[h,e]+=(hi-lo)*comp
                        for label in ('0','1'):
                            need(abs(by_label[label]-label_mean[label])<r, 'XXH row discrepancy')
                for e in supported:
                    used=sum(Counter(tuple(x) for x in combinations(p,2))[e]*m
                             for p,label,y,m,roles in data)
                    if e[0]==e[1]:
                        need(total_complement[e[0],e]==2*(cap[e]-used), 'internal parity identity')
                    else:
                        need(total_complement[e[0],e]==total_complement[e[1],e]==cap[e]-used,
                             'cross complement sums')
                wanted=sum(y for p,label,y,m,roles in data if label!='spare')
                actual=sum(m for p,label,y,m,roles in data if label!='spare')
                need(wanted-actual<=(lam/2+M)*s,'interior loss')
                records.append([r,bits,scale,len(data),str(wanted-actual)])
    return {'profiles':len(records),'compressed_intervals':intervals,
            'maximum_order':6*10**12,'records_sha256':digest(records),
            'scope':'exact truncated counts and role/complement identities; no giant packing'}


def parameter_audit():
    records=[]
    for r in range(1,9):
        E=comb(r+1,2)
        for off in (0,1,3):
            beta=F(1,r+off);s=ceil(64*E/beta);N=ceil(64*s/beta)
            for D in (1,3,100):
                Tmin=64*(r+1);ss=max(s,r*Tmin);NN=64*ss
                for m in (16*(D+1)*ss,32*(D+1)*ss):
                    bad=(F(4*ss,NN)+F(2*(r+1),Tmin))*m+2*ss+F(D*ss*ss,NN)+2*D*(r+1)
                    need(bad<=F(7*m,32)<m,'color rejection bound')
            for d in range(1,9):
                L=off;A=3*r;B=2**(d+L)*(r+3);Q=8*B*(A+r*d+1)
                delta=r+1
                for j in range(d+L):
                    need(delta+2<B,'flow recurrence')
                    delta=2*delta+2
                need(Q>=8*A*B and Q>=8*r*d*B and Q>=2*A,'quota inequalities')
                alpha=F(1,d+1)
                eta=min(alpha/64,alpha/(8*A),alpha/(16*d))
                need(2*d*eta*Q/alpha+r*d*B<=F(Q,4),'Hall endpoint')
                records.append([r,off,d,str(eta),B,Q])
    return {'parameter_tuples':len(records),'records_sha256':digest(records)}


def induction_audit():
    """Exact bookkeeping tests; illustrative tolerances are not design bounds."""
    rng=random.Random(20260925)
    hierarchy=[]
    for t in range(2,9):
        eps=[F(1,t)];etas=[]
        for j in range(t):
            eta=eps[-1]/(64*(t+1))
            etas.append(eta)
            eps.append(min(eps[-1]/2,eta/(2*t*t))/2)
        choices=[eps[-1]/2]+eps[1:]+[(a+b)/2 for a,b in zip(eps,eps[1:])]
        tuples=(product(choices,repeat=t-1) if t<=4 else
                (tuple(rng.choice(choices) for _ in range(t-1)) for rep in range(1000)))
        for small in tuples:
            p=list(small)+[1-sum(small)]
            need(min(p)>0 and max(p)>=F(1,t),'proportions')
            empty=[j for j in range(t) if not any(eps[j+1]<=v<eps[j] for v in p)]
            need(empty,'no empty size band')
            j=empty[0]
            core=[v for v in p if v>=eps[j]]
            rest=[v for v in p if v<eps[j]]
            n=sum(core);s=sum(rest)
            need(n>=F(1,t) and len(rest)<=t-1,'core size')
            need(all(v>=eps[j]*n for v in core),'core comparability')
            need(all(v<eps[j+1] for v in rest) and s<etas[j]*n,'small union')
            hierarchy.append([t,j,len(rest),str(s),str(n)])
    deletions=[]
    for r in (1,2,3):
        sizes=list(range(2,r+2))
        all_edges=list(combinations_with_replacement(range(r),2))
        for bits in range(1<<len(all_edges)):
            support={e for k,e in enumerate(all_edges) if bits>>k&1}
            cap={e:(comb(sizes[e[0]],2) if e[0]==e[1] else sizes[e[0]]*sizes[e[1]]) for e in support}
            tris=[p for p in combinations_with_replacement(range(r),3)
                  if all(p.count(h)<=sizes[h] for h in set(p))
                  and all(tuple(e) in support for e in combinations(p,2))]
            y={};remaining={e:F(v) for e,v in cap.items()}
            for p in tris:
                ae=Counter(tuple(e) for e in combinations(p,2))
                mass=min(F(cap[e],a) for e,a in ae.items())/(2*max(1,len(tris)))
                y[p,'triangle']=mass
                for e,a in ae.items():remaining[e]-=a*mass
            for e,m in remaining.items():y[e,'edge']=m
            for removed in range(r):
                filler=Counter();kept=Counter();discarded=F(0)
                for (p,label),mass in y.items():
                    if removed in p:
                        discarded+=mass
                        for e in combinations(p,2):
                            if removed not in e:filler[tuple(e)]+=mass
                    else:
                        for e in combinations(p,2):kept[tuple(e)]+=mass
                need(discarded<=sum(v for e,v in cap.items() if removed in e),'small-cell loss')
                for e,v in cap.items():
                    if removed not in e:need(kept[e]+filler[e]==v,'released filler capacity')
                deletions.append([r,bits,removed,str(discarded)])
    growth=[]
    # Actual valid sparse type graphs K_(192,b), not generated huge graphs.
    # Their ratios tend to zero while all color-lemma inequalities hold.
    for b in (1000,10**6,10**12,10**24):
        a=192;s=a+b;N=64*s;m=a*b;D=1;r=2
        need(min(a,b)>=64*(r+1) and m>=16*(D+1)*s,'unbalanced growth domain')
        bad=(F(4*s,N)+F(2*(r+1),min(a,b)))*m+2*s+F(D*s*s,N)+2*D*(r+1)
        need(bad<=F(7*m,32),'unbalanced growth inequality')
        growth.append([a,b,N,str(F(bad,m))])
    return {'hierarchy_cases':len(hierarchy),'hierarchy_sha256':digest(hierarchy),
            'small_class_deletions':len(deletions),'deletions_sha256':digest(deletions),
            'unbalanced_color_profiles':growth,
            'scope':'illustrative rational size hierarchies and exact filler identities; no computed design tolerance'}


def make_fixture():
    points,classes=affine_classes(3)
    types=[p[0] for p in points]
    within=[item for item in classes if item[0][0]==0]
    cross=[item for item in classes if item[0][0]!=0]
    # X_1 is independent. X_0,X_2 are cliques, all cross pairs complete.
    interior=[t for _,cc in within[:1]+cross[:2] for t in cc
              if not all(types[x]==1 for x in t)]
    neighborhoods=[{0,1},{0},{1}]
    labels=[]
    for i in range(2):
        candidates=[edge(a,b) for _,cc in within[i+1:i+2]+cross[2+2*i:4+2*i]
                    for tri in cc for a,b in combinations(tri,2)]
        labels.append(sorted(e for e in candidates
                             if not all(types[x]==1 for x in e)
                             and all(i in neighborhoods[types[x]] for x in e)))
    targets={(0,0,0):4000,(0,0,1):5000,(0,1,1):4500,(1,0,0):8000,(2,1,1):9000}
    w={t:F(9*(q+3))+F(1,7) for t,q in targets.items()}
    v=Counter()
    for i,edges in enumerate(labels):
        for a,b in edges:v[tuple(sorted((types[a],types[b])))+(i,)]+=1
    v={t:F(m)+F(1,5) for t,m in v.items()}
    u=Counter(tuple(sorted(types[x] for x in t)) for t in interior)
    u={t:F(m)+F(1,7) for t,m in u.items()}
    sizes=[18000,19000]
    spokes={}
    for h in range(3):
        for i in neighborhoods[h]:
            vload=sum((int(a==h)+int(b==h))*m for (a,b,j),m in v.items() if j==i)
            wload=sum((int(a==i)+int(b==i))*m for (g,a,b),m in w.items() if g==h)
            spokes[h,i,0]=9*sizes[i]-vload-wload
    return {'core_sizes':sizes,'types':types,'interior':interior,'labels':labels,'spokes':spokes,
            'neighborhoods':neighborhoods,'w':w,'v':v,'u':u,'cutoff':3840,'buffer':3}


def checked_exterior(fixture,cert):
    f=fixture; sizes=f['core_sizes'];types=f['types'];s=len(types);n=sum(sizes)
    offsets=[0,sizes[0]];r=3;d=2;B=48;A=3
    groups=[[x for x,t in enumerate(types) if t==h] for h in range(r)]
    xedges={e for e in combinations(range(s),2) if not all(types[x]==1 for x in e)}
    xcap=Counter(tuple(sorted(types[x] for x in e)) for e in xedges)
    consumed=Counter()
    for t,m in f['u'].items():
        for a,b in combinations(t,2):consumed[a,b]+=m
    for (a,b,i),m in f['v'].items():consumed[a,b]+=m
    need(all(consumed[e]<=c for e,c in xcap.items()),'X fractional capacity')
    need(set(consumed)<=set(xcap),'unsupported X profile')
    for h,vertices in enumerate(groups):
        for i,N in enumerate(sizes):
            load=sum((int(a==h)+int(b==h))*m for (a,b,j),m in f['v'].items() if i==j)
            load+=sum((int(a==i)+int(b==i))*m for (g,a,b),m in f['w'].items() if g==h)
            load+=sum(m for (g,j,label),m in f['spokes'].items() if (g,j)==(h,i))
            need(load==(len(vertices)*N if i in f['neighborhoods'][h] else 0),'full fractional spoke capacity')
            need(i in f['neighborhoods'][h] or load==0,'unsupported spokes')
    expected=[tuple(n+x for x in t) for t in f['interior']]
    occupied=[[set() for _ in range(s)] for _ in sizes]
    color_swaps=0
    need(len(cert['colorings'])==len(f['labels']),'coloring count')
    for i,(edges,c) in enumerate(zip(f['labels'],cert['colorings'])):
        color_swaps+=checked_coloring(types,edges,sizes[i],c)
        degree=Counter(x for e in edges for x in e)
        typed_degree=defaultdict(Counter)
        for e in edges:
            t=tuple(sorted(types[x] for x in e))
            typed_degree[t].update(e)
        for t,row in typed_degree.items():
            for h in set(t):
                avg=F(sum(row[x] for x in groups[h]),len(groups[h]))
                need(all(abs(row[x]-avg)<1 for x in groups[h]),'interior typed roles')
        for (x,y),color in zip(edges,c['colors']):
            need((x,y) in xedges and i in f['neighborhoods'][types[x]] and
                 i in f['neighborhoods'][types[y]],'XXH support')
            for x0 in (x,y):
                need(color not in occupied[i][x0],'XXH repeated spoke')
                occupied[i][x0].add(color)
            expected.append((n+x,n+y,offsets[i]+color))
        for h,vertices in enumerate(groups):
            if i not in f['neighborhoods'][h]:continue
            tavg=F(sum(degree[x] for x in vertices),len(vertices))
            need(all(abs(degree[x]-tavg)<A for x in vertices),'initial row discrepancy')
            col=Counter(y for x in vertices for y in occupied[i][x])
            need(all(abs(col[y]-len(vertices)*tavg/sizes[i])<r+1 for y in range(sizes[i])),
                 'initial column discrepancy')
    spoke_quotas={t:(F(m)//len(groups[t[0]])-f['buffer']) for t,m in f['spokes'].items()}
    spoke_quotas={t:q for t,q in spoke_quotas.items() if q>=f['cutoff']}
    need([tuple(sp['type']) for sp in cert['labeled_spokes']]==sorted(spoke_quotas),'labeled spoke types')
    retained_spokes=[];spoke_errors=[]
    for sp in cert['labeled_spokes']:
        h,i,label=sp['type'];a=spoke_quotas[h,i,label];vertices=groups[h];N=sizes[i]
        need(sp['demand']==a and len(sp['selected'])==len(vertices),'labeled spoke rows')
        values=[F(0) for _ in range(N)];available=[]
        for x in vertices:
            row=set(range(N))-occupied[i][x];available.append(row)
            need(len(row)>=a,'labeled spoke feasibility')
            for y in row:values[y]+=F(a,len(row))
        col=Counter()
        for x,row,chosen in zip(vertices,available,sp['selected']):
            need(len(chosen)==len(set(chosen))==a and set(chosen)<=row,'labeled spoke selection')
            col.update(chosen);occupied[i][x].update(chosen)
            retained_spokes.extend(edge(n+x,offsets[i]+y) for y in chosen)
        need(all(v.__floor__()<=col[y]<=ceil(v) for y,v in enumerate(values)), 'labeled column rounding')
        err=max(abs(col[y]-F(len(vertices)*a,N)) for y in range(N))
        need(err<B,'labeled spoke discrepancy');spoke_errors.append(str(err))
    quotas={t:(F(m)//len(groups[t[0]])-f['buffer']) for t,m in f['w'].items()}
    quotas={t:q if q>=f['cutoff'] else 0 for t,q in quotas.items()}
    need(cert['quotas']==sorted(quotas.items()),'wrong quota table')
    order=[t for t,q in sorted(quotas.items(),key=lambda x:(x[1],x[0])) if q]
    need([tuple(rec['type']) for rec in cert['allocations']]==order,'allocation order')
    forbidden=defaultdict(set);typed_core=defaultdict(Counter)
    flow_discrepancies=[];matching_checks=0
    for rec in cert['allocations']:
        h,i,j=rec['type'];vertices=groups[h];q=quotas[h,i,j]
        need(rec['quota']==q,'wrong quota')
        need([(x['part'],x['demand']) for x in rec['spokes']]==
             ([(i,2*q)] if i==j else [(i,q),(j,q)]),'allocation shape')
        selected={}
        for sp in rec['spokes']:
            part,a=sp['part'],sp['demand'];N=sizes[part]
            need(len(sp['selected'])==len(vertices),'flow rows')
            available=[set(range(N))-occupied[part][x] for x in vertices]
            values=[F(0) for _ in range(N)]
            for neighbors in available:
                need(len(neighbors)>=a,'flow row feasibility')
                for y in neighbors:values[y]+=F(a,len(neighbors))
            col=Counter();selected[part]=[]
            for x,neighbors,chosen in zip(vertices,available,sp['selected']):
                need(len(chosen)==a and len(set(chosen))==a and set(chosen)<=neighbors,'bad selected row')
                selected[part].append(set(chosen));col.update(chosen)
                occupied[part][x].update(chosen)
            for y,value in enumerate(values):
                need(value.__floor__()<=col[y]<=ceil(value),'flow column floor/ceiling')
            err=max(abs(F(col[y])-F(len(vertices)*a,N)) for y in range(N))
            need(err<B,'selected column discrepancy')
            flow_discrepancies.append(str(err))
        need(len(rec['pairings'])==len(vertices),'pairing rows')
        for idx,(x,pairs) in enumerate(zip(vertices,rec['pairings'])):
            if i==j:
                endpoints=sorted(offsets[i]+y for y in selected[i][idx])
                left,right=set(endpoints[:q]),set(endpoints[q:])
            else:
                left={offsets[i]+y for y in selected[i][idx]}
                right={offsets[j]+y for y in selected[j][idx]}
            need(len(pairs)==q and {a for a,b in pairs}==left and {b for a,b in pairs}==right,
                 'pairing endpoint mismatch')
            maxbad=max([len(forbidden[a]&right) for a in left]+
                       [len(forbidden[b]&left) for b in right],default=0)
            need(maxbad<=F(q,4),'dense matching bound')
            matching_checks+=1
            for a,b in pairs:
                need(b not in forbidden[a],'repeated core edge')
                forbidden[a].add(b);forbidden[b].add(a)
                typed_core[i,j][a]+=1;typed_core[i,j][b]+=1
                expected.append((n+x,a,b))
    need(cert['triangles']==expected,'triangle certificate mismatch')
    seen=set(retained_spokes);tritypes=Counter()
    need(len(seen)==len(retained_spokes),'repeated labeled edge')
    for tri in cert['triangles']:
        need(len(tri)==3 and len(set(tri))==3,'bad triangle')
        for a,b in combinations(tri,2):
            need(0<=a<n+s and 0<=b<n+s,'triangle endpoint')
            if a>=n and b>=n:need(edge(a-n,b-n) in xedges,'unsupported internal edge')
            elif max(a,b)>=n:
                x=max(a,b)-n;v=min(a,b);i0=int(v>=sizes[0])
                need(i0 in f['neighborhoods'][types[x]],'unsupported spoke')
            e=edge(a,b);need(e not in seen,'edge reused');seen.add(e)
        tritypes[sum(v>=n for v in tri)]+=1
    need(max(map(len,forbidden.values()),default=0)<=s,'F maximum degree')
    max_disc=F(0)
    core_counts={e:sum(row.values())//2 for e,row in typed_core.items()}
    for e,row in typed_core.items():
        for i in set(e):
            avg=F(e.count(i)*core_counts[e],sizes[i])
            err=max(abs(row[x]-avg) for x in range(offsets[i],offsets[i]+sizes[i]))
            need(err<r*B,'core typed discrepancy');max_disc=max(max_disc,err)
    # Exact HHH profile: include repeated and cross types; not materialized.
    cap={(0,0):comb(sizes[0],2),(0,1):sizes[0]*sizes[1],(1,1):comb(sizes[1],2)}
    wsum=Counter()
    for (h,i,j),mass in f['w'].items():wsum[i,j]+=mass
    z={(0,0,1):F(100,3),(0,1,1):F(101,3)}
    z[0,0,0]=(cap[0,0]-wsum[0,0]-z[0,0,1])/6
    z[1,1,1]=(cap[1,1]-wsum[1,1]-z[0,1,1])/6
    demand=Counter()
    for t,m in z.items():
        need(m>=0,'negative HHH mass')
        for a,b in combinations(t,2):demand[a,b]+=m
    for e,b in cap.items():
        spare=b-demand[e]-wsum[e]
        new_spare=spare+wsum[e]-core_counts.get(e,0)
        need(spare>=0 and new_spare>=0 and demand[e]+new_spare==b-core_counts.get(e,0),
             'residual capacity profile')
    original=sum(f['u'].values())+sum(f['v'].values())+sum(f['w'].values())
    return {'vertices_X':s,'X_classes':[len(v) for v in groups],'core_order':n,
            'triangles':len(expected),'XXX':tritypes[3],'XXH':tritypes[2],'XHH':tritypes[1],
            'labeled_XH_edges':len(retained_spokes),'labeled_column_discrepancies':spoke_errors,
            'labeled_spoke_loss':str(sum(f['spokes'].values())-len(retained_spokes)),
            'replayed_color_swaps':color_swaps,'matching_checks':matching_checks,
            'matching_repairs':cert['matching_repairs'],'flow_column_discrepancies':flow_discrepancies,
            'maximum_core_degree':max(map(len,forbidden.values()),default=0),
            'maximum_core_type_discrepancy':str(max_disc),'external_fractional_loss':str(original-len(expected)),
            'preserved_HHH_mass':str(sum(z.values())),'triangles_sha256':digest(expected),
            'certificate_sha256':digest(cert),
            'scope':'explicit interior witnesses; universal flow cutoff met, design threshold not asserted'}


def negative_audit(f,cert):
    rejected=[]
    def fails(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError):rejected.append(name)
        else:raise ValueError('negative control accepted: '+name)
    fails('unbalanced_tag',lambda:pendant_tag([1,3]))
    fails('zero_tag',lambda:pendant_tag([0,0]))
    fails('unequitable_initial_colors',lambda:type_balanced_coloring([0]*3,[(0,1),(1,2)],2,[0,0]))
    fails('duplicate_simple_edge',lambda:type_balanced_coloring([0]*2,[(0,1),(0,1)],3))
    simple=type_balanced_coloring([0]*3,[(0,1),(1,2),(0,2)],3)
    bad=dict(simple);bad['colors']=[0,0,0]
    fails('improper_endpoint_colors',lambda:checked_coloring([0]*3,[(0,1),(1,2),(0,2)],3,bad))
    # Check cheap certificate failures before the expensive full positive replay.
    bad=dict(cert);bad['colorings']=cert['colorings'][:-1]
    fails('missing_label_coloring',lambda:checked_exterior(f,bad))
    bad=dict(cert);bad['quotas']=[]
    fails('wrong_quota_table',lambda:checked_exterior(f,bad))
    first=dict(cert['allocations'][0]);first['quota']+=1
    bad=dict(cert);bad['allocations']=[first]+cert['allocations'][1:]
    fails('wrong_row_quota',lambda:checked_exterior(f,bad))
    first=dict(cert['allocations'][0]);sp=dict(first['spokes'][0]);sp['selected']=[[]]+sp['selected'][1:]
    first['spokes']=[sp]+first['spokes'][1:]
    bad=dict(cert);bad['allocations']=[first]+cert['allocations'][1:]
    fails('missing_selected_spokes',lambda:checked_exterior(f,bad))
    return rejected


def main():
    audit={'status':'PASS','scope':'finite author audits; no universal design constructor or independent review'}
    audit['pendant_tags']=tag_audit()
    audit['labeled_embedding_loads']=embedding_audit()
    audit['augmented_fano_decomposition']=augmented_fano()
    audit['type_balanced_coloring']=coloring_audit()
    audit['compressed_profiles']=profile_audit()
    audit['parameter_bounds']=parameter_audit()
    audit['induction_bookkeeping']=induction_audit()
    f=make_fixture()
    cert=exterior_fixture(f['core_sizes'],f['types'],f['interior'],f['labels'],
                          f['neighborhoods'],f['w'],f['cutoff'],f['buffer'],f['spokes'])
    audit['interacting_extension']=checked_exterior(f,cert)
    audit['negative_controls']=negative_audit(f,cert)
    print(json.dumps(audit,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
