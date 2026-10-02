"""Separate integer evaluation/Fraction Gaussian certificate checker.

Imports NO generator polynomial arithmetic. Complete explicit degree bounds
prove polynomial identities; finite unbounded extrapolation is not used.
The shared author physical recipe is numerical Fraction specialization,
not an independent peer derivation. Ordinary bridges are in PROOF.md.
"""
from fractions import Fraction as F
from math import prod
from model import construct,blocks

def require(ok,msg):
 if not ok:raise ValueError(msg)

def decode(data,positive=False):
 den=data['denominator'];require(type(den) is int and den>0,'positive coefficient denominator')
 terms={};require(len(data['terms'])<=512,'unchanged512 term guard')
 for ex,value in data['terms']:
  require(type(ex) is list and len(ex)==2 and ex[0]==0 and type(ex[1]) is int and ex[1]>=0,'univariate embedded exponent')
  co=int(value);require(str(co)==value and co and ex[1] not in terms,'canonical unique nonzero integer coefficient')
  terms[ex[1]]=co
 if positive:require(terms.get(0,0)>0 and all(c>=0 for c in terms.values()),'strict shifted coefficient positivity')
 return terms,den

def degree(p):return max(p[0],default=0)
def value(p,q):return F(sum(c*q**e for e,c in p[0].items()),p[1])
def determinant(a):
 a=[[F(z) for z in row] for row in a];answer=F(1)
 for j in range(len(a)):
  pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
  if pivot is None:return F(0)
  if pivot!=j:a[j],a[pivot]=a[pivot],a[j];answer=-answer
  d=a[j][j];answer*=d
  for i in range(j+1,len(a)):
   c=a[i][j]/d
   for k in range(j+1,len(a)):a[i][k]-=c*a[j][k]
 return answer

def shift_identity(original,shifted):
 bound=degree(original);require(degree(shifted)<=bound,'exact shift degree bound')
 for v in range(bound+1):require(value(original,4+v)==value(shifted,v),'FULL q4 substitution identity')
 return bound+1

def factor(data):
 old,new=decode(data['original']),decode(data['shifted'],True)
 count=shift_identity(old,new);power=data['power'];require(type(power) is int and power>0,'positive factor exponent')
 return old,power,count

def factors_value(fs,q):return prod(value(p,q)**e for p,e in fs)
def factors_degree(fs):return sum(degree(p)*e for p,e in fs)

