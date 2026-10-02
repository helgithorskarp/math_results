"""Reproduce the complete native20 exclusion, serially under55s stage guards."""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def clean(value):
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items() if k not in ('seconds','maximum_rss_kib','elapsed')}
    if isinstance(value,list):return [clean(v) for v in value]
    return value
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',default='scratch/native20-evidence')
    args=parser.parse_args();work=Path(args.output_dir).resolve();work.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((HERE/'source-manifest.json').read_text())
    for path,pin in manifest['dependencies'].items():
        raw=(HERE.parent.parent.parent/path).read_bytes()
        need(hashlib.sha256(raw).hexdigest()==pin,'Published dependency changed: '+path)
    for path,pin in manifest['sources'].items():
        need(hashlib.sha256((HERE/path).read_bytes()).hexdigest()==pin,'Source changed: '+path)
    env=dict(os.environ,NATIVE20_WORKDIR=str(work),OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    plan=[('intake',[]),('phase_generate',[]),('preparations_generate',[]),('joint_generate',[]),('post_generate',[]),('phase_verify',[]),('images_verify',['joint']),('images_verify',['post']),('constants_generate',['0','135']),('constants_generate',['135','4231']),('constants_generate',['4231','23006']),('constants_verify',[]),('nested_generate',['0','20']),('nested_generate',['20','765']),('nested_verify',['0','20']),('nested_verify',['20','400']),('nested_verify',['400','765'])]
    rows=[]
    for index,(name,extra) in enumerate(plan):
        command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+['-B',str(HERE/(name+'.py'))]+extra
        start=time.monotonic()
        try:result=subprocess.run(command,text=True,capture_output=True,env=env,timeout=55)
        except subprocess.TimeoutExpired as error:
            (work/'INCOMPLETE.json').write_text(json.dumps({'stage':name,'args':extra,'not_nonexistence':True,'guard_seconds':55})+'\n')
            raise SystemExit('Operational stage guard reached; no theorem is certified by this incomplete run.')
        (work/f'stage-{index:02d}-{name}.log').write_text(result.stdout+result.stderr)
        need(result.returncode==0,'Stage failed: '+name+'; see its generated log.')
        stage={'stage':name,'args':extra,'seconds':time.monotonic()-start,'output':[]}
        for line in result.stdout.splitlines():
            try:stage['output'].append(json.loads(line))
            except json.JSONDecodeError:pass
        rows.append(stage)
        # Only summaries, not large generated arrays, are shown to the reader.
        print(json.dumps({'stage':name,'args':extra,'status':'PASS','seconds':round(stage['seconds'],3)}),flush=True)
        if index==2:
            pins={p:hashlib.sha256((work/p).read_bytes()).hexdigest() for p in ['p20-intake.json','pre6-cover.json','preparation-functions.json']}
            (work/'initial-artifacts.json').write_text(json.dumps(pins,indent=2)+'\n')
    final={'agent':'six-sorting-2','role':'researcher','status':'NATIVE20_COMPLETE_SIZE44_EXCLUSION_VERIFIED','total_lower_bound':45,'native_prefix_total_interval':[45,46],'native_prefix_suffix_interval':[25,26],'normalized22_target_suffix_interval':[23,24],'nine_core_images':23006,'semantic_exclusions':22241,'nested_exclusions':765,'remaining_roots':0,'root_image_budget_sha256':'1f4a83e1057bf83d4d56211f42c117b8ac81352fcd2028d189c1134309dc96ca','stage_results':rows,'trust_boundary':'Imported published9207/8539/8604/9007, smaller-size lower bounds and unformalized normalization/pruning/zero-one/category-collapse bridges. Same-author distinct exact algorithms; no external-review verdict.'}
    required=[('verify-phase-tf.json','NUMERIC_PHASE_AND_DNF_FUNCTION_COVER_VERIFIED'),('verify-joint.json','BULK_COLUMN_ALL_JOINT_IMAGES_AND_MINIMUM_LENGTHS_VERIFIED'),('verify-postjoint.json','BALANCED_SUBSET_TREE_AND_ALL_NINE_CORE_IMAGES_VERIFIED'),('verify-constants.json','ALL_SELECTED_CONSTANT_ROOT_CERTIFICATES_NUMERIC_IMAGE_SET_VERIFIED')]
    for filename,status in required:need(json.loads((work/filename).read_text())['status']==status,'Missing complete check: '+filename)
    posts=json.loads((work/'verify-postjoint.json').read_text())
    need(posts['distinct_nine_core_images']==23006 and posts['root_image_budget_sha256']==final['root_image_budget_sha256'],'Complete root cover differs')
    constants=json.loads((work/'verify-constants.json').read_text())
    need(constants['verified_exclusions']==22241 and constants['not_excluded_roots']==765,'Constant exclusion count differs')
    nested=[json.loads((work/f'verify-nested-{a}-{b}.json').read_text()) for a,b in [(0,20),(20,400),(400,765)]]
    need(all(x['status']=='SELECTED_NESTED_PARTITION_ALL_NUMERIC_FIELDS_AND_PRUNING_FUNCTIONS_VERIFIED' for x in nested),'Missing complete nested check')
    need([x['remaining_position_range'] for x in nested]==[[0,20],[20,400],[400,765]] and sum(x['verified_exclusions'] for x in nested)==765,'Nested exclusion coverage differs')
    (work/'checks.json').write_text(json.dumps(final,indent=2)+'\n')
    finite=clean(final)
    (work/'finite-checks.json').write_text(json.dumps(finite,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in final.items() if k!='stage_results'},sort_keys=True),flush=True)
if __name__=='__main__':main()
