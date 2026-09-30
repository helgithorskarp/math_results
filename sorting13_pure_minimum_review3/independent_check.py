#!/usr/bin/env python3
"""Independent L16 audit. Python 3.11 standard library; no author imports.

Provide a scratch/repository root containing the published input directories.
The exact CNF layout is reproduced so the existing source RUP certificate applies.
Propagation uses literal occurrences, remaining counts and XOR, not watched literals.
"""
from collections import Counter,deque
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse,json,time

HERE=Path(__file__).resolve().parent
PAIRS=tuple(combinations(range(9),2))
LOWER=[0,0,1,3,5,9,12,16,19,25,29,35]
PINS={'sorting13_maximum_preparation/fixture.json': '6e319b54ce58a437fd4b3146aa063c6286aad31f0d4688460bd361c805e19185', 'sorting13_maximum_preparation/min0-closure.json': 'b7a52fd2c3b2338f9fd079700b70599baec969d5e4cc503494ef7ac370e49fb9', 'sorting13_maximum_preparation/core.cnf': '7a78eeb6441a0e43e6399d30f8cb0faf27ad5f18ec2366107b1da78ecc1fc9ad', 'sorting13_maximum_preparation/proof.rup': '4c4308b756f6cf641322e08a19334564bb41ffbc20758aa2ae21d43cc60dd83f', 'sorting13_double_pure_obstruction/fixture.json': 'be55487f88b04341ebd9416af4d44e5813e1c09d4548f1a50ad227d853f08891', 'sorting13_double_pure_obstruction/closure.json': 'a40402d3ccec1c8a05f872ad80151ae9a1a1aaeafe74b36fc0a289fe5978cd4a'}
COMPLETE_PINS = {k:v for k,v in PINS.items() if k not in ('sorting13_maximum_preparation/core.cnf','sorting13_maximum_preparation/proof.rup')}
COMPLETE_PINS.update({'sorting13_pure_minimum_exclusion/additional_witnesses.json':'d415bfa839e1ff75d82d5d476d10049e1b4f1c5f1945b8e3f34ed0a741fe786f','sorting13_pure_minimum_exclusion/core.cnf':'fed63e0fce0629399ae5ccb901f926d60bad57ddffd721d9359d7c2ebb148989','sorting13_pure_minimum_exclusion/proof.rup':'db2fbd1257789f51eb810591e776abf2ebbabcb051af6e39db7899e7eb93f061'})
def require(ok,label):
    if not ok:raise ValueError(label)
def digest(data):return sha256(data).hexdigest()
def canonical(rows):return digest(json.dumps(rows,sort_keys=True,separators=(',',':')).encode())
def cmpmask(mask,pair):
    a,b=pair
    if mask>>a&1 and not(mask>>b&1):mask^=(1<<a)|(1<<b)
    return mask
def runmask(mask,word):
    for pair in word:mask=cmpmask(mask,pair)
    return mask
def sortmask(mask,n):return ((1<<mask.bit_count())-1)<<(n-mask.bit_count())
def prefixmask(mask,f,after=None):
    mask=runmask(mask,f['prefix'])
    mask=sum(((mask>>i)&1)<<j for j,i in enumerate(f['prefix_output_order']))
    return runmask(mask,f['after'] if after is None else after)

