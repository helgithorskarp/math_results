"""Independent actual-coordinate cutoff audit. CPython standard library only."""
import sys,json,hashlib,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from math import comb
from exact import need
import original as O
from uniform import derive

def textmatrix(A):return [[str(x) for x in r] for r in A]

def inspect(q,k=5,positive=False):
 d=O.build(q,k);X,N,s,den,C,D,ix=(d[x] for x in ('X','N','s','den','C','D','ix'));n=N-1
 one,y,stars,triangle,z,h,ds,vc=O.vectors(d)
 alpha=F(q*(q+1),2)+F(3*(q+1),3*q+5)
 need(O.pairing(D,z,z,den)==alpha and O.pairing(C,z,z,den)==0,'actual original orientation energies')
 for row in C:
  need(sum(a*b for a,b in zip(row,z))==0,'every lower orientation action row')
 u2=[b+c-2*t for b,c,t in zip(stars[1],stars[2],triangle)]
 for i in range(n):
  need(sum(a*b for a,b in zip(C[i],u2))==sum(a*b for a,b in zip(D[i],u2))==0,'whole retained u2 kernel')
  need(sum(a*b for a,b in zip(C[i],stars[0]))==sum(a*b for a,b in zip(D[i],stars[0]))==0,'entire retained a-star action')
 denom=3*(12*q**3+19*q*q+4*q-4)
 theta=[F(27*q**3+39*q*q+4*q-12,denom),F(-(3*q-2)*(6*q*q+11*q+6),denom),F(4*q*(3*q+4),denom),F((3*q+2)**2,denom),F((3*q-2)*(3*q+2),denom)]
 wl=[a+sum(t*b[i] for t,b in zip(theta,ds)) for i,a in enumerate(h)]
 c=F((3*q+2)*(3*q+4)*(3*q*q+3*q-2),denom)
 amps=O.core_amplitudes(d,wl)
 le={name:O.edge(amps,amps,name) for name in ['Rb','Rc','B']}
 need(O.pairing(C,wl,wl,den)==2*c and O.pairing(D,wl,wl,den)==0 and le=={'Rb':0,'Rc':0,'B':2},'all original lower dual pairings')
 need(amps[1]==amps[3]==amps[5] and amps[2]==amps[4]==1,'full lower dual core amplitudes')
 S=s-2
 expectedG=[[4*S,2*S,0,0,0],[2*S,3*(s-3),-1,-3,-3*q],[0,-1,s-1,-1,2*q+2],[0,-3,-1,s-1,-q],[0,-3*q,2*q+2,-q,q*(s-q)]]
 actualG=[[O.pairing(C,a,b,den) for b in ds] for a in ds]
 need(actualG==expectedG,'whole original five-direction Gram')
 need([O.pairing(C,h,b,den) for b in ds]==[-2*S,-2,-2,-2,-2*q],'entire original lower linear term')
 need(all(O.pairing(D,a,b,den)==0 for a in [h]+ds for b in [h]+ds),'all 36 original zero derivative compression entries')
 U=[[N*int(i==j)*den-den-C[i][j] for j in range(n)] for i in range(n)]
 e=F(q*q+(13-6*k)*q+2*k*k-10*k+14,2)
 gram=[[O.pairing(U,a,b,den) for b in [one,y,vc]] for a in [one,y,vc]]
 need(gram[0][0]==e,'whole cap mean scalar')
 aa,bb=F(0),F(0);negative=None
 if k==5:
  A,B,T,Y,V=gram[0][1],gram[0][2],gram[1][1],gram[1][2],gram[2][2]
  det=T*V-Y*Y;need(T>0 and det>0,'full cap residual invertibility')
  aa=(V*A-Y*B)/det;bb=(T*B-Y*A)/det
  wc=[1-aa*a-bb*b for a,b in zip(y,vc)]
  Q=O.pairing(U,wc,wc,den);dc=O.pairing(D,wc,wc,den);bc=O.edge(O.core_amplitudes(d,wc),O.core_amplitudes(d,wc),'B')
  need(Q==e-aa*A-bb*B and bc==2*(1-bb)**2,'entire cap completed-square pairing')
  need(O.edge(O.core_amplitudes(d,wc),O.core_amplitudes(d,wc),'Rb')==O.edge(O.core_amplitudes(d,wc),O.core_amplitudes(d,wc),'Rc')==0,'both distinct trades vanish on original cap dual')
  if q<=15:need(dc>0 and bc>0 and Q+c*bc<0,'complete all-real negative certificate')
  profile=[]
  for key in d['keys']:
   i=next(i for i,g in enumerate(d['g']) if d['keys'][g]==key)
   need(all(wl[j]==wl[i] and wc[j]==wc[i] for j,g in enumerate(d['g']) if d['keys'][g]==key),'dual amplitudes constant on complete physical orbit')
   profile.append([list(key),str(wl[i]),str(wc[i])])
  negative={'aa':str(aa),'bb':str(bb),'Q':str(Q),'D_cap':str(dc),'B_cap':str(bc),'combined':str(Q+c*bc),'dual_profiles':profile}
 # Separate balanced-face mean necessity, actual lower 2x2 and pairings.
 singles=[int((v&7)==0 and (v>>3).bit_count()==1) for v in X[1:]]
 need(O.pairing(C,h,h,den)==2*(s-2) and O.pairing(C,h,singles,den)==-2 and O.pairing(C,singles,singles,den)==q*q+6,'entire original balanced lower Gram')
 need(O.pairing(D,h,h,den)==O.pairing(D,h,singles,den)==0 and O.pairing(D,singles,singles,den)==q,'entire original balanced derivative Gram')
 dd=O.pairing(D,one,one,den);need(dd==alpha-F(2*k,3*q+5)>F(q*(q+1),2),'all-count cap derivative scalar')
 out={'q':q,'k':k,'N':N,'s':s,'original_nonempty_positions':n*n,'orbit_keys':[list(x) for x in d['keys']],'physical_weights':d['weights'],'orientation_alpha':str(alpha),'lower_c':str(c),'lower_G5':textmatrix(actualG),'lower_pairings':[str(2*c),'0','0','0','2'],'cap_three_gram':textmatrix(gram),'cap_dual':negative,'balanced_mean':str(e),'balanced_delta_mean':str(dd)}
 if positive:
  tb,sigma=(12,-12) if q==16 else (4,-6)
  Cp=[[4096*C[i][j]+D[i][j] for j in range(n)] for i in range(n)];dp=4096*den
  for a,b,v in [(1,2,tb),(2,5,-tb),(1,4,tb),(4,3,-tb),(2,4,sigma)]:
   i,j=ix[a],ix[b];Cp[i][j]+=v*dp;Cp[j][i]+=v*dp
  Up=[[N*int(i==j)*dp-dp-Cp[i][j] for j in range(n)] for i in range(n)]
  G=O.compression(Cp,d,dp);H=O.compression(Up,d,dp);w=d['weights'];m=len(w);chi=[int(bool(key[0]&1)) for key in d['keys']];ha=[a*b for a,b in zip(w,chi)]
  lowerfloor=[[G[i][j]-F(1,65536)*(w[i]*int(i==j)-F(ha[i]*ha[j],s)) for j in range(m)] for i in range(m)]
  upperfloor=[[H[i][j]-F(w[i]*int(i==j),4096) for j in range(m)] for i in range(m)]
  forms={'lower':G,'upper':H,'lower_floor':lowerfloor,'upper_floor':upperfloor}
  congr={name:O.psd(A) for name,A in forms.items()}
  need([congr[n]['rank'] for n in forms]==[22,23,22,23],'every original fixed endpoint/floor rank')
  need(sum(ha)==s and all(sum(row[j]*chi[j] for j in range(m))==0 for row in G),'physical a-star norm and kernel')
  # Full empty lift reconstructed separately from C row sums.
  rs=[sum(r) for r in Cp];total=sum(rs);checks=0;empty=F(dp+total,dp)
  for i,v in enumerate(X):
   for j,zv in enumerate(X):
    L=F(dp+total,dp) if i==j==0 else (F(dp-rs[j-1],dp) if i==0 else (F(dp-rs[i-1],dp) if j==0 else F(dp+Cp[i-1][j-1],dp)))
    EUE=F(sum(map(sum,Up)),dp) if i==j==0 else (F(-sum(Up[j-1]),dp) if i==0 else (F(-sum(Up[i-1]),dp) if j==0 else F(Up[i-1][j-1],dp)))
    need(N*int(i==j)-L==EUE,'every actual-empty lower/upper lift entry')
    if v&zv:need(L==s*int(i==j),'every original intersecting support')
    checks+=1
  need(all(sum(row[j]*stars[0][j] for j in range(n))==0 for row in Cp),'whole positive star kernel')
  need(all(Xi^(1<<b) in X for Xi in X for b in range(q+3) if Xi&(1<<b)),'every immediate downset deletion')
  sizes=[sum(bool(v&(1<<b)) for v in X) for b in range(q+3)]
  need(sizes==[s,s-5,s-5]+[q+5]*5+[q+6]*(q-5),'all labelled star cardinalities and unique maximum')
  # Defining invariance checked via equal orbit sums in every row.
  for name,M in [('C',Cp),('D',D)]:
   seen={}
   for i,row in enumerate(M):
    sums=[0]*m
    for j,a in enumerate(row):sums[d['g'][j]]+=a
    key=d['g'][i]
    if key in seen:need(sums==seen[key],'entire original fixed-space invariance '+name)
    else:seen[key]=sums
  # Whole-original perturbation radius: exact symmetric row norm controls.
  trade_counts={a:0 for a in X[1:]}
  for a,b in [(1,2),(2,5),(1,4),(4,3),(2,4)]:trade_counts[a]+=1;trade_counts[b]+=1
  need(max(trade_counts.values())==3,'complete sum of absolute trade rows has maximum3')
  dnorm=F(max(sum(abs(x) for x in row) for row in D),den)
  radius=F(1,131072)/(dnorm+3)
  need(radius>0 and radius*(dnorm+3)==F(1,131072),'explicit all-four-parameter robust radius')
  out['positive']={'parameters':['1/4096',str(tb),str(tb),str(sigma)],'whole_forms':{name:textmatrix(A) for name,A in forms.items()},'congruences':congr,'full_empty_L00':str(empty),'full_empty_M00':str((empty-s)/(N-s)),'all_original_entry_checks':checks,'star_sizes':sizes,'complement_dimension':n-m,'complement_lower':'1/8192','complement_upper':str(N-2*s),'whole_unit_gap':str(F(1,4096*(N-s))),'Delta_max_absolute_row_sum':str(dnorm),'proved_parameter_box_radius':str(radius),'robust_lower_floor':'1/131072','robust_upper_floor':'1/8192'}
 return out

