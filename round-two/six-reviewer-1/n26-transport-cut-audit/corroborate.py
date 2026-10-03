"""Optional LATE native source replay; not the primary independent proof."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from fractions import Fraction as Q
from pathlib import Path

HERE=Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)


def main(native,primary,out):
    p=json.loads(primary.read_text());prov=json.loads((HERE/'PROVENANCE.json').read_text())
    seal=json.loads((HERE/'PRIMARY_SEAL.json').read_text())
    for name,row in seal['primary_files'].items():need(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==row['sha256'],'unchanged independent primary seal')
    # Every target field is compared to fresh primary results or explicitly
    # credited inputs/status/control data, not merely to a compact digest.
    mask_to_points=lambda mask:[j+1 for j in range(26)if mask&(1<<j)]
    inp=json.loads((HERE/'INPUT.json').read_text())
    expected={'agent':'six-downset-2','role':'researcher','status':'exact original rank-nine PSD dual verified','n':26,'N':p['N'],'s':p['s'],'h':p['h'],'original_profiles':[inp['integer_layer_direction'],inp['old_integer_layer_direction']],'original_positive_weights':p['nine_positive_weights'],'original_dual_rank':p['rank_Y'],'rank_minor_vertices':list(map(mask_to_points,p['rank_minor_rows'])),'rank_minor':p['rank_minor'],'rank_minor_determinant':p['rank_minor_determinant'],'complete_affine_basis_probes':p['basis_count'],'whole_table_entries_compared':p['original_class_coefficient_count'],'all_original_row_star_support_and_empty_equations':True,'full36_affine_cut_intercept':str(p['cut'][0]),'full36_affine_cut_coefficients':list(map(str,p['cut'][1:])),'fixed_transported_proper_values':p['transported_values'],'strict_negative_fixed_slice_pairing':p['P0'],'all_real_six_deficit_fixed30_family_excluded':True,'original_lower_PSD_only':True,'upper_cap_not_used':True,'full36_real_face_infeasible':False,'literal_baseline':{'credited_claim':'8319/0','vertices':247,'entries_compared':61009,'signed_profile_energies':['1461768/5','3652'],'difference_energies':['12','179/50','449/100'],'actual_empty_loop':'20841/100','new_research':False},'public_dependency_sha256':{row['name']:row['sha256']for row in prov['native_dependencies']},'solver_or_numeric_input_used':False,'harmonic_completeness_needed':False,'ordinary_proof_unformalized':True,'independent_new_result_review':'pending','semantic_rejections':[{'label':label,'rejected':True,'reason':reason}for label,reason in [('negative_empty_weight','All eight nontrivial original outer-product weights positive'),('negative_profile_weight','All eight nontrivial original outer-product weights positive'),('negative_difference_weight','All eight nontrivial original outer-product weights positive'),('missing_empty_energy','All eight nontrivial original outer-product weights positive'),('wrong_independent_deficit_weight','ALL six independent real deficit coefficients cancel'),('wrong_actual_profile','ALL six independent real deficit coefficients cancel'),('wrong_proper_only_cut','Entire claimed proper-only affine cut regenerated exactly'),('wrong_exact_transport','All30 exact proper values reproduced from public10080 seed')]]}
    env=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:env[key]='1'
    native_bytes=[];runs=[]
    with tempfile.TemporaryDirectory(prefix='late-native-original-cut-')as tmp:
        root=Path(tmp);target=root/'six_deficits_n26';target.mkdir()
        for name,row in prov['all9_target_file_whole_byte_pins'].items():
            raw=(native/name).read_bytes();need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'every whole native source pin');(target/name).write_bytes(raw)
        for row in prov['native_dependencies']:
            src=native.parent/'minimal_complement_classes_n24'/row['name'];raw=src.read_bytes()
            need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'every whole native dependency pin')
            dst=root/'minimal_complement_classes_n24'/row['name'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
        for optimized in [False,True]:
            output=root/('optimized.json'if optimized else 'normal.json')
            cmd=[sys.executable,'-I','-B']+(['-O']if optimized else [])+[str(target/'verify.py'),'--audit','--check',str(target/'expected.json'),'--output',str(output)]
            start=time.monotonic();child=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=45);elapsed=time.monotonic()-start
            need(child.returncode==0 and not child.stderr,'late native positive child\n'+child.stderr)
            raw=output.read_bytes();need(json.loads(raw)==expected,'EVERY entire native mathematical field versus declared fresh/credited comparison')
            native_bytes.append(raw);runs.append({'optimized':optimized,'returncode':child.returncode,'seconds':round(elapsed,6),'stdout':json.loads(child.stdout)})
        need(native_bytes[0]==native_bytes[1],'WHOLE original native normal/O record equality')
    raw=native_bytes[0];(out/'native-whole-record.json').write_bytes(raw)
    record={'agent':'six-reviewer-1','role':'independent mathematical reviewer','new_native_exposure_late_after_primary_seal':True,'corroboration_not_primary_proof':True,'all_original_native_record_fields_compared':True,'credited_literal_n8_control_not_independent_new_proof':True,'native_record_bytes':len(raw),'native_record_sha256_after_full_comparison':hashlib.sha256(raw).hexdigest(),'whole_normal_optimized_records_equal':True,'positive_children':2,'author_semantic_rejections':16,'all_target_and_three_dependency_pins_verified':True,'serial_one_math_child':True,'fixed_child_guard_seconds':45,'native_threads':{k:env[k]for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']},'runs':runs,'total_child_wall_seconds':round(sum(r['seconds']for r in runs),6),'maximum_child_wall_seconds':max(r['seconds']for r in runs)}
    (out/'CORROBORATION.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items()if k!='runs'},indent=2))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--native',type=Path,required=True);a.add_argument('--primary',type=Path,required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args();x.out.mkdir(parents=True,exist_ok=True);main(x.native,x.primary,x.out)