def packed_witness(f,w,after,slice_wires):
    """Erase colored extreme wires; compare all free Boolean assignments in parallel."""
    hi=set(w['fixed_high']);lo=set(w['fixed_low'])
    require(not(hi&lo),'disjoint marker classes')
    free=[i for i in range(11) if i not in hi|lo];m=len(free);size=1<<m
    require(m==w['middle_count'] and w['cap']==35-LOWER[m]-w['deleted'],'marker budget')
    columns=[sum(((a>>j)&1)<<a for a in range(size)) for j in range(m)]
    full=(1<<size)-1
    colors=[2 if i in hi else 0 if i in lo else 1 for i in range(11)]
    ports=[free.index(i) if i in free else None for i in range(11)]
    functions=[full if i in hi else 0 if i in lo else columns[free.index(i)] for i in range(11)]
    reduced=columns[:];deleted=0
    for stage,word in enumerate((f['prefix'],after)):
        for a,b in word:
            if colors[a]==colors[b]==1:
                pa,pb=ports[a],ports[b]
                reduced[pa],reduced[pb]=reduced[pa]&reduced[pb],reduced[pa]|reduced[pb]
            else:deleted+=1
            functions[a],functions[b]=functions[a]&functions[b],functions[a]|functions[b]
            if colors[a]>colors[b]:
                colors[a],colors[b]=colors[b],colors[a]
                ports[a],ports[b]=ports[b],ports[a]
        if stage==0:
            order=f['prefix_output_order']
            colors=[colors[i] for i in order];ports=[ports[i] for i in order]
            functions=[functions[i] for i in order]
    require(deleted==w['deleted'],'prefix deletion count')
    require(all(functions[i]==reduced[ports[i]] for i in range(11) if colors[i]==1),
            'packed erased-port correspondence')
    require(sum((colors[i]==2)<<j for j,i in enumerate(slice_wires))==w['x'],'high threshold')
    require(sum((colors[i]!=0)<<j for j,i in enumerate(slice_wires))==w['y'],'nonlow threshold')
    return size

def structure(f,binary):
    require(f['lower_sizes']==LOWER and len(f['prefix'])==14,'baseline fixture')
    K=set();L=set()
    for state in range(2048):
        k=prefixmask(state,f,f['K_after']);ell=prefixmask(state,f)
        require((k>>10)==int(state!=0),'prefix maximum')
        require((ell&1)==int(state==2047) and ell>>10==int(state!=0),'prefix extrema')
        K.add(k&1023);L.add((ell>>1)&511)
        require(runmask(ell,[[a+1,b+1] for a,b in f['control18']])==sortmask(state,11),'full positive control')
    require(sorted(L)==f['states'] and len(L)==109,'exact L image')
    require(sorted(K)==f['K_states'] and len(K)==127,'exact K image')
    witnesses=list({(w['x'],w['y']):w for w in
       f['critical_single_bounds']+f['selected_mixed_bounds']+f['designated_bounds']}.values())
    packed=sum(packed_witness(f,w,f['after'],range(1,10)) for w in witnesses)
    caps={(w['x'],w['y']):w['cap'] for w in witnesses}
    require([caps[1<<i,511] for i in (3,4,5,7,8)]==[4,4,2,4,1],'maximum capacities')
    require(caps[288,510]==4,'stationary minimum mixed capacity')
    # Include the earlier binary-only exclusions without accepting their counts.
    images=[];extra_packed=0
    for case in binary['cases']:
        word=case['maximum_prefix']
        require(all((runmask(s,word)>>8)==int(s!=0) for s in L),
                'binary front fixes the global L maximum')
        image=sorted({runmask(s,word)&255 for s in L})
        require(image==case['states'],'binary maximum image')
        require({32,64,128,254,160,case['two_one_test']}<=set(image),'binary exclusion rows')
        after=f['after']+[[a+1,b+1] for a,b in word]
        for w in case['witnesses']:extra_packed+=packed_witness(f,w,after,range(1,9))
        images.append(len(image))
    # Live-group DFS has no imposed kernel-word length.
    words=[]
    def dfs(pos,cost,word):
        if pos==(7,7,7):
            words.append(word);return
        for pair in combinations((1,2,3,4,6,7),2):
            active=[p in pair for p in pos]
            if not any(active):continue
            c=tuple(a+b for a,b in zip(cost,active))
            if max(c)>2:continue
            nxt=tuple(pair[1] if p in pair else p for p in pos)
            dfs(nxt,c,word+(pair,))
    dfs((3,4,7),(0,0,0),())
    require(Counter(map(len,words))=={2:3,3:21},'complete DFS kernel cover')
    full=[w+((5,7),(7,8)) for w in words if len(w)==3]
    require(set(full)=={tuple(map(tuple,w)) for w in f['maximum_kernel_words']},'all kernel entries')
    for word in full:
        pos=(3,4,5,7,8);cost=[0]*5;types=Counter()
        for pair in word:
            live=set(pos);types[len(live&set(pair))]+=1
            for i,p in enumerate(pos):cost[i]+=p in pair
            pos=tuple(pair[1] if p in pair else p for p in pos)
        require(cost==[4,4,2,4,1] and types=={2:4,1:1} and pos==(8,)*5,'exact kernel passages')
    return {'original_boolean_inputs':2048,'L_states':109,'K_states':127,
            'packed_marker_witnesses':len(witnesses),'packed_free_assignments':packed,
            'binary_pruning_assignments':extra_packed,'binary_images':images,
            'kernel_words_by_events':{'4':3,'5':21},
            'kernel_entry_digest':canonical([list(map(list,w)) for w in sorted(full)])}

