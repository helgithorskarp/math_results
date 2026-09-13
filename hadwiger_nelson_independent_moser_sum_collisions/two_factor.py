"""Complete exceptional unit-contact census for each two-factor coincidence."""
from family import *
from local import f_local

def rotations():
    M=spindle(); D=sorted({sub(a,b) for a,b in product(M,repeat=2) if a!=b})
    U={scale(mul(a,inv(b)),-1) for a,b in product(D,repeat=2) if norm(a)==norm(b)}
    lam=mul(M[2],M[4])
    require({mul(lam,K.conj(m)) for m in M}==set(M),'conjugation symmetry')
    require({K.conj(u) for u in U}==U,'rotation conjugation closure')
    return sorted({min(u,K.conj(u)) for u in U}),len(U)

def cases():
    M=spindle(); Dm=K.differences(M); dm=[b for b in Dm if b!=ZERO]
    Nm={b:norm(b) for b in dm}; U,_=rotations()
    for u in U:
        require(norm(u)==ONE,'non-unit u')
        B=sorted({add(a,mul(u,b)) for a,b in product(M,repeat=2)})
        require(len(B)<49,'missing two-factor collision')
        for x in B+M: K.residue(x) # exact local integrality control
        Db=K.differences(B); db=[a for a in Db if a!=ZERO]
        Na={a:norm(a) for a in db}; shapes={}; stats=Counter(); groups={}
        for an,bn in product(set(Na.values()),set(Nm.values())):
            S=sub(add(an,bn),ONE)
            if S==ZERO: shapes[an,bn]=('trace_zero',None);continue
            va=f_local(an)[0]; vb=f_local(bn)[0]
            require(va%2==vb%2==0,'norm valuation parity')
            vv=f_local(S)[0]-(va+vb)//2
            if vv>=-1: shapes[an,bn]=('trace_ge_minus1',None);continue
            delta=sub(scale(mul(an,bn),4),mul(S,S))
            if sign(delta)<=0: shapes[an,bn]=('nonpositive_delta',None);continue
            ss=scale(delta,F(1,3))
            shapes[an,bn]=('E_root',None) if K.sqrt_real(ss) is not None else ('event',(S,ss,vv))
        ia={a:inv(a) for a in db}; ib={b:inv(b) for b in dm}
        for a,b in product(db,dm):
            kind,extra=shapes[Na[a],Nm[b]];stats[kind]+=1
            if kind!='event':continue
            S,ss,vv=extra; ci=mul(K.conj(ia[a]),ib[b])
            T=scale(mul(S,ci),-1); J=mul(mul(a,K.conj(b)),ci)
            key=(T,J)
            groups.setdefault(key,{'ss':ss,'witness':(a,b),'directions':[],'trace_valuation':vv})['directions'].append((a,b))
        base=set()
        for i,a in enumerate(B):
            for j,b in enumerate(M):
                for ii in range(i+1,len(B)):
                    if norm(sub(a,B[ii]))==ONE:base.add((7*i+j,7*ii+j))
                for jj in range(j+1,7):
                    if norm(sub(b,M[jj]))==ONE:base.add((7*i+j,7*i+jj))
        yield u,B,Db,Dm,base,sorted(groups.items()),dict(stats)

def event_graph(Db,Dm,base,g):
    es=set(base)
    for a,b in g['directions']:
        for i,ii in Db[a]:
            for j,jj in Dm[b]:es.add(tuple(sorted((7*i+j,7*ii+jj))))
    return sorted(es)

def event_phase(key,g):
    T,J=key; a,b=g['witness'];ci=inv(mul(K.conj(a),b))
    v=(scale(T,F(1,2)),scale(mul(ALPHA,ci),F(1,2)))
    ss=g['ss']
    for eps in (-1,1):
        w=(v[0],scale(v[1],eps))
        require(emul(w,econj(w),ss)==(ONE,ZERO),'phase norm')
        require(eadd(esub(emul(w,w,ss),ecscale(w,T)),(J,ZERO))==(ZERO,ZERO),'minimal polynomial')
    return v
