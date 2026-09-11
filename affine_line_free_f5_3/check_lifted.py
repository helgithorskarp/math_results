"""Exact arithmetic certificate for every lifted base spectrum in Tables4–7."""
from pathlib import Path
from itertools import product
from math import comb
import json

data=json.loads(Path(__file__).with_name('lifted_catalogue.json').read_text())
full_types={'B5':(3,1,1,1,1,1),'B8':(2,2,1,1,1,1),'D1':(3,3,3,3,3,3)}
def constraints(size,base):
    assert sum(base)==31 and sum(i*n for i,n in enumerate(base))==size
    lam=[5*n for n in base];lam[3]+=1
    low=43-size
    const=120*lam[0]+105*(lam[1]-1)+91*lam[2]+78*lam[3]
    assert (const-15768)%5==0
    C=13*low-(const-15768)//5
    survivors=[]
    for u in range(lam[2]+1):
        for v in range(lam[1]):
            w=low-u-v
            if 0<=w<=lam[0] and 2*u+v==C:survivors.append((u,v,w))
    return {'base_size':size,'base_multiplicities':base,'dual_multiplicities':lam,
            'low_planes':low,'required_2a9_plus_a10':C,'surviving_low_counts':survivors}

answer=[]
for row in data['types18']:
    q=constraints(18,row['multiplicities'])
    assert row['full_line_count']>0 and min(full_types[row['full_line']])>0
    q['disposition']='full support line lifts to full support plane; branch F'
    answer.append(q)

row=data['type23'];q=constraints(23,row['multiplicities'])
line_counts=row['line_type_counts']
assert set(line_counts)=={'A1','A2','A3','B2','B3'}
assert sum(line_counts.values())==31
assert 3*sum(line_counts[t] for t in ('A1','A2','A3'))+8*(line_counts['B2']+line_counts['B3'])==6*23
assert 3*sum(line_counts[t] for t in ('A1','A2','A3'))+28*(line_counts['B2']+line_counts['B3'])==comb(23,2)+5*(4+3*3)
assert min(u for u,v,w in q['surviving_low_counts'])==11
# At any base point of multiplicity one only A2,A3,B2,B3 can occur.
# Count respectively all multiplicity-three, -two and other -one points.
local=[]
for a2,a3,b2,b3 in product(range(7),repeat=4):
    if a2+a3+b2+b3==6 and 2*b2+b3==3 and a2+2*b3==4 and 2*a3+b2==5:
        local.append((a2,a3,b2,b3))
assert local==[(2,2,1,1)]
assert 5*local[0][0]==10<11
q.update(disposition='excluded: a9>=11 but only10 A2 lines at a marked1-point',base_one_point_line_counts=local[0])
answer.append(q)

q=constraints(28,data['type28']['multiplicities']);assert not q['surviving_low_counts']
q['disposition']='excluded by nonnegative integral plane spectrum';answer.append(q)
assert sum(row['isomorphism_types'] for row in data['spectra33'])==10
for row in data['spectra33']:
    q=constraints(33,row['multiplicities']);assert q['required_2a9_plus_a10']>2*q['low_planes']
    assert not q['surviving_low_counts']
    q['disposition']='excluded by 2a9+a10<=2*(a9+a10+a11)';answer.append(q)
print(json.dumps({'all_lifted_cases_eliminated_or_in_F':True,'cases':answer},indent=2))
