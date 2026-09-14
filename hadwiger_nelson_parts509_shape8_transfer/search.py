"""Isolated exact a=8 construction search. All mutable state stays in --work."""
from pathlib import Path
from itertools import combinations
from datetime import datetime, timezone
import argparse, importlib.util, json, hashlib, random, time, os, sys
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def need(ok, msg):
    if not ok: raise ValueError(msg)


def save(p, x):
    tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(x,indent=2)+'\n');tmp.replace(p)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def load_geometry(repo):
    p=repo/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py'
    spec=importlib.util.spec_from_file_location('accepted_geometry_reader',p)
    m=importlib.util.module_from_spec(spec)
    before=sys.dont_write_bytecode;sys.dont_write_bytecode=True
    try:spec.loader.exec_module(m)
    finally:sys.dont_write_bytecode=before
    den,points,vertices,U,edges=m.read_geometry()
    return den,points,list(vertices),list(U),list(edges)


def seed_clauses(repo,U):
    paths=[repo/'hadwiger_nelson_parts509_pool_shape_closure/killing_sets.json',
           repo/'hadwiger_nelson_parts509_s_replacement_budget/certificate.json',
           repo/'hadwiger_nelson_parts509_pool_shape6_verified/killing_clauses.cnf',
           repo/'hadwiger_nelson_parts509_pool_shape7_verified/killing_clauses.cnf',
           repo/'hadwiger_nelson_parts509_pool_cover_shrink01/colourings.json']
    rows=[]
    rows += [r['D'] for r in json.loads(paths[0].read_text())['sets']]
    rows += [r['D'] for r in json.loads(paths[1].read_text())['killing_sets']]
    for p in paths[2:4]:
        for line in p.read_text().splitlines()[1:]:
            q=list(map(int,line.split()));need(q[-1]==0 and all(1<=x<=303 for x in q[:-1]),'positive seed clause')
            rows.append([U[i-1] for i in q[:-1]])
    rows += [r['D'] for r in json.loads(paths[4].read_text())]
    need(all(r and set(r)<=set(U) for r in rows),'seed labels')
    return sorted(set(tuple(sorted(r)) for r in rows),key=lambda r:(len(r),r)),{str(p.relative_to(repo)):sha(p) for p in paths}


class Oracle:
    def __init__(self,U,edges,words):
        self.U=U;self.us=set(U);self.words=words;self.pos={v:i for i,v in enumerate(U)}
        self.adj={v:set() for v in range(374)}|{v:set() for v in U}
        for a,b in edges:self.adj[a].add(b);self.adj[b].add(a)
        self.edges=edges
        self.inner=[(self.pos[a],self.pos[b]) for a,b in edges if a in self.us and b in self.us]
        self.cross=[(a,self.pos[b]) if a<374 else (b,self.pos[a]) for a,b in edges if (a<374)!=(b<374)]
        base=[]
        for a,b in self.inner:
            for c in range(4):base.append([-self.act(a),-self.act(b)]+self.neq(a,c)+self.neq(b,c))
        self.solvers=[]
        for w in words:
            need(len(w)==374 and all(w[a]!=w[b] for a,b in edges if b<374),'L witness')
            clauses=base+[[-self.act(u)]+self.neq(u,int(w[l])) for l,u in self.cross]
            self.solvers.append(Solver(name='cadical195',bootstrap_with=clauses))
        self.calls=0;self.seconds=0;self.hits=[0]*20

    @staticmethod
    def act(i):return 607+i
    @staticmethod
    def neq(i,c):return [-(2*i+b+1) if c>>b&1 else 2*i+b+1 for b in range(2)]

    def check(self,X,p,c):
        need(len(c)==303 and set(c)<=set('.0123'),'pool word')
        need({v for v,t in zip(self.U,c) if t!='.'}==set(X),'word domain')
        col=dict(enumerate(self.words[p]));col.update({v:t for v,t in zip(self.U,c) if t!='.'})
        need(all(col[a]!=col[b] for a,b in self.edges if a in col and b in col),'physical colouring')

    def solve(self,X,p,budget):
        ass=[self.act(i) if v in X else -self.act(i) for i,v in enumerate(self.U)]
        s=self.solvers[p];s.conf_budget(budget);t=time.monotonic();ans=s.solve_limited(assumptions=ass)
        self.seconds+=time.monotonic()-t;self.calls+=1
        if ans is not True:return ans,None
        model=set(s.get_model());c=''.join(str(sum(1<<b for b in range(2) if 2*i+b+1 in model)) if v in X else '.' for i,v in enumerate(self.U))
        self.check(X,p,c);self.hits[p]+=1
        return True,c

    def find(self,X,budget,preferred=None):
        order=sorted(range(20),key=lambda p:(p!=preferred,-self.hits[p],p));unknown=False
        for p in order:
            a,c=self.solve(X,p,budget)
            if a is True:return True,p,c
            if a is None:unknown=True
        return (None if unknown else False),None,None

    def grow(self,X,p,c):
        col=dict(enumerate(self.words[p]));col.update({v:t for v,t in zip(self.U,c) if t!='.'})
        Y=set(X)
        for v in self.U:
            if v in Y:continue
            used={col[u] for u in self.adj[v] if u in col}
            for t in '0123':
                if t not in used:col[v]=t;Y.add(v);break
        c=''.join(col.get(v,'.') for v in self.U);self.check(Y,p,c)
        return Y,c

    def shrink(self,X,p,c,rng):
        Y,c=self.grow(X,p,c);D=self.us-Y
        order=sorted(D);rng.shuffle(order)
        for v in order:
            if v not in D:continue
            trial=self.us-(D-{v})
            ans,pp,cc=self.find(trial,20000,p)
            if ans is True:
                Y,c=self.grow(trial,pp,cc);D=self.us-Y;p=pp
        self.check(self.us-D,p,c)
        return sorted(D),p,c


