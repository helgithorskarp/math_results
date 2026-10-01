"""Exact negative controls for certificate and quantitative scope failures."""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import copy
import json
import check
import audit

HERE=Path(__file__).resolve().parent


def rejected(callback,message):
    try: callback()
    except ValueError: return message
    raise ValueError('negative control was accepted: '+message)


def value(p,t):
    total=Q(0)
    for a in reversed(p): total=total*t+a
    return total


def rv(obj,t):
    return value(obj['numerator'],t)/value(obj['denominator'],t)


def verify():
    c=json.loads((HERE/'certificate.json').read_text())
    raw=json.loads((HERE/'model-functions.json').read_text())
    result=[]
    bad=copy.deepcopy(c);bad['edges'].pop()
    result.append(rejected(lambda:check.validate_config(bad),'missing prescribed edge'))
    bad=copy.deepcopy(c);bad['epsilon']=[1,10**12]
    result.append(rejected(lambda:check.validate_config(bad),'changed tolerance'))
    result.append(rejected(lambda:check.need(10*2000000*Q(1,10**12)<=Q(1,400000),
                                           'larger tolerance leaves local radius'),
                           'larger tolerance fails the actual radius bridge'))
    bad=copy.deepcopy(raw);bad['height2']['numerator']=[]
    result.append(rejected(lambda:audit.audit_bounds(bad,16),'false common-neighbor height'))
    # A too-small derivative bound fails at an exact rational endpoint.
    endpoint=Q(14,25)
    sums=[]
    for label in range(15):
        total=Q(0)
        for i in range(3):
            obj=raw[f's_{label}_{i}']
            n,d=audit.rational_derivative((tuple(map(Q,obj['numerator'])),
                                           tuple(map(Q,obj['denominator']))))
            total+=abs(value(n,endpoint)/value(d,endpoint))
        sums.append(total)
    result.append(rejected(lambda:check.need(max(sums)<=10,'model derivative l1 cannot be ten'),
                           'false derivative bound fails at a rational endpoint'))
    # A corrupted inverse fails a directly reconstructed matrix identity at t=59/100.
    point=Q(59,100)
    H=[[Q(1) if i==j else point for j in range(3)] for i in range(3)]
    V=[rv(raw[f's_9_{i}'],point) for i in range(3)]
    B8=[rv(raw[f's_8_{i}'],point) for i in range(3)]
    B12=[rv(raw[f's_12_{i}'],point) for i in range(3)]
    cross=(B12[1]*V[2]-B12[2]*V[1], B12[2]*V[0]-B12[0]*V[2],
           B12[0]*V[1]-B12[1]*V[0])
    HI=[[(Q(1)/(1-point) if i==j else Q(0))-point/((1-point)*(1+2*point))
         for j in range(3)] for i in range(3)]
    mu=(point-1)*(point+1)*(2*point+1)*(3*point-1)/(9*point**3-point**2-point+1)
    gamma=rv(raw['gamma'],point)
    C=[gamma*B12[i]+mu*sum(HI[i][j]*cross[j] for j in range(3)) for i in range(3)]
    X=[[sum(v[j]*H[j][i] for j in range(3)) for i in range(3)] for v in (V,B8,C)]
    xi=[[rv(raw[f'plus_xi_{i}_{j}'],point) for j in range(3)] for i in range(3)]
    def identity(matrix):
        return all(sum(X[i][k]*matrix[k][j] for k in range(3))==(1 if i==j else 0)
                   for i in range(3) for j in range(3))
    check.need(identity(xi),'uncorrupted inverse at the rational control point')
    xi[0][0]+=1
    result.append(rejected(lambda:check.need(identity(xi),'corrupted exact inverse'),
                           'corrupted inverse fails a rational matrix identity'))
    return {'status':'VERIFIED','negative_controls':result,'count':len(result)}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prerequisite-root',type=Path,default=check.ROOT,
                   help='accepted for command consistency; these controls have no prerequisite imports')
    p.parse_args()
    print(json.dumps(verify(),sort_keys=True,indent=2))
