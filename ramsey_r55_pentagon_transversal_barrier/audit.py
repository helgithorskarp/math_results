from itertools import combinations
from collections import Counter
from pathlib import Path
from math import comb
import json,sys
lines=[list(map(int,l.split())) for l in Path(sys.argv[1]).read_text().splitlines()];n,m=lines[0]
if n!=43 or len(lines)!=m+1:raise ValueError('header')
a=[0]*n;seen=set()
for u,v in lines[1:]:
 if not 0<=u<v<n or (u,v) in seen:raise ValueError('bad edge')
 seen.add((u,v));a[u]|=1<<v;a[v]|=1<<u
full=(1<<n)-1;blue=[full^(1<<v)^a[v] for v in range(n)]
P=[];bad=[[],[]]
for S in combinations(range(n),5):
 mask=sum(1<<v for v in S);ds=[(a[v]&mask).bit_count() for v in S]
 if all(d==2 for d in ds):P.append(mask)
 if all(d==0 for d in ds):bad[0].append(S)
 if all(d==4 for d in ds):bad[1].append(S)
L=[0]*10+[2,4,7,12];qhist=Counter();row_fails=[];rowW=0
for u,v in combinations(range(n),2):
 col=a if a[u]>>v&1 else blue;N=col[u]&col[v];q=N.bit_count();qhist[q]+=1
 p=sum(mask&N==mask for mask in P);rowW+=p
 if q>13 or p<L[q]:row_fails.append([u,v,q,p])
colW=0;homo=0;maxu=maxe=0;col_fails=[]
for mask in P:
 for ci,col in enumerate((blue,a)):
  N=full^mask
  for v in range(n):
   if mask>>v&1:N&=col[v]
  u=N.bit_count();e=sum((col[v]&N).bit_count() for v in range(n) if N>>v&1)//2
  maxu=max(maxu,u);maxe=max(maxe,e);homo+=u;colW+=e
  if u>13 or e>2*u or e>26:col_fails.append([mask,ci,u,e])
d=[x.bit_count() for x in a];sigma=sum((x-21)**2 for x in d);F=sum(2*(9-q)*v for q,v in qhist.items() if q<=8)+qhist[12]+4*qhist[13]
if rowW!=colW:raise ValueError('W identity')
result={'n':n,'red_edges':m,'degrees':dict(sorted(Counter(d).items())),'same_color_codegrees':dict(sorted(qhist.items())),'P':len(P),'W_by_pairs':rowW,'W_by_cycles':colW,'homogeneous_vertex_cycle_incidences':homo,'max_homogeneous_set_order':maxu,'max_homogeneous_edges':maxe,'sigma':sigma,'F':F,'strong_W_lower':903+3*sigma+F,'degree_window_pass':min(d)>=18 and max(d)<=24,'edge_window_390_513_pass':390<=m<=513,'q_window_pass':max(qhist)<=13,'local_cycle_count_inequalities_pass':not row_fails,'local_failures':row_fails,'homogeneous_caps_pass':not col_fails,'homogeneous_failures':col_fails,'strong_W_inequality_pass':rowW>=903+3*sigma+F,'W_upper_pass':rowW<=2*homo<=52*len(P),'monochromatic_blue_fives':bad[0],'monochromatic_red_fives':bad[1],'ramsey_good':not any(bad),'all_five_sets':comb(n,5),'all_21_sets':comb(n,21)}
print(json.dumps(result,indent=2))
