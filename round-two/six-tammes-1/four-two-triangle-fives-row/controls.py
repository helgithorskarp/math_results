"""Positive partial incidences, changed geometric guards and damaged inputs."""
from pathlib import Path
import json,hashlib
from patch import *
from check import evaluate,need
from audit import DartAudit,Reject,evaluate as audit_evaluate,bit

def build_report():
    fixtures=[
        ('ordinary triangle',[(I,R,S)],[],True),
        ('triangle extracted from three bars',[],[(I,R),(I,S),(R,S)],True),
        ('two-T ordinary path',[(I,R,S),(I,S,C)],[],True),
        ('D both three suppliers retained',[(D,U,A,V)],[],True),
        ('D isolated Q allowed with one three',[(D,I,A,R)],[(D,U)],True),
        ('other five opposite Q now excluded',[(F,I,D,R)],[],False),
        ('D isolated Q excluded with two threes',[(D,I,A,R)],[(D,U),(D,V)],False),
        ('nonsimple face',[(I,R,R)],[],False),
        ('ordinary opposite five',[(F,I,R,S)],[],False),
        ('Q diagonal contact',[(I,R,12,S)],[(I,12)],False),
        ('ordinary contacts three',[],[(I,U)],False),
        ('F cannot supply a three',[(F,I,A,R)],[(F,U)],False),
        ('proper closed link',[(D,I,R),(D,R,S),(D,S,A),(D,A,E,I)],[],False),
        ('one-T three QQ edges',[(A,I,E,U),(A,I,C,R)],[(A,V)],False),
        ('degree overflow',[],[(F,x)for x in (A,B,C,E,I,R)],False),
    ]
    checked=[]
    for name,fs,ex,expected in fixtures:
        a=evaluate(Patch(fs,ex))is not None;b=audit_evaluate(DartAudit(fs,ex))is not None
        need(a==b==expected,('fixture',name,a,b));checked.append([name,a,b])
    fs=[(I,R,S),(I,S,C),(A,I,C,U),(A,U,E,V)];released=[]
    for flag in (False,True):
        outcomes=[]
        for cls,error,method in ((Patch,Bad,'evaluate'),(DartAudit,Reject,'inspect')):
            try:getattr(cls(fs,missing_capacity=flag),method)(False);good=True
            except error:good=False
            outcomes.append(good)
        need(outcomes==[not flag,not flag],'missing T-capacity release');released.append([flag,outcomes])
    # Literal admitted contact-fan prefix, with both five stars complete.
    fs=[(F,S,D),(F,D,I),(F,I,R),(F,R,P),
        (F,S,E,P),(D,I,B,U),(D,U,A,V),(D,V,C,S)]
    ex=[(U,x)for x in (A,B,D)]+[(V,x)for x in (A,C,D)]
    p,q=Patch(fs,ex,fd_contact=True),DartAudit(fs,ex,fd_contact=True)
    # This concrete fixture is required to pass; it is not a sphere packing.
    positive=[evaluate(p)is not None,audit_evaluate(q)is not None]
    need(positive==[True,True],'contact-fan positive control')
    # A noncontacting full-three-star prefix needs exactly one ordinary
    # internal original to supply D's two Ts. All seven reject.
    fs=[(F,E,B,P),(F,E,I),(F,I,R),(F,R,S),(F,S,P),
        (D,U,A,V),(D,U,B,P),(D,V,C,13),(U,A,12,B),(V,A,14,C)]
    p,q=Patch(fs,ex),DartAudit(fs,ex)
    need(evaluate(p)is not None and audit_evaluate(q)is not None,'noncontact D parent')
    internals=[]
    for i in sorted(ORD):
        left=evaluate(p.plus((D,P,i),(D,i,13)))is not None
        right=audit_evaluate(q.plus((D,P,i),(D,i,13)))is not None
        need(left==right==False,('D ordinary internal',i))
        internals.append([i,left,right])
    try:bit(I,I)
    except ValueError:mask_guard=True
    else:mask_guard=False
    need(mask_guard,'mask self-pair guard')
    return {'partial_incidence_controls':checked,
            'missing_star_T_capacity_release':released,
            'contact_fan_positive_prefix':positive,'noncontact_D_positive_parent':True,
            'D_all_original_internal_controls':internals,'audit_self_pair_mask_rejected':mask_guard}

def main():
    report=build_report();expected=json.loads(Path(__file__).with_name('CONTROLS_EXPECTED.json').read_text())
    need(report==expected,'complete controls mismatch');print(json.dumps(report,sort_keys=True,indent=2))
if __name__=='__main__':main()