def closure(fixture,kind):
    """Rebuild all reachable Boolean executions; compare every source state."""
    n=9 if kind=='min0' else 8
    if kind=='min0':
        initial=(1<<5,1<<7,511^(1<<1),288,40,0,0,0,0)
    else:
        initial=None
    def convert(s):
        if kind=='min0':
            return (1<<s[0],1<<s[1],511^(1<<s[2]),*s[3:])
        return (1<<s[0],1<<s[1],255^(1<<s[2]),*s[3:])
    initials=[initial] if initial else [convert(s) for s in fixture['initials']]
    seen=set(initials);todo=deque(initials);allowed=transitions=terminals=0
    while todo:
        s=todo.popleft()
        if kind=='min0':
            r5,r7,lo,h,test,q5,q8,union,q0=s
            terminals+= (r5,r7,lo,h,test,q0)==(256,256,510,384,384,2)
        else:
            r5,r6,lo,h,test,u1,u2=s
            terminals+= (r5,r6,lo,h,test)==(128,128,254,192,192)
        for pair in combinations(range(n),2):
            transitions+=1;a,b=pair;endpoint=(1<<a)|(1<<b)
            if kind=='min0':
                nq5=q5+bool(r5&endpoint);nq8=q8+int(8 in pair)
                nu=union+bool(h&endpoint or 0 in pair)
                if nq5>2 or nq8>1 or nu>4:continue
                nxt=tuple(cmpmask(r,pair) for r in (r5,r7,lo,h,test))+(nq5,nq8,nu,min(2,q0+int(0 in pair)))
            else:
                nu1=u1+int(0 in pair or 7 in pair);nu2=u2+bool(h&endpoint or 0 in pair)
                if nu1>2 or nu2>3:continue
                nxt=tuple(cmpmask(r,pair) for r in (r5,r6,lo,h,test))+(nu1,nu2)
            allowed+=1
            if nxt not in seen:seen.add(nxt);todo.append(nxt)
    expected={convert(s) for s in fixture['states']}
    require(len(expected)==len(fixture['states']) and seen==expected,'all reachable closure entries '+kind)
    require(terminals==0,'no reachable forbidden terminal '+kind)
    return {'states':len(seen),'transitions':transitions,'allowed':allowed,
            'terminals':terminals,'reachable_state_digest':canonical(sorted(seen))}

class Formula:
    """Independent streaming reproduction of the documented CNF layout."""
    def __init__(self,core,variables,clauses):
        self.variables=0;self.clauses=0;self.hasher=sha256()
        header=f'p cnf {variables} {clauses}'
        self.full_hasher=sha256((header+' '*(100-len(header))+'\n').encode())
        self.needed=set(core);self.by_group=Counter();self.group='base'
        self.core_groups={};self.core_witnesses=Counter()
    def var(self):
        self.variables+=1;return self.variables
    def emit(self,*lits):
        if True in [v for v in lits if isinstance(v,bool)]:return
        row=tuple(dict.fromkeys(v for v in lits if v is not False))
        if any(-v in row for v in row):return
        self.clauses+=1;self.by_group[self.group]+=1
        raw=(' '.join(map(str,row))+' 0\n').encode()
        self.hasher.update(raw);self.full_hasher.update(raw)
        key=tuple(sorted(row))
        if key in self.needed:
            self.needed.remove(key);self.core_groups[key]=self.group
    def one(self,row):
        self.emit(*row)
        aux=[self.var() for _ in row[:-1]]
        if not aux:return
        self.emit(-row[0],aux[0])
        for i in range(1,len(row)-1):
            self.emit(-row[i],aux[i]);self.emit(-aux[i-1],aux[i]);self.emit(-row[i],-aux[i-1])
        self.emit(-row[-1],-aux[-1])
    def either(self,out,row):
        self.emit(-out,*row)
        for lit in row:self.emit(flip(lit),out)
    def cap(self,row,k):
        if k>=len(row):return
        if k<0:self.emit();return
        if k==0:
            for lit in row:self.emit(flip(lit))
            return
        aux=[[self.var() for _ in range(k)] for _ in row[:-1]]
        self.emit(flip(row[0]),aux[0][0])
        for j in range(1,k):self.emit(-aux[0][j])
        for i in range(1,len(row)-1):
            self.emit(flip(row[i]),aux[i][0])
            for j in range(k):self.emit(-aux[i-1][j],aux[i][j])
            for j in range(1,k):self.emit(flip(row[i]),-aux[i-1][j-1],aux[i][j])
        for i in range(1,len(row)):self.emit(flip(row[i]),-aux[i-1][-1])
