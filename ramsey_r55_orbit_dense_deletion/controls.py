#!/usr/bin/env python3
"""Exact small orbit-cover checks and adversarial receiver controls."""
import copy,json
from itertools import combinations
from pathlib import Path
import family,interface,check

ROOT=Path(__file__).resolve().parent


def rejects(fn,fragment):
    try:fn()
    except ValueError as exc:
        if fragment not in str(exc):raise ValueError('wrong rejection: '+str(exc))
        return 1
    raise ValueError('accepted corrupt control: '+fragment)


def combinatorial_controls():
    count=0
    # All five-seeds in two 6-cycles and a fixed point; delete one point per
    # 6-cycle. Test actual set avoidance, not a restatement of the average.
    permutation=[(v//6)*6+(v+1)%6 if v<12 else 12 for v in range(13)]
    for seed in combinations(range(13),5):
        translates=[];current=seed
        for _ in range(6):
            translates.append(set(current));current=tuple(permutation[v] for v in current)
        for a in range(6):
            for b in range(6,12):
                if not any(not {a,b}.intersection(t) for t in translates):raise ValueError('small orbit avoidance')
                count+=1
    # Equality cannot replace strictness for an arbitrary given five-orbit.
    seed=set(range(5));retained=set(range(4))
    if any({(v+t)%5 for v in seed}<=retained for t in range(5)):
        raise ValueError('strict boundary control')
    return count


def main():
    certificate=json.loads((ROOT/'CERTIFICATE.json').read_text());check.check_certificate(certificate)
    certificate_bad=0
    corruptions=[('complete translate list',lambda c:c['paley53']['translates'].pop()),
                 ('uniform cover incidence',lambda c:c['paley53']['vertex_incidence'].__setitem__(0,4)),
                 ('Paley integer certificate',lambda c:c['paley53'].__setitem__('farkas_gap',2)),
                 ('template orbit size',lambda c:c['two_orbit53']['edge_classes'][0].__setitem__('size',25)),
                 ('template representatives',lambda c:c['two_orbit53']['edge_classes'][0].__setitem__('representative',[0,2])),
                 ('physical job inventory',lambda c:c['inventory']['two_orbit53'].__setitem__('physical_parameter_jobs',1))]
    for message,mutate in corruptions:
        bad=copy.deepcopy(certificate);mutate(bad);certificate_bad+=rejects(lambda:check.check_certificate(bad),message)
    permutation,classes=check.template_partition()
    independent_index={}
    labels={tuple(r['representative']):r['index'] for r in certificate['two_orbit53']['edge_classes']}
    for row in classes:
        for pair in row:independent_index[pair]=labels[row[0]]
    for pair,index in independent_index.items():
        if family.two_orbit_index(*pair)!=index:raise ValueError('template all-pair bridge')
    # Basis assignments audit the template's physical output, including all
    # antipodal edge orbits and the fixed vertex; no 2^54 enumeration is needed.
    for i in range(54):
        data=family.two_orbit(1<<i,list(range(5)),list(range(5)))
        wanted={pair for pair,index in independent_index.items() if index==i}
        if set(map(tuple,data['red_edges']))!=wanted:raise ValueError('template basis assignment')
    data=family.paley53(list(range(10)));cert=interface.certify(data);check.check_physical(data,cert)
    invalid_inputs=0
    for label,mutate in [('generator permutation',lambda d:d['generators'][0].__setitem__(0,d['generators'][0][1])),
                         ('generator is not automorphism',lambda d:d['red_edges'].pop()),
                         ('duplicate edge',lambda d:d['red_edges'].append(d['red_edges'][0])),
                         ('edge endpoints',lambda d:d['red_edges'].__setitem__(0,[0,0])),
                         ('selected 43-set',lambda d:d['selected'].pop())]:
        bad=copy.deepcopy(data);mutate(bad)
        invalid_inputs+=rejects(lambda:interface.certify(bad),label)
        invalid_inputs+=rejects(lambda:check.check_physical(bad,cert),label)
    physical_bad=0
    for label,mutate in [('physical seed monochromatic',lambda c:c.__setitem__('color','blue')),
                         ('translated witness',lambda c:c['ambient_witness'].__setitem__(0,0)),
                         ('exact deletion average',lambda c:c.__setitem__('expected_deleted_intersection',[1,1])),
                         ('physical relabeling',lambda c:c['physical_witness'].__setitem__(4,c['physical_witness'][4]+1)),
                         ('physical certificate status',lambda c:c.__setitem__('status','SAT'))]:
        bad=copy.deepcopy(cert);mutate(bad)
        physical_bad+=rejects(lambda:check.check_physical(data,bad),label)
    # Keep 20 vertices of the first 26-cycle and 22 of the second: 43 total,
    # but the first orbit violates strict density. No Ramsey verdict is allowed.
    outside=family.two_orbit(0x123456789abcde,list(range(5)),list(range(5)))
    outside['selected']=[v for v in range(53) if v not in set(range(6))|set(range(26,30))]
    out=interface.certify(outside)
    if check.check_physical(outside,out)!={'status':'CHECKED_OUTSIDE_DECLARED_FAMILY','ramsey_verdict':None}:
        raise ValueError('outside-family receiver')
    order_controls=0
    for n in range(46,54):
        for red in (False,True):
            example={'n':n,'red_edges':[list(e) for e in combinations(range(n),2)] if red else [],
                     'generators':[[(v+1)%n for v in range(n)]],
                     'selected':list(range(n-43,n))}
            check.check_physical(example,interface.certify(example));order_controls+=1
    # A nontransitive, nonabelian subgroup: S47 on a red clique, one fixed
    # isolated vertex. Only the supplied generators are certified.
    cycle=list(range(1,47))+[0,47];swap=list(range(48));swap[0],swap[1]=swap[1],swap[0]
    example={'n':48,'red_edges':[list(e) for e in combinations(range(47),2)],
             'generators':[cycle,swap],'selected':list(range(5,48))}
    check.check_physical(example,interface.certify(example))
    result={'status':'PASSED_ORBIT_DELETION_CONTROLS','small_seed_deletion_pairs':combinatorial_controls(),
            'strict_equality_counterexample_checked':True,'template_all_pairs_checked':len(independent_index),
            'template_basis_assignments_checked':54,'rejected_global_certificate_corruptions':certificate_bad,
            'rejected_invalid_inputs_across_two_implementations':invalid_inputs,
            'rejected_physical_certificate_corruptions':physical_bad,'outside_family_has_no_ramsey_verdict':True}
    result.update(ambient_order_color_controls=order_controls,nonabelian_multiorbit_control=True)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
