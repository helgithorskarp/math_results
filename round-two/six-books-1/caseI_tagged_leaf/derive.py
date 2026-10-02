"""Row-based exact necessary-domain producer for a tagged Case-I leaf.

Standard-library integers only. No external graph corpus or solver.
The ordinary proof and the finite-code correspondence are in PROOF.md.
"""
from itertools import combinations,product
from math import comb
import json,time

START=time.monotonic()
OWN=(40,20)
CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
MINIMUM=(2,2,1,1,1,1)
COORDINATES=['u','v','a',*[f'X{i}' for i in range(6)],'SX0','SX1','SY0','SY1','T0','T1','T2',*[f'Y{i}' for i in range(6)]]
SCOPE='specified one-nine leaf on22, degree multiset9^4,10^18, SY repeated omission; necessary interface exclusion'

def guard():
    if time.monotonic()-START>30:
        raise RuntimeError('unchanged30s guard: incomplete enumeration proves nothing')

def masks(n):
    return tuple(sum(1<<i for i in s) for s in combinations(range(6),n))

def cycle_histograms():
    pairs=tuple(combinations(range(4),2));caps=(2,2,2,2,3,2)
    pairwords=tuple((1<<i)|(1<<j) for i,j in pairs)
    extras=[()]+[(1<<i,15^(1<<j)) for i in range(4) for j in range(4)]
    found=set()
    for extra in extras:
        for values in product(*(range(c+1) for c in caps)):
            h=[0]*16
            for w in extra:h[w]+=1
            for w,n in zip(pairwords,values):h[w]+=n
            if sum(h)!=12:continue
            if any(sum(n for w,n in enumerate(h) if w&(1<<i))!=6 for i in range(4)):continue
            if any(sum(n for w,n in enumerate(h) if w&(1<<i) and w&(1<<j))>cap
                   for (i,j),cap in zip(pairs,caps)):continue
            # At root a, p0=u is blue exactly to OY. The fixed leaf's
            # SX red sets have no common point in OX (bit0 absent).
            if sum(n for w,n in enumerate(h) if not w&1 and not w&2 and not w&8):continue
            found.add(tuple(h))
    answer=sorted(found)
    if len(answer)!=2:raise ValueError('cited Case-I histogram reduction not recovered')
    for h in answer:
        if sum(n for w,n in enumerate(h) if not w&1 and not w&4)!=2:
            raise ValueError('T0 OX red count not recovered')
        if any(n and not w&1 and not w&4 and (not w&2 or not w&8) for w,n in enumerate(h)):
            raise ValueError('T0 OX red row incompatible with fixed special sets')
    return answer

def known_rows(c,s):
    r=[0]*16
    def edge(i,j):r[i]|=1<<j;r[j]|=1<<i
    for z in (1,2,*range(3,11)):edge(0,z)
    for z in (2,11,12):edge(1,z)
    for z in range(9,16):edge(2,z)
    for i,j in CYCLE:edge(3+i,3+j)
    for j in range(2):
        for i in range(6):
            if OWN[j]&(1<<i):edge(9+j,3+i)
            if s[j]&(1<<i):edge(11+j,3+i)
    for i in range(8):
        for t in range(3):
            if c[i]&(1<<t):edge(3+i,13+t)
    for j in range(2):
        for t in (1,2):edge(11+j,13+t)
    return r

def necessary(lows,c,s,beta):
    r=known_rows(c,s)
    d=(10,10,9,*([10]*8),10-lows[2],10-lows[3],9,10-lows[0],10-lows[1])
    q=(0,6,0,*(3+b for b in beta),4,4,2,2,4,2,2)
    if tuple(r[i].bit_count()+q[i] for i in range(16))!=d:
        raise ValueError('actual tagged degree budget correspondence')
    if sum(beta)!=2+sum(lows):raise ValueError('edge budget correspondence')
    for i in range(16):
        for j in range(i+1,16):
            # For a blue pair on22, cB=20-di-dj+cR.
            lower=(r[i]&r[j]).bit_count()+max(0,q[i]+q[j]-6)
            cap=3 if r[i]&(1<<j) else d[i]+d[j]-14
            if lower>cap:return False
    return True

