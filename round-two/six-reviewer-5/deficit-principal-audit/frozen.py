"""Read-only rational certificate validation without float scouting or root searching."""
import json,copy,pathlib,sys
from fractions import Fraction as Q
from math import comb
P=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(P/'core'))
from original import parameters,phi,need
from optimizer import slope,gamma,gprime,up,down,BITS,UNIT,ROUND

def validate(row):
 n=row['n'];k=row['k'];need(type(n) is int and type(k) is int and n>=6 and 2<=k<=(n-2)//2,'integer original domain')
 s,h,N,r,Z,T,K,G,c=parameters(n,k);m=Q(row['normalized_mu']);mu=Q(row['mu']);need(m>0 and mu==2*s*m,'positive exact multiplier scale')
 need(row['root_bits']==BITS and row['old_budget']==str(T) and row['linear_budget']==str(Q(4*s*G,G+2)),'complete domain/budget')
 need([z['a'] for z in row['brackets']]==list(range(k+1,n//2+1)),'complete complementary bracket layers')
 upper=c+2*mu;proposals={};xi=Q(row['schedule_floor']);need(xi>0,'strict odd schedule floor')
 for obj in row['brackets']:
  a=obj['a'];idx=int(obj['lower_index']);need(type(obj['inactive']) is bool and 0<=idx<UNIT,'typed bounded root index')
  if obj['inactive']:
   need(idx==0 and slope(n,a,Q(0))<=m,'inactive derivative branch');lo=hi=Q(0)
  else:
   lo=Q(Z*idx,UNIT);hi=Q(Z*(idx+1),UNIT)
   need(slope(n,a,Q(0))>m and slope(n,a,lo)-mu*gprime(s,lo)>=0 and slope(n,a,hi)-mu*gprime(s,hi)<=0,'complete active derivative bracket')
  d=slope(n,a,hi)-mu*gprime(s,hi);need(d<=0,'upper supporting tangent')
  weight=comb(n,a)*(1 if 2*a==n else 2);upper+=up(weight*(phi(n,a,hi)-mu*gamma(s,hi)-d*(hi-lo)));proposals[a]=lo+xi
 gup=sum(up(comb(n,a)*(1 if 2*a==n else 2)*gamma(s,z)) for a,z in proposals.items());theta=min(Q(1),(Q(2)-Q(1,2**40))/gup)
 need(str(theta)==row['theta'],'full exact strict schedule normalization')
 zs={a:theta*z for a,z in proposals.items()};need(all(0<z<Z for z in zs.values()),'every principal even/odd weight')
 gamup=sum(up(comb(n,a)*(1 if 2*a==n else 2)*gamma(s,z)) for a,z in zs.items());lower=c+sum(down(comb(n,a)*(1 if 2*a==n else 2)*phi(n,a,z)) for a,z in zs.items())
 need(gamup<2 and row['gamma_upper']==str(gamup) and row['upper']==str(upper) and row['lower']==str(lower),'entire rational energy/gamma fields')
 need(type(row['principal_schedule_positive']) is bool and row['principal_schedule_positive']==(lower>0),'typed positive-energy verdict')
 return True

def controls(doc):
 rows=doc['optimizer']['full_principal_certificates'];need(all(validate(r) for r in rows),'all positive bindings')
 base=rows[1];changes=[]
 def damage(label,change):
  x=copy.deepcopy(base);change(x)
  try:validate(x)
  except (ValueError,KeyError,ZeroDivisionError):changes.append(label);return
  raise ValueError('accepted damaged '+label)
 damage('missing layer',lambda x:x['brackets'].pop())
 damage('wrong active branch',lambda x:x['brackets'][0].update(inactive=True))
 damage('wrong root interval',lambda x:x['brackets'][0].update(lower_index=str(UNIT//2)))
 damage('wrong multiplier scale',lambda x:x.update(mu=str(Q(x['mu'])+1)))
 damage('wrong root multiplier',lambda x:x.update(normalized_mu='1'))
 damage('wrong bulk budget',lambda x:x.update(linear_budget=x['old_budget']))
 damage('zero odd schedule',lambda x:x.update(schedule_floor='0'))
 damage('wrong normalization',lambda x:x.update(theta='2'))
 damage('missing curvature',lambda x:x.update(gamma_upper='0'))
 damage('flipped energy',lambda x:x.update(upper=str(-Q(x['upper']))))
 damage('wrong positive verdict',lambda x:x.update(principal_schedule_positive=False))
 damage('Boolean order',lambda x:x.update(n=True))
 return dict(valid_certificates=len(rows),rejected_semantic_damages=changes,float_inputs=False)
if __name__=='__main__':print(json.dumps(controls(json.loads((P/'PRIMARY.json').read_text())),sort_keys=True))
