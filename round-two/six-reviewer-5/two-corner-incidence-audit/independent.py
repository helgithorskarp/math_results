"""Own integer-evaluation/Sturm and dart-permutation/cap audit; no author input."""
from fractions import Fraction as Q
from itertools import product
from collections import Counter
import json,pathlib,hashlib
import kernel as K
need=K.need

def closure_value(word,r):
    state=K.E
    for m in word:state=K.fan_at(r,m,state)
    v=state[1]
    return state,(2-r)*v[0]+r*(v[1]+v[2])-r

def closure(word):
    D=sum(m-1 for m in word)
    samples=[closure_value(word,r) for r in range(D+2)]
    vectors=tuple(K.interpolate([s[0][1][k] for s in samples[:D+1]]) for k in range(3))
    g=K.interpolate([s[1] for s in samples])
    need(len(g)-1<=D+1,'proved degree bound')
    for r in (Q(-3,2),Q(2,3),Q(3,4),Q(10,13),Q(17)):
        state,gv=closure_value(word,r)
        need(tuple(K.value(p,r) for p in vectors)==state[1] and K.value(g,r)==gv,'vector/Gram interpolation bridge')
    results=[]
    for lo,hi in ((Q(2,3),Q(3,4)),(Q(18,29),Q(19,25)),(Q(19,25),Q(16,21))):
        n,seq=K.sturm(g,lo,hi)
        results.append(dict(interval=(lo,hi),distinct_roots=n,endpoint_values=(K.value(g,lo),K.value(g,hi)),sequence=seq))
    need(results[0]['distinct_roots']==results[1]['distinct_roots']==0,'original and extended closed bands')
    need(results[2]['distinct_roots']==(1 if word==(3,4,3) else 0),'boundary-method countercontrol')
    return dict(word=word,degree_bound=D+1,final_vector=vectors,g=g,sturm=results)

def annulus(qs,ks):
    darts={(i,j) for i,q in enumerate(qs) for j in range(q)}
    alpha={}
    for i,k in enumerate(ks):
        a=(i,k);b=((i+1)%3,0)
        need(a not in alpha and b not in alpha,'two disjoint ports')
        alpha[a]=b;alpha[b]=a
    need(len(alpha)==6,'three distinct seams')
    external=darts-set(alpha)
    nxt=lambda e:(e[0],(e[1]+1)%qs[e[0]])
    def successor(e):
        e=nxt(e);seen=set()
        while e in alpha:
            need(e not in seen,'all-internal dart cycle');seen.add(e)
            e=nxt(alpha[e])
        return e
    succ={e:successor(e) for e in external}
    need(set(succ.values())==external,'external permutation')
    # Vertex pairs are recovered directly from reversed dart identifications.
    pairs=[]
    for i,k in enumerate(ks):
        pairs.extend([((i,k),((i+1)%3,1)),((i,k+1),((i+1)%3,0))])
    flat=[v for pair in pairs for v in pair]
    need(len(flat)==len(set(flat))==12,'no triple seam endpoints')
    pairmap={v:tuple(sorted(pair)) for pair in pairs for v in pair}
    vc=lambda v:pairmap.get(v,(v,))
    cycles=[];unused=set(external)
    while unused:
        start=min(unused);e=start;cycle=[]
        while e in unused:
            unused.remove(e);cycle.append(e);e=succ[e]
        need(e==start,'disjoint boundary orbit')
        vertices=[vc(e) for e in cycle]
        need(len(vertices)==len(set(vertices)),'simple boundary cycle')
        mixed=[j for j,v in enumerate(vertices) if len(v)==2]
        need(len(mixed)==3,'three mixed vertices per boundary')
        need(all(vc(nxt(e))==vc(succ[e]) for e in cycle),'dart-to-vertex boundary transport')
        cycles.append(dict(darts=cycle,vertices=vertices,mixed=mixed,length=len(cycle)))
    need(len(cycles)==2,'annulus boundary components')
    vertices={vc(e) for e in darts}; edges=sum(qs)-3
    need(len(vertices)==sum(qs)-6 and len(vertices)-edges+3==0,'full Euler and coverage')
    need({v for cy in cycles for v in cy['vertices']}==vertices,'all vertices on boundary')
    return dict(q=qs,k=ks,vertex_classes=sorted(vertices),seams=sorted((a,b) for a,b in alpha.items() if a<b),successor=sorted((a,b) for a,b in succ.items()),cycles=cycles,chi=0)

