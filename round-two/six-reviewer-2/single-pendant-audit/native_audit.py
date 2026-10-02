"""Late producer-visible correspondence; not a premise of the sealed proof.
Run in a separate process. Primary code never imports producer modules.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json, signal, sys
from linear import need, digest, canonical, inverse, form
ROOT=Path(__file__).resolve().parent

def own_sets(n,r):
 old=list(range(1,1<<n));us=[1<<(n+2*i)for i in range(r)];vs=[1<<(n+2*i+1)for i in range(r)];b=1<<(n+2*r)
 marked=[(1<<i)|a for i in range(r)for a in [us[i],vs[i],us[i]|vs[i]]]+[(1<<r)|b]
 private=[a for i in range(r)for a in [us[i],vs[i],us[i]|vs[i]]]+[b]
 return [0]+old+marked+private

def run(repo,primary):
 manifest=json.loads((ROOT/'AUTHOR-INPUTS.json').read_text())['packets'][0];packet=repo/manifest['source_directory']
 for name,row in manifest['files'].items():
  raw=(packet/name).read_bytes();need(len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'],'entire pinned producer input before import: '+name)
 sys.path.insert(0,str(packet))
 from builder import build,solve
 from exact import lift
 from sectors import parameters
 from model import arrow as author_arrow,forms as author_forms,base_pairing
 # These modules are deliberately imported ONLY after the primary seal.
 rows=[]
 for n,r in [(3,2),(4,3),(4,2),(5,3),(5,4)]:
  family,C,W,p,*_=build(n,r,1,mean_recipe='cap-harmonic');sets=own_sets(n,r)
  need(set(family)==set(sets)and len(set(family))==len(family),'ENTIRE actual bitmask family')
  N=len(family);index={A:i for i,A in enumerate(family)};full=[index[A]for A in sets];core=[index[A]-1 for A in sets[1:]]
  meta=json.loads((primary/f'original-{n}-{r}-1-seed.json').read_text());params=parameters(p['q'],r,1,'cap-harmonic');mapping={'pair':'R','C':'cross'}
  scalars=meta['scalar_parameters'];need(len(scalars)==16,'all16 encoded scalar fields accounted for')
  for name,value in scalars.items():
   if name=='nuL':need(F(value)==0 and params['nuL']is None,'ABSENT pendant standard: own0 and producerNone bookkeeping')
   else:need(F(value)==F(params[mapping.get(name,name)]),'every actual scalar field: '+name)
  for phase in ['seed','old']:
   data=json.loads((primary/f'original-{n}-{r}-1-{phase}.json').read_text());cc=[row[:]for row in C];delta=F(0)
   if phase=='old':
    A=[row[:-1]for row in W[:-1]];u=[F(i<3)for i in range(len(W)-1)];kappa=sum(x*y for x,y in zip(u,solve(A,u)))
    need(kappa==F(data['kappa']),'whole deleted Gaussian inverse');delta=1/(4*(8+kappa));need(delta==F(data['delta']),'exact target repair step')
    private=[2*p['q']-1+2*i for i in range(p['m'])]
    for i in range(3):cc[private[i]][private[-1]]+=delta;cc[private[-1]][private[i]]+=delta
   M=lift(cc,p['s']);Q=[[(N-p['s'])*M[i][j]+p['s']*F(i==j)-1 for j in range(N)]for i in range(N)]
   decoded={'C':[[str(cc[i][j])for j in core]for i in core],'M':[[str(M[i][j])for j in full]for i in full],'Q':[[str(Q[i][j])for j in full]for i in full]}
   need(decoded==data['matrix_for_late_comparison'],'ALL reindexed actual C/Q/M entries '+phase)
   rows.append({'n':n,'r':r,'l':1,'phase':phase,'N':N,'all_core_positions':(N-1)**2,'all_whole_positions_each_Q_M':N*N,'actual_numeric_scalar_fields':15,'encoded_scalar_fields':16,'absent_nuL_bridge':'own0 equals absence represented by producerNone; no positive eigenvalue asserted','whole_decoded':digest(decoded)})
 from forms import arrow as own_arrow,tests as own_tests
 controls=json.loads((primary/'controls.json').read_text());groups=[];small=[]
 def compare_base(q,r,expected):
  S,b,ee,info=base_pairing(q,r,1);tau=ee+form(inverse(S),b,b)
  need(tau==F(expected),'ENTIRE native base-pairing/Woodbury quadratic equals independent Gaussian tau')
  return tau
 for control in controls['inverse_controls']:
  r=F(control['r']);q=F(control['q']);aug,_=author_arrow(q,r,1);ours=own_tests(r,F(1),q);native=author_forms(q,r,1)
  need(aug==own_arrow(r,F(1),q)==ours['fixed_inverse'],'EVERY uniform augmented entry')
  for name in ['anti','triangle','final']:need(native[name]==ours[name],'EVERY uniform actual sufficient Schur entry '+name)
  tau=compare_base(q,r,control['tau']);groups.append({'r':r,'q':q,'tau':tau,'whole_forms':digest([aug,native['anti'],native['triangle'],native['final']])})
 for control in controls['small_actual_final_controls']:
  r=F(control['r']);q=F(control['q']);native=author_forms(q,r,1);tau=compare_base(q,r,control['tau']);v=[native['aZ'],native['dE']];Tb=native['tauhat']
  actual=[[native['final'][i][j]+(Tb-tau)*v[i]*v[j]for j in range(2)]for i in range(2)]
  need([[str(v)for v in row]for row in actual]==control['actual_final'],'ALL actual exceptional final entries')
  need([[str(v)for v in row]for row in native['final']]==control['coarse_final'],'ALL exceptional coarse entries, including failure at n3r2')
  small.append({'r':r,'q':q,'tau':tau,'actual_final':actual,'coarse_final':native['final']})
 return {'scope':'late native correspondence; no primary proof premise','producer_inputs':len(manifest['files']),'whole_original_comparisons':rows,'whole_uniform_form_comparisons':groups,'whole_exception_comparisons':small,'all_original_entries_matched':True,'all_form_entries_matched':True}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=ROOT.parents[2]);p.add_argument('--primary',type=Path,required=True);a=p.parse_args()
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed60s late correspondence guard')));signal.alarm(60)
 print(json.dumps(canonical(run(a.repo,a.primary)),sort_keys=True,separators=(',',':')))
