"""Optional deterministic SAT witness producer; not imported by verify.py."""
import argparse,itertools,json,pathlib
from pysat.solvers import Glucose42
import geometry as g

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path,required=True);args=ap.parse_args()
 h=g.H();ds=sorted({(a-c,b-d) for a,b in h for c,d in h});ks,_=g.catalog(ds);rows=[]
 for k in ks:
  ps,es,labels=g.graph(h,ds,k);n=len(ps)
  with Glucose42() as sol:
   sol.append_formula([[4*v+c+1 for c in range(4)] for v in range(n)])
   sol.append_formula([[-(4*a+c+1),-(4*b+c+1)] for a,b in es for c in range(4)])
   sol.conf_budget(200000);answer=sol.solve_limited(expect_interrupt=True)
   if answer is not True:raise RuntimeError('Gate did not return a checked colouring; no automatic retry')
   model=set(v for v in sol.get_model() if v>0);colour=[next(c for c in range(4) if 4*v+c+1 in model) for v in range(n)]
   if any(colour[a]==colour[b] for a,b in es):raise ValueError('invalid decoded word')
  word=''.join(str(colour[i]) for i in labels);chi=4
  for sign in (-1,1):
   w=[(a-b+sign*(c-d))%3 for a,b in h for c,d in h];cw={};ok=True
   for i,l in enumerate(labels):
    if l in cw and cw[l]!=w[i]:ok=False;break
    cw[l]=w[i]
   if ok and all(cw[a]!=cw[b] for a,b in es):word=''.join(map(str,w));chi=3;break
  rows.append({'angle':g.keyjson(k),'vertices':n,'edges':len(es),'chi':chi,'colours':word})
 g.dump(args.output,{'family':'H2+uH2; |u|=1; all strict unit edges','cases':rows})
if __name__=='__main__':main()
