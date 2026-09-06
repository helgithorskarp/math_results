"""Exhaustive small-case alignment against named-colour enumeration."""
import argparse,json,subprocess
from pathlib import Path
from itertools import combinations,product
from colour_check import solve as reference
from native import solve
ROOT=Path(__file__).resolve().parent

def brute(n,es,pins):
    for c in product(range(4),repeat=n):
        if all(c[v]==x for v,x in pins) and all(c[i]!=c[j] for i,j in es):return True
    return False

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--binary',type=Path,default=ROOT/'out/colour-check');parser.add_argument('--small',action='store_true');args=parser.parse_args()
    pairs=list(combinations(range(5),2));pinsets=[[],[(0,0)],[(0,0),(1,0)],[(0,0),(1,1)],[(0,0),(1,1),(2,2)]];count=0
    masks=range(1024) if not args.small else [0,1,3,31,511,1023]
    for mask in masks:
        es=[list(e) for i,e in enumerate(pairs) if mask>>i&1]
        for pins in pinsets:
            a,s=solve(args.binary,5,es,pins);b,t=reference(5,es,pins=pins)
            if a!=b or s!=t or (a is not None)!=brute(5,es,pins):raise ValueError('Small-case disagreement')
            count+=1
    malformed=['-1 0 0\n','2 1 0\n0 0\n','2 1 0\n0 2\n','3 2 0\n0 1\n1 0\n','2 0 1\n0 4\n','2 0 2\n0 0\n0 1\n','2 0 0\nextra\n','4097 0 0\n']
    for data in malformed:
        p=subprocess.run([str(args.binary)],input=data,capture_output=True,text=True)
        if p.returncode!=2:raise ValueError('Malformed instance not rejected normally')
    print(json.dumps({'complete_small_cases':count,'named_colour_agreement':True,'reference_words_and_search_counts_match':True,'malformed_rejected':len(malformed)},sort_keys=True))
if __name__=='__main__':main()
