"""Semantic certificate damages; operational interruptions are never rejections."""
import copy,json,time,signal,resource
from pathlib import Path
from check_harmonic import check
from pack_certificate import unpack
from exact import require
from completion_harmonic import alarm


def main():
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    folder=Path.cwd()
    raw=json.loads((Path(__file__).resolve().parent/'CERTIFICATE.json').read_text())
    baseline=check(unpack(raw));require(baseline['complete'],'actual complete positive baseline')
    cases=[]
    def variant(name,change):
        data=copy.deepcopy(raw);change(data);cases.append((name,data))
    variant('missing_last_pivot',lambda x:x['rows'].pop())
    variant('wrong_uniform_domain',lambda x:x.__setitem__('domain','q=8,h=3 only'))
    variant('wrong_original_light_mean',lambda x:x['forms']['aggregate'][4].__setitem__(4,x['forms']['x-nu'][0][0]))
    variant('missing_original_mean_coordinate',lambda x:x['forms']['aggregate'].pop())
    variant('missing_last_Schur_identity',lambda x:x['updates'].pop())
    variant('extra_unreferenced_polynomial',lambda x:x['polynomials'].append(copy.deepcopy(x['polynomials'][0])))
    def reverse_shift(x):
        p=x['polynomials'][x['rows'][0]['shifted_numerator']]
        p['terms'][0][1]=str(-int(p['terms'][0][1]))
    variant('reverse_shifted_sign',reverse_shift)
    variant('wrong_original_update_link',lambda x:x['updates'][0].__setitem__('before',x['forms']['tau'][0][0]))
    records=[]
    for name,data in cases:
        try:check(unpack(data))
        except ValueError as e:records.append(dict(case=name,exactly_rejected=True,reason=str(e)))
        else:raise ValueError('damaged certificate accepted: '+name)
    result=dict(agent='six-downset-1',role='researcher',complete=True,
                semantic_rejections=records,operational_failure_not_rejection=True)
    (folder/'DAMAGES.json').write_text(json.dumps(result,indent=2)+'\n')
    signal.alarm(0)
    print(json.dumps(result|dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        optimized=not __debug__)),flush=True)


if __name__=='__main__':main()
