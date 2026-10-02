"""Ten exact parameter identities by characteristic-zero field normal form.
These CAS bridges are distinct from the standard-library determinant checker.
"""
from cas import K,r,l,q
from forms import model
from linear import need,canonical
import json,signal
def run():
 rr,ll,qq=K.convert(r),K.one,K.convert(q);z=model(rr,ll,qq,False);s=z['s'];w=z['w'];ell=z['ell'];t=z['t'];rho=z['rho'];d=z['d'];g=z['g'];c=z['c'];A=z['A'];ast=z['ast'];common=z['common'];E2=z['e2'];Di2=z['di2'];X=A*A*E2+ast*ast*Di2;Y=d*d*(E2+Di2);Z=A*d*E2+ast*d*Di2
 identities={
  'marked_full':-(qq-1)/ell+d*qq/3+1,
  'marked_leaf':-(qq-1)/ell+(z['a']*qq-c*s)/3+1,
  'marked_pendant':-(qq+1)/ell+g*w+1,
  'projection_sum':rr*(2*A+d)+ll*z['Fp'],
  'mean_norm':3*z['mu']-(qq-3*common-d*d*qq/9-d*g*rho*w/rr-2*s*c*c*(rr-1)/(3*t*t)),
  'pendant_norm':z['etaP']-(w-common-g*g*(w+qq/(3*rr*rho*rho))-2*s*c*c*rr/(3*t*t)),
  'internal_alpha':z['alpha']-(2*s-4*X+2*Z+2*Y-8*s*c*c/3+4*s*c*c*(rr-1)/(3*t*t)),
  'internal_beta':z['beta']-(2*s/3-8*d*d*qq/27+d*g*rho*w/(3*rr)-d*d*rho*rho*w/ll-4*s*c*c*(rr-1)/(9*t*t)),
  'leaf_norm_decomposition':z['etaL']-(z['mu']+(z['alpha']+z['beta'])/4),
  'full_norm_decomposition':z['etaF']-z['mu']-z['beta']}
 for name,value in identities.items():need(value==K.zero,'exact field identity '+name)
 return {'identities':sorted(identities),'all_remainders_zero':True,'domain':'QQ(r,q), characteristic0','trust':'SymPy1.14.0 field normal form; written identities and direct literal Fraction controls also audited'}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed60s identity phase')));signal.alarm(60);print(json.dumps(canonical(run()),sort_keys=True,separators=(',',':')))
