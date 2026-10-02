"""Meaningful falsified-domain/form/coverage controls, explicit exceptions under-O."""
from copy import deepcopy
from fractions import Fraction as F
from linear import need,psd,canonical,mv,form
from dual import data
from coefficient import polynomials,positive
from sparse import x,y,poly,add
from orbits import counts,forms,vectors,three_space
from boundary import positive as cap, FLOORS
from literal import domain as literal_domain

def rejected(label,f):
 try:f()
 except(ValueError,ZeroDivisionError):return label
 raise ValueError('damaged input accepted: '+label)

def audit():
 bad=[]
 for label,f in[
 ('boolean ground order',lambda:data(True,1)),('noninteger deletion',lambda:data(8,F(2))),('outside deletion exceeds ground',lambda:data(4,5)),('q3 affine denominator',lambda:data(3,2)),('zero deletion',lambda:data(4,0)),('unpublished literal scope',lambda:literal_domain(75,15)),('zero diagonal nonzero PSD row',lambda:psd([[0,1],[1,0]])),('negative PSD diagonal',lambda:psd([[-1]]))]:bad.append(rejected(label,f))
 g=forms(74,15);vec=vectors(g['keys']);a=data(74,15)
 for label,index in[('wrong physical norm with preserved dimension',0),('missing whole orbit',1),('wrong diagonal support',2),('reversed repair edge',3),('nonzero slope on repair-zero frame',4)]:
  def test(index=index):
   if index==0:
    sizes=list(g['sizes']);sizes[0]+=1;sizes[1]-=1;need(sizes==counts(74,15)[1],'exact EVERY physical norm')
   if index==1:need(sum(g['sizes'][1:])==g['N']-1,'whole omitted orbit invalid')
   if index==2:
    U=deepcopy(g['U0']);U[0][0]+=1;need([[form(U,v,w)for w in vec]for v in vec]==a['U0'],'actual three-space Gram')
   if index==3:
    R=deepcopy(g['R']);i=g['keys'].index((1,0,0));j=g['keys'].index((2,0,0));R[i][j]=R[j][i]=-1;need(not any(mv(R,[1]*len(R))),'changed repair action')
   if index==4:
    D=deepcopy(g['Delta']);D[0][0]+=1;need([[form(D,v,w)for w in vec]for v in vec]==a['Delta'],'whole derivative Gram')
  bad.append(rejected(label,test))
 bad.append(rejected('changed universal coefficient constant',lambda:positive(add(polynomials()['V2'],poly(-100000)),add(poly(6),x),poly(2),'damaged')))
 bad.append(rejected('negative original Q0 promoted to positive cap',lambda:cap(18,5,F(1,256))))
 bad.append(rejected('unjustified high cap floor',lambda:cap(35,8,F(10**6))))
 for label,key in[('q74 negativeQ sign erased','Q'),('q74 positive derivative sign erased','d')]:
  bad.append(rejected(label,lambda key=key:need(-a[key]==a[key],'exact original signed dual')))
 # Strict lower-energy threshold equality cannot be used in a PD bridge.
 bad.append(rejected('lower energy equality counted as strict',lambda:need(1-F(2*(2*8+1),8)*F(8,2*(2*8+1))>0,'strict residual')))
 # Wrong original v accidentally includes ab/ac and destroys R-zero.
 def wrongv():
  w=[F(bool(c&6))for c,z,ww in g['keys']];need(form(g['R'],w,[1]*len(w))==0,'incorrect v repair cross term')
 bad.append(rejected('v includes excluded plain ab/ac',wrongv))
 need(len(bad)==20,'complete20 semantic damages')
 # These positive boundary cases demonstrate failure of old variance sufficiency.
 from variance import scalar
 failures=[]
 for k,q in[(8,35),(10,46),(18,91)]:need(scalar(q,k)['m']<0 and cap(q,k,FLOORS[k])['zero_shift_certificate']['rank']==23,'failed variance is NOT exclusion');failures.append([q,k])
 broad=[three_space(q,k)for q,k in[(4,1),(4,4),(5,5),(6,6),(19,19)]]
 need(all(r['V']>0 and r['D']>0 and r['d']>0 for r in broad),'newdomain positive controls')
 return {'damage_rejections':bad,'damage_count':len(bad),'actual_positive_boundaries_with_failed_variance':failures,'newdomain_positive_controls':[{'q':r['q'],'k':r['k'],'orbits':r['orbits'],'V':r['V'],'D':r['D'],'d':r['d']}for r in broad]}

if __name__=='__main__':
 import json,signal
 def alarm(*args):raise TimeoutError('fixed60s controls; incomplete is not exclusion')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60);print(json.dumps(canonical(audit()),sort_keys=True,separators=(',',':')))
