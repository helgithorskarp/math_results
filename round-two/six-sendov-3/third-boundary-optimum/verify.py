"""Strict entire-record/source checker; ordinary analytic proof unformalized."""
from pathlib import Path
import argparse,json,resource,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from jets import build,compare_baselines,canonical,sha256,need
from arithmetic import CertificateError

RECORD_SHA='9b36c2b079c995601d1d81fb68f0e77d835127a5c3dbb59ec1b4ca4b5737633a'
DAMAGES=('wrong_embedding','wrong_sixth_moment_sign','wrong_anchor','wrong_scalar_third','wrong_normalization_offset','wrong_dual_weight','wrong_skew_coefficient','wrong_repair','missing_ninth_root')
HERE=Path(__file__).resolve().parent


def unique_object(pairs):
    out={}
    for key,v in pairs:
        need(key not in out,'duplicate JSON object key');out[key]=v
    return out


def parse(raw):
    return json.loads(raw,object_pairs_hook=unique_object,
        parse_constant=lambda x:(_ for _ in ()).throw(CertificateError('nonfinite JSON')))


def same(actual,expected,path='record'):
    need(type(actual) is type(expected),'typed mismatch '+path)
    if isinstance(actual,dict):
        need(set(actual)==set(expected),'whole key set '+path)
        for k in expected:same(actual[k],expected[k],path+'.'+k)
    elif isinstance(actual,list):
        need(len(actual)==len(expected),'whole list length '+path)
        for j,(a,e) in enumerate(zip(actual,expected)):same(a,e,path+'['+str(j)+']')
    else:need(actual==expected,'whole value '+path)


def source_guard():
    raw=(HERE/'SHA256SUMS').read_bytes();names={}
    for line in raw.decode('ascii').splitlines():
        h,n=line.split('  ',1)
        need(n not in names and Path(n).name==n,'unique local source name');names[n]=h
    actual={p.name for p in HERE.iterdir() if p.is_file()}-{'SHA256SUMS','VALIDATION.json'}
    need(set(names)==actual,'whole fixed-source census')
    for n,h in names.items():need(sha256((HERE/n).read_bytes()).hexdigest()==h,'whole sealed source '+n)
    need(names['arithmetic.py']=='5527bcc330398f6618f10e1705e9ed56133e61e94de9155faa148e84e09539e2',
         'unchanged same-author kernel pin')
    return sha256(raw).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--validation-batch',action='store_true');parser.add_argument('--baseline-root',type=Path)
    args=parser.parse_args();t=time.monotonic();seal=source_guard();record=build()
    need(sha256(canonical(record)).hexdigest()==RECORD_SHA,'entire reconstructed record hash')
    same(parse(args.fixture.read_text()),record);rejected=[]
    if args.validation_batch:
        for damage in DAMAGES:
            try:build(damage)
            except CertificateError as exc:rejected.append({'damage':damage,'rejected':True,'reason':str(exc)})
            else:raise CertificateError('mathematical damage accepted: '+damage)
        need(len(rejected)==len(DAMAGES),'all mathematical damages rejected')
    baseline=compare_baselines(args.baseline_root,record) if args.baseline_root else None
    print(json.dumps({'status':'PASS','whole_record_sha256':RECORD_SHA,'manifest_sha256':seal,
        'field_identity_count':len(record['field_polynomial_identities']),'rational_identity_count':len(record['rational_polynomial_identities']),'all_nine_roots':len(record['all_nine_roots']),'sign_count':len(record['rational_sign_bounds']),
        'mathematical_damages':rejected,'prior_baselines':baseline,'seconds':time.monotonic()-t,
        'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'ordinary_analytic_bridges_unformalized':True,'independent_review':False},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (CertificateError,ValueError,OSError) as exc:
        print('REJECTED: '+str(exc),file=sys.stderr);sys.exit(1)