def check(data):
 scalar_names=['alphaH','betaH','alphaL','betaL','nu','muL']
 expected=[(name,1) for name in scalar_names]+[(name,k) for name,size in [('heavy-anti-1',2),('light-anti',2),('heavy-standard',4),('fixed',10)] for k in range(1,size+1)]
 require([(r['group'],r['order']) for r in data['rows']]==expected,'ALL24 scalar/Sylvester obligations')
 require(data['domain']=='realq>=4,q4+v,v>=0','ENTIRE stated uniform domain')
 require(data['identities']=={'cross_sector_positions':272,'heavy_anti_equal_positions':8,'physical_change_rank':20,'original_field_positions':99},'complete physical multiplicities and cross identities')
 require(set(data['forms'])==set(name for name,k in expected),'whole original-field catalogue')
 cache={};live_positions=0
 def live(q):
  if q not in cache:
   p,G,S,C,v=construct(q,'mean',F(0),F(-2,5));a,ids=blocks(G,S,C,v)
   require(ids=={k:v for k,v in data['identities'].items() if k!='original_field_positions'},'EVERY actual rational cross-sector/multiplicity identity')
   cache[q]={name:[[p[name]]] for name in scalar_names}|a
  return cache[q]
 parsed_rows=[]
 for row in data['rows']:
  name,k=row['group'],row['order'];form=data['forms'][name]
  require(row['cleared_original_matrix']==[values[:k] for values in form['cleared'][:k]],'ENTIRE leading-prefix matrix')
  for key,source in [('positive_row_domains','domains'),('positive_removed_row_factors','removed'),('positive_row_constants','constants')]:require(row[key]==form[source][:k],'ENTIRE original positive prefix data')
  original,shifted=decode(row['original']),decode(row['shifted'],True)
  points=shift_identity(original,shifted);parsed_rows.append((row,original,shifted,points))
 form_records=[];clearing_shift_points=0;entry_identity_points=0
 for name,form in data['forms'].items():
  raw=form['raw_original'];size=len(raw);a=[[decode(z) for z in row] for row in form['cleared']]
  require(len(a)==size and all(len(row)==size for row in a) and all(len(row)==size for row in raw),'entire original raw/cleared matrix dimensions')
  require(len(form['domains'])==len(form['removed'])==len(form['constants'])==size,'entire row normalization')
  for i in range(size):
   domains=[];removed=[]
   for group,output in [(form['domains'][i],domains),(form['removed'][i],removed)]:
    for f in group:
     p,e,count=factor(f);output.append((p,e));clearing_shift_points+=count
   const=F(form['constants'][i]);require(const>0,'strict positive row constant')
   for j in range(size):
    z=raw[i][j];numerator=decode(z['numerator']);den=[]
    for item in z['denominator_factors']:
     p=decode(item['factor']);e=item['power'];require(type(e) is int and e>0,'raw rational denominator exponent')
     # All raw poles are the explicitly positive q,q-1,q+2,q+3,q+6 linear factors.
     require(p[1]==1 and p[0] in [{1:1},{0:-1,1:1},{0:2,1:1},{0:3,1:1},{0:6,1:1}],'only stated original rational poles')
     den.append((p,e))
    lhs_degree=degree(a[i][j])+factors_degree(removed)+factors_degree(den)
    rhs_degree=degree(numerator)+factors_degree(domains);bound=max(lhs_degree,rhs_degree)
    for q in range(4,5+bound):
     left=value(a[i][j],q)*factors_value(removed,q)*factors_value(den,q)
     right=value(numerator,q)*factors_value(domains,q)*const
     require(left==right,'FULL original row-clearing polynomial identity')
     require(value(numerator,q)/factors_value(den,q)==live(q)[name][i][j],'whole independent Fraction original-form binding')
     entry_identity_points+=1;live_positions+=1
  form_records.append({'group':name,'size':size,'whole_entry_positions':size*size})
 checks=[];total_shift=0;total_det=0
 for row,original,shifted,points in parsed_rows:
  name,k=row['group'],row['order'];form=data['forms'][name]
  a=[[decode(z) for z in values[:k]] for values in form['cleared'][:k]]
  require(row['cleared_original_matrix']==[values[:k] for values in form['cleared'][:k]],'ENTIRE leading-prefix matrix')
  for key,source in [('positive_row_domains','domains'),('positive_removed_row_factors','removed'),('positive_row_constants','constants')]:require(row[key]==form[source][:k],'ENTIRE original positive prefix data')
  total_shift+=points
  bound=max(degree(original),sum(max((degree(z) for z in values),default=0) for values in a))
  for q in range(4,5+bound):
   require(value(original,q)==determinant([[value(z,q) for z in values] for values in a]),'FULL degree-bounded Fraction Gaussian leading determinant identity')
   total_det+=1
  require(row['degree']==degree(original) and row['coefficients']==len(shifted[0]) and row['positive'] is True,'entire reported sign data')
  checks.append({'group':name,'order':k,'positive_coefficients':len(shifted[0]),'full_determinant_identity_bound':bound,'full_determinant_identity_points':bound+1,'full_shift_points':points})
 return {'checks':checks,'positive_coefficients':sum(x['positive_coefficients'] for x in checks),'full_determinant_identity_points':total_det,'full_shift_points':total_shift,'positive_clearing_factor_shift_points':clearing_shift_points,'full_original_entry_identity_points':entry_identity_points,'live_original_fraction_bindings':live_positions,'whole_original_form_positions':sum(x['whole_entry_positions'] for x in form_records),'cached_original_q_values':len(cache),'complete':True}
