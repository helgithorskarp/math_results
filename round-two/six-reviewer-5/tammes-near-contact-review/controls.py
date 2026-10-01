"""Exact geometry/interpolation controls and substantive corruption rejections."""
import argparse
import copy
from fractions import Fraction as Q
import json
from pathlib import Path

import audit as A

CONTACTS = [(0,1),(0,7),(1,2),(1,7),(2,3),(2,6),(2,7),
            (3,4),(3,5),(3,6),(4,5),(5,6),(6,7)]


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--upper-export',type=Path,required=True)
    p.add_argument('--author-expected',type=Path,required=True)
    args=p.parse_args()
    unit_checks=contact_checks=chart_checks=restriction_checks=0
    lo,hi=Q(14,25),Q(593,1000)
    for k in range(8):
        t=lo+(hi-lo)*Q(k,7)
        points=A.core(t)
        gram=lambda x,y:(1-t)*sum(a*b for a,b in zip(x,y))+t*sum(x)*sum(y)
        for x in points.values():
            A.need(gram(x,x)==1,'Exact unit identity at polynomial recovery nodes')
            unit_checks+=1
        for i,j in CONTACTS:
            A.need(gram(points[i],points[j])==t,'Exact prescribed-contact identity')
            contact_checks+=1
    # The cleared chart-norm identity has degrees at most (5,4,4).
    # Its complete tensor grid proves the polynomial identity by interpolation.
    for i in range(6):
        t=lo+(hi-lo)*Q(i,5)
        for u in map(Q,range(-2,3)):
            for v in map(Q,range(-2,3)):
                r=1+A.metric(u,v,t)
                y=(r-2-2*t*(u+v),2*u,2*v)
                A.need((1-t)*sum(z*z for z in y)+t*sum(y)**2==r*r,'Chart norm identity')
                chart_checks+=1
    values=A.interpolate(4,lo,hi)
    for cell in [(0,0,0),(1,0,1),(3,5,2),(6,41,17)]:
        coefficients=A.cell_coefficients(values,cell)
        depth,i,j=cell
        for x,y,z in [(Q(0),Q(0),Q(1)),(Q(1,7),Q(3,11),Q(5,13)),(Q(1),Q(1),Q(0))]:
            u=-4+Q(8,2**depth)*(i+y)
            v=-4+Q(8,2**depth)*(j+z)
            A.need(A.evaluate_bernstein(coefficients,(x,y,z))==A.actual_polynomial(4,lo+(hi-lo)*x,u,v),
                   'Closed-cell de Casteljau endpoint/interior evaluation')
            restriction_checks+=1
    exported=json.loads(args.upper_export.read_text())
    expected=next(z for z in json.loads(args.author_expected.read_text())['strips'] if z['strip']=='upper')
    rejected=0

    def reject(data, messages):
        nonlocal rejected
        try:
            A.audit(data,expected)
        except ValueError as error:
            A.need(str(error) in messages,'Unexpected rejection: '+str(error))
            rejected+=1
        else:
            raise ValueError('Corruption accepted')

    changed=copy.deepcopy(exported)
    index=next(i for i,row in enumerate(changed['discarded']) if row[1]=='bernstein')
    changed['discarded'].pop(index)
    reject(changed,{'Entrywise original transfer hashes'})
    changed=copy.deepcopy(exported)
    changed['interval'][0]=[57,100]
    reject(changed,{'Exact strip'})
    changed=copy.deepcopy(exported)
    changed['conditioned_pairs'][0]['weights'][0]='-1'
    reject(changed,{'Normalized nonnegative dual weights'})
    changed=copy.deepcopy(exported)
    changed['single_cells'][0]['negative_rhs']='-100'
    reject(changed,{'Entrywise original transfer hashes'})
    previous=A.NEW_DELTA
    try:
        A.NEW_DELTA=Q('868844/128783337075')
        reject(exported,{'Improved transferred margin','Improved dual transfer'})
        A.NEW_DELTA=Q(1,140000)
        reject(exported,{'Improved transferred margin','Improved dual transfer'})
    finally:
        A.NEW_DELTA=previous
    A.need(A.stability()['growth']=='2837/32','Final stability value')
    print(json.dumps({'agent':'six-reviewer-5','role':'independent reviewer',
                      'status':'ALL_GEOMETRY_AND_CORRUPTION_CONTROLS_PASS',
                      'unit_identity_checks':unit_checks,'contact_identity_checks':contact_checks,
                      'chart_identity_grid_checks':chart_checks,'subcell_evaluation_checks':restriction_checks,
                      'substantive_corruptions_rejected':rejected,
                      'limiting_certificate_failure_is_not_nonexistence':True},indent=2))


if __name__=='__main__':
    main()
