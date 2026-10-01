"""Exact rational replay for equal loads at distinct cube marks.

Standard-library helpers credited to verify.py, verify_two_marks.py, and
verify_all_marks.py. The unbounded proof is EQUAL_LOAD_MARKS.md.
"""
from pathlib import Path
import argparse,json
from hashlib import sha256
from fractions import Fraction as F
import verify as base
import verify_two_marks as two
import verify_all_marks as one


def sectors(q,r,d):
    base.require(type(q) is int and type(r) is int and type(d) is int and r>=2 and d>=1
                 and (q==r==2 or q>=r+1),'sector domain')
    m=r*d;N=2*q+2*m;w=F(q+d-1);ell=w-F(q,m)
    c=F(q-m-2,m+1)/ell;B=F((m+1)*q+d-1-2*m)
    eta=w-B/(m+1)**2-c*c*ell;e=F(m,m-1)*eta
    base.require(eta>0,'positive global simplex residual')
    numerator=(m*m-2)*q*q+(2*(m*m+m-1)*(d-1)+4*m+2)*q+m*(m+2)*(d-1)**2+2*m*(d-1)-(m+2)**2
    base.require(eta==F(numerator,(m+1)**2)/ell,'eta polynomial identity')
    g=F(q-1);z=F(d*(q-r),r);metric=[g,F(d),z]
    h=[F(0),F(d),z];k=[g,F((r-1)*d),r*z]
    f0=[[F((q+1)*g),d*g,F(0)],[d*g,F(d*d),F(0)],[F(0),F(0),2*d*z]]
    frame=[[f0[i][j]+F(r,d)*h[i]*h[j]+k[i]*k[j]/(m+1) for j in range(3)] for i in range(3)]
    sigma=F(4,3) if d>=2 else F(1)
    cap=[[(N-sigma)*metric[i]*int(i==j)-frame[i][j] for j in range(3)] for i in range(3)]
    base.require(base.psd_rank(cap)==(3 if z else 2),'symmetric frame uniform cap')
    small=[]
    for label,t,v2 in [('between',q+2*d,q),('within',q+d,q+d)]:
        if label=='within' and d==1:continue
        mat=[[F(v2)*(N-sigma-t)-c*c*v2*v2,-c*v2*e],[-c*v2*e,(N-sigma)*e-e*e]]
        base.require(base.psd_rank(mat)==2,label+' frame uniform cap')
        budget=c*c*v2/(N-t)+e/N
        small.append({'label':label,'budget_at_N':str(budget),'scaled_dimension':2})
    if d>=2:
        base.require(abs(c)<=F(1,3),'uniform correction bound')
        base.require(e<=F(4,3)*w,'uniform residual frame bound')
        base.require(all(F(x['budget_at_N'])<F(7,9) for x in small),'uniform rank-one budgets')
        base_frame=[[f0[i][j]+F(r,d)*h[i]*h[j] for j in range(3)] for i in range(3)]
        crude=[[(q+2*d+r)*metric[i]*int(i==j)-base_frame[i][j] for j in range(3)] for i in range(3)]
        base.require(base.psd_rank(crude)==(3 if z else 2),'crude symmetric base cap')
        base.require(q+2*d+r+B/(m+1)<=N-1,'common-vector symmetric budget')
    dimension=(3+2*(r-1)+2*r*(d-1)+(q-2)+(q-r-1) if z else 2+2*(r-1)+2*r*(d-1))
    base.require(dimension==N-r-2,'complete sector dimension')
    return {'q':q,'r':r,'d':d,'m':m,'w':str(w),'ell':str(ell),'c':str(c),
            'eta':str(eta),'e':str(e),'B_seed':str(B),'symmetric_dimension':3 if z else 2,
            'frame_dimension':dimension,'budgets':small,'scaled_seed_gap':str(sigma)}


