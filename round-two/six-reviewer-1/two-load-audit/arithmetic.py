"""Independent native fraction-field checks of the UFD arithmetic invariant."""
def run():
    from algebra import Rat as R,POLY,Q,tvar,Dvar,avar,uvar,product,ATOMS,require
    f=POLY.to_field()
    g=[Q+4,tvar,Dvar,avar,uvar,avar+uvar,avar+uvar-1,Q+Dvar+3]
    refs=[f(x) for x in g];zs=[R(0),R(1)]+[R(x) for x in g];fs=[f(0),f(1)]+refs
    for i in range(len(g)):
        for e in (1,2):
            zs.append(R(g[(i+1)%len(g)])/R(g[i])**e)
            fs.append(refs[(i+1)%len(g)]/refs[i]**e)
    def compare(z,expected):
        require(f(z.n)/f(product(z.d))==expected,'whole native fraction-field identity')
        for k in z.d:require(bool(z.n.div(ATOMS[k])[1]),'reduced numerator invariant')
    checks=0
    for z,x in zip(zs,fs):compare(z,x);checks+=1
    for z,x in zip(zs,fs):
        for w,y in zip(zs,fs):
            for out,ref in [(z+w,x+y),(z-w,x-y),(z*w,x*y)]:compare(out,ref);checks+=1
            if y:compare(z/w,x/y);checks+=1
        for e in (0,1,2):compare(z**e,f(1) if e==0 else x**e);checks+=1
    return {'exact_whole_fraction_field_identities':checks,'reduced_invariants_checked':True,'variables':5,
            'method':'native SymPy fraction-field GCD arithmetic; no author executable input'}
