"""New tuple-set singleton builder (74,15), last15 deletion labels.

No author executable/decoder/oracle, no expansion of earlier bitmask guards.
ALL representative x original-member positions and amplitudes are tested.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
from affine import table
from linear import need,mv,form,canonical,digest
from orbits import forms,vectors
from dual import data

def domain(q,k):
 need((type(q),type(k))==(int,int)and(q,k)==(74,15),'new tuple builder ONLY published74/15 singleton')
 core=frozenset(range(3));outside=tuple(range(3,q+3));Z=frozenset(outside[-k:]);S=[()]
 for r in range(1,4):
  for A in combinations(range(q+3),r):
   aa=frozenset(A)
   if r==3 and(len(aa&core)<2 or(aa&core==frozenset((1,2))and aa&Z)):continue
   S.append(A)
 S.sort();sets=[frozenset(A)for A in S];present=set(S);N=(q*q+13*q+16)//2-k
 need(len(S)==len(set(S))==N and S[0]==(),'complete independent tuple membership census')
 for A in S:
  for j in A:need(tuple(x for x in A if x!=j)in present,'every literal downset edge')
 stars=[sum(j in A for A in sets)for j in range(q+3)];expected=[3*q+4,3*q+4-k,3*q+4-k]+[q+6]*(q-k)+[q+5]*k
 need(stars==expected,'ENTIRE original star counts and actual empty')
 def key(A):return sum(1<<j for j in A&core),len(A&Z),len(A-core-Z)
 return S,sets,Z,key,stars

def coefficients(A,B,N,s,Q,slope):
 if A==B:c=F(s-1);de=F(0)
 elif A&B:c=F(-1);de=F(0)
 else:
  ta=(sum(j<3 for j in A),sum(j>=3 for j in A));tb=(sum(j<3 for j in B),sum(j>=3 for j in B));code=tuple(sorted((ta,tb)));c=Q[code]-1;de=slope[code]
 # Literal set edges independent of bitmask repair helper.
 edge={A,B}if A!=B else set()
 r=F(1)if edge in[{frozenset((0,)),frozenset((1,))},{frozenset((0,)),frozenset((2,))}]else F(-1)if edge in[{frozenset((1,)),frozenset((0,2))},{frozenset((2,)),frozenset((0,1))}]else F(0)
 return c,de,r,F(N*(A==B)-1)-c

def audit():
 q,k=74,15;S,sets,Z,key,stars=domain(q,k);non=sets[1:];N=len(S);s=3*q+4;g=forms(q,k);keys=g['keys'];where={key:j for j,key in enumerate(keys)};indices=[where[key(A)]for A in non];counts=Counter(indices);weights=[counts[i]for i in range(len(keys))]
 need(weights==g['sizes']and len(keys)==23 and len(non)==3211,'ALL physical orbit members/norms')
 representative=[max((A for A in non if key(A)==wanted),key=lambda a:tuple(sorted(a)))for wanted in keys];Q=table(q,0);slope={code:v-Q[code]for code,v in table(q,1).items()};names=['C0','Delta','R','U0'];actual=[[[F(0)]*23 for _ in keys]for unused in names];all_pair_record=[]
 for i,A in enumerate(representative):
  subtotal=[[F(0)]*23 for unused in names]
  for B,j in zip(non,indices):
   vals=coefficients(A,B,N,s,Q,slope)
   for f,value in enumerate(vals):subtotal[f][j]+=value
  for f in range(4):actual[f][i]=[weights[i]*v for v in subtotal[f]]
 for name,A in zip(names,actual):need(A==g[name],'EVERY original representative/member coefficient '+name)
 # Physical frame amplitudes on EVERY member, not one orbit witness.
 vec=[[F(1)for A in non],[F(len(A)==2 and 0 in A and any(j>=3 for j in A))for A in non],[F(bool(A&frozenset((1,2)))and A not in[frozenset((0,1)),frozenset((0,2))])for A in non]]
 orbit_vec=vectors(keys);need(all(v[i]==orbit_vec[j][indices[i]]for j,v in enumerate(vec)for i in range(len(non))),'ALL9633 actual frame amplitudes')
 z=[F(1-int(1 in A)-int(2 in A)+int(sum(j<3 for j in A)>=2))for A in non];z_orbit=[F(1-int(bool(c&2))-int(bool(c&4))+int(c.bit_count()>=2))for c,zz,ww in keys];need(all(z[i]==z_orbit[indices[i]]for i in range(len(non))),'every actual lower orientation amplitude')
 row0=mv(g['C0'],z_orbit);rowR=mv(g['R'],z_orbit);need(not any(row0)and not any(rowR),'all lower kernel rows')
 # Invariance gives the representative action to EVERY actual physical row.
 full_rows=[[row0[i]/weights[i],rowR[i]/weights[i]]for i in indices];need(all(x==y==0 for x,y in full_rows),'ALL3211 original kernel row values')
 a=data(q,k);framegram={name:[[form(g[name],v,w)for w in orbit_vec]for v in orbit_vec]for name in['U0','Delta','R']};need(all(framegram[name]==a[name]for name in framegram),'ENTIRE3space actual Gram')
 w=[255-3*y+v for one,y,v in zip(*vec)];wo=[255-3*y+v for one,y,v in zip(*orbit_vec)];need(all(w[i]==wo[indices[i]]for i in range(len(non))),'EVERY compact integer dual amplitude')
 pairings={name:form(g[name],wo,wo)for name in['U0','Delta','R']};need(pairings=={'U0':F(-1118484,37),'Delta':F(40973507610,227),'R':F(0)},'full original integer negative dual')
 alpha=form(g['Delta'],z_orbit,z_orbit);need(alpha==F(630150,227)>0,'original alpha orientation')
 return {'q':q,'k':k,'N':N,'nonempty_original_members':len(non),'whole_representative_member_positions':23*len(non),'frame_amplitude_positions':3*len(non),'all_kernel_rows':len(non),'all_compact_dual_amplitudes':len(non),'deletion_labels':'last15 outside points, not first15 target coordinate convention','original_domain_sha256':digest(S),'orbit_keys':keys,'norm_weights':weights,'whole_original_four_coefficient_Grams':{name:A for name,A in zip(names,actual)},'full_original_frame_Grams':framegram,'every_frame_amplitude_sha256':digest(vec),'every_original_kernel_row_sha256':digest(full_rows),'every_compact_integer_amplitude_sha256':digest(w),'integer_original_dual_pairings':pairings,'alpha':alpha,'all_star_sizes':stars,'no10310521_full_pair_enumeration_claim':True}

if __name__=='__main__':
 import json,signal
 def alarm(*args):raise TimeoutError('fixed60s original tuple-domain audit; incomplete is not exclusion')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60);print(json.dumps(canonical(audit()),sort_keys=True,separators=(',',':')))
