#!/usr/bin/env python3
"""Actual sub-509 construction search: 503 fixed points and at most five additions.

A checked four-colour extension supplies a necessary hitting clause. Relative
minimality justifies requiring degree at least4 at each selected new point.
Only a checked final refutation can turn MASTER_UNSAT into a family theorem.
"""
from pathlib import Path
import argparse,json,time,random,subprocess,hashlib
import build,record

HERE=Path(__file__).resolve().parent

def save(p,o):
 q=p.with_suffix(p.suffix+'.tmp');q.write_text(json.dumps(o,separators=(',',':'))+'\n');q.replace(p)
def expand(witness,adj,fixed,free):
 T=set(witness['selected']);vs=sorted(fixed|T);word=witness['seed_word']
 if len(word)!=len(vs) or any(c not in '0123' for c in word):raise ValueError('seed word')
 colour={v:int(c) for v,c in zip(vs,word)};iteration=witness['iteration'];variant=witness['variant']
 rng=random.Random(20260913+3*iteration+variant);noise={v:rng.random() for v in free}
 order=sorted(set(free)-T,key=lambda v:(-len(adj[v]&(fixed|T)),-len(adj[v]),noise[v],v))
 for v in order:
  allowed=set(range(4))-{colour[u] for u in adj[v]&colour.keys()}
  if not allowed:continue
  if variant==0:c=min(allowed)
  elif variant==1:c=max(allowed)
  else:
   def score(c):return sum(c in {colour[w] for w in adj[u]&colour.keys()} for u in adj[v]-colour.keys())
   c=max(allowed,key=lambda c:(score(c),-c))
  colour[v]=c
 C=set(colour);cut=sorted(set(free)-C)
 if not fixed|T<=C or not cut or any(colour[a]==colour[b] for a in C for b in adj[a]&C):raise ValueError('invalid extension witness')
 if 'cut' in witness and cut!=witness['cut']:raise ValueError('cut reconstruction mismatch')
 return colour,cut

def solve_four(n,ee):
 from pysat.solvers import Solver
 clauses=[]
 for v in range(n):
  clauses.append([4*v+c+1 for c in range(4)]);clauses.extend([-4*v-a-1,-4*v-b-1] for a in range(4) for b in range(a))
 for a,b in ee:clauses.extend([-4*a-c-1,-4*b-c-1] for c in range(4))
 clauses.append([1])
 with Solver(name='cadical153',bootstrap_with=clauses) as s:
  s.conf_budget(200000);ok=s.solve_limited();stats=s.accum_stats()
  if ok is not True:return ok,None,stats
  m=set(s.get_model());word=''.join(str(next(c for c in range(4) if 4*v+c+1 in m)) for v in range(n))
  if any(word[a]==word[b] for a,b in ee):raise ValueError('invalid decoded candidate word')
  return True,word,stats