def interfaces():
    states=[];placements=[]
    for lows in product(range(2),repeat=4):
        if sum(lows)>2:continue
        accepted=0
        for tx1 in masks(4-lows[0]):
            for tx2 in masks(4-lows[1]):
                c=tuple(int(i in (0,1))+2*int(bool(tx1&(1<<i)))+4*int(bool(tx2&(1<<i))) for i in range(6))+(5,3)
                k=tuple(c[i].bit_count()-MINIMUM[i] for i in range(6))
                if min(k)<0:continue
                if sum(k)!=2-lows[0]-lows[1]:raise ValueError('T-row defect budget')
                # Necessary whole-Y pigeonhole bounds on actual red
                # C6 and SX--own-OX spines; proved in PROOF.md.
                if any((c[i]&c[j]).bit_count()>min(2,k[i]+k[j]) for i,j in CYCLE):continue
                if any((c[6+s]&c[i]).bit_count()>min(2,1+k[i])
                       for s in range(2) for i in range(6) if OWN[s]&(1<<i)):continue
                for s0 in masks(4-lows[2]):
                    for s1 in masks(4-lows[3]):
                        beta=tuple(2-k[i]-int(bool(s0&(1<<i)))-int(bool(s1&(1<<i))) for i in range(6))
                        if min(beta)<0 or max(beta)>2:continue
                        if necessary(lows,c,(s0,s1),beta):
                            states.append({'low_T1_T2_SY0_SY1':list(lows),'T_columns':list(c),
                                           'SY_cross_OX':[s0,s1],'beta':list(beta)})
                            accepted+=1
                guard()
        placements.append({'low_T1_T2_SY0_SY1':list(lows),'OY_low_count':2-sum(lows),
                           'labeled_OY_tag_choices':comb(6,2-sum(lows)), 'surviving_X_interfaces':accepted})
    states.sort(key=lambda x:(x['T_columns'],x['SY_cross_OX']))
    return states,placements

def ordinary_finish(states):
    frames=0
    for state in states:
        lows=state['low_T1_T2_SY0_SY1'];c=state['T_columns'];s=state['SY_cross_OX']
        if lows!=[0,0,1,1]:raise ValueError('additional low placement: no claimed exclusion')
        if s[0]&s[1] or (s[0]|s[1])!=63:raise ValueError('SY cross partition')
        tx=tuple(sum(bool(c[i]&(1<<t))<<i for i in range(6)) for t in (1,2))
        if any(x.bit_count()!=4 for x in tx) or (tx[0]&tx[1]).bit_count()!=2:
            raise ValueError('ordinary T-row intersection')
        if any((x&z).bit_count()!=2 for x in tx for z in s):raise ValueError('red SY--T saturation')
        r=known_rows(c,s)
        if (r[11]&r[12]).bit_count()!=4:raise ValueError('blue SY-pair base count')
        for sy0 in masks(2):
            for sy1 in masks(2):
                if sy0&sy1:continue
                free=63^(sy0|sy1)
                if free.bit_count()!=2:raise ValueError('ordinary Y complement')
                # Red SY--T spines force both ordinary T rows to this
                # free two-set. Unknown ordinary X--Y/Y--Y edges do not
                # touch either T endpoint and cannot repair its pages.
                cr=(r[14]&r[15]).bit_count()+free.bit_count()
                degrees=(r[14].bit_count()+free.bit_count(),r[15].bit_count()+free.bit_count())
                cb=20-sum(degrees)+cr
                if (cr,cb,degrees)!=(7,7,(10,10)):raise ValueError('literal T-pair contradiction')
                frames+=1
    return {'disjoint_SY_own_row_choices':90,'T_pair_frames':frames,
            'T_endpoint_degrees':[10,10],'common_red_pages':7,'common_blue_pages':7,'blue_cap':6}

def outside_controls():
    red={};blue={}
    for i in range(64):
        for j in range(64):
            key=(i.bit_count(),j.bit_count())
            red[key]=min(red.get(key,7),(i&j).bit_count())
            blue[key]=min(blue.get(key,7),((63^i)&(63^j)).bit_count())
    if any(red[i,j]!=max(0,i+j-6) or blue[i,j]!=max(0,6-i-j) for i,j in red):
        raise ValueError('outside subset pigeonhole control')
    return {'order':6,'subset_pair_trials':4096,'both_colored_minima_agree':True}

def record():
    hist=cycle_histograms();states,placements=interfaces()
    if sum(p['labeled_OY_tag_choices'] for p in placements)!=45:raise ValueError('actual low-tag coverage')
    return {'schema':1,'agent':'six-books-1','role':'researcher','scope':SCOPE,'coordinates':COORDINATES,
            'recovered_cycle_histograms':[list(h) for h in hist],'Tstar_ordinary_X_red':[0,1],
            'actual_low_placements':placements,'X_interfaces':states,
            'ordinary_finish_controls':ordinary_finish(states),'outside_pair_controls':outside_controls()}

if __name__=='__main__':
    print(json.dumps(record(),sort_keys=True,separators=(',',':')))
