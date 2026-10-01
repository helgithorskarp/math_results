#!/usr/bin/env python3
"""Exact replay and complete sector identities for distinct marked pendants.

Python3.11+ standard library; credited verify.py/verify_two_marks.py helpers.
Literal family order is at most80; the unbounded proof is ALL_MARKS.md.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
from hashlib import sha256
import verify as base
import verify_two_marks as two


def det3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def sectors(q,r):
    base.require(type(q) is int and type(r) is int and r>=2 and ((q==r==2) or (q>=4 and q>=r+1)), 'valid frame parameter domain')
    n=2*q+2*r;g=F(q-1);z=F(q-r,r)
    b=F(r*(q-r-2),(r+1)*q*(r-1))
    eta=F(r*q,r+1)+F(2*r,(r+1)**2)-b*b*F(q*(r-1),r)
    base.require(eta>0,'positive simplex residual')
    metric=[g,F(1),z];h=[F(0),F(1),z];k=[g,F(r-1),r*z]
    f0=[[F((q+1)*g),g,F(0)],[g,F(1),F(0)],[F(0),F(0),2*z]]
    frame=[[f0[i][j]+r*h[i]*h[j]+k[i]*k[j]/(r+1) for j in range(3)] for i in range(3)]
    cap=[[(n-1)*metric[i]*int(i==j)-frame[i][j] for j in range(3)] for i in range(3)]
    first=cap[0][0]/g;second=(cap[0][0]*cap[1][1]-cap[0][1]**2)/g
    third=det3(cap)/(g*z) if z else None
    base.require(first==F(r*q+2*r*r-1,r+1),'first symmetric identity')
    base.require(second==F(2*r*(r+1)*q*q+(4*r**3+r*r-5*r-2)*q+2*r**3-2*r*r-r+3,(r+1)**2),'second symmetric identity')
    expected=F(2*(r-1)*(2*r+1)*q*q+(12*r**3-12*r*r-7*r+9)*q+8*r**4-8*r**3-12*r*r+21*r-9,r+1)
    base.require(third==expected or (q==r==2 and third is None), 'full symmetric determinant identity')
    base.require(base.psd_rank(cap)==(3 if z else 2), 'symmetric frame margin1')
    e=F(r,r-1)*eta
    anti=[[F(q)*(n-1-q-2)-b*b*q*q,-b*q*e],[-b*q*e,(n-1)*e-e*e]]
    base.require(base.psd_rank(anti)==2,'antisymmetric frame margin1')
    base.require((3+2*(r-1)+(q-r-1)+(q-2) if z else 2+2)==2*q+r-2, 'complete frame dimension')
    return {'q':q,'r':r,'b':str(b),'eta':str(eta),'sym_minors':[str(v) for v in [first,second,third] if v is not None], 'symmetric_dimension':3 if z else 2,'scaled_seed_margin':1}


def build(n,r,mark_positions=None):
    base.require(type(n) is int and type(r) is int and 2<=n<=6 and 2<=r<=n,'literal n2..6,r2..n')
    q=1<<(n-1);s=q+1;N=2*q+2*r;full=2*q-1
    base.require(N<=80, 'literal family order guard80')
    positions=list(range(r)) if mark_positions is None else list(mark_positions)
    base.require(len(positions)==r and len(set(positions))==r and all(type(i) is int and 0<=i<n for i in positions), 'distinct valid marked coordinates')
    family=list(range(2*q));leaves=[1<<(n+i) for i in range(r)];marks=[1<<i for i in positions]
    for leaf,mark in zip(leaves,marks):family += [leaf,leaf|mark]
    old=list(range(1,2*q));m=len(old)
    c0=[[F((q+1)*int(u==v)+(q-1)*int(u^v==full)-1) for v in old] for u in old]
    base.require(base.psd_rank(c0)==m,'modified cube is PD')
    hs=[[F(-bool(u&mark)) for u in old] for mark in marks]
    k=[1+sum(h[j] for h in hs) for j in range(m)]
    mean=[sum(h[j] for h in hs)/r for j in range(m)]
    one=[F(1)]*m;full_co=[F(u==full) for u in old]
    h0=[-(u+v)/2 for u,v in zip(one,full_co)]
    gperp=[u+v for u,v in zip(one,h0)];zco=[u-v for u,v in zip(mean,h0)]
    metric=[F(q-1),F(1),F(q-r,r)]
    coords=[gperp,h0,zco]
    actual=two.gram(c0,coords,[[F(0)]*3 for _ in range(3)])
    base.require(actual==[[metric[i]*int(i==j) for j in range(3)] for i in range(3)], 'literal symmetric orthogonal decomposition')
    base.require(two.matvec(c0,h0)==[u+2*v for u,v in zip(one,h0)], 'literal old h0 frame action')
    base.require(two.matvec(c0,gperp)==[(q+1)*u+(q-1)*v for u,v in zip(gperp,h0)], 'literal old Gperp frame action')
    base.require(two.matvec(c0,zco)==[2*v for v in zco], 'literal old mean antisymmetric action')
    params=sectors(q,r);b=F(params['b']);eta=F(params['eta'])
    co=[[F(i==j) for j in range(m)] for i in range(m)]
    for h in hs:co += [[-k[j]/(r+1)+b*(h[j]-mean[j]) for j in range(m)],h]
    ind=[[F(0)]*(N-1) for _ in range(N-1)]
    for i in range(r):
        for j in range(r):ind[m+2*i][m+2*j]=eta if i==j else -eta/(r-1)
    seed=two.gram(c0,co,ind)
    base.require(sum(map(sum,seed))==F((r+1)*q-2*r,(r+1)**2), 'empty vector is -K/(r+1)')
    rawco=[v[:] for v in co]
    residual=[[F(0)]*(N-1) for _ in range(N-1)]
    for i,h in enumerate(hs):rawco[m+2*i]=[-v/q for v in h];residual[m+2*i][m+2*i]=q-F(1,q)
    raw=two.gram(c0,rawco,residual)
    B=sum(map(sum,raw));T=(N-1)*q+B
    base.require(B==(2*r+1)*q-4*r+F(2*r,q),'new raw constant form')
    base.require(T==2*q*q+4*r*q-4*r+F(2*r,q),'new raw full trace')
    eps=1/(2*(1+T))
    mixed=[[(1-eps)*seed[i][j]+eps*raw[i][j] for j in range(N-1)] for i in range(N-1)]
    return family,s,q,seed,raw,mixed,eps,T,params


def ordinary(family,matrix,s):
    matrix=base.rational_matrix(matrix);N=len(family)
    base.require(len(matrix)==N and base.family_star(family)==s,'ordinary dimensions/star')
    for i in range(N):
        base.require(sum(matrix[i])==1,'ordinary row sum')
        for j in range(N):
            base.require(matrix[i][j]==matrix[j][i],'ordinary symmetry')
            if family[i]&family[j]:base.require(matrix[i][j]==0,'ordinary support')
    low=[[(N-s)*matrix[i][j]+s*int(i==j) for j in range(N)] for i in range(N)]
    return base.psd_rank(low)


def check(n,r,mark_positions=None):
    f,s,q,seed,raw,mix,eps,T,params=build(n,r,mark_positions);N=len(f)
    sm=base.lift(seed,s);rm=base.lift(raw,s);mm=base.lift(mix,s)
    a=base.check(f,mm,s);b=base.check(f,sm,s)
    base.require(a['lower_rank']==N-r and a['upper_rank']==N-1,'maximal endpoint ranks')
    base.require(b['lower_rank']==N-r-1 and b['upper_rank']==N-1,'seed endpoint ranks')
    base.require(ordinary(f,rm,s)==N-r,'raw maximal ordinary rank')
    for label,matrix,margin in [('seed',sm,F(1)),('mixed',mm,F(1,2))]:
        gap=[[(N-s)*(int(i==j)-matrix[i][j])-margin*(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
        base.require(base.psd_rank(gap)==N-1,label+' full original-index uniform gap')
    a.update(n=n,r=r,mark_positions=list(range(r)) if mark_positions is None else list(mark_positions),seed_lower_rank=b['lower_rank'],seed_sha256=b['matrix_sha256'],raw_sha256=base.fingerprint(rm),epsilon=str(eps),T=str(T),sector=params)
    return a


def polynomial_certificates():
    """Formal two-variable polynomial identities; not sampled interpolation."""
    def add(*args):
        out={}
        for p in args:
            for ij,v in p.items():out[ij]=out.get(ij,0)+v
        return {ij:v for ij,v in out.items() if v}
    def const(v):return {(0,0):v} if v else {}
    def neg(p):return {ij:-v for ij,v in p.items()}
    def sub(a,b):return add(a,neg(b))
    def mul(*args):
        out=const(1)
        for p in args:
            new={}
            for (i,j),v in out.items():
                for (k,l),w in p.items():new[i+k,j+l]=new.get((i+k,j+l),0)+v*w
            out={ij:v for ij,v in new.items() if v}
        return out
    def scale(v,p):return mul(const(v),p)
    def power(p,k):return mul(*([p]*k))
    q={(1,0):1};t={(0,1):1};r=add(t,const(2));R=add(r,const(1))
    a=sub(add(mul(r,q),scale(2,power(r,2))),const(1))
    b=add(scale(2,mul(q,R)),r,const(-3))
    c=add(q,scale(4,power(r,2)),const(-3))
    qm1=sub(q,const(1));qmr=sub(q,r)
    second=sub(mul(a,b),scale(4,mul(power(r,2),qm1)))
    expected_second={(2,2):2,(2,1):10,(2,0):12,
                     (1,3):4,(1,2):25,(1,1):47,(1,0):24,
                     (0,3):2,(0,2):10,(0,1):15,(0,0):9}
    determinant=add(mul(a,b,c),neg(scale(4,mul(a,power(r,3),qmr))),
                    neg(mul(b,r,qm1,qmr)),neg(scale(4,mul(c,power(r,2),qm1))),
                    neg(scale(8,mul(power(r,3),qm1,qmr))))
    expected_det={(2,2):4,(2,1):14,(2,0):10,
                  (1,3):12,(1,2):60,(1,1):89,(1,0):43,
                  (0,4):8,(0,3):56,(0,2):132,(0,1):133,(0,0):49}
    base.require(second==expected_second, 'formal second-minor polynomial identity')
    base.require(determinant==mul(power(R,2),expected_det), 'formal determinant polynomial identity')
    q=add(t,const(4));qm4=sub(q,const(4))
    first=sub(scale(9,mul(q,add(q,const(1)))),scale(4,power(qm4,2)))
    det_anti=add(scale(9,mul(q,add(q,const(1)),add(scale(2,q),const(3)))),
                 neg(mul(add(q,const(1)),add(scale(8,power(q,2)),scale(40,q),const(-64)))),
                 neg(scale(4,mul(add(scale(2,q),const(3)),power(qm4,2)))))
    expected_first={(0,2):5,(0,1):81,(0,0):180}
    expected_anti={(0,3):2,(0,2):73,(0,1):507,(0,0):860}
    base.require(first==expected_first and det_anti==expected_anti, 'formal r2 antisymmetric identities')
    records={}
    for name,p in [('symmetric_second',expected_second),('symmetric_determinant',expected_det),
                   ('r2_antisymmetric_first',expected_first),('r2_antisymmetric_determinant',expected_anti)]:
        base.require(all(v>0 for v in p.values()), 'strictly positive polynomial coefficients')
        records[name]={'terms':len(p),'minimum_coefficient':min(p.values()),
                       'coefficients':[[i,j,v] for (i,j),v in sorted(p.items())]}
    return records


def old_core_checks(n):
    """Ordinary baseline plus original-index Cauchy cap obstructions."""
    r=3;q=1<<(n-1);N=2*q+6;s=q+1;full=2*q-1;m=2*q-1
    old=list(range(1,2*q));c0=[[F(s*int(u==v)+q*int(u^v==full)-1) for v in old] for u in old]
    one=[F(1)]*m;hs=[[F(-bool(u&(1<<i))) for u in old] for i in range(3)]
    hsum=[sum(h[j] for h in hs) for j in range(m)];k=[1+v for v in hsum]
    co=[[F(i==j) for j in range(m)] for i in range(m)]
    family=list(range(2*q))
    for i,h in enumerate(hs):
        leaf=1<<(n+i);family += [leaf,leaf|(1<<i)];co += [[-v/q for v in h],h]
    residual=[[F(0)]*(N-1) for _ in range(N-1)]
    for i in range(3):residual[m+2*i][m+2*i]=q-F(1,q)
    raw=two.gram(c0,co,residual);matrix=base.lift(raw,s)
    base.require(ordinary(family,matrix,s)==N-3, 'old ordinary maximal-rank baseline')
    base.require((N-1)*q+sum(map(sum,raw))==2*q*q+11*q-8+F(3,q), 'old raw trace identity')
    hg=[(v-1)/(q+1) for v in two.matvec(c0,one)]
    coords=[[v/2 for v in hsum], [u-v+w/2 for u,v,w in zip(one,hg,hsum)], hg]
    images=[two.matvec(c0,v) for v in coords]
    gram=two.gram(c0,coords,[[F(0)]*3 for _ in range(3)])
    norms=[F(3*q,2),F(q*(q-3),2*(q+1)),F((q+2)*(q-1),q+1)]
    base.require(gram==[[norms[i]*int(i==j) for j in range(3)] for i in range(3)], 'old literal changed-sector indexing')
    spoke_inner=[[two.dot(h,v) for h in hs] for v in images]
    known=[[two.dot(images[i],images[j])+two.dot(spoke_inner[i],spoke_inner[j]) for j in range(3)] for i in range(3)]
    summed=[two.dot(k,v) for v in images]
    base.require(summed==norms, 'old known sum K coefficient')
    records=[];gaps=[F(5),F(2*q+5),F(q+4)]
    for count in [3,4]:
        necessary=[[N*gram[i][j]-known[i][j]-summed[i]*summed[j]/count for j in range(3)] for i in range(3)]
        formula=[[gaps[i]*norms[i]*int(i==j)-norms[i]*norms[j]/count for j in range(3)] for i in range(3)]
        base.require(necessary==formula, 'original-index Q-squared Cauchy compression')
        theta=sum(v/g for v,g in zip(norms,gaps))/count
        determinant=det3(necessary)
        base.require((determinant<0)==(theta>1), 'exact negative determinant certificate')
        records.append({'unknown_vectors':count,'theta':str(theta),'necessary_determinant':str(determinant),'obstructed':theta>1})
    image=two.matvec(c0,hsum);norm=two.dot(hsum,image)
    fixed_squared=two.dot(image,image)+sum(two.dot(h,image)**2 for h in hs)
    summed=two.dot(k,image)
    rayleigh=N-(fixed_squared+summed*summed/4)/norm
    base.require(norm==6*q and rayleigh==5-F(3*q,8), 'original-index empty-inclusive Rayleigh identity')
    return {'n':n,'q':q,'N':N,'s':s,'ordinary_lower_rank':N-3,'raw_matrix_sha256':base.fingerprint(matrix),
            'compressions':records,'empty_inclusive_normalized_cap_Rayleigh_upper':str(rayleigh)}


def rejection_controls():
    rejected=[]
    def reject(label,fn):
        try:fn()
        except ValueError:rejected.append(label);return
        raise ValueError('control accepted: '+label)
    for n,r,label in [(1,2,'small cube'),(7,2,'literal order guard'),(3,1,'single mark'),
                      (3,4,'too many marks'),(3.0,2,'floating order'),(3,True,'Boolean mark count')]:
        reject(label,lambda n=n,r=r:build(n,r))
    reject('duplicate marks',lambda:build(3,2,[0,0]))
    reject('outside mark',lambda:build(3,2,[0,3]))
    reject('bad mark type',lambda:build(3,2,[0,True]))
    reject('invalid sector domain',lambda:sectors(3,2))
    f,s,q,_,_,c,_,_,_=build(3,3);m=base.lift(c,s)
    bad=[row[:] for row in m];bad[0][0]+=1
    reject('damaged row sum',lambda:base.check(f,bad,s))
    bad=[row[:] for row in m];i,j=1,3
    bad[i][j]+=1;bad[j][i]+=1;bad[0][i]-=1;bad[i][0]-=1;bad[0][j]-=1;bad[j][0]-=1;bad[0][0]+=2
    reject('damaged intersecting entry',lambda:base.check(f,bad,s))
    reject('wrong star parameter',lambda:base.check(f,m,s-1))
    reject('negative PSD input',lambda:base.psd_rank([[-1,0],[0,1]]))
    reject('singular nonzero residual',lambda:base.psd_rank([[0,1],[1,0]]))
    return rejected


def product_checks():
    def marked(n,r):
        f,s,_,_,_,c,_,_,_=build(n,r)
        return (f,base.lift(c,s),s,'marked(%d,%d)'%(n,r)),r
    boundary,k=marked(2,2);three,k3=marked(3,3)
    singleton=([0,1,2],[[F(int(i!=j),2) for j in range(3)] for i in range(3)],1,'two_singletons')
    base.check(*singleton[:2],singleton[2])
    records=[]
    for factors,nullities in [([boundary,boundary],[k,k]),([three,singleton],[k3,2])]:
        f,a,s,label=base.tensor_parts(factors);N=len(f)
        base.require(N<=80, 'product literal guard80')
        densities=[F(p[2],len(p[0])) for p in factors];best=max(densities)
        eligible=[i for i,z in enumerate(densities) if z==best]
        nullity=sum(nullities[i] for i in eligible)
        checked=base.check(f,a,s)
        base.require(checked['lower_rank']==N-nullity and checked['upper_rank']==N-1, 'strict eligible-factor product ranks')
        checked.update(label=label,eligible_factors=eligible,forced_nullity=nullity)
        records.append(checked)
    return records


def results():
    entries=[check(2,2)]+[check(n,r) for n in range(3,7) for r in range(2,n+1)]
    relabeled=check(4,3,[3,1,0])
    parameters=sorted(set([(q,r) for r in range(2,21) for q in [max(4,r+1),2**max(3,r.bit_length()+1),1<<20]]))
    return {'schema':1,'author':'six-downset-1','role':'researcher',
            'status':'author-checked unformalized proof; exact finite validation',
            'coverage':{'literal_n_range':[2,6],'all_canonical_r_values':True,'largest_N':76,
                        'all_order_theorem':'n>=2,2<=r<=n; ALL_MARKS.md','scalar_frame_fixtures':len(parameters)},
            'entries':entries,'relabeled_fixture':relabeled,'frame_fixtures':[sectors(q,r) for q,r in parameters],
            'polynomial_certificates':polynomial_certificates(),
            'old_core_baselines_and_obstructions':[old_core_checks(n) for n in range(3,7)],
            'products':product_checks(),
            'rejection_controls':rejection_controls()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write',type=Path);group.add_argument('--check',type=Path)
    args=parser.parse_args();answer=results();encoded=(json.dumps(answer,indent=2,sort_keys=True)+'\n').encode()
    if args.write:args.write.write_bytes(encoded)
    else:
        base.require(json.loads(args.check.read_text())==answer,'expected result mismatch')
        base.require(args.check.read_bytes()==encoded,'expected byte mismatch')
    print(json.dumps({'canonical_instances':len(answer['entries']),'relabeled_instances':1,
                      'frame_fixtures':len(answer['frame_fixtures']),'positive_coefficients':sum(z['terms'] for z in answer['polynomial_certificates'].values()),
                      'old_core_cases':len(answer['old_core_baselines_and_obstructions']),
                      'products':len(answer['products']),
                      'rejection_controls':len(answer['rejection_controls']),'largest_N':76,
                      'results_sha256':sha256(encoded).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
