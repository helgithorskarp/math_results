#!/usr/bin/env python3
"""Independent matrix/union-find checks; imports no producer or interface."""
import argparse,json,math
from itertools import combinations
from pathlib import Path


def need(ok,message):
    if not ok:raise ValueError(message)


def partition(n,links):
    parent=list(range(n))
    def root(v):
        while parent[v]!=v:
            parent[v]=parent[parent[v]];v=parent[v]
        return v
    for u,v in links:parent[root(u)]=root(v)
    groups={}
    for v in range(n):groups.setdefault(root(v),[]).append(v)
    return sorted(groups.values())


def template_partition():
    pairs=list(combinations(range(53),2));number={p:i for i,p in enumerate(pairs)}
    permutation=list(range(53))
    for cycle in (list(range(26)),list(range(26,52))):
        for i,v in enumerate(cycle):permutation[v]=cycle[(i+1)%len(cycle)]
    links=[(i,number[tuple(sorted((permutation[u],permutation[v])))]) for i,(u,v) in enumerate(pairs)]
    groups=partition(len(pairs),links)
    return permutation,[[pairs[i] for i in row] for row in groups]


def check_certificate(c):
    need(c['schema']=='r55-orbit-dense-deletion-v1','certificate schema')
    need(all(53%d for d in range(2,math.isqrt(53)+1)),'prime53')
    matrix=[[int(u!=v and pow((v-u)%53,26,53)==1) for v in range(53)] for u in range(53)]
    need(all(matrix[u][v]==matrix[v][u] for u,v in combinations(range(53),2)), 'Paley symmetry')
    need(all(sum(row)==26 for row in matrix),'Paley degree')
    paley=c['paley53'];seed=paley['seed']
    need(len(seed)==5 and seed==sorted(set(seed)) and all(type(v) is int and 0<=v<53 for v in seed), 'seed five')
    need(paley['color']=='red' and all(matrix[u][v] for u,v in combinations(seed,2)), 'seed clique')
    translations=sorted({tuple(sorted((t+v)%53 for v in seed)) for t in range(53)})
    need(len(translations)==53,'translation orbit size')
    need(paley['translates']==[list(row) for row in translations], 'complete translate list')
    multiplicity=[0]*53
    for row in translations:
        need(all(matrix[u][v] for u,v in combinations(row,2)), 'translated clique')
        for v in row:multiplicity[v]+=1
    need(multiplicity==[5]*53 and paley['vertex_incidence']==multiplicity,'uniform cover incidence')
    expected={'retained_vertex_count':43,'deleted_vertex_count':10,'cover_rows':53,
              'maximum_rows_hit_by_deletions':50,'minimum_surviving_rows':3,
              'farkas_left':215,'farkas_right':212,'farkas_gap':3}
    need(all(paley[k]==v for k,v in expected.items()),'Paley integer certificate')
    need(5*43>4*53,'strict Farkas contradiction')
    permutation,classes=template_partition();two=c['two_orbit53']
    need(two['generator']==permutation,'two-orbit generator')
    vertex_partition=partition(53,[(v,permutation[v]) for v in range(53)])
    need(two['vertex_orbits']==vertex_partition==[list(range(26)),list(range(26,52)),[52]],'vertex orbit partition')
    need(len(classes)==54 and sum(map(len,classes))==1378, 'complete edge partition')
    class_table={row[0]:len(row) for row in classes}
    records=two['edge_classes']
    need(len(records)==54 and [x['index'] for x in records]==list(range(54)), 'edge class labels')
    expected_reps=[(0,i) for i in range(1,14)]+[(26,i) for i in range(27,40)]+[(0,i) for i in range(26,52)]+[(0,52),(26,52)]
    need([tuple(r['representative']) for r in records]==expected_reps, 'template representatives')
    need(len(set(expected_reps))==54 and set(expected_reps)==set(class_table), 'all template edge orbits')
    need(all(r['size']==class_table[tuple(r['representative'])] for r in records),'template orbit size')
    need(two['selected_per_orbit']==[21,21,1] and two['deleted_per_orbit']==[5,5,0], 'retained orbit profile')
    need(all(5*k>4*len(o) for k,o in zip(two['selected_per_orbit'],vertex_partition)), 'strict orbit density')
    need(two['five_seed_translate_multiplicity']==26 and two['maximum_total_deleted_incidence']==25 and
         two['minimum_surviving_translate_multiplicity']==1,'two-orbit count certificate')
    # Independent binomial evaluation, without math.comb or a producer import.
    choose=lambda n,k:math.factorial(n)//math.factorial(k)//math.factorial(n-k)
    inventory={'paley53':{'ambient_order':53,'deleted':10,'physical_subset_jobs':choose(53,10),'surviving_good43_jobs':0},
               'two_orbit53':{'ambient_order':53,'ambient_edge_orbit_bits':54,'deletion_pairs':choose(26,5)**2,
                              'physical_parameter_jobs':2**54*choose(26,5)**2,'surviving_good43_jobs':0,
                              'count_convention':'parameter jobs; resulting labeled or unlabeled graphs can coincide'},
               'not_multiplied_by_h3887':True,'whole_q10_task_decided':False,'target43_found':False}
    need(c['inventory']==inventory,'physical job inventory')
    return {'status':'CHECKED_COMPLETE_ORBIT_DENSE_DELETION_FAMILY_CERTIFICATES',
            'paley_cliques_checked':53,'paley_literal_pairs_checked':530,'paley_incidence_gap':3,
            'paley_physical_jobs_excluded':choose(53,10),'two_orbit_edge_classes':54,
            'two_orbit_pairs_covered':1378,'two_orbit_physical_parameter_jobs_excluded':2**54*choose(26,5)**2,
            'general_family_premise':'Angeltveit-McKay R(5,5)<=46 imported',
            'paley_finite_certificate_uses_ramsey_bound':False,'target43_found':False}