def master_formula(adj,fixed,free,bound,witnesses):
 from pysat.card import CardEnc,EncType
 ix={v:i+1 for i,v in enumerate(free)};m=len(free);card=CardEnc.atmost(list(range(1,m+1)),bound=bound,top_id=m,encoding=EncType.seqcounter);clauses=list(card.clauses);top=card.nv;guards=[]
 for v in free:
  required=4-len(adj[v]&fixed)
  if required<=0:continue
  guards.append(v);lits=[ix[u] for u in sorted(adj[v]-fixed)]
  if required>len(lits):clauses.append([-ix[v]])
  else:
   c=CardEnc.atleast(lits,bound=required,top_id=top,encoding=EncType.seqcounter);top=c.nv;clauses.extend([[-ix[v]]+row for row in c.clauses])
 for w in witnesses:clauses.append([ix[v] for v in w['cut']])
 return clauses,top,ix,guards

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);p.add_argument('--kissat',required=True);p.add_argument('--resume',type=Path);p.add_argument('--iterations',type=int,default=100);p.add_argument('--seconds',type=int,default=900);p.add_argument('--query-seconds',type=int,default=90);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True);start=time.monotonic()
 pts,_=build.generate(False);ee=build.edges(pts);matching=record.compare(pts);fixed=set(matching['map'].values());free=sorted(set(range(len(pts)))-fixed);bound=508-len(fixed)
 if (len(fixed),bound)!=(503,5):raise ValueError('unexpected repair target')
 adj=[set() for _ in pts]
 for u,v in ee:adj[u].add(v);adj[v].add(u)
 witnesses=[];rounds=[]
 if a.resume:
  previous=json.loads(a.resume.read_text());witnesses=previous['witnesses']
  for w in witnesses:expand(w,adj,fixed,free)
 clauses,top,ix,guards=master_formula(adj,fixed,free,bound,witnesses);status='RUNNING'
 print(json.dumps({'stage':'start','host':len(pts),'fixed':len(fixed),'bound':bound,'guards':len(guards),'witnesses':len(witnesses),'variables':top,'clauses':len(clauses),'seconds':time.monotonic()-start}),flush=True)
 for iteration0 in range(a.iterations):
  iteration=10000+iteration0
  text=f'p cnf {top} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses);cnf=a.work/'master.cnf';cnf.write_text(text)
  with (a.work/'master.log').open('w') as f:r=subprocess.run([a.kissat,f'--time={a.query_seconds}',str(cnf),str(a.work/'master.drat')],stdout=f,stderr=subprocess.STDOUT)
  if r.returncode==20:status='MASTER_UNSAT_UNCHECKED';break
  if r.returncode==0:status='UNKNOWN_MASTER';break
  if r.returncode!=10:raise RuntimeError('master native exit '+str(r.returncode))
  positives={int(z) for line in (a.work/'master.log').read_text().splitlines() if line.startswith('v ') for z in line[2:].split() if int(z)>0}
  T={v for v in free if ix[v] in positives}
  if len(T)>bound or any(len(adj[v]&(fixed|T))<4 for v in T):raise ValueError('invalid master model')
  vs=sorted(fixed|T);where={v:i for i,v in enumerate(vs)};es=[(where[u],where[v]) for u,v in ee if u in where and v in where]
  ok,word,stats=solve_four(len(vs),es);row={'iteration':iteration,'selected':sorted(T),'n':len(vs),'e':len(es),'answer':str(ok),'stats':stats,'seconds':time.monotonic()-start};rounds.append(row);print(json.dumps(row),flush=True)
  if ok is not True:
   status='NONFOUR_SIGNAL' if ok is False else 'UNKNOWN_CANDIDATE';save(a.work/'candidate.json',{'vertices':vs,'edges':es,'status':str(ok)});candidate_cnf,_=build.cnf(len(vs),es);(a.work/'candidate.cnf').write_text(candidate_cnf);break
  for variant in range(3):
   w={'iteration':iteration,'variant':variant,'selected':sorted(T),'seed_word':word};colour,cut=expand(w,adj,fixed,free);w['cut']=cut;w['coloured_vertices']=len(colour);witnesses.append(w);clauses.append([ix[v] for v in cut])
  save(a.work/'progress.json',{'status':status,'fixed':sorted(fixed),'free':free,'bound':bound,'rounds':rounds,'witnesses':witnesses,'degree_guards':guards,'seconds':time.monotonic()-start})
  if time.monotonic()-start>=a.seconds:status='TIME_CHECKPOINT';break
 else:status='ITERATION_CHECKPOINT'
 save(a.work/'result.json',{'status':status,'fixed':sorted(fixed),'free':free,'bound':bound,'rounds':rounds,'witnesses':witnesses,'degree_guards':guards,'seconds':time.monotonic()-start,'master_variables':top,'master_clauses':len(clauses),'last_master_cnf_sha256':hashlib.sha256(text.encode()).hexdigest()})
 print(json.dumps({'stage':'done','status':status,'queries':len(rounds),'witnesses':len(witnesses),'seconds':time.monotonic()-start}),flush=True)
if __name__=='__main__':main()