def flip(v):return not v if isinstance(v,bool) else -v

def regenerate(f,core,preparation=False):
    dimensions=(23197,455027) if preparation else (34194,726755)
    expected_hash='fce6e10203ef60b1b6ff331eba0ff70a24f5b99bcada3f281a9c2f260e764b5b' if preparation else '4fb7cabafebaa7a4287be430eec234ae5d59aa048d92bb99bb5c4a141c3d7875'
    w=Formula(core,*dimensions);g=16;n=9;pairs=PAIRS
    choice=[[w.var() for _ in pairs] for t in range(g)]
    low=[[w.var() for i in range(n)] for t in range(g)]
    high=[[w.var() for i in range(n)] for t in range(g)]
    for t in range(g):
        w.one(choice[t])
        for i in range(n):
            w.either(low[t][i],[choice[t][j] for j,(a,b) in enumerate(pairs) if a==i])
            w.either(high[t][i],[choice[t][j] for j,(a,b) in enumerate(pairs) if b==i])
    bits={}
    for s in f['states']:
        w.group='row:'+str(s)
        frames=[[bool(s>>i&1) for i in range(n)]]
        frames+=[[w.var() for i in range(n)] for t in range(g-1)]
        target=sortmask(s,n);frames.append([bool(target>>i&1) for i in range(n)]);bits[s]=frames
        for t in range(g):
            x,y=frames[t:t+2]
            for i in range(n):
                w.emit(low[t][i],high[t][i],flip(x[i]),y[i])
                w.emit(low[t][i],high[t][i],x[i],flip(y[i]))
                w.emit(-low[t][i],flip(y[i]),x[i]);w.emit(-high[t][i],flip(x[i]),y[i])
            for j,(a,b) in enumerate(pairs):
                c=choice[t][j]
                w.emit(-c,flip(y[a]),x[b]);w.emit(-c,y[a],flip(x[a]),flip(x[b]))
                w.emit(-c,y[b],flip(x[a]));w.emit(-c,flip(y[b]),x[a],x[b])
    witnesses=list({(r['x'],r['y']):r for r in
         f['critical_single_bounds']+f['selected_mixed_bounds']+f['designated_bounds']}.values())
    events={}
    for row in witnesses:
        x,y=row['x'],row['y'];w.group='witness:'+str(x)+':'+str(y)
        hits=[w.var() for t in range(g)]
        for t in range(g):
            for j,(a,b) in enumerate(pairs):
                c=choice[t][j];outside=[bits[x][t][a],bits[x][t][b],flip(bits[y][t][a]),flip(bits[y][t][b])]
                for v in outside:w.emit(-c,flip(v),hits[t])
                w.emit(-c,-hits[t],*outside)
        w.cap(hits,row['cap']);events[x,y]=hits
    w.group='sole0'
    w.one([choice[t][pairs.index((0,1))] for t in range(g)])
    for t in range(g):
        for j,pair in enumerate(pairs):
            if 0 in pair and pair!=(0,1):w.emit(-choice[t][j])
    w.group='phase'
    phases=[[w.var() for i in range(3)] for t in range(g+1)]
    for p in phases:w.one(p)
    w.emit(phases[0][0]);w.emit(phases[-1][2])
    for t in range(g):
        for s in range(3):
            for j,pair in enumerate(pairs):
                if s==0:dest=1 if pair==(5,7) else 0 if 5 not in pair and 8 not in pair else None
                elif s==1:dest=2 if pair==(7,8) else 1 if 7 not in pair and 8 not in pair else None
                else:dest=2 if 8 not in pair else None
                if dest is None:w.emit(-phases[t][s],-choice[t][j])
                else:w.emit(-phases[t][s],-choice[t][j],phases[t+1][dest])
    w.group='refill';post=[];early67=[]
    for t in range(g):
        inc=w.var();w.either(inc,[choice[t][j] for j,(a,b) in enumerate(pairs) if b==7])
        p=w.var();post.append(p)
        w.emit(-p,phases[t][2]);w.emit(-p,inc);w.emit(p,-phases[t][2],-inc)
        for j,(a,b) in enumerate(pairs):
            if b==7 and a<5:w.emit(-phases[t][2],-choice[t][j])
        e=w.var();early67.append(e);c=choice[t][pairs.index((6,7))]
        w.emit(-e,phases[t][0]);w.emit(-e,c);w.emit(e,-phases[t][0],-c)
    w.one(post);early=w.var();w.either(early,early67)
    for t in range(g):w.emit(-phases[t][2],-choice[t][pairs.index((5,7))],early)
    w.group='exact_passages'
    for i,k in zip((3,4,5,7,8),(4,4,2,4,1)):
        w.cap([flip(v) for v in events[1<<i,511]],g-k)
    w.group='kernel_count';kernel=[w.var() for t in range(g)]
    for t in range(g):w.either(kernel[t],[events[1<<i,511][t] for i in (3,4,5,7,8)])
    w.cap(kernel,5);w.cap([flip(v) for v in kernel],g-5)
    if preparation:
        w.group='root_by_six';w.emit(*[choice[t][pairs.index((7,8))] for t in range(6)])
    require(not w.needed,'every core clause belongs to regenerated source formula')
    require((w.variables,w.clauses)==dimensions,'exact formula dimensions')
    require(w.full_hasher.hexdigest()==expected_hash,'complete source formula digest')
    header=f'p cnf {w.variables} {w.clauses}'
    # Keep the source's padded header while streaming only the clause body.
    return w, (header+' '*(100-len(header))+'\n').encode()

