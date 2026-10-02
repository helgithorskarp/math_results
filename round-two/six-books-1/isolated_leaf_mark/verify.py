"""Independent columns/Boolean third-vertex checker; never imports derive.py."""
from collections import Counter
from itertools import combinations,permutations,product
from pathlib import Path
import argparse,copy,hashlib,json,time

START=time.monotonic()
LOCAL=((1,8,9),(0,),(6,7),(4,5),(3,7,9),(3,6,8),(2,5,9),(2,4,8),(0,5,7),(0,4,6))
MAPPING=(2,1,3,4,5,6,7,8,9,10)
FIXED=(0,1,2,9,10,11,12,13,14,15)
SYMMETRIES=(((0,1,2,3,4,5),(0,1)),((0,1,3,2,5,4),(1,0)),
            ((1,0,4,5,2,3),(0,1)),((1,0,5,4,3,2),(1,0)))

def guard():
    if time.monotonic()-START>45:raise RuntimeError('fixed45s guard: incomplete checks prove nothing')

def subsets(n,rank):
    return tuple(z for z in range(1<<n) if z.bit_count()==rank)

def outside_minima(n):
    table=[[n+1]*(n+1) for _ in range(n+1)]
    sets=[frozenset(i for i in range(n) if z&(1<<i)) for z in range(1<<n)]
    for left in sets:
        for right in sets:
            h=len(left&right)
            if h<table[len(left)][len(right)]:table[len(left)][len(right)]=h
    if any(table[i][j]!=max(0,i+j-n) for i in range(n+1) for j in range(n+1)):
        raise ValueError('literal pigeonhole control mismatch')
    return table

def matrix(state,n=16,y=None,sy_own=(0,0),sx_cross=(0,0)):
    word,beta,rx0,rx1,st0,st1=state
    m=[[False]*n for _ in range(n)]
    def red(i,j):m[i][j]=m[j][i]=True
    for old in range(10):
        red(0,MAPPING[old])
        for j in LOCAL[old]:red(MAPPING[old],MAPPING[j])
    for s in range(2):
        red(1,11+s);red(2,11+s)
        for i in range(6):
            if (rx0,rx1)[s]&(1<<i):red(11+s,3+i)
    for t in range(3):
        red(2,13+t)
        for i in range(8):
            if (word>>(3*i))&(1<<t):red(3+i,13+t)
        for s in range(2):
            if (st0,st1)[s]&(1<<t):red(11+s,13+t)
    if n==22:
        if y is None:raise ValueError('missing Y columns')
        for i in range(6):
            red(1,16+i)
            for t in range(3):
                if y[i]&(1<<t):red(16+i,13+t)
            for s in range(2):
                if sy_own[s]&(1<<i):red(16+i,11+s)
                if sx_cross[s]&(1<<i):red(16+i,9+s)
    return m

def red_sets(m):return [frozenset(j for j,c in enumerate(row) if c) for row in m]

def literal_bad(m,i,j):
    red=m[i][j]
    pages=sum(k!=i and k!=j and m[i][k]==red and m[j][k]==red for k in range(len(m)))
    return pages>(3 if red else 6),int(red),pages

def rename_mask(z,p):
    bits=[bool(z&(1<<i)) for i in range(len(p))];target=[False]*len(p)
    for i,j in enumerate(p):target[j]=bits[i]
    return sum(int(b)<<i for i,b in enumerate(target))

def images(state):
    word,beta,r0,r1,t0,t1=state
    old=[(word>>(3*i))&7 for i in range(8)]
    for p,sp in SYMMETRIES:
        for tp in permutations(range(3)):
            cols=[0]*8
            for i in range(6):cols[p[i]]=rename_mask(old[i],tp)
            for i in range(2):cols[6+sp[i]]=rename_mask(old[6+i],tp)
            for yp in ((0,1),(1,0)):
                rs=[0,0];ts=[0,0]
                for i in range(2):
                    rs[yp[i]]=rename_mask((r0,r1)[i],p)
                    ts[yp[i]]=rename_mask((t0,t1)[i],tp)
                yield (sum(c<<(3*i) for i,c in enumerate(cols)),p[beta],*rs,*ts)

