"""Small arithmetic/metric controls outside the enumerated parameter inventory."""
from geometry import *
import random

def run(path):
    G=Geometry(path);rng=random.Random(490509);pairs=0
    # Genuinely quadratic real extensions, rational translations,
    # and deliberately inserted zero/non-unit/unit distances.
    for r in (2,5,13,17,19,29):
        ss=scale(ONE,r)
        require(K.sqrt_real(ss) is None,'control radicand')
        pp=[]
        for k in range(10):
            p=tuple(tuple(F(rng.randrange(-7,8),rng.choice((1,3,5))) for _ in range(4)) for _ in range(2))
            pp.extend((p,eadd(p,(ONE,ZERO))))
        es=G.graph(pp,ss)
        slow=[]
        for i,j in combinations(range(len(pp)),2):
            d=esub(pp[i],pp[j]);n=emul(d,econj(d),ss)
            if n==(ONE,ZERO):slow.append((i,j))
        require(slow==es,'rational arithmetic metric control')
        pairs+=len(pp)*(len(pp)-1)//2
    # Native range guards supplement the Python guard; no overflowing value
    # is sent to a squaring operation.
    a=(ct.c_int64*8)(*([0]*8));out=(ct.c_int*2)()
    for name in ('contacts','real_contacts'):
        f=getattr(G.lib,name)
        require(f(344,1,1,2,0,a,out)==-1,'native n guard')
        require(f(1,10**9+1,1,2,0,a,out)==-1,'native denominator guard')
        a[0]=10**9+1;require(f(1,1,1,2,0,a,out)==-2,'native numerator guard');a[0]=0
    # Exact valuation and odd part at a range of positive and negative depths.
    from local import f_local
    for e in range(-20,21):
        for odd in (1,3,5,7,9,11,13,15):
            x=scale(ONE,F(2)**e*odd)
            require(f_local(x)==(e,odd%8),'local rational control')
    return {'independent_fraction_metric_pairs':pairs,'native_guard_rejections':6,'local_valuation_controls':41*8}
if __name__=='__main__':
    print(json.dumps(run(sys.argv[1]),sort_keys=True,indent=2))
