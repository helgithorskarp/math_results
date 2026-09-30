"""Reproduce the finite exclusion and its exact ordinary-weight barrier."""
import copy
import hashlib
import json
from pathlib import Path
from binary_certificate import verify, need, prime_powers
from fractional_certificate import verify_fractional


ROOT=Path(__file__).resolve().parent


def clean(result):
    return {k:v for k,v in result.items() if k!='seconds'}


def compute():
    integer_bytes=(ROOT/'input.json').read_bytes()
    fractional_bytes=(ROOT/'fractional.json').read_bytes()
    c=json.loads(integer_bytes);f=json.loads(fractional_bytes)
    known=[[8,0],[9,0],[10,1],[14,1],[12,6],[16,4],[15,2],[18,5],
           [20,16],[21,4],[24,2],[27,2]]
    need(c['prefix']==f['prefix']==known and c['N']==f['N']==15120 and
         c['minimum']==f['minimum']==8, 'Declared common finite prefix')
    integer=clean(verify(c));fractional=clean(verify_fractional(f))
    mutations=[]
    m=copy.deepcopy(c);m['evidence']['capacity']+=1;mutations.append(('advertised gap',m))
    m=copy.deepcopy(c);m['minimum']=9;mutations.append(('minimum domain',m))
    m=copy.deepcopy(c);m['cluster'].append(9);mutations.append(('duplicate cluster',m))
    m=copy.deepcopy(c);m['prefix'].append([48,0]);mutations.append(('second prescribed top',m))
    m=copy.deepcopy(c);m['u_boxes'][0][0].append(m['u_boxes'][0][0][0]);mutations.append(('axis duplicate',m))
    m=copy.deepcopy(c);m['v_values'][0]=-1;mutations.append(('negative weight',m))
    m=copy.deepcopy(c);m['u_boxes'].append([[4],[4],[4],[4]]);m['u_values'].append(1);mutations.append(('covered u weight',m))
    m=copy.deepcopy(c);m['u_values']=[0]*len(m['u_values']);m['v_values']=[0]*len(m['v_values']);m.pop('evidence');mutations.append(('zero nonstrict cut',m))
    integer_rejected=[]
    for label,m in mutations:
        try:verify(m)
        except ValueError:integer_rejected.append(label)
        else:raise ValueError('Invalid integer certificate accepted: '+label)
    mutations=[]
    m=copy.deepcopy(f);m['denominator']=0;mutations.append(('zero denominator',m))
    m=copy.deepcopy(f);m['groups'][0]['numerator']=-1;mutations.append(('negative phase mass',m))
    m=copy.deepcopy(f);m['groups'][0]['numerator']=f['denominator']+1;mutations.append(('overbudget resource',m))
    m=copy.deepcopy(f);m['groups'][0]['phase_count']+=1;mutations.append(('phase count',m))
    m=copy.deepcopy(f);m['groups'][0]['modulus']=8;mutations.append(('known resource reused',m))
    m=copy.deepcopy(f);m['groups'][0]['phase_axes'][0].append(m['groups'][0]['phase_axes'][0][0]);mutations.append(('phase duplicate',m))
    m=copy.deepcopy(f);m.pop('expected')
    for group in m['groups']:group['numerator']=1
    mutations.append(('insufficient coverage',m))
    fractional_rejected=[]
    for label,m in mutations:
        try:verify_fractional(m)
        except ValueError:fractional_rejected.append(label)
        else:raise ValueError('Invalid fractional certificate accepted: '+label)
    # A genuine small integer cover supplies a positive fractional-control case.
    # Its minimum2 is separate from the assigned minimum8 application.
    toy={'N':36,'minimum':2,'prefix':[[4,1]],'denominator':1,'groups':[]}
    for n,a in [(2,0),(3,0),(6,3),(12,7),(9,2),(18,5),(36,35)]:
        toy['groups'].append({'modulus':n,'numerator':1,'phase_count':1,
                              'phase_axes':[[a%P] for P in prime_powers(n)]})
    positive=clean(verify_fractional(toy))
    return {'agent':'six-covering-2','role':'researcher','all_passed':True,
            'input_sha256':hashlib.sha256(integer_bytes).hexdigest(),
            'fractional_sha256':hashlib.sha256(fractional_bytes).hexdigest(),
            'integer_exclusion':integer,'fractional_completion':fractional,
            'positive_fractional_control':positive,
            'integer_malformed_rejections':integer_rejected,
            'fractional_malformed_rejections':fractional_rejected,
            'scope':'Fixed12-class15120 exclusion and exact absence of any ordinary resource-by-resource weighted obstruction; no global L_min(8) improvement or independent review'}


if __name__=='__main__':
    result=compute()
    need(result==json.loads((ROOT/'expected.json').read_text()), 'Changed exact expected result')
    print(json.dumps(result,indent=2))
