"""Optional deterministic positive-word discovery; verification does not use SAT."""
import argparse,hashlib,json
from pathlib import Path
from pysat.solvers import Solver
import model as m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 if args.output.exists():raise ValueError('output must be a new path')
 den,M,B,addresses,generic,lines,phases,stats=m.inventory();words=[]
 def solve(edges,collisions):
  for i,w in enumerate(words):
   if all(w[a]!=w[b]for a,b in edges)and all(w[a]==w[b]for a,b in collisions):return i
  labels,E=m.merged_graph(343,edges,collisions);n=1+max(labels)
  cs=[[4*v+c+1 for c in range(4)]for v in range(n)]
  cs += [[-(4*v+a+1),-(4*v+b+1)]for v in range(n)for a in range(4)for b in range(a)]
  cs += [[-(4*a+c+1),-(4*b+c+1)]for a,b in E for c in range(4)]
  with Solver(name='cadical195',bootstrap_with=cs)as s:
   s.conf_budget(200000);ans=s.solve_limited()
   if ans is not True:raise RuntimeError('UNKNOWN or non-four signal: stop and preserve, never claim closure')
   vals=set(s.get_model());col=[next(c for c in range(4)if 4*v+c+1 in vals)for v in range(n)]
   w=''.join(str(col[v])for v in labels)
  if not all(w[a]!=w[b]for a,b in edges)or not all(w[a]==w[b]for a,b in collisions):raise ValueError('invalid positive word')
  words.append(w);return len(words)-1
 gi=solve(generic,[]);keys=sorted(phases)
 ids=[solve(generic+sorted(phases[v]['edges']),phases[v]['collisions'])for v in keys]
 stream=json.dumps([m.encode(v)for v in keys],separators=(',',':'),sort_keys=True).encode()
 data={'generic_word':gi,'words':words,'word_indices':ids,'phase_sha256':hashlib.sha256(stream).hexdigest()}
 args.output.write_text(json.dumps(data,separators=(',',':'))+'\n')
 print(json.dumps(stats|{'words':len(words),'all_positive_words_checked':True,'record_candidate':False},indent=2))
if __name__=='__main__':main()
