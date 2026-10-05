"""Fresh four-mark physical forms; own earlier exact identity engine is credited.

The polynomial arithmetic and bounded integer identity reader are reused from
six-reviewer-1/three-mark-audit, source61516022faa5df5f379af89637b7d3c74f410d10.
No three-mark matrix, certificate or mathematical verdict is an input here.
"""
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
    """Read every coefficient of a cleared identity using an explicit carry bound."""
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
    # d=1+u, l=2+v, h=l+d, q=8+w, all three variables nonnegative.
    u={(1,0,0):1};v={(0,1,0):1};w={(0,0,1):1}
    d=plus(p(1),u);l=plus(p(2),v);h=plus(l,d);q=plus(p(8),w)
    s=plus(q,scale(h,3));F=plus(h,scale(l,3));ell=plus(scale(F,3),p(1))
    T=plus(plus(scale(q,2),scale(F,6)),p(-1));D=scale(h,3);t0=scale(times(h,l),3)
    # Metric in the physical E,U,R,Hc, Bbar_y+Bbar_z+Bbar_w basis, times t0.
    gm=[scale(times(plus(q,p(-1)),t0),4),scale(times(D,t0),4),
        scale(prod([D,plus(q,p(-4)),t0]),4),scale(prod([q,D,t0]),12),scale(times(s,d),3)]
    # Reconstruct every old-row score product from all16 four-bit patterns.
    # The two corner counts omit respectively the empty and the full old row;
    # the actual full old row is added separately below. The empty row is kept
    # in the common-vector term Z Z^t/ell of the COMPLETE aggregate frame.
    old=[[{}for _ in range(5)]for _ in range(5)]
    for mask in range(16):
        ix,iy,iz,iw=[(mask>>g)&1 for g in range(4)]
        mult8=plus(q,p(-8 if mask in [0,15]else 0))
        scores=[p(2),{},scale(D,4-2*(ix+iy+iz+iw)),
                scale(D,2*(-3*ix+iy+iz+iw)),{}]
        for i in range(5):
            for j in range(5):old[i][j]=plus(old[i][j],prod([mult8,scores[i],scores[j]]))
    full=[scale(plus(q,p(-1)),-2),scale(D,2),{},{},{}]
    for i in range(5):
        for j in range(5):
            if any(c%8 for c in old[i][j].values()):raise ValueError('old16-pattern clearing')
            old[i][j]={e:c//8 for e,c in old[i][j].items()}
            old[i][j]=plus(old[i][j],times(full[i],full[j]))
    # Marked physical scores (each repeated3h or9l) and complete common row.
    jx=[{},scale(t0,-2),times(plus(q,p(-4)),t0),scale(times(q,t0),3),{}]
    jl=[{},scale(t0,-2),times(plus(q,p(-4)),t0),scale(times(q,t0),-1),times(s,d)]
    Z=[scale(times(plus(q,p(-1)),t0),-2),scale(times(l,t0),18),
       scale(prod([F,plus(q,p(-4)),t0]),-3),scale(prod([q,d,t0]),-9),scale(prod([l,s,d]),-9)]
    forms=[]
    for i in range(5):
        row=[]
        for j in range(5):
            frame=plus(prod([old[i][j],t0,t0,ell]),
                  plus(scale(prod([h,jx[i],jx[j],ell]),3),
                  plus(scale(prod([l,jl[i],jl[j],ell]),9),times(Z[i],Z[j]))))
            numerator=plus(prod([T,gm[i],t0,ell])if i==j else {},scale(frame,-1))
            row.append((numerator,prod([gm[i],t0,ell])))
        forms.append(row)
    return forms,old
