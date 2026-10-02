"""Postseal own-only adapter; no author function imported or executed.

Input is the byte-pinned target frozen JSON. Not a premise of primary proof.
Only whole original common records are compared; new domain/repair is separate.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,signal
from linear import need,canonical,digest
from affine import parameters
from variance import scalar
from orbits import forms,three_space,vectors
from coefficient import audit as coefficients

ROOT=Path(__file__).resolve().parent

def encoded(q,k):
 g=forms(q,k);return canonical({'q':q,'k':k,'N':g['N'],'s':g['s'],'keys':g['keys'],'sizes':g['sizes'],**{n:g[n]for n in ['C0','Delta','R','U0']}})

def run(author):
 a=json.loads(Path(author).read_text());own=json.loads((ROOT/'EXPECTED.json').read_text());by={r['phase']:r['record']for r in own['records']};fields=[]
 def match(label,left,right):
  need(canonical(left)==canonical(right),'ENTIRE common record mismatch '+label);fields.append({'label':label,'whole_sha256':digest(left)})
 cert=by['coefficient.py']['original_coefficients']
 for r,name in zip(cert,['V2','det_num','Delta_num']):
  # Author axes are (q-3k,k-2); own axes are (k-2,q-3k).
  target=sorted([[ij[1],ij[0],v]for ij,v in a['new_universal_necessary_mechanism']['certificates'][name]['coefficients']]);match('ALL '+name+' coefficient positions',r['all_coefficients'],target)
 match('whole positive boundary partition',[r['k']for r in by['boundary.py']['all20_boundary_records']if r['decision']=='positive'],a['complete_classification']['positive_boundary_cutoff_b_minus5'])
 match('whole negative boundary partition',[r['k']for r in by['boundary.py']['all20_boundary_records']if r['decision']=='negative'],a['complete_classification']['negative_boundary_cutoff_b_minus4'])
 cases=[];scalar_positions=0
 for r,t in zip(by['boundary.py']['all20_boundary_records'],a['finite_boundary_cases']['records']):
  q,k=r['q'],r['k'];g=forms(q,k);d=three_space(q,k);old=parameters(q,k);ss=scalar(q,k)
  left={'q':q,'k':k,'N':g['N'],'Q0':str(old['Q0']),'credited_dual_Delta':str(old['D4']),'m':str(ss['m']),'forms_digest':digest(encoded(q,k)),'three_vector_Q':str(d['Q']),'three_vector_Delta':str(d['d'])}
  right={n:t[n]for n in left}
  if r['decision']=='positive':
   p=r['repairs'][0];extra={'zero_fixed_cap_floor':r['delta'],'whole_zero_cap_floor':r['whole_zero_floor'],'kappa':r['kappa'],'t':p['t'],'whole_repaired_cap_floor':p['whole_projected_cap_floor'],'repaired_fixed_lower_rank':p['lower_rank'],'repaired_fixed_cap_rank':p['upper_floor_rank'],'new_beyond_9546_m_criterion':ss['m']<=0}
   left.update(canonical(extra));right.update({n:t[n]for n in extra})
  match('ENTIRE common finite record k'+str(k),left,right);scalar_positions+=len(left);cases.append({'k':k,'q':q,'decision':r['decision'],'whole_common_fields':len(left),'whole_common_sha256':digest(left)})
 for t in a['new_universal_necessary_mechanism']['exact_calibrations']:
  q,k=t['q'],t['k'];d=three_space(q,k);renames={'determinant':'D','Delta':'d'};left={n:d[renames.get(n,n)]if type(t[n])is int else str(d[renames.get(n,n)])for n in t};match('every3space calibration q'+str(q),left,t)
 baseline=[]
 for r,t in zip(by['baselines.py'],a['calibration']['fixtures']):
  q,k=r['q'],r['k'];g=forms(q,k);left={'q':q,'k':k,'N':g['N'],'original_pair_count':r['all_original_nonempty_positions'],'orbit_sizes':g['sizes'],'forms_digest':digest(encoded(q,k))};right={n:t[n]for n in left};match('full original-pair forms q'+str(q),left,right);baseline.append(left)
 lit=by['literal.py'];q,k=74,15;g=forms(q,k);vec=vectors(g['keys']);w=[255-3*y+v for one,y,v in zip(*vec)];target=a['independent_original_exception'];pairs=lit['integer_original_dual_pairings'];left={'N':lit['N'],'q':q,'k':k,'original_members':lit['nonempty_original_members'],'original_representative_positions':lit['whole_representative_member_positions'],'original_dual':canonical(w),'original_U0':pairs['U0'],'original_Delta':pairs['Delta'],'original_R':pairs['R'],'original_lower_orientation':lit['alpha'],'original_forms_digest':digest(encoded(q,k))};match('whole physical exception common exported record',left,{n:target[n]for n in left})
 match('each of ALL4x529 original exception coefficients',lit['whole_original_four_coefficient_Grams'],canonical({n:g[n]for n in ['C0','Delta','R','U0']}))
 target=a['new_compact_original_exceptional_dual'];left={'keys':g['keys'],'sizes':g['sizes'],'vector':w,'original_U0':pairs['U0'],'original_Delta':pairs['Delta'],'original_R':pairs['R'],'q':q,'k':k};match('entire compact original dual',left,{n:target[n]for n in left})
 record={'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'PASS','postseal_adapter_only_no_primary_changes':True,'author_frozen_file_sha256':hashlib.sha256(Path(author).read_bytes()).hexdigest(),'entire_common_records':fields,'finite_cases':cases,'finite_common_field_positions':scalar_positions,'complete_original_coefficient_positions':133,'full_original_baseline_positions':291661,'full_original_exception_representative_positions':73853,'all_four_exception_Gram_entry_positions':2116,'baselines':baseline,'scope':'ALL original shifted coefficient lists with explicit axis permutation, every exported common scalar/decision/floor/repair/rank/weighted form hash/wholecompact dual; own original exceptional Grams. New208coeffdomain and9enlargedrepairs are primary evidence, not native exported results. Label-dependent original member amplitude streams not equated; last15 vs first15 are related by outside permutation. Native characteristic fingerprints not independently regenerated; earlier q24 evaluated fullpoint credited to owned9586, not new thispass.'}
 return canonical(record)

if __name__=='__main__':
 def alarm(*args):raise TimeoutError('fixed60s lateadapter; incomplete is not exclusion')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60);parser=argparse.ArgumentParser();parser.add_argument('--author-expected',required=True);args=parser.parse_args();record=run(args.author_expected);raw=json.dumps(record,sort_keys=True,separators=(',',':'))+'\n';expected=ROOT/'COMPARISON.json'
 if not expected.exists()or json.loads(expected.read_text())!=record:raise ValueError('ENTIRE latecomparison differs')
 print(json.dumps({'status':'PASS','entire_COMPARISON_equal':True,'whole_record_sha256':hashlib.sha256(raw.encode()).hexdigest(),'whole_common_records':len(record['entire_common_records']),'finite_common_field_positions':record['finite_common_field_positions']},sort_keys=True))