class OccurrenceRUP:
    """Exact local counters with XOR remaining literals; no watched pairs."""
    def __init__(self,n,clauses):
        self.n=n;self.rows=[];self.occ=[[] for _ in range(2*n+2)];self.units=[];self.xors=[]
        self.base=bytearray(n+1);self.base_count=[];self.base_xor=[]
        self.base_satisfied=bytearray();self.base_queue=[];self.base_head=0;self.base_conflict=False
        for clause in clauses:self.add(clause)
    def add(self,clause):
        encoded=tuple((abs(x)<<1)|int(x<0) for x in clause)
        require(all(1<=abs(x)<=self.n for x in clause),'literal domain')
        index=len(self.rows);self.rows.append(encoded);self.xors.append(0)
        for e in encoded:self.occ[e].append(index);self.xors[-1]^=e
        if len(encoded)<=1:self.units.append(encoded[0] if encoded else 0)
        remaining=[e for e in encoded if not self.base[e>>1]]
        satisfied=any(self.base[e>>1]==1+(e&1) for e in encoded)
        self.base_count.append(len(remaining));x=0
        for e in remaining:x^=e
        self.base_xor.append(x);self.base_satisfied.append(satisfied)
        if not satisfied and len(remaining)<=1:self.base_queue.append(x)
    def root_closure(self):
        """Cache only unit consequences of the current formula, without assumptions."""
        while self.base_head<len(self.base_queue) and not self.base_conflict:
            e=self.base_queue[self.base_head];self.base_head+=1
            if e==0:self.base_conflict=True;break
            var=e>>1;value=1+(e&1)
            if self.base[var]:
                if self.base[var]!=value:self.base_conflict=True
                continue
            self.base[var]=value
            for c in self.occ[e]:self.base_satisfied[c]=1
            for c in self.occ[e^1]:
                if self.base_satisfied[c]:continue
                self.base_count[c]-=1;self.base_xor[c]^=e^1
                if self.base_count[c]<=1:self.base_queue.append(self.base_xor[c])
    def rup(self,clause):
        self.root_closure()
        if self.base_conflict:return True
        assignment=self.base.copy();queue=[((abs(x)<<1)|int(x>0)) for x in clause]
        count={};remaining={};satisfied=set();head=0
        while head<len(queue):
            e=queue[head];head+=1
            if e==0:return True
            var=e>>1;value=1+(e&1)
            if assignment[var]:
                if assignment[var]!=value:return True
                continue
            assignment[var]=value
            satisfied.update(c for c in self.occ[e] if not self.base_satisfied[c])
            for c in self.occ[e^1]:
                if self.base_satisfied[c] or c in satisfied:continue
                k=count.get(c,self.base_count[c])-1;count[c]=k
                x=remaining.get(c,self.base_xor[c])^(e^1);remaining[c]=x
                if k==0:return True
                if k==1:queue.append(x)
        return False

