"""Complete odd CRT footprints and an ordinary sharp two-parent relaxation."""
import argparse,itertools,json,math
from base import need,digest
D=[d for d in range(1,316) if 315%d==0]
def shadow(r):
    if r in (2,6):return {y for y in range(315) if y%9!=0 and y%3!=1 and y%7!=0}
    if r==4:return {y for y in range(315) if y%9!=0 and y%7 not in (0,4)}
    return {y for y in range(315) if y%9!=0 and y%5!=1}
def generate():
    U=shadow(2);masks={d:[sum(1<<y for y in U if y%d==a) for a in range(d)] for d in D};C={d:max(v.bit_count() for v in masks[d]) for d in D};extra=D[1:]
    pairs=[[a,b,math.lcm(a,b),C[math.lcm(a,b)]]for a,b in itertools.combinations(extra,2)]
    triples=[[a,b,c,math.lcm(a,b,c),C[math.lcm(a,b,c)],sum(C[math.lcm(x,y)]for x,y in itertools.combinations((a,b,c),2))]for a,b,c in itertools.combinations(extra,3)]
    quartets=[[list(v),sum(C[d]for d in v)]for v in itertools.combinations(extra,4)]
    minima={}
    for a,b in ((3,5),(3,7),(5,7)):
        values=[(x&y).bit_count() for x in masks[a] for y in masks[b] if x and y];minima[f'{a},{b}']=min(values)
    need(min(minima.values())>=5,'unavoidable same-parent footprint overlap')
    need([v for v,s in quartets if s>170]==[[3,5,7,9]],'only potentially excessive global H quartet')
    witness=dict(parent2=[[3,2],[9,3]],parent6=[[5,0],[7,1]],parent2_holes=(masks[3][2]|masks[9][3]).bit_count(),parent6_holes=(masks[5][0]|masks[7][1]).bit_count())
    need(witness['parent2_holes']+witness['parent6_holes']==170,'attainment ONLY of two-parent odd-footprint relaxation')
    third=[]
    for r in (1,3,4,5,7):
        U3=shadow(r)
        for g,h in itertools.combinations(extra,2):
            lcm=math.lcm(g,h);counts=[sum(y%lcm==a for y in U3)for a in range(lcm)];third.append([r,g,h,lcm,counts])
    return dict(divisors=D,shadow_sizes=[[r,len(shadow(r))] for r in range(1,8)],cofactor_phase_counts=[[d,[v.bit_count()for v in masks[d]]]for d in D],capacities=[[d,C[d]]for d in D],pairs=pairs,triples=triples,quartets=quartets,S=[sum(sorted([C[d]for d in extra],reverse=True)[:k])for k in range(1,5)],minimum_nonempty_phase_intersections=minima,two_parent_four_H_bound=170,relaxed_witness=witness,third_parent_phase_counts=third)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();data=generate();open(a.output,'w').write(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
    hist={}
    for r,g,h,lcm,counts in data['third_parent_phase_counts']:hist[str(r)]=max(hist.get(str(r),0),max(counts))
    print(json.dumps(dict(record_sha256=digest(data),third_parent_whole_phase_sha256=digest(data['third_parent_phase_counts']),third_parent_phase_entries=sum(len(t[-1])for t in data['third_parent_phase_counts']),third_parent_maxima=hist,two_parent_four_H_bound=170,minimum_nonempty_intersections=data['minimum_nonempty_phase_intersections'],pair_intersection_maximum=max(t[-1]for t in data['pairs']),triple_intersection_maximum=max(t[-2]for t in data['triples']),triple_pair_sum_maximum=max(t[-1]for t in data['triples']),all_unused_quartets=len(data['quartets'])),sort_keys=True))
if __name__=='__main__':main()
