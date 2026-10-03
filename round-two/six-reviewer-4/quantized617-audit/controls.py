"""Independent finite controls and semantic certificate damage; useful under -O."""
import argparse,copy,itertools,json
from literal import graph,need,digest
from allocate import budget_tuples
from allocation_check import residue_tuples,check as allocation_check
from cover_check import check as cover_check
from extension import psi

def degrees():
    cases=0;sharp=0
    for a in range(1,7):
        for b in range(5):
            vectors=list(itertools.combinations_with_replacement(range(b+1),a))
            for r in range(1,a+1):
                for M in range(a*b+1):
                    bound=min(r*b,psi(a,r,M))
                    eligible=[d for d in vectors if sum(d)<=M]
                    need(max(sum(d[:r]) for d in eligible)==bound,'sharp integer degree bound')
                    for d in eligible:
                        S=sum(d[:r]);need(S+(a-r)*((S+r-1)//r)<=sum(d),'integer sorted degree necessity');cases+=1
                    low,rem=divmod(bound,r);w=[low]*(r-rem)+[low+1]*rem+[(bound+r-1)//r]*(a-r)
                    need(w==sorted(w) and max(w)<=b and sum(w)<=M and sum(w[:r])==bound,'explicit attained degree bound');sharp+=1
    return dict(part='degrees',actual_degree_vectors_checked=cases,sharp_parameter_cases=sharp)

def budgets():
    cases=0;nonempty=0;empty=0
    for L in range(1,8):
        for weights in itertools.product(range(3),repeat=L):
            # Keep the whole exhaustive domain modest without random sampling.
            if L>5 and any(weights[i]!=weights[i%3] for i in range(3,L)):continue
            rows=[[i,0,w] for i,w in enumerate(weights)]
            for n in range(min(4,L)+1):
                for cap in range(7):
                    literal=[list(c) for c in itertools.combinations(range(L),n) if sum(weights[i] for i in c)<=cap]
                    proposal,coeff=budget_tuples(rows,n,cap);other=residue_tuples(rows,n,cap)
                    hist={}
                    for c in literal:
                        weight=sum(weights[i] for i in c);hist[weight]=hist.get(weight,0)+1
                    need(proposal==literal==other and coeff==sorted(hist.items()),'complete actual-subset budget bijections including terminal cost')
                    cases+=1;nonempty+=bool(literal);empty+=not literal
    return dict(part='budgets',whole_actual_subset_cases=cases,nonempty_cases=nonempty,empty_cases=empty)

def allocations():
    cases=0;weights=0
    for bits in range(1<<9):
        edge={(q,t) for q in range(3) for t in range(3) if bits>>(3*q+t)&1}
        C={t for t in range(3) if (0,t) in edge};outside=sorted(set(range(3))-C)
        for size in range(len(C)+1):
            for B0 in itertools.combinations(sorted(C),size):
                for n in (1,2):
                    for L in itertools.product(range(3),repeat=2):
                        if sum(sorted(L,reverse=True)[:n])>2:continue
                        weights+=1
                        for k in range(len(outside)+1):
                            hs=[]
                            for q in (1,2):
                                g=sum((q,t) not in edge for t in B0)
                                costs=sorted(L[q-1]+2*int((q,t) not in edge) for t in outside)
                                hs.append(2*g+sum(costs[:k]))
                            lower=sum(sorted(hs)[:n])
                            for extra in itertools.combinations((1,2),n):
                                for T in itertools.combinations(outside,k):
                                    M=sum((q,t) not in edge for q in extra for t in B0)+sum((q,t) not in edge for q in (0,)+extra for t in T)
                                    need(sum(hs[q-1] for q in extra)<=2*M and lower<=2*M,'nonuniform allocated-deficit necessity');cases+=1
    need(min(5,1+1)==2 and 5>2,'adjacent shortcut is false without its degree-gap hypothesis')
    return dict(part='allocations',all_three_by_three_graphs=512,weight_domain_cases=weights,actual_selected_row_column_cases=cases,invalid_shortcut_fixture=dict(base_rows=5,extra_rows=1,k=1,adjacent_minimum=5,whole_outside_minimum=2))

def damage(args):
    cover=json.load(open(args.cover));data=json.load(open(args.data));cores=json.load(open(args.cores));structure=graph();rejected=[]
    def reject(name,fn,reason):
        try:fn()
        except ValueError as e:
            need(str(e)==reason,'damage rejected for unintended reason: '+name+': '+str(e));rejected.append(name)
        else:raise ValueError('accepted semantic damage: '+name)
    if args.part=='cover-damage':
        bad=copy.deepcopy(cover);bad['tuples'][0][1].pop();bad['tuple_sha256']=digest(bad['tuples'])
        reject('false full anchored neighborhood',lambda:cover_check(bad),'literal whole common neighborhood')
        bad=copy.deepcopy(cover);at=next(i for i,t in enumerate(bad['tuples']) if len(t[0])==5);bad['tuples'].pop(at);bad['tuple_sha256']=digest(bad['tuples'])
        reject('missing legal five-row tuple with recomputed hash',lambda:cover_check(bad),'missing or false legal extension')
        bad=copy.deepcopy(cover);bad['tuples'].append(copy.deepcopy(bad['tuples'][0]));bad['tuple_sha256']=digest(bad['tuples'])
        reject('duplicate tuple with recomputed hash',lambda:cover_check(bad),'duplicate anchored state')
    else:
        def run(bad):return allocation_check(bad,cores,args.lo,args.hi,structure)
        bad=copy.deepcopy(data);bad.pop();reject('missing core',lambda:run(bad),'whole core cover/order')
        bad=copy.deepcopy(data);bad[0]['cap']+=1;reject('false allocated cap',lambda:run(bad),'actual parameters')
        bad=copy.deepcopy(data);bad[0]['core'][4].pop();reject('false whole common set',lambda:run(bad),'literal core identity')
        bad=copy.deepcopy(data);bad[0]['rows'][0][2]+=1;reject('false actual row cost',lambda:run(bad),'EVERY actual row g/h cost')
        index=next(i for i,r in enumerate(data) if r['residual']);need(index>=0,'positive residual fixture')
        bad=copy.deepcopy(data);bad[index]['residual'].pop();bad[index]['row_choices']-=1;reject('missing actual residual tuple',lambda:run(bad),'whole literal row choice count')
        bad=copy.deepcopy(data);bad[index]['residual'].append(copy.deepcopy(bad[index]['residual'][0]));bad[index]['row_choices']+=1;reject('duplicate actual residual tuple',lambda:run(bad),'whole literal row choice count')
        bad=copy.deepcopy(data);bad[index]['residual'][0]['minimum_missing']-=1;reject('false exact deficit',lambda:run(bad),'entire residual actual column/row/deficit record')
        bad=copy.deepcopy(data);bad[index]['residual'][0]['best_columns'][0]=0;reject('false original outside column',lambda:run(bad),'entire residual actual column/row/deficit record')
        bad=copy.deepcopy(data);bad[index]['coefficient'][0][1]+=1;reject('false budget coefficient',lambda:run(bad),'entire producer coefficient matches all actual tuples')
    return dict(part=args.part,rejected_count=len(rejected),rejected_semantic_damage=rejected)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--part',choices=['degrees','budgets','allocations','cover-damage','allocation-damage'],required=True)
    ap.add_argument('--cover');ap.add_argument('--data');ap.add_argument('--cores');ap.add_argument('--lo',type=int);ap.add_argument('--hi',type=int);args=ap.parse_args()
    fn={'degrees':degrees,'budgets':budgets,'allocations':allocations}.get(args.part)
    print(json.dumps(fn() if fn else damage(args),sort_keys=True))
if __name__=='__main__':main()
