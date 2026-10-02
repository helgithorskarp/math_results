"""Literal valid controls and semantic negative controls; assertions unnecessary."""
import copy,hashlib,json
from geometry import canonical,need,roots,color,inverse
from positive import validate_state,validate_pack

def checks():
    valid=[[6+42*j,6]for j in range(9)]
    good=[]
    for state in ((1,0,0),(2,1,0),(3,2,0)):
        transcript=validate_pack(state,valid)
        good.append({'state':state,'APs':valid,'whole_positive_transcript_sha256':hashlib.sha256(canonical(transcript)).hexdigest()})
    rejected=[]
    def bad(name,fn):
        try:fn()
        except (ValueError,TypeError,IndexError):rejected.append(name);return
        raise ValueError('damage accepted: '+name)
    for name,s in [('root-count', [0,0,0]),('coincident-label',[3,1,0]),('truth-gauge',[3,2,1]),('truth-range',[1,0,4]),('typed-boolean',[True,0,0]),('truncated-state',[1,0])]:
        bad(name,lambda s=s:validate_state(s))
    for name,mutate in [
        ('missing-AP',lambda a:a.pop()),
        ('noninteger',lambda a:a[0].__setitem__(0,True)),
        ('start-range',lambda a:a[0].__setitem__(0,618)),
        ('zero-step',lambda a:a[0].__setitem__(1,0)),
        ('singleton-step',lambda a:a[0].__setitem__(1,103)),
        ('original-root',lambda a:a[0].__setitem__(0,0)),
        ('overlap',lambda a:a.__setitem__(1,a[0][:])),
        ('nonmonochromatic-phase',lambda a:a[0].__setitem__(1,1)),
    ]:
        a=copy.deepcopy(valid);mutate(a);bad(name,lambda a=a:validate_pack((3,2,0),a))
    need(len(rejected)==14,'whole damage coverage')
    # The truth function ignores both extra roots; those roots still invalidate an AP.
    rootdam=copy.deepcopy(valid);rootdam[0][0]=1
    bad('ignored-original-root',lambda:validate_pack((3,2,0),rootdam))
    # A nonconstant Boolean rule cannot borrow an unchecked constant-rule pack.
    bad('whole-Boolean-rule',lambda:validate_pack((3,2,2),valid))
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','positive_controls':good,
            'semantic_rejections':rejected,'rejection_count':len(rejected),'assertions_required':False}
if __name__=='__main__':
    raw=canonical(checks());print(raw.decode(),end='')
