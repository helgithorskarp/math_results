"""Changed role guards, retained aliases, and a full incidence QQ obstruction."""
from pathlib import Path
import json
from patch import *
from check import evaluate,need,closed_obstruction
from audit import DartAudit,Reject,evaluate as audit_evaluate,bit,closed_obstruction as audit_obstruction

def build_report():
    fixtures=[
        ('ordinary triangle',[(I,R,S)],[],True),
        ('triangle extracted from three bars',[],[(I,R),(I,S),(R,S)],True),
        ('two-T ordinary path',[(I,R,S),(I,S,C)],[],True),
        ('D both three suppliers retained',[(D,U,A,V)],[],True),
        ('D isolated Q allowed with one three',[(D,I,A,R)],[(D,U)],True),
        ('other five opposite Q retained',[(F,I,D,R)],[],True),
        ('D isolated Q excluded with both threes',[(D,I,A,R)],[(D,U),(D,V)],False),
        ('F isolated Q excluded with one three',[(F,I,A,R)],[(F,U)],False),
        ('F cannot supply both threes',[],[(F,U),(F,V)],False),
        ('F QQ to ordinary excluded',[(F,I,A,R),(F,S,B,I)],[],False),
        ('D QQ to ordinary excluded',[(D,I,A,R),(D,S,B,I)],[],False),
        ('ordinary opposite five',[(F,I,R,S)],[],False),
        ('Q diagonal contact',[(I,R,12,S)],[(I,12)],False),
        ('ordinary contacts three',[],[(I,U)],False),
        ('proper closed link',[(D,I,R),(D,R,S),(D,S,A,I)],[],False),
        ('one-T three QQ edges',[(A,I,B,U),(A,I,C,R)],[(A,V)],False),
        ('nonsimple face',[(I,R,R)],[],False),
        ('degree overflow',[],[(F,x)for x in (A,B,C,I,R,S)],False),
    ]
    checked=[]
    for name,fs,ex,expected in fixtures:
        a=evaluate(Patch(fs,ex))is not None;b=audit_evaluate(DartAudit(fs,ex))is not None
        need(a==b==expected,('fixture',name,a,b));checked.append([name,a,b])
    fs=[(I,R,S),(I,S,C),(A,I,C,U),(A,U,B,V)];released=[]
    for flag in (False,True):
        outcomes=[]
        for cls,error,method in ((Patch,Bad,'evaluate'),(DartAudit,Reject,'inspect')):
            try:getattr(cls(fs,missing_capacity=flag),method)(False);good=True
            except error:good=False
            outcomes.append(good)
        need(outcomes==[not flag,not flag],'missing T-capacity release');released.append([flag,outcomes])
    # A literal closed incidence map from the unpruned cover. This is NOT a
    # sphere packing: edge7--14 violates the proved ordinary-ordinary QQ bound.
    fs=[(0,7,8),(0,7,9),(0,8,6,11),(0,9,5,10),(0,10,11),
        (1,2,4,3),(1,2,5,12),(1,3,6,13),(1,12,14),(1,13,14),
        (2,4,10,5),(3,4,11,6),(4,10,11),(5,9,12),(6,8,13),
        (7,8,13,14),(7,9,12,14)]
    p=evaluate(Patch(fs));q=audit_evaluate(DartAudit(fs));need(p is not None and q is not None,'closed incidence retained')
    a=closed_obstruction(p);b=audit_obstruction(q);need(a==b and a[0]==[7,14],'closed QQ witness')
    damaged=[]
    for label,remove in [('delete Q',15),('delete T',8)]:
        outcomes=[]
        for st,method in ((p,closed_obstruction),(q,audit_obstruction)):
            bad=dict(st);bad['faces']=st['faces']-{face(fs[remove])}
            try:method(bad);fails=False
            except RuntimeError:fails=True
            outcomes.append(fails)
        need(outcomes==[True,True],('damaged closed map',label));damaged.append([label,outcomes])
    guarded=0
    for v in range(15):
        try:bit(v,v)
        except ValueError:guarded+=1
    need(guarded==15,'distinct-pair mask guard')
    return {'partial_fixtures':checked,'missing_capacity_release':released,
            'closed_incidence_passes_necessary_predicates':[True,True],
            'closed_map_metric_obstruction':{'ordinary_QQ_edge':a[0],'full_faces_sha256':a[1]},
            'damaged_closed_profiles_rejected':damaged,'same_vertex_mask_guards':guarded}
def main():
    x=build_report();e=json.loads(Path(__file__).with_name('CONTROLS_EXPECTED.json').read_text())
    need(x==e,'complete control output mismatch');print(json.dumps(x,sort_keys=True,indent=2))
if __name__=='__main__':main()