def parse_cnf(raw):
    lines=raw.decode().splitlines();h=lines[0].split();require(h[:2]==['p','cnf'],'CNF header')
    n,k=map(int,h[2:]);rows=[]
    for line in lines[1:]:
        row=list(map(int,line.split()));require(row and row[-1]==0,'CNF terminator')
        clause=tuple(sorted(set(row[:-1])));require(all(0<abs(v)<=n for v in clause),'CNF variables')
        require(not any(-v in clause for v in clause),'no core tautology')
        rows.append(clause)
    require(len(rows)==k,'CNF clause count');return n,rows

def proof_check(n,core,raw,expected_count=13084):
    checker=OccurrenceRUP(n,core)
    require(not checker.rup(()),'premature empty rejected')
    count=0;empty=False
    for lineno,line in enumerate(raw.decode().splitlines(),1):
        tokens=line.split();require(tokens and tokens[0]!='d','addition-only RUP')
        row=list(map(int,tokens));require(row[-1]==0 and 0 not in row[:-1],'RUP terminator')
        clause=tuple(sorted(set(row[:-1])))
        require(not empty,'empty clause must be last')
        require(checker.rup(clause),'invalid RUP addition '+str(lineno))
        checker.add(clause);count+=1;empty=not clause
    require(empty,'refutation reaches empty')
    require(count==expected_count,'all proof additions')
    return {'additions':count,'deletions':0,'premature_empty_rejected':True}

def propagation_controls():
    # Hand-built formulas distinguish RUP from full semantic entailment.
    cases=[(3,[(1,),(-1,2),(-2,3)],(3,),True),
           (3,[(1,),(-1,2),(-2,3)],(-3,),False),
           (2,[(1,2),(-1,2),(1,-2)],(2,),True),
           (2,[(1,2),(-1,2),(1,-2)],(-2,),False),
           (2,[(1,2),(-1,2),(1,-2),(-1,-2)],(),False),
           (2,[(1,),(-1,)],(),True),
           (2,[(1,2)],(1,-1),True),
           (2,[],(1,),False)]
    for n,clauses,candidate,wanted in cases:
        require(OccurrenceRUP(n,clauses).rup(candidate)==wanted,'RUP boundary control')
        if wanted:
            for assignment in range(1<<n):
                truth=lambda lit:bool(assignment>>(abs(lit)-1)&1)==(lit>0)
                require(not all(any(truth(x) for x in c) for c in clauses)
                        or any(truth(x) for x in candidate),'RUP implies semantic entailment')
    return len(cases)

