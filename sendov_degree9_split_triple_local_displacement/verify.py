#!/usr/bin/env python3
"""Exact degree-nine split-triple local displacement certificate.
Actual author six-sendov-2, researcher, 2026-10-01.
Q[u,S,A2,A3], standard library only. Every coefficient is rebuilt.
Classical spectral projection, Maclaurin and analytic interpretations are
ordinary written proof; unformalized, independent review pending.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
import argparse,hashlib,json
CHECKS=0
def require(ok,label):
    global CHECKS
    CHECKS+=1
    if not ok:raise ValueError(label)
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
class P:
    def __init__(self,value=0):
        if isinstance(value,P):value=value.t
        if isinstance(value,(int,F)):value={(0,0,0,0):F(value)}
        self.t={e:F(c) for e,c in value.items() if c}
    def __add__(self,other):
        t=dict(self.t)
        for e,c in P(other).t.items():t[e]=t.get(e,F(0))+c
        return P(t)
    __radd__=__add__
    def __neg__(self):return P({e:-c for e,c in self.t.items()})
    def __sub__(self,other):return self+-P(other)
    def __rsub__(self,other):return P(other)+-self
    def __mul__(self,other):
        t={}
        for e,c in self.t.items():
            for f,b in P(other).t.items():
                g=tuple(x+y for x,y in zip(e,f));t[g]=t.get(g,F(0))+c*b
        return P(t)
    __rmul__=__mul__
    def __truediv__(self,n):return self*(1/F(n))
    def __pow__(self,n):
        out=P(1)
        for _ in range(n):out*=self
        return out
    def __eq__(self,other):return self.t==P(other).t
    def evaluate(self,x):return sum(c*prod_scalar(v**k for v,k in zip(x,e)) for e,c in self.t.items())
    def dump(self):return [[*e,str(c)] for e,c in sorted(self.t.items())]

def prod_scalar(values):
    out=1
    for v in values:out*=v
    return out
def prod(values):
    out=P(1)
    for v in values:out*=v
    return out
def trace_words(r):
    result={}
    for mask in range(1<<r):
        positions=[i for i in range(r) if mask>>i&1]
        if not positions:key=(r,);c=F(1)
        else:
            key=tuple(sorted((positions[(i+1)%len(positions)]-p)%r or r for i,p in enumerate(positions)))
            c=F((-1)**len(positions),8**len(positions))
        result[key]=result.get(key,F(0))+c
    return result
def adj3(g):
    out=[]
    for i in range(3):
        row=[]
        for j in range(3):
            a=[r for r in range(3) if r!=j];b=[c for c in range(3) if c!=i]
            row.append((-1)**(i+j)*(g[a[0]][b[0]]*g[a[1]][b[1]]-g[a[0]][b[1]]*g[a[1]][b[0]]))
        out.append(row)
    return out

u,S,A2,A3=[P({tuple(int(i==j) for j in range(4)):1}) for i in range(4)]
def bernstein(poly,box):
    degrees=[max((e[i] for e in poly.t),default=0) for i in range(4)]
    data=dict(poly.t)
    for axis,(a,b) in enumerate(box):
        out={}
        for e,c in data.items():
            for q in range(e[axis]+1):
                h=tuple(q if i==axis else v for i,v in enumerate(e))
                out[h]=out.get(h,F(0))+c*comb(e[axis],q)*a**(e[axis]-q)*(b-a)**q
        data={e:c for e,c in out.items() if c}
    normalized=dict(data)
    for axis,n in enumerate(degrees):
        out={}
        for e,c in data.items():
            for q in range(e[axis],n+1):
                h=tuple(q if i==axis else v for i,v in enumerate(e))
                out[h]=out.get(h,F(0))+c*F(comb(q,e[axis]),comb(n,e[axis]))
        data={e:c for e,c in out.items() if c}
    from itertools import product
    indices=list(product(*(range(n+1) for n in degrees)))
    values=[data.get(e,F(0)) for e in indices]
    # Independent inverse conversion; complete power arrays must match.
    inverse=dict(data)
    for axis,n in enumerate(degrees):
        out={}
        for e,c in inverse.items():
            for q in range(e[axis],n+1):
                h=tuple(q if i==axis else v for i,v in enumerate(e))
                out[h]=out.get(h,F(0))+c*comb(n,q)*comb(q,e[axis])*(-1)**(q-e[axis])
        inverse={e:c for e,c in out.items() if c}
    require(inverse==normalized,'complete4D inverse Bernstein identity')
    return values,degrees


def mm(a,b):
    return [[sum(a[i][h]*b[h][j] for h in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def independent_rows(rows):
    pivots={};selected=[]
    for original in rows:
        r=list(original)
        for j,b in sorted(pivots.items()):
            c=r[j]
            if c:r=[u-c*v for u,v in zip(r,b)]
        if any(r):
            j=next(j for j,v in enumerate(r) if v);c=r[j]
            pivots[j]=[v/c for v in r];selected.append(original)
    return selected
def solve(a,b):
    a=[list(r)+[v] for r,v in zip(a,b)];n=len(b)
    for j in range(n):
        pivots=[i for i in range(j,n) if a[i][j]]
        require(bool(pivots),'independent commutant nonzero pivot')
        i=pivots[0];a[j],a[i]=a[i],a[j];t=a[j][j]
        a[j]=[v/t for v in a[j]]
        for i in range(j+1,n):
            t=a[i][j]
            if t:a[i]=[u-t*v for u,v in zip(a[i],a[j])]
    x=[F(0)]*n
    for j in range(n-1,-1,-1):x[j]=a[j][-1]-sum(a[j][h]*x[h] for h in range(j+1,n))
    return x
def pinching(theta):
    # Adapted with attribution from the preceding author's defining
    # symmetric-commutant controls. It does not use any moment quotient.
    c=[[(theta[i] if i==j else F(0))-(theta[i]+theta[j])/8
        for j in range(8)] for i in range(8)]
    pairs=list(combinations_with_replacement(range(8),2))
    weights=[F(1 if i==j else 2) for i,j in pairs]
    ww=[theta[i]*theta[j]/8 for i,j in pairs];rows=[]
    for i in range(8):
        for j in range(i+1,8):
            row=[]
            for h,k in pairs:
                v=(c[i][h] if k==j else 0)-(c[k][j] if i==h else 0)
                if h!=k:v+=(c[i][k] if h==j else 0)-(c[h][j] if i==k else 0)
                row.append(v)
            rows.append(row)
    selected=independent_rows(rows)
    rhs=[sum(a*b for a,b in zip(row,ww)) for row in selected]
    gram=[[sum(a*b/g for a,b,g in zip(row,other,weights)) for other in selected] for row in selected]
    lam=solve(gram,rhs)
    projected=[v-sum(row[k]*b for row,b in zip(selected,lam))/weights[k] for k,v in enumerate(ww)]
    for row in rows:require(sum(a*b for a,b in zip(row,projected))==0,'full defining commutation equation')
    residual=[a-b for a,b in zip(ww,projected)]
    require(sum(g*a*b for g,a,b in zip(weights,projected,residual))==0,'defining Frobenius orthogonality')
    return sum(g*v*v for g,v in zip(weights,projected)),len(selected)
def definition_controls(mu,d,n,divided,dm):
    profiles=[(F(1,4),(F(0),)*3),(F(3,10),(F(0),)*3),(F(1,3),(F(0),)*3),
              (F(1,4),(F(1,100),F(0),F(0))),
              (F(3,10),(F(1,600),F(1,300),F(1,200))),
              (F(1,3),(F(1,1000),F(3,1000),F(6,1000))),
              (F(2,7),(F(1,1000),F(2,1000),F(3,1000)))]
    records=[]
    for x,alpha in profiles:
        total=sum(alpha);a2=sum(alpha[i]*alpha[j] for i in range(3) for j in range(i+1,3));a3=prod_scalar(alpha)
        theta=[F(-1)]*3+[1-v for v in alpha]+[total/2+x,total/2-x]
        require(sum(theta)==0 and max(map(abs,theta))==1,'literal local physical profile')
        point=(x*x,total,a2,a3);moments=[sum(t**r for t in theta) for r in range(9)]
        for r in range(9):require(mu[r].evaluate(point)==moments[r],'literal full moment'+str(r))
        c=[[(theta[i] if i==j else F(0))-(theta[i]+theta[j])/8 for j in range(8)] for i in range(8)]
        ww=[[theta[i]*theta[j]/8 for j in range(8)] for i in range(8)]
        identity=[[F(int(i==j)) for j in range(8)] for i in range(8)]
        powers=[identity]
        for r in range(1,9):powers.append(mm(powers[-1],c))
        traces=[F(7)]+[tr(powers[r]) for r in range(1,9)]
        for r in range(1,9):
            direct=sum(coef*prod_scalar(moments[j] for j in word) for word,coef in trace_words(r).items())
            require(direct==traces[r],'full8x8 versus cyclic trace word'+str(r))
        bb=[tr(mm(ww,powers[r])) for r in range(5)]
        reference=[moments[2]/8,moments[3]/8,
                   moments[4]/8-moments[2]**2/64,
                   moments[5]/8-moments[2]*moments[3]/32,
                   moments[6]/8-(2*moments[2]*moments[4]+moments[3]**2)/64+moments[2]**3/512]
        for a,b in zip(bb,reference):require(a==b,'literal b moment identity')
        polys=[[[powers[r][i][j]-powers[r+2][i][j] for j in range(8)] for i in range(8)] for r in range(3)]
        gg=[[tr(mm(polys[i],polys[j]))-F(int(i==j==0)) for j in range(3)] for i in range(3)]
        br=[tr(mm(ww,p)) for p in polys]
        for i in range(3):
            require(br[i]==bb[i]-bb[i+2],'literal filtered rhs')
            for j in range(3):require(gg[i][j]==traces[i+j]-2*traces[i+j+2]+traces[i+j+4],'literal7-space filtered Gram')
        det=gg[0][0]*(gg[1][1]*gg[2][2]-gg[1][2]*gg[2][1])-gg[0][1]*(gg[1][0]*gg[2][2]-gg[1][2]*gg[2][0])+gg[0][2]*(gg[1][0]*gg[2][1]-gg[1][1]*gg[2][0])
        require(det==d.evaluate(point)>0,'defining determinant versus whole polynomial')
        sol=solve(gg,br);lower=sum(a*b for a,b in zip(br,sol))
        require(lower*det==n.evaluate(point),'defining filtered numerator')
        psi,rank=pinching(theta)
        require(lower<=psi,'filtered minorant versus full defining pinching')
        actual=122*moments[2]+(224*moments[4]-5760*psi)/moments[2]
        majorant=122*moments[2]+(224*moments[4]-5760*lower)/moments[2]
        scalar=(2058+21912*x*x-15876*x**4+19224*x**6+3402*x**8)/((3+x*x)*(1+3*x*x)**2)
        require(actual<=majorant<=scalar-200*total,'full objective and exact normal-loss control')
        if total:
            y=3*a2/total**2;z=27*a3/total**3
            require(0<=y<=1 and 0<=z<=1,'actual Maclaurin domain control')
            require(dm.evaluate((x*x,total,y,z))==det,'Maclaurin determinant pullback')
        else:require(psi==lower and actual==scalar,'complete symmetric face control')
        records.append({'x':str(x),'deficits':list(map(str,alpha)),'S':str(total),
                        'D':str(det),'Psi':str(psi),'filtered_lower':str(lower),
                        'J':str(actual),'J_majorant':str(majorant),'commutant_rank':rank})
    return records
def derive():
    elem=[P(1),S,A2,A3];powers=[P(3)]
    for r in range(1,9):
        if r<=3:
            value=sum(((-1)**(j-1)*elem[j]*powers[r-j] for j in range(1,r)),P(0))
            value+=(-1)**(r-1)*r*elem[r]
        else:value=sum(((-1)**(j-1)*elem[j]*powers[r-j] for j in range(1,4)),P(0))
        powers.append(value)
    mu=[P(8)]
    for r in range(1,9):
        positives=sum(((-1)**j*comb(r,j)*powers[j] for j in range(r+1)),P(0))
        small=sum((2*comb(r,j)*(S/2)**(r-j)*u**(j//2) for j in range(0,r+1,2)),P(0))
        mu.append(3*(-1)**r+positives+small)
    require(mu[1]==0,'full balanced local chart')
    traces=[P(7)]+[sum((c*prod(mu[j] for j in word) for word,c in trace_words(r).items()),P(0)) for r in range(1,9)]
    inverse=[P(1)]
    for r in range(1,7):inverse.append(-sum((mu[j]*inverse[r-j]/8 for j in range(1,r+1)),P(0)))
    b=[-inverse[r+2] for r in range(5)]
    gram=[[traces[i+j]-2*traces[i+j+2]+traces[i+j+4] for j in range(3)] for i in range(3)]
    rhs=[b[i]-b[i+2] for i in range(3)]
    adj=adj3(gram);d=sum((gram[0][j]*adj[j][0] for j in range(3)),P(0))
    n=sum((rhs[i]*adj[i][j]*rhs[j]*(1 if i==j else 2) for i in range(3) for j in range(i,3)),P(0))
    jn=2058+21912*u-15876*u**2+19224*u**3+3402*u**4
    jd=(3+u)*(1+3*u)**2
    target=((jn-200*S*jd)*mu[2]-jd*(122*mu[2]**2+224*mu[4]))*d+5760*jd*n
    def maclaurin(poly):
        out={}
        for e,c in poly.t.items():
            h=(e[0],e[1]+2*e[2]+3*e[3],e[2],e[3])
            out[h]=out.get(h,F(0))+c/F(3)**e[2]/F(27)**e[3]
        return P(out)
    mapped=maclaurin(target);dm=maclaurin(d)
    require(all(e[1]>=1 for e in mapped.t),'entire target divisible by total deficitS')
    divided=P({(e[0],e[1]-1,e[2],e[3]):c for e,c in mapped.t.items()})
    require(divided*S==mapped,'normal factor multiplication back')
    box=[(F(1,16),F(1,9)),(F(0),F(1,100)),(F(0),F(1)),(F(0),F(1))]
    records=[]
    for name,poly in [('normal_loss_200',divided),('filtered_Gram_determinant',dm)]:
        values,degrees=bernstein(poly,box)
        for value in values:require(value>0,name+' exact continuous Bernstein sign')
        records.append({'name':name,'degrees':degrees,'entries':len(values),
                        'minimum':str(min(values)),
                        'polynomial_sha256':digest(poly.dump()),
                        'coefficient_sha256':digest(list(map(str,values)))})
    # Entire credited symmetric face, not only selected scalar controls.
    def face(poly):return P({e:c for e,c in poly.t.items() if e[1:]==(0,0,0)})
    require(face(d)==81*(1-u)**4*(1+3*u)**3/4096,'unrestricted filtered Gram face determinant')
    require(face(n)==81*(1-u)**4*(1+3*u)*(9*(1-u)**4+512*u**2)/131072,'full face pinching numerator')
    matrix_controls=definition_controls(mu,d,n,divided,dm)
    return {'normalization':'balanced max norm1, fixed negative unit triple',
            'domain':{'S_upper':'1/100','u_interval':['1/16','1/9'],
                      'Maclaurin_Y_Z_interval':['0','1']},
            'continuous_certificates':records,
            'moment_sha256':digest([p.dump() for p in mu]),
            'trace_sha256':digest([p.dump() for p in traces]),
            'b_sha256':digest([p.dump() for p in b]),
            'det_sha256':digest(d.dump()),'numerator_sha256':digest(n.dump()),
            'definition_controls':matrix_controls,'checks_before_manifest':CHECKS}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-manifest',type=Path)
    args=parser.parse_args()
    record=derive()
    if args.write_manifest:
        args.write_manifest.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        status='AUTHOR_MANIFEST_REGENERATED'
    else:
        require(args.manifest.is_file(),'required compact manifest absent')
        require(record==json.loads(args.manifest.read_text()),'complete exact record equality')
        status='PASS'
    print(json.dumps({'status':status,'checks':CHECKS,
                      'bound_sign_entries':record['continuous_certificates'][0]['entries'],
                      'determinant_sign_entries':record['continuous_certificates'][1]['entries'],
                      'full_definition_controls':len(record['definition_controls']),
                      'canonical_record_sha256':digest(record)} ,sort_keys=True))
if __name__=='__main__':main()
