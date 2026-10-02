"""Own-only postseal adapter; no author imports; compares EVERY common field."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,signal,time
from linear import need,canonical,digest,psd
from core import read_seed,complete,sector,constants,pairs,mass,lift_rows
ROOT=Path(__file__).resolve().parent

def native_digest(A):return hashlib.sha256(json.dumps([[str(v)for v in row]for row in A],separators=(',',':')).encode()).hexdigest()
def audit(native,fields):
 own=json.loads((ROOT/'EXPECTED.json').read_text())['core'];beta,dec=complete(32,read_seed());r,N,s,h=constants(32);reference={p:F(s-1)if sum(p)==32 else F(0)for p in beta if p[0]>=2};rb,rd=complete(32,reference)
 need(fields['all255_supported_coordinates']==dec['whole_supported_table'],'ALL255 original decoded coordinates')
 common={};positions=0;certificates=[]
 for name,b in [('seed',beta),('ordinary_reference',rb)]:
  wanted=[]
  for j in range(17):
   g=sector(32,b,j);wanted.append({k:g[k]for k in ['degree','layers','metric','K','U','G','H']});positions+=4*len(g['layers'])**2
  need(canonical(wanted)==fields[name],'ALL original full coefficient fields; every position/norm/layer including mean/high')
  common[name+'_whole_fields_sha256']=digest(wanted)
 sectors=[];reference_sectors=[]
 for j in range(17):
  g=sector(32,beta,j);d=len(g['layers']);shift=[[g['H'][i][t]-F(1,1024)*g['metric'][i]*(i==t)for t in range(d)]for i in range(d)];rec=own['all17_full_sector_certificates'][j]
  sectors.append({'j':j,'layers':g['layers'],'order':d,'multiplicity':g['multiplicity'],'lower_rank':rec['lower']['rank'],'upper_gap_rank':rec['original_cap_floor_certificate']['rank'],'lower_sha256':native_digest(g['G']),'upper_gap_sha256':native_digest(shift)})
  rg=sector(32,rb,j);rr=own['all17_ordinary_uncapped_reference_sectors'][j];reference_sectors.append({'j':j,'order':len(rg['layers']),'lower_rank':rr['lower']['rank'],'lower_sha256':native_digest(rg['G']),'upper_sha256':native_digest(rg['H'])})
 li=canonical(lift_rows(32,beta));ma=mass(32,beta,8);classes=[[z['a'],z['b'],str(beta[z['a'],z['b']]),z['count'],str(z['mass'])]for z in ma['all_positive_original_classes']]
 seed={'n':32,'N':N,'s':s,'h':h,'free_coordinates':225,'active_S8_coordinates':169,'excluded_proper_pairs':56,'star_equation_rank':30,'least_support_cutoff':8,'core_lower_rank':N-33,'whole_lower_rank':N-32,'whole_upper_rank':N-1,'whole_cap_floor':'1/1024','noncentered_core_row_sums':li['all_core_constant_rows'],'actual_empty_L00':li['actual_empty_L_loop'],'actual_empty_L0a':li['all_actual_empty_L_entries'],'sectors':sectors,'positive_bulk_mass_k7':str(ma['total_mass']),'positive_bulk_classes':classes,'credited9471_tail_control':{'B':own['imported_necessity_control']['B'],'R':own['imported_necessity_control']['R'],'holds':True}}
 native_seed={k:v for k,v in native['seed'].items()if k!='star_decoders'};need(seed==native_seed,'ENTIRE native mathematical seed export, only method-count label excluded')
 ref={'whole_lower_rank':N-32,'upper0_diagonal':-31138511967,'sectors':reference_sectors};need(ref=={k:v for k,v in native['credited_n32_ordinary_reference'].items()if k!='credited'},'ENTIRE ordinary reference mathematical export')
 common.update({'entire_seed_mathematical_export':seed,'entire_ordinary_reference_mathematical_export':ref,'all255_decoded_coordinates_sha256':digest(dec['whole_supported_table']),'all225_seed_inputs_sha256':own['original_seed_sha256'],'original_seed_file_sha256':hashlib.sha256((ROOT/'seed.json').read_bytes()).hexdigest(),'total_full_coefficient_positions':positions,'all34_full_sector_norm_layer_fields':True,'all68_lower_and_upper_form_hashes':True})
 need(common['original_seed_file_sha256']==native['seed_sha256'],'ENTIRE original rational seed bytes');need(positions==50360,'entire2tablesx4field coefficient census')
 common['scope']='ALL common mathematical n32seed/reference fields except native-method count and explanatory labels; entire baseline729arithmetic/n6native-controls later replay only, not new primary independent baseline verdict. New1/512 gap independent, not native output. No truncated-hash/selected-coefficient comparison.'
 return common

def main():
 p=argparse.ArgumentParser();p.add_argument('native_record',type=Path);p.add_argument('native_fields',type=Path);p.add_argument('--freeze',action='store_true');args=p.parse_args();t=time.monotonic();result=audit(json.loads(args.native_record.read_text()),json.loads(args.native_fields.read_text()));raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode();expected=ROOT/'COMPARISON.json'
 if args.freeze:need(not expected.exists(),'late full comparison already frozen');expected.write_bytes(raw+b'\n')
 else:need(json.loads(expected.read_text())==result,'ENTIRE frozen common comparison')
 print(json.dumps({'whole_comparison_sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'seconds':time.monotonic()-t,'optimize':__import__('sys').flags.optimize,'entire_COMPARISON_equal':not args.freeze,'all_original_positions':result['total_full_coefficient_positions']}))
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s late own comparison')));signal.alarm(45);main()
