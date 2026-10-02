"""LATE public target comparison, explicitly outside primary evidence.

Read the exact pinned14-file public packet supplied by --native-dir.
All hashes are checked before import. Never affects EXPECTED/primary files.
Each mode is one serial bounded45s phase (outer55s), no network.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,sys,json,hashlib,argparse,signal
from linear import need,digest,canonical
from formulas import model as own_model
from original import seed as own_seed,lift as own_lift
from quadrant import R,FACTORS,constant,times_factors,pmul,padd,precord

ROOT=Path(__file__).resolve().parent
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path/(name+'.py'));m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def inputs(path):
 record=json.loads((ROOT/'AUTHOR-INPUTS.json').read_text());entries=[]
 for item in record['files']:
  f=path/Path(item['path']).name;raw=f.read_bytes();need(len(raw)==item['bytes']and hashlib.sha256(raw).hexdigest()==item['sha256'],'ENTIRE pinned input before import');entries.append([f.name,len(raw),item['sha256']])
 need(len(entries)==14,'entire native input closure')
 exact=load(path,'exact');biv=load(path,'bivariate');mod=load(path,'model');native=load(path,'original')
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s late common phase')));signal.alarm(45)
 return exact,biv,mod,native,entries

def symbolic(path):
 exact,biv,mod,native,entries=inputs(path);u=R({(1,0):1});v=R({(0,1):1});own=own_model(4*(u+2)-4+v,u+2)
 U=biv.R(biv.P({(1,0):1}));V=biv.R(biv.P({(0,1):1}));l=2+U;q=4*l-4+V
 S3,final,params,info=mod.fixed(q,l,fraction=lambda a,b=1:biv.R(a)/b,compute_tau=False)
 def convert(x):
  z=biv.R(x);out=R({k:F(a,z.num.den)for k,a in z.num.a.items()})
  for atom,power in z.den.items():
   p=biv.ATOMS[atom];factor=R({k:F(a,p.den)for k,a in p.a.items()})
   for _ in range(power):out=out/factor
  return out
 def compare(a,b):
  b=convert(b);need(a==b,'ENTIRE symbolic rational numerator identity, not selected scalar sampling')
  # Record both complete rational expressions and a full coefficient-stream
  # cross product; it is identically the zero polynomial.
  left=pmul(a.p,times_factors(constant(1),b.e));right=pmul(b.p,times_factors(constant(1),a.e));res=padd(left,{k:-x for k,x in right.items()});need(not res,'ENTIRE cross multiplied coefficient stream')
  return {'own':a.record(),'native_as_own':b.record(),'cross_identity_sha256':digest(precord(res))}
 scalars={}
 for old,new in [('etaL','etaL'),('etaF','etaF'),('etaP','etaP'),('mu','mu'),('alpha','alpha'),('beta','beta'),('nu','nuL'),('d','d'),('g','g'),('A','A'),('Fp','Fp'),('c','c')]:scalars[old]=compare(own[old],params[new])
 change=[[1,-1,0],[3,l,0],[-3,-l,1]]
 arrow=[[sum(x[a]*S3[a][b]*y[b]for a in range(3)for b in range(3))for y in change]for x in change];rho=(q-1)/(q+1);cross=[F(1,3)+rho/l,1-rho,rho-1];aug=[row+[cross[i]]for i,row in enumerate(arrow)]+[cross+[info['tau_bound']+F(1,3)+rho*rho/l]]
 matrices={}
 for name,other in [('anti',params['anti']),('standard',params['standard']),('arrow',aug),('final',final)]:matrices[name]=[[compare(R(a),b)for a,b in zip(row,otherrow)]for row,otherrow in zip(own[name],other)]
 return {'phase':'symbolic','all_scalar_identities':scalars,'all_matrix_identities':matrices,'positive_factors':[precord(x)for x in FACTORS],'full_input_hashes':entries,'scope':'LATE comparison of EVERY rational parameter/28 small matrix entries by complete cross-multiplied coefficient streams, not independent primary proof'}

def original(path,n,l):
 exact,biv,mod,native,entries=inputs(path);a=own_seed(n,l);family,C,W,p,*rest=native.build(n,l);sets=[0]+a['sets'];need(set(sets)==set(family),'EVERY actual original set independent of author order');ix={A:i for i,A in enumerate(family[1:])};mapped=[[C[ix[A]][ix[B]]for B in a['sets']]for A in a['sets']];need(mapped==a['C'],'EVERY core position on actual masks');need(W==a['W'],'EVERY balanced residual position');ownQ=own_lift(a['C']);M=exact.lift(C,p['s']);fullix={A:i for i,A in enumerate(family)};N=a['N'];ownM=[[(1+ownQ[i][j]-p['s']*F(i==j))/(N-p['s'])for j in range(N)]for i in range(N)];need(all(ownM[i][j]==M[fullix[A]][fullix[B]]for i,A in enumerate(sets)for j,B in enumerate(sets)),'EVERY original M including actual empty')
 v=a['f'];parameters=[]
 for old,new in [('etaL','etaL'),('etaF','etaF'),('etaP','etaP'),('mu','mu'),('alpha','alpha'),('beta','beta'),('nu','nuL'),('d','d'),('g','g'),('A','A'),('Fp','Fp'),('c','c')]:need(v[old]==p[new],'all direct original scalars');parameters.append(v[old])
 return {'phase':'original','n':n,'l':l,'N':N,'entire_actual_masks_sha256':digest(sets),'entire_C_sha256':digest(mapped),'entire_W_sha256':digest(W),'entire_M_sha256':digest(ownM),'every_core_positions':(N-1)**2,'every_residual_positions':(l+3)**2,'every_original_M_positions':N*N,'entire_original_parameter_sha256':digest(parameters),'full_input_hashes':entries,'scope':'LATE whole entry comparison keyed by every ACTUAL set, not index convention or independent primary proof'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native-dir',type=Path,required=True);p.add_argument('phase',choices=['symbolic','original']);p.add_argument('--n',type=int);p.add_argument('--l',type=int);a=p.parse_args();r=symbolic(a.native_dir)if a.phase=='symbolic'else original(a.native_dir,a.n,a.l);print(json.dumps(canonical(r),sort_keys=True,separators=(',',':')))