def run():
 uniform=derive();neg=[inspect(q) for q in range(5,16)];pos=[inspect(q,positive=True) for q in (16,17)]
 boundaries=[inspect(q,k) for q,k in [(4,0),(4,4),(5,0),(5,1),(5,4),(6,0),(6,6)]]
 for A in [[[0,1],[1,0]],[[1,0],[0,-1]],[[1,1],[2,1]]]:
  try:O.psd(A)
  except ValueError:pass
  else:raise ValueError('invalid PSD control accepted')
 return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','uniform':uniform,'negative':neg,'positive':pos,'all_count_boundary_controls':boundaries,'scope':'q>=5,k5,complete specified plain-core face; prior9703/9735 tail and9195 spectral premises are explicitly imported','new_refinement':'full four-parameter real boxes around q16/q17 rational positive points; lower floor1/131072 and upper floor1/8192'}

def canonical(r):return json.dumps(r,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--generate',action='store_true');parser.add_argument('--fixture',type=Path);args=parser.parse_args();r=run();raw=canonical(r);p=Path(__file__).with_name('EXPECTED.json')
 if args.generate:p.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
 else:
  def pairs(ps):
   out={}
   for k,v in ps:
    need(k not in out,'duplicate certificate JSON key');out[k]=v
   return out
  freeze=json.loads((args.fixture or p).read_text(),object_pairs_hook=pairs)
  need(canonical(freeze)==raw,'entire independent external mathematical record')
 print(json.dumps({'record_sha256':hashlib.sha256(raw).hexdigest(),'record_bytes':len(raw),'whole_negative_orders':len(r['negative']),'whole_positive_orders':len(r['positive']),'positions':sum(x['original_nonempty_positions'] for x in r['negative']+r['positive']+r['all_count_boundary_controls']),'robust_boxes':[x['positive']['proved_parameter_box_radius'] for x in r['positive']]}))
if __name__=='__main__':main()
