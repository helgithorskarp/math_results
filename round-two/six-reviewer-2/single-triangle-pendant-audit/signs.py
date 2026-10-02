"""All-quadrant independent Gaussian/Newton signs and rational identities.

Each mode has fixed45s internal/55s outer guards. No target code/oracle.
"""
import json,signal,argparse
from fractions import Fraction as F
from linear import need,canonical,digest,psd
from quadrant import R,FACTORS,positive,precord,certificate,pmul,pdiv,peval
from formulas import model

def run(which):
 u=R({(1,0):1});v=R({(0,1):1});l=2+u;q=4*l-4+v;a=model(q,l)
 need(all(a['transformed'][i][j]==a['arrow'][i][j]for i in range(4)for j in range(4)),'ALL16 symbolic augmented inverse congruence entries')
 norms={}
 for name in ['etaL','etaF','etaP','mu','alpha','beta','nu']:
  x=a[name];need(positive(x.p),'positive scalar '+name);norms[name]={'rational':x.record(),'coefficients_sha256':digest(precord(x.p)),'coefficient_count':len(x.p)}
 for name in ['q','l','s','w','ell','D','H','A0','J']:
  need(positive(R(a[name]).p),'positive base factor '+name)
 need(positive((q-l-1).p)and positive((a['N']-1-a['s']).p),'full Gram and base gaps')
 matrices={k:[[R(x)for x in row]for row in a[k]]for k in ['anti','standard','arrow','final']}
 record=certificate(matrices[which],which)
 # Distinct direct Fraction formula checks, including the corner q4/l2
 # where d,g are negative and the untouched antisymmetric subspace is0.
 controls=[]
 for q0,l0 in [(4,2),(8,2),(8,3),(16,4),(32,2),(32,5),(64,6),(128,7)]:
  f=model(F(q0),F(l0));u0=l0-2;v0=q0-4*l0+4
  need(all(matrices[which][i][j].value(u0,v0)==f[which][i][j]for i in range(len(matrices[which]))for j in range(len(matrices[which]))),'EVERY direct Fraction matrix entry')
  need(all(a[k].value(u0,v0)==f[k]>0 for k in norms),'EVERY residual norm direct Fraction')
  need(all(f['arrow'][i][j]==f['transformed'][i][j]for i in range(4)for j in range(4)),'EVERY direct congruence identity')
  need(psd(f[which])['rank']==len(f[which]),'literal positive definite test')
  controls.append({'q':q0,'l':l0,'whole_direct_matrix_sha256':digest(f[which])})
 factors=[precord(p)for p in FACTORS];need(all(positive(p)for p in FACTORS),'EVERY registered denominator, no numerical sign oracle')
 # Complete small polynomial engine controls in a different dense rule.
 p={(0,0):F(3),(1,0):F(-2),(0,1):F(4),(2,1):F(1)};z={(0,0):F(2),(1,0):F(1),(0,2):F(3)};prod=pmul(p,z)
 need(pdiv(prod,z)==p and pdiv(prod,p)==z,'both exact division multiplication-back controls')
 need(all(peval(prod,i,j)==peval(p,i,j)*peval(z,i,j)for i in range(4)for j in range(5)),'ALL20 direct convolution controls')
 need(pdiv({(0,0):F(1)},z)is None,'nondivisible polynomial')
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','method':'Fraction Gaussian on entire proven rectangular degree grid; tensor Newton power-coefficient reconstruction; positive-factor rational ring. No target code/certificate/oracle. Defining written formulas visible; own prior one-variable method credited.','quadrant':'l=2+u,q=4l-4+v,u>=0,v>=0','all_scalar_norms':norms,'every_registered_positive_denominator':factors,'symbolic_augmented_congruence_entries':16,'test':record,'direct_fraction_controls':controls}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('which',choices=['anti','standard','arrow','final']);args=p.parse_args();signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s uniform-sign phase')));signal.alarm(45);print(json.dumps(canonical(run(args.which)),sort_keys=True,separators=(',',':')))
