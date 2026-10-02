"""Positive completion and malformed-domain controls, including optimized execution."""
import copy,json,hashlib,argparse
from pathlib import Path
from geometry import canonical,need
from positive import verify
from merge import merge

def checks(certificate,parts):
    pristine=merge(parts);rejected=[]
    def bad(name,fn):
        try:fn()
        except (ValueError,TypeError,IndexError,KeyError):rejected.append(name);return
        raise ValueError('damaged completion accepted: '+name)
    for name,change in[
        ('missing-case',lambda c:c.pop()),('duplicate-case',lambda c:c.__setitem__(1,c[0])),
        ('extra-schema',lambda c:c[0].__setitem__('unused',1)),('wrong-short-representative',lambda c:c[-1]['state'].__setitem__(1,57)),
        ('root-sentinel',lambda c:c[2]['state'].__setitem__(1,0)),
        ('odd-truth',lambda c:c[0]['state'].__setitem__(2,1)),('last-case-missing-pair',lambda c:c[-1]['aps'].pop())]:
        c=copy.deepcopy(certificate);change(c);bad(name,lambda c=c:verify(c,2175,2176))
    for name,change in[
        ('missing-batch',lambda p:p.pop()),('duplicate-batch',lambda p:p.__setitem__(1,p[0])),
        ('range-gap',lambda p:p[0].__setitem__('case_end',255)),('missing-case-digest',lambda p:p[0]['case_transcript_digests'].pop()),
        ('duplicate-case-digest',lambda p:p[0]['case_transcript_digests'].__setitem__(1,p[0]['case_transcript_digests'][0])),
        ('wrong-orbit-size',lambda p:p[0]['case_transcript_digests'][0].__setitem__(2,6)),
        ('different-certificate',lambda p:p[1].__setitem__('whole_certificate_sha256','0'*64)),
        ('different-domain',lambda p:p[1].__setitem__('whole_representatives_sha256','0'*64)),
        ('wrong-AP-total',lambda p:p[0].__setitem__('all_transported_APs',0)),
        ('invalid-digest',lambda p:p[0]['case_transcript_digests'][0].__setitem__(3,'X'*64)),
        ('incomplete-status',lambda p:p[0].__setitem__('nine_disjoint_regular_columns_verified',False))]:
        damaged=copy.deepcopy(parts);change(damaged);bad(name,lambda damaged=damaged:merge(damaged))
    need(len(rejected)==18,'complete coverage/domain damage inventory')
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','whole_valid_merge_sha256':hashlib.sha256(canonical(pristine)).hexdigest(),'malformed_domain_and_coverage_rejections':rejected,'count':len(rejected),'no_assertions_required':True}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();c=json.loads((a.work/'neutral.json').read_text());parts=[json.loads((a.work/('normal-'+str(k)+'.json')).read_text())for k in range(0,2176,256)];a.out.write_bytes(canonical(checks(c,parts)))
