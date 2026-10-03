"""LATE whole native certificate comparison; primary records already sealed.

This stage reads producer expected.json. It is corroboration, not blindness.
No producer executable is imported. Exact stdlib sparse arithmetic decodes
records and checks all ten claimed native maps, including all zero rows.
"""
from fractions import Fraction as F
import pathlib,json,sys,hashlib
P=pathlib.Path(__file__).resolve().parent

def need(q,label):
 if not q:raise ValueError(label)
z=(0,)*12

def dec(row):
 out={}
 for key,value in row:
  need(type(key)==list and len(key)==12 and all(type(i)==int and i>=0 for i in key),'typed nonnegative 12-variable exponent')
  key=tuple(key);need(key not in out,'no duplicate coefficient')
  v=F(value);need(v!=0,'canonical nonzero coefficient');out[key]=v
 return out

def add(*arrays):
 out={}
 for a in arrays:
  for k,v in a.items():out[k]=out.get(k,F(0))+v
 return {k:v for k,v in out.items() if v}
def scale(a,c):return {k:v*c for k,v in a.items() if v*c}
def mul(a,b):
 out={}
 for k,v in a.items():
  for l,w in b.items():
   key=tuple(i+j for i,j in zip(k,l));out[key]=out.get(key,F(0))+v*w
 return {k:v for k,v in out.items() if v}
def var(i):k=list(z);k[i]=1;return {tuple(k):F(1)}
def power(a,n):
 out={z:F(1)}
 for _ in range(n):out=mul(out,a)
 return out
raw=(P/'primary.py.out.json').read_bytes();seal=json.loads((P/'primary-seal.json').read_text());pin=next(r for r in seal['files'] if r['path']=='primary.py.out.json')
need(hashlib.sha256(raw).hexdigest()==pin['sha256'],'entire pre-native primary seal')
own=json.loads(raw);native=json.loads((P/'producer/expected.json').read_text())['whole_maps'];maps=own['maps'];checks=[]
def compare(name,rows):
 left=[dec(q) for q in native[name]];right=[dec(q) for q in rows]
 while len(left)<len(right):left.append({})
 while len(right)<len(left):right.append({})
 need(left==right,'ENTIRE native map '+name)
 checks.append(dict(name=name,polynomials=len(left),coefficients=sum(len(q) for q in left),entire_all_coefficients_equal=True))
for n,k in [('Q','Q'),('ODE','O'),('Phi','Phi'),('rho_p_squared','rho_p2'),('rho_p_Q_minus_pprime','rho_mixed'),('p5_difference_quotients','p5_differences'),('projected_quartic_Phi','projected_quartic')]:compare(n,maps[k])
compare('Newton_tau_0_through_6',maps['trace'][:7])
p0=var(5);cube=[scale(power(p0,3),F(1,512)),{},scale(power(p0,2),F(3,64)),{},scale(p0,F(3,8)),{},{z:F(1)}]
def enc(q):return [[list(k),str(v)] for k,v in sorted(q.items())]
compare('monic_resonance_cube',list(map(enc,cube)))
jet=[var(i) for i in range(5)]+[var(6),{z:F(1)}];rr=[{}]*8
for k,a in enumerate(jet):
 if k:rr[k-1]=add(rr[k-1],scale(mul(p0,a),k));rr[k+1]=add(rr[k+1],scale(a,8*k))
 rr[k+1]=add(rr[k+1],scale(a,-48))
inv=[[dec(q) for q in row] for row in own['resonance_inverse']]
recovered=[add(*(mul(inv[i][j],rr[j+1]) for j in range(6))) for i in range(6)]
need(recovered==[add(jet[i],scale(cube[i],-1)) for i in range(6)],'fresh nilpotent inversion of generic jet, constant residual not discarded')
compare('resonance_inverse',list(map(enc,recovered)))
need(len(checks)==10,'all ten native maps')
print(json.dumps(dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',producer_source_access='after primary seal',not_blind=True,ten_whole_maps_equal=checks,independent_inverse_total_abs_coefficient=own['resonance_inverse_total_abs_coefficient'],independent_inverse_degree=own['resonance_inverse_degree']),sort_keys=True,separators=(',',':')))
