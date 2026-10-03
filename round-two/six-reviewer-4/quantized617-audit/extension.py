"""Bounded neighboring size24 split9/15, using the complete same25 C8 cores."""
import argparse,json
from literal import digest,need
def psi(a,r,M):
    return max(s for s in range(M+1) if s+(a-r)*((s+r-1)//r)<=M)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cover',required=True);ap.add_argument('--cores',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    cover=json.load(open(args.cover));cores=json.load(open(args.cores));extra=[]
    for rows,C in cover['tuples']:
        if len(rows)==5 and len(C)==8:extra.append([9,15,rows,C,C])
    extra.sort(key=lambda r:r[2]);need(len(extra)==25,'whole size24 extension core domain')
    need(psi(8,5,8)==5 and psi(9,5,15)==7,'integer optimal degree reductions')
    result=cores+extra;open(args.output,'w').write(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps(dict(target_core_count=len(cores),extension_core_count=len(extra),all_core_count=len(result),all_core_sha256=digest(result),size24_8_16_common_lower=11,size24_9_15_common_lower=8,optimal_degree_sum_10_13=psi(10,5,15),optimal_degree_sum_11_12=psi(11,5,17)),sort_keys=True))
if __name__=='__main__':main()
