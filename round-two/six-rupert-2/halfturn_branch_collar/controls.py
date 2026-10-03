#!/usr/bin/env python3
"""Meaningful false-geometry controls; every check runs also under -O."""
from pathlib import Path
from fractions import Fraction as F
import copy,json
import check as c
g,a,Q=c.g,c.a,c.Q
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'certificate.json').read_text());rejected=[]
def reject(label,fn):
    try:fn()
    except (ValueError,ZeroDivisionError):rejected.append(label);return
    raise ValueError('false mathematical fixture accepted: '+label)
bad=copy.deepcopy(data);bad['face_source_indices'].pop()
reject('omitted actual face vertex loses the positive centroid disk',lambda:c.geometry(bad))
bad=copy.deepcopy(data);bad['face_source_indices'][1]=14
reject('nongenuine positive supporting face point',lambda:c.geometry(bad))
bad=copy.deepcopy(data);bad['actual_antipodes'][1]=9
reject('nongenuine original antipode cannot eliminate arbitrary translation',lambda:c.geometry(bad))
bad=copy.deepcopy(data);bad['receiving_endpoints'].pop()
reject('omitted closed top-edge endpoint',lambda:c.parameters(bad))
ratio=Q(F(29,121),F(-12,121))
reject('unproved larger radius1/7 fails the actual cusp margin',lambda:g.require(ratio>Q(F(1,49)),'strict cusp inequality'))
bad=copy.deepcopy(data);bad['line_antipodes'][1]=39
reject('nongenuine original antipode in a nonlinear width row',lambda:c.geometry(bad))
reject('improper body Mx cannot be an original proper source',lambda:g.proper(g.MX))
r=g.raw(Q());M=g.reflection(r)
reject('wrong companion action loses the actual merger at q',lambda:g.require(g.mm(g.mm(M,g.G),g.MX)==g.G,'wrong branch action'))
eps=Q(F(1,100));M=g.reflection(g.raw(eps));J=g.mm(g.mm(M,g.G),g.MY)
kap=eps/(4*g.t-g.qx*eps)
g.require(kap*kap*g.U2<g.rho*g.rho,'distinct fitted companion is actually inside the closed G collar')
reject('false isolated-G conclusion ignores a genuine nearby companion',lambda:g.require(J==g.G,'false isolated conclusion'))
reject('duplicated physical normal does not remove the second translation coordinate',lambda:g.require(a.cross(g.U,g.U)==a.scale(g.t,g.raw(eps)),'false receiving-normal basis'))
y=g.t+Q(F(1,100));Uy=(Q(),y,Q(1));hy=a.dot(Uy,g.V[0])
reject('false equal opposite support height above the top edge',lambda:g.require(a.dot(Uy,g.V[27])>=-hy,'opposite receiving support changes immediately'))
out={'agent':'six-rupert-2','role':'researcher','semantic_false_mathematical_fixtures_rejected':rejected,'count':len(rejected),'status':'all explicit exception checks; no Python assert statement'}
print(json.dumps(out,indent=2))
