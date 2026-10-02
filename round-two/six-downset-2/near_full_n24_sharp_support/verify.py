"""Exact n24 sharp-support source checker; six-downset-2, researcher.

Star-only direct/RREF credited9365; complete blocks, empty lift, two PSD
algorithms and baseline controls credited9521/9017. No solver input.
"""
import argparse,copy,hashlib,json
from fractions import Fraction as Q
from math import comb
from pathlib import Path
from affine import direct,rref,supported_pairs
from baseline import arithmetic_audit,check_original,digest,harmonic_literal_control,literal_baseline,rejected
from exact import both
from model import affine,blocks,original,parameters,require
ROOT=Path(__file__).resolve().parent

def seed_fixture(doc):
 require((doc['n'],doc['r'],doc['N'],doc['s'])==(24,22,16777191,8388584),'Fixed original n24 domain')
 require(doc['proper_support_cutoff']==6 and doc['star_only'] is True,'Full noncentered S6 domain')
 require(doc['common_denominator']==10**9 and doc['upper_floor']=='1/64','Exact defining metadata')
 pairs=[p for p in supported_pairs(24) if p[0]>=2]
 require(doc['free_pairs']==[list(p) for p in pairs] and len(pairs)==121,'Full star free-pair census')
 require(len(doc['free_values'])==121 and all(type(v) is str for v in doc['free_values']),'All rational strings')
 values=[Q(v) for v in doc['free_values']]
 require(all(10**9%v.denominator==0 for v in values),'Common-denominator rational values')
 beta=direct(24,values);free,recover=rref(24)
 require(free==pairs and recover(values)==beta,'Independent star decoders')
 excluded=[(a,b) for a,b in pairs if a>=7 and a+b<24]
 require(len(excluded)==30 and all(beta[a][b]==0 for a,b in excluded),'All proper pairs above6 vanish')
 return pairs,beta

def seed_checks(doc):
 pairs,beta=seed_fixture(doc);n=24;r,N,s=parameters(n);h=N-s
 rows=[Q(s-(N-1))+sum(beta[a][b]*comb(n-a,b) for b in range(1,min(r,n-a)+1))
       for a in range(1,r+1)]
 require(any(rows),'Noncentering is explicit, not imposed')
 empty00=Q(1)+sum(comb(n,a)*rows[a-1] for a in range(1,r+1))
 emptyrow=[Q(1)-v for v in rows]
 require(empty00+sum(comb(n,a)*emptyrow[a-1] for a in range(1,r+1))==N,'Actual aggregated empty row')
 require(all((N-1)+rows[a-1]+emptyrow[a-1]==N for a in range(1,r+1)),'Actual aggregated nonempty rows')
 records=[];dimension=0;core_rank=0;upper_rank=0
 for j,aa,g,K,U in blocks(n,beta):
  d=len(aa);lower=[[g[i]*v for v in row] for i,row in enumerate(K)]
  expected=d-int(j<=1)
  if j<=1:
   v=aa if j==0 else [1]*d
   require(all(sum(K[i][k]*v[k] for k in range(d))==0 for i in range(d)),'Exact required star kernel')
  both(lower,expected)
  upper=[[g[i]*(v-Q(1,64)*int(i==k)) for k,v in enumerate(row)] for i,row in enumerate(U)]
  both(upper,d)
  mult=comb(n,j)-(comb(n,j-1) if j else 0)
  dimension+=mult*d;core_rank+=mult*expected;upper_rank+=mult*d
  records.append({'j':j,'layers':aa,'order':d,'multiplicity':mult,
                  'lower_rank':expected,'upper_gap_rank':d,
                  'lower_sha256':digest(lower),'upper_gap_sha256':digest(upper)})
 require(len(records)==13 and records[0]['order']==22 and dimension==N-1,'Every complete sector, full upper0')
 require(core_rank==N-n-1 and upper_rank==N-1,'Whole greatest ranks')
 classes=[];mass=Q(0)
 for a,b in pairs:
  if a<6 or a+b>=n or beta[a][b]<=0:continue
  count=comb(n,a)*comb(n-a,b)//(2 if a==b else 1)
  value=Q(count,h)*beta[a][b];mass+=value
  classes.append([a,b,str(beta[a][b]),count,str(value)])
 B=sum(a*a*comb(n,a) for a in range(3,6));R=s-12*n*n
 require(6*B<=R and classes and all(a==6 for a,b,v,c,m in classes),'Imported9471 cutoff5 and realized layer6')
 require(mass>Q(1,2*n*n),'Original positive proper bulk mass control')
 return {'n':n,'N':N,'s':s,'h':h,'free_coordinates':121,'active_S6_coordinates':91,
         'excluded_proper_pairs':30,'star_equation_rank':22,'star_decoders':2,
         'least_support_cutoff':6,'core_lower_rank':core_rank,'whole_lower_rank':core_rank+1,
         'whole_upper_rank':upper_rank,'whole_cap_floor':'1/64',
         'noncentered_core_row_sums':[str(v) for v in rows],
         'actual_empty_L00':str(empty00),'actual_empty_L0a':[str(v) for v in emptyrow],
         'sectors':records,'positive_bulk_mass_k5':str(mass),'positive_bulk_classes':classes,
         'credited9471_tail_control':{'B':B,'R':R,'holds':True}}

