"""Reject damaged coverage and actual vertex inequalities, with no full rerun."""
from copy import deepcopy
from pathlib import Path
import json
import audit,generate,polytope as p
def reject(operation,label):
    try:operation()
    except (ValueError,ArithmeticError):return label
    raise ValueError('damaged control was accepted: '+label)
def controls():
    plan=json.loads((Path(__file__).resolve().parent/'PLAN.json').read_text())
    bad=deepcopy(plan);bad['cells'][1]=bad['cells'][0]
    rejected=[reject(lambda:generate.cells(bad),'duplicate_cell_leaves_a_gap')]
    a,b,_,_=generate.cells()[0]
    A,rhs,H,br,nn,model=p.geometry(a,b)
    rejected.append(reject(lambda:audit.verify((0,1,2),('analytic-critical',None),A,rhs,H,model),
                           'wrong_triple_claims_critical_exception'))
    norm=None;hom=None
    for triple in p.TRIPLES:
        result=p.classify(triple,A,rhs,H)
        if result is None:continue
        if result[0]=='norm' and norm is None:norm=(triple,result)
        if result[0]=='homogeneous' and hom is None:hom=(triple,result)
        if norm and hom:break
    p.e.require(norm is not None and hom is not None,'positive controls available')
    audit.verify(norm[0],norm[1],A,rhs,H,model)
    audit.verify(hom[0],hom[1],A,rhs,H,model)
    rejected.append(reject(lambda:audit.verify(norm[0],('norm',p.S),A,rhs,H,model),
                           'non_strict_norm_witness'))
    triple,result=hom;C,D=audit.minors([A[i] for i in triple],[rhs[i] for i in triple])
    bad_witness=list(result[1]);wanted=1 if D.sign()>=0 else -1
    wrong=None
    for index,row in enumerate(A):
        if index in triple:continue
        residual=audit.inner(row,C)-rhs[index]*D
        if (wanted==1 and residual.l<=0) or (wanted==-1 and residual.h>=0):wrong=index;break
    p.e.require(wrong is not None,'a geometrically invalid row exists for control')
    bad_witness[0 if wanted==1 else 1]=wrong
    rejected.append(reject(lambda:audit.verify(triple,('homogeneous',bad_witness),A,rhs,H,model),
                           'wrong_row_fails_required_homogeneous_sign'))
    return {'status':'DAMAGED_CONTROLS_REJECTED','positive_witnesses_verified':2,'rejected':rejected}
if __name__=='__main__':print(json.dumps(controls(),sort_keys=True))
