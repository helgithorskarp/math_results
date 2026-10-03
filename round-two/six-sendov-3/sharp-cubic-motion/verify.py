"""Strict whole-record and sealed-source checker; no analytic formalization."""
from pathlib import Path
import argparse, json, resource, sys, time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from jets import build, compare_baseline, canonical, sha256, need
from arithmetic import CertificateError

RECORD_SHA='502f5360199c1d393450e77293b36dc47a9af1895541f5c8308452befeee28e6'
DAMAGES=('wrong_cosine_embedding','wrong_anchor','wrong_sine_closure',
         'missing_ninth_root','wrong_cubic_harmonic','wrong_norm_conjugation',
         'cube_is_maximum','missing_skewness_case','wrong_sharp_constant','wrong_repair_infimum')
HERE=Path(__file__).resolve().parent


def unique_object(pairs):
    out={}
    for key,value in pairs:
        need(key not in out,'duplicate JSON object key')
        out[key]=value
    return out


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique_object,
                      parse_constant=lambda x:(_ for _ in ()).throw(CertificateError('nonfinite JSON')))


def same(actual, expected, path='record'):
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
        digest,name=line.split('  ',1)
        need(name not in names and Path(name).name==name,'unique local source name')
        names[name]=digest
    actual={p.name for p in HERE.iterdir() if p.is_file()}-{'SHA256SUMS','VALIDATION.json'}
    need(set(names)==actual,'whole fixed-source census')
    for name,digest in names.items():
        need(sha256((HERE/name).read_bytes()).hexdigest()==digest,'whole sealed source '+name)
    need(names['arithmetic.py']=='5527bcc330398f6618f10e1705e9ed56133e61e94de9155faa148e84e09539e2',
         'unchanged same-author kernel pin')
    return sha256(raw).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixture',type=Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--validation-batch',action='store_true')
    parser.add_argument('--baseline',type=Path)
    args=parser.parse_args();start=time.monotonic()
    seal=source_guard();record=build()
    need(sha256(canonical(record)).hexdigest()==RECORD_SHA,'entire reconstructed record hash')
    same(parse(args.fixture.read_text()),record)
    rejected=[]
    if args.validation_batch:
        for damage in DAMAGES:
            try:build(damage)
            except CertificateError as exc:rejected.append({'damage':damage,'rejected':True,'reason':str(exc)})
            else:raise CertificateError('mathematical damage accepted: '+damage)
        need(len(rejected)==len(DAMAGES),'every mathematical damage rejected')
    baseline=compare_baseline(args.baseline,record) if args.baseline else None
    print(json.dumps({'status':'PASS','whole_record_sha256':RECORD_SHA,
                      'manifest_sha256':seal,'all_nine_labels':len(record['all_nine_harmonics']),
                      'all_seven_skewness_cases':len(record['all_seven_skewness_cases']),
                      'mathematical_damages':rejected,'prior_baseline':baseline,
                      'seconds':time.monotonic()-start,
                      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'unformalized_analytic_bridges':True,'independent_review':False},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (CertificateError,ValueError,OSError) as exc:
        print('REJECTED: '+str(exc),file=sys.stderr);sys.exit(1)