def build(n,r,d,mark_positions=None):
    base.require(type(n) is int and type(r) is int and type(d) is int
                 and 2<=n<=6 and 2<=r<=n and d>=1,'valid family parameter')
    q=1<<(n-1);m=r*d;N=2*q+2*m;s=q+d;w=F(s-1)
    base.require(N<=80,'literal family guard80')
    positions=list(range(r)) if mark_positions is None else list(mark_positions)
    base.require(len(positions)==r and len(set(positions))==r and all(type(i) is int and 0<=i<n for i in positions),'distinct valid marks')
    full=2*q-1;old=list(range(1,2*q));oldm=len(old)
    family=list(range(2*q));c0=[[F((q+d)*int(a==b)+(q-d)*int(a^b==full)-1) for b in old] for a in old]
    base.require(base.psd_rank(c0)==oldm,'old modified cube PD')
    hs=[[F(-bool(a&(1<<i))) for a in old] for i in positions]
    k=[1+sum(h[j] for h in hs) for j in range(oldm)];mean=[sum(h[j] for h in hs)/r for j in range(oldm)]
    params=sectors(q,r,d);c=F(params['c']);eta=F(params['eta'])
    oneco=[F(1)]*oldm;fullco=[F(a==full) for a in old]
    h0=[-(x+y)/2 for x,y in zip(oneco,fullco)];gperp=[x+y for x,y in zip(oneco,h0)];zco=[x-y for x,y in zip(mean,h0)]
    coords=[gperp,h0,zco];metric=[F(q-1),F(d),F(d*(q-r),r)]
    literal=two.gram(c0,coords,[[F(0)]*3 for _ in range(3)])
    base.require(literal==[[metric[i]*int(i==j) for j in range(3)] for i in range(3)],'literal orthogonal symmetric coordinates')
    base.require(two.matvec(c0,h0)==[d*(x+2*y) for x,y in zip(oneco,h0)],'literal h0 old-frame action')
    base.require(two.matvec(c0,gperp)==[(q+1)*x+(q-1)*y for x,y in zip(gperp,h0)],'literal Gperp old-frame action')
    base.require(two.matvec(c0,zco)==[2*d*x for x in zco],'literal Z old-frame action')
    co=[[F(i==j) for j in range(oldm)] for i in range(oldm)]
    for i in range(r):
        for j in range(d):
            leaf=1<<(n+i*d+j);family += [leaf,leaf|(1<<positions[i])]
            co += [[-k[z]/(m+1)+c*(hs[i][z]-mean[z])/d for z in range(oldm)], [x/d for x in hs[i]]]
    def residual(single_coefficient,global_eta,independent_norm=F(0)):
        out=[[F(0)]*(N-1) for _ in range(N-1)]
        for u in range(m):
            for v in range(m):
                ti=(F(q+d)*(int(u==v))-F(q,d)-1) if u//d==v//d else F(0)
                for a,ca in [(0,single_coefficient),(1,F(1))]:
                    for b,cb in [(0,single_coefficient),(1,F(1))]:
                        out[oldm+2*u+a][oldm+2*v+b]+=ca*cb*ti
                out[oldm+2*u][oldm+2*v]+=global_eta if u==v else -global_eta/(m-1)
            out[oldm+2*u][oldm+2*u]+=independent_norm
        return out
    seed=two.gram(c0,co,residual(c,eta))
    base.require(sum(map(sum,seed))==F(params['B_seed'])/(m+1)**2,'full seed empty energy')
    rawco=[x[:] for x in co]
    for u in range(m):rawco[oldm+2*u]=[-x/w for x in co[oldm+2*u+1]]
    raw=two.gram(c0,rawco,residual(-1/w,F(0),w-1/w))
    B=sum(map(sum,raw));Bformula=(m+1)*w+m*q-2*m+F(m*(1-2*q))/w+F(m*q)/(w*w)
    base.require(B==Bformula,'raw empty energy identity')
    T=(N-1)*w+B;sigma=F(params['scaled_seed_gap']);epsilon=sigma/(2*(sigma+T))
    mixed=[[(1-epsilon)*seed[i][j]+epsilon*raw[i][j] for j in range(N-1)] for i in range(N-1)]
    return family,s,seed,raw,mixed,params,T,epsilon


