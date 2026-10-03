"""Small definition-level controls, independent of the current packet."""
import json
from fractions import Fraction as F
from digit import T, Z, monomials, prove_zero, coefficients
from geometry import model, dot, CONTACTS, LABELS
from signs import bound, complete_sign


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    simple = (T+Z)**3-T**3-3*T*T*Z-3*T*Z*Z-Z**3
    prove_zero(simple)
    p=monomials([(0,0,-13),(4,0,29),(0,3,-47),(2,2,101)])
    require(coefficients(p)=={(0,0):-13,(4,0):29,(0,3):-47,(2,2):101},
            'balanced digit recovery failed')
    rejected=[]
    for name,p in [('false_identity',simple+1),('digit_collision',T**2-Z)]:
        try:
            prove_zero(p)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('false polynomial accepted')
    lo,hi=bound({(0,0):1,(2,0):1,(0,2):1},[0,1,0,2])
    require((lo,hi)==(F(1),F(6)),'interval bound failed')
    lo,hi=bound({(0,0):-1,(1,0):-2},[0,1,0,1])
    require((lo,hi)==(F(-3),F(-1)),'negative interval failed')
    try:
        complete_sign({(1,0):1},[0,1,0,1],1)
    except RuntimeError:
        rejected.append('closed_endpoint_zero')
    else:
        raise ValueError('closed endpoint zero accepted')
    m=model();records={}
    for i in LABELS:
        residual=dot(m['Y'][i],m['Y'][i])-m['Omega']**2
        records['unit'+str(i)]=[prove_zero(residual.p),prove_zero(residual.q)]
    for i,j in CONTACTS:
        residual=dot(m['Y'][i],m['Y'][j])-T*m['Omega']**2
        records['contact'+str(i)+'-'+str(j)]=[prove_zero(residual.p),prove_zero(residual.q)]
    print(json.dumps({'generic_radix_zero_controls':1,'balanced_digits':4,
                      'rejected':rejected,'original_labels':list(LABELS),
                      'unit_contacts_components':records},sort_keys=True))


if __name__=='__main__':
    main()
