"""Independent positive-gap coefficients, multiplicities and complete small circles."""
from collections import Counter
import itertools
import json
import math
from pathlib import Path
from common import pins,require

def coefficient(parts,total,bound):
    if total<0:return 0
    polynomial=[1]+[0]*total
    for _ in range(parts):
        following=[0]*(total+1)
        for degree,value in enumerate(polynomial):
            for gap in range(1,bound+1):
                if degree+gap<=total:following[degree+gap]+=value
        polynomial=following
    return polynomial[total]

def independent_ie(parts,total,bound):
    if parts==0:return int(total==0)
    if total<parts:return 0
    excess=total-parts
    return sum((-1)**j*math.comb(parts,j)*math.comb(total-1-j*bound,parts-1)
        for j in range(min(parts,excess//bound)+1))

def check():
    pins();records=[];ordered=0
    for a1 in range(1,4):
        for a2 in range((11-3*a1)//2+1):
            a3=11-3*a1-2*a2;a4=2*a1+a2
            require(a3>=0 and a4>=2 and a1+a2+a3+a4==11 and a1+2*a2+3*a3+4*a4==33,
                    'wrong complete isolated-gap multiplicity classification')
            multiplicity=math.factorial(11)//math.prod(math.factorial(a) for a in (a1,a2,a3,a4))
            ordered+=multiplicity
            records.append(dict(a1=a1,a2=a2,a3=a3,a4=a4,ordered_gap_compositions=multiplicity))
    bounded=coefficient(11,33,4);without_one=coefficient(11,22,3)
    require(bounded==independent_ie(11,33,4)==154518
            and without_one==independent_ie(11,22,3)==25653
            and ordered==bounded-without_one==128865 and len(records)==10,
            'independent polynomial/IE/multinomial coefficients differ')
    require(coefficient(11,33,3)==independent_ie(11,33,3)==1
            and coefficient(11,22,2)==independent_ie(11,22,2)==1,'regular-gap boundary differs')
    words=Counter();literal=0
    for n in range(5,13):
        for bits in itertools.product((0,1),repeat=n):
            selected=[i for i,v in enumerate(bits) if v]
            if len(selected)<2:continue
            gaps=[(selected[(j+1)%len(selected)]-i)%n-1 for j,i in enumerate(selected)]
            if min(gaps)==1 and max(gaps)==4:
                words[n,len(selected)]+=1;literal+=1
    identities=0
    for n in range(5,13):
        for k in range(2,n//2+1):
            total=n-k
            numbers=[coefficient(k,total,4),coefficient(k,total,3),
                coefficient(k,total-k,3),coefficient(k,total-k,2)]
            require(numbers==[independent_ie(k,total,4),independent_ie(k,total,3),
                independent_ie(k,total-k,3),independent_ie(k,total-k,2)],'small independent coefficients differ')
            ordered_small=numbers[0]-numbers[1]-numbers[2]+numbers[3]
            require(k*words[n,k]==n*ordered_small,'whole small cyclic gap-four count differs');identities+=1
    labeled=44*ordered//11
    require(44*ordered%11==0 and labeled==515460,'wrong ordinary marked-word quotient')
    return dict(agent='six-vdw-2',role='researcher',status='EXACT_ORDINARY_RESIDUAL_GAP4_COUNTS',
        multiplicities=records,ordered_gap_compositions=ordered,
        labeled_necessary_phase_words_per_background=labeled,
        all_isolated_gap4_words_before_parent_minimum_condition=4*(bounded-1),
        actual_gap_one_required_by_parent=True,at_least_two_maximum_background_gaps=True,
        gap_one_multiplicity_range=[1,3],positive_background_gap_sum=33,
        small_literal_cyclic_words=literal,small_marking_identities=identities,
        ordinary_marked_word_count_not_free_symmetry_orbit_division=True,
        counts_are_feasible_field_colorings=False,phase_endpoint_exclusion=False,global_W_bound=False)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    result=check();args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
