"""Full outside-column costs plus per-row suffix polynomial and exact unranking."""
import argparse,heapq,json
from owned_model import endpoint,neighbors,need,digest
def graph():
    supports,V,D=endpoint();sq,ns,masks=neighbors(D)
    A={q:{t for i,t in enumerate(ns) if masks[q]>>i&1} for q in sq}
    columns={t:{q for q in sq if t in A[q]} for t in ns}
    return supports,V,D,sq,ns,A,columns
def budget_tuples(rows,n,cap):
    """All actual-row factors, not cost groups. No incomplete heuristic search."""
    L=len(rows);suffix=[[{} for r in range(n+1)] for i in range(L+1)];suffix[L][0]={0:1}
    for i in range(L-1,-1,-1):
        weight=rows[i][2]
        for r in range(n+1):
            here=dict(suffix[i+1][r])
            if r:
                for cost,count in suffix[i+1][r-1].items():
                    if cost+weight<=cap:here[cost+weight]=here.get(cost+weight,0)+count
            suffix[i][r]=here
    out=[]
    def possible(i,r,c):return any(k<=c for k in suffix[i][r])
    def walk(i,r,c,selected):
        if r==0:out.append(selected);return
        if i==L:return
        q,g,h=rows[i]
        if h<=c and possible(i+1,r-1,c-h):walk(i+1,r-1,c-h,selected+[q])
        if possible(i+1,r,c):walk(i+1,r,c,selected)
    walk(0,n,cap,[])
    need(len(out)==sum(suffix[0][n].values()),'whole coefficient/unranking bijection')
    return out,sorted(suffix[0][n].items())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cores',required=True);ap.add_argument('--lo',type=int,required=True);ap.add_argument('--hi',type=int,required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    cores=json.load(open(args.cores));need(0<=args.lo<args.hi<=len(cores),'core partition');supports,V,D,sq,ns,A,columns=graph();results=[]
    for index in range(args.lo,args.hi):
        a,b,A0,B0,C=cores[index];n=a-5;k=b-len(B0);cap=n*(a*b-5*(a+b));outside=[t for t in ns if t not in C];rows=[]
        d0={t:5-len(set(A0).intersection(columns[t])) for t in outside}
        need(set(C)==set.intersection(*(A[q] for q in A0)) and all(v>=1 for v in d0.values()),'whole common/outside domain')
        for q in sq:
            if q in A0:continue
            g=len(set(B0)-A[q]);costs=[d0[t]+n*int(t not in A[q]) for t in outside]
            h=n*g+sum(heapq.nsmallest(k,costs));rows.append([q,g,h])
        lower=sum(heapq.nsmallest(n,[r[2] for r in rows]));minimum_g=sum(heapq.nsmallest(n,[r[1] for r in rows]));selected=[];coeff=[];residual=[]
        if lower<=cap:
            selected,coeff=budget_tuples(rows,n,cap)
            for extra in selected:
                full=set(A0+extra);base=sum(len(set(B0)-A[q]) for q in extra)
                costs=sorted((a-len(full.intersection(columns[t])),t) for t in outside)
                best=costs[:k];M=base+sum(v for v,t in best)
                residual.append(dict(rows=extra,h_cost=sum(r[2] for r in rows if r[0] in extra),base_missing=base,whole_outside_cost_sha256=digest(costs),best_columns=[t for v,t in best],best_costs=[v for v,t in best],minimum_missing=M))
        results.append(dict(index=index,core=cores[index],n=n,k=k,cap=cap,rows=rows,lower=lower,elementary_lower=k+minimum_g,coefficient=coeff,row_choices=len(selected),residual=residual))
    raw=(json.dumps(results,sort_keys=True,separators=(',',':'))+'\n').encode();open(args.output,'wb').write(raw)
    print(json.dumps(dict(lo=args.lo,hi=args.hi,core_cases=len(results),entire_result_sha256=digest(results),all_row_costs=sum(len(r['rows']) for r in results),allocated_rejected=sum(r['lower']>r['cap'] for r in results),residual_core_cases=sum(r['lower']<=r['cap'] for r in results),row_choices=sum(r['row_choices'] for r in results),residual_minimum=min([v['minimum_missing'] for r in results for v in r['residual']],default=None)),sort_keys=True))
if __name__=='__main__':main()
