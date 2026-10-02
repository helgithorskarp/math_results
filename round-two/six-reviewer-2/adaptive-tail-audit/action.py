"""Independent universal original constant/kernel action identity.

Exact Q(u), q=4+u. Standalone whole frozen record, guards and-O checks.
New author programs/EXPECTED still unread. Requires no positive-PSD
claim at kappa1, merely affine coefficient arithmetic.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys
from endpoint import q,TYPES,table,choose
from polynomial import Rat
from affine import table as literal
from linear import need

def run():
 Q0=table();Delta={key:Rat(0)for key in Q0};o,p,a,b,c,d,e=TYPES;h=1/(3*q+5)
 def put(x,y,v):Delta[tuple(sorted((x,y)))]=v
 put(o,o,1/(q-1));put(p,p,(1-6*h*(q+1)/(q*(q-1)))/((q-2)*(q-3)/2))
 for z in [a,c]:put(p,z,2*h/(q*(q-1)))
 for z in [b,d]:put(p,z,2*h/((q-1)*(q-2)))
 put(p,e,-6*h*(q+1)/(q*(q-1)))
 for qq in [4,5,7,12,23]:
  A=literal(qq,0);B=literal(qq,1)
  need({key:v.value(qq-4)for key,v in Delta.items()}=={key:B[key]-v for key,v in A.items()},'all20 affine slopes against separate original table')
 r=[Rat(1)if aa==0 else h if aa<3 else -3*(q+1)*h for aa,bb in TYPES];rows=[];kernel_actions=[]
 for j,l in [(0,0),(1,0)]:
  kept=[t for t in TYPES if j<=t[0]<=3-j and l<=t[1]]
  H=[]
  for aa,bb in kept:
   row=[]
   for cc,dd in kept:row.append(Delta.get(tuple(sorted(((aa,bb),(cc,dd)))),Rat(0))*((-1)**(j+l))*choose(3-aa-j,cc-j)*choose(q-bb-l,dd-l))
   H.append(row)
  if j==l==0:
   rows=[sum(row)for row in H];need(rows==r,'universal actual constant perturbation action')
   kernels=[[aa for aa,bb in kept],[int(aa>=2)for aa,bb in kept]]
  else:kernels=[[1]*len(kept)]
  for v in kernels:need(all(sum(z*v[m]for m,z in enumerate(row))==0 for row in H),'all symbolic affine family kernel actions')
  kernel_actions.append({'sector':[j,l],'columns':kernels,'zero_actions':True})
 weights=[choose(3,aa)*choose(q,bb)for aa,bb in TYPES];alpha=q*(q+1)/2+3*(q+1)*h
 need(sum(w*v*v for w,v in zip(weights,r))==alpha,'complete norm of original r')
 need(all(1-v==(1-h)*(aa-int(aa>=2))for(aa,bb),v in zip(TYPES,r)),'r=P1 full kernel split')
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','variable':'q=4+u','all_seven_constant_actions':[v.record()for v in rows],'kernel_actions':kernel_actions,'alpha_norm_squared':alpha.record(),'affine_slope_calibration_entries':100,'scope':'ALL q>=4 original affine table identities, degree-exact rational arithmetic; kappa1 used only for coefficient comparison, no PSD claim there'}
v=run();raw=(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()
if '--emit'in sys.argv:sys.stdout.buffer.write(raw)
else:
 expected=json.loads((Path(__file__).resolve().parent/'EXPECTED-action.json').read_text());need(v==expected,'whole universal-action frozen record')
 print(json.dumps({'status':'PASS','whole_record_sha256':hashlib.sha256(raw).hexdigest(),'whole_expected_equal':True,'original_constant_rows':7,'slope_calibration_entries':100},sort_keys=True))
