"""Late native correspondence, separate from the sealed primary proof.
Run each packet in its own process; primary code never imports producer code.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,sys,signal
from linear import need,digest,canonical
ROOT=Path(__file__).resolve().parent
def own_sets(n,r,l):
 old=list(range(1,(1<<n)));us=[1<<(n+2*i) for i in range(r)];vs=[1<<(n+2*i+1) for i in range(r)];bs=[1<<(n+2*r+j) for j in range(l)];marked=[(1<<i)|a for i in range(r) for a in [us[i],vs[i],us[i]|vs[i]]]+[(1<<(r+j))|bs[j] for j in range(l)];private=[a for i in range(r) for a in [us[i],vs[i],us[i]|vs[i]]]+bs
 return [0]+old+marked+private
def run(packet,primary,boundary):
 sys.path.insert(0,str(packet));from builder import build,solve;from exact import lift;from sectors import parameters
 # The producer modules are intentionally opened ONLY by this late adapter.
 rows=[];comparisons=[]
 for n,r,l in [(4,2,2),(5,2,3),(5,3,2)]:
  if boundary and r!=2:continue
  family,C,W,p,*_=build(n,r,l,mean_recipe='cap-harmonic');sets=own_sets(n,r,l);need(set(family)==set(sets) and len(set(family))==len(family),'ENTIRE actual family correspondence');N=len(family);index={A:i for i,A in enumerate(family)};full=[index[A] for A in sets];core=[index[A]-1 for A in sets[1:]];params=parameters(p['q'],r,l,'cap-harmonic')
  meta=json.loads((primary/f'original-{n}-{r}-{l}-seed.json').read_text());mapping={'pair':'R','C':'cross'}
  for name,value in meta['scalar_parameters'].items():need(F(value)==F(params[mapping.get(name,name)]),'ENTIRE scalar parameter '+name)
  for phase in ['seed','old']:
   data=json.loads((primary/f'original-{n}-{r}-{l}-{phase}.json').read_text());cc=[row[:] for row in C];delta=F(0)
   if phase=='old':
    A=[row[:-1] for row in W[:-1]];u=[F(i<3) for i in range(len(W)-1)];kappa=sum(x*y for x,y in zip(u,solve(A,u)));need(kappa==F(data['kappa']),'whole deleted Gaussian inverse');delta=1/(12*N*(1+kappa));need(delta==F(data['delta']),'exact conservative repair step');native_private=[2*p['q']-1+2*i for i in range(p['m'])]
    for i in range(3):cc[native_private[i]][native_private[-1]]+=delta;cc[native_private[-1]][native_private[i]]+=delta
   M=lift(cc,p['s']);Q=[[(N-p['s'])*M[i][j]+p['s']*F(i==j)-1 for j in range(N)] for i in range(N)];decoded={'C':[[str(cc[i][j]) for j in core] for i in core],'M':[[str(M[i][j]) for j in full] for i in full],'Q':[[str(Q[i][j]) for j in full] for i in full]};need(decoded==data['matrix_for_late_comparison'],'ALL reindexed actual C/Q/M entries '+phase);rows.append({'n':n,'r':r,'l':l,'phase':phase,'N':N,'all_core_positions':(N-1)**2,'all_whole_positions_each_Q_M':N*N,'all_scalar_fields':len(meta['scalar_parameters']),'whole_decoded':digest(decoded)})
 from forms import arrow as own_arrow,tests as own_tests,model as own_model
 if boundary:
  from model import fixed as author_fixed,parameters as author_parameters
  for l in [2,3,8,1000]:
   for slack in [0,1,16]:
    q=4*l+slack;aug,final,pars,_=author_fixed(q,l,upper_bounds=True);need(aug==own_arrow(F(2),F(l),F(q)),'EVERY boundary augmented entry');own=own_tests(F(2),F(l),F(q),True)
    for name in ['anti','pendant','triangle']:need(pars[name]==own[name],'EVERY boundary substituted Schur entry')
    need(final==own['final'],'EVERY boundary final Schur entry');comparisons.append([q,2,l,digest([aug,final,pars['anti'],pars['pendant'],pars['triangle']])])
 else:
  from model import arrow as author_arrow,forms as author_forms
  controls=json.loads((primary/'controls.json').read_text())['inverse_controls']
  for control in controls:
   r=int(F(control['r']));l=int(F(control['l']));q=F(control['q']);aug,_=author_arrow(q,r,l);need(aug==own_arrow(F(r),F(l),q),'EVERY target augmented entry')
   if r>=3:
    af=author_forms(q,r,l);own=own_tests(F(r),F(l),q);z=own_model(F(r),F(l),q)
    # The primary tests deliberately substitute larger nuL and C.  The
    # native model returns the actual forms.  Check the exact PSD subtraction
    # connecting them, rather than incorrectly asking the two forms to agree.
    upper_nuL=F(l)*z['etaP']/(l-1);upper_C=q/(2*z['m']);H=z['H']
    need(upper_nuL>z['nuL'] and upper_C>z['C'],'strict sufficient substitution direction')
    compared={name:[row[:] for row in af[name]] for name in ['anti','pendant','triangle','final']}
    compared['pendant'][1][1]-=(upper_nuL-z['nuL'])/(2*H)
    compared['final'][0][0]-=F(l)*(upper_C-z['C'])/(3*r*H)
    for name in ['anti','pendant','triangle','final']:need(compared[name]==own[name],'EVERY target sufficient Schur entry and exact PSD bridge: '+name)
   comparisons.append([str(q),r,l,digest(aug)])
 return {'scope':'late native correspondence; no primary proof premise','boundary':boundary,'whole_original_comparisons':rows,'whole_form_comparisons':comparisons,'all_original_entries_matched':True,'all_form_entries_matched':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=ROOT.parents[2]);p.add_argument('--primary',type=Path,required=True);p.add_argument('--boundary',action='store_true');a=p.parse_args();packet=a.repo/'round-two/six-downset-1'/('two-triangle-pendants-cap' if a.boundary else 'mixed-attachment-cap');signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed60s late correspondence guard')));signal.alarm(60);print(json.dumps(canonical(run(packet,a.primary,a.boundary)),sort_keys=True,separators=(',',':')))
