#!/usr/bin/env python3
"""Native-cardinality version of the same exact five-addition construction search.

A degree condition uses sum(not x_u : u in free neighbours)+r*x_v<=d.
Distinct clones equivalent to x_v express the coefficient r without relying
on duplicate-literal handling. An UNSAT master verdict remains unchecked.
"""
from pathlib import Path
import argparse,json,time
from pysat.solvers import Solver
import build,record
from search_repair import save,expand,solve_four,master_formula

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);p.add_argument('--resume',type=Path);p.add_argument('--iterations',type=int,default=200);p.add_argument('--seconds',type=int,default=900);p.add_argument('--conflicts',type=int,default=1000000);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True);start=time.monotonic()
 pts,_=build.generate(False);ee=build.edges(pts);matching=record.compare(pts);fixed=set(matching['map'].values());free=sorted(set(range(len(pts)))-fixed);bound=508-len(fixed);ix={v:i+1 for i,v in enumerate(free)};top=len(free)
 if (len(fixed),bound)!=(503,5):raise ValueError('target cardinality')
 adj=[set() for _ in pts]
 for u,v in ee:adj[u].add(v);adj[v].add(u)
 previous=json.loads(a.resume.read_text()) if a.resume else {'witnesses':[]};witnesses=previous['witnesses'];rounds=[]
 for w in witnesses:expand(w,adj,fixed,free)
 master=Solver(name='minicard');master.add_atmost(list(range(1,top+1)),bound);guards=0
 for v in free:
  required=4-len(adj[v]&fixed)
  if required<=0:continue
  neighbours=sorted(adj[v]-fixed);clones=[]
  for _ in range(required):
   top+=1;clones.append(top);master.add_clause([-ix[v],top]);master.add_clause([ix[v],-top])
  master.add_atmost([-ix[u] for u in neighbours]+clones,len(neighbours));guards+=1
 for w in witnesses:master.add_clause([ix[v] for v in w['cut']])
 print(json.dumps({'stage':'start','variables':top,'guards':guards,'witnesses':len(witnesses),'seconds':time.monotonic()-start}),flush=True)
 status='RUNNING'
 for j in range(a.iterations):
  master.conf_budget(a.conflicts);ok_master=master.solve_limited()
  if ok_master is not True:status='MASTER_UNSAT_UNCHECKED' if ok_master is False else 'UNKNOWN_MASTER';break
  positives=set(master.get_model());T={v for v in free if ix[v] in positives}
  if len(T)>bound or any(len(adj[v]&(fixed|T))<4 for v in T):raise ValueError('bad native-cardinality model')
  vs=sorted(fixed|T);where={v:i for i,v in enumerate(vs)};es=[(where[u],where[v]) for u,v in ee if u in where and v in where]
  ok,word,stats=solve_four(len(vs),es);iteration=20000+j;row={'iteration':iteration,'selected':sorted(T),'n':len(vs),'e':len(es),'answer':str(ok),'candidate_stats':stats,'master_stats':master.accum_stats(),'seconds':time.monotonic()-start};rounds.append(row);print(json.dumps(row),flush=True)
  if ok is not True:
   status='NONFOUR_SIGNAL' if ok is False else 'UNKNOWN_CANDIDATE';save(a.work/'candidate.json',{'vertices':vs,'edges':es,'status':str(ok)});text,_=build.cnf(len(vs),es);(a.work/'candidate.cnf').write_text(text);break
  for variant in range(3):
   w={'iteration':iteration,'variant':variant,'selected':sorted(T),'seed_word':word};colour,cut=expand(w,adj,fixed,free);w['cut']=cut;w['coloured_vertices']=len(colour);witnesses.append(w);master.add_clause([ix[v] for v in cut])
  save(a.work/'progress.json',{'status':status,'fixed':sorted(fixed),'free':free,'bound':bound,'rounds':rounds,'witnesses':witnesses,'seconds':time.monotonic()-start})
  if time.monotonic()-start>=a.seconds:status='TIME_CHECKPOINT';break
 else:status='ITERATION_CHECKPOINT'
 save(a.work/'result.json',{'status':status,'fixed':sorted(fixed),'free':free,'bound':bound,'rounds':rounds,'witnesses':witnesses,'seconds':time.monotonic()-start,'master_stats':master.accum_stats()});master.delete()
 # A normal CNF encoding is available for a separate proof-producing replay.
 clauses,nvars,_ix,_guards=master_formula(adj,fixed,free,bound,witnesses)
 text=f'p cnf {nvars} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses);(a.work/'master.cnf').write_text(text)
 print(json.dumps({'stage':'done','status':status,'queries':len(rounds),'witnesses':len(witnesses),'seconds':time.monotonic()-start}),flush=True)
if __name__=='__main__':main()
