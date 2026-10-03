"""Separate literal finite-field graph checker definitions; no proposal imports."""
import hashlib,json
P=617
def need(test,reason):
    if not test:raise ValueError(reason)
def digest(value):
    return hashlib.sha256((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def graph():
    need(all(P%d for d in range(2,25)),'prime field')
    squares={x*x%P for x in range(1,P)};sq=sorted(squares);ns=sorted(set(range(1,P))-squares)
    supports=[]
    for d in range(1,P):
        points=[(1+j*d)%P for j in range(1,7)]
        if 0 not in points and not set(points).intersection(squares):supports.append([d,sorted(points)])
    V={x for d,points in supports for x in points};inverse={pow(x,-1,P) for x in V};D=V|inverse
    need(len(supports)==6 and len(V)==33 and len(D)==66 and not V.intersection(inverse),'literal directed supports')
    A={q:{q*d%P for d in D} for q in sq}
    need(all(len(A[q])==66 and A[q]<=set(ns) for q in sq),'actual bipartite row domains')
    columns={t:{q for q in sq if t in A[q]} for t in ns}
    need(all(len(columns[t])==66 for t in ns),'actual column degrees')
    return supports,V,D,sq,ns,A,columns
