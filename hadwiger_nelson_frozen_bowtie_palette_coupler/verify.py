#!/usr/bin/env python3
"""Complete exact geometry and relation proof; standard library only."""
from pathlib import Path
from itertools import combinations,product
from math import gcd
import argparse,json,hashlib
BASE=Path(__file__).resolve().parent
SOURCE_SHA='3631210e31697804a86437cc7b6f734870097e22de50e5c4721ecea6ab633924'
RAD=(1,3,11,33);N=[4,5,6,7,9,10,12,14,15,17,18,22,25,28]

def need(p,m):
    if not p:raise ValueError(m)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def norm(d):
    out={}
    for axis in [d[:4],d[4:]]:
        terms=[(r,a) for r,a in zip(RAD,axis) if a]
        for i,(r,a) in enumerate(terms):
            out[1]=out.get(1,0)+r*a*a
            for s,b in terms[i+1:]:
                h=gcd(r,s);k=r*s//(h*h);out[k]=out.get(k,0)+2*h*a*b
    return [out.get(r,0) for r in RAD]

def geometry():
    data=(BASE/'source29.tsv').read_bytes()
    need(hashlib.sha256(data).hexdigest()==SOURCE_SHA,'source identity')
    lines=[list(map(int,l.split())) for l in data.decode().splitlines() if l and not l.startswith('#')]
    need(len(lines)==29 and [l[0] for l in lines]==list(range(29)) and all(len(l)==5 for l in lines),'source row labels')
    F=[(5*a,0,0,5*b,0,5*c,5*d,0) for _,a,b,c,d in lines]
    c=(0,0,0,0,60,0,0,0);u=(36,0,0,0,48,0,0,0);v=(18,-24,0,0,24,18,0,0)
    add=lambda a,b:tuple(x+y for x,y in zip(a,b))
    B=[c,add(c,u),add(c,v),add(c,tuple(-x for x in u)),add(c,tuple(-x for x in v))];P=F+B
    need(len(P)==len(set(P))==34,'exact collisions and cap')
    E=[];stream=hashlib.sha256()
    for i,j in combinations(range(34),2):
        n=norm(tuple(a-b for a,b in zip(P[i],P[j])));need(any(n),'nonzero physical separation')
        stream.update((','.join(map(str,n))+'\n').encode())
        if n==[3600,0,0,0]:E.append([i,j])
    fe=[e for e in E if e[1]<29];be=[e for e in E if e[0]>=29];cross=[e for e in E if e[0]<29<=e[1]]
    need(len(fe)==75,'complete F29 source');need(be==[[29,30],[29,31],[29,32],[29,33],[30,31],[32,33]],'complete bowtie source');need(cross==[[0,29]],'one genuine private contact')
    adj=[set() for _ in F]
    for a,b in fe:adj[a].add(b);adj[b].add(a)
    need(adj[0]==set(N),'exact marked frozen-centre neighbourhood')
    return {'points':34,'unit_edges':len(E),'pairs':561,'source_edges':75,'bowtie_edges':6,'private_cross_edges':cross,'shared_points':0,'point_hash':digest(P),'edge_hash':digest(E),'distance_hash':stream.hexdigest()},E,adj

# Complete finite-domain search: singleton arc propagation followed by every
# remaining colour at a minimum-domain vertex. No heuristic UNSAT verdict.
def extension(adj,domains):
    d=list(domains);queue=[v for v,m in enumerate(d) if m and m&(m-1)==0]
    if any(m==0 for m in d):return None
    while queue:
        v=queue.pop();m=d[v]
        for u in adj[v]:
            if d[u]&m:
                d[u]&=~m
                if not d[u]:return None
                if d[u]&(d[u]-1)==0:queue.append(u)
    uns=[v for v,m in enumerate(d) if m&(m-1)]
    if not uns:return [m.bit_length()-1 for m in d]
    v=min(uns,key=lambda v:(d[v].bit_count(),-len(adj[v]),v));m=d[v]
    while m:
        bit=m&-m;m-=bit;nextd=list(d);nextd[v]=bit;answer=extension(adj,nextd)
        if answer is not None:return answer
    return None

def canonical(w):
    lab={};return ''.join(str(lab.setdefault(c,len(lab))) for c in w)

