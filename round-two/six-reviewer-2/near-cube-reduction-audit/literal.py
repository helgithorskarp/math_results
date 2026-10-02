"""Full original even/odd literal domains, all matching actions and exact gap metric."""
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from functools import reduce
import json,signal
from linear import need,canonical,digest,psd,mv
from core import constants,complete,free_pairs,sector,projected_upper_form,core_upper_form

def original(n):
 need(type(n)is int and n in[6,7],'ONLYn6/n7 actual original allocations');return[A for A in range(1<<n)if A.bit_count()<=n-2]

def matchings(points):
 if not points:yield();return
 a=points[0]
 for i,b in enumerate(points[1:],1):
  for P in matchings(points[1:i]+points[i+1:]):yield((a,b),)+P

def vector(S,P,a):return[int(A.bit_count()==a)*reduce(lambda t,p:t*(((A>>p[0])&1)-((A>>p[1])&1)),P,1)for A in S]

def rank(rows):
 basis={};chosen=[]
 for ix,row in enumerate(rows):
  v={i:F(x)for i,x in enumerate(row)if x}
  for p,b in sorted(basis.items()):
   t=v.get(p,0)
   if t:
    for i,x in b.items():
     value=v.get(i,F(0))-t*x
     if value:v[i]=value
     else:v.pop(i,None)
  if v:
   p=min(v);d=v[p];basis[p]={i:x/d for i,x in v.items()};chosen.append(ix)
 return len(basis),chosen

def lift(C,n):
 S=original(n);r,N,s,h=constants(n);cr=[sum(row)for row in C];L=[[F(0)]*N for _ in S];L[0][0]=1+sum(cr)
 for i in range(N-1):
  L[0][i+1]=L[i+1][0]=1-cr[i]
  for t in range(N-1):L[i+1][t+1]=1+C[i][t]
 return L

