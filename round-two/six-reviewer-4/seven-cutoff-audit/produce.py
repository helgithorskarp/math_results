"""Fresh orbit proof producer; imported vectors are untrusted attributed DATA."""
import json,sys
from pathlib import Path
from fractions import Fraction as F
from exact import need,canon,ldlt
from model import build

def energy(a,x):return sum(a[i][j]*x[i]*x[j]for i in range(len(x))for j in range(len(x)))
def encode(a):return [[str(x)for x in r]for r in a]
def lower_dyadic(x):
 need(x>0,'positive dyadic input');e=x.numerator.bit_length()-x.denominator.bit_length();v=F(2**e)if e>=0 else F(1,2**(-e))
 if v>x:v/=2
 need(v<=x<2*v,'dyadic bound');return v
def negative(case):
 q=case['q'];m=build(q);keys=m['keys'];W=m['weights'];forms=m['forms'];zeta=[F(1)if not c else F(-1)if c==7 else F(0)for c,z,w in keys]
 orientation=[energy(a,zeta)for a in forms[:5]];need(orientation[0]==0 and orientation[1]>0 and orientation[2:]==[0,0,0],'complete kappa orientation');need(orientation[1]==F(q*(q+1),2)+F(3*(q+1),3*q+5),'closed orientation identity')
 need(len(case['weights'])==len(case['planes'])and len(case['planes'])in (1,2),'all planes');planes=[];total=[F(0)]*5;mass=F(0)
 for plane,weight in zip(case['planes'],case['weights'],strict=True):
  need(plane['endpoint']in ('lower','cap'),'actual endpoint');den=plane['denominator'];need(type(den)is int and den>0,'positive denominator');need(len(plane['coordinates'])==len(keys)and all(type(x)is int for x in plane['coordinates']),'full integer vector');x=[F(v,den)for v in plane['coordinates']];e=[energy(a,x)for a in forms];coef=e[:5]if plane['endpoint']=='lower'else[e[5]]+[-v for v in e[1:5]];weight=F(weight);need(weight>0,'positive dual weight');norm=sum(w*v*v for w,v in zip(W,x,strict=True));mass+=weight*norm
  total=[a+weight*b for a,b in zip(total,coef,strict=True)];planes.append(dict(endpoint=plane['endpoint'],energies=list(map(str,e)),coefficients=list(map(str,coef)),norm_squared=str(norm),weight=str(weight)))
 need(total[0]<0 and total[1]<=0 and total[2:]==[0,0,0],'all-real separate trade/BC obstruction');z_norm=sum(w*v*v for w,v in zip(W,zeta,strict=True));distance=-total[0]/(mass-total[1]*z_norm/orientation[1]);need(distance>0,'robust spectral separation')
 return dict(q=q,N=m['N'],s=m['s'],keys=keys,weights=W,forms=list(map(encode,forms)),orientation=list(map(str,orientation)),orientation_norm_squared=str(z_norm),planes=planes,dual_sum=list(map(str,total)),weighted_vector_norm_squared=str(mass),spectral_separation=str(distance),dyadic_spectral_separation=str(lower_dyadic(distance)))
def positive(case):
 q=case['q'];m=build(q);keys=m['keys'];W=m['weights'];d=len(W);forms=m['forms'];p=list(map(F,[case[x]for x in ('kappa','tb','tc','sigma')]));C=[[forms[0][i][j]+sum(p[k]*forms[k+1][i][j]for k in range(4))for j in range(d)]for i in range(d)];U=[[F(m['N']*W[i]if i==j else 0)-W[i]*W[j]-C[i][j]for j in range(d)]for i in range(d)];star=[bool(c&1)for c,z,w in keys];need(sum(w*x for w,x in zip(W,star))==m['s'],'actual a-star');need(all(sum(C[i][j]*star[j]for j in range(d))==0 for i in range(d)),'forced star');lower=F(case['lower_floor']);upper=F(case['upper_floor']);P=[[F(W[i]if i==j else 0)-F(W[i]*star[i]*W[j]*star[j],m['s'])for j in range(d)]for i in range(d)];A=[[C[i][j]-lower*P[i][j]for j in range(d)]for i in range(d)];B=[[U[i][j]-(upper*W[i]if i==j else 0)for j in range(d)]for i in range(d)];matrices=[C,U,A,B];cert=[ldlt(a)for a in matrices];need([x[0]for x in cert]==[d-1,d,d-1,d],'all complete lower/upper/floored ranks')
 rows=[sum(C[i][j]for j in range(d))/W[i]for i in range(d)];empty=[1-x for x in rows];loop=F(1)+sum(W[i]*rows[i]for i in range(d));h=m['N']-m['s'];empty_M=(loop-m['s'])/h
 return dict(q=q,N=m['N'],s=m['s'],h=h,keys=keys,weights=W,forms=list(map(encode,forms)),positive_forms=list(map(encode,matrices)),congruence_certificates=[dict(rank=r,pivots=piv)for r,piv in cert],original_empty_lower_rows=list(map(str,empty)),original_empty_M_loop=str(empty_M),whole_lower_rank=m['N']-1,whole_cap_rank=m['N']-1,unit_gap=str(upper/h))
if __name__=='__main__':
 w=json.loads(Path(__file__).with_name('INPUT.json').read_text());q=int(sys.argv[1]);need(7<=q<=27,'literal covered q');v=positive(w['positive'])if q==27 else negative(next(c for c in w['negative_cases']if c['q']==q));Path(sys.argv[2]).write_bytes(canon(v));print(json.dumps(dict(complete=True,q=q,orbits=len(v['keys']),separation=v.get('dyadic_spectral_separation'),gap=v.get('unit_gap'))))
