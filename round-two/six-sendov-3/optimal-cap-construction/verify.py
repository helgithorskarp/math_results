"""Strict same-author whole-source/whole-record checker; stdlib only."""
from pathlib import Path
import argparse,json,resource,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from cap import build,compare_baselines,canonical,sha256,need
from arithmetic import CertificateError

RECORD_SHA='d6925c6515ee6ad211c51a2fa9ad68124b3dee5a41b3aca3ea48dda49a647769'
DAMAGES=('wrong_embedding','wrong_anchor','missing_ninth_root','wrong_even_repair',
         'wrong_odd_repair','wrong_inward_shift','wrong_pair_distance_sign',
         'wrong_fourth_binomial','wrong_skew_scaling')
HERE=Path(__file__).resolve().parent

def unique_object(pairs):
 out={}
 for key,value in pairs:
  need(key not in out,'duplicate JSON object key');out[key]=value
 return out
def parse(raw):
 return json.loads(raw,object_pairs_hook=unique_object,
   parse_constant=lambda x:(_ for _ in ()).throw(CertificateError('nonfinite JSON')))
def same(actual,expected,path='record'):
 need(type(actual) is type(expected),'typed mismatch '+path)
 if isinstance(actual,dict):
  need(set(actual)==set(expected),'whole key set '+path)
  for key in expected:same(actual[key],expected[key],path+'.'+key)
 elif isinstance(actual,list):
  need(len(actual)==len(expected),'whole list length '+path)
  for i,(a,e) in enumerate(zip(actual,expected)):same(a,e,path+'['+str(i)+']')
 else:need(actual==expected,'whole value '+path)
def source_guard():
 raw=(HERE/'SHA256SUMS').read_bytes();names={}
 for line in raw.decode('ascii').splitlines():
  digest,name=line.split('  ',1)
  need(name not in names and Path(name).name==name,'unique local source name')
  names[name]=digest
 actual={p.name for p in HERE.iterdir() if p.is_file()}-{'SHA256SUMS','VALIDATION.json'}
 need(set(names)==actual,'whole fixed-source census')
 for name,digest in names.items():need(sha256((HERE/name).read_bytes()).hexdigest()==digest,'whole sealed source '+name)
 need(names['arithmetic.py']=='5527bcc330398f6618f10e1705e9ed56133e61e94de9155faa148e84e09539e2',
      'unchanged same-author arithmetic kernel pin')
 return sha256(raw).hexdigest()
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--fixture',type=Path,default=HERE/'EXPECTED.json')
 parser.add_argument('--baseline-root',type=Path)
 parser.add_argument('--damage',choices=DAMAGES)
 args=parser.parse_args();start=time.monotonic();seal=source_guard()
 # Reject malformed external records cheaply by whole typed comparison
 # with the sealed expected record, before doing the substantial replay.
 expected=parse((HERE/'EXPECTED.json').read_text())
 same(parse(args.fixture.read_text()),expected)
 record=build(args.damage)
 same(record,expected)
 need(sha256(canonical(record)).hexdigest()==RECORD_SHA,'ENTIRE reconstructed record hash')
 baseline=compare_baselines(args.baseline_root,record) if args.baseline_root else None
 print(json.dumps({'status':'PASS','whole_record_sha256':RECORD_SHA,'manifest_sha256':seal,
  'field_identities':len(record['field_polynomial_identities']),
  'generic_identities':len(record['rational_polynomial_identities']),
  'signs':len(record['rational_sign_bounds']),'original_root_count':9,'critical_count':8,
  'original_epsilon_order':9,'prior_baselines':baseline,'seconds':time.monotonic()-start,
  'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  'ordinary_analytic_bridges_unformalized':True,'independent_review':False},sort_keys=True))
if __name__=='__main__':
 try:main()
 except (CertificateError,ValueError,OSError) as exc:
  print('REJECTED: '+str(exc),file=sys.stderr);sys.exit(1)
