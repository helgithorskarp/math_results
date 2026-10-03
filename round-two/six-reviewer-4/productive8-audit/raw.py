"""All original third-parent phases; odd intersections vs physical four lifts."""
import argparse,itertools,json,hashlib
from base import need
from odd import shadow

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--parent',type=int,required=True);ap.add_argument('--method',choices=['odd','physical'],required=True);ap.add_argument('--output',required=True);args=ap.parse_args();r=args.parent
    need(r in (1,3,4,5,7),'original third parent');D=[d for d in range(3,316,2) if 315%d==0];out=bytearray();hist={};cache={};raw_pairs=0
    if args.method=='odd':
        U=shadow(r)
        for d in D:cache[d]=[sum(1<<y for y in U if y%d==a)for a in range(d)]
    else:
        fixed=[(8,0),(9,0),(10,1),(14,0),(12,10),(28,4)]
        holes=[n for n in range(r,2520,8) if all(n%m!=a for m,a in fixed)]
        for d in D:
            phases=[]
            for a in range(r,16*d,8):
                quarters=[]
                for ell in range(4):quarters.append(sum(1<<i for i,n in enumerate(holes) if (n+2520*ell-a)%(16*d)==0))
                phases.append(quarters)
            cache[d]=phases
    for g,h in itertools.combinations(D,2):
        for i,a in enumerate(range(r,16*g,8)):
            for j,b in enumerate(range(r,16*h,8)):
                if args.method=='odd':count=(cache[g][a%g]&cache[h][b%h]).bit_count() if (a-b)%16==8 else 0
                else:
                    A=cache[g][i];B=cache[h][j];count=((A[0]|B[0])&(A[1]|B[1])&(A[2]|B[2])&(A[3]|B[3])).bit_count()
                out.append(count);hist[str(count)]=hist.get(str(count),0)+1;raw_pairs+=1
    open(args.output,'wb').write(out)
    print(json.dumps(dict(parent=r,raw_original_phase_pairs=raw_pairs,whole_ordered_raw_vector_sha256=hashlib.sha256(out).hexdigest(),count_histogram=hist,maximum_repaired_base_holes=max(out)),sort_keys=True))
if __name__=='__main__':main()