def cached_propagation_controls():
    """Compare incremental caching with a clause-scanning reference on tiny CNFs."""
    import random
    from itertools import product
    def reference(rows,candidate):
        true=set()
        pending=[-x for x in candidate]
        while True:
            while pending:
                lit=pending.pop()
                if -lit in true:return True
                true.add(lit)
            for row in rows:
                if any(x in true for x in row):continue
                remaining=[x for x in row if -x not in true]
                if not remaining:return True
                if len(remaining)==1 and remaining[0] not in true:pending.append(remaining[0])
            if not pending:return False
    universe=[tuple((i+1)*v for i,v in enumerate(row) if v) for row in product((-1,0,1),repeat=3)]
    rng=random.Random(74747510);checks=0
    for _ in range(512):
        rows=rng.sample([c for c in universe if c],rng.randrange(7))
        checker=OccurrenceRUP(3,rows)
        for _ in range(6):
            candidate=rng.choice(universe+[(1,-1),(2,-2),(3,-3)])
            actual=checker.rup(candidate);wanted=reference(rows,candidate)
            require(actual==wanted,'cached versus clause-scanning propagation')
            checks+=1
            if actual:
                for assignment in range(8):
                    truth=lambda lit:bool(assignment>>(abs(lit)-1)&1)==(lit>0)
                    require(not all(any(truth(x) for x in c) for c in rows)
                            or any(truth(x) for x in candidate),'cached RUP semantic entailment')
                checker.add(candidate);rows.append(candidate)
    return checks

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('source_root',type=Path)
    ap.add_argument('--write',action='store_true');ap.add_argument('--preparation',action='store_true');args=ap.parse_args();start=time.monotonic()
    pins=PINS if args.preparation else COMPLETE_PINS
    raw={}
    for p,h in pins.items():
        data=(args.source_root/p).read_bytes();require(digest(data)==h,'SHA-pinned input '+p);raw[p]=data
    f=json.loads(raw['sorting13_maximum_preparation/fixture.json'])
    binary=json.loads(raw['sorting13_double_pure_obstruction/fixture.json'])
    structural=structure(f,binary)
    zero=closure(json.loads(raw['sorting13_maximum_preparation/min0-closure.json']),'min0')
    binary_closed=closure(json.loads(raw['sorting13_double_pure_obstruction/closure.json']),'binary')
    if not args.preparation:
        extra=json.loads(raw['sorting13_pure_minimum_exclusion/additional_witnesses.json'])
        old={(r['x'],r['y']) for r in f['critical_single_bounds']+f['selected_mixed_bounds']+f['designated_bounds']}
        require(len(extra)==92 and len({(r['x'],r['y']) for r in extra})==92,'92 distinct extra witnesses')
        require(not old & {(r['x'],r['y']) for r in extra},'additional witness disjointness')
        require(all(r['cap']<=8 and r['x'] in f['states'] and r['y'] in f['states'] for r in extra),'extra witness scope')
        structural['additional_marker_witnesses']=92
        structural['additional_packed_free_assignments']=sum(packed_witness(f,r,f['after'],range(1,10)) for r in extra)
        f=dict(f,selected_mixed_bounds=f['selected_mixed_bounds']+extra)
    target='sorting13_maximum_preparation' if args.preparation else 'sorting13_pure_minimum_exclusion'
    n,core=parse_cnf(raw[target+'/core.cnf'])
    formula,header=regenerate(f,core,args.preparation)
    proof=proof_check(n,core,raw[target+'/proof.rup'],5298 if args.preparation else 13084)
    controls=propagation_controls()
    cached_controls=cached_propagation_controls()
    result={'reviewer':'six-reviewer-3','role':'independent mathematical reviewer',
            'structure':structural,'min0_reachable_closure':zero,'binary_reachable_closure':binary_closed,
            'CNF':{'variables':formula.variables,'clauses':formula.clauses,
                   'sha256':formula.full_hasher.hexdigest(),
                   'clause_body_sha256':formula.hasher.hexdigest(),
                   'header_sha256':digest(header),'all_core_clauses_members':True,
                   'core_groups':dict(sorted(Counter(formula.core_groups.values()).items()))},
            'RUP':proof,'propagation_controls':controls,'cached_propagation_controls':cached_controls,
            'inputs':pins,'analytic_bridges_formalized':False}
    expected=HERE/('expected-preparation.json' if args.preparation else 'expected.json')
    text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.write:expected.write_text(text)
    else:require(json.loads(expected.read_text())==result,'every expected field matches')
    print(text,end='');print('Elapsed seconds:',round(time.monotonic()-start,3))
if __name__=='__main__':main()
