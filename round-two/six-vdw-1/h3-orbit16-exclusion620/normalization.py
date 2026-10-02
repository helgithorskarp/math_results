"""Whole signed input actions for field scalars/phase affines; orbit16 coverage."""
import argparse
import json
from math import gcd
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def check(d):
    require((d['field_prime'],d['row_half'],d['AP_length'],d['subgroup'],d['fixed_first_coset_row'],d['variables'])==(31,10,7,[1,5,25],16,100),'exact audited production family')
    H={1,5,25};classes=sorted({tuple(s for s in range(1,31) if s*pow(r,-1,31)%31 in H) for r in range(1,31)},key=lambda c:c[0])
    group_of={r:i for i,c in enumerate(classes) for r in c}
    literal=[None if x%31==0 else (1 if x%20<10 else -1)*(10*group_of[x%31]+x%10+1) for x in range(620)]
    require(literal==d['point_literals'] and d['cosets']==[list(c) for c in classes],'whole actual independent input/coset table')
    crt={(r,s):next(x for x in range(620) if x%31==r and x%20==s) for r in range(31) for s in range(20)}
    units=[v for v in range(20) if gcd(v,20)==1]
    row=lambda mask,s:((mask//2**(s%10))%2+s//10)%2
    orbit={sum(row(16,(v*s+z)%20)*2**s for s in range(10)) for v in units for z in range(20)}
    require(len(orbit)==160 and min(orbit)==16,'complete local orbit16')
    normalizers={}
    for mask in sorted(orbit):
        matches=[(v,z) for v in units for z in range(20) if all(row(mask,(v*s+z)%20)==row(16,s) for s in range(20))]
        require(len(matches)==1,'each forbidden-class row has its complete unique phase normalizer');normalizers[mask]=matches[0]
    local=[[(a+j*h)%20 for j in range(7)] for a in range(20) for h in range(1,20)]
    admissible={m for m in range(1024) if all(len({row(m,s) for s in pos})>1 for pos in local)}
    require(len(admissible)==580 and orbit<=admissible,'whole1024 local census and all160 class members admissible')
    actions=set();identities=maps=0;first_images=set()
    for mu in range(1,31):
        first_images.add(group_of[mu])
        for v in units:
            A=crt[mu,v];require(gcd(A,620)==1,'actual CRT affine multiplier must be a unit')
            for z in range(20):
                B=crt[0,z]
                require({(A*x+B)%620 for x in range(620)}==set(range(620)),'whole actual affine bijection')
                substitution=[]
                for c in classes:
                    for j in range(10):substitution.append(literal[(A*crt[c[0],j]+B)%620])
                require({abs(s) for s in substitution}==set(range(1,101)),'global input action is a signed permutation, not an invariance assumption')
                for x,l in enumerate(literal):
                    y=(A*x+B)%620
                    if l is None:require(literal[y] is None,'actual poles preserve their modular domain');continue
                    require(literal[y]==(1 if l>0 else -1)*substitution[abs(l)-1],'whole actual signed input action');identities+=1
                actions.add(tuple(substitution));maps+=1
    require(first_images==set(range(10)) and maps==4800 and len(actions)==1600,'complete fieldcoset/phase action coverage')
    return {'author':'six-vdw-1','role':'researcher','status':'COMPLETE_H3_ANY_COSET_ORBIT16_NORMALIZATION',
            'local_raw_inputs':1024,'locally_admissible_rows':580,'forbidden_orbit_representative':16,
            'forbidden_local_row_masks':sorted(orbit),'forbidden_orbit_size':160,'remaining_local_row_masks':420,
            'field_scalar_maps':30,'phase_affine_maps':160,'combined_actual_CRT_maps':maps,
            'distinct_signed_input_permutations':len(actions),'all_actual_regular_signed_point_identities':identities,
            'first_coset_field_images':len(first_images),'unique_phase_normalizers':len(normalizers),
            'scope':'Conditional transfer: IF audited firstcoset16 formula is strictly refuted, every coset row in orbit16 is forbidden for any H3-invariant AP7-free regular620 core. No finite pole extension or arbitrary-core quotient.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model',type=Path);a=p.parse_args()
    print(json.dumps(check(json.loads(a.model.read_text())),sort_keys=True),flush=True)