def controls(seed):
 cases=[]
 excluded=next(i for i,(a,b) in enumerate(seed['free_pairs']) if a>=7 and a+b<24)
 for name,change in [
  ('missing coordinate',lambda z:z['free_values'].pop()),
  ('floating coordinate',lambda z:z['free_values'].__setitem__(0,0.5)),
  ('wrong denominator',lambda z:z.__setitem__('common_denominator',1000)),
  ('wrong cutoff',lambda z:z.__setitem__('proper_support_cutoff',7)),
  ('centering assumption',lambda z:z.__setitem__('star_only',False)),
  ('wrong free pair',lambda z:z['free_pairs'].__setitem__(0,[1,1])),
  ('wrong cap floor',lambda z:z.__setitem__('upper_floor','0')),
  ('changed proper bulk support',lambda z:z['free_values'].__setitem__(excluded,'1/1000000000'))]:
  wrong=copy.deepcopy(seed);change(wrong)
  require(rejected(lambda:seed_fixture(wrong)),'Reject '+name);cases.append(name)
 wrong=copy.deepcopy(seed);wrong['free_values'][0]='1000000000'
 require(rejected(lambda:seed_checks(wrong)),'Damaged lower positivity');cases.append('damaged lower positivity')
 meta,recover=affine(6);beta=recover([Q(24)])
 F,C,L=original(6,beta,Q(1,528));L[0][0]+=1
 require(rejected(lambda:check_original(6,C,L,F)),'Actual empty loop damage');cases.append('actual empty loop')
 require(rejected(lambda:original(24,seed_fixture(seed)[1])),'Forbid n24 literal allocation');cases.append('n24 literal allocation')
 require(rejected(lambda:both([[Q(1),Q(2)],[Q(2),Q(1)]])),'Reject indefinite matrix');cases.append('indefinite input')
 return cases

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check',type=Path);parser.add_argument('--output',type=Path)
 args=parser.parse_args();seed=json.loads((ROOT/'seed.json').read_text())
 result={'agent':'six-downset-2','role':'researcher',
  'status':'Exact rational certificate; ordinary bridges unformalized; independent review pending',
  'seed':seed_checks(seed),'literal_published_n6_baseline':literal_baseline(),
  'whole_literal_harmonic_control':harmonic_literal_control(),'arithmetic_audit':arithmetic_audit(),
  'rejected_controls':controls(seed),'seed_sha256':hashlib.sha256((ROOT/'seed.json').read_bytes()).hexdigest(),
  'arithmetic':'integers and fractions.Fraction','no_original_n24_allocation':True}
 body=json.dumps(result,indent=2,sort_keys=True)+'\n'
 if args.check:require(body==args.check.read_text(),'Whole frozen record mismatch')
 if args.output:args.output.write_text(body)
 print(json.dumps({'ok':True,'record_sha256':hashlib.sha256(body.encode()).hexdigest(),
                   'complete_sectors':26,'least_support_cutoff':6,
                   'literal_action_columns':112,'controls':len(result['rejected_controls'])}))

if __name__=='__main__':main()
