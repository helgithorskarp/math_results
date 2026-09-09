"""Complete physical q8 carrier controls for the new packing predicate."""
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json
from physical import encode,decode,inspect,verify,need,PAIRS
def parse(g):
    n=ord(g[0])-63;a=[[0]*n for _ in range(n)];bit=0
    for v in range(1,n):
        for u in range(v):a[u][v]=a[v][u]=((ord(g[1+bit//6])-63)>>(5-bit%6))&1;bit+=1
    return a
def color(core):
    # Exact backtracking produces four triangle-free color classes.
    n=len(core);colors=[-1]*n
    def visit(v):
        if v==n:return True
        for c in range(4):
            if any(colors[u]==colors[w]==c and core[v][u] and core[v][w] and core[u][w] for u,w in combinations(range(v),2)):continue
            colors[v]=c
            if visit(v+1):return True
        colors[v]=-1;return False
    need(visit(0),'four triangle-free classes');return colors
def build(core,r):
    q=8;a=[[0]*43 for _ in range(43)];colors=color(core)
    for b in range(q):
        for u,v in combinations(range(4*b,4*b+4),2):a[u][v]=a[v][u]=int(b<r)
    for left,right in combinations(range(q),2):
        for u in range(4):
            for v in range(4):a[4*left+u][4*right+v]=a[4*right+v][4*left+u]=int(u//2 != v//2) if left==0 else int(u//2==v//2)
    for u,v in combinations(range(11),2):a[32+u][32+v]=a[32+v][32+u]=core[u][v]
    for b in range(q):
        for u in range(4):
            for v in range(11):a[4*b+u][32+v]=a[32+v][4*b+u]=int(u==(0 if b<r else colors[v]))
    return a
def parent(a,r):
    pairs=fives=0
    for left,right in combinations(range(8),2):
        for five in combinations([*range(4*left,4*left+4),*range(4*right,4*right+4)],5):
            colors={a[u][v] for u,v in combinations(five,2)};need(len(colors)==2,'pair palette');fives+=1
        pairs+=1
    keys=[]
    for b in range(1,8):
        signatures=[sum(a[u][4*b+v]<<u for u in range(4)) for v in range(4)]
        need(signatures==sorted(signatures,reverse=True),'root column order');keys.append(sum(a[u][4*b+v]<<(4*u+v) for u in range(4) for v in range(4)))
    need(len(set(keys))==1,'root multiset ties')
    # Every cross-column in an ordinary non-root pair has exactly two red and
    # two blue neighbours, excluding every h4069 centred 3+1+1 event.
    for left in range(1,8):
        for right in range(1,8):
            if left!=right:
                for v in range(4):need(sum(a[4*left+u][4*right+v] for u in range(4))==2,'h4069 ordinary column')
    for b in range(8):
        for v in range(32,43):
            column=sum(a[4*b+u][v]<<u for u in range(4));need(column!=15 if b<r else column!=0,'parent core star')
            if b<r:need(column==1,'augmentation excluded: at most one common red block neighbour')
    return pairs,fives
def run(data,out):
    data,out=Path(data),Path(out);out.mkdir();graphs=(data/'r44_11.g6').read_text().splitlines();indices=[0,len(graphs)//2,len(graphs)-1]
    fixtures=[];mutations=0;pairs=fives=0;core_fours=0;h=hashlib.sha256();stream=(out/'MUTATIONS.jsonl').open('wb')
    for index in indices:
        core=parse(graphs[index]);ts=[t for t in combinations(range(11),3) if all(core[u][v] for u,v in combinations(t,2))];need(ts,'physical negative control triangle')
        for four in combinations(range(11),4):need(len({core[u][v] for u,v in combinations(four,2)})==2,'R44 core');core_fours+=1
        for r in range(5,9):
            a=build(core,r);task=f'bo1-q8-r{r}-c{index:06d}';p,f=parent(a,r);pairs+=p;fives+=f
            obj=dict(task=task,graph=encode(a));need(inspect(obj)['witness'] is None,'positive filter');need(decode(obj['graph'])==a,'physical codec')
            fixtures.append(dict(**obj,passes_filter=True))
            bad=[4,8,12,16,20];need(all(a[u][v] for u,v in combinations(bad,2)),'control is not a target')
            for b in range(r,8):
                for row in range(4):
                    for t in ts:
                        c=[line[:] for line in a]
                        for v in t:
                            for u in range(4):c[4*b+u][32+v]=c[32+v][4*b+u]=int(u==row)
                        need(all(c[u][v]==a[u][v] for u,v in PAIRS if not(4*b<=u<4*b+4 and v in [32+x for x in t])),'only declared contact columns changed')
                        need(all(sum(c[4*b+u][v] for u in range(4))==1 for v in range(32,43)),'blue stars remain nonzero')
                        obj=dict(task=task,graph=encode(c));result=inspect(obj);need(result['status']=='RED_MAXIMALITY_WITNESS','negative filter');verify(c,8,r,result['witness'])
                        literal=dict(vertices=[4*b+row,*[32+x for x in t]],colour=1,block=b);verify(c,8,r,literal)
                        need(all(c[u][v] for u,v in combinations(bad,2)),'mutation is not target')
                        record=dict(**obj,witness=result['witness']);blob=(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n').encode();stream.write(blob);h.update(blob);mutations+=1
                        if b==r and row==0 and t==ts[0]:fixtures.append(dict(**obj,passes_filter=False,witness=result['witness']))
    stream.close();(out/'FIXTURES.json').write_text(json.dumps(fixtures,sort_keys=True,indent=2)+'\n')
    base=next(x for x in fixtures if not x['passes_filter']);a=decode(base['graph']);r=int(base['task'].split('-')[2][1:]);w=base['witness'];corruptions=0
    for change in (dict(colour=0),dict(vertices=w['vertices'][:3]),dict(vertices=[0,*w['vertices'][1:]]),dict(block=w['block']+1)):
        try:verify(a,8,r,dict(w,**change))
        except (ValueError,KeyError):corruptions+=1
        else:raise ValueError('corrupt witness accepted')
    return dict(status='PHYSICAL_MAXIMAL_RESIDUAL_CONTROLS_PASS',full_positive_controls=12,indexed_mutations=mutations,
                pair_palette_checks=pairs,literal_pair_fives=fives,literal_core_fours=core_fours,corruptions_rejected=corruptions,
                mutation_stream_sha256=h.hexdigest(),fixtures_sha256=hashlib.sha256((out/'FIXTURES.json').read_bytes()).hexdigest(),
                q10_child_inputs_inspected=0,target_found=False)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('out');a=p.parse_args();r=run(a.data,a.out)
    (Path(a.out)/'PHYSICAL.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