def generate():
    low6=outside_minima(6);low8=outside_minima(8)
    base=matrix((0,0,0,0,0,0));rb=red_sets(base)
    # The four permitted permutations are checked against the literal leaf,
    # and closure is checked explicitly. Maximality of this subgroup is unused.
    for p,sp in SYMMETRIES:
        lift=list(range(16))
        for i in range(6):lift[3+i]=3+p[i]
        for i in range(2):lift[9+i]=9+sp[i]
        if any(base[i][j]!=base[lift[i]][lift[j]] for i in range(11) for j in range(11)):
            raise ValueError('not a literal leaf symmetry')
    gs=set(SYMMETRIES)
    for p,sp in gs:
        for q,sq in gs:
            if (tuple(q[p[i]] for i in range(6)),tuple(sq[sp[i]] for i in range(2))) not in gs:
                raise ValueError('permutation subgroup not closed')
    red_X=[(i,j) for i in range(3,11) for j in range(i+1,11) if base[i][j]]
    local_degree=[sum(base[i][j] for j in range(3,11)) for i in range(3,11)]
    floors=tuple(4-h for h in local_degree[:6])
    pools=tuple(tuple(z for z in range(1,8) if z.bit_count()>=floors[i]) if i<6 else (3,5,6) for i in range(8))
    budget_cache={};stats=Counter();stats['row_triples']=56**3;accepted=[]
    for cols in product(*pools):
        row_ranks=tuple(sum(bool(z&(1<<t)) for z in cols) for t in range(3))
        if row_ranks!=(5,5,5):continue
        stats['basic_X']+=1
        word=sum(z<<(3*i) for i,z in enumerate(cols))
        probe=matrix((word,0,0,0,0,0));rs=red_sets(probe)
        y_degrees=tuple(10-1-int(base[2][3+i])-local_degree[i]-cols[i].bit_count() for i in range(8))
        if any(len(rs[i]&rs[j])+low8[y_degrees[i-3]][y_degrees[j-3]]>3 for i,j in red_X):continue
        stats['early_X_pages']+=1
        k=tuple(cols[i].bit_count()-floors[i] for i in range(6))
        if k not in budget_cache:
            b=[]
            for beta in range(6):
                ranks=tuple(2-k[i]-int(i==beta) for i in range(6))
                if min(ranks)<0:continue
                choices=tuple(tuple(z for z in range(4) if z.bit_count()==h) for h in ranks)
                for sc in product(*choices):
                    r0=sum(int(bool(z&1))<<i for i,z in enumerate(sc))
                    r1=sum(int(bool(z&2))<<i for i,z in enumerate(sc))
                    if r0.bit_count()==4 and r1.bit_count()==4:b.append((beta,r0,r1))
            budget_cache[k]=b
        for beta,r0,r1 in budget_cache[k]:
            stats['budget_choices']+=1
            p=matrix((word,beta,r0,r1,0,0));rp=red_sets(p)
            q=(0,6,0,*(3+int(i==beta) for i in range(6)),4,4,2,2,0,0,0)
            if any(len(rp[i]&rp[j])+low6[q[i]][q[j]]>3 for i,j in red_X):continue
            stats['early_budget_pages']+=1
            for t0,t1 in product((3,5,6),repeat=2):
                state=(word,beta,r0,r1,t0,t1)
                m=matrix(state);rr=red_sets(m)
                if any(len(rr[2]&rr[13+t])>3 for t in range(3)):continue
                stats['special_cores']+=1
                qq=(*q[:13],*(4-int(bool(t0&(1<<t)))-int(bool(t1&(1<<t))) for t in range(3)))
                if tuple(len(rr[i])+qq[i] for i in range(16))!=(10,10,9,*([10]*13)):
                    raise ValueError('K/outside degrees mismatch')
                bb=[frozenset(range(16))-rr[i]-{i} for i in range(16)]
                ok=True
                for i in range(16):
                    for j in range(i+1,16):
                        if m[i][j]:bad=len(rr[i]&rr[j])+low6[qq[i]][qq[j]]>3
                        else:bad=len(bb[i]&bb[j])+low6[6-qq[i]][6-qq[j]]>6
                        if bad:ok=False;break
                    if not ok:break
                if ok:accepted.append(state)
        guard()
    accepted.sort();domain=set(accepted)
    if len(domain)!=len(accepted):raise ValueError('duplicate X state')
    reps=[];covered=set()
    for state in accepted:
        if state in covered:continue
        orbit=set(images(state))
        if not orbit<=domain:raise ValueError('state symmetry leaves the domain')
        covered.update(orbit);reps.append((min(orbit),len(orbit)))
    if covered!=domain:raise ValueError('uncovered state')
    reps.sort();per_rep=[];total=Counter();obstructions=[]
    for rid,(state,orbit_size) in enumerate(reps):
        w,beta,rx0,rx1,t0,t1=state
        m16=matrix(state)
        ordinary_row_sizes=tuple(4-int(bool(t0&(1<<t)))-int(bool(t1&(1<<t))) for t in range(3))
        ty_types=set()
        for rows in product(*(subsets(6,h) for h in ordinary_row_sizes)):
            c=tuple(sum(int(bool(rows[t]&(1<<i)))<<t for t in range(3)) for i in range(6))
            if min(c)>0:ty_types.add(tuple(sorted(c)))
        hist=Counter();counts=Counter()
        for y in sorted(ty_types):
            counts['TY_types']+=1
            m0=matrix(state,22,y)
            # Each S row and each T row is already fully known for this
            # individual test. No global degree identity is used here.
            p_sx=[[],[]];p_sy=[[],[]]
            for s in range(2):
                for missing in subsets(6,2):
                    row=63^missing
                    mm=[r.copy() for r in m0]
                    for i in range(6):mm[9+s][16+i]=mm[16+i][9+s]=bool(row&(1<<i))
                    if all(not literal_bad(mm,9+s,13+t)[0] for t in range(3)):p_sx[s].append(row)
                for row in subsets(6,2):
                    mm=[r.copy() for r in m0]
                    for i in range(6):mm[11+s][16+i]=mm[16+i][11+s]=bool(row&(1<<i))
                    if all(not literal_bad(mm,11+s,13+t)[0] for t in range(3)):p_sy[s].append(row)
                p_sx[s].sort();p_sy[s].sort()
            for r0,r1,z0,z1 in product(p_sy[0],p_sy[1],p_sx[0],p_sx[1]):
                if any(4-y[i].bit_count()-int(bool(r0&(1<<i)))-int(bool(r1&(1<<i)))<0 for i in range(6)):continue
                counts['candidate_frames']+=1
                m=matrix(state,22,y,(r0,r1),(z0,z1))
                if any(sum(m[f])!=(9 if f==2 else 10) for f in FIXED):raise ValueError('fixed degrees')
                if any(literal_bad(m,i,j)[0] for k,i in enumerate(FIXED) for j in FIXED[k+1:]):continue
                counts['fixed_spines']+=1
                failed=None
                for i in range(6):
                    failures=[];any_good=False
                    for row in subsets(6,3+int(i==beta)):
                        mm=[r.copy() for r in m]
                        for j in range(6):mm[3+i][16+j]=mm[16+j][3+i]=bool(row&(1<<j))
                        if sum(mm[3+i])!=10:raise ValueError('OX row degree')
                        for f in FIXED:
                            bad,red,pages=literal_bad(mm,3+i,f)
                            if bad:failures.append([row,f,red,pages]);break
                        else:any_good=True
                    if not any_good:
                        failed={'rep':rid,'Y_columns':list(y),'SY_own_rows':[r0,r1],
                                'SX_cross_rows':[z0,z1],'empty_X':i,'failures':failures};break
                if failed is None:raise ValueError('unexcluded frame; no finite proof')
                counts['empty_X_row']+=1;hist[failed['empty_X']]+=1;obstructions.append(failed)
            guard()
        per_rep.append({'rep':rid,'counts':dict(counts),'first_empty_X':dict(hist)});total.update(counts)
    return {'schema':1,'agent':'six-books-1','role':'researcher',
            'scope':'fixed one-nine leaf, E<=108, all nine N(a) vertices global10; finite fixed-spine obstruction, no global max/rootlessness/catalogue',
            'coordinates':['u','v','a',*[f'X{i}' for i in range(6)],'SX0','SX1','SY0','SY1','T0','T1','T2',*[f'Y{i}' for i in range(6)]],
            'outside_pair_controls':{'orders':[6,8],'subset_pair_trials':[4096,65536],'agrees_with_pigeonhole':True},
            'x_counts':dict(stats),'x_domain_count':len(domain),
            'x_domain_sha256':hashlib.sha256(json.dumps(accepted,separators=(',',':')).encode()).hexdigest(),
            'ordinary_symmetries':[[list(p),list(sp)] for p,sp in SYMMETRIES],'subgroup_size':48,
            'orbits':[[list(r),n] for r,n in reps],'Y_counts':dict(total),'per_rep':per_rep,
            'obstructions':sorted(obstructions,key=lambda x:(x['rep'],x['Y_columns'],x['SY_own_rows'],x['SX_cross_rows']))}

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))

