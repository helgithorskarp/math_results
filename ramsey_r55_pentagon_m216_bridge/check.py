"""Literal exhaustive kernel and exact cancellation; imports no producer."""
from itertools import combinations,product
import hashlib,json
from pathlib import Path


def need(ok,message):
    if not ok:raise ValueError(message)


def verify(cert):
    cycle={frozenset((i,(i+1)%5)) for i in range(5)}
    a=[[False]*20 for _ in range(20)]
    for u,v in combinations(range(20),2):
        i,j=u//5,v//5
        a[u][v]=a[v][u]=(frozenset((u%5,v%5)) in cycle if i==j else (i,j) in ((0,1),(1,2),(2,3)))
    need(cert['schema']==1 and cert['profile']==[19]*2+[20]*5+[21]*36,'profile identity')
    need(cert['core_order']==20 and cert['core_red_edges']==[[u,v] for u,v in combinations(range(20),2) if a[u][v]],'core identity')
    need(cert['free_physical_pairs_before_degrees']==903-190,'physical pair scope')
    for q in combinations(range(20),5):need(len({a[u][v] for u,v in combinations(q,2)})==2,'core five-set')
    qs=[[],[]]
    for q in combinations(range(20),4):
        colors={a[u][v] for u,v in combinations(q,2)}
        if len(colors)==1:qs[int(next(iter(colors)))].append(sum(1<<v for v in q))
    models=[]
    for m in range(1<<20):
        if any(m&q==q for q in qs[1]):continue
        if any(m&q==0 for q in qs[0]):continue
        models.append(m)
    expected=[];tables=[[],[],[],[]]
    for m in range(32):
        r=any(a[u][v] and m>>u&1 and m>>v&1 for u,v in combinations(range(5),2))
        b=any(not a[u][v] and not(m>>u&1) and not(m>>v&1) for u,v in combinations(range(5),2))
        tables[int(r)+2*int(b)].append(m)
    need(tables==cert['bag_status_masks'],'literal bag table')
    for blocks in product(tables[1],tables[2],tables[2],tables[1]):
        expected.append(sum(m<<(5*i) for i,m in enumerate(blocks)))
    need(models==sorted(expected),'entrywise complete star sets')
    need(cert['status_words_checked']==256 and cert['feasible_positive_words']==[[1,2,2,1]],'activity word scope')
    need(len(models)==cert['admissible_stars'],'star count')
    digest=hashlib.sha256(''.join(f'{m}\n' for m in models).encode()).hexdigest()
    need(digest==cert['star_set_sha256'],'star digest')
    edge_types=[{i,(i+1)%5} for i in range(5)]
    need(cert['edge_classes']==[[i,(i+1)%5] for i in range(5)],'class identity')
    need(len(cert['class_pair_supports'])==5,'all five class pairs')
    for i,record in enumerate(cert['class_pair_supports']):
        u,v=record['classes'];center=record['common_blue'];p,q=record['common_red_edge']
        need((u,v)==(i,(i+1)%5),'class pair order')
        need(edge_types[u]&edge_types[v]=={center},'common blue vertex')
        need(set(range(5))-(edge_types[u]|edge_types[v])=={p,q} and a[p][q],'common red edge')
    need(all(sum(a[v])==7 for v in range(5)) and cert['end_bag_core_degree']==7,'end-bag degree')
    need(cert['outside_order']==23 and cert['bag_degree_sum_cap']==5*max(cert['profile']),'degree ceiling')
    lower=5*23-(cert['bag_degree_sum_cap']-5*7)
    need(cert['blue_incidence_minimum']==lower==45,'physical blue incidence identity')
    need(cert['ordinary_star_minimum']==lower-23==22 and cert['small_ramsey_threshold']==9,'pigeonhole inputs')
    total=[0]*5;rhs=0
    need(len(cert['farkas_rows'])==6 and cert['farkas_multipliers']==[1,1,1,1,1,2],'multiplier scope')
    for i,(row,mult) in enumerate(zip(cert['farkas_rows'],cert['farkas_multipliers'])):
        expected_a=[int(j==i or j==(i+1)%5) for j in range(5)] if i<5 else [-1]*5
        need(row=={'a':expected_a,'rhs':8 if i<5 else -22},'literal count row')
        total=[x+mult*y for x,y in zip(total,row['a'])];rhs+=mult*row['rhs']
    need(total==[0]*5 and rhs==cert['farkas_rhs']==-4,'exact contradiction')
    # Independent occupancy enumeration of all possible counts under pair caps.
    maximum=-1;winners=[];feasible=0
    for counts in product(range(9),repeat=5):
        if any(counts[i]+counts[(i+1)%5]>8 for i in range(5)):continue
        feasible+=1;s=sum(counts)
        if s>maximum:maximum=s;winners=[list(counts)]
        elif s==maximum:winners.append(list(counts))
    need(maximum==20 and winners==[[4]*5],'occupancy bound')
    return {'status':'VERIFIED_PENTAGON_LIVE_PROFILE_KERNEL','stars_examined':1<<20,
            'admissible_stars':len(models),'rejected_stars':(1<<20)-len(models),
            'core_four_cliques_blue_red':list(map(len,qs)),'star_set_sha256':digest,
            'core_five_sets_checked':15504,'occupancy_tuples_examined':9**5,
            'feasible_occupancy_tuples':feasible,'occupancy_maximum':maximum,
            'ordinary_stars_required':22,'farkas_rhs':rhs}

if __name__=='__main__':print(json.dumps(verify(json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())),indent=2))
