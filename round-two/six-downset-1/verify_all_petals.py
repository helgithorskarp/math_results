#!/usr/bin/env python3
"""Definition-level exact replay of arbitrary Boolean-petal attachments.

Standard library only. verify.py and verify_multi.py are credited local
dependencies. All arithmetic is rational; the literal matrix guard is80.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import argparse
import json
import verify as base
import verify_multi as three


def validate_orders(orders, unique=False):
    base.require(len(orders) >= 2 and all(isinstance(a, int) and 1 <= a <= 12 for a in orders),
                 "positive orders required")
    base.require(list(orders) == sorted(orders, reverse=True), "decreasing orders required")
    base.require(sum(2**a for a in orders)-len(orders)+1 <= 80, "literal matrix order exceeds80")
    base.require(not unique or orders[0] > orders[1], "unique largest order required")


def small_lmi(stars, g, beta):
    """Independent full r-by-r Sherman--Morrison cap check."""
    r, t = len(stars), stars[0]
    n = 1+sum(2*v-1 for v in stars)
    base.require(len(g) == r and all(len(row) == r for row in g), "bad Gram dimensions")
    base.require(all(g[i][i] == t-1 for i in range(r)), "bad Gram diagonal")
    gram_rank = base.psd_rank(g)
    alpha = [F(t-2*v+1, t-1) for v in stars]
    d_inv = [1/(1+F(2*v-2, (t-1)**2)) for v in stars]
    denominator = 1+sum(a*a*d for a,d in zip(alpha,d_inv))
    inverse = [[d_inv[i]*int(i == j)-d_inv[i]*alpha[i]*alpha[j]*d_inv[j]/denominator
                for j in range(r)] for i in range(r)]
    matrix_r = [[F(int(i == j))/d_inv[i]+alpha[i]*alpha[j] for j in range(r)] for i in range(r)]
    base.require(all(sum(matrix_r[i][k]*inverse[k][j] for k in range(r)) == int(i == j)
                     for i in range(r) for j in range(r)), "R inverse mismatch")
    margin_rank = base.psd_rank([[(n-beta)*inverse[i][j]-g[i][j] for j in range(r)] for i in range(r)])
    base.require(base.psd_rank([[n*inverse[i][j]-g[i][j] for j in range(r)] for i in range(r)]) == r,
                 "small cap not strict")
    return {"Gram_rank":gram_rank,"small_margin_rank":margin_rank,"Gram_sha256":base.fingerprint(g)}


def unique_gram(stars):
    """Two/three leading petals, arbitrary many opposite smaller pairs."""
    r, t = len(stars), stars[0]
    base.require(r >= 2 and t > stars[1] >= 1, "unique maximal star required")
    base.require(all(isinstance(v,int) and v > 0 and v & (v-1) == 0 for v in stars), "dyadic stars required")
    a = t-1
    leading = 2 if r % 2 == 0 else 3
    g = [[F(0) for _ in range(r)] for _ in range(r)]
    if leading == 2:
        u = stars[1]
        lead_g = [[F(a),F(a)],[F(a),F(a)]]
        beta0 = F((2*u-1)*(t-2*u+1),a)
        leading_mode = "two_aligned"
    else:
        lead_g,beta0,regime = three.small_parameters(stars[:3])
        alpha0 = [F(t-2*v+1,a) for v in stars[:3]]
        centered = all(sum(lead_g[i][j]*alpha0[j] for j in range(3)) == 0 for i in range(3))
        leading_mode = "three_centered:"+regime if centered else "three_aligned:"+regime
        base.require(centered or lead_g == [[F(a) for _ in range(3)] for _ in range(3)], "unhandled leading frame")
    for i in range(leading):
        for j in range(leading):
            g[i][j] = lead_g[i][j]
    pairs=[]
    for start in range(leading,r,2):
        v,w=stars[start:start+2]
        base.require(v >= w >= 1 and 2*v <= t,"paired petals must be smaller")
        delta=2*a+F(2*(v+w-2),a)
        energy=F(4*(v-w)**2,a)
        mass=2*(v+w-1)
        base.require(delta <= 2*t and energy <= mass-2,"pair norm budget failed")
        g[start][start]=g[start+1][start+1]=F(a)
        g[start][start+1]=g[start+1][start]=F(-a)
        pairs.append({"stars":[v,w],"delta":str(delta),"empty_energy":str(energy),"nonempty_mass":mass})
    p=len(pairs)
    tail_mass=sum(pair['nonempty_mass'] for pair in pairs)
    leading_n=1+sum(2*v-1 for v in stars[:leading])
    if leading_mode.startswith("three_centered:"):
        beta=min(tail_mass+beta0,F(leading_n-2*t+2*p))
    else:
        delta0=leading*a+F(sum(2*v-2 for v in stars[:leading]),a)
        base.require(delta0 >= 2*t,"leading diagonal frame too small")
        beta=beta0+2*p
    base.require(beta > 0,"nonpositive global margin")
    return g,beta,{"leading_count":leading,"leading_mode":leading_mode,"leading_beta":str(beta0),
                   "paired_tail_count":p,"paired_tail_nonempty_mass":tail_mass,"tail_pairs":pairs,
                   "beta":str(beta),**small_lmi(stars,g,beta)}


def unique_cubes(orders):
    validate_orders(orders,unique=True)
    parts=[base.cube(a) for a in orders]
    stars=[p[2] for p in parts]
    t=stars[0]
    family,shifted,_,_=base.union_parts(parts,equal=False)
    n=len(family)
    g,beta,meta=unique_gram(stars)
    vertices=[(j,mask,len(part[0])-1) for j,part in enumerate(parts) for mask in part[0][1:]]
    c=[]
    for i,x,full_i in vertices:
        row=[]
        for j,y,full_j in vertices:
            if i == j:
                if x == y: value=F(t-1)
                elif x == full_i or y == full_j: value=F(-1)
                elif x ^ y == full_i: value=F(1+t*(2*stars[i]-t-2),t-1)
                else: value=F(-1)
            else:
                factor_i=F(1) if x == full_i else F(-1,t-1)
                factor_j=F(1) if y == full_j else F(-1,t-1)
                value=factor_i*factor_j*g[i][j]
            row.append(value)
        c.append(row)
    seed=base.lift(c,t)
    shifted_core=base.core(shifted,t)
    row_form=sum(sum(row) for row in shifted_core)
    expected_row_form=sum(v-1+(t-v)*(2*v-1) for v in stars)
    base.require(row_form == expected_row_form,"shifted constant form mismatch")
    # Reviewed8640 norm bound, extended to every shifted cube block.
    base.psd_rank([[2*t*int(i == j)-shifted_core[i][j] for j in range(n-1)] for i in range(n-1)])
    q_shift=[[sum(sum(row) for row in shifted_core)]+[-sum(row) for row in shifted_core]]
    q_shift += [[-sum(shifted_core[i])]+shifted_core[i][:] for i in range(n-1)]
    base.psd_rank([[(2*t+row_form)*int(i == j)-q_shift[i][j] for j in range(n)] for i in range(n)])
    z=max(F(0),F(2*t+row_form-n))
    epsilon=beta/(2*(beta+z))
    base.require(0 < epsilon <= F(1,2),"bad repair coefficient")
    mixed=[[ (1-epsilon)*seed[i][j]+epsilon*shifted[i][j] for j in range(n)] for i in range(n)]
    mixed_core=[[(1-epsilon)*c[i][j]+epsilon*shifted_core[i][j] for j in range(n-1)] for i in range(n-1)]
    base.require(base.lift(mixed_core,t) == mixed,"core/full mixtures disagree")
    meta.update(orders=list(orders),stars=stars,shifted_constant_form=expected_row_form,z=str(z),epsilon=str(epsilon),
                upper_gap_bound=str(beta/(2*(n-t))),lower_positive_gap_bound=str(epsilon*(t-stars[1])),
                forced_nullity=t)
    return (family,mixed,t,'unique_petals('+','.join(map(str,orders))+')'),seed,meta


def all_cubes(orders):
    validate_orders(orders)
    k=orders.count(orders[0])
    t=2**(orders[0]-1)
    if k == 1:
        part,seed,meta=unique_cubes(orders)
        meta.update(k=1,r=len(orders),assembly="unique_largest")
        return part,seed,meta
    packets=[]
    if k < len(orders):
        packet_orders=(orders[0],)+tuple(orders[k:])
        packet,_,packet_meta=unique_cubes(packet_orders)
        packets.append(packet)
    else:
        packet_orders=()
        packet_meta=None
        packets.append(base.cube(orders[0]))
    packets.extend(base.cube(orders[0]) for _ in range(k-1))
    part=base.union_parts(packets)
    gamma=base.quantitative_gap(packets,part[1],t)
    meta={"orders":list(orders),"r":len(orders),"k":k,"assembly":"equal_star_packets",
          "unique_packet_orders":list(packet_orders),"unique_packet_repair":packet_meta,
          "forced_nullity":k*t,"scaled_upper_gap":gamma}
    return part,None,meta


def run():
    coefficients,summary=three.sign_certificates()
    base.require(coefficients == json.loads(Path(__file__).with_name('MARGIN_COEFFICIENTS.json').read_text()),
                 "credited leading-three coefficient certificate mismatch")
    quadruples=[tuple(reversed(p)) for p in combinations_with_replacement(range(1,5),4)]
    fixtures=[(2,1),(3,1),(3,2,1),(4,2,1),(3,1,1,1,1),(5,4,3,2,1),(5,3,2,1,1),
              (4,3,2,2,1,1),(6,2,1,1,1,1),(5,4,3,2,2,1,1),
              (4,3,2,2,2,1,1,1),(3,2,1,1,1,1,1,1,1),
              (3,3,2,2,1,1,1,1,1,1),(3,)+(1,)*13,(3,2)+(1,)*13]
    entries=[]
    built={}
    for orders in quadruples+fixtures:
        part,seed,meta=all_cubes(orders)
        family,matrix,s,label=part
        checked=base.check(family,matrix,s)
        base.require(checked['lower_rank'] == len(family)-meta['forced_nullity'],"wrong maximal lower rank")
        base.require(checked['upper_rank'] == len(family)-1,"unit endpoint not simple")
        if seed is not None:
            seed_check=base.check(family,seed,s)
            three.full_margin(seed,s,F(meta['beta']))
            three.full_margin(matrix,s,F(meta['beta'])/2)
            # Separate original-index test of the positive lower eigenvalue gap.
            # L^2-gL>=0 is equivalent when L>=0; guard extra multiplication.
            gap_checked=len(family) <= 24
            if gap_checked:
                n=len(family)
                lower=[[(n-s)*matrix[i][j]+s*int(i == j) for j in range(n)] for i in range(n)]
                gap=F(meta['lower_positive_gap_bound'])
                polynomial=[[sum(lower[i][k]*lower[k][j] for k in range(n))-gap*lower[i][j]
                             for j in range(n)] for i in range(n)]
                base.psd_rank(polynomial)
            # General reviewed-bound interval and two-facet boundary example.
            if tuple(orders) == (3,1):
                base.require(F(meta['epsilon']) == F(1,12),"reviewed two-facet boundary coefficient")
            checked.update(seed_sha256=seed_check['matrix_sha256'],seed_lower_rank=seed_check['lower_rank'],
                           positive_lower_gap_checked=gap_checked)
        checked.update(label=label,**meta)
        entries.append(checked)
        built[tuple(orders)]=part
    products=[]
    p4=built[(2,1,1,1)]
    p5=all_cubes((2,1,1,1,1))[0]
    p_many=all_cubes((2,2,1,1,1))[0]
    for factors in [[p4,p4],[p4,p5],[p4,p_many]]:
        family,matrix,s,label=base.tensor_parts(factors)
        density=max(F(p[2],len(p[0])) for p in factors)
        eligible=[i for i,p in enumerate(factors) if F(p[2],len(p[0])) == density]
        forced=sum(len(factors[i][0])-base.check(*factors[i][:3])['lower_rank'] for i in eligible)
        checked=base.check(family,matrix,s)
        base.require(checked['lower_rank'] == len(family)-forced and checked['upper_rank'] == len(family)-1,
                     "tensor forced rank failed")
        checked.update(label=label,eligible_factors=eligible,forced_nullity=forced)
        products.append(checked)
    core_products=[]
    for factors in [[base.cube(1),p4],[base.cube(2),p4],
                    [base.cube(2),built[(3,2,1,1)]],
                    [base.cube(1),p4,all_cubes((1,1))[0]]]:
        family,matrix,s,label=base.tensor_parts(factors)
        c=len(factors[0][0]).bit_length()-1
        checked=base.check(family,matrix,s)
        base.require(2*s == len(family),"wrong common-core star")
        base.require(checked['lower_rank'] == checked['upper_rank'] == len(family)-2**(c-1),
                     "common-core endpoint ranks failed")
        checked.update(label=label,common_core_order=c)
        core_products.append(checked)
    controls=[]
    def reject(label,fn):
        base.expect_error(fn);controls.append(label)
    reject('unsorted_orders',lambda:all_cubes((1,3,2,1)))
    reject('zero_order',lambda:all_cubes((3,2,1,0)))
    reject('noninteger_order',lambda:all_cubes((3,2,F(3,2),1)))
    reject('literal_size_guard',lambda:all_cubes((6,6,1,1)))
    reject('missing_unique_maximum',lambda:unique_cubes((3,3,1,1)))
    reject('nondyadic_stars',lambda:unique_gram([7,3,2,1]))
    reject('tail_exceeds_half',lambda:unique_gram([8,4,8,1]))
    stars=[8,4,2,1]
    g,beta,_=unique_gram(stars)
    reject('false_small_margin',lambda:small_lmi(stars,g,F(25)))
    bad=[row[:] for row in g];bad[0][0]+=1
    reject('corrupt_Gram_diagonal',lambda:small_lmi(stars,bad,beta))
    f,m,s,_=p4
    bad=[row[:] for row in m];bad[1][1]=1
    reject('corrupt_full_support',lambda:base.check(f,bad,s))
    reject('false_full_margin',lambda:three.full_margin(m,s,F(100)))
    reject('wrong_star',lambda:base.check(f,m,s+1))
    result={'claim_status':'author-checked unformalized arbitrary-petal norm/frame proof; credited leading-three exact signs',
            'leading_three_sign_certificate':summary,'cube_unions':entries,'products':products,
            'common_core_products':core_products,'coverage':{'complete_sorted_four_orders_1_to_4':len(quadruples),
            'additional_union_fixtures':len(fixtures),'largest_literal_matrix_order':max(e['N'] for e in entries+products+core_products),
            'largest_petal_count':max(e['r'] for e in entries)},'rejection_controls':controls}
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',type=Path)
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=run()
    encoded=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    if args.write:args.write.write_bytes(encoded)
    if args.check:base.require(json.loads(args.check.read_text()) == result,'result fixture mismatch')
    print(json.dumps({'ok':True,'coverage':result['coverage'],'rejection_controls':len(result['rejection_controls']),
                      'results_sha256':sha256(encoded).hexdigest()},sort_keys=True))


if __name__ == '__main__':main()