def check_record(candidate,correct):
    if canonical(candidate)!=canonical(correct):raise ValueError('entire typed mathematical record differs')

def damage_controls(correct):
    trials=[]
    def add(name,mutate):
        x=copy.deepcopy(correct);mutate(x);trials.append((name,x))
    add('omit obstruction',lambda x:x['obstructions'].pop())
    add('omit blocked row',lambda x:x['obstructions'][0]['failures'].pop())
    add('wrong color',lambda x:x['obstructions'][0]['failures'][0].__setitem__(2,1-x['obstructions'][0]['failures'][0][2]))
    add('wrong page count',lambda x:x['obstructions'][0]['failures'][0].__setitem__(3,0))
    add('wrong row mask',lambda x:x['obstructions'][0]['failures'][0].__setitem__(0,0))
    add('wrong empty vertex',lambda x:x['obstructions'][0].__setitem__('empty_X',5))
    add('zero Y column',lambda x:x['obstructions'][0]['Y_columns'].__setitem__(0,0))
    add('wrong SY rank',lambda x:x['obstructions'][0]['SY_own_rows'].__setitem__(0,0))
    add('invalid symmetry',lambda x:x['ordinary_symmetries'][0][0].__setitem__(0,1))
    add('wrong orbit size',lambda x:x['orbits'][0].__setitem__(1,0))
    add('wrong X digest',lambda x:x.__setitem__('x_domain_sha256','0'*64))
    add('wrong coordinate',lambda x:x['coordinates'].__setitem__(0,'a'))
    add('Boolean for integer',lambda x:x.__setitem__('x_domain_count',True))
    for name,damaged in trials:
        try:check_record(damaged,correct)
        except ValueError:continue
        raise ValueError('accepted deliberate damage: '+name)
    return {'damages_rejected':len(trials),'names':[name for name,_ in trials]}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--record',type=Path,default=Path(__file__).with_name('EXPECTED.json'))
    p.add_argument('--emit',action='store_true');p.add_argument('--damage-controls',action='store_true');args=p.parse_args()
    correct=generate()
    if args.emit:print(json.dumps(correct,sort_keys=True,separators=(',',':')))
    else:
        check_record(json.loads(args.record.read_text()),correct)
        if args.damage_controls:print(json.dumps(damage_controls(correct),sort_keys=True))
        else:print(json.dumps({'X_domain':correct['x_domain_count'],'orbits':len(correct['orbits']),
                               'fixed_frames':len(correct['obstructions']),'unexcluded_frames':0},sort_keys=True))
