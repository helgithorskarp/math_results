#!/usr/bin/env python3
"""Exact local phase classification and arithmetic controls for the group corollary."""
import itertools, json, math

def need(ok,message):
    if not ok: raise ValueError(message)

def main():
    f = (0,0,0,1,1,1); legal = []; rotations = {tuple(f[(y-s)%6] for y in range(6)):s for s in range(6)}
    for b in itertools.product((0,1),repeat=6):
        direct = all(len({b[(y+j*d)%6] for j in range(7)}) == 2 for y in range(6) for d in range(1,6))
        elementary = all(b[y]!=b[y+3] for y in range(3)) and all(len({b[(y+2*j)%6] for j in range(3)})==2 for y in (0,1))
        need(direct==elementary==(b in rotations),'Complete six-bit phase classification differs')
        if direct: legal.append(b)
    units = [m for m in range(618) if math.gcd(m,618)==1]
    need(len(units)==204 and all((m*309)%618==309 for m in units),'Antipodal centrality arithmetic')
    need((413%103,206%103,413%6,206%6)==(1,0,5,2),'Residual CRT involution differs')
    reflection_controls = 0
    for b in legal:
        s=rotations[b]
        for orientation in (0,1):
            for y in range(6):
                need((orientation^b[(2*s+2-y)%6])==(orientation^b[y]),'Separable reflection identity failed')
                reflection_controls+=1
    return {'six_bit_inputs':64,'legal_phases':len(legal),'all_nonzero_phase_steps_checked':30,
            'unit_multipliers':len(units),'affine_group_order':618*len(units),
            'global_complement_quotient_orbit':618*len(units)//2,
            'reflection_controls':reflection_controls,'maximum_lift_endpoint_zero_based':617+6*309,
            'separable_constant_skeleton_orientations':3*(1<<103),
            'status':'LOCAL_PHASE_CLASSIFICATION_AND_AFFINE_ARITHMETIC_CHECKED'}

if __name__=='__main__': print(json.dumps(main(),sort_keys=True))
