"""All literal residual residues and modulo histograms, no producer imports."""
import argparse,hashlib,json

def need(ok,why):
    if not ok:raise ValueError(why)
def digest(obj):return hashlib.sha256((json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def actual():
    fixed=[[8,0],[9,0],[10,1],[14,0],[12,10],[28,4]]
    R=[n for n in range(2520) if all(n%m!=a for m,a in fixed)]
    labels=sorted({2**i*3**j*5**k*7**l for i in range(4) for j in range(3) for k in range(2) for l in range(2)}-{1,2,3,4,5,6,7}-{m for m,a in fixed})
    need(len(labels)==35 and all(2520%m==0 for m in labels),'literal original divisor domain')
    other=[m for m in labels if m not in (15,18)];rows={}
    for b in range(17,-1,-1):
        for a in range(14,-1,-1):
            residual=[n for n in R if n%15!=a and n%18!=b];removed=len(R)-len(residual);marginal=[]
            for m in other:
                counts=[0]*m
                for n in residual:counts[n%m]+=1
                marginal.append(max(counts))
            rows[a,b]=[a,b,removed,marginal,removed+sum(marginal)]
    return dict(fixed=fixed,period=2520,initial_holes=len(R),original_labels=labels,remaining_original_labels=other,raw_phase_pairs=270,rows=[rows[a,b] for a in range(15) for b in range(18)])
def check(data,expected):
    for key in expected:need(data.get(key)==expected[key],'literal entire BASE '+key)
    need(set(data)==set(expected),'BASE unknown or omitted fields')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);args=ap.parse_args();data=json.load(open(args.input));expected=actual();check(data,expected)
    print(json.dumps(dict(all_literal_entries_equal=True,record_sha256=digest(data),whole_row_sha256=digest(data['rows']),actual_marginal_values=8910,base_hole_lower=len([n for n in range(2520) if all(n%m!=a for m,a in expected['fixed'])])-max(r[-1] for r in expected['rows'])),sort_keys=True))
if __name__=='__main__':main()
