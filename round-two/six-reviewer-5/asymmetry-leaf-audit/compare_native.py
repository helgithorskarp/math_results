"""Late comparison only. Stdlib exact whole maps; never repair primary from producer."""
import argparse,hashlib,importlib.util,json,pathlib
from fractions import Fraction as F

def need(x,m):
 if not x:raise ValueError(m)
def add(p,q):
 r=dict(p)
 for k,v in q.items():
  r[k]=r.get(k,F(0))+v
  if not r[k]:del r[k]
 return r
def scale(p,t):return {k:v*t for k,v in p.items() if v*t}
def mul(p,q):
 r={}
 for k,v in p.items():
  for j,w in q.items():
   e=tuple(x+y for x,y in zip(k,j));r[e]=r.get(e,F(0))+v*w
 return {k:v for k,v in r.items() if v}
def power(p,n):
 r={(0,)*len(next(iter(p))):F(1)}
 for _ in range(n):r=mul(r,p)
 return r
def decode(rows,n,trim=False):
 need(isinstance(rows,list),'whole coefficient list');r={}
 for e,c in rows:
  need(type(e) is list and all(type(x) is int for x in e),'exact powers')
  if trim:need(not any(e[n:]),'all unused columns zero');e=e[:n]
  need(len(e)==n and tuple(e) not in r,'full arity unique monomial');v=F(c)
  if v:r[tuple(e)]=v
  else:need(len(rows)==1 and not any(e),'only canonical explicit zero allowed')
 return r