def check_physical(data,c):
    n=data['n'];need(type(n) is int and 46<=n<=53,'ambient order')
    matrix=[[0]*n for _ in range(n)];seen=set()
    for edge in data['red_edges']:
        need(isinstance(edge,list) and len(edge)==2,'edge pair')
        u,v=edge;need(type(u) is int and type(v) is int and 0<=u<v<n,'edge endpoints')
        need((u,v) not in seen,'duplicate edge');seen.add((u,v));matrix[u][v]=matrix[v][u]=1
    selected=data['selected'];need(isinstance(selected,list) and len(selected)==43 and
                                  all(type(v) is int and 0<=v<n for v in selected) and selected==sorted(set(selected)),'selected 43-set')
    permutations=data['generators'];need(isinstance(permutations,list) and permutations,'generators')
    for perm in permutations:
        need(len(perm)==n and all(type(v) is int for v in perm) and sorted(perm)==list(range(n)), 'generator permutation')
        need(all(matrix[u][v]==matrix[perm[u]][perm[v]] for u,v in combinations(range(n),2)), 'generator is not automorphism')
    orbits=partition(n,[(v,p[v]) for p in permutations for v in range(n)])
    profile=[{'orbit':o,'retained':sum(v in selected for v in o),'size':len(o)} for o in orbits]
    need(c['orbit_profile']==profile,'physical orbit profile')
    strict=all(5*x['retained']>4*x['size'] for x in profile)
    if not strict:
        need(c=={'status':'OUTSIDE_DECLARED_ORBIT_DENSE_FAMILY','orbit_profile':profile,'ramsey_verdict':None},'outside-family verdict')
        return {'status':'CHECKED_OUTSIDE_DECLARED_FAMILY','ramsey_verdict':None}
    need(c['status']=='CERTIFIED_MONOCHROMATIC_FIVE_IN_PHYSICAL43' and c['ambient_order']==n,'physical certificate status')
    seed=c['seed'];need(len(seed)==5 and seed==sorted(set(seed)) and all(type(v) is int and 0<=v<n for v in seed),'seed five')
    need(c['color'] in ('red','blue'),'certificate color');color=int(c['color']=='red')
    need(all(matrix[u][v]==color for u,v in combinations(seed,2)),'physical seed monochromatic')
    denominator=math.lcm(*(len(o) for o in orbits));numerator=0
    for o in orbits:
        numerator+=sum(v in seed for v in o)*sum(v not in selected for v in o)*(denominator//len(o))
    factor=math.gcd(numerator,denominator)
    need(c['expected_deleted_intersection']==[numerator//factor,denominator//factor] and numerator<denominator,'exact deletion average')
    mapped=list(seed)
    for step in c['generator_word']:
        need(type(step) is int and 0<=step<len(permutations),'generator word')
        mapped=[permutations[step][v] for v in mapped]
    need(sorted(mapped)==c['ambient_witness'],'translated witness')
    witness=c['ambient_witness'];need(set(witness)<=set(selected),'witness survives deletion')
    physical=c['physical_witness'];need(len(physical)==5 and physical==sorted(set(physical)) and all(type(v) is int and 0<=v<43 for v in physical),'physical five indices')
    need([selected[v] for v in physical]==witness,'physical relabeling')
    need(all(matrix[selected[u]][selected[v]]==color for u,v in combinations(physical,2)),'literal physical pair check')
    need(c['target43_found'] is False,'no target claim')
    return {'status':'CHECKED_LITERAL_MONOCHROMATIC_FIVE','physical_pairs_checked':10,'color':c['color']}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('certificate');parser.add_argument('--input');args=parser.parse_args()
    c=json.loads(Path(args.certificate).read_text())
    result=check_physical(json.loads(Path(args.input).read_text()),c) if args.input else check_certificate(c)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
