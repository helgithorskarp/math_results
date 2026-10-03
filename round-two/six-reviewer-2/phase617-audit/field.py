"""Independent literal-square model; all roots are actual independent positions."""
from itertools import product
P=617
ROOTS=(0,1,4)
OPTIONS=tuple((j,b) for j in range(3) for b in range(2))

def require(ok,why):
    if not ok:raise ValueError(why)

def character():
    require(all(P%d for d in range(2,25)), 'prime617')
    sq={r*r%P for r in range(1,P)}
    require(len(sq)==308 and 0 not in sq, 'whole nonzero square class')
    return tuple(None if r==0 else int(r not in sq) for r in range(P))

def inputs(N,L=None):
    L=character() if L is None else L
    return tuple(None if n%P in ROOTS else tuple(L[(n-r)%P] for r in ROOTS) for n in range(N))

def tables():
    return tuple(sum((((k>>(2-j))&1)^b)<<k for k in range(8))for j,b in OPTIONS)

def progressions(N):
    for e in range(6,N):
        for d in range(1,e//6+1):yield e-6*d,d

def root_positions(N):return tuple(n for n in range(N) if n%P in ROOTS)

def phase_masks():
    """Base-six index uses phase0 as the least significant digit."""
    count=6**6
    membership=[]
    for s in range(6):
        step=6**s;units=[]
        for j in range(6):
            x=0
            for start in range(j*step,count,6*step):x|=((1<<step)-1)<<start
            units.append(x)
        membership.append(tuple(sum((units[j] for j in range(6)if m>>j&1),0)for m in range(64)))
    return membership

def decode_index(i):return tuple((i//6**s)%6 for s in range(6))