def lift(p,n):return {k+(0,)*(n-len(k)):v for k,v in p.items()}
def cleared(p,num,den,deg):
 r={};a={(1,0):F(1)}
 for (i,j),v in p.items():r=add(r,scale(mul(mul(power(a,i),power(num,j)),power(den,deg-j)),v))
 return r
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def compare(primary,native):
 pp={k:decode(v,2) for k,v in primary['polynomials'].items()};np={k:decode(v,3,True) for k,v in native['whole_algebra']['complete_polynomials'].items()}
 count=0
 for k in pp:
  if k in np:need(lift(pp[k],3)==np[k],'whole '+k);count+=1
 # All additional native maps are generated from SEALED primary coefficients.
 for name,k in [('H_F_cleared','H'),('V_F_cleared','V')]:
  need(lift(cleared(pp[k],{(2,0):F(-4)},pp['d'],2),3)==np[name],'whole '+name);count+=1
 b2={(0,2,0):F(1)};c2={(0,0,2):F(1)};cv={(0,0,1):F(1)}
 DZ=scale(mul({(0,1,0):F(1)},lift(pp['L'],3)),F(-1,2048))
 den=mul(b2,power(DZ,2));eta_num=decode(primary['eta']['numerator'],3);eta_den=decode(primary['eta']['denominator'],3)
 need(den==np['eta_den'],'whole eta_den');count+=1
 need(mul(eta_num,den)==mul(np['eta_num'],eta_den),'entire unreduced eta_num rational equivalence');count+=1
 eta_clear=add(add(scale(mul(lift(pp['H'],3),c2),F(1536)),scale(mul(mul(b2,lift(pp['U'],3)),cv),F(-6144))),scale(mul(b2,lift(pp['W'],3)),F(-1)))
 need(eta_clear==np['eta_cleared'],'whole eta_cleared');count+=1
 need(add(mul(cv,lift(pp['H'],3)),scale(mul(b2,lift(pp['U'],3)),F(-2)))==np['centered_remainder'],'whole centered_remainder');count+=1
 need(count==22,'all 22 whole algebra objects')
 normmap={'H_a':'Ha','H_b':'Hb','L_a':'La','L_b':'Lb','center_num':'n','center_num_a':'na','center_num_b':'nb'}
 for k,v in native['whole_algebra']['complete_coefficient_norms'].items():need(F(v)==F(primary['norms'][normmap.get(k,k)]),'whole norm '+k)
 # Entire jet, including ordering change and Laurent denominator inversion.
 pjet=primary['jet'];num=decode(pjet['numerator'],11);denj=decode(pjet['denominator'],11)
 need(len(denj)==1,'single jet localization');(de,dc),=denj.items();jn={tuple(e[i] for i in [1,2,0,8,3,4,5,6,7,9,10]):v for e,v in decode(native['whole_moving_node_jet']['whole_second_mass_derivative'],11).items()}
 ownjet={tuple(x-y for x,y in zip(e,de)):v/dc for e,v in num.items()};need(ownjet==jn,'entire nine Laurent monomials')
 coeff=native['whole_Newton']['complete_first_seven_octic_coefficients'];need(len(coeff)==8,'all seven stages')
 for k in range(1,8):need(decode(primary['moments'][str(8-k)],5)==decode(coeff[k],5),'whole coefficient '+str(k))
 need(decode(coeff[0],5)=={(0,0,0,0,0):F(1)},'whole leading')
 scal=native['whole_scalar_certificate']['complete_scalars']
 checks={'projection_ratio':primary['comparisons']['small_H']['lower'],'Ca_error':primary['comparisons']['small_error']['lower'],'Cb_floor':primary['refinements']['reduced_margin'],'loga':primary['comparisons']['wlog_a']['lower'],'logb':primary['comparisons']['wlog_b']['lower'],'center_derivative':primary['comparisons']['center']['lower'],'full_gradient_transfer':primary['comparisons']['transfer']['lower'],'mass_second':str(sum(map(F,primary['jet_budgets']))),'weights_square':primary['refinements']['moment_weight']}
 for k,v in checks.items():need(F(v)==F(scal[k]),'scalar '+k)
 need(primary['jet_budgets']==native['whole_scalar_certificate']['complete_second_mass_bound_terms'],'all nine scalar terms')
 need(all(native['whole_scalar_certificate']['checks'].values()) and len(native['whole_scalar_certificate']['checks'])==20,'native all20checks')
 # Fresh ordinary rational identity absent from primary seal; disclosed as late supplement.
 HF=np['H_F_cleared'];VF=np['V_F_cleared']
 need(mul(VF,{(1,0,0):F(448),(0,0,0):F(-45)})==mul(mul({(1,0,0):F(224),(0,0,0):F(15)},lift(pp['A'],3)),HF),'late centered F identity')
 return dict(all_22_algebra_objects=True,all_10_norms=True,entire_eta_equivalence=True,all_nine_jet_monomials=True,all_eight_moment_coefficient_maps=True,all_nine_mass_budget_terms=True,nine_named_scalar_matches=True,native20checks=True,late_centered_F_identity=True)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--primary',type=pathlib.Path,required=True);ap.add_argument('--producer',type=pathlib.Path,required=True);a=ap.parse_args()
 spec=importlib.util.spec_from_file_location('late_native',a.producer/'verify.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 native=module.build_record();need(canonical(native)==canonical(json.loads((a.producer/'expected.json').read_text())),'ENTIRE native typed fixture')
 primary=json.loads(a.primary.read_text());result=compare(primary,native)
 # These six altered sealed coefficient records are rejected by cross-method equations.
 import copy
 damages=[]
 for name,edit in [
 ('DF-last',lambda p:p['polynomials']['DF'][-1].__setitem__(1,str(F(p['polynomials']['DF'][-1][1])+1))),
 ('G-lift-constant',lambda p:p['polynomials']['WG'][-1].__setitem__(1,str(F(p['polynomials']['WG'][-1][1])+1))),
 ('central-eta',lambda p:p['eta']['numerator'][-1].__setitem__(1,str(F(p['eta']['numerator'][-1][1])+1))),
 ('last-moving-node',lambda p:p['jet']['numerator'].pop()),
 ('seventh-moment-sign',lambda p:p['moments']['1'][-1].__setitem__(1,str(-F(p['moments']['1'][-1][1])))),
 ('large-F-budget',lambda p:p['refinements'].__setitem__('reduced_margin',str(F(p['refinements']['reduced_margin'])/100)))]:
  damaged=copy.deepcopy(primary);edit(damaged)
  try:compare(damaged,native)
  except ValueError as e:damages.append(dict(name=name,rejection=str(e)))
  else:raise ValueError('damaged whole record accepted '+name)
 result.update(native_whole_record_sha256=hashlib.sha256(canonical(native)).hexdigest(),primary_whole_sha256=hashlib.sha256(a.primary.read_bytes()).hexdigest(),cross_method_damages=damages,native_six_mathematical_damages=native['rejected_mathematical_damages'],scope='late corroboration after sealed independent primary; no producer edits or primary repairs')
 print(json.dumps(result,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