def triangulations(v):
    """Every polygon triangulation once via its unique triangle at the root edge."""
    if len(v)<3:return [()]
    out=[]
    for i in range(1,len(v)-1):
        triangle=(v[0],v[i],v[-1])
        for left in triangulations(v[:i+1]):
            for right in triangulations(v[i:]):out.append(tuple(sorted(left+right+(triangle,))))
    need(len(out)==len(set(out)),'unique recursive triangulations')
    return out

def cap(cycle):
    n=cycle['length'];mixed=set(cycle['mixed']);valid=[]
    for tris in triangulations(tuple(range(n))):
        incidence=[sum(v in t for t in tris) for v in range(n)]
        need(sum(incidence)==3*n-6,'triangular cap incidence')
        if all(incidence[v]>=(1 if v in mixed else 3) for v in range(n)):
            need(all(incidence[v]==(1 if v in mixed else 3) for v in range(n)),'equality saturation')
            valid.append(dict(triangles=tris,incidence=incidence))
    return dict(length=n,mixed=sorted(mixed),triangulations=len(triangulations(tuple(range(n)))),valid=valid)

def canonical(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,(tuple,list)):return [canonical(v) for v in x]
    if isinstance(x,dict):return {k:canonical(v) for k,v in x.items()}
    return x

def build():
    cases=[closure(w) for q in (4,5) for w in product((3,4),repeat=q-2)]
    need(len(cases)==12 and len({c['word'] for c in cases})==12,'whole word domain')
    ports=[annulus(qs,ks) for qs in product((4,5),repeat=3) for ks in product(*(range(2,q-1) for q in qs))]
    need(len(ports)==27 and len({(a['q'],a['k']) for a in ports})==27,'whole oriented port domain')
    histogram=Counter((sum(q==5 for q in a['q']),tuple(sorted(c['length'] for c in a['cycles']))) for a in ports)
    need(histogram==Counter({(0,(3,3)):1,(1,(3,4)):6,(2,(3,5)):6,(2,(4,4)):6,(3,(3,6)):2,(3,(4,5)):6}),'catalog normalization')
    caps=[dict(q=a['q'],k=a['k'],caps=[cap(cy) for cy in a['cycles']]) for a in ports]
    for a in caps:
        for c in a['caps']:
            need(bool(c['valid'])==(c['length'] in (3,6)),'complete possible cap lengths')
            if c['length']==6:
                need(c['mixed'] in ([0,2,4],[1,3,5]) and len(c['valid'])==1,'six alternating ears')
    residuals=[]
    for a,ac in zip(ports,caps):
        for b,bc in zip(ports,caps):
            if sum(q==5 for q in a['q']+b['q'])!=3:continue
            for i,j in product(range(2),repeat=2):
                if not ac['caps'][i]['valid'] or not bc['caps'][j]['valid']:continue
                la,lb=a['cycles'][i]['length'],b['cycles'][j]['length']
                mid=tuple(sorted((a['cycles'][1-i]['length'],b['cycles'][1-j]['length'])))
                ntri=11-(la-2)-(lb-2)
                need(ntri==sum(mid) and (mid,ntri) in (((3,6),9),((4,5),9),((3,3),6)),'all middle annulus counts')
                residuals.append(dict(first=(a['q'],a['k']),second=(b['q'],b['k']),cap_indices=(i,j),cap_lengths=(la,lb),middle_lengths=mid,middle_triangles=ntri))
    return canonical(dict(method='integer evaluation/Newton interpolation/rational Sturm; face-dart boundary permutation; recursive rooted-edge Catalan caps',closures=cases,ports=ports,caps=caps,histogram=[dict(pentagons=p,lengths=l,count=n) for (p,l),n in sorted(histogram.items())],residuals=residuals))

if __name__=='__main__':
    data=build();raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
    pathlib.Path(__file__).with_name('EVIDENCE.json').write_bytes(raw)
    print(json.dumps(dict(words=12,ports=27,extended_roots=[c['sturm'][1]['distinct_roots'] for c in data['closures']],upper_countercontrol='343: one necessary root between19/25 and16/21',caps=54,residual_labelled_records=len(data['residuals']),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)),sort_keys=True))
