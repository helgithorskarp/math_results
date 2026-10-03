"""Complete labelled Q-role generation and explicit free-label orbits."""
from itertools import combinations,product

def record(rank,t0,t2,eps):
    t=[set(t0),{4,5},set(t2)];sy=[{0,1},{2,3}]
    return {'t2rank':rank,'TQ':[sorted(a) for a in t],'SYQ':[sorted(a) for a in sy],
        'epsilon':list(eps),'h':[4+eps[j]-sum(j in a for a in t+sy) for j in range(6)]}

def catalog():
    out=[]
    for name,t0,t2,ex in (
        ('I-U',(0,4,5),(1,2,3),(4,5)),('I-V',(0,1,4),(1,2,3),(1,4)),
        ('II-a4',(0,4,5),(1,2,3,4),(4,)),('II-a5',(0,4,5),(1,2,3,4),(5,)),
        ('II-b1',(0,1,4),(1,2,3,4),(1,)),('II-b4',(0,1,4),(1,2,3,4),(4,)),
        ('II-c1',(0,1,5),(1,2,3,4),(1,)),('II-c4',(0,1,5),(1,2,3,4),(4,)),
        ('II-c5',(0,1,5),(1,2,3,4),(5,))):
        c=record(len(t2),t0,t2,[int(i in ex) for i in range(6)]);c['name']=name;out.append(c)
    return out

def raw_profiles():
    return sorted(tuple(int(k==i)+int(k==j) for k in range(11)) for i in range(11) for j in range(i,11))

def generate():
    out=[]
    for rank in (3,4):
        for t0 in combinations((0,1,4,5),3):
            for t2 in combinations(range(6),rank):
                if not {2,3}<=set(t2) or len(set(t2)&{0,1})>1:continue
                if len(set(t2)&{4,5})>rank-3:continue
                if set(t0)|set(t2)|{4,5}!=set(range(6)):continue
                for eps in product(range(3),repeat=6):
                    if sum(eps)!=5-rank:continue
                    if any(eps[j]>int(j in t0)+int(j in t2)+int(j in {4,5})-1 for j in range(6)):continue
                    out.append(record(rank,t0,t2,eps))
    return out

def key(c):return c['t2rank'],tuple(map(tuple,c['TQ'])),tuple(c['epsilon'])
PERMUTATIONS=tuple(tuple(j^f[j//2] for j in range(6)) for f in product((0,1),repeat=3))

def transport(c,p):
    ep=[0]*6
    for i,e in enumerate(c['epsilon']):ep[p[i]]=e
    return record(c['t2rank'],[p[i] for i in c['TQ'][0]],[p[i] for i in c['TQ'][2]],ep)

def orbit(c):return min(key(transport(c,p)) for p in PERMUTATIONS)
