#!/usr/bin/env python3
"""Complete exact geometry and explicit colour check of the named474-point assembly."""
from pathlib import Path
from hashlib import sha256
from math import lcm
from fractions import Fraction as F
import argparse,json,time
import projection as P
K=P.K;ROOT=P.ROOT
INPUT=ROOT/'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv'
INPUT_SHA='4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02'
D0,D1=330,-42;D=K.element(D0,D1);DREAL=D[:2]

def source():
 raw=INPUT.read_bytes();P.need(sha256(raw).hexdigest()==INPUT_SHA,'point input hash');A=[]
 for l in raw.decode().splitlines():
  if not l or l.startswith('#'):continue
  v=tuple(map(int,l.split()));P.need(len(v)==16 and all(v[k]==0 for k in range(16) if k not in (0,5,9,12)),'point basis');A.append(K.element(*(F(v[k],12) for k in (0,5,9,12))))
 P.need(len(A)==len(set(A))==159 and A[0]==K.ZERO,'source points');return A

def unit(q,s):
 a,b,c,d,e,f,g,h=q;n=e*e+33*f*f+3*g*g+11*h*h;m=2*(e*f+g*h)
 return (a*a+33*b*b+3*c*c+11*d*d+D0*n+33*D1*m==s*s and
  2*(a*b+c*d)+D1*n+D0*m==0 and a*e+33*b*f+3*c*g+11*d*h==0 and a*f+b*e+c*h+d*g==0)

# Independent generic quotient reduction in R[t], r^2=33, t^2=D0+D1*r.
TABLE=[]
for i in range(4):
 for j in range(4):
  k=i^j;v=33 if (i&j&1) else 1
  TABLE.append([(k,v)] if not(i&j&2) else [(k,v*D0),(k^1,v*D1*(33 if k&1 else 1))])
def ring_mul(x,y):
 out=[0]*4
 for i,a in enumerate(x):
  for j,b in enumerate(y):
   for k,m in TABLE[4*i+j]:out[k]+=a*b*m
 return out

def cartesian_unit(q,s):
 a,b,c,d,e,f,g,h=q;x=ring_mul((3*a,3*b,3*e,3*f),(3*a,3*b,3*e,3*f));y=ring_mul((3*c,d,3*g,h),(3*c,d,3*g,h));return [a+3*b for a,b in zip(x,y)]==[9*s*s,0,0,0]

def build():
 A=source();u=(K.element(-F(3,32),F(3,32),-F(1,32),F(3,32)),K.element(-F(1,64),-F(1,192),F(1,64),F(1,64)));T=K.element(-F(3,16),F(3,16),-F(1,16),F(3,16));V=K.element(F(1,2),0,F(1,2),0)
 P.need(P.mul(u,P.conj(u),D)==P.ONE,'unit multiplier');P.need(P.add(P.sub(P.mul(u,u,D),P.mul((T,K.ZERO),u,D)),(V,K.ZERO))==P.ZERO,'named quadratic')
 B=[(a,K.ZERO) for a in A]+[P.mul(u,(a,K.ZERO),D) for a in A[1:]];P.need(len(set(B))==317,'base collisions')
 a,b,c,d=18,113,13,28;edge=P.sub(B[158+b],B[a]);v=K.conjugate(K.add(A[d],K.negate(A[c])));P.need(K.is_unit(v) and P.mul(edge,P.conj(edge),D)==P.ONE,'bridge source and target units')
 third=[P.add(B[a],P.mul(edge,(K.multiply(v,K.add(z,K.negate(A[c]))),K.ZERO),D)) for z in A]
 P.need(len(set(third))==159 and set(B)&set(third)=={B[a],B[158+b]},'physical overlaps');points=list(dict.fromkeys(B+third));P.need(len(points)==474,'physical size')
 den=lcm(*(q.denominator for p in points for x in p for q in x));nums=[tuple(int(q*den) for x in p for q in x) for p in points];word=''.join(str(P.color(p,DREAL)) for p in points)
 return nums,den,word

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args();W=args.work;W.mkdir(parents=True,exist_ok=True);started=time.monotonic();pts,s,word=build();ee=[];checks=0
 for i,p in enumerate(pts):
  for j in range(i):
   d=tuple(a-b for a,b in zip(p,pts[j]));u=unit(d,s);P.need(u==cartesian_unit(d,s),'metric formula disagreement');checks+=1
   if u:ee.append((j,i))
 P.need(all(word[a]!=word[b] for a,b in ee),'monochromatic edge');be=[(a,b) for a,b in ee if b<317];cross=sorted((a,b-158) for a,b in be if 0<a<159<=b)
 P.need(len(be)==1308 and len(cross)==16 and len(ee)==1953,'edge inventory')
 point_bytes=('\n'.join(' '.join(map(str,p)) for p in pts)+'\n').encode();edge_bytes=('\n'.join(f'{a} {b}' for a,b in ee)+'\n').encode()
 out={'status':'EXACT_PHYSICAL_FOUR_COLOURING','vertices':474,'edges':len(ee),'pair_checks':checks,'denominator':s,'max_coefficient':max(abs(x) for p in pts for x in p),'base_vertices':317,'base_edges':len(be),'cross_edges':cross,'source_edge':[13,28],'target_bridge':[18,113],'D_valuation_plus':P.certify_radicand(DREAL),'point_sha256':sha256(point_bytes).hexdigest(),'edge_sha256':sha256(edge_bytes).hexdigest(),'word_sha256':sha256(word.encode()).hexdigest(),'sat_calls':0,'seconds':time.monotonic()-started}
 (W/'physical.json').write_text(json.dumps({'points':pts,'denominator':s,'edges':ee,'word':word},separators=(',',':'))+'\n');(W/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
