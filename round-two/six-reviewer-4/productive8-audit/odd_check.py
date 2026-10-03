"""Literal BASE members and all residue histograms; no odd-producer imports."""
import argparse,itertools,json,math
from base_check import need,digest
FIXED=[[8,0],[9,0],[10,1],[14,0],[12,10],[28,4]]
def holes(r):return [n for n in range(r,2520,8) if all(n%m!=a for m,a in FIXED)]
def actual():
    D=sorted({3**i*5**j*7**k for i in range(3)for j in range(2)for k in range(2)});extra=D[1:];U=holes(2)
    need({n%315 for n in U}=={n%315 for n in holes(6)},'actual same mandatory-parent odd shadow')
    masks={d:[{n for n in U if n%d==a}for a in range(d)]for d in D};C={d:max(map(len,masks[d]))for d in D}
    pairs=[]
    for a,b in itertools.combinations(extra,2):
        v=a*b//math.gcd(a,b);pairs.append([a,b,v,C[v]])
    triples=[]
    for a,b,c in itertools.combinations(extra,3):
        v=math.lcm(a,b,c);paircost=sum(C[x*y//math.gcd(x,y)]for x,y in itertools.combinations((a,b,c),2));triples.append([a,b,c,v,C[v],paircost])
    minima={f'{a},{b}':min(len(x&y)for x in masks[a]for y in masks[b]if x and y)for a,b in ((3,5),(3,7),(5,7))}
    original_witness=[[48,26,2],[144,66,2],[80,30,6],[112,22,6]];touched={2:set(),6:set()}
    for modulus,phase,parent in original_witness:
        touched[parent].update(n for n in holes(parent)if any((n+2520*ell-phase)%modulus==0 for ell in range(4)))
    need(sum(map(len,touched.values()))==170,'relaxed literal original-class footprint witness')
    third=[]
    for r in (1,3,4,5,7):
        R=holes(r)
        for g,h in itertools.combinations(extra,2):
            q=g*h//math.gcd(g,h);counts=[0]*q
            for n in R:counts[n%q]+=1
            third.append([r,g,h,q,counts])
    return dict(divisors=D,shadow_sizes=[[r,len(holes(r))]for r in range(1,8)],cofactor_phase_counts=[[d,list(map(len,masks[d]))]for d in D],capacities=[[d,C[d]]for d in D],pairs=pairs,triples=triples,quartets=[[list(v),sum(C[d]for d in v)]for v in itertools.combinations(extra,4)],S=[sum(sorted([C[d]for d in extra],reverse=True)[:k])for k in range(1,5)],minimum_nonempty_phase_intersections=minima,two_parent_four_H_bound=170,relaxed_witness=dict(parent2=[[3,2],[9,3]],parent6=[[5,0],[7,1]],parent2_holes=len(touched[2]),parent6_holes=len(touched[6])),third_parent_phase_counts=third)
def check(data,expected):
    need(set(data)==set(expected),'whole odd-domain field census')
    for key in expected:need(data[key]==expected[key],'literal entire odd '+key)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);a=ap.parse_args();data=json.load(open(a.input));check(data,actual());print(json.dumps(dict(all_literal_entries_equal=True,record_sha256=digest(data),third_parent_phase_entries=sum(len(r[-1])for r in data['third_parent_phase_counts']),two_parent_four_H_bound=170),sort_keys=True))
if __name__=='__main__':main()
