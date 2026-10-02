"""Independent column/Boolean checker. Imports no producer or proof corpus."""
from itertools import combinations,product
from math import comb
from pathlib import Path
import argparse,copy,json,time

START=time.monotonic()
COORDINATES=['u','v','a',*[f'X{i}' for i in range(6)],'SX0','SX1','SY0','SY1','T0','T1','T2',*[f'Y{i}' for i in range(6)]]
SCOPE='specified one-nine leaf on22, degree multiset9^4,10^18, SY repeated omission; necessary interface exclusion'
K=tuple(range(16));CORE=tuple(i for i in K if i not in (11,12))

def guard():
    if time.monotonic()-START>30:
        raise RuntimeError('unchanged30s guard: incomplete check proves nothing')

def base(columns,sycolumns):
    a=[[False]*22 for _ in range(22)]
    def red(i,j):a[i][j]=True;a[j][i]=True
    for j in (1,2,3,4,5,6,7,8,9,10):red(0,j)
    for j in (0,2,11,12,16,17,18,19,20,21):red(1,j)
    for j in (0,1,9,10,11,12,13,14,15):red(2,j)
    for i,j in ((3,7),(7,6),(6,4),(4,5),(5,8),(8,3)):red(i,j)
    for j in (6,8):red(9,j)
    for j in (5,7):red(10,j)
    for i,col in enumerate(columns):
        for t in range(3):
            if col&(1<<t):red(3+i,13+t)
    for i,col in enumerate(sycolumns):
        for s in range(2):
            if col&(1<<s):red(3+i,11+s)
    for s in (11,12):
        for t in (14,15):red(s,t)
    return a

def colored_count(a,i,j,red,universe):
    return sum(k!=i and k!=j and a[i][k]==red and a[j][k]==red for k in universe)

