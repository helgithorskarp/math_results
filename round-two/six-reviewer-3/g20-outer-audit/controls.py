"""Actual damaged mathematical inputs and invalid radical guards."""
import copy
import json
from fractions import Fraction as F
from pathlib import Path
import audit
from digit import T, coefficients, prove_zero
from geometry import dot


def reject(name,call,records):
    try:
        call()
    except (ValueError,TypeError,RuntimeError):
        records.append(name)
    else:
        raise ValueError('damaged input accepted: '+name)


def guard(A,B,w,kind):
    if w<=0:raise ValueError('root is not positive')
    if kind=='lower':
        if not (B>0 and A*A-B*B*w*w<0):raise ValueError('lower guard')
    elif kind=='upper':
        if not (A>0 and A*A-B*B*w*w>0):raise ValueError('upper guard')
    elif kind=='boundary':
        if not (A>0 and B>0):raise ValueError('boundary guard')
    else:raise ValueError('unknown guard')
    if A+B*w<=0:raise ValueError('claimed positive excess failed')


def main():
    original=json.loads(Path('FACTORS.json').read_text());records=[]
    for name in ['L5','M6','H10','H12']:
        damaged=copy.deepcopy(original)
        damaged['rows'][name][0][3]=str(int(damaged['rows'][name][0][3])+1)
        # Change the actual coefficient; do not merely change an expected flag.
        reject('actual_coefficient_'+name,
               lambda d=damaged:audit.compile_identities(audit.packet(d)),records)
        missing=copy.deepcopy(original);del missing['rows'][name]
        reject('missing_'+name,lambda d=missing:audit.packet(d),records)
    damaged=copy.deepcopy(original);damaged['rows']['L5'].append(damaged['rows']['L5'][0][:])
    reject('duplicate_actual_monomial',lambda:audit.packet(damaged),records)
    badroot=copy.deepcopy(original);badroot['rows']['L5'][0][2]=1
    reject('nonzero_radical_exponent',lambda:audit.packet(badroot),records)
    badorder=copy.deepcopy(original);badorder['variable_order']=['z','t','w']
    reject('swapped_variables',lambda:audit.packet(badorder),records)
    for cut in [F(7,5),F(1399,1000)]:
        boxes=audit.cover(cut)
        for k in range(3):
            reject('missing_closed_box_'+str(cut)+'_'+str(k),
                   lambda k=k,b=boxes,c=cut:audit.complete_cover(b[:k]+b[k+1:],c),records)
    m=audit.model();damaged=dict(m);damaged['Y']=dict(m['Y'])
    damaged['Y'][5],damaged['Y'][6]=damaged['Y'][6],damaged['Y'][5]
    r=dot(damaged['Y'][5],damaged['Y'][9])-T*m['Omega']**2
    reject('actual_original_label_swap',lambda:prove_zero(r.p),records)
    reject('nondividing_integer_factor',lambda:audit.univariate_quotient(
        coefficients(T*T+1),coefficients(T+1)),records)
    for name,A,B,w,kind in [('negative_B_lower',-2,-3,1,'lower'),
                          ('negative_A_upper',-3,2,1,'upper'),
                          ('negative_root',-2,3,-1,'lower'),
                          ('zero_root',-2,3,0,'lower'),
                          ('squared_boundary_zero',3,-3,1,'upper')]:
        reject(name,lambda A=A,B=B,w=w,k=kind:guard(A,B,w,k),records)
    for A,B,w,kind in [(-2,3,1,'lower'),(3,-2,1,'upper'),(1,1,1,'boundary')]:
        guard(A,B,w,kind)
    print(json.dumps({'actual_agent':'six-reviewer-3','rejected_actual_damages':records,
                      'rejected_count':len(records),'valid_radical_guards':3},sort_keys=True))


if __name__=='__main__':
    main()
