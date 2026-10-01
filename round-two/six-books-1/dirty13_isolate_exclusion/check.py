"""Exact bit-pattern certificate replay. Python standard library only."""
from pathlib import Path
from itertools import combinations
import json,hashlib
BASE=Path(__file__).resolve().parent
KEY=710617334208
PAIRS=list(combinations(range(10),2))
def require(ok,message):
    if not ok:raise ValueError(message)
def model():
    g=[0]*10
    for bit,(i,j) in enumerate(PAIRS):
        if KEY>>bit&1:g[i]|=1<<j;g[j]|=1<<i
    h=[x.bit_count() for x in g];w=[h[i]+2+(i==0) for i in range(10)]
    cap=[h[i]+h[j]-2-(g[i]&g[j]).bit_count()-(3-(i==0)-(j==0) if g[i]>>j&1 else 0) for i,j in PAIRS]
    return g,w,cap
G,W,CAP=model()
CYCLES=[sum(1<<i for i in q) for q in ((0,4,7,9),(0,3,8,9))]
def words(tag,cycles=False):
    return [z for z in range(1024) if z.bit_count()==4+tag and not any(c==0 and z>>i&1 and z>>j&1 for c,(i,j) in zip(CAP,PAIRS)) and (not cycles or all(1<=(z&q).bit_count()<=2 for q in CYCLES))]
def target(tags,counts,columns,caps):return [counts[t] for t in tags]+columns+caps

def accepts(v,tags,counts,columns,caps,domains):
    require(len(v)==len(tags)+55 and all(type(x) is int for x in v),'invalid integer vector')
    require(min(v[len(tags)+10:])>=0,'negative pair multiplier')
    if sum(a*b for a,b in zip(v,target(tags,counts,columns,caps)))>=0:return False
    for d in tags:
        for z in domains[d]:
            score=v[tags.index(d)]+sum(v[len(tags)+i] for i in range(10) if z>>i&1)+sum(v[len(tags)+10+b] for b,(i,j) in enumerate(PAIRS) if z>>i&1 and z>>j&1)
            if score<0:return False
    return True

def run(data):
    require(data['graph_key']==KEY,'wrong marked graph')
    require(len(data['direct'])==2 and [r['outside_deficits'] for r in data['direct']]==[[3],[2,1]],'direct case cover missing')
    direct=[]
    for rec in data['direct']:
        ds=rec['outside_deficits'];tags=sorted(set(ds+[0]));counts={t:ds.count(t) if t else 11-len(ds) for t in tags};domains={t:words(t) for t in tags}
        require(rec['tags']==tags,'wrong degree tags')
        require(accepts(rec['weights'],tags,counts,W,CAP,domains),'direct counting contradiction failed')
        direct.append({'deficits':ds,'domains':{str(t):len(domains[t]) for t in tags},'upper_score':sum(a*b for a,b in zip(rec['weights'],target(tags,counts,W,CAP)))})
    split=data['split'];require(split['outside_deficits']==[1,1,1] and split['tags']==[0,1] and len(split['weights'])==4,'split case cover missing')
    domain={t:words(t,True) for t in (0,1)};parts=[(t,z) for t in (0,1) for z in domain[t] if z>>1&1];keys=[];usage=[0]*4;coverage=[0]*4
    for at,(d,z) in enumerate(parts):
        for e,y in parts[at:]:
            if z&y!=2:continue
            counts={0:8-(d==0)-(e==0),1:3-(d==1)-(e==1)}
            columns=[W[i]-(z>>i&1)-(y>>i&1) for i in range(10)]
            caps=[c-int(z>>i&1 and z>>j&1)-int(y>>i&1 and y>>j&1) for c,(i,j) in zip(CAP,PAIRS)]
            require(min(columns)>=0 and min(caps)>=0 and min(counts.values())>=0,'invalid branch residual')
            domains={t:[r for r in domain[t] if not r>>1&1 and not any(columns[i]==0 and r>>i&1 for i in range(10)) and not any(c==0 and r>>i&1 and r>>j&1 for c,(i,j) in zip(caps,PAIRS))] for t in (0,1)}
            hits=[j for j,v in enumerate(split['weights']) if accepts(v,[0,1],counts,columns,caps,domains)]
            require(hits,'branch has no exact counting contradiction')
            usage[hits[0]]+=1
            for j in hits:coverage[j]+=1
            keys.append([[d,z],[e,y]])
    keybytes=json.dumps(sorted(keys),separators=(',',':')).encode()
    return {'complete':True,'marked_graph_key':KEY,'miss_columns':W,'pair_capacity_sum':sum(CAP),'direct_cases':direct,'split_initial_domains':{str(t):len(domain[t]) for t in (0,1)},'split_branches':len(keys),'split_branch_sha256':hashlib.sha256(keybytes).hexdigest(),'split_certificate_coverage':coverage,'split_first_certificate_usage':usage,'counting_vectors':6}
if __name__=='__main__':
    result=run(json.loads((BASE/'certificate.json').read_text()))
    if (BASE/'expected.json').exists():require(result==json.loads((BASE/'expected.json').read_text())['result'],'expected result mismatch')
    print(json.dumps(result,sort_keys=True))
