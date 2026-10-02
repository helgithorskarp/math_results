"""Independent positive tail and complete original phase controls."""
from argparse import ArgumentParser
import json
from math import gcd
from pathlib import Path
HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise RuntimeError(message)

def compute(f):
    need(set(f)=={'schema','target_t','classes','tail_target_size','first_stage_witness_asserted','full_15120_cover_asserted'},'fixture fields')
    need(f['schema']==1 and f['tail_target_size']==82 and f['first_stage_witness_asserted'] is False and f['full_15120_cover_asserted'] is False,'fixture scope')
    K=set(f['target_t']);expected={t for t in range(180) if t%9!=6 and (t%3==1 or (t%2==0 and t%5==0 and t%3!=1) or t%30==26 or t%90==2 or t in (8,68,128,44))};need(K==expected,'positive fixture target definition');need(len(K)==len(f['target_t'])==82 and all(type(t) is int and 0<=t<180 and t%9!=6 for t in K),'physical tail target')
    rows=f['classes'];need(len(rows)==29 and all(type(a) is int and type(m) is int and 0<=a<m for a,m in rows),'tail class phases')
    moduli=[m for a,m in rows];need(sorted(moduli)==[7*d for d in range(2,721) if 720%d==0],'all29 original moduli')
    demand={x for x in range(5040) if x%4==0 and (x%720)//4 in K}
    need(len(demand)==574 and all(any(x%m==a for a,m in rows) for x in demand),'positive physical seven-copy coverage')
    shared={t for t in range(180) if t%9!=6 and all(any(x%m==a for a,m in rows) for x in range(4*t,5040,720))}
    need(shared==K,'positive fixture shared support is not exactly the specified82 points')
    need({t for t in range(180) if t%3==1}<=K,'positive ternary block')
    need(sum(t%2==0 for t in K)==52 and sum(t%2==1 for t in K)==30,'positive eight-halves')
    g=720
    x0=4*min(K)
    for t in K:g=gcd(g,4*t-x0)
    need(g==4,'positive difference gcd')
    # Nonempty strict union loss on a representative equality state.
    S={t for t in range(180) if t%9!=6};A={t for t in S if t%3==1};B={t for t in S if t%2==0};C={t for t in S if t%5==0};U=A|B|C
    V={t for t in S if t%9==1};W={t for t in S if t%4==0};Q=[B]+[A|C]*3+[set()]
    weight={t:sum(t in q for q in Q)+3*(t in V)+(t in W) for t in S}
    best=sorted(S,key=lambda t:(-weight[t],t))[:111]
    need(sum(weight[t] for t in best)==411 and set(best)<=U and A|W<=set(best),'relaxation equality positive control')
    physical=[{x for x in range(s,5040,7) if x%4==0 and (x%720)//4 in H} for s,H in enumerate(Q)]
    extra=[{x for x in range(4,5040,7) if x%4==0 and (x%720)//4 in H} for H in ({t for t in S if t%9==1},{t for t in S if t%9==4},{t for t in S if t%9==7},W)]
    need(sum(len(x) for x in extra)==100 and len(set().union(*extra))==85,'physical relaxed/actual loss positive control')
    # Exact ORIGINAL first-stage group bound for this fixed template.
    residual={x for x in range(720) if x%8!=5 and x%9!=6 and x%18!=3 and x not in {4*t for t in K}}
    pairs=((10,18),(12,15),(16,20),(24,30),(36,40),(45,48),(60,72))
    labels=[m for m in range(8,721) if 720%m==0 and m not in (8,9)]
    singles=sorted(set(labels)-{m for pair in pairs for m in pair})
    need(len(labels)==22 and len(singles)==8,'template first ORIGINAL inventory')
    masks={m:[set(range(a,720,m))&residual for a in range(m)] for m in labels}
    capacities=[max(len(u|v) for u in masks[m] for v in masks[n]) for m,n in pairs]
    capacities += [max(map(len,masks[m])) for m in singles]
    need(len(residual)==448 and sum(capacities)<448,'fixed template first-stage obstruction')
    return {'positive_template_first_demand':len(residual),'positive_template_first_group_capacity':sum(capacities),'positive_template_first_group_capacities':capacities,'positive_template_raw_pair_checks':sum(m*n for m,n in pairs),'positive_template_singleton_phase_checks':sum(singles),'positive_shared_support_exact':True,'positive_target_size':82,'positive_original_tail_moduli':29,'positive_physical_points_covered':574,'positive_target_difference_gcd':4,'relaxation_equality_score':411,'equality_raw_extra':100,'equality_actual_union':85,'equality_loss':15,'first_stage_or_full_cover_asserted':False}

def main():
    p=ArgumentParser();p.add_argument('--fixture',type=Path,default=HERE/'positive-tail.json');p.add_argument('--output',type=Path);a=p.parse_args();r=compute(json.loads(a.fixture.read_text()))
    need(r==json.loads((HERE/'positive-expected.json').read_text()),'frozen positive/template counters differ')
    if a.output:a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r))
if __name__=='__main__':main()
