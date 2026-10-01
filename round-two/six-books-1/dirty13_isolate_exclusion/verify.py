"""Separate set-based literal-capacity replay; imports no producer."""
from pathlib import Path
from itertools import combinations
from copy import deepcopy
import hashlib,json
BASE=Path(__file__).resolve().parent
J=tuple(map(frozenset,({7,8,9},set(),{5,6},{6,8,9},{5,7,9},{2,4,8},{2,3,7},{0,4,6},{0,3,5},{0,3,4})))
POINTS=frozenset(range(10));PAIRS=list(combinations(range(10),2))
def require(ok,message):
    if not ok:raise ValueError(message)
def fixture():
    require(all(i not in J[i] and ((j in J[i])==(i in J[j])) for i in range(10) for j in range(10)),'bad literal graph')
    key=sum(1<<at for at,(i,j) in enumerate(PAIRS) if j in J[i])
    columns=[11-((9 if i==0 else 10)-1-len(J[i])) for i in range(10)]
    caps=[]
    for i,j in PAIRS:
        if j in J[i]:caps.append(3-(1+len(J[i]&J[j]))-(11-columns[i]-columns[j]))
        else:caps.append(6-len((POINTS-{i,j})-J[i]-J[j]))
    cycles=[]
    for T in combinations(range(10),4):
        S=frozenset(T)
        if all(len(J[i]&S)==2 for i in S):
            require(0 in S and sum(columns[i] for i in S)==21 and sum(caps[at] for at,(i,j) in enumerate(PAIRS) if i in S and j in S)==10,'four-column equality mismatch')
            cycles.append(S)
    require(len(cycles)==2 and columns[1]==2 and all(caps[PAIRS.index(tuple(sorted((1,j))))]<=1 for j in POINTS-{1}),'isolated-column split not justified')
    return key,columns,caps,cycles
KEY,COLUMNS,CAPS,CYCLES=fixture()
def patterns(delta,cycle_rows):
    result=[]
    for selected in combinations(range(10),4+delta):
        S=frozenset(selected)
        if any(c==0 and {i,j}<=S for c,(i,j) in zip(CAPS,PAIRS)):continue
        if cycle_rows and any(len(S&T) not in (1,2) for T in CYCLES):continue
        result.append(S)
    return result

def certify(vector,tags,counts,col,caps,domains):
    require(len(vector)==len(tags)+55 and all(type(x) is int for x in vector),'invalid certificate vector')
    q=len(tags);rowcoef={t:vector[j] for j,t in enumerate(tags)};unary={i:vector[q+i] for i in POINTS};paircoef={p:vector[q+10+j] for j,p in enumerate(PAIRS)}
    require(all(v>=0 for v in paircoef.values()),'negative capacity multiplier')
    upper=sum(rowcoef[t]*counts[t] for t in tags)+sum(unary[i]*col[i] for i in POINTS)+sum(paircoef[p]*c for p,c in zip(PAIRS,caps))
    if upper>=0:return False,upper
    for d in tags:
        for S in domains[d]:
            score=rowcoef[d]+sum(unary[i] for i in S)+sum(paircoef[p] for p in combinations(sorted(S),2))
            if score<0:return False,upper
    return True,upper

def word(S):return sum(1<<i for i in S)
def verify(data):
    require(data['graph_key']==KEY==710617334208,'wrong graph')
    require(len(data['direct'])==2 and [r['outside_deficits'] for r in data['direct']]==[[3],[2,1]],'incomplete degree cover')
    direct=[]
    for case in data['direct']:
        d=case['outside_deficits'];full=[0]*(11-len(d))+d;tags=sorted(set(full));counts={t:full.count(t) for t in tags};domains={t:patterns(t,False) for t in tags}
        require(case['tags']==tags,'altered degree tags')
        ok,score=certify(case['weights'],tags,counts,COLUMNS,CAPS,domains);require(ok,'invalid direct dual certificate')
        direct.append({'deficits':d,'domains':{str(t):len(domains[t]) for t in tags},'upper_score':score})
    split=data['split'];require(split['outside_deficits']==[1,1,1] and split['tags']==[0,1] and len(split['weights'])==4,'incomplete split cover')
    domain={t:patterns(t,True) for t in (0,1)};candidates=[(d,S) for d in (0,1) for S in domain[d] if 1 in S]
    # Product decomposition, followed by exchange quotient for the two actual points.
    fixed=set()
    for d,S in candidates:
        for e,T in candidates:
            if S&T=={1}:fixed.add(tuple(sorted(((d,word(S)),(e,word(T))))))
    coverage=[0]*4;usage=[0]*4;keys=[]
    for fixedpair in sorted(fixed):
        (d,a),(e,b)=fixedpair;S=frozenset(i for i in POINTS if a&(1<<i));T=frozenset(i for i in POINTS if b&(1<<i));counts={t:([0]*8+[1]*3).count(t)-(d==t)-(e==t) for t in (0,1)}
        col=[COLUMNS[i]-(i in S)-(i in T) for i in range(10)];caps=[c-({i,j}<=S)-({i,j}<=T) for c,(i,j) in zip(CAPS,PAIRS)]
        require(min(col)>=0 and min(caps)>=0 and min(counts.values())>=0,'invalid residual')
        zero_cols={i for i in POINTS if col[i]==0};zero_pairs=[{i,j} for c,(i,j) in zip(caps,PAIRS) if c==0]
        domains={t:[U for U in domain[t] if not(U&zero_cols) and not any(p<=U for p in zero_pairs)] for t in (0,1)}
        hits=[]
        for j,v in enumerate(split['weights']):
            ok,_=certify(v,[0,1],counts,col,caps,domains)
            if ok:hits.append(j);coverage[j]+=1
        require(hits,'uncovered actual pair')
        usage[hits[0]]+=1;keys.append([list(x) for x in fixedpair])
    result={'complete':True,'marked_graph_key':KEY,'miss_columns':COLUMNS,'pair_capacity_sum':sum(CAPS),'direct_cases':direct,'split_initial_domains':{str(t):len(domain[t]) for t in (0,1)},'split_branches':len(keys),'split_branch_sha256':hashlib.sha256(json.dumps(keys,separators=(',',':')).encode()).hexdigest(),'split_certificate_coverage':coverage,'split_first_certificate_usage':usage,'counting_vectors':6}
    return result

def controls(data):
    bad=[]
    b=deepcopy(data);b['graph_key']+=1;bad.append(b)
    b=deepcopy(data);b['direct'].pop();bad.append(b)
    b=deepcopy(data);b['direct'][0]['tags']=[0,1];bad.append(b)
    b=deepcopy(data);b['direct'][0]['weights'][12]=-1;bad.append(b)
    b=deepcopy(data);b['direct'][0]['weights']=[0]*57;bad.append(b)
    b=deepcopy(data);b['split']['weights'].pop();bad.append(b)
    b=deepcopy(data);b['split']['weights'][0]=[0]*57;bad.append(b)
    b=deepcopy(data);b['split']['outside_deficits']=[2,1];bad.append(b)
    for b in bad:
        try:verify(b)
        except ValueError:pass
        else:raise ValueError('damaged evidence was accepted')
    return len(bad)
if __name__=='__main__':
    data=json.loads((BASE/'certificate.json').read_text());result=verify(data);n=controls(data)
    if (BASE/'expected.json').exists():
        expected=json.loads((BASE/'expected.json').read_text());require(result==expected['result'] and n==expected['damages'],'expected independent records mismatch')
    print(json.dumps({'result':result,'damages':n},sort_keys=True))
