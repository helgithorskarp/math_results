"""Exact ordinary bridge and exhaustive cyclic-power type inventory.

The numerical local bounds are declared imported mathematical premises;
this arithmetic checker does not silently prove their source censuses.
"""
from math import lcm
from core import require, digest

def cycle_partitions(total, minimum=1):
    if total==0:
        yield ()
    for first in range(minimum,total+1):
        for rest in cycle_partitions(total-first,first):yield (first,)+rest

def literal_power(parts, exponent):
    output=[];offset=0
    for length in parts:
        output.extend(offset+(i+exponent)%length for i in range(length));offset+=length
    return tuple(output)

def valuation(n):
    result=0
    while n%2==0:result+=1;n//=2
    return result

def check():
    # Universal point cap gives size<=72. At size>=69, no saturated moved
    # point would imply5N<=344. A g-mate shares its exact degree. Three-tails
    # are disjoint, so all six possible pair multiplicities are retained.
    bounds=(56,58,60,56,58,69)
    require(18*20//5==72 and (16*19+2*20)//5==68,'point/moved capacity arithmetic')
    excluded=[]
    for size in range(70,73):
        require(5*size>16*19+2*20,'saturated moved pair not forced')
        require(all(bound<size for bound in bounds),'missing local branch contradiction')
        excluded.append(size)
    # Deletion at multiplicity1 has19 possible private mate words. Each
    # leaves center degrees20/19 and pair multiplicity1. Upper57 gives58.
    require(20-1==19 and 57+1==58,'arbitrary-packing single-pair deletion')
    # At size69, all16 moved degrees occur in equal pairs. Write R for
    # the sum of fixed degrees and k for the number of saturated pairs.
    # Then345<=40k+38(8-k)+R =304+2k+R, with R odd and <=39.
    equality=[]
    for R in range(0,41):
        for k in range(9):
            if R%2==1 and 345<=304+2*k+R:
                require(k>0 and 25<=R<=39 and k>=(41-R)//2,'equality parity/capacity implication')
                equality.append((R,k))
    parts=list(cycle_partitions(18));require(len(parts)==385,'all18-point cycle partitions')
    accepted=[];checked=0
    for p in parts:
        order=lcm(*p)
        if order%2:continue
        h=literal_power(p,order//2)
        require(sorted(h)==list(range(18)) and all(h[h[i]]==i for i in range(18)),'literal half-order involution')
        fixed=sum(h[i]==i for i in range(18))
        maximum=max(valuation(a) for a in p)
        moved=sum(a for a in p if valuation(a)==maximum)
        require(fixed==18-moved,'maximal2-adic cycle-mass bridge')
        if fixed==2:accepted.append({'cycles':p,'order':order,'half_order_power':h})
        checked+=1
    require(len(accepted)==14,'complete two-fixed involution-power type inventory')
    return {'status':'PASS_ORDINARY_GLOBAL_AND_CYCLIC_BRIDGES','imported_local_bounds':bounds,
            'global_upper':69,'excluded_sizes':excluded,'single_pair_private_deletions':19,
            'equality_necessary_R_k':equality,'cycle_partitions':385,'even_order_types':checked,
            'two_fixed_power_types':accepted,'type_inventory_sha256':digest(accepted)}

if __name__=='__main__':
    import json
    print(json.dumps(check(),sort_keys=True))
