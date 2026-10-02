"""Semantic failures with explicit checks, including parity and actual metric."""
from fractions import Fraction as F
import json,signal
from linear import need,canonical,psd
from core import constants,architecture,free_pairs,complete,sector,embedding,supported,projected_upper_form
from literal import original

def audit():
 records=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,TypeError,IndexError)as e:records.append({'control':name,'rejected':True,'reason':str(e)});return
  raise ValueError('damage accepted: '+name)
 reject('dense original n8 allocation forbidden',lambda:original(8))
 reject('guard does not permit original n40',lambda:constants(40))
 reject('boolean is not an original order',lambda:constants(True))
 reject('cutoff0 forbidden',lambda:architecture(7,0))
 reject('cutoff above actual rank forbidden',lambda:architecture(7,6))
 n=7;_,_,s,h=constants(n);free={p:F(0)for p in free_pairs(n)};free[(3,4)]=F(5);beta=complete(n,free)
 reject('incomplete free-coordinate face',lambda:complete(n,{p:v for p,v in free.items()if p!=(2,2)}))
 reject('float is not exact input',lambda:complete(n,{p:(0.0 if p==(2,2)else v)for p,v in free.items()}))
 damaged=dict(beta);damaged[(2,2)]=1
 reject('proper S1 support actually forbidden',lambda:supported(n,1,damaged))
 low=sector(n,beta,2);high=sector(n,beta,3);ix=[low['layers'].index(a)for a in high['layers']]
 reject('odd high degree without the above-middle sign',lambda:need(high['K']==[[low['K'][i][j]for j in ix]for i in ix],'odd off-complement sign differs'))
 reject('above-middle physical norms replaced by1',lambda:need(low['metric']==[1]*len(low['layers']),'actual physical norm census differs'))
 n=10;_,_,s,h=constants(n);f={p:F(0)for p in free_pairs(n)};f[(5,5)]=F(7);b=complete(n,f);a2=sector(n,b,2);a3=sector(n,b,3);i2=a2['layers'].index(5);i3=a3['layers'].index(5)
 reject('even middle singleton low2 replaces low3',lambda:need(a2['K'][i2][i2]==a3['K'][i3][i3],'even middle needs both signs'))
 f[(2,8)]=F(s);b=complete(n,f);g=sector(n,b,2)
 reject('automatic floor n replaces n-1 at extremal complement',lambda:psd([[g['H'][i][j]-n*g['metric'][i]*(i==j)for j in range(len(g['layers']))]for i in range(len(g['layers']))]))
 n=6;_,N,s,h=constants(n);b=complete(n,{(2,2):F(4,3),(2,3):0,(2,4):22,(3,3):24});g=sector(n,b,0)
 reject('mean block replaced by coreI at same whole gap2',lambda:psd([[g['H'][i][j]-2*g['metric'][i]*(i==j)for j in range(4)]for i in range(4)]))
 reject('degree0 projected metric drops physical mean term',lambda:need(g['W']==[[g['metric'][i]*(i==j)for j in range(4)]for i in range(4)],'entire projected metric differs'))
 reject('asymmetric form',lambda:psd([[1,2],[0,1]]))
 reject('zero diagonal with nonzero residual',lambda:psd([[0,1],[1,0]]))
 valid=embedding(7,1,beta);records.append({'control':'positive odd signed principal transfer','rejected':False,'positions':valid['positions']});need(psd([[1,1],[1,1]])['rank']==1,'positive singular boundary must pass');records.append({'control':'positive PSD singular boundary retained','rejected':False})
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','semantic_controls':records,'damage_count':sum(x['rejected']for x in records),'positive_count':sum(not x['rejected']for x in records),'scope':'Explicit acceptance and rejection, not assertions; no failure is mathematical nonexistence.'}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s controls')));signal.alarm(45);print(json.dumps(canonical(audit()),sort_keys=True,separators=(',',':')))