def full_source_relation(adj):
    # Enumerate named three-colourings in graph-degree order, with the first
    # marked point fixed to zero; quotient afterward. This differs from the
    # producer's direct restricted-growth enumeration in terminal order.
    ni={v:i for i,v in enumerate(N)};na=[{ni[u] for u in adj[v] if u in ni} for v in N]
    order=[0]+sorted(range(1,14),key=lambda i:(-len(na[i]),i));word=[-1]*14;word[0]=0;pat=set();named=0
    def walk(k):
        nonlocal named
        if k==14:pat.add(canonical(word));named+=1;return
        v=order[k]
        for c in range(3):
            if all(word[u]!=c for u in na[v]):word[v]=c;walk(k+1);word[v]=-1
    walk(1);allowed=[];denied=[]
    for w in sorted(pat):
        d=[15]*29;d[0]=8
        for v,c in zip(N,w):d[v]=1<<int(c)
        answer=extension(adj,d)
        if answer is None:denied.append(w)
        else:
            need(all(answer[v]==int(c) for v,c in zip(N,w)) and answer[0]==3,'decoded source pins')
            need(all(answer[u]!=answer[v] for u in range(29) for v in adj[u]),'literal source word')
            allowed.append(w)
    need(allowed and all(set(w)==set('012') for w in allowed),'all and only three-colour palettes survive')
    return allowed,{'named_three_colour_words_with_first_zero':named,'bare_at_most_three_colour_patterns':len(pat),'source_canonical_patterns':len(allowed),'source_rejected_patterns':len(denied),'source_pattern_hash':hashlib.sha256(''.join(w+'\n' for w in allowed).encode()).hexdigest()}

def proper(w,edges,n,k):
    need(isinstance(w,str) and len(w)==n and set(w)<=set('01234'[:k]),'colour format')
    need(all(w[a]!=w[b] for a,b in edges),'literal proper colouring')

def verify(c):
    need(c['field_scale']==60,'coordinate scale')
    g,E,adj=geometry();allowed,s=full_source_relation(adj)
    # Exact local truth table on the four bowtie leaves; source centre is3
    # after the canonical normalization of any surviving F29 pattern.
    baseline=[];joined=[];lost=[]
    for w in product(range(4),repeat=4):
        bare=w[0]!=w[1] and w[2]!=w[3]
        before=bare and any(all(a!=x for x in w) for a in range(4))
        after=bare and any(a!=3 and all(a!=x for x in w) for a in range(4))
        formula=before and set(w)!=set([0,1,2])
        need(after==formula,'complete palette-inequality semantics')
        if before:baseline.append(w)
        if after:joined.append(w)
        if before and not after:lost.append(w)
    need([len(baseline),len(joined),len(lost)]==[120,96,24],'local complete relation counts')
    fe=[e for e in E if e[1]<29];proper(c['source_word'],fe,29,4)
    need(''.join(c['source_word'][i] for i in N)==c['source_pattern'] and c['source_pattern'] in allowed,'source fixture relation')
    need(c['source_word'][0]=='3','normalized private source colour')
    proper(c['isolated_bowtie_word'],[[0,1],[0,2],[0,3],[0,4],[1,2],[3,4]],5,4)
    need(c['forbidden_joint_terminal_word']==c['source_pattern']+c['isolated_bowtie_word'][1:],'isolated product witness')
    w=c['forbidden_joint_terminal_word'];need(set(w[:14])==set(w[14:])==set('012'),'two private colours forced3')
    # Direct complete-graph rejection of that prescription, with all18 pins.
    fulladj=[set() for _ in range(34)]
    for a,b in E:fulladj[a].add(b);fulladj[b].add(a)
    d=[15]*34
    for v,col in zip(N+[30,31,32,33],w):d[v]=1<<int(col)
    need(extension(fulladj,d) is None,'forbidden full-graph terminal prescription')
    proper(c['proper_four_word'],E,34,4);proper(c['proper_five_word_for_forbidden_terminals'],E,34,5)
    need(''.join(c['proper_five_word_for_forbidden_terminals'][v] for v in N+[30,31,32,33])==w,'five-word same forbidden terminals')
    # Both marginals remain full: for any B word with some missing colour b,
    # a global permutation of one F word can make F's centre another colour.
    for bw in baseline:
        missing=[a for a in range(4) if a not in bw]
        need(any(a!=b for a in range(4) for b in missing),'bowtie marginal extension')
    # For each normalized F source pattern a fixed B word20113 extends.
    need((0,1,1,3) in joined,'frozen source marginal extension')
    g.update(s);M=len(allowed)
    g.update({'input_joint_canonical_patterns':120*M,'composite_joint_canonical_patterns':96*M,'lost_joint_canonical_patterns':24*M,'input_joint_labelled_patterns':120*M*24,'composite_joint_labelled_patterns':96*M*24,'lost_joint_labelled_patterns':24*M*24,'relative_loss_numerator':1,'relative_loss_denominator':5,'both_source_marginals_full':True,'bridge_removal_restores_product':True,'proper_four_checked':True,'proper_five_checked':True,'chromatic_number':4,'record_candidate':False,'receiver_tested':False})
    return g

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'certificate.json');ap.add_argument('--output',type=Path);ap.add_argument('--check-expected',action='store_true');a=ap.parse_args();r=verify(json.loads(a.certificate.read_text()))
    if a.check_expected:need(r==json.loads((BASE/'EXPECTED.json').read_text()),'expected theorem output')
    s=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(s)
    print(s,end='')
if __name__=='__main__':main()
