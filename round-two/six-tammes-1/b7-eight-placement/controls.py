"""Fresh full geometric negative checks for both same-author implementations."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from contextlib import redirect_stdout
from io import StringIO
import json
import check as P
import audit as A


def need(ok, why):
    if not ok:
        raise ValueError(why)


def primary_accept(record, tag):
    with redirect_stdout(StringIO()):
        fresh=P.case(record['map'])
    return record == fresh


def alternate_accept(record):
    try:
        with redirect_stdout(StringIO()):
            A.audit(record['map'], record)
    except ValueError:
        return False
    return True


original=P.load_certificate()['cases'][0]
A.require(A.load_certificate()['cases'][0]==original,'whole shared literal record')
negative = []
damaged = deepcopy(original)
damaged['branches'] = damaged['branches'][:1]
negative.append(('missing-orientation', damaged))
damaged = deepcopy(original)
damaged['branches'][0]['equations'] = damaged['branches'][0]['equations'][:2]
negative.append(('missing-unused-contact', damaged))
damaged = deepcopy(original)
damaged['branches'][0]['equations'][0]['polynomial'][0] = str(int(damaged['branches'][0]['equations'][0]['polynomial'][0])+1)
negative.append(('wrong-norm-coefficient', damaged))
damaged = deepcopy(original)
damaged['branches'][0]['gcd'][0] = str(int(damaged['branches'][0]['gcd'][0])+1)
negative.append(('wrong-common-factor', damaged))
damaged = deepcopy(original)
damaged['branches'][0]['whole_closed_Bernstein'][-1] = '0'
negative.append(('lost-strict-closed-endpoint', damaged))
for tag, record in negative:
    need(not primary_accept(record, tag), 'fresh primary accepted damaged full record '+tag)
    need(not alternate_accept(record), 'fresh alternate accepted damaged full record '+tag)

# A valid tangent common-neighbor fiber must survive, including at the
# endpoint c=3/5,r=3/4. This checks the actual metric formula, not a tolerance.
r, d = F(3,4), F(5,4)
w = [F(1), F(0), F(0)]
u = [F(0), F(1), F(0)]
v = [2*r/d, F(-1), F(0)]
def dot(x, y):
    return (2-2*r)*sum(a*b for a,b in zip(x,y))+r*sum(x)*sum(y)
g = dot(u, v)
L, E = d+g, d-g
S, V = d*L-2*r*r, (2+r)*E
need(all(dot(x,x)==d for x in (w,u,v)), 'tangent three vectors unit')
need(dot(w,u)==r and dot(w,v)==r, 'tangent contacts exact')
need(S==0 and V>0 and L>0 and E>0, 'zero discriminant valid and denominator nonzero')
need([r*(x+y)/L for x,y in zip(u,v)]==w, 'tangent formula returns exact valid point')

# Incorrect degree-dropping modular specialization would report gcd1 for
# two identical nonconstant polynomials. The leading-coefficient gate must
# reject that claim before applying Gauss's lemma.
f = {(0,0): 1, (1,0): A.PRIME}
try:
    A.check_gcd([f,f], A.ONE)
except ValueError as e:
    need('preserves degree' in str(e), 'specific degree-preservation obligation')
else:
    raise ValueError('accepted invalid modular coprimality')

# Whole Bernstein endpoint values zero do not establish strict exclusion.
try:
    A.check_Bernstein_identity({(0,0): 1, (1,0): -1}, ['1','0'])
except ValueError as e:
    need('strict Bernstein' in str(e), 'strict closed endpoint obligation')
else:
    raise ValueError('accepted a zero endpoint as a strict exclusion')

for presented in [json.dumps(original, indent=2), json.dumps(original, sort_keys=True, separators=(',',':'))]:
    record = json.loads(presented)
    need(record == original and alternate_accept(record), 'valid JSON representation retained')

# Closed coverage and original physical/literal scope are mathematical inputs.
full=P.load_certificate();scope_damages=[]
for key,value in [('cosine_closed_band',['7/13','599/1000']),
                  ('r_closed_band',['701/1000','3/4']),
                  ('extra_contacts_allowed',False),
                  ('independent_mathematical_review',True),
                  ('literal_masks_have_15_distinct_unit_vectors',1),
                  ('remaining_closed_maps',[]),
                  ('remaining_strict_maps',[36])]:
    bad=deepcopy(full);bad[key]=value;scope_damages.append(bad)
bad=deepcopy(full);bad['cases']=bad['cases'][:-1];scope_damages.append(bad)
bad=deepcopy(full);bad['cases'][1]=deepcopy(bad['cases'][0]);scope_damages.append(bad)
for bad in scope_damages:
    for loader in (P.load_certificate,A.load_certificate):
        try:loader(bad)
        except ValueError:pass
        else:raise ValueError('accepted damaged full closed case cover or scope')

result = {'actual_agent':'six-tammes-1', 'role':'researcher',
          'full_geometric_negative_records':len(negative), 'each_negative_freshly_rebuilt_by_both':True,
          'valid_tangent_endpoint_retained':True, 'invalid_degree_drop_rejected':True,
          'zero_Bernstein_endpoint_rejected':True, 'valid_presentations':2, 'whole_scope_damages_rejected_by_both':len(scope_damages),
          'status':'complete; same-author checking, not independent mathematical review'}
expected=json.loads(Path(__file__).with_name('CONTROLS.json').read_text())
need(A.canon(result)==A.canon(expected),'entire exact control record')
print(A.canon(result),end='')
