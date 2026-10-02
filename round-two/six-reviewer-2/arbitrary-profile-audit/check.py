from pathlib import Path
import argparse,json
from linear import canonical,digest,need
from scalars import record
from literal import audit
FIXTURES=[(8,[1,3,2,1],[3,1,0,2]),(8,[9,3,2,1],[0,3,1,2]),(16,[5,5,3,2,1],[4,0,3,1,2]),(16,[3,3,3,2,1],[2,4,0,3,1]),(32,[3,2,1,1],[5,0,3,1])]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int);ap.add_argument('--scalars',action='store_true');ap.add_argument('--expected',type=Path);args=ap.parse_args()
    if args.scalars:
        profiles=[(q,[1,3,2,1]) for q in [8,16,128,2**100]]
        profiles += [(32,[1,3,2,1,3,2]),(64,[4,3,2,1,4,3,2,1]),(2**19,list(range(1,13))+[12]*8),(2**100,[10**8,1,2,3]),(2**30,[10**12,10**12,10**6,2,1])]
        out={'kind':'independent scalar controls; finite checks, not unbounded proof','records':[record(q,loads) for q,loads in profiles]}
    else:
        need(args.case is not None and 0<=args.case<len(FIXTURES),'choose fixed finite case');out={'kind':'independent actual-index physical audit','case':args.case,'record':audit(*FIXTURES[args.case])}
    out=canonical(out);out['record_sha256']=digest(out)
    if args.expected:need(json.loads(args.expected.read_text())==out,'complete external record equality')
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
