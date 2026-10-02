"""Late data-only comparison; no producer import or execution here.
Every new polynomial stream and characteristic-zero determinant coefficient
is compared. The producer's different257 unit is independently multiplied.
"""
import json,hashlib,sys
from pathlib import Path
from fractions import Fraction as F
from polys import Poly,symbol,need
from audit import load
from exact import ma,mm,mt,scalar,quotient

NAMES=['B','E','r','s','t','v','w','unused7','unused8','unused9']
def decode(a):
 d={}
 for key,z in a:
  need(len(key)==10 and all(type(n)==int and n>=0 for n in key),'whole typed producer exponent')
  k=tuple(sorted((x,n) for x,n in zip(NAMES,key) if n));need(k not in d,'unique producer exponent');d[k]=(F(z),0)
 return Poly(d)
def main():
 own=json.loads(Path(__file__).with_name('EXPECTED.json').read_text());p=json.loads(Path(sys.argv[1]).read_text());g=p['entire_generated_polynomials'];comparisons=[]
 def eq(label,a,b):need(a==b,label);comparisons.append(label)
 for i in range(5):
  for j in range(3):eq('whole matrix '+str(i)+','+str(j),load(own['whole_s0_matrix'][i][j]),decode(g['matrix_s0'][i][j]))
  eq('whole residual '+str(i),load(own['whole_s0_residuals'][i]),decode(g['residuals_s0'][i]))
 for j,i in enumerate([0,1,2,4]):
  eq('whole Y '+str(i),load(own['whole_Y'][j]),decode(g['Y'][str(i)]));eq('whole W '+str(i),load(own['whole_Wi'][j]),decode(g['cleared_W'][str(i)]))
 for j,k in enumerate(['A5','A4']):eq('whole '+k,load(own['whole_A'][j]),decode(g[k]))
 rr=symbol('r');fullR3=load(own['whole_checks']['complete R3']);hh=fullR3.coefficient('t',1)/-112;kk=fullR3.coefficient('t',2).divide_monomial({'B':1});ww=-(2112*kk-14400*hh)/3456;dd=quotient(load(own['whole_checks']['complete 023 minor']),F(5,774144)*(7*rr+3)*hh)
 for name,poly in [('H',hh),('K',kk),('W',ww),('D',dd)]:eq('every auxiliary coefficient '+name,poly,decode(g[name]))
 eq('whole H0 linear primitive remainder',load(own['H0']['primitive_L']),decode(g['HK_linear_remainder']))
 for j,k in enumerate(['1','4']):
  a=own['resultants'][j];b=p['D_branch_fixed_resultants'][k]
  eq('every entire resultant coefficient '+k,list(map(int,a['whole_coefficients'])),b['entire_determinant'])
  eq('entire resultant content '+k,F(a['content']),F(b['content']))
  eq('entire normalized quotient '+k,load(own['whole_quotients'][j]),decode([[([0,0,i,0,0,0,0,0,0,0]),str(c)] for i,c in enumerate(b['normalized_quotient']) if c]))
 for ownname,prodname in [('H0','H0_K0_nonzero_resultant'),('exceptional_r','r_minus3over7_nonzero_resultant')]:
  a=own[ownname];b=p[prodname];eq('entire fixed matrix '+ownname,[[int(scalar(load(x))) for x in row] for row in a['full_matrix']],b['entire_matrix']);eq('full determinant '+ownname,a['determinant'],b['determinant'])
 z=p['D_branch_whole_finite_unit'];prime=z['prime'];need(prime==257 and all(prime%d for d in range(2,17)),'producer prime257')
 arr=[p['D_branch_fixed_resultants'][k]['normalized_quotient'] for k in ['1','4']];eq('all257 left coefficients',mt(arr[0],prime),z['left']);eq('all257 right coefficients',mt(arr[1],prime),z['right']);need(arr[0][-1]%prime and arr[1][-1]%prime,'producer integer leading degrees retained')
 eq('entire257 multiplier identity',ma(mm(z['left_multiplier'],z['left'],prime),mm(z['right_multiplier'],z['right'],prime),prime),[1])
 raw=json.dumps(p,sort_keys=True,separators=(',',':')).encode();out={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','phase':'late after sealed new independent proof/code/record','producer_canonical_sha256':hashlib.sha256(raw).hexdigest(),'producer_canonical_bytes':len(raw),'full_comparisons':comparisons,'producer_code_imports':0,'different_modular_unit':'own263 and producer257 both fully verified','all_whole_streams_matched':True};print(json.dumps(out,indent=2))
if __name__=='__main__':main()
