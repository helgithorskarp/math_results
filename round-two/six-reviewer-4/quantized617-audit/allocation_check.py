"""Adjacent-column costs; literal increasing-row budget enumeration and full deficits."""
import argparse,itertools,json
from literal import graph,need,digest
def residue_tuples(rows,n,cap):
    L=len(rows);minimum=[[None]*(n+1) for i in range(L+1)];minimum[L][0]=0
    for i in range(L-1,-1,-1):
        weights=sorted(r[2] for r in rows[i:]);minimum[i][0]=0
        for r in range(1,n+1):
            if len(weights)>=r:minimum[i][r]=sum(weights[:r])
    out=[]
    def walk(start,left,cost,chosen):
        if left==0:
            if cost<=cap:out.append(chosen)
            return
        bound=minimum[start][left]
        if bound is None or cost+bound>cap:return
        for i in range(start,L-left+1):
            q,g,h=rows[i];walk(i+1,left-1,cost+h,chosen+[q])
    walk(0,n,0,[]);return out
def check(data,cores,lo,hi,structure=None):
    need(0<=lo<hi<=len(cores),'literal valid core partition')
    supports,V,D,sq,ns,A,columns=graph() if structure is None else structure
    need([r['index'] for r in data]==list(range(lo,hi)),'whole core cover/order')
    choices=0;hist={}
    for record in data:
        index=record['index'];need(record['core']==cores[index],'literal core identity');a,b,A0,B0,C=cores[index];n=a-5;k=b-len(B0);cap=n*(a*b-5*(a+b))
        need((record['n'],record['k'],record['cap'])==(n,k,cap),'actual parameters')
        common=set.intersection(*(A[q] for q in A0));need(common==set(C) and set(B0)<=common,'entire original common set')
        outside=set(ns)-common;d0={t:sum(t not in A[q] for q in A0) for t in outside};need(n>=4 and max(d0.values())<=5 and min(d0.values())>=1,'proved adjacent-minimum condition (ties allowed at n4)')
        rows=[]
        for q in sq:
            if q in A0:continue
            eligible=outside.intersection(A[q]);need(len(eligible)>=k,'at least k adjacent actual outside columns')
            g=sum(t not in A[q] for t in B0);h=n*g+sum(sorted(d0[t] for t in eligible)[:k]);rows.append([q,g,h])
        need(rows==record['rows'],'EVERY actual row g/h cost')
        lower=sum(sorted(r[2] for r in rows)[:n]);elementary=k+sum(sorted(r[1] for r in rows)[:n])
        need((lower,elementary)==(record['lower'],record['elementary_lower']),'entire lower bounds')
        selected=residue_tuples(rows,n,cap) if lower<=cap else []
        need(len(selected)==record['row_choices'],'whole literal row choice count')
        need(selected==[r['rows'] for r in record['residual']],'ALL actual row tuples, not aggregate count only')
        coefficient={}
        for extra,leaf in zip(selected,record['residual'],strict=True):
            hsum=sum(h for q,g,h in rows if q in extra);coefficient[hsum]=coefficient.get(hsum,0)+1
            full=A0+extra;base=sum(t not in A[q] for q in extra for t in B0)
            costs=sorted((sum(t not in A[q] for q in full),t) for t in outside)
            best=costs[:k];M=base+sum(c for c,t in best)
            expected=dict(rows=extra,h_cost=hsum,base_missing=base,whole_outside_cost_sha256=digest(costs),best_columns=[t for c,t in best],best_costs=[c for c,t in best],minimum_missing=M)
            need(leaf==expected,'entire residual actual column/row/deficit record');hist[str(M)]=hist.get(str(M),0)+1
            need(M>a*b-5*(a+b),'actual feasible counterexample to exclusion');choices+=1
        need(record['coefficient']==[[cost,count] for cost,count in sorted(coefficient.items())],'entire producer coefficient matches all actual tuples')
    return dict(lo=lo,hi=hi,core_cases=len(data),entire_result_sha256=digest(data),all_row_costs=sum(len(r['rows']) for r in data),allocated_rejected=sum(r['lower']>r['cap'] for r in data),residual_core_cases=sum(r['lower']<=r['cap'] for r in data),row_choices=choices,minimum_missing_histogram=hist,all_literal_records_equal=True)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--cores',required=True);ap.add_argument('--lo',type=int,required=True);ap.add_argument('--hi',type=int,required=True);args=ap.parse_args()
    print(json.dumps(check(json.load(open(args.input)),json.load(open(args.cores)),args.lo,args.hi),sort_keys=True))
if __name__=='__main__':main()
