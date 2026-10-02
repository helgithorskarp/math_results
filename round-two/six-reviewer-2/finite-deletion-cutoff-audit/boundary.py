"""Independent ALL20 remaining boundary decisions and full weighted certificates."""
from fractions import Fraction as F
from linear import need,canonical,digest,mv,psd
from affine import parameters
from variance import boundary,scalar
from orbits import forms,three_space
FLOORS={8:F(1,256),10:F(1,4096),13:F(1,512),16:F(1,512),18:F(1,8192),19:F(1,512),21:F(1,2048),22:F(1,512),24:F(1,1024)}

def positive(q,k,delta):
 g=forms(q,k);size=g['sizes'];d=len(size);N=g['N'];s=g['s'];gap=N-2*s;star=g['star'];need(d==23,'entire fixed23 domain')
 shift=[[g['U0'][i][j]-delta*size[i]*(i==j)for j in range(d)]for i in range(d)];zero=psd(shift);need(zero['rank']==23 and gap>=delta>0,'full shifted zero-cap fixed floor')
 kap=delta/(4*(16*s+1));old=kap/24;new=F(k,4*(2*k+1))*kap;records=[]
 for label,t in[('original',old),('enlarged',new)]:
  C=[[g['C0'][i][j]+kap*g['Delta'][i][j]+t*g['R'][i][j]for j in range(d)]for i in range(d)]
  U=[[g['U0'][i][j]-kap*g['Delta'][i][j]-t*g['R'][i][j]for j in range(d)]for i in range(d)]
  lower=psd(C);upper=psd([[U[i][j]-F(3,4)*delta*size[i]*(i==j)for j in range(d)]for i in range(d)])
  need(lower['rank']==22 and upper['rank']==23 and not any(mv(C,star)),'all repaired lower/cap ranks and exact star')
  need(16*s*kap+2*t<delta/4 and 0<t< F(k,2*(2*k+1))*kap,'full perturbation and strict lower energy')
  empty_L=1+sum(sum(row)for row in C);h=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*h;expected=1+k*(s-k)+kap*(alpha-2*k*h)
  need(empty_L==expected,'actual empty loop ALL nonempty double sum')
  records.append({'repair':label,'t':t,'lower_rank':lower['rank'],'upper_floor_rank':upper['rank'],'whole_lower_rank':N-1,'whole_cap_rank':N-1,'lower_certificate':lower,'upper_certificate':upper,'whole_G_H_sha256':digest([C,U]),'actual_empty_M':(empty_L-s)/(N-s),'whole_projected_cap_floor':F(3,4)*delta,'whole_unit_gap':F(3,4)*delta/(N-s)})
 return {'q':q,'k':k,'N':N,'orbits':d,'delta':delta,'kappa':kap,'zero_shift_certificate':zero,'whole_zero_floor':min(gap,delta),'whole_complement_dimension':N-1-d,'whole_complement_zero_cap_floor':gap,'whole_complement_lower_floor':kap/2,'norm_weights':size,'original_table_Q0':parameters(q,k)['Q0'],'failed_or_positive_variance_margin':scalar(q,k)['m'],'repairs':records,'new_to_old':new/old}

def audit():
 records=[]
 for k in range(5,25):
  q=boundary(k)-5;need(q>=3*k,'ALL boundary domain covered by original dual quadrant');a=three_space(q,k);old=parameters(q,k)['Q0']
  if k in FLOORS:
   r=positive(q,k,FLOORS[k]);r.update({'decision':'positive','cutoff':q,'dual':a});need(old>=0,'positive case compatible with old necessary dual')
  else:
   if k==15:
    need(old>0 and a['Q']==F(-143801893468984,75947686734101)and a['d']==F(47856140532212612494,17240124888640927)>0,'sole new complementary negative')
    reason='new three-vector dual'
   else:need(old<0,'ALL old necessary negatives');reason='owned9434 universal Q0'
   r={'q':q,'k':k,'decision':'negative','cutoff':q+1,'old_Q0':old,'new_dual':a,'reason':reason}
  records.append(r)
 need([r['k']for r in records if r['decision']=='positive']==list(FLOORS),'complete nine-positive eleven-negative partition')
 calibrations=[]
 # Interior and boundary faces of NEW original-domain dual; all fields checked.
 for q,k in[(4,1),(4,2),(4,3),(4,4),(5,5),(6,5),(8,8),(19,19),(35,8),(74,15)]:calibrations.append(three_space(q,k))
 return {'all20_boundary_records':records,'new_domain_calibrations_only':calibrations,'scope':'ALL-q classification combines these20 complete exact remaining-order decisions with owned9586 positive and9508 negative unbounded tails. No complete feasible face or arbitraryH exclusion.'}

if __name__=='__main__':
 import json,signal
 def alarm(*args):raise TimeoutError('fixed60s boundary phase; incomplete is not exclusion')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60);print(json.dumps(canonical(audit()),sort_keys=True,separators=(',',':')))
