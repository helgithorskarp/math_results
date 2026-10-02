"""Independent semantic countercontrols, not target-native tests."""
import json,signal
from fractions import Fraction as F
from linear import need,digest,canonical,psd,inverse,form,mv
from quadrant import R,positive,reconstruct,pmul,padd,peval
from formulas import model
from original import seed,lift

def run():
 damages=[]
 def reject(name,fun):
  try:fun()
  except (ValueError,TypeError):damages.append(name);return
  raise ValueError('semantic damage accepted '+name)
 a=seed(3,2);C=a['C'];Q=lift(C);N=a['N'];s=a['f']['s'];h=N-s
 # Different two-by-two exact determinant rule vs Gaussian/Newton.
 p={(0,0):F(3),(1,0):F(2),(0,1):F(1)};q={(0,0):F(1),(1,1):F(-2)};r={(0,0):F(5),(0,2):F(3)};z={(0,0):F(7),(2,0):F(1)}
 A=[[p,q],[r,z]];actual=padd(pmul(p,z),{k:-v for k,v in pmul(q,r).items()});recovered,bounds,grid=reconstruct(A);need(actual==recovered,'ENTIRE Gaussian/Newton coefficient stream vs2x2 Leibniz')
 reject('negative constant cannot be positive denominator',lambda:R(1)/R({(0,0):-1,(1,0):1}))
 reject('negative quadrant coefficient cannot certify a uniform sign',lambda:need(positive({(0,0):F(1),(1,0):F(-1)}),'coefficient sign'))
 changed=dict(recovered);changed[1,0]=changed.get((1,0),F(0))+1
 reject('one changed determinant coefficient',lambda:need(all(peval(changed,i,j)==grid[i][j]for i in range(bounds[0]+1)for j in range(bounds[1]+1)),'complete identity grid'))
 reject('singular PSD with surviving cross coupling',lambda:psd([[F(0),F(1)],[F(1),F(1)]]))
 reject('original n7 exceeds fixed guard',lambda:seed(7,2))
 reject('l1 does not satisfy current family',lambda:seed(3,1))
 reject('Boolean n is not a domain integer',lambda:seed(True,2))
 wrong=[list(row)for row in C];i=a['sets'].index(a['u']);j=a['sets'].index(1|a['u']);wrong[i][j]+=F(1,10);wrong[j][i]+=F(1,10);badQ=lift(wrong)
 reject('one allowed-order label changed to an intersecting pair',lambda:need((1+badQ[i+1][j+1])/h==0,'actual intersecting M entry'))
 reject('seed incorrectly claims greatest lower rank',lambda:need(psd([[1+Q[i][j]for j in range(N)]for i in range(N)])['rank']==N-1,'seed rank isN-2'))
 actualempty=a['empty'];omit=[x for x in a['columns']];x=a['K'];whole=sum(a['ip'](x,y)**2 for y in omit+[actualempty]);missing=sum(a['ip'](x,y)**2 for y in omit)
 reject('omit actual empty from fixed frame',lambda:need(whole==missing,'complete K pairing changes'))
 f=a['f'];wrongarrow=[list(row)for row in f['arrow']];wrongarrow[0][3]=-wrongarrow[0][3];wrongarrow[3][0]=wrongarrow[0][3]
 reject('wrong augmented inverse cross sign',lambda:need(wrongarrow==f['transformed'],'complete congruence'))
 W=a['W'];u=[F(i<3)for i in range(len(W)-1)];kappa=form(inverse([row[:-1]for row in W[:-1]]),u,u)
 reject('drop pendant standard inverse term',lambda:need(kappa==3/(2*f['Cmean']),'complete deleted quadratic'))
 need(a['f']['d']<0 and a['f']['g']<0,'boundary fixture detects unneeded numerator sign assumption')
 reject('unjustified d and g positivity at q4/l2',lambda:need(a['f']['d']>0 and a['f']['g']>0,'boundary signs'))
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','damages':damages,'complete_small_Leibniz_coefficient_sha256':digest(recovered),'complete_small_identity_grid_sha256':digest(grid),'boundary_d':f['d'],'boundary_g':f['g']}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s semantic controls')));signal.alarm(45);print(json.dumps(canonical(run()),sort_keys=True,separators=(',',':')))
