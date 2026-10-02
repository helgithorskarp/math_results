"""Independent exhaustive unit adjacency check and literal cut verification.

No import of cuts.py or produce.py. All possible simple graphs induced
on ordinary units are enumerated; external matching remains a relaxation.
"""
import itertools
import time

def need(condition,message):
    if not condition:raise ValueError(message)

def check_one(vertices,certificate):
    unit=[i for i,r in enumerate(vertices) if r['e']==0]
    A=[i for i in unit if not vertices[i]['eligible']]
    C=[i for i,r in enumerate(vertices) if r['e']>0 and not r['eligible']]
    demands=[sum(r['ss_hist']) for r in vertices]
    D=sum(demands[i] for i in unit)
    cap=sum(vertices[i]['ss_hist'][0] for i in C)
    endpoint_upper=sum(min(demands[i],len(A)-1) for i in A)
    need((certificate['unit_demand'],certificate['internal_upper'],certificate['external_upper'])
         ==(D,endpoint_upper,cap),'certificate endpoint totals')
    pairs=list(itertools.combinations(A,2))
    need(len(pairs)<=15,'INCOMPLETE independent graph guard; no scope escalation')
    examined=0;admissible=0;maximum=0;residuals=set();started=time.monotonic()
    # Explicit adjacency subsets; degree is rebuilt from the chosen edges.
    # Eligible units have no unit neighbors in either orientation.
    for bits in range(1<<len(pairs)):
        examined+=1
        if time.monotonic()-started>10:
            raise RuntimeError('INCOMPLETE fixed unit-graph time guard; no absence')
        degree={i:0 for i in A}
        for bit,(i,j) in enumerate(pairs):
            if bits&(1<<bit):degree[i]+=1;degree[j]+=1
        if any(degree[i]>demands[i] for i in A):continue
        total=sum(degree.values());maximum=max(maximum,total)
        residual=D-total
        if residual<=cap:
            admissible+=1;residuals.add(residual)
    need(maximum<=endpoint_upper,'finite internal endpoints exceed stated upper bound')
    if certificate['kind']=='unit_capacity':
        need(D>endpoint_upper+cap and admissible==0,'capacity exclusion does not hold')
    elif certificate['kind']=='closed_partition':
        inside=certificate['inside'];outside=certificate['outside'];root=certificate['root']
        need(len(set(inside))==len(inside) and len(set(outside))==len(outside),'repeated cut point')
        need(set(inside).isdisjoint(outside) and set(inside)|set(outside)==set(range(len(vertices))),'complete disjoint cut')
        need(root in inside and outside and vertices[root]['k']==0,'actual radius root and nonempty outside')
        equality=D==endpoint_upper+cap
        need(certificate['capacity_equality']==equality,'false saturation declaration')
        if equality:need(not admissible or residuals=={cap},'ineligible capacity not entirely consumed')
        # Check each crossing pair directly, not by repeating a BFS.
        # If no induced-unit graph survives, a stronger endpoint exclusion
        # already holds. The finite crossing check still verifies the cut.
        for i,j in itertools.product(inside,outside):
            if (i in unit and vertices[j]['eligible']) or (j in unit and vertices[i]['eligible']):continue
            for colour in range(5):
                if not (vertices[i]['ss_hist'][colour] and vertices[j]['ss_hist'][colour]):continue
                consumed=(equality and colour==0 and i not in unit and j not in unit
                          and (i in C or j in C))
                need(consumed,'actual permitted deficit may cross the alleged closed cut')
    else:raise ValueError('unsupported physical certificate kind')
    return dict(examined_unit_graphs=examined,unit_degree_admissible_maximum=maximum,
                externally_relaxed_unit_graphs=admissible,residual_endpoint_demands=sorted(residuals))

def verify_all(inventory,certificate):
    need(len(inventory['branches'])==15,'full15 arithmetic branches')
    need(sum(len(b['templates']) for b in inventory['branches'])==47,'full47 raw populations')
    expected=[(b,t) for b in inventory['branches'] for t in b['templates'] if not t['failures']]
    need(len(expected)==len(certificate['records'])==18,'all18 old survivors require individual physical cuts')
    details=[]
    for (branch,template),record in zip(expected,certificate['records']):
        need(record['branch']==[branch[k] for k in ('Q','T','X','tau')],'branch correspondence')
        need(record['population']==template['population'],'complete population correspondence')
        need(record['branch'][1:]==[0,0,0],'zero excess/triple hypotheses established, not assumed')
        vertices=[inventory['types'][i] for i,c in template['population'] for _ in range(c)]
        need(len(vertices)==14 and all(r['ss_excess']==0 for r in vertices),'complete physical support degree rows')
        details.append(check_one(vertices,record))
    return dict(status='PASS',branches=15,raw_populations=47,prior_test_survivors=18,
                capacity_certificates=sum(r['kind']=='unit_capacity' for r in certificate['records']),
                closed_partition_certificates=sum(r['kind']=='closed_partition' for r in certificate['records']),
                examined_unit_graphs=sum(d['examined_unit_graphs'] for d in details),
                details=details,four_hub_pair_total_lower_bound=21,
                independent_mathematical_review=False,ordinary_bridges_formalized=False)
