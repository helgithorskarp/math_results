"""POSTSEAL full native entry comparison with sealed independent arithmetic."""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as F
import reconstruct as R
import original as O
from exact import need
from bivar import derive

def run(export,frozen,records):
 x=json.loads(export.read_text());native=json.loads(frozen.read_text());u=derive();counts=0;orders=[]
 def independent(phase):
  direct=records/(phase+'.json')
  if direct.exists():return json.loads(direct.read_text())
  if phase.startswith('negative'):return json.loads((records/'EXPECTED-negative.json').read_text())[phase]
  return json.loads((records/('EXPECTED-'+phase+'.json')).read_text())
 for q in range(6,24):
  d=R.build(q,6);n=d['N']-1;C=d['C'];Delta=d['D'];den=d['den'];ix=d['ix'];m=len(d['keys']);row=x['forms'][str(q)];keys=sorted(d['keys']);perm=[d['keys'].index(k) for k in keys]
  need(row['keys']==[list(k) for k in keys] and row['sizes']==[d['weights'][i] for i in perm],'ALL physical orbit keys and sizes')
  matrices={'C0':C,'Delta':Delta,'U0':[[den*(d['N']*int(i==j)-1)-C[i][j] for j in range(n)] for i in range(n)]}
  for name,edges in [('Rb',[(1,2,1),(2,5,-1)]),('Rc',[(1,4,1),(4,3,-1)]),('B',[(2,4,1)])]:
   mat=[[0]*n for _ in range(n)]
   for a,b,v in edges:mat[ix[a]][ix[b]]=mat[ix[b]][ix[a]]=den*v
   matrices[name]=mat
  compressed={}
  for name,mat in matrices.items():
   block=O.compression(mat,d,den);want=[[str(block[i][j]) for j in perm] for i in perm]
   need(want==row[name],'EVERY physical coefficient matrix entry '+name);compressed[name]=want;counts+=m*m
  if q in [22,23]:
   own=independent('positive-'+str(q))['positive'];g=[[F(compressed['C0'][i][j])+F(compressed['Delta'][i][j])/4096+8*(F(compressed['Rb'][i][j])+F(compressed['Rc'][i][j]))-10*F(compressed['B'][i][j]) for j in range(m)] for i in range(m)];h=[[d['N']*row['sizes'][i]*int(i==j)-row['sizes'][i]*row['sizes'][j]-g[i][j] for j in range(m)] for i in range(m)]
   w=row['sizes'];chi=[int(bool(k[0]&1)) for k in keys];ha=[a*b for a,b in zip(w,chi)]
   forms={'lower':g,'cap':h,'lower_floor':[[g[i][j]-F(1,65536)*(w[i]*int(i==j)-F(ha[i]*ha[j],d['s'])) for j in range(m)] for i in range(m)],'cap_floor':[[h[i][j]-F(w[i]*int(i==j),65536) for j in range(m)] for i in range(m)]}
   parent=native['positive' if q==22 else 'positive23']
   for name,mat in forms.items():
    values=[[str(v) for v in r] for r in mat];owned=own['whole_forms'][name];need(values==[[owned[i][j] for j in perm] for i in perm],'entire independent endpoint/floor form')
    digest=hashlib.sha256(json.dumps(values,sort_keys=True,separators=(',',':')).encode()).hexdigest();need(digest==parent['fixed_checks'][name]['matrix_sha256'],'whole native endpoint/floor digest')
    need(own['exact_congruences'][name]['rank']==parent['fixed_checks'][name]['rank'],'both complete ranks')
   need(own['all_actual_empty_positions']==parent['whole_positions'] and own['whole_unit_gap']==parent['whole_projected_unit_gap'] and own['star_sizes']==parent['stars'],'entire actual-empty/gap/star data')
  orders.append({'q':q,'physical_dimension':m,'actual_nonempty_positions':n*n})
 for own,name in [('Dn','cap_block_denominator'),('an','a_numerator'),('bn','b_numerator'),('dn','Delta_numerator')]:need(u[own]==x['ordinary_polynomials'][name],'ENTIRE ordinary polynomial '+own)
 need(u['P']==x['P'],'ENTIRE50-term necessary polynomial')
 for own,name in [('shifted_denominator','cap_block_denominator'),('shifted_slope','Delta_numerator')]:
  flipped=sorted([[j,i,v] for i,j,v in x['shifted'][name]])
  need(u[own]==flipped,'EVERY shifted coefficient after explicit variable-order transport')
 for phase in native['mean']+native['residual']:
  q=phase['q'];o=independent('negative-'+str(q));need(o['N']==phase['N'] and o['orientation']==(phase['orientation']['alpha'] if q<=18 else str(F(q*(q+1),2)+F(3*(q+1),3*q+5))),'whole negative cardinality/orientation')
  if q<=18:need(o['mean_plus_2c']==phase['margin'],'every actual mean margin')
  else:need(o['Qstar']==phase['values']['adjusted_cap_minimum'] and o['dstar']==phase['values']['Delta_pairing'] and o['entire_moment_Gram']==phase['values']['moment'],'entire adjusted residual/moment/slope')
 j=independent('joint-21');need(j['joint']['selected_three_rows']==native['joint']['rows_constant_kappa_tb_tc_sigma'] and j['joint']['all_original_affine_dual_coefficients']==native['joint']['total'],'ALL5 joint dual rows/total')
 for own,p in zip(j['joint']['all_six_original_energy_rows'],native['joint']['literal_pairings']):
  need(own['lower']==[p['C0'],p['Delta'],p['Rb'],p['Rc'],p['B']] and own['cap']==[p['U0'],str(-F(p['Delta'])),str(-F(p['Rb'])),str(-F(p['Rc'])),str(-F(p['B']))],'ALL6 separately decoded joint energies')
 return {'entire_physical_coefficients_compared':counts,'orders':orders,'entire_endpoint_and_floor_entries_compared':8*23*23,'all5_joint_dual_coefficients_match':True,'all6_literal_energy_rows_match':True,'entire_polynomial_maps_match':True,'native_output_is_comparison_not_independent_premise':True,'whole_export_sha256':hashlib.sha256(export.read_bytes()).hexdigest(),'native_full_record_sha256':hashlib.sha256(json.dumps(native,sort_keys=True,separators=(',',':')).encode()).hexdigest()}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('export',type=Path);ap.add_argument('frozen',type=Path);ap.add_argument('records',type=Path);ap.add_argument('--emit',type=Path);a=ap.parse_args();x=run(a.export,a.frozen,a.records)
 if a.emit:a.emit.write_text(json.dumps(x,indent=2)+'\n')
 print(json.dumps(x))
