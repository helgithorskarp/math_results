"""Generate the compact positive witnesses; PySAT is not used by verify.py."""
import argparse,base64,json,time
from itertools import combinations
from pathlib import Path
from pysat.solvers import Solver

def pack(c):
 out=bytearray((len(c)+3)//4)
 for i,v in enumerate(c):out[i//4]|=v<<(2*(i%4))
 return base64.b64encode(out).decode()
def produce(args):
 data=json.loads(args.frontier.read_text());g=data['geometry'];rows=[];stats=[]
 require=lambda ok,msg:None if ok else (_ for _ in ()).throw(ValueError(msg))
 for r in data['frontier']:
  qs=r['fresh'];b=len(qs)
  for D in combinations(r['unknown'],b+1):
   retained=[v for v in range(509)if v not in D];labels=retained+[509+i for i in range(b)];index={v:i for i,v in enumerate(labels)}
   require(len(labels)==508,'order')
   edges=[(a,v)for a,v in g['base_edges']if a not in D and v not in D]
   edges += [(v,509+i)for i,q in enumerate(qs)for v in g['neighbours'][q]if v not in D]
   edges += [(509+i,509+j)for i,j in r['edges']]
   edges=[tuple(sorted((index[a],index[v])))for a,v in edges];es=set(edges)
   def x(i,c):return 4*i+c+1
   cnf=[[x(i,c)for c in range(4)]for i in range(508)]
   cnf += [[-x(a,c),-x(v,c)]for a,v in edges for c in range(4)]
   tri=next((a,v,w)for a,v in edges for w in range(v+1,508)if (a,w)in es and (v,w)in es)
   cnf += [[x(i,c)]for c,i in enumerate(tri)]
   start=time.monotonic()
   with Solver(name='cadical195',bootstrap_with=cnf)as solver:
    solver.conf_budget(args.conflicts);answer=solver.solve_limited();model=solver.get_model()if answer else None;stat=solver.accum_stats()
   stats.append({'fresh':qs,'deleted':list(D),'answer':answer,'seconds':time.monotonic()-start,'stats':stat})
   args.log.write_text(json.dumps(stats,indent=2)+'\n')
   if answer is not True:
    p=args.log.with_name('inconclusive-'+str(len(stats))+'.cnf');p.write_text(f'p cnf 2032 {len(cnf)}\n'+''.join(' '.join(map(str,c))+' 0\n'for c in cnf))
    raise RuntimeError('Witness not obtained; SAT status and CNF saved. No conclusion from this answer.')
   positive={v for v in model if v>0};col=[next(c for c in range(4)if x(i,c)in positive)for i in range(508)]
   require(all(col[a]!=col[v]for a,v in edges),'model decoding')
   rows.append({'fresh':qs,'deleted':list(D),'colours':pack(col)})
   print('checked positive witness',len(rows),flush=True)
 args.output.write_text(json.dumps({'format':'parts-moser-isometry-colours-v1','rows':rows},separators=(',',':'))+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('frontier',type=Path);p.add_argument('output',type=Path);p.add_argument('--log',type=Path,required=True);p.add_argument('--conflicts',type=int,default=250000);produce(p.parse_args())