def check(n,r,d,mark_positions=None):
    family,s,seed,raw,mix,params,T,eps=build(n,r,d,mark_positions);N=len(family)
    sm=base.lift(seed,s);rm=base.lift(raw,s);mm=base.lift(mix,s)
    seed_record=base.check(family,sm,s);answer=base.check(family,mm,s)
    base.require(seed_record['lower_rank']==N-r-1 and answer['lower_rank']==N-r,'seed/repaired ranks')
    base.require(one.ordinary(family,rm,s)==N-r,'raw maximal ordinary rank')
    for label,a,margin in [('seed',sm,F(params['scaled_seed_gap'])),('mixed',mm,F(params['scaled_seed_gap'])/2)]:
        gap=[[(N-s)*(int(i==j)-a[i][j])-margin*(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
        base.require(base.psd_rank(gap)==N-1,label+' full original-index gap')
    answer.update(n=n,r=r,d=d,mark_positions=list(range(r)) if mark_positions is None else list(mark_positions),T=str(T),epsilon=str(eps),sector=params,
                  seed_lower_rank=seed_record['lower_rank'],seed_sha256=seed_record['matrix_sha256'],raw_sha256=base.fingerprint(rm))
    return answer


def positive_polynomials():
    """Formal identities over Z[Q,M,D], shifted q=Q+2,m=M+4,d=D+2."""
    def const(x):return {(0,0,0):x} if x else {}
    def add(*args):
        out={}
        for p in args:
            for k,v in p.items():out[k]=out.get(k,0)+v
        return {k:v for k,v in out.items() if v}
    def neg(p):return {k:-v for k,v in p.items()}
    def sub(p,q):return add(p,neg(q))
    def mul(*args):
        out=const(1)
        for p in args:
            new={}
            for k,v in out.items():
                for l,w in p.items():
                    j=tuple(x+y for x,y in zip(k,l));new[j]=new.get(j,0)+v*w
            out={k:v for k,v in new.items() if v}
        return out
    def scale(v,p):return mul(const(v),p)
    def sq(p):return mul(p,p)
    q=add({(1,0,0):1},const(2));m=add({(0,1,0):1},const(4));d=add({(0,0,1):1},const(2))
    w=add(q,d,const(-1));dm1=sub(d,const(1))
    literal=sub(mul(sub(mul(m,w),q),add(mul(add(m,const(2)),w),neg(q),const(2))),sq(add(q,neg(m),const(-2))))
    formula=add(mul(sub(sq(m),const(2)),sq(q)),
                mul(add(scale(2,mul(add(sq(m),m,const(-1)),dm1)),scale(4,m),const(2)),q),
                mul(m,add(m,const(2)),sq(dm1)),scale(2,mul(m,dm1)),neg(sq(add(m,const(2)))))
    base.require(literal==formula,'formal residual numerator identity')
    boundary=sub(add(mul(d,add(scale(2,d),const(1)),add(d,const(1))),neg(add(scale(2,d),const(1)))),scale(6,sq(d)))
    boundary_formula=add(mul(d,sub(d,const(2)),add(scale(2,d),const(1))),d,const(-1))
    base.require(boundary==boundary_formula,'formal small-boundary correction identity')
    result={}
    for name,p in [('residual_numerator',formula),('q2_correction_bound',boundary_formula)]:
        base.require(all(x>0 for x in p.values()),'positive shifted coefficients')
        result[name]={'terms':len(p),'minimum_coefficient':min(p.values()),'coefficients':[[*k,v] for k,v in sorted(p.items())]}
    return result


def parent_baselines():
    expected=__import__('json').loads(Path(__file__).with_name('ALL_MARKS_RESULTS.json').read_text())['entries']
    records=[]
    for n,r in [(2,2),(3,3),(4,4)]:
        actual=check(n,r,1);parent=next(x for x in expected if x['n']==n and x['r']==r)
        for key in ['N','s','lower_rank','upper_rank','matrix_sha256','seed_lower_rank','seed_sha256','raw_sha256','T','epsilon']:
            base.require(actual[key]==parent[key],'credited load1 exact baseline '+key)
        records.append({'n':n,'r':r,'d':1,'matrix_sha256':actual['matrix_sha256'],'matches_parent':True})
    return records


def product_checks():
    def marked(n,r,d):
        family,s,_,_,c,_,_,_=build(n,r,d)
        return (family,base.lift(c,s),s,'equal_load(%d,%d,%d)'%(n,r,d)),r
    singleton=([0,1,2],[[F(int(i!=j),2) for j in range(3)] for i in range(3)],1,'two_singletons')
    base.check(*singleton[:2],singleton[2]);records=[]
    for parameter in [(2,2,2),(3,3,2)]:
        factor,k=marked(*parameter);parts=[factor,singleton]
        family,a,s,label=base.tensor_parts(parts);N=len(family)
        base.require(N<=80,'product literal guard80')
        densities=[F(p[2],len(p[0])) for p in parts];eligible=[i for i,z in enumerate(densities) if z==max(densities)]
        nullity=sum([k,2][i] for i in eligible)
        record=base.check(family,a,s)
        base.require(record['lower_rank']==N-nullity and record['upper_rank']==N-1,'eligible product ranks')
        record.update(label=label,eligible_factors=eligible,forced_nullity=nullity);records.append(record)
    return records


def small_family_census():
    from itertools import combinations
    family,s,_,_,_,_,_,_=build(2,2,2)
    maxima=[list(c) for c in combinations(family[1:],s) if all(a&b for a,b in combinations(c,2))]
    stars=[sorted(a for a in family if a&(1<<i)) for i in range(2)]
    base.require(sorted(maxima)==sorted(stars),'literal maximum families are marked stars')
    return {'n':2,'r':2,'d':2,'candidates':330,'maximum_families':maxima}


def rejection_controls():
    rejected=[]
    def reject(label,fn):
        try:fn()
        except ValueError:rejected.append(label);return
        raise ValueError('Control accepted: '+label)
    for n,r,d,label in [(1,2,2,'small cube'),(7,2,2,'literal cube guard'),(2,2,20,'literal matrix guard'),
                        (3,1,2,'single mark'),(3,4,2,'too many marks'),(3,2,0,'zero load'),
                        (3,2,-1,'negative load'),(3,2,2.0,'floating load'),(3,2,True,'Boolean load')]:
        reject(label,lambda n=n,r=r,d=d:build(n,r,d))
    reject('duplicate marks',lambda:build(3,2,2,[0,0]))
    reject('outside mark',lambda:build(3,2,2,[0,3]))
    reject('bad mark type',lambda:build(3,2,2,[0,True]))
    reject('invalid scalar sector',lambda:sectors(3,3,2))
    family,s,_,_,c,_,_,_=build(3,3,2);a=base.lift(c,s)
    bad=[v[:] for v in a];bad[0][0]+=1
    reject('damaged row sum',lambda:base.check(family,bad,s))
    bad=[v[:] for v in a];i,j=9,11
    bad[i][j]+=1;bad[j][i]+=1;bad[0][i]-=1;bad[i][0]-=1;bad[0][j]-=1;bad[j][0]-=1;bad[0][0]+=2
    reject('damaged same-mark spoke intersection',lambda:base.check(family,bad,s))
    reject('wrong star parameter',lambda:base.check(family,a,s-1))
    reject('negative PSD input',lambda:base.psd_rank([[-1,0],[0,1]]))
    reject('singular nonzero residual',lambda:base.psd_rank([[0,1],[1,0]]))
    return rejected


def results():
    parameters=[(n,r,d) for n in range(2,5) for r in range(2,n+1) for d in range(2,5)]
    parameters += [(2,2,8),(2,2,19),(3,3,8),(4,4,6),(5,5,4),(6,2,2),(6,3,2),(6,4,2)]
    frames=sorted(set([(q,r,d) for r in range(2,13) for d in [2,8,1<<20]
                       for q in [max(4,r+1),1024,1<<20]]+[(2,2,d) for d in [2,3,8,19,1<<20]]))
    return {'schema':1,'author':'six-downset-1','role':'researcher','status':'author-checked unformalized proof; exact finite validation',
            'coverage':{'all_order_theorem':'n>=2,2<=r<=n,d>=2; EQUAL_LOAD_MARKS.md','literal_guard':80,'largest_N':80},
            'entries':[check(*args) for args in parameters],'relabeled_fixture':check(4,3,2,[3,1,0]),
            'parent_load1_baselines':parent_baselines(),'frame_fixtures':[sectors(*args) for args in frames],
            'positive_polynomials':positive_polynomials(),'products':product_checks(),
            'small_family_census':small_family_census(),'rejection_controls':rejection_controls()}


def main():
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write',type=Path);group.add_argument('--check',type=Path)
    args=parser.parse_args();answer=results();encoded=(json.dumps(answer,indent=2,sort_keys=True)+'\n').encode()
    if args.write:args.write.write_bytes(encoded)
    else:base.require(args.check.read_bytes()==encoded,'Expected exact record byte mismatch')
    print(json.dumps({'literal_cases':len(answer['entries']),'relabeled_cases':1,'parent_baselines':len(answer['parent_load1_baselines']),
                      'frame_fixtures':len(answer['frame_fixtures']),'positive_coefficients':sum(x['terms'] for x in answer['positive_polynomials'].values()),
                      'products':len(answer['products']),'maximum_family_candidates':answer['small_family_census']['candidates'],
                      'rejection_controls':len(answer['rejection_controls']),'largest_N':80,'results_sha256':sha256(encoded).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
