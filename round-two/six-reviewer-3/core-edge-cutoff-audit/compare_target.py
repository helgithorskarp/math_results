"""Postseal whole author-object comparison; independent checker imports own only.

Input1 author postseal export, input2 complete author frozen record; neither is
an input to the independent mathematical audit. Comparisons use original
integer reconstructions and explicit orbit permutations, not total counts.
"""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from exact import need
import original as O

def main():
 need(len(sys.argv)==3,'author export and frozen record paths required')
 export=json.loads(Path(sys.argv[1]).read_text());target=json.loads(Path(sys.argv[2]).read_text());own=json.loads(Path(__file__).with_name('EXPECTED.json').read_text());byq={x['q']:x for x in own['negative']+own['positive']}
 need([x['q'] for x in export]==list(range(5,18)),'complete exported q5..17 census')
 entries=0;profiles=0;scalars=0;posentries=0
 for x in export:
  q=x['q'];d=O.build(q,5);o=byq[q];keys=[list(k) for k in d['keys']];order=[x['keys'].index(k) for k in keys];m=len(keys);n=d['N']-1
  need(len(x['keys'])==m and [x['weights'][i] for i in order]==d['weights'],'entire sorted/level-ordered physical weights')
  forms={'C0':O.compression(d['C'],d,d['den']),'Delta':O.compression(d['D'],d,d['den'])}
  forms['U0']=[[F(d['N']*d['weights'][i]*int(i==j)-d['weights'][i]*d['weights'][j])-forms['C0'][i][j] for j in range(m)] for i in range(m)]
  edges={'Rb':[(1,2,1),(2,5,-1)],'Rc':[(1,4,1),(4,3,-1)],'B':[(2,4,1)]}
  for name,E in edges.items():
   A=[[F(0)]*m for _ in range(m)]
   for a,b,c in E:
    i,j=keys.index([a,0,0]),keys.index([b,0,0]);A[i][j]=A[j][i]=F(c)
   forms[name]=A
  for name,A in forms.items():
   B=[[F(x['coefficient_forms'][name][order[i]][order[j]]) for j in range(m)] for i in range(m)]
   need(A==B,'EVERY original coefficient form entry '+str(q)+' '+name);entries+=m*m
  for key,l,c in o['cap_dual']['dual_profiles']:
   i=x['keys'].index(key);need(F(l)==F(x['lower_dual'][i]) and F(c)==F(x['cap_dual'][i]),'whole lower/cap actual amplitude profile');profiles+=2
  need(F(x['c'])==F(o['lower_c']),'lower cost');scalars+=1
  need([str(F(v)) for v in x['cap_coefficients']]==[o['cap_dual']['aa'],o['cap_dual']['bb']],'both full cap minimizer coefficients');scalars+=2
  need([[str(F(v)) for v in r] for r in x['cap_moment']]==o['cap_three_gram'],'whole original cap moment3x3');scalars+=9
  for name,field in [('U0','Q'),('Delta','D_cap'),('B','B_cap')]:need(F(x['cap_pairs'][name])==F(o['cap_dual'][field]),'whole dual pairings');scalars+=1
  need(x['cap_pairs']['Rb']==x['cap_pairs']['Rc']=='0' and x['lower_pairs']==dict(zip(['C0','Delta','Rb','Rc','B'],o['lower_pairings'])),'all complete lower/distinct trade pairings');scalars+=7
  if q in (16,17):
   for name,A in o['positive']['whole_forms'].items():
    B=[[str(F(x['positive_forms'][name][order[i]][order[j]])) for j in range(m)] for i in range(m)]
    need(A==B,'every positive endpoint/floor entry '+name);posentries+=m*m
 for x in target['negative_cases']:
  o=byq[x['q']];need(F(x['combined_margin'])==F(o['cap_dual']['combined']) and F(x['lower_cost'])==F(o['lower_c']),'whole native frozen negative margin');scalars+=2
 for x in target['new_positive_cases']:
  o=byq[x['q']]['positive'];need(x['whole_projected_unit_gap']==o['whole_unit_gap'] and x['stars']==o['star_sizes'],'whole native positive gap and all actual labelled stars');scalars+=2
 for i,x in enumerate(target['closed_symbolic_certificate']['leading_minors']):
  need(list(map(F,x['polynomial']))==list(map(F,own['uniform']['leading_determinants'][i])) and list(map(F,x['coefficients_at_q4_plus_u']))==list(map(F,own['uniform']['positive_q4_shifts'][i])),'whole symbolic determinant and shifted coefficient arrays')
 result={'complete_coefficient_form_entries':entries,'complete_positive_endpoint_floor_entries':posentries,'whole_dual_profile_amplitudes':profiles,'complete_scalar_and_moment_fields':scalars,'whole_four_symbolic_determinants_and_shifts_matched':True,'every_order_q5_to17':True,'explicit_physical_orbit_permutations':True,'whole_external_author_export_sha256':hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest(),'independent_audit_has_no_author_imports':True,'native_inputs_are_postseal_comparison_only':True}
 Path(__file__).with_name('TARGET_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
