"""Physical and cut-scope controls, including all small permitted role graphs."""
import copy
import itertools
import produce
import verify
import cuts
import verify_cuts

def need(condition,message):
    if not condition:raise ValueError(message)

def rejects(function,*args):
    try:function(*args)
    except ValueError:return
    raise ValueError('semantic damage was accepted')

def run(data,inventory,certificate):
    checks=[]
    for damage in ('missing_quadruple','repeated_quadruple','repeated_pair','out_of_domain'):
        bad=copy.deepcopy(data)
        if damage=='missing_quadruple':bad['stars'][0].pop()
        elif damage=='repeated_quadruple':bad['stars'][0][1]=bad['stars'][0][0][:]
        elif damage=='out_of_domain':bad['stars'][0][0][0]=17
        else:
            p,q=bad['stars'][0][0][:2]
            other=[v for v in range(17) if v not in (p,q)]
            bad['stars'][0][1]=[p,q]+other[:2]
        rejects(produce.rows_from_data,bad);rejects(verify.literal_rows,bad)
        checks.append('physical_'+damage)
    transported=0
    for mapping in ([16-p for p in range(17)],[(3*p+7)%17 for p in range(17)]):
        moved=copy.deepcopy(data)
        moved['stars']=[[[mapping[p] for p in reversed(word)] for word in reversed(star)] for star in data['stars']]
        a=produce.rows_from_data(moved);b=verify.literal_rows(moved)
        need(produce.canonical(a)==verify.CANON(b),'actual point transport differs')
        need(produce.canonical(produce.inventories(a))==verify.CANON(inventory),'transport changes complete inventory')
        transported+=len(a)
    checks.append('two_actual_point_bijections_on_all23_stars_and426_marks')
    rows=produce.rows_from_data(data)
    need(any(r['e']==4 and r['h']==1 for r in rows),'genuine missing-link-point marks omitted')
    failures=[r for r in rows if r['margin']<0]
    need(len(failures)==8 and all(r['k']==5 and r['margin']==-3 for r in failures),'genuine five-hub scope failures omitted')
    checks+=['retain_actual_e4_marks','retain_all_eight_actual_k5_failures']
    for damage in ('missing_record','wrong_population','false_capacity','false_equality','missing_outside_point','repeated_inside_point','root_with_deficient_hub'):
        bad=copy.deepcopy(certificate)
        cap=next(r for r in bad['records'] if r['kind']=='unit_capacity')
        closed=next(r for r in bad['records'] if r['kind']=='closed_partition')
        if damage=='missing_record':bad['records'].pop()
        elif damage=='wrong_population':cap['population'][0][1]+=1
        elif damage=='false_capacity':cap['external_upper']+=10
        elif damage=='false_equality':closed['capacity_equality']=not closed['capacity_equality']
        elif damage=='missing_outside_point':closed['outside'].pop()
        elif damage=='repeated_inside_point':closed['inside'].append(closed['inside'][0])
        else:
            vertices=cuts.expand(inventory['types'],closed['population'])
            closed['root']=next(i for i in closed['inside'] if vertices[i]['k']>0)
        rejects(verify_cuts.verify_all,inventory,bad);checks.append('cut_damage_'+damage)
    # Enumerate every permitted graph for three ordinary units, one eligible
    # unit, one ineligible nonunit, and one eligible nonunit. These are
    # endpoint-algebra controls, not stars or codes.
    units={0,1,2,3};eligible={3,5};C={4}
    pairs=[(i,j) for i,j in itertools.combinations(range(6),2)
           if not ((i in units and j in eligible) or (j in units and i in eligible))]
    graphs=0;equality_graphs=0
    for bits in range(1<<len(pairs)):
        adjacency=[set() for _ in range(6)]
        for b,(i,j) in enumerate(pairs):
            if bits&(1<<b):adjacency[i].add(j);adjacency[j].add(i)
        vertices=[dict(e=0 if i in units else 1,eligible=i in eligible,k=1,
                       ss_hist=[len(adjacency[i]),0,0,0,0]) for i in range(6)]
        U,A,external,D,I,cap=cuts.endpoints(vertices)
        need(D<=I+cap,'endpoint upper bound fails on a literal permitted graph')
        if D==I+cap:
            equality_graphs+=1
            need(all(adjacency[i]<=units for i in C),'equality leaves unused ineligible colour-one endpoints')
        graphs+=1
    checks.append('all256_small_literal_permitted_role_graphs_and_equality_cuts')
    need(graphs==256,'small graph coverage changed')
    # Saturation consumes only colour one. An actual colour-two candidate
    # between nonunits must survive and invalidate an alleged closed cut.
    colored=[dict(e=0,eligible=False,k=0,ss_hist=[1,0,0,0,0]),
             dict(e=1,eligible=False,k=1,ss_hist=[1,1,0,0,0]),
             dict(e=1,eligible=True,k=1,ss_hist=[0,1,0,0,0])]
    U,A,C,D,I,cap=cuts.endpoints(colored)
    need(D==I+cap and cuts.potential_colours(colored,1,2,U,C,True)==[1],'cut improperly consumes higher deficit colours')
    false_cut=dict(kind='closed_partition',root=0,inside=[0,1],outside=[2],
                   unit_demand=D,internal_upper=I,external_upper=cap,capacity_equality=True)
    rejects(verify_cuts.check_one,colored,false_cut)
    checks.append('higher_deficit_colour_retained_at_unit_capacity_equality')
    return dict(status='PASS',checks=checks,checks_count=len(checks),
                transported_physical_rows=transported,small_permitted_graphs=graphs,
                small_equality_graphs=equality_graphs,
                graph_controls_are_not_packing_realizations=True)
