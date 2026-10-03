"""Literal integer endpoint lift, all actual m and all field steps, in bounded shards."""
import argparse,json
from model import P,need,digest
def run(N,lo,hi):
 need(N in (3702,3704) and 1<=lo<=hi<=N,'shard domain')
 total=forward=backward=0;trace=[]
 for m in range(lo,hi+1):
  for d in range(1,P):
   if m+6*d<=N:
    a=m;s=d;slot=0;forward+=1
   else:
    s=P-d;a=m-6*s;slot=6;backward+=1
   points=[a+j*s for j in range(7)]
   need(1<=points[0] and points[-1]<=N and s>0,'literal interval bounds')
   need(points[slot]==m and len(set(points))==7,'literal endpoint target')
   support={x%P for i,x in enumerate(points) if i!=slot}
   need(support=={(m+j*d)%P for j in range(1,7)} and len(support)==6 and m%P not in support,'literal field supports')
   total+=1;trace.append([m,d,a,s,slot])
 return dict(N=N,lo=lo,hi=hi,total=total,forward=forward,backward=backward,trace_sha256=digest(trace))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--N',type=int,required=True);a.add_argument('--lo',type=int,required=True);a.add_argument('--hi',type=int,required=True);a.add_argument('--output',required=True);args=a.parse_args();r=run(args.N,args.lo,args.hi)
 open(args.output,'w').write(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,sort_keys=True))
