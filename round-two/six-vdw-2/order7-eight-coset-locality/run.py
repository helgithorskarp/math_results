"""Fresh generation, two exact audits, and compact expected-result checks."""
from pathlib import Path
import argparse,hashlib,json,os,resource,subprocess,sys,time

HERE=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    args=ap.parse_args();work=args.work.absolute()
    require(not work.exists(),'use a fresh directory outside public source')
    require(HERE not in (work,*work.parents),'generated output must be outside source directory')
    for row in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=row.split('  ')
        require(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,'changed own source: '+name)
    work.mkdir(parents=True);start=time.monotonic()
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
             MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    def run(command):
        r=subprocess.run([str(v) for v in command],capture_output=True,text=True,
                         check=True,timeout=55,env=env)
        return json.loads(r.stdout)
    certificate=work/'certificate.json'
    generation=run([sys.executable,HERE/'encode.py','--output',certificate])
    checks=[]
    expected=json.loads((HERE/'expected.json').read_text())
    for flags in ([],['-O']):
        result=run([sys.executable,*flags,HERE/'audit.py',certificate])
        semantic={k:v for k,v in result.items() if k not in ('seconds','maxrss_kib')}
        require(semantic==expected,'literal audit differs from compact expected results')
        checks.append(result)
    receipt={'agent':'six-vdw-2','role':'researcher',
             'status':'FRESH_EIGHT_COSET_LOCALITY_REPLAY_VERIFIED',
             'generation':generation,'normal_audit':checks[0],'optimized_audit':checks[1],
             'seconds':time.monotonic()-start,'python':sys.version.split()[0],
             'maxrss_parent_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'maxrss_child_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (work/'result.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in
                      ('generation','normal_audit','optimized_audit')}),flush=True)

if __name__=='__main__':main()
