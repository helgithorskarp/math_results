"""Untrusted compact data producer; no solver and no PSD certificate reuse."""
from fractions import Fraction
from pathlib import Path
from collections import deque
import json

base=Path(__file__).resolve().parent
parent=json.loads((base/'BASE-DATA.json').read_text())
keys=parent['free_original_entry_orbit_keys']
bad={(0,2,0),(0,0,2),(6,0,1)}
nums=[]
for key in keys:
    u,v=map(tuple,key)
    if not u[0]&1 and not v[0]&1:
        if u in bad and v in bad:
            pair=tuple(sorted((u,v)))
            x={tuple(sorted(((0,2,0),(0,0,2)))):Fraction(7,18),
               tuple(sorted(((0,2,0),(6,0,1)))):Fraction(7,9),
               ((0,0,2),(0,0,2)):Fraction(-1,3)}.get(pair,Fraction(-1))
        elif u not in bad and v not in bad:
            x=Fraction(-7804,81) if set((u,v))=={(0,1,0),(0,0,1)} else Fraction(1)
        else:x=Fraction(0)
    else:
        x=Fraction(-1) if set((u,v))=={(0,1,0),(7,0,0)} else Fraction(0)
    nums.append(int(162*x))

# An explicit spanning tree and a chord making an odd triangle.
z=[1<<i for i in range(3,12)];w=[1<<i for i in range(12,21)]
vertices=sorted([x+y for i,x in enumerate(z) for y in z[i+1:]]+
                [x+y for i,x in enumerate(w) for y in w[i+1:]]+[6+x for x in w])
queue=deque([vertices[0]]);seen={vertices[0]};edges=[]
while queue:
    a=queue.popleft()
    for b in vertices:
        if b not in seen and not a&b:
            seen.add(b);queue.append(b);edges.append(sorted((a,b)))
chord=[(1<<12)+(1<<13),(1<<14)+(1<<15)]
edges.append(chord)
data={'actual_agent':'six-downset-3','role':'researcher','q':18,'k':9,
      'actual_empty_N':278,'s':58,'real_tau_interval':['0','1/128'],
      'eta':'1/1152921504606846976','perturbation_denominator':162,
      'free_original_entry_orbit_keys':keys,'free_original_perturbation_numerators':nums,
      'bad_incidence_rank_witness_edges':edges,'bad_incidence_absolute_determinant':2,
      'odd_triangle_masks':[vertices[0],*chord],
      'claimed_affine_dimension':20711,'claimed_forced_ordered_entry_positions':163,
      'claimed_bad_bad_free_l1':'1512','claimed_good_good_free_l1':'15608',
      'claimed_anchored_free_l1':'9','claimed_proper_operator_coefficient_bound':'17138',
      'claimed_actual_entry_coefficient_bound':'34249',
      'published_parent_C_starperp_and_U_uniform_floor':'1/128',
      'derived_C_starperp_and_U_uniform_floor':'1/256',
      'PSD_proof_uses_explicit_published_10296_dependency_not_new_factors':True}
(base/'GEOMETRY.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
print(json.dumps({'untrusted_data_produced':True,'orbit_coefficients':len(nums),
                  'incidence_vertices_visited':len(seen),'selected_edges':len(edges)}))
