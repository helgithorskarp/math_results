"""Exact, solver-free verifier for the shortcut construction's certificate.

No discovery code is imported. The reduction is rebuilt from simple paths
and connected components of the explicit graph. All arithmetic is rational.
"""
from collections import deque
from fractions import Fraction
from itertools import combinations
from math import gcd,lcm
from functools import reduce
from hashlib import sha256
from pathlib import Path
import argparse,copy,json,sys

HERE=Path(__file__).resolve().parent


def edge(a,b):return tuple(sorted((a,b)))


def normalized(vector):
    q=list(map(Fraction,vector));scale=lcm(*(x.denominator for x in q))
    ints=[int(x*scale) for x in q];div=reduce(gcd,map(abs,ints))
    return tuple(x//div for x in ints) if div else tuple(ints)


class Encoding:
    def __init__(self):self.next=1;self.linear={};self.vector={};self.clauses=[]
    def new(self):
        result=self.next;self.next+=1;return result
    def atom(self,vector):
        v=normalized(vector)
        if not any(v[:-1]):return v[-1]>=0
        if v not in self.linear:
            index=self.new();self.linear[v]=index;self.vector[index]=v
        return self.linear[v]
    @staticmethod
    def negate(lit):return not lit if type(lit) is bool else -lit
    def inequality(self,vector,strict=False):
        if strict:return self.negate(self.atom([-q for q in vector]))
        return self.atom(vector)
    def add(self,clause):
        if any(x is True for x in clause):return
        c=set(x for x in clause if x is not False)
        if any(-x in c for x in c):return
        self.clauses.append(tuple(sorted(c)))


def components(adj,removed):
    left=set(range(len(adj)))-set(removed);out=[]
    while left:
        root=min(left);left.remove(root);part={root};todo=[root]
        while todo:
            v=todo.pop();new=adj[v]&left;left-=new;part|=new;todo.extend(new)
        out.append(part)
    return out


def graph(data):
    n=data['vertices'];es={tuple(e) for e in data['edges']}
    assert n==20 and len(es)==len(data['edges'])==54
    def v(i,j):return 2+3*(i%6)+j
    described=set()
    for i in range(6):
        described|={edge(0,v(i,0)),edge(1,v(i,2))}
        for j in range(3):described.add(edge(v(i,j),v(i+1,j)))
        for j in range(2):
            described.add(edge(v(i,j),v(i,j+1)))
            described.add(edge(v(i,j),v(i+1,j+1)) if (i+j)%2==0 else edge(v(i+1,j),v(i,j+1)))
    assert es==described
    adj=[set() for _ in range(n)]
    for a,b in es:assert 0<=a<b<n;adj[a].add(b);adj[b].add(a)
    assert len(components(adj,[]))==1
    marks=data['marks'];assert marks==[5,9,13,11,15,19,17,3,7]
    core=set(range(n))-set(marks);assert len(core)==11
    assert all(len(adj[z])==4 and adj[z]<=core for z in marks)
    branches=[[0,2,6,10,1],[0,8,12,16,1],[0,14,18,4,1]]
    ce=sorted({edge(a,b) for p in branches for a,b in zip(p,p[1:])}|{(2,18)})
    assert len(ce)==13 and set(ce)<=es
    faces=data['faces'];assert len(faces)==36
    darts=set();rotation=[{} for _ in range(n)]
    for f in faces:
        assert len(f)==len(set(f))==3
        for i,a in enumerate(f):
            before,after=f[i-1],f[(i+1)%3]
            assert edge(a,after) in es and (a,after) not in darts
            assert before not in rotation[a]
            darts.add((a,after));rotation[a][before]=after
    assert darts=={(a,b) for a in range(n) for b in adj[a]}
    for a,row in enumerate(rotation):
        assert set(row)==set(row.values())==adj[a]
        root=min(row);x=root;seen=set()
        while x not in seen:seen.add(x);x=row[x]
        assert x==root and seen==adj[a]
    assert n-len(es)+len(faces)==2
    return adj,marks,core,ce


def routes(core,ce):
    adj={v:set() for v in core}
    for a,b in ce:adj[a].add(b);adj[b].add(a)
    # Direct recursive definition of every simple core path, no quotient.
    def extend(path,target):
        if path[-1]==target:
            yield tuple(path);return
        for x in sorted(adj[path[-1]]):
            if x not in path:yield from extend(path+[x],target)
    return {(a,b):list(extend([a],b)) for a in sorted(core) for b in sorted(core) if a<=b}


def build(data):
    adj,marks,core,ce=graph(data);catalog=routes(core,ce);encoding=Encoding()
    attachments=data['attachment_marks'];assert attachments==[3,15]
    parents={(z,v):encoding.new() for z in attachments for v in sorted(adj[z])}
    for z in attachments:
        row=[parents[z,v] for v in sorted(adj[z])];encoding.add(row)
        for a,b in combinations(row,2):encoding.add([-a,-b])
    def incidence(path):
        row=[0]*(len(ce)+1)
        for a,b in zip(path,path[1:]):row[ce.index(edge(a,b))]+=1
        return row
    def difference(q,p):return [a-b for a,b in zip(incidence(q),incidence(p))]
    for i in range(len(ce)):
        row=[0]*(len(ce)+1);row[i]=1;row[-1]=-1
        encoding.add([encoding.inequality(row)])
    # No hypothesis that a core edge is itself shortest is permitted.
    assert data['strict_taut'] is False
    seen=set()
    for template in data['pairs']:
        assert len(template)==2;requirements={};parts=[]
        for p in template:
            assert p and len(p)==len(set(p))
            assert all(type(v) is int and 0<=v<len(adj) for v in p)
            assert all(b in adj[a] for a,b in zip(p,p[1:]))
            assert not set(p[1:-1])&set(marks)
            q=p[:]
            for reverse in (False,True):
                if reverse:q.reverse()
                if q[0] in marks:
                    assert len(q)>=2;z=q.pop(0);v=q[0]
                    assert v in core and (z not in requirements or requirements[z]==v)
                    requirements[z]=v
                if reverse:q.reverse()
            assert q and set(q)<=core
            if q[0]>q[-1]:q.reverse()
            assert tuple(q) in catalog[q[0],q[-1]]
            parts.append(q)
        assert all(len(part&set(marks))<=4 for part in components(adj,set(template[0])|set(template[1])))
        key=(tuple(sorted(tuple(p) for p in parts)),tuple(sorted(requirements.items())))
        assert key not in seen;seen.add(key)
        assert set(requirements)<=set(attachments)
        clause=[-parents[z,v] for z,v in sorted(requirements.items())]
        for q in parts:
            for p in catalog[q[0],q[-1]]:
                clause.append(encoding.negate(encoding.inequality(difference(p,q))))
        encoding.add(clause)
    counts={'vertices':len(adj),'edges':sum(map(len,adj))//2,'core_edges':len(ce),
            'simple_core_paths':sum(map(len,catalog.values())),'templates':len(data['pairs']),
            'required_parent_assignments':4**len(attachments),'base_clauses':len(encoding.clauses)}
    return encoding,counts


def add_theory(encoding,certificate):
    # Explicit atom IDs bind the sparse arithmetic certificates to the CNF.
    for index,vector in certificate['extra_linear_atoms']:
        assert type(index) is int and index==encoding.next
        assert len(vector)==14 and all(type(x) is int for x in vector)
        assert normalized(vector)==tuple(vector) and tuple(vector) not in encoding.linear
        assert encoding.atom(vector)==index
    for row in certificate['farkas']:
        assert row;total=[Fraction(0) for _ in range(14)];strict=Fraction(0);clause=[]
        for literal,multiplier in row:
            assert type(literal) is int and abs(literal) in encoding.vector
            assert type(multiplier) is str
            weight=Fraction(multiplier);assert weight>0
            vector=encoding.vector[abs(literal)]
            # A positive literal means f>=0; a negative literal means -f>0.
            sign=1 if literal>0 else -1
            for j,value in enumerate(vector):total[j]+=weight*sign*value
            if literal<0:strict+=weight
            clause.append(-literal)
        assert all(x==0 for x in total[:-1])
        assert total[-1]<0 or (total[-1]==0 and strict>0)
        encoding.add(clause)


def rup(clauses,proof,variables):
    """Replay additions by reverse unit propagation; deletions are optional."""
    assert proof and proof[-1]==[],'proof must end with the empty clause'
    database=[tuple(c) for c in clauses]
    for row in proof:
        assert all(type(lit) is int and 1<=abs(lit)<=variables for lit in row)
        assert len(set(row))==len(row)
        assigned={};queue=deque(-x for x in row);conflict=False
        while True:
            while queue:
                literal=queue.popleft();v=abs(literal);value=literal>0
                if v in assigned:
                    if assigned[v]!=value:conflict=True;break
                else:assigned[v]=value
            if conflict:break
            changed=False
            for clause in database:
                open_lits=[];satisfied=False
                for literal in clause:
                    v=abs(literal)
                    if v not in assigned:open_lits.append(literal)
                    elif assigned[v]==(literal>0):satisfied=True;break
                if satisfied:continue
                if not open_lits:conflict=True;break
                if len(open_lits)==1:queue.append(open_lits[0]);changed=True
            if conflict:break
            if not changed:break
        assert conflict,'RUP addition failed'
        database.append(tuple(row))
    return len(proof)


def verify(data):
    enc,counts=build(data)
    add_theory(enc,data)
    counts.update({'variables':enc.next-1,'linear_atoms':len(enc.linear),'farkas_lemmas':len(data['farkas']),
                   'clauses_with_theory':len(enc.clauses),'rup_additions':rup(enc.clauses,data['rup'],enc.next-1)})
    return {'status':'PASS',**counts}


def distances(n,cost,require_connected=True):
    """Floyd--Warshall, independent of the simple-path inequality encoding."""
    d=[[None]*n for _ in range(n)];paths=[[None]*n for _ in range(n)]
    for a in range(n):d[a][a]=0;paths[a][a]=[a]
    for (a,b),length in cost.items():
        assert length>0;d[a][b]=d[b][a]=length
        paths[a][b]=[a,b];paths[b][a]=[b,a]
    for k in range(n):
        for a in range(n):
            if d[a][k] is None:continue
            for b in range(n):
                if d[k][b] is None:continue
                value=d[a][k]+d[k][b]
                if d[a][b] is None or value<d[a][b]:
                    d[a][b]=value;paths[a][b]=paths[a][k]+paths[k][b][1:]
    if require_connected:assert all(x is not None for row in d for x in row)
    return d,paths


def number(*items):
    return int.from_bytes(sha256(':'.join(map(str,items)).encode()).digest()[:8],'big')


def regressions(data):
    adj,marks,core,ce=graph(data);catalog=routes(core,ce)
    nongeodesic=0;tied=0;mass_checks=0;nonleaf_examples=0
    for seed in range(64):
        core_cost={e:1+number('core',seed,*e)%101 for e in ce}
        if seed==0:core_cost={e:1 for e in ce}
        elif 1<=seed<=13:core_cost={e:(100 if e==ce[seed-1] else 1) for e in ce}
        elif seed==14:core_cost={e:(1 if e==(2,18) else 100) for e in ce}
        parents={z:sorted(adj[z])[number('parent',seed,z)%4] for z in marks}
        cheap=core_cost.copy()
        required=set(data['attachment_marks']) if seed%2 else set(marks)
        cheap.update({edge(z,parents[z]):1+number('leaf',seed,z)%31 for z in required})
        partial,_=distances(len(adj),cheap,require_connected=False)
        ceiling=max(x for row in partial for x in row if x is not None)
        full={tuple(e):cheap.get(tuple(e),(partial[e[0]][e[1]]+seed%2)
                                if partial[e[0]][e[1]] is not None else ceiling) for e in data['edges']}
        d,paths=distances(len(adj),full)
        assert all(d[a][b]==partial[a][b] for a in core|required for b in core|required)
        if seed%2:
            # Equal positive distances to all four distinct core neighbors
            # rule out a metric-leaf representation for each other mark.
            for z in set(marks)-required:
                assert {d[z][a] for a in adj[z]}=={ceiling}
            nonleaf_examples+=1
        nongeodesic+=any(cost>d[a][b] for (a,b),cost in core_cost.items())
        tied+=any(sum(sum(core_cost[edge(a,b)] for a,b in zip(p,p[1:]))==d[s][t] for p in ps)>1
                  for (s,t),ps in catalog.items())
        certified=None
        for pair in data['pairs']:
            valid=True
            for p in pair:
                for z,parent in ((p[0],p[1]),(p[-1],p[-2])) if len(p)>1 else ():
                    if z in marks and parents[z]!=parent:valid=False
                if sum(full[edge(a,b)] for a,b in zip(p,p[1:]))!=d[p[0]][p[-1]]:valid=False
            if valid:certified=pair;break
        assert certified is not None
        assert all(len(c&set(marks))<=4 for c in components(adj,certified[0]+certified[1]))
        for mode in range(8):
            weights={z:(0 if mode==0 else 1 if mode==1 else 2**marks.index(z) if mode==2
                        else (1000 if z==marks[0] else 1) if mode==3 else number('mass',seed,mode,z)%101) for z in marks}
            total=sum(weights.values());top=sorted(marks,key=lambda z:(-weights[z],z))[:4]
            if 2*sum(weights[z] for z in top)>=total:
                pair=[paths[top[0]][top[1]],paths[top[2]][top[3]]]
            else:pair=certified
            for p in pair:
                assert len(p)==len(set(p))
                assert sum(full[edge(a,b)] for a,b in zip(p,p[1:]))==d[p[0]][p[-1]]
            assert all(2*sum(weights.get(z,0) for z in part)<=total for part in components(adj,pair[0]+pair[1]))
            mass_checks+=1
    return {'exact_metric_regressions':64,'metrics_with_nongeodesic_core_edge':nongeodesic,
            'metrics_with_tied_core_routes':tied,'mass_regressions':mass_checks,
            'metrics_with_seven_nonleaf_marks':nonleaf_examples}


def subset_transfer(adj,paths,marks,faces):
    """All support subsets, all intervals and rooted faces in this embedding.

    S intersect P has no effect, so enumerate exactly S subset U minus P.
    Each shortest path in this comparison metric is unique.
    """
    n=len(adj);total=len(marks);all_vertices=(1<<n)-1
    am=[sum(1<<x for x in row) for row in adj]
    pm=[[sum(1<<x for x in p) for p in row] for row in paths]
    marked=sum(1<<x for x in marks);cache={};checks=0;terminal_cases=0
    def admissible(P,S):
        key=P,S
        if key in cache:return cache[key]
        left=all_vertices&~(P|S)
        while left:
            bit=left&-left;left^=bit;part=bit;frontier=bit;boundary=0
            while frontier:
                bit=frontier&-frontier;frontier^=bit;neighbors=am[bit.bit_length()-1]
                boundary|=neighbors&S;new=neighbors&left;left^=new;part|=new;frontier|=new
            mass=(part&marked).bit_count()
            if 2*mass>total or (mass>0 and boundary.bit_count()>1):
                cache[key]=False;return False
        cache[key]=True;return True
    for root in range(n):
        for terminals in [[v] for v in range(n)]+faces:
            union=0
            for target in terminals:union|=pm[root][target]
            for target in terminals:
                terminal_cases+=1;P=pm[root][target];available=union&~P;S=available
                while True:
                    checks+=1
                    if admissible(P,S):return {'applicable':True}
                    if not S:break
                    S=(S-1)&available
    return {'applicable':False,'terminal_cases':terminal_cases,'subset_checks':checks,
            'distinct_first_path_support_checks':len(cache)}


def comparison(data,spec):
    adj,marks,core,ce=graph(data)
    cheap={(a,b):length for a,b,length in spec['core_prices']}
    assert set(cheap)==set(ce) and len(cheap)==len(spec['core_prices'])
    assert all(type(length) is int and length>0 for length in cheap.values())
    parents=dict(spec['parents']);assert set(parents)==set(marks) and len(spec['parents'])==len(marks)
    assert spec['leaf_price']==1 and spec['extra_edge_excess']==1
    for z,parent in parents.items():assert parent in adj[z];cheap[edge(z,parent)]=1
    d,_=distances(len(adj),cheap)
    full={tuple(e):cheap.get(tuple(e),d[e[0]][e[1]]+1) for e in data['edges']}
    ambient,paths=distances(len(adj),full);assert ambient==d
    for root in range(len(adj)):
        for target in range(len(adj)):
            if root!=target:
                assert sum(d[root][a]+full[edge(a,target)]==d[root][target] for a in adj[target])==1
    old,_=distances(len(adj),{e:c for e,c in cheap.items() if e!=(2,18)})
    saving=old[2][18]-cheap[2,18];assert saving>0
    result=subset_transfer(adj,paths,marks,data['faces']);assert not result['applicable']
    for pair in data['pairs']:
        valid=all(sum(cheap.get(edge(a,b),full[edge(a,b)]) for a,b in zip(p,p[1:]))==d[p[0]][p[-1]] for p in pair)
        if valid:
            masses=sorted(len(c&set(marks)) for c in components(adj,pair[0]+pair[1]))
            assert max(masses,default=0)<=4
            result.update({'positive_separator':pair,'component_mark_counts':masses,'chord_saving':saving});break
    else:raise AssertionError('no certified separator in comparison fixture')
    # Positive control: deleting the centre of a nine-leaf star suffices.
    star=[set(range(1,10))]+[{0} for _ in range(9)]
    _,star_paths=distances(10,{(0,z):1 for z in range(1,10)})
    assert subset_transfer(star,star_paths,list(range(1,10)),[])['applicable']
    return result


def rejections(data):
    def reject(call):
        try:call()
        except AssertionError:return
        raise AssertionError('invalid certificate or proof accepted')
    bad=[]
    q=copy.deepcopy(data);q['strict_taut']=True;bad.append(q)
    q=copy.deepcopy(data);q['faces'][0].reverse();bad.append(q)
    q=copy.deepcopy(data);q['pairs'][0][0].append(q['pairs'][0][0][0]);bad.append(q)
    q=copy.deepcopy(data);q['pairs'][0]=[[0],[1]];bad.append(q)
    q=copy.deepcopy(data);q['farkas'][0][0][1]='0';bad.append(q)
    q=copy.deepcopy(data);q['farkas'][0][0][1]=str(Fraction(q['farkas'][0][0][1])+1);bad.append(q)
    q=copy.deepcopy(data);q['extra_linear_atoms'][0][0]=-1;bad.append(q)
    q=copy.deepcopy(data);q['rup']=q['rup'][:-1];bad.append(q)
    q=copy.deepcopy(data);q['rup']=[[]];bad.append(q)
    for q in bad:reject(lambda q=q:verify(q))
    # An all-weak combination equaling zero is not a contradiction.
    enc=Encoding();x=enc.atom([1]+[0]*13);minus_x=enc.atom([-1]+[0]*13)
    reject(lambda:add_theory(enc,{'extra_linear_atoms':[],'farkas':[[[x,'1'],[minus_x,'1']]]}))
    # A strict inequality in a zero combination is a contradiction.
    add_theory(enc,{'extra_linear_atoms':[],'farkas':[[[x,'1'],[-x,'1']]]})
    assert rup([(1,2),(-1,),(1,-2)],[[]],2)==1
    reject(lambda:rup([(1,2)],[[1],[]],2))
    return len(bad)+2


def main():
    if sys.flags.optimize:raise RuntimeError('run with assertions enabled')
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    raw=(HERE/'certificate.json').read_bytes();data=json.loads(raw)
    result=verify(data);result['certificate_sha256']=sha256(raw).hexdigest()
    result.update(regressions(data));result['rejected_controls']=rejections(data)
    result['subset_transfer_comparison']=comparison(data,json.loads((HERE/'comparison.json').read_text()))
    if args.check:assert result==json.loads((HERE/'expected.json').read_text())
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':main()
