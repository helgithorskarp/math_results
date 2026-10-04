"""Fresh integer polynomials and complete bounded coefficient-identity decoding."""
import math
ZERO=(0,0,0)


def p(c):return {ZERO:c}if c else {}


def plus(a,b):
    c=a.copy()
    for e,v in b.items():
        c[e]=c.get(e,0)+v
        if c[e]==0:del c[e]
    return c


def times(a,b):
    c={}
    for e,x in a.items():
        for f,y in b.items():
            g=tuple(e[i]+f[i]for i in range(3));c[g]=c.get(g,0)+x*y
    return {e:v for e,v in c.items()if v}


def scale(a,c):return {e:v*c for e,v in a.items()if v*c}


def prod(polys):
    a=p(1)
    for b in polys:a=times(a,b)
    return a


def degree(a):return tuple(max((e[i]for e in a),default=0)for i in range(3))


def identity(terms):
    """Terms (integer scalar, list of full integer polynomial factors)."""
    bounds=[];ds=[]
    for coefficient,factors in terms:
        bounds.append(abs(coefficient)*math.prod(sum(abs(v)for v in a.values())for a in factors))
        ds.append(tuple(sum(degree(a)[i]for a in factors)for i in range(3)))
    bound=sum(bounds);d=tuple(max((v[i]for v in ds),default=0)for i in range(3))
    width=max(2,(2*bound+1).bit_length());weights=(1,d[0]+1,(d[0]+1)*(d[1]+1))
    maximum=(sum(d[i]*weights[i]for i in range(3))+1)*width
    if maximum>8*4*1024*1024:raise ValueError('fixed4MiB identity guard')
    cache={}
    def encode(a):
        key=tuple(sorted(a.items()))
        if key not in cache:
            cache[key]=sum(v << (width*sum(e[i]*weights[i]for i in range(3)))for e,v in a.items())
        return cache[key]
    residual=sum(c*math.prod(encode(a)for a in factors)for c,factors in terms)
    if residual:raise ValueError('complete coefficient identity failed')
    return {'degrees':list(d),'l1_bound':str(bound),'base_bits':width,
            'encoding_bound_bytes':(maximum+7)//8,'entire_coefficients_zero':True}


def value(a,x):return sum(v*math.prod(x[i]**e[i]for i in range(3))for e,v in a.items())


def original_forms():
    u={(1,0,0):1};v={(0,1,0):1};w={(0,0,1):1}
    d=plus(p(1),u);l=plus(p(2),v);h=plus(l,d);q=plus(p(4),w)
    s=plus(q,scale(h,3));F=plus(h,scale(l,2));ell=plus(scale(F,3),p(1))
    T=plus(plus(scale(q,2),scale(F,6)),p(-1));D=scale(h,3);t0=scale(times(h,l),3)
    gm=[scale(times(plus(q,p(-1)),t0),4),scale(times(D,t0),4),
        scale(prod([D,plus(q,p(-3)),t0]),3),scale(prod([q,D,t0]),6),scale(times(s,d),2)]
    # Whole old-frame matrix from all eight mark-patterns and the full old row.
    old=[[{}for _ in range(5)]for _ in range(5)]
    for ix in range(2):
        for iy in range(2):
            for iz in range(2):
                mult4=plus(q,p(-4 if (ix,iy,iz)in[(0,0,0),(1,1,1)]else 0))
                scores=[p(2),{},scale(D,3-2*(ix+iy+iz)),scale(D,2*(-2*ix+iy+iz)),{}]
                for i in range(5):
                    for j in range(5):old[i][j]=plus(old[i][j],prod([mult4,scores[i],scores[j]]))
    full=[scale(plus(q,p(-1)),-2),scale(D,2),{},{},{}]
    for i in range(5):
        for j in range(5):
            if any(c%4 for c in old[i][j].values()):raise ValueError('old row-pattern clearing')
            old[i][j]={e:c//4 for e,c in old[i][j].items()}
            old[i][j]=plus(old[i][j],times(full[i],full[j]))
    jx=[{},scale(t0,-2),times(plus(q,p(-3)),t0),scale(times(q,t0),2),{}]
    jl=[{},scale(t0,-2),times(plus(q,p(-3)),t0),scale(times(q,t0),-1),times(s,d)]
    Z=[scale(times(plus(q,p(-1)),t0),-2),scale(times(l,t0),12),
       scale(prod([F,plus(q,p(-3)),t0]),-3),scale(prod([q,d,t0]),-6),scale(prod([l,s,d]),-6)]
    forms=[]
    for i in range(5):
        row=[]
        for j in range(5):
            frame=plus(prod([old[i][j],t0,t0,ell]),
                  plus(scale(prod([h,jx[i],jx[j],ell]),3),
                  plus(scale(prod([l,jl[i],jl[j],ell]),6),times(Z[i],Z[j]))))
            numerator=plus(prod([T,gm[i],t0,ell])if i==j else {},scale(frame,-1))
            row.append((numerator,prod([gm[i],t0,ell])))
        forms.append(row)
    return forms,old
