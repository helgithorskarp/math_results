"""Late data-only audit: no producer module import or coefficient discovery claim."""
import hashlib,json,pathlib,sys,itertools
from fractions import Fraction as F
import sympy as sp
from sympy.polys.rings import ring
from sympy.polys.domains import QQ
P=pathlib.Path(sys.argv[1]);own=json.loads((P/'normal.stdout').read_text())
native=json.loads((P/'native-normal.json').read_text());old=json.loads((P/'cubic-quintic-exclusion/expected.json').read_text());base=json.loads((P/'degree-five-triangular/expected.json').read_text())
export=json.loads((P/'pencil-export.json').read_text())
damage=sys.argv[sys.argv.index('--damage')+1] if '--damage' in sys.argv else None
if damage=='unit':native['whole_small_s_row_unit_Z'][3][-1][1]=str(F(native['whole_small_s_row_unit_Z'][3][-1][1])+1)
if damage=='witness':old['whole_primitive_minor_x_unit_multipliers'][0][-1][1]=str(F(old['whole_primitive_minor_x_unit_multipliers'][0][-1][1])+1)
if damage=='content':old['whole_specialized_positive_contents'][4]='1'
def need(ok,label):
 if not ok:raise ValueError(label)
def canon(rows,n=5):
 out=[]
 for e,c in rows:
  need(len(e)>=n and all(k==0 for k in e[n:]),'complete coefficient localization')
  need(isinstance(c,str),'typed rational coefficient')
  out.append((tuple(e[:n]),str(F(c))))
 need(len(set(e for e,c in out))==len(out),'unique complete coefficient keys')
 return sorted(out)
for i,key in enumerate(['tODE2','tODE1','tODE0','K1','K0plus4']):need(canon(own['full_residuals'][i])==canon(export['residuals_ascending'][i]),'entire original residual '+key)
need(canon(own['full_Fstar'])==canon(export['h_ascending'][2]),'entire original reconstructed Fstar')
for name,key in [('full_row_unit','whole_small_s_row_unit_Z'),('all_five_difference_quotients','whole_E_difference_quotients')]:
 need([canon(v) for v in own[name]]==[canon(v) for v in native[key]],'every late full map '+key)
need([[str(v) for v in own['derivative_norms_degrees'][3*i+j][:1]] for i in range(5) for j in range(3)]==[[x] for row in native['whole_R_B_E_s_derivative_norms'] for x in row],'all fifteen norms')
need(own['constants']['c0']==native['unrounded_coercivity_constant'],'whole exact constant')
R,r,x,u=ring('r,x,u',QQ)
def dec(rows):
 out=R.zero
 for e,c in rows:
  need(len(e)==10 and all(not e[j] for j in [0,1,5,6,7,8,9]),'parent exact r/x/u variables')
  out+=QQ.convert(F(c))*r**e[2]*x**e[3]*u**e[4]
 return out
M=[[dec(v) for v in row] for row in old['whole_five_by_three_matrix']]
ps=[dec(v) for v in old['whole_Fstar_zero_primitive_quadratics']]
for row,p in zip(M,ps):need(row[0]*u*u+row[1]*u+row[2]==p,'all five complete matrix rows')
Ds=[];U=[]
def norm(p):return sum((F(str(c)).__abs__() for c in p.values()),F(0))
for idx,trip in enumerate(itertools.combinations(range(5),3)):
 d=R.zero
 for perm in itertools.permutations(range(3)):
  sign=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3));d+=sign*M[trip[0]][perm[0]]*M[trip[1]][perm[1]]*M[trip[2]][perm[2]]
 g=int(old['whole_positive_integer_determinant_contents'][idx]);need(d==g*dec(old['whole_primitive_three_by_three_minors'][idx]),'every full determinant')
 lu=R.zero
 for e,c in old['whole_primitive_minor_x_unit_multipliers'][idx]:
  need(len(e)==2,'whole witness exponents');lu+=QQ.convert(F(c))*r**e[0]*x**e[1]
 Ds.append(d);U.append(lu/g)
need(sum((a*b for a,b in zip(U,Ds)),R.zero)==x,'all seventy-two parent witness coefficients multiply to x')
normraw=sum(map(norm,U),F(0));Q=sum((norm(v)**2 for row in M for v in row),F(0))
need(str(normraw)==old['exact_raw_unit_coefficient_norm'] and 0<normraw<F(1,10**13),'whole raw margin')
need(Q==14913669297722925580854623,'whole fifteen-entry coefficient norm')
# Original Laurent pullbacks retain every coefficient and all five positive contents.
bs,es,rs,ss,ts=sp.symbols('B E r s t')
def expression(rows,vars):return sp.Add(*(sp.Rational(c)*sp.prod(g**k for g,k in zip(vars,e)) for e,c in rows))
ep=(-141120*rs**2*ss*ts+94080*rs*ss**3*ts-82320*rs*ss*ts+501760*rs+21840*ss**3*ts-9945*ss*ts-376320*ss**2+215040)/(37184*ss*ts)
for i,k in enumerate([2,1,2,1,2]):
 left=expression(own['full_residuals'][i],(bs,es,rs,ss,ts)).subs({bs:0,es:ep},simultaneous=True)*ss**k
 right=ps[i].as_expr().subs({'r':rs,'x':ss**2,'u':ss*ts},simultaneous=True)*sp.Rational(old['whole_specialized_positive_contents'][i])
 need(sp.cancel(left-right)==0,'whole original primitive row pullback')
out=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',data_only=True,producer_imports=False,whole_defining_maps=6,whole_new_maps=10,whole_new_unit_coefficients=45,all_fifteen_derivative_norms=True,all_five_original_primitive_pullbacks=True,all_fifteen_matrix_entries_all_ten_minors_all_seventy_two_credited_witness_coefficients=True,exact_parent_raw_unit_norm=str(normraw),Q=str(Q),all_five_content_inverses=[str(1/F(c)) for c in old['whole_specialized_positive_contents']],full_native_record_sha256=hashlib.sha256(json.dumps(native,sort_keys=True,separators=(',',':')).encode()).hexdigest())
print(json.dumps(out,sort_keys=True,separators=(',',':')))