def histograms():
    pairs=tuple(combinations(range(4),2));capacity=(2,2,2,2,3,2)
    words=sorted(range(16),key=lambda w:(-w.bit_count(),w));found=set()
    def visit(pos,left,margins,caps,cost,h):
        if min(margins)<0 or max(margins)>left or min(caps)<0 or cost>1:return
        if pos==16:
            if left==0 and not any(margins):found.add(tuple(h))
            return
        w=words[pos];inc=tuple(int(bool(w&(1<<i))) for i in range(4))
        pi=tuple(inc[i]*inc[j] for i,j in pairs)
        upper=min([left]+[margins[i] for i in range(4) if inc[i]]+[caps[k] for k in range(6) if pi[k]])
        for n in range(upper+1):
            m=tuple(margins[i]-n*inc[i] for i in range(4));rows=left-n
            if any(m[i] and not any(z&(1<<i) for z in words[pos+1:]) for i in range(4)):continue
            h[w]=n
            visit(pos+1,rows,m,tuple(caps[k]-n*pi[k] for k in range(6)),
                  cost+n*((w.bit_count()-1)*(w.bit_count()-2)//2),h)
        h[w]=0
    visit(0,12,(6,6,6,6),capacity,0,[0]*16)
    case=[]
    for h in found:
        rows=[w for w,n in enumerate(h) for _ in range(n)]
        ordinary_x=[w for w in rows if not w&1]
        if any(not w&2 and not w&8 for w in ordinary_x):continue
        if len(ordinary_x)!=6:raise ValueError('ordinary X partition size')
        red_t=[w for w in ordinary_x if not w&4]
        if len(red_t)!=2 or any(not w&2 or not w&8 for w in red_t):raise ValueError('T0 ordinary X reduction')
        # Literal22 selected-cycle control: root0, J1..9, outside10..21.
        a=[[False]*22 for _ in range(22)]
        def edge(i,j):a[i][j]=True;a[j][i]=True
        for j in range(1,10):edge(0,j)
        for i,j in ((1,2),(2,3),(3,4),(4,1),(1,5),(2,6),(4,7)):edge(i,j)
        for j,w in enumerate(rows,10):
            for p in range(4):
                if not w&(1<<p):edge(p+1,j)
        if tuple(sum(a[i]) for i in range(1,5))!=(10,10,9,10):raise ValueError('literal cycle global degrees')
        if any(colored_count(a,i+1,j+1,a[i+1][j+1],range(22))>(3 if a[i+1][j+1] else 6) for i,j in pairs):
            raise ValueError('literal selected cycle pages')
        case.append(list(h))
    return sorted(case)

def enumerate_columns():
    # Fresh two-bit column words, bucketed only by actual SY row sizes.
    sybuckets={}
    for cols in product(range(4),repeat=6):
        sizes=tuple(sum(bool(c&(1<<s)) for c in cols) for s in range(2))
        if min(sizes)>=3 and max(sizes)<=4:sybuckets.setdefault(sizes,[]).append(cols)
    states=[];placements=[]
    for lows in product(range(2),repeat=4):
        if sum(lows)>2:continue
        d=(10,10,9,*([10]*8),10-lows[2],10-lows[3],9,10-lows[0],10-lows[1])
        accepted=0
        for ordinary in product((1,3,5,7),(1,3,5,7),(2,4,6),(2,4,6),(2,4,6),(2,4,6)):
            if tuple(sum(bool(c&(1<<t)) for c in ordinary) for t in (1,2))!=(4-lows[0],4-lows[1]):continue
            columns=ordinary+(5,3);a=base(columns,(0,)*6)
            # Direct common-blue pages in the exactly known B(v)=X union T.
            if any(colored_count(a,1,i,False,(*range(3,11),13,14,15))>6 for i in range(3,9)):continue
            qy={i:10-sum(a[i][j] for j in CORE) for i in range(3,11)}
            if any(colored_count(a,i,j,True,CORE)+max(0,qy[i]+qy[j]-8)>3
                   for i in range(3,11) for j in range(i+1,11) if a[i][j]):continue
            for sycols in sybuckets[(4-lows[2],4-lows[3])]:
                a=base(columns,sycols)
                q=tuple(d[i]-sum(a[i][j] for j in K) for i in K)
                if min(q)<0 or max(q)>6:continue
                failed=False
                for i in K:
                    for j in range(i+1,16):
                        red=a[i][j]
                        known=colored_count(a,i,j,red,K)
                        lower=max(0,q[i]+q[j]-6) if red else max(0,6-q[i]-q[j])
                        if known+lower>(3 if red else 6):failed=True;break
                    if failed:break
                if failed:continue
                beta=[q[i]-3 for i in range(3,9)]
                if min(beta)<0 or max(beta)>2 or sum(beta)!=2+sum(lows):raise ValueError('derived actual Ba degree budgets')
                if (q[0],q[1],q[2],q[9],q[10],q[11],q[12],q[13],q[14],q[15])!=(0,6,0,4,4,2,2,4,2,2):
                    raise ValueError('derived fixed outside degrees')
                s=[sum(bool(c&(1<<j))<<i for i,c in enumerate(sycols)) for j in range(2)]
                states.append({'low_T1_T2_SY0_SY1':list(lows),'T_columns':list(columns),'SY_cross_OX':s,'beta':beta})
                accepted+=1
            guard()
        placements.append({'low_T1_T2_SY0_SY1':list(lows),'OY_low_count':2-sum(lows),
                           'labeled_OY_tag_choices':comb(6,2-sum(lows)),'surviving_X_interfaces':accepted})
    states.sort(key=lambda x:(x['T_columns'],x['SY_cross_OX']))
    return states,placements

def finish(states):
    frames=0
    for state in states:
        c=state['T_columns'];s=state['SY_cross_OX']
        if state['low_T1_T2_SY0_SY1']!=[0,0,1,1]:raise ValueError('unexcluded low-tag placement')
        if s[0]&s[1] or (s[0]|s[1])!=63:raise ValueError('SY ordinary X partition')
        sycols=tuple(int(bool(s[0]&(1<<i)))+2*int(bool(s[1]&(1<<i))) for i in range(6))
        a=base(c,sycols)
        if colored_count(a,11,12,True,K)!=4:raise ValueError('SY common-red base')
        for y0 in combinations(range(16,22),2):
            for y1 in combinations(range(16,22),2):
                if set(y0)&set(y1):continue
                b=[row[:] for row in a]
                for sy,ys in ((11,y0),(12,y1)):
                    for y in ys:b[sy][y]=True;b[y][sy]=True
                free=set(range(16,22))-set(y0)-set(y1)
                for t in (14,15):
                    # Each red SY--T spine already has exactly three
                    # known pages. Its ordinary-Y row avoids both sets.
                    if any(colored_count(b,sy,t,True,K)!=3 for sy in (11,12)):
                        raise ValueError('red SY--T base saturation')
                    for y in free:b[t][y]=True;b[y][t]=True
                if (sum(b[14]),sum(b[15]))!=(10,10):raise ValueError('literal T endpoint degrees')
                if colored_count(b,14,15,True,range(22))!=7 or colored_count(b,14,15,False,range(22))!=7:
                    raise ValueError('literal seven-page blue T spine')
                frames+=1
    return {'disjoint_SY_own_row_choices':90,'T_pair_frames':frames,'T_endpoint_degrees':[10,10],
            'common_red_pages':7,'common_blue_pages':7,'blue_cap':6}

def outside_controls():
    buckets={}
    for x in product((False,True),repeat=6):
        for y in product((False,True),repeat=6):
            key=(sum(x),sum(y));cr=sum(a and b for a,b in zip(x,y));cb=sum(not a and not b for a,b in zip(x,y))
            buckets.setdefault(key,[]).append((cr,cb))
    for (i,j),values in buckets.items():
        if min(v[0] for v in values)!=max(0,i+j-6) or min(v[1] for v in values)!=max(0,6-i-j):
            raise ValueError('literal outside subset pair minima')
    return {'order':6,'subset_pair_trials':4096,'both_colored_minima_agree':True}

def regenerate():
    hist=histograms();states,placements=enumerate_columns()
    if len(hist)!=2 or sum(p['labeled_OY_tag_choices'] for p in placements)!=45:
        raise ValueError('actual histogram/tag coverage')
    return {'schema':1,'agent':'six-books-1','role':'researcher','scope':SCOPE,'coordinates':COORDINATES,
            'recovered_cycle_histograms':hist,'Tstar_ordinary_X_red':[0,1],
            'actual_low_placements':placements,'X_interfaces':states,
            'ordinary_finish_controls':finish(states),'outside_pair_controls':outside_controls()}

def strict_match(actual,expected):
    if type(actual) is not type(expected):raise ValueError('exact type mismatch')
    if isinstance(expected,dict):
        if actual.keys()!=expected.keys():raise ValueError('record field mismatch')
        for k in expected:strict_match(actual[k],expected[k])
    elif isinstance(expected,list):
        if len(actual)!=len(expected):raise ValueError('record length mismatch')
        for x,y in zip(actual,expected):strict_match(x,y)
    elif actual!=expected:raise ValueError('record value mismatch')

def unique_pairs(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('duplicate JSON key')
        d[k]=v
    return d

def damage_controls(expected):
    changes=[]
    def add(change):
        bad=copy.deepcopy(expected);change(bad);changes.append(bad)
    add(lambda b:b.pop('X_interfaces'))
    add(lambda b:b.update({'unused_field':0}))
    add(lambda b:b.update({'schema':True}))
    add(lambda b:b['coordinates'].__setitem__(0,'v'))
    add(lambda b:b['Tstar_ordinary_X_red'].__setitem__(0,2))
    add(lambda b:b['X_interfaces'].pop())
    add(lambda b:b['X_interfaces'].append(copy.deepcopy(b['X_interfaces'][0])))
    add(lambda b:b['X_interfaces'][0]['beta'].__setitem__(0,2))
    add(lambda b:b['X_interfaces'][0]['T_columns'].__setitem__(0,7))
    add(lambda b:b['X_interfaces'][0]['SY_cross_OX'].__setitem__(0,63))
    add(lambda b:b['actual_low_placements'][0].update({'labeled_OY_tag_choices':14}))
    add(lambda b:b['recovered_cycle_histograms'][0].__setitem__(0,1))
    add(lambda b:b['ordinary_finish_controls'].update({'common_blue_pages':6}))
    for bad in changes:
        try:strict_match(bad,expected)
        except ValueError:continue
        raise ValueError('damage accepted')
    try:json.loads('{"schema":1,"schema":1}',object_pairs_hook=unique_pairs)
    except ValueError:pass
    else:raise ValueError('duplicate key damage accepted')
    return len(changes)+1

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--emit',action='store_true');p.add_argument('--damage-controls',action='store_true');p.add_argument('certificate',nargs='?',default='EXPECTED.json')
    args=p.parse_args();expected=regenerate()
    if args.emit:print(json.dumps(expected,sort_keys=True,separators=(',',':')))
    else:
        actual=json.loads(Path(args.certificate).read_text(),object_pairs_hook=unique_pairs)
        strict_match(actual,expected)
        if args.damage_controls:print(json.dumps({'verified':True,'damages_rejected':damage_controls(expected)}))
        else:print(json.dumps({'verified':True,'X_interfaces':len(expected['X_interfaces'])}))
