"""Cold normal/optimized full comparisons plus meaningful semantic rejections."""
import argparse,copy,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path
from fractions import Fraction as Q

HERE=Path(__file__).resolve().parent
THREADS=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']

def need(ok,reason):
    if not ok:raise ValueError(reason)


def main(out):
    seal=json.loads((HERE/'PRIMARY_SEAL.json').read_text())
    for name,row in seal['primary_files'].items():
        raw=(HERE/name).read_bytes();need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'whole primary seal '+name)
    env=os.environ.copy()
    for key in THREADS:env[key]='1'
    runs=[];outputs={};rejected=[]
    with tempfile.TemporaryDirectory(prefix='original-cut-')as folder:
        cold=Path(folder)
        for name in seal['primary_files']:shutil.copyfile(HERE/name,cold/name)
        def run(file,optimized,args,expect_success):
            rawout=cold/'child-output.json'
            if rawout.exists():rawout.unlink()
            cmd=[sys.executable,'-B']+(['-O']if optimized else [])+[str(cold/file),*args,'--output',str(rawout)]
            start=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=45)
            seconds=time.monotonic()-start
            runs.append({'file':file,'optimized':optimized,'seconds':round(seconds,6),'returncode':p.returncode})
            need((p.returncode==0)==expect_success,'expected semantic child status '+file+'\n'+p.stderr)
            if expect_success:
                need(not p.stderr,'unexpected positive stderr');return rawout.read_bytes()
            need('ValueError:'in p.stderr,'semantic rejection, not kill/timeout')
            need(not rawout.exists(),'damaged input emitted acceptance record')
            return p.stderr.split('ValueError:')[-1].strip()
        for file in ['check.py','literal.py']:
            normals=run(file,False,[],True);optimized=run(file,True,[],True)
            need(json.loads(normals)==json.loads(optimized) and normals==optimized,'EVERY whole regenerated record field normal/O '+file)
            outputs[file]={'bytes':len(normals),'sha256_after_full_comparison':hashlib.sha256(normals).hexdigest()}
            (out/(file+'.json')).write_bytes(normals)
        original=json.loads((cold/'INPUT.json').read_text());old=json.loads((cold/'N24_INPUT.json').read_text())
        changes=[('wrong_original_ground','n',None,25),('incomplete_real_labels','names',-1,'t12_12'),('wrong_profile','integer_layer_direction',7,526),('negative_empty_weight','empty_direction_weight',None,-2518),('lost_deficit_cancellation','deficit_difference_weights',4,original['deficit_difference_weights'][4]+1),('wrong_proper_cut','full36_affine_cut_coefficients',10,str(Q(original['full36_affine_cut_coefficients'][10])+1)),('wrong_transport','fixed_transported_proper_values',29,str(Q(original['fixed_transported_proper_values'][29])+1)),('wrong_negative_pairing','strict_negative_fixed_slice_pairing',None,str(Q(original['strict_negative_fixed_slice_pairing'])+1))]
        for label,key,index,value in changes:
            changed=copy.deepcopy(original)
            if index is None:changed[key]=value
            else:changed[key][index]=value
            p=cold/'damage.json';p.write_text(json.dumps(changed))
            for opt in [False,True]:rejected.append({'label':label,'optimized':opt,'rejected_semantically':True,'reason':run('check.py',opt,['--input',str(p)],False)})
        bad=copy.deepcopy(old);bad['values'][6]=str(Q(bad['values'][6])+1);p=cold/'old-damage.json';p.write_text(json.dumps(bad))
        for opt in [False,True]:rejected.append({'label':'wrong_credited_n24_transport_input','optimized':opt,'rejected_semantically':True,'reason':run('check.py',opt,['--old-input',str(p)],False)})
    record={'agent':'six-reviewer-1','role':'independent mathematical reviewer','python':sys.version,'full_cold_positive_records':outputs,'positive_children':4,'semantic_rejections':rejected,'total_children':len(runs),'serial_one_math_child':True,'native_threads':{k:env[k]for k in THREADS},'fixed_child_guard_seconds':45,'all_six_primary_sealed_files_unchanged':True,'whole_normal_optimized_positive_records_equal':True,'runs':runs,'total_child_wall_seconds':round(sum(r['seconds']for r in runs),6),'maximum_child_wall_seconds':max(r['seconds']for r in runs),'proof_scope':'Ordinary real affine counting, exact input, no imported author code, no float/solver/PSD sample extrapolation.'}
    (out/'VALIDATION.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items()if k not in ['runs','semantic_rejections']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);main(a.out)
