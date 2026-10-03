"""Fresh actual-labelled k6 reconstruction using explicitly reused OWN table.

No producer executable or fixture is imported. The original 20-type affine
table and congruence kernel are byte-identical OWN9807, source1af2899533.
Every new coefficient is constructed over the actual ordered member pairs.
"""
from itertools import combinations
from math import lcm
from fractions import Fraction as F
from exact import need
import original as O

def build(q,k=6):
 need(type(q)is int and type(k)is int and 6<=q<=23 and 0<=k<=q,'bounded independently checked original domain')
 X=[0]
 for size in [1,2,3]:
  for pts in combinations(range(q+3),size):
   core=[i for i in pts if i<3];outside=[i-3 for i in pts if i>=3]
   if size==3 and len(core)<2:continue
   if core==[1,2] and len(outside)==1 and outside[0]<k:continue
   X.append(sum(1<<i for i in pts))
 N=len(X);s=3*q+4;n=N-1;need(N==(q*q+13*q+16)//2-k,'actual whole size')
 T=O.table(q);den=lcm(*(v.denominator for p in T.values() for v in p));table={key:(int((a-1)*den),int(b*den)) for key,(a,b) in T.items()}
 A=X[1:];types=[((v&7).bit_count(),(v>>3).bit_count()) for v in A];C=[];D=[]
 for i,v in enumerate(A):
  r=[];d=[]
  for j,w in enumerate(A):
   if i==j:a,b=(s-1)*den,0
   elif v&w:a,b=-den,0
   else:a,b=table[tuple(sorted((types[i],types[j])))]
   r.append(a);d.append(b)
  C.append(r);D.append(d)
 keys=[];ix={v:i for i,v in enumerate(A)};groups={};g=[]
 for v in A:
  z=((v>>3)&((1<<k)-1)).bit_count();key=(v&7,z,(v>>3).bit_count()-z)
  if key not in groups:groups[key]=len(keys);keys.append(key)
  g.append(groups[key])
 weights=[g.count(i) for i in range(len(keys))]
 return dict(q=q,k=k,X=X,N=N,s=s,den=den,C=C,D=D,ix=ix,keys=keys,g=g,weights=weights)

def moments(data):
 q,k,N,s,den,C,D=(data[n] for n in ['q','k','N','s','den','C','D']);n=N-1
 one,y,stars,tri,z,h,ds,v=O.vectors(data);U=[[den*(N*int(i==j)-1)-C[i][j] for j in range(n)] for i in range(n)]
 alpha=F(q*(q+1),2)+F(3*(q+1),3*q+5)
 need(O.pairing(C,z,z,den)==0 and O.pairing(D,z,z,den)==alpha,'actual orientation energies')
 need(all(sum(a*b for a,b in zip(row,z))==0 for row in C),'every actual orientation action')
 for a in [C,D]:need(all(sum(x*y for x,y in zip(row,stars[0]))==0 for row in a),'all original a-star actions')
 for vec in [z,stars[0]]:
  amp=O.core_amplitudes(data,vec)
  for repair in ['Rb','Rc','B']:
   need(all(O.edge({j:int(j==i) for j in amp},amp,repair)==0 for i in amp),'every literal repair annihilates orientation and a-star')
 e=F(q*q+(13-6*k)*q+2*k*k-10*k+14,2);ell=5*q+4-k;gap=N-s;A=(2*k+1)*q+k-F(2*k,q);B=-(q-k)*s-k*(3+F(2,q));V=ell*gap-4*q*s;cc=ell*(1-k)
 S=F(q*(q+1),2)+F(3*(q+1)-2*k,3*q+5);hh=F(1,3*q+5)
 vectors=[one,y,v];gu=[[O.pairing(U,a,b,den) for b in vectors] for a in vectors];gd=[[O.pairing(D,a,b,den) for b in vectors] for a in vectors]
 need(gu==[[e,A,cc],[A,q*gap,B],[cc,B,V]],'EVERY original three-direction moment entry')
 need(gd==[[S,q*hh,(2*q-k)*hh],[q*hh,0,0],[(2*q-k)*hh,0,0]],'EVERY original three-direction slope entry')
 amps=[O.core_amplitudes(data,a) for a in vectors]
 for repair in ['Rb','Rc']:need(all(O.edge(a,b,repair)==0 for a in amps for b in amps),'both independent trade Gram matrices vanish')
 need([[O.edge(a,b,'B') for b in amps] for a in amps]==[[2,0,2],[0,0,0],[2,0,2]],'entire BC rank-one Gram')
 c=F((3*q+2)*s*(3*q*q+3*q-2),3*(12*q**3+19*q*q+4*q-4));denom=3*(12*q**3+19*q*q+4*q-4)
 theta=[F(27*q**3+39*q*q+4*q-12,denom),F(-(3*q-2)*(6*q*q+11*q+6),denom),F(4*q*(3*q+4),denom),F((3*q+2)**2,denom),F((3*q-2)*(3*q+2),denom)]
 wl=[hh0+sum(t*d[i] for t,d in zip(theta,ds)) for i,hh0 in enumerate(h)];al=O.core_amplitudes(data,wl)
 need(O.pairing(C,wl,wl,den)==2*c and O.pairing(D,wl,wl,den)==0,'entire actual lower BC scalar')
 need([O.edge(al,al,n) for n in ['Rb','Rc','B']]==[0,0,2],'both independent lower trade zeros and BC2')
 need(q*gap>0 and q*gap*(V+2*c)-B*B>0,'actual adjusted block positivity')
 det=q*gap*(V+2*c)-B*B;aa=((V+2*c)*A-B*(cc+2*c))/det;bb=(q*gap*(cc+2*c)-B*A)/det
 wc=[1-aa*yi-bb*vi for yi,vi in zip(y,v)];Q=e+2*c-aa*A-bb*(cc+2*c);dstar=S-2*hh*(aa*q+bb*(2*q-k));bc=2*(1-bb)**2
 need(O.pairing(U,wc,wc,den)+c*bc==Q and O.pairing(D,wc,wc,den)==dstar,'complete actual adjusted dual energies')
 need(dstar>0 and alpha>0,'positive original orientation and adjusted slopes')
 for name in ['Rb','Rc']:need(O.edge(O.core_amplitudes(data,wc),O.core_amplitudes(data,wc),name)==0,'separate actual adjusted trade cancellation')
 if k==6 and q<=18:need(e+2*c<0,'all-real negative mean')
 if k==6 and q in [19,20]:need(Q<0,'all-real adjusted residual exclusion')
 if k==6 and q==21:need(Q>0,'adjusted residual deliberately supplies NO q21 exclusion')
 return {'q':q,'k':k,'N':N,'s':s,'physical_weights':data['weights'],'orbit_keys':[list(x) for x in data['keys']],'original_ordered_positions':n*n,'orientation':str(alpha),'lower_c':str(c),'entire_moment_Gram':[[str(x) for x in row] for row in gu],'entire_slope_Gram':[[str(x) for x in row] for row in gd],'mean_plus_2c':str(e+2*c),'a':str(aa),'b':str(bb),'Qstar':str(Q),'dstar':str(dstar)}

def positive(data):
 q,N,s,den,C,D,ix=(data[n] for n in ['q','N','s','den','C','D','ix']);n=N-1;need(data['k']==6 and q in [22,23],'two new actual positive orders')
 scale=den*4096;Cp=[[4096*C[i][j]+D[i][j] for j in range(n)] for i in range(n)]
 for a,b,v in [(1,2,8),(2,5,-8),(1,4,8),(4,3,-8),(2,4,-10)]:
  i,j=ix[a],ix[b];Cp[i][j]+=scale*v;Cp[j][i]+=scale*v
 Up=[[scale*(N*int(i==j)-1)-Cp[i][j] for j in range(n)] for i in range(n)]
 G=O.compression(Cp,data,scale);H=O.compression(Up,data,scale);w=data['weights'];m=len(w);chi=[int(bool(key[0]&1)) for key in data['keys']];ha=[a*b for a,b in zip(w,chi)]
 need(m==23 and sum(ha)==s,'complete fixed dimension and physical a-star norm')
 floors={'lower':G,'cap':H,'lower_floor':[[G[i][j]-F(1,65536)*(w[i]*int(i==j)-F(ha[i]*ha[j],s)) for j in range(m)] for i in range(m)],'cap_floor':[[H[i][j]-F(w[i]*int(i==j),65536) for j in range(m)] for i in range(m)]}
 cert={name:O.psd(mat) for name,mat in floors.items()};need([cert[x]['rank'] for x in floors]==[22,23,22,23],'entire weighted original endpoints and sufficient floors')
 star=[int(bool(x&1)) for x in data['X'][1:]]
 need(all(sum(a*b for a,b in zip(row,star))==0 for row in Cp),'every actual positive star action')
 rs=list(map(sum,Cp));total=sum(rs);urs=list(map(sum,Up));utotal=sum(urs);checks=0
 for i,A in enumerate(data['X']):
  for j,B in enumerate(data['X']):
   L=scale+total if i==j==0 else (scale-rs[j-1] if i==0 else (scale-rs[i-1] if j==0 else scale+Cp[i-1][j-1]))
   eu=utotal if i==j==0 else (-urs[j-1] if i==0 else (-urs[i-1] if j==0 else Up[i-1][j-1]))
   need(scale*N*int(i==j)-L==eu,'every actual-empty EUE lifted position')
   if A&B:need(L==scale*s*int(i==j),'every actual intersecting support including original loops')
   checks+=1
 need(all(A^(1<<j) in data['X'] for A in data['X'] for j in range(q+3) if A&(1<<j)),'all immediate downset inclusions')
 sizes=[sum(bool(A&(1<<i)) for A in data['X']) for i in range(q+3)]
 need(sizes==[s,s-6,s-6]+[q+5]*6+[q+6]*(q-6),'EVERY labelled maximum and deleted/retained star')
 for name,mat in [('lower',Cp),('slope',D)]:
  seen={}
  for i,row in enumerate(mat):
   sums=[0]*m
   for j,x in enumerate(row):sums[data['g'][j]]+=x
   g=data['g'][i]
   if g in seen:need(sums==seen[g],'EVERY actual row fixed-space invariance '+name)
   else:seen[g]=sums
 # Original-space symmetric row norm controls all real independent repair changes.
 dnorm=F(max(sum(abs(x) for x in row) for row in D),den)
 degree={v:0 for v in [1,2,4,3,5]}
 for a,b in [(1,2),(2,5),(1,4),(4,3),(2,4)]:degree[a]+=1;degree[b]+=1
 repairnorm=max(degree.values());need(repairnorm==3,'complete union of independent literal repair row degrees')
 radius=F(1,131072)/(dnorm+repairnorm)
 need(radius*(dnorm+3)==F(1,131072),'full four-parameter closed-box perturbation budget')
 need(radius<F(1,4096) and F(1,4096)+radius<F(1,8),'all perturbed kappa remain in credited complementary spectral regime')
 return {'q':q,'N':N,'s':s,'parameters':['1/4096','8','8','-10'],'whole_forms':{name:[[str(x) for x in row] for row in mat] for name,mat in floors.items()},'exact_congruences':cert,'all_actual_empty_positions':checks,'fixed_dimension':m,'complement_dimension':n-m,'lower_cap_endpoint_ranks':N-1,'whole_unit_gap':str(F(1,65536*(N-s))),'star_sizes':sizes,'Delta_max_absolute_row_sum':str(dnorm),'literal_repair_row_degrees':{str(k):v for k,v in degree.items()},'proved_closed_parameter_box_radius':str(radius),'robust_lower_and_cap_floors':'1/131072','robust_whole_unit_gap':str(F(1,131072*(N-s))),'whole_complement_math_input':'credited9195 undeleted lower kappa/2 and upper2s; original repairs vanish on omitted space'}

def joint(data,vectors,weights):
 need(data['q']==21 and data['k']==6 and len(vectors)==3 and len(weights)==3,'complete physical q21 joint input')
 need(all(w>0 for w in weights) and sum(weights)==1,'all positive normalized dual weights')
 n=data['N']-1;den=data['den'];C=data['C'];D=data['D'];U=[[den*(data['N']*int(i==j)-1)-C[i][j] for j in range(n)] for i in range(n)];rows=[];pairs=[]
 for index,v in enumerate(vectors):
  need(len(v)==n and all(isinstance(x,(int,F)) for x in v),'complete exact actual-labelled vector')
  am=O.core_amplitudes(data,v);lower=[O.pairing(C,v,v,den),O.pairing(D,v,v,den),*[F(O.edge(am,am,name)) for name in ['Rb','Rc','B']]]
  cap=[O.pairing(U,v,v,den),-lower[1],*[-x for x in lower[2:]]]
  pairs.append({'lower':list(map(str,lower)),'cap':list(map(str,cap))})
  rows.append(cap if index<2 else lower)
 combined=[sum((w*row[j] for w,row in zip(weights,rows)),F(0)) for j in range(5)]
 need(combined[2:]==[0,0,0],'BOTH independent real trades and BC cancel separately')
 need(combined[0]<-F(1,256) and combined[1]<0,'whole strict original joint dual contradiction for ALL kappa>=0')
 return {'all_six_original_energy_rows':pairs,'selected_three_rows':[[str(x) for x in row] for row in rows],'all_original_affine_dual_coefficients':list(map(str,combined)),'actual_original_positions':n*n,'all_real_independent_repairs_excluded':True}
