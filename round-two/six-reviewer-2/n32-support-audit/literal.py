"""Own full n6 original-space action and all-matching harmonic span controls.

Two arbitrary affine star-only tables are diagnostic, NOT PSD constructions.
No native basis/decoder/table imported; actual empty coordinate included.
"""
from fractions import Fraction as F
from itertools import combinations
import json,signal
from linear import need,canonical,digest,mv
from core import constants,complete,sector

def original(n):
 need(type(n)is int and n==6,'ONLYn6 literal allocation; n32 forbidden');return[A for A in range(1<<n)if A.bit_count()<=n-2]

def matchings(points):
 if not points:yield();return
 a=points[0]
 for i,b in enumerate(points[1:],1):
  for rest in matchings(points[1:i]+points[i+1:]):yield((a,b),)+rest

def column(S,pairs,a):
 return[F((A.bit_count()==a)*__import__('functools').reduce(lambda v,p:v*(((A>>p[0])&1)-((A>>p[1])&1)),pairs,1))for A in S]

def basis_span(columns,size):
 basis={};chosen=[]
 for index,c in enumerate(columns):
  v=list(c)
  for p,b in sorted(basis.items()):
   t=v[p]
   if t:v=[x-t*y for x,y in zip(v,b)]
  p=next((i for i,x in enumerate(v)if x),None)
  if p is not None:
   d=v[p];basis[p]=[x/d for x in v];chosen.append(index)
 need(len(basis)==size,'ALL ORIGINAL harmonic columns span entire physical space')
 return {'rank':len(basis),'selected_column_indices':chosen,'whole_basis_sha256':digest(columns)}

def audit():
 n=6;S=original(n);non=S[1:];r,N,s,h=constants(n);need(len(S)==N==57 and len(non)==56,'full actual n6 downset includingempty');frames=[];groups=[];matching_count=0
 for j in range(4):
  g=sector(n,complete(n,{(2,2):0,(2,3):0,(2,4):0,(3,3):0})[0],j);layers=g['layers']
  for points in combinations(range(n),2*j):
   for P in matchings(points):
    matching_count+=1;vectors=[column(non,P,a)for a in layers];start=len(frames);frames.extend(vectors);groups.append((j,layers,P,vectors,start))
    need(all(sum(x*x for x in v)==2**j*metric for v,metric in zip(vectors,g['metric'])),'every actual harmonic norm, including above-middle')
 span=basis_span(frames,56);need(matching_count==76 and len(frames)==214,'ENTIRE chosen matching/column census')
 records=[]
 for values in[[-3,4,5,-7],[9,-2,11,3]]:
  free=dict(zip([(2,2),(2,3),(2,4),(3,3)],values));beta,dec=complete(n,free);C=[[F(s*(A==B)-1)+beta.get(tuple(sorted((A.bit_count(),B.bit_count()))),F(0))*int(not(A&B))for B in non]for A in non];U=[[F(N*(A==B)-1)-C[i][t]for t,B in enumerate(non)]for i,A in enumerate(non)]
  actions=[]
  for j,layers,P,vectors,start in groups:
   g=sector(n,beta,j)
   for col,(b,v)in enumerate(zip(layers,vectors)):
    actual=[mv(C,v),mv(U,v)];predicted=[[sum(g[name][row][col]*vectors[row][i]for row in range(len(layers)))for i in range(56)]for name in ['K','U']];need(actual==predicted,'EVERY literal original C/U action column');actions.append(actual)
  stars=[[F(bool(A&(1<<i)))for A in non]for i in range(n)];need(all(not any(mv(C,v))for v in stars),'ALL actual point-star kernel rows')
  cr=[sum(row)for row in C];empty=1+sum(cr);L=[[F(0)]*N for A in S]
  L[0][0]=empty
  for i in range(56):
   L[0][i+1]=L[i+1][0]=1-cr[i]
   for t in range(56):L[i+1][t+1]=1+C[i][t]
  M=[[(x-s*(i==t))/h for t,x in enumerate(row)]for i,row in enumerate(L)]
  need(all(sum(row)==N for row in L)and all(sum(row)==1 for row in M),'EVERY actual whole row/empty row')
  need(all(M[i][t]==M[t][i]and(not(A&B)or M[i][t]==0)for i,A in enumerate(S)for t,B in enumerate(S)),'ENTIRE original symmetry/intersectionsupport includingemptyloop')
  # Direct EUE^T coefficient construction, independent from wholeL decoder.
  ur=[sum(row)for row in U];V=[[sum(ur)if i==t==0 else-ur[t-1]if i==0 else-ur[i-1]if t==0 else U[i-1][t-1]for t in range(N)]for i in range(N)];need(V==[[F(N*(i==t))-L[i][t]for t in range(N)]for i in range(N)],'ALL whole original lift/cap identity entries')
  records.append({'free_values':values,'all_action_positions':2*214*56,'all_original_lift_positions':N*N,'whole_actions_sha256':digest(actions),'whole_C_U_L_M_sha256':digest([C,U,L,M]),'actual_empty_L_loop':empty,'actual_empty_M_loop':M[0][0],'all_stars_action_sha256':digest([mv(C,v)for v in stars]),'status':'full affine/control family, NOT assertedPSD orcapped'})
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','n':6,'actual_original_order':57,'nonempty_order':56,'all_matchings':matching_count,'harmonic_columns':len(frames),'whole_harmonic_span':span,'two_full_original_controls':records,'total_action_positions':2*2*214*56,'scope':'EVERY column/member/wholelift entry in these complete original domains. Algebraic n32 harmonic completeness is proved separately, not extrapolated from n6.'}

if __name__=='__main__':
 def alarm(*args):raise TimeoutError('fixed45s fulloriginal control; incomplete is not exclusion')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(45);print(json.dumps(canonical(audit()),sort_keys=True,separators=(',',':')))
