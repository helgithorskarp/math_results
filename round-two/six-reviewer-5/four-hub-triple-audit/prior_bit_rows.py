"""Different bit ownership, weak compositions and exact matrix moments."""
from itertools import combinations


def need(ok,text):
    if not ok:raise ValueError(text)


def literal_rows(stars):
    output=[]
    for index,star in enumerate(stars):
        blocks=[sum(1<<p for p in w) for w in star]
        ownership={}
        for a,b in combinations(range(17),2):
            hits=[i for i,w in enumerate(blocks) if w&((1<<a)|(1<<b))==((1<<a)|(1<<b))]
            need(len(hits)<=1,'independent unique owner')
            ownership[a,b]=hits
        counts=[sum(w>>p&1 for w in blocks) for p in range(17)];deficits=[5-r for r in counts]
        high=[p for p in range(17) if deficits[p]];hh=[(a,b) for a,b in combinations(high,2) if not ownership[min(a,b),max(a,b)]]
        for bits in range(1<<len(high)):
            hubs=[p for i,p in enumerate(high) if bits>>i&1];S=[p for p in high if p not in hubs]
            e=5-len(high);k=len(hubs);q=len([edge for edge in hh if any(p in hubs for p in edge)])
            eligible=bool([p for p in hubs if all(p not in edge for edge in hh)])
            g1=sum(deficits[p]==1 for p in S);sigma=sum(deficits[p]-1 for p in S)
            psi=g1 if e==0 and eligible else -g1 if e!=0 and not eligible else 0
            I5=int(e==0 and len(hubs)==5)
            output.append({'star':index,'hubs':hubs,'high':high,'delta':deficits,'high_edges':hh,'e':e,'k':k,'q':q,'eligible':eligible,'h':len(high),'g1':g1,'sigma':sigma,'psi':psi,'I5':I5,'margin':psi-3*(k-e-q-I5),'old_margin':psi-3*(k-e-q)})
    return sorted(output,key=lambda r:(r['star'],r['k'],r['hubs']))


def compositions(total,parts):
    # Stars-and-bars bijection, no producer recursive category pruning.
    for separators in combinations(range(total+parts-1),parts-1):
        points=(-1,)+separators+(total+parts-1,)
        yield [points[i+1]-points[i]-1 for i in range(parts)]


def compute(stars,untrusted):
    own=literal_rows(stars)
    need(own==untrusted['rows'],'every426row field from physical bit owners')
    categories=('e','k','q','eligible','h','g1','sigma','psi','I5','margin');composition_checks=[]
    for branch in untrusted['boundaries']:
        Q=branch['Q'];budget=3*(7-(6+Q))
        cats=sorted({tuple(r[k] for k in categories) for r in own if r['sigma']==r['I5']==0 and r['q']<=Q and r['margin']<=budget})
        need(cats==branch['categories'],'complete independently projected categories')
        result=[];checks=0
        for vector in compositions(13,len(cats)):
            checks+=1
            if (sum(n*c[0] for n,c in zip(vector,cats)),sum(n*c[1] for n,c in zip(vector,cats)),sum(n*c[2] for n,c in zip(vector,cats)))!=(7-Q,6+Q,Q):continue
            if sum(n*c[-1] for n,c in zip(vector,cats))<=budget:result.append(vector)
        need(sorted(result)==sorted(branch['complete_population_vectors']),'all positive boundary coefficient patterns')
        composition_checks.append(checks)
    edges=list(combinations(range(6),2));cubic=trianglefree=squarefree=0
    trace_pairs=[]
    for chosen in combinations(edges,9):
        A=[[0]*6 for _ in range(6)]
        for a,b in chosen:A[a][b]=A[b][a]=1
        if any(sum(row)!=3 for row in A):continue
        cubic+=1;A2=[[sum(A[a][c]*A[c][b] for c in range(6)) for b in range(6)] for a in range(6)]
        trace3=sum(A2[a][b]*A[b][a] for a in range(6) for b in range(6))
        if trace3:continue
        trianglefree+=1;trace4=sum(A2[a][b]**2 for a in range(6) for b in range(6));trace_pairs.append(trace4)
        need((trace4-90)%8==0,'literal cubic moment identity square count')
        if trace4==90:squarefree+=1
    need((cubic,trianglefree,squarefree)==(70,10,0),'independent full matrix cubic-girth census')
    return {'every426row_field_matched':True,'weak_composition_cases':composition_checks,'matrix_moment_all5005graphs':True,'cubic_counts':[cubic,trianglefree,squarefree],'trianglefree_cubic_trace4':sorted(trace_pairs)}
