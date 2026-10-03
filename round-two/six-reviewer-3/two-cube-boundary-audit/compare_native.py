#!/usr/bin/env python3
"""LATE DATA-only full correspondence. Imports only sealed reviewer arithmetic."""
import argparse,json,math,hashlib
from pathlib import Path
from fractions import Fraction as F
from poly import Rat,require,trim,scale,sub,mul,power,tick
from audit import scalar_data,forms,POS,bareiss,shift
R=Rat
def dec(z):
 require(type(z) is dict and set(z)=={'denominator','terms'},'polynomial schema');d=z['denominator'];require(type(d) is int and d>0,'positive integer coefficient denominator');coeff={}
 for e,c in z['terms']:
  require(type(e) is list and len(e)==2 and all(type(v) is int for v in e) and e[0]>=0 and e[1]==0 and e[0] not in coeff,'unique univariate exponent')
  require(type(c) is str and str(int(c))==c and int(c)!=0,'canonical nonzero integer coefficient');coeff[e[0]]=int(c)
 require(len(coeff)<=512,'bounded complete polynomial');return R(tuple(coeff.get(i,0) for i in range(max(coeff,default=-1)+1)),d)
def eq(a,b,msg):require(not (a-b).n,msg)
def factors(group):
 p=R(1);count=0
 for z in group:
  old,new=dec(z['original']),dec(z['shifted']);require(old.d==(1,) and old.n in POS,'allowed positive original pole');eq(R(shift(old.n)),new,'pole shift whole identity');e=z['power'];require(type(e) is int and e>0,'strict factor exponent');p*=old**e;count+=1
 return p,count

def run(data):
 require(data['domain']=='q=2, real h>=2 for sign forms only; original family requires integer h>=2' and type(data['fixed_quotient']) is int and data['fixed_quotient']==9,'exact original domain')
 sizes={'alphaH':1,'betaH':1,'alphaL':1,'betaL':1,'nu':1,'muL':1,'antiH':2,'antiL':2,'standard':4,'fixed':9};expected=[(n,k) for n,s in sizes.items() for k in range(1,s+1)]
 require(list(data['forms'])==list(sizes) and [(r['group'],r['order']) for r in data['rows']]==expected,'all111 entries and23 obligations in order')
 s=scalar_data();live={n:[[s[k]]] for n,k in zip(list(sizes)[:6],('ah','bh','al','bl','nu','ml'))}
 for native,own in [('antiH','heavy-odd'),('antiL','light-odd'),('standard','contrast'),('fixed','fixed')]:
  m=forms(own)[1];perm=[0,1,3,2] if native=='standard' else list(range(len(m)));live[native]=[[m[perm[i]][perm[j]] for j in range(len(m))] for i in range(len(m))]
 records=[];matrices={};entries=0;clearing=0;factor_count=0
 for n,size in sizes.items():
  d=data['forms'][n];require(all(len(d[k])==size for k in ('raw_original','cleared','domains','removed','constants')),'whole form dimensions')
  A=[];denoms=[]
  for i in range(size):
   require(len(d['raw_original'][i])==len(d['cleared'][i])==size,'whole row')
   domain,ct=factors(d['domains'][i]);factor_count+=ct;removed,ct=factors(d['removed'][i]);factor_count+=ct
   const=F(d['constants'][i]);require(const>0,'positive row constant');k=R(const.numerator,const.denominator);polys=[dec(v) for v in d['cleared'][i]]
   for j in range(size):
    raw=d['raw_original'][i][j];den=R(1)
    for term in raw['denominator_factors']:
     z=dec(term['factor']);e=term['power'];require(z.d==(1,) and z.n in POS and type(e) is int and e>0,'raw original positive poles');den*=z**e
    rawrat=dec(raw['numerator'])/den;eq(rawrat,live[n][i][j],'entire own/native QQ(h) original correspondence');entries+=1
    eq(polys[j]*removed,rawrat*domain*k,'whole native clearing identity');clearing+=1
   require(all(len(p.d)==1 for p in polys),'cleared forms polynomial')
   dd=math.lcm(*(p.d[0] for p in polys));A.append([scale(p.n,dd//p.d[0]) for p in polys]);denoms.append(dd)
  matrices[n]=(A,denoms);records.append({'group':n,'entire_own_rational_form':[[[list(z.n),list(z.d)] for z in r] for r in live[n]]})
 signs=[]
 for row in data['rows']:
  n,k=row['group'],row['order'];old,new=dec(row['original']),dec(row['shifted']);require(len(old.d)==1 and len(new.d)==1,'whole sign polynomial')
  eq(R(shift(old.n),old.d),new,'complete native shifted coefficient identity')
  require(bool(new.n) and new.n[0]>0 and all(c>=0 for c in new.n),'all native h2 shifted signs')
  require(row['positive'] is True and type(row['degree']) is int and row['degree']==len(old.n)-1 and row['original_terms']==sum(bool(c) for c in old.n) and row['shifted_terms']==sum(bool(c) for c in new.n),'all sign metadata')
  a,ds=matrices[n];det=bareiss([r[:k] for r in a[:k]]);eq(R(det,math.prod(ds[:k])),old,'complete polynomial native determinant by own Bareiss')
  signs.append({'group':n,'order':k,'original':[list(old.n),list(old.d)],'shifted':[list(new.n),list(new.d)]});tick()
 require(entries==clearing==111 and len(signs)==23,'full correspondence counts')
 return {'status':'PASS','data_only':True,'basis_bridge':'standard swaps coordinates2 and3; all other physical bases identical','original_field_identities':entries,'clearing_identities':clearing,'positive_factor_occurrences':factor_count,'sign_obligations':len(signs),'original_forms':records,'complete_native_sign_polynomials':signs}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('--output',required=True);a=ap.parse_args();raw=Path(a.input).read_bytes();o=run(json.loads(raw));o['full_input_sha256']=hashlib.sha256(raw).hexdigest();Path(a.output).write_text(json.dumps(o,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'status':'PASS','identities':o['original_field_identities'],'signs':o['sign_obligations']}))