def make_master(U,edges,seed,new):
    index={v:i+1 for i,v in enumerate(U)};ids=IDPool(start_from=304)
    clauses=[[index[v] for v in row] for row in seed+new]
    for lits,k in [([-index[v] for v in U[:135]],9),([index[v] for v in U[135:]],8)]:
        clauses.extend(CardEnc.equals(lits=lits,bound=k,vpool=ids,encoding=EncType.totalizer).clauses)
    adj={v:set() for v in range(374)}|{v:set() for v in U};us=set(U)
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    for w in U[135:]:
        need_count=4-len([v for v in adj[w] if v<374]);nb=sorted(adj[w]&us)
        if need_count<=0:continue
        if need_count>len(nb):clauses.append([-index[w]]);continue
        cs=CardEnc.atmost(lits=[-index[v] for v in nb],bound=len(nb)-need_count,vpool=ids,encoding=EncType.totalizer).clauses
        clauses.extend([[-index[w]]+q for q in cs])
    return ids.top,clauses,index,adj


def write_cnf(path,nv,clauses):
    with path.open('w') as f:
        f.write(f'p cnf {nv} {len(clauses)}\n')
        for c in clauses:f.write(' '.join(map(str,c))+' 0\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--work',type=Path,required=True);ap.add_argument('--seconds',type=int,default=3600);ap.add_argument('--seed',type=int,default=20260914);args=ap.parse_args()
    w=args.work;w.mkdir(parents=True,exist_ok=True);start=time.monotonic();rng=random.Random(args.seed)
    print('exact geometry preflight',flush=True)
    den,points,vertices,U,edges=load_geometry(args.repo)
    save(w/'geometry.json',{'denominator':den,'vertices':vertices,'points':[[v,points[v]] for v in vertices],'U':U,'edges':edges})
    interface_path=args.repo/'hadwiger_nelson_parts509_interface_lemma/interface_L.json'
    need(sha(interface_path)=='a160340461815e57c46936fb7d0001b74881fe753d904a5ddc7fb866cfc29637','source interface hash')
    source=json.loads(interface_path.read_text())
    need({a if a<374 else b for a,b in edges if (a<374)!=(b<374)}==set(source['interface_L']),'complete pool interface')
    words=[x['witness_colouring_L'] for x in source['classes']]
    need(len(words)==20,'interface class count')
    oracle=Oracle(U,edges,words);seed,hashes=seed_clauses(args.repo,U)
    save(w/'preflight.json',{'points':677,'unit_edges':3400,'denominator':den,'selected_S':126,'selected_Q5':8,'merged_selection_order':508,'L_unchanged':True,'physical_preflight_passed':True,'seed_clauses':len(seed),'seed_source_hashes':hashes,'geometry_sha256':sha(w/'geometry.json')})
    new=[];records=[]
    if (w/'cuts.jsonl').exists():
        for line in (w/'cuts.jsonl').read_text().splitlines():
            r=json.loads(line);D=r['D'];oracle.check(set(U)-set(D),r['p'],r['c']);new.append(D);records.append(r)
    seen=set(seed)|{tuple(r) for r in new}
    nv,clauses,index,adj=make_master(U,edges,seed,new)
    # Validate requested cardinalities on each decoded model; positive witness
    # checks are definition-level, independent of all SAT encodings.
    rounds=len(records);status='RUNNING';best=None
    if (w/'best.json').exists():best=json.loads((w/'best.json').read_text())
    def checkpoint(stage,**extra):
        out={'status':stage,'pid':os.getpid(),'updated_utc':datetime.now(timezone.utc).isoformat(),'rounds':rounds,'seed_clauses':len(seed),'new_cuts':len(new),'oracle_calls':oracle.calls,'oracle_seconds':round(oracle.seconds,3),'elapsed_seconds':round(time.monotonic()-start,3),'best_allowed_classes':best['allowed_count'] if best else None,'record_signal':False,**extra}
        save(w/'checkpoint.json',out)
        print(json.dumps(out),flush=True)
    # Input/decoder calibration: empty driver, original S with one deletion.
    for X in [set(),set(U[:134])]:
        a,p,c=oracle.find(X,200000)
        need(a is True,'known positive calibration');oracle.check(X,p,c)
    checkpoint('PREFLIGHT_AND_POSITIVE_CALIBRATION_PASS')
    with Solver(name='cadical195',bootstrap_with=clauses) as master,(w/'cuts.jsonl').open('a',buffering=1) as cuts:
        while time.monotonic()-start<args.seconds:
            checkpoint('MASTER_SOLVING')
            master.conf_budget(2000000);ans=master.solve_limited()
            if ans is not True:
                write_cnf(w/'master.cnf',nv,clauses);status='MASTER_UNSAT_UNCERTIFIED' if ans is False else 'MASTER_UNKNOWN'
                checkpoint(status,master_sha256=sha(w/'master.cnf'));break
            model=set(master.get_model());X={v for v in U if index[v] in model}
            need(len(X)==134 and len(X&set(U[:135]))==126 and len(X&set(U[135:]))==8,'decoded counts')
            need(all(len(adj[v]&(set(range(374))|X))>=4 for v in X if v>=509),'decoded degree condition')
            save(w/'current_selection.json',{'X':sorted(X),'R':sorted(set(U[:135])-X),'A':sorted(X&set(U[135:])),'order':508})
            a,p,c=oracle.find(X,200000)
            if a is not True:
                status='INTERFACE_NONFOUR_SIGNAL' if a is False else 'ORACLE_UNKNOWN'
                checkpoint(status,selection_sha256=sha(w/'current_selection.json'));break
            # Census of this capped physical support (not a Boolean model claim).
            allowed=[];witnesses=[];unknown=[]
            for k in range(20):
                answer,word=oracle.solve(X,k,200000)
                if answer is True:allowed.append(k);witnesses.append({'p':k,'c':word})
                elif answer is None:unknown.append(k)
            if best is None or (len(allowed)+len(unknown),len(unknown))<(best['allowed_count']+len(best['unknown']),len(best['unknown'])):
                best={'X':sorted(X),'allowed':allowed,'allowed_count':len(allowed),'unknown':unknown,'positive_words':witnesses,'complete_negative_certificates':False,'edges':sum(a in set(range(374))|X and b in set(range(374))|X for a,b in edges)}
                save(w/'best.json',best)
            D,pp,cc=oracle.shrink(X,p,c,rng)
            need(not (X&set(D)),'cut excludes tested selection')
            need(tuple(D) not in seen,'new selection already excluded')
            row={'D':D,'p':pp,'c':cc,'excluded_X':sorted(X),'allowed_classes':allowed,'unknown_classes':unknown}
            cuts.write(json.dumps(row,separators=(',',':'))+'\n');cuts.flush();os.fsync(cuts.fileno())
            records.append(row);new.append(D);seen.add(tuple(D));cl=[index[v] for v in D];master.add_clause(cl);clauses.append(cl);rounds+=1
            checkpoint('CHECKED_SELECTION_AND_NEW_COLOURING_CUT',cut_size=len(D),allowed=len(allowed),unknown=len(unknown))
        else:
            status='TIME_CHECKPOINT';write_cnf(w/'master.cnf',nv,clauses);checkpoint(status,master_sha256=sha(w/'master.cnf'))
    for s in oracle.solvers:s.delete()
    save(w/'result.json',{'status':status,'rounds':rounds,'new_cuts':len(new),'elapsed_seconds':time.monotonic()-start,'record_certified':False})


if __name__=='__main__':main()
