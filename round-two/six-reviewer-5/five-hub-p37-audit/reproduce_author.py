"""Optional pinned native replay; all generated data in a new separate work dir."""
import argparse,pathlib,sys,subprocess,json,urllib.request,hashlib,os,shutil
P=pathlib.Path(__file__).resolve().parent
def need(ok,msg):
    if not ok:raise ValueError(msg)
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'six-reviewer-5 pinned native corroboration'}),timeout=20) as r:return r.read()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',required=True,type=pathlib.Path);args=ap.parse_args();w=args.work.resolve()
    need(not w.exists(),'choose a NEW separate native work directory')
    need(not w.is_relative_to(P),'generated native data must be outside contribution source')
    w.mkdir(parents=True);(w/'core').mkdir();(w/'author').mkdir();(w/'five_hub_pair_total36').mkdir()
    for f in ('audit.py','census.py','prior_rows.py','prior_bit_rows.py','fixtures.json'):shutil.copyfile(P/f,w/'core'/f)
    shutil.copyfile(P/'compare_author.py',w/'compare_author.py')
    manifest=json.loads((P/'AUTHOR_SOURCE.json').read_text())
    for f,row in manifest['files'].items():
        b=fetch('https://raw.githubusercontent.com/helgithorskarp/math_results/'+manifest['commit']+'/'+manifest['path']+'/'+f)
        need(hashlib.sha256(b).hexdigest()==row['sha256'],'pinned native byte hash:'+f);(w/'author'/f).write_bytes(b)
    deps=json.loads((w/'author/DEPENDENCIES.json').read_text())
    for f,sha in deps['frozen_source_sha256'].items():
        b=fetch('https://raw.githubusercontent.com/helgithorskarp/math_results/'+deps['frozen_source_commit']+'/round-two/six-code-1/five_hub_pair_total36/'+f)
        need(hashlib.sha256(b).hexdigest()==sha,'pinned prerequisite:'+f);(w/'five_hub_pair_total36'/f).write_bytes(b)
    env=dict(os.environ)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
    records=[]
    for program,optimized in [('core/audit.py',False),('author/verify.py',False),('author/verify.py',True),('compare_author.py',False),('compare_author.py',True)]:
        result=subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(w/program)],cwd=w,env=env,capture_output=True,timeout=45)
        need(result.returncode==0,'INCOMPLETE/failed native stage '+program+':'+result.stderr.decode())
        records.append(dict(program=program,optimized=optimized,output=result.stdout.decode()))
    need(json.loads((w/'CORROBORATION.json').read_text())==json.loads((P/'CORROBORATION.json').read_text()),'entire published late corroboration')
    (w/'native-replay.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(dict(agent='six-reviewer-5',role='independent mathematical reviewer',pinned_files=13,serial_stages=5,
      native_whole_sha256=json.loads((w/'CORROBORATION.json').read_text())['native_whole_sha256'],
      every_5236_vector_and_native_certificate_agrees=True,work=str(w)),indent=2))
if __name__=='__main__':main()
