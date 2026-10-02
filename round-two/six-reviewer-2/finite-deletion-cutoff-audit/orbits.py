"""Fresh actual membership and weighted fixed forms; no target decoder/import."""
from fractions import Fraction as F
from math import comb
from affine import table,repair
from linear import need,mv,form,psd,digest
from dual import domain,data

def choose(n,r):return comb(n,r)if 0<=r<=n else 0
def counts(q,k):
 domain(q,k);keys=[];weights=[]
 for core in range(8):
  for z in range(4):
   for w in range(4):
    r=core.bit_count()+z+w
    if not 1<=r<=3 or(r==3 and core.bit_count()<2)or(core,z,w)==(6,1,0):continue
    size=choose(k,z)*choose(q-k,w)
    if size:keys.append((core,z,w));weights.append(size)
 need(sum(weights)==(q*q+13*q+16)//2-k-1,'ALL original nonempty orbit cardinality')
 return keys,weights

def forms(q,k):
 keys,sizes=counts(q,k);s=3*q+4;N=(q*q+13*q+16)//2-k;Q=table(q,0);slope={key:v-Q[key]for key,v in table(q,1).items()};d=len(keys);C0=[];Delta=[];R=[]
 for i,(c,z,w)in enumerate(keys):
  cr=[];dr=[];rr=[]
  for j,(cc,zz,ww)in enumerate(keys):
   no=0 if c&cc else choose(k-z,zz)*choose(q-k-w,ww)
   # The factor sizes[i]*no counts EVERY ordered disjoint original pair.
   value=F(s*sizes[i]*(i==j)-sizes[i]*sizes[j]);der=F(0)
   if no:
    key=tuple(sorted(((c.bit_count(),z+w),(cc.bit_count(),zz+ww))));value+=sizes[i]*no*Q[key];der=sizes[i]*no*slope[key]
   rep=repair(c,cc)if z+w+zz+ww==0 else F(0)
   cr.append(value);dr.append(der);rr.append(rep)
  C0.append(cr);Delta.append(dr);R.append(rr)
 U0=[[F(N*sizes[i]*(i==j)-sizes[i]*sizes[j])-C0[i][j]for j in range(d)]for i in range(d)]
 for A in[C0,Delta,R,U0]:need(all(A[i][j]==A[j][i]for i in range(d)for j in range(d)),'every weighted form symmetric')
 star=[int(bool(c&1))for c,z,w in keys];need(sum(w*a for w,a in zip(sizes,star))==s,'weighted a-star physical norm')
 return {'keys':keys,'sizes':sizes,'C0':C0,'Delta':Delta,'R':R,'U0':U0,'star':star,'N':N,'s':s}

def vectors(keys):
 return [[F(1)]*len(keys),[F(c==1 and z+w==1)for c,z,w in keys],[F(bool(c&6)and not(z+w==0 and c in[3,5]))for c,z,w in keys]]

def three_space(q,k):
 g=forms(q,k);vec=vectors(g['keys']);a=data(q,k)
 for name in['U0','Delta','R']:
  actual=[[form(g[name],v,w)for w in vec]for v in vec];need(actual==a[name],'ALL nine original '+name+' frame fields')
 z=[F(1-int(bool(c&2))-int(bool(c&4))+int(c.bit_count()>=2))for c,zz,ww in g['keys']]
 need(not any(mv(g['C0'],z))and not any(mv(g['R'],z)),'all lower orientation kernel rows')
 alpha=F(q*(q+1),2)+F(3*(q+1),3*q+5);need(form(g['Delta'],z,z)==alpha>0,'exact original lower orientation')
 need(a['T']>0 and a['V']>0 and a['D']>0 and a['d']>0,'exact positive dual quantities')
 u=[one-a['a']*y-a['b']*v for one,y,v in zip(*vec)]
 need(form(g['U0'],u,u)==a['Q']and form(g['Delta'],u,u)==a['d']and form(g['R'],u,u)==0,'actual original dual pairing')
 return a|{'orbits':len(g['keys']),'alpha':alpha,'original_kernel_vector':z,'dual_original_orbit_amplitudes':u,'whole_original_forms_sha256':digest([g[n]for n in['C0','Delta','R','U0']])}
