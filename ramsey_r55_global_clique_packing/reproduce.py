"""Fresh exact family census, independent physical checks and six full CNFs."""
from pathlib import Path
import argparse,hashlib,json,resource,sys,tempfile,time
import domains,census,check_domains,audit
HERE=Path(__file__).resolve().parent

def compare(actual,name):
 if json.loads(json.dumps(actual))!=json.loads((HERE/name).read_text()):raise ValueError('certificate mismatch: '+name)

def reproduce(work):
 started=time.monotonic();print('Regenerating all matrix domains and branch counts',file=sys.stderr,flush=True)
 catalog=domains.certificate();compare(catalog,'DOMAINS.json');counts=census.count(catalog);compare(counts,'COUNTS.json')
 root_catalog=domains.root_certificate();compare(root_catalog,'ROOT_DOMAINS.json')
 checked=check_domains.verify(catalog,root_catalog,counts);compare(checked,'EXPECTED_DOMAIN_AUDIT.json')
 print('Checking all branch dimensions, index boundaries and graph transports',file=sys.stderr,flush=True)
 controls={'stencils':audit.stencil_counts(counts),'interfaces':audit.controls(counts)}
 result={'status':'VERIFIED_UNCONDITIONAL_GLOBAL_PACKING_HANDOFF','controls':controls,'cnfs':[]}
 for branch in audit.FULL_BRANCHES:
  print('Checking every full43 clause: '+str(branch),file=sys.stderr,flush=True)
  path=work/('branch-'+'-'.join(map(str,branch))+'.cnf');result['cnfs'].append(audit.full_cnf(branch,path));path.unlink()
 compare(result,'EXPECTED_AUDIT.json')
 encoded=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
 return {'status':result['status'],'audit_sha256':hashlib.sha256(encoded).hexdigest(),'domain_sha256':hashlib.sha256((json.dumps(catalog,indent=2)+'\n').encode()).hexdigest(),
         'root_domain_sha256':hashlib.sha256((json.dumps(root_catalog,indent=2)+'\n').encode()).hexdigest(),'seconds':time.monotonic()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'python_optimization':sys.flags.optimize,
         'physical_matrix_cases':checked['physical_matrix_cases'],'complete_branches':60,'target_solver_calls':0}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--work-root');p.add_argument('--output');a=p.parse_args()
 with tempfile.TemporaryDirectory(prefix='r55-global-packing-',dir=a.work_root) as directory:result=reproduce(Path(directory))
 text=json.dumps(result,indent=2,sort_keys=True)+'\n'
 if a.output:Path(a.output).write_text(text)
 print(text,end='')