def audit():
 records=[];total_actions=0;total_lifts=0
 for n in[6,7]:
  S=original(n);non=S[1:];r,N,s,h=constants(n);free={p:F(s-1)if sum(p)==n else F(0)for p in free_pairs(n)};beta=complete(n,free);frames=[];chosen_frames=[];norms=0;all_matchings=0;harmonic_dims=[]
  for j in range(n//2+1):
   layers=sector(n,beta,j)['layers'];base_sets=[A for A in range(1<<n)if A.bit_count()==j];Ps=[P for points in combinations(range(n),2*j)for P in matchings(points)];all_matchings+=len(Ps);base=[vector(base_sets,P,j)for P in Ps];dimension,indices=rank(base);need(dimension==__import__('math').comb(n,j)-( __import__('math').comb(n,j-1)if j else 0),'EVERY actual initial harmonic span');harmonic_dims.append(dimension)
   for P in Ps:
    cols=[vector(non,P,a)for a in layers]
    for a,v in zip(layers,cols):need(sum(x*x for x in v)==2**j*__import__('math').comb(n-2*j,a-j),'every actual matching norm including above-middle');norms+=1
    frames.append((j,layers,cols))
   for ix in indices:
    for a in layers:chosen_frames.append((a,vector(non,Ps[ix],a)))
  per_layer=[]
  for a in range(1,r+1):
   cols=[v for b,v in chosen_frames if b==a];positions=[i for i,A in enumerate(non)if A.bit_count()==a];span,_=rank([[v[i]for i in positions]for v in cols]);need(span==len(positions),'ENTIRE actual layer span; including all high layers');per_layer.append([a,len(positions),span])
  need(sum(z[2]for z in per_layer)==N-1 and len(chosen_frames)==N-1,'complete actual nonempty space')
  C=[[F(s*(A==B)-1)+beta.get(tuple(sorted((A.bit_count(),B.bit_count()))),F(0))*int(not(A&B))for B in non]for A in non];U=[[F(N*(i==t)-1)-C[i][t]for t in range(N-1)]for i in range(N-1)];den=lcm(*(x.denominator for row in C+U for x in row));Ci=[[int(x*den)for x in row]for row in C];Ui=[[int(x*den)for x in row]for row in U];actions=[];count=0
  for j,layers,cols in frames:
   g=sector(n,beta,j)
   for bindex,v in enumerate(cols):
    actual=[[sum(x*y for x,y in zip(row,v))for row in A]for A in[Ci,Ui]];predicted=[[sum(int(den*g[field][i][bindex])*cols[i][t]for i in range(len(layers)))for t in range(N-1)]for field in['K','U']];need(actual==predicted,'EVERY literal C/U matching action at every original coordinate');actions.append(actual);count+=2*(N-1)
  stars=[[F(bool(A&(1<<i)))for A in non]for i in range(n)];need(all(not any(mv(C,v))for v in stars),'EVERY actual point-star action');L=lift(C,n);M=[[(x-s*(i==t))/h for t,x in enumerate(row)]for i,row in enumerate(L)];need(all(sum(row)==N for row in L)and all(sum(row)==1 for row in M),'all whole/empty row sums');need(all(M[i][t]==M[t][i]and(not(A&B)or M[i][t]==0)for i,A in enumerate(S)for t,B in enumerate(S)),'EVERY original symmetry/intersection position')
  Q=[[F(i==t)-F(1,N)for t in range(N-1)]for i in range(N-1)];ur=[sum(row)for row in U];EUE=[[sum(ur)if i==t==0 else-ur[t-1]if i==0 else-ur[i-1]if t==0 else U[i-1][t-1]for t in range(N)]for i in range(N)];qr=[sum(row)for row in Q];EQE=[[sum(qr)if i==t==0 else-qr[t-1]if i==0 else-qr[i-1]if t==0 else Q[i-1][t-1]for t in range(N)]for i in range(N)];need(EUE==[[N*F(i==t)-L[i][t]for t in range(N)]for i in range(N)],'ENTIRE actual original cap lift');need(EQE==[[F(i==t)-F(1,N)for t in range(N)]for i in range(N)],'ENTIRE actual projected metric lift, not coreI')
  records.append({'n':n,'actual_N':N,'nonempty':N-1,'all_matchings':all_matchings,'all_matching_columns':norms,'harmonic_dimensions':harmonic_dims,'all_layer_spans':per_layer,'chosen_complete_columns':len(chosen_frames),'actual_C_U_positions':count,'original_lift_positions':N*N,'whole_action_stream_sha256':digest(actions),'whole_C_U_L_M_Q_EUE_EQE_sha256':digest([C,U,L,M,Q,EUE,EQE]),'status':'credited ordinary8106 z1 control, not asserted capped'});total_actions+=count;total_lifts+=2*N*N
 # Known n6 centered beta33=24 baseline, solved anew from explicit free table.
 n=6;r,N,s,h=constants(n);beta=complete(n,{(2,2):F(4,3),(2,3):0,(2,4):22,(3,3):24});S=original(n);non=S[1:];C=[[F(s*(A==B)-1)+beta.get(tuple(sorted((A.bit_count(),B.bit_count()))),F(0))*int(not(A&B))for B in non]for A in non];need(all(sum(row)==0 for row in C),'known centered baseline entire actual zero moment');L=lift(C,n);lower=psd(L);P=[[F(i==t)-F(1,N)for t in range(N)]for i in range(N)];gap=[[N*F(i==t)-L[i][t]-2*P[i][t]for t in range(N)]for i in range(N)];upper=psd(gap);need(lower['rank']==N-n-1 and upper['rank']==N-1,'actual capped baseline and STRICT normalized whole gap2')
 g=sector(n,beta,0);one=[F(1)]*len(g['layers']);reduced=[psd(projected_upper_form(sector(n,beta,j),F(2)))for j in range(4)];core_constant_energy=sum(sum(x for x in row)for row in core_upper_form(g,F(2)));need(core_constant_energy==F(-56),'same delta2 coreI floor fails on actual constant direction')
 example={'n':6,'credited':'known9521 centered beta33=24 baseline, not new construction','whole_L_rank':lower['rank'],'normalized_whole_gap2_certificate':upper,'all4_full_projected_metric_cap_certificates':reduced,'whole_original_L_gap_sha256':digest([L,gap]),'core_U_minus2I_actual_constant_energy':core_constant_energy,'scope':'VALID original cappedH with full gap>=2 but U NOT>=2I. Lower rank50, not greatest51. Separates scalar sufficient floor from exact normalized metric on actual H.'}
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','complete_even_odd_literal_controls':records,'all_actual_C_U_positions':total_actions,'all_original_cap_and_metric_lift_positions':total_lifts,'actual_normalized_metric_separation':example,'scope':'Only actual original n6/n7 allocations. Complete ALL matching/layer/coordinate actions, no random or selected-coordinate control. Ordinary all-order proof supplies universal coverage; prior baseline is explicit credited input.'}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s whole literal; incomplete is not exclusion')));signal.alarm(45);print(json.dumps(canonical(audit()),sort_keys=True,separators=(',',':')))
