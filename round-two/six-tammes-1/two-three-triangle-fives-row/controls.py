"""Positive partial incidences, damaged inputs, and a released local rule."""
from pathlib import Path
import json
from patch import *
from check import evaluate,need
from audit import DartAudit,Reject,inspect,bit

def build_report():
    fixtures=[
        ('ordinary triangle',[(I,R,S)],[],True),
        ('contact triangle extracted',[],[(I,R),(I,S),(R,S)],True),
        ('two-T ordinary path',[(I,R,S),(I,S,C)],[],True),
        ('other five opposite Q retained',[(F,I,D,R)],[],True),
        ('nonsimple face',[(I,R,R)],[],False),
        ('ordinary opposite five',[(F,I,R,S)],[],False),
        ('Q diagonal contact',[(I,R,12,S)],[(I,12)],False),
        ('ordinary contacts three',[],[(I,U)],False),
        ('five Q misses its three',[(F,I,A,R)],[(F,U)],False),
        ('proper closed link',[(D,I,R),(D,R,S),(D,S,A),(D,A,E,I)],[],False),
        ('one-T three QQ edges',[(A,I,E,U),(A,I,C,R)],[(A,V)],False),
        ('more than five contacts',[],[(F,x)for x in (A,B,C,E,I,R)],False),
    ]
    outcomes=[]
    for name,fs,ex,expected in fixtures:
        a=evaluate(Patch(fs,ex))is not None;b=inspect(DartAudit(fs,ex))is not None
        need(a==b==expected,('control',name,a,b))
        outcomes.append([name,a,b])
    fs=[(I,R,S),(I,S,C),(A,I,C,U),(A,U,E,V)]
    release=[]
    for enabled in (False,True):
        result=[]
        for cls,error,method in ((Patch,Bad,'evaluate'),(DartAudit,Reject,'inspect')):
            try:getattr(cls(fs,missing_capacity=enabled),method)(False);good=True
            except error:good=False
            result.append(good)
        need(result==[not enabled,not enabled],'missing T capacity release')
        release.append([enabled,result])
    # A full F,D fan plus both three stars, admitted as partial incidence data.
    # It has an ordinary opposite shared by two three Qs, so aliases matter.
    fs=[(F,D,I),(F,D,R),(F,R,S),(D,I,P),
        (F,U,A,S),(F,U,B,I),(D,V,C,R),(D,V,E,P),
        (U,A,12,B),(V,C,12,E)]
    ex=[(U,x)for x in (F,A,B)]+[(V,x)for x in (D,C,E)]
    p,q=Patch(fs,ex,fd_contact=True),DartAudit(fs,ex,fd_contact=True)
    need(evaluate(p)is not None and inspect(q)is not None,'shared-original partial prefix')
    # Test all 225 assignments across a fixed open edge, including nonsimple
    # words and the already known face. This is separate from edge selection.
    choices=[]
    for w in range(15):
        for x in range(15):
            cell=(A,12,w)if w==x else(A,12,x,w)
            left=evaluate(p.plus(cell))is not None;right=inspect(q.plus(cell))is not None
            need(left==right,('all-original second-face control',w,x))
            choices.append([w,x,left])
    admitted=[[w,x]for w,x,good in choices if good]
    need(admitted==[[2,5]],'only the already known face can be re-added')
    need(face((A,12,5,2))in p.faces,'admitted pair repeats the known Q')
    try:bit(I,I)
    except ValueError:self_pair_rejected=True
    else:self_pair_rejected=False
    need(self_pair_rejected,'self-pair mask must not encode an edge')
    return {'partial_incidence_controls':outcomes,
            'missing_star_T_capacity_release':release,
            'shared_original_partial_prefix':True,
            'all_original_second_face_pairs':len(choices),
            'second_face_admitted_pairs':admitted,
            'only_admitted_assignment_repeats_known_face':True,
            'audit_self_pair_mask_rejected':True,
            'second_face_decision_sha256':__import__('hashlib').sha256(
                json.dumps(choices,separators=(',',':')).encode()).hexdigest()}

def main():
    report=build_report()
    expected=json.loads(Path(__file__).with_name('CONTROLS_EXPECTED.json').read_text())
    need(report==expected,'complete controls mismatch')
    print(json.dumps(report,sort_keys=True,indent=2))

if __name__=='__main__':main()
