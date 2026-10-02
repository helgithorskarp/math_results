"""Meaningful corruption controls; failures are exceptions under python -O."""
from pathlib import Path
import copy,json
from fractions import Fraction as F
import bootstrap
from exact import schur_psd
from literal import require,domain
from duals import all_checks,check
from finite import build,audit,phase
from boundary_parameters import parameters,NORMS
from entries import certificate


def checks():
    out=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError):out.append(name)
        else:raise ValueError('corruption accepted: '+name)
    fixtures=json.loads(Path(__file__).resolve().with_name('DUALS.json').read_text())
    bad=copy.deepcopy(fixtures);del bad['7']
    reject('omitted q7 upper dual',lambda:all_checks(bad))
    bad=copy.deepcopy(fixtures['5']);bad['weight']='-3'
    reject('negative rank-two PSD weight',lambda:check(5,bad))
    bad=copy.deepcopy(fixtures['6']);bad['vectors'][0].pop()
    reject('truncated original vector',lambda:check(6,bad))
    bad=copy.deepcopy(fixtures['5']);bad['vectors'][0][1]+=1
    reject('changed original b coefficient',lambda:check(5,bad))
    bad=copy.deepcopy(fixtures['7']);bad['weight']='1'
    reject('lost exact repair cancellation',lambda:check(7,bad))
    bad=copy.deepcopy(fixtures['6']);bad['combined']['a']='6736/105'
    reject('flipped negative upper pairing',lambda:check(6,bad))
    bad=copy.deepcopy(fixtures['5']);bad['pairings'][0]['d']='0'
    reject('lost derivative pairing',lambda:check(5,bad))
    reject('negative Schur pivot',lambda:schur_psd([[F(-1)]]))
    reject('zero pivot with nonzero row',lambda:schur_psd([[F(0),F(1)],[F(1),F(1)]]))
    reject('asymmetric exact matrix',lambda:schur_psd([[1,2],[0,1]]))
    reject('inexact floating matrix',lambda:schur_psd([[1.0]]))
    p=parameters(4,2);rec,_,_,_,_,_,L,_,_=build(4,2,p['kappa'],p['tau'],whole=True)
    X=domain(4,2)
    bad=copy.deepcopy(L);bad[0][0]+=1
    reject('changed actual empty loop',lambda:audit(4,2,X,bad,p['kappa'],p['tau']))
    bad=copy.deepcopy(L);ix={A:i for i,A in enumerate(X)}
    for A,B,x in ((1,3,1),(1,5,-1),(0,3,-1),(0,5,1)):
        i,j=ix[A],ix[B];bad[i][j]+=x;bad[j][i]+=x
    require(all(sum(row)==rec['N'] for row in bad),'damage row-preservation premise')
    reject('row-preserving intersecting support damage',lambda:audit(4,2,X,bad,p['kappa'],p['tau']))
    reject('omitted actual empty vertex',lambda:audit(4,2,X[1:],L,p['kappa'],p['tau']))
    reject('noncanonical original domain order',lambda:audit(4,2,list(reversed(X)),L,p['kappa'],p['tau']))
    _,entry=certificate(8,3)
    reject('deleted bcx supplied as member',lambda:entry(6|8,0))
    reject('unadmitted one-core triple',lambda:entry(1|8|16,0))
    reject('q8 zero repair outside rectangle',lambda:certificate(8,3,t=F(0)))
    reject('q8 negative kappa outside rectangle',lambda:certificate(8,3,kappa=F(-1)))
    reject('q8 below rectangle endpoint',lambda:certificate(8,3,t=F(1,4)))
    reject('q4,k3 infeasible branch',lambda:parameters(4,3))
    reject('unproved fourth deletion branch',lambda:parameters(12,4))
    reject('altered published helper pin',lambda:bootstrap.setup(pins={'triangle-majority/poly.py':'0'*64}))
    old=NORMS[4,2]
    try:
        NORMS[4,2]=old+1
        reject('incorrect finite derivative row norm',lambda:phase(4,2,'continuity'))
    finally:NORMS[4,2]=old
    from verify import census,TASKS
    mock=[{'q':int(task[0]),'k':int(task[1]),'phase':task[2],
           **({'kappa':task[3],'t':task[4]} if len(task)==5 else {})} for task in TASKS]
    census(mock)
    reject('omitted affine rectangle corner',lambda:census(mock[:6]+mock[7:]))
    reject('duplicated original matrix phase',lambda:census(mock+[mock[0]]))
    return out


if __name__=='__main__':print(json.dumps(checks(),sort_keys=True,indent=2))
