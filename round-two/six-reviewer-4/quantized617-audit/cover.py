"""Fresh anchored increasing tuples, not a closed-intersection producer."""
import argparse,json
from owned_model import endpoint,neighbors,need,digest
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    supports,V,D=endpoint();sq,ns,A=neighbors(D)
    visits=[0]*8;trials=[0]*8;size_hist=[{} for _ in range(8)];tuples=[]
    def visit(rows,B,start):
        depth=len(rows);visits[depth]+=1;k=str(B.bit_count())
        size_hist[depth][k]=size_hist[depth].get(k,0)+1
        tuples.append([list(rows),[x for i,x in enumerate(ns) if B>>i&1]])
        if depth==7:return
        for i in range(start,len(sq)):
            trials[depth+1]+=1;C=B&A[sq[i]]
            if C.bit_count()>=6:visit(rows+(sq[i],),C,i+1)
    visit((1,),A[1],1)
    need(visits[7]==0,'unexpected actual K7,6 witness; no exclusion')
    result=dict(schema=1,method='all anchored increasing tuples with complete monotone threshold6 pruning',supports=supports,V=sorted(V),D=sorted(D),visits=visits,trials=trials,size_histograms=size_hist,tuple_count=len(tuples),tuple_sha256=digest(tuples),tuples=tuples)
    raw=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode()
    open(args.output,'wb').write(raw)
    print(json.dumps({k:v for k,v in result.items() if k!='tuples'},sort_keys=True))
if __name__=='__main__':main()
