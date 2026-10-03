"""Producer-only export boundary; never imported by independent programs."""
import argparse,json,pathlib,sys

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=pathlib.Path);a=ap.parse_args()
    sys.path.insert(0,str(a.source.resolve()));import model
    original_fingerprint=model.fingerprint;original_check=model.check;matrices=[];families=[]
    def capture_fingerprint(M):
        matrices.append([[str(z) for z in row] for row in M]);return original_fingerprint(M)
    def capture_check(family,M,s):
        families.append(list(family));return original_check(family,M,s)
    model.fingerprint=capture_fingerprint;model.check=capture_check
    output=[]
    for n,h in [(3,3),(3,4),(3,10),(5,3)]:
        matrices.clear();families.clear();fixture=model.actual(h,n)
        if len(matrices)!=2 or len(families)!=2 or families[0]!=families[1]:raise ValueError('entire native export boundary')
        output.append(dict(n=n,h=h,vertices=families[0],seed=matrices[0],repaired_M=matrices[1],fixture=fixture))
    print(json.dumps(output,sort_keys=True,separators=(',',':'),default=str))
if __name__=='__main__':main()
