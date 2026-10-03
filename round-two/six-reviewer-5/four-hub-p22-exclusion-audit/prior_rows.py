"""Fresh physical-pair reconstruction; only credited literal23 stars input."""
from collections import Counter
from itertools import combinations


def need(ok,text):
    if not ok:raise ValueError(text)


def marks(stars):
    result=[]
    for index,star in enumerate(stars):
        words=[frozenset(w) for w in star]
        need(len(words)==len(set(words))==20 and all(len(w)==4 and all(type(p)==int and 0<=p<17 for p in w) for w in words),'twenty distinct actual quadruples')
        covered=[tuple(sorted(t)) for w in words for t in combinations(w,2)]
        need(len(covered)==len(set(covered))==120,'every actual pair singly owned')
        leave=sorted(set(combinations(range(17),2))-set(covered))
        degree=[sum(p in w for w in words) for p in range(17)];delta=[5-r for r in degree]
        need(all(0<=d<=5 for d in delta) and sum(delta)==5,'literal deficit sum5 including a missing link point')
        high=tuple(p for p in range(17) if delta[p]);h=len(high);e=5-h
        high_edges=[(a,b) for a,b in leave if a in high and b in high]
        high_degree={p:sum(p in edge for edge in high_edges) for p in high}
        need(len(leave)==16 and len(high_edges)==h-1,'complete high-induced leave')
        need(all(sum(p in edge for edge in leave)==1+3*delta[p] for p in range(17)),'actual leave degrees')
        need(all(a in high or b in high for a,b in leave),'imported no-low-low physical fixture property')
        for k in range(h+1):
            for hubs in combinations(high,k):
                saturated=tuple(p for p in high if p not in hubs)
                q=sum(a in hubs or b in hubs for a,b in high_edges)
                eligible=any(high_degree[p]==0 for p in hubs)
                g1=sum(delta[p]==1 for p in saturated);sigma=sum(delta[p]-1 for p in saturated)
                psi=g1 if e==0 and eligible else (-g1 if e>0 and not eligible else 0)
                I5=int(e==0 and k==5)
                row={'star':index,'hubs':list(hubs),'high':list(high),'delta':delta,'high_edges':high_edges,
                     'e':e,'k':k,'q':q,'eligible':eligible,'h':h,'g1':g1,'sigma':sigma,'psi':psi,'I5':I5,
                     'margin':psi-3*(k-e-q-I5),'old_margin':psi-3*(k-e-q)}
                need(row['margin']>=0,'corrected426 physical-row inequality')
                result.append(row)
    return result


FIELDS=('e','k','q','eligible','h','g1','sigma','psi','I5','margin')


def category(row):return tuple(row[key] for key in FIELDS)


def boundaries(rows):
    result=[]
    for Q in (0,1):
        E=7-Q;K=6+Q;budget=3*(E+Q-K)
        cats=sorted({category(r) for r in rows if r['sigma']==0 and r['I5']==0 and r['q']<=Q and r['margin']<=budget})
        coefficients=[dict(zip(FIELDS,c)) for c in cats];solutions=[];states=0
        def visit(index,left,e,k,q,margin,path):
            nonlocal states
            states+=1
            if e>E or k>K or q>Q or margin>budget:return
            if index==len(cats):
                if (left,e,k,q)==(0,E,K,Q):solutions.append(path)
                return
            r=coefficients[index]
            for n in range(left+1):visit(index+1,left-n,e+n*r['e'],k+n*r['k'],q+n*r['q'],margin+n*r['margin'],path+[n])
        visit(0,13,0,0,0,0,[])
        result.append({'Q':Q,'E':E,'K':K,'margin_budget':budget,'categories':cats,'complete_population_vectors':solutions,'recursive_states':states})
    need(len(result[0]['categories'])==3 and not result[0]['complete_population_vectors'],'Q0 impossible whole-domain count')
    need(len(result[1]['categories'])==4 and len(result[1]['complete_population_vectors'])==1,'unique Q1 category population')
    return result


def graph_checks():
    N=6;edges=list(combinations(range(N),2));cubic=trianglefree=squarefree=0
    accepted=[]
    for selected in combinations(edges,9):
        adjacency=[set() for _ in range(N)]
        for a,b in selected:adjacency[a].add(b);adjacency[b].add(a)
        if any(len(row)!=3 for row in adjacency):continue
        cubic+=1
        if any(adjacency[a]&adjacency[b] for a,b in selected):continue
        trianglefree+=1
        if any(len(adjacency[a]&adjacency[b])>1 for a,b in edges):continue
        squarefree+=1;accepted.append(selected)
    peterson=[set() for _ in range(10)]
    for i in range(5):
        for a,b in [(i,(i+1)%5),(i,i+5),(i+5,(i+2)%5+5)]:peterson[a].add(b);peterson[b].add(a)
    need(all(len(r)==3 for r in peterson),'literal Petersen cubic positive control')
    need(all(not(peterson[a]&peterson[b]) for a in range(10) for b in peterson[a]),'Petersen no triangle')
    need(all(len(peterson[a]&peterson[b])<=1 for a,b in combinations(range(10),2)),'Petersen no four-cycle')
    layer_counts=[]
    for v in range(10):
        first=peterson[v];second={q for p in first for q in peterson[p]}-{v}-first
        need(len(second)==6,'actual distinct six second neighbors')
        layer_counts.append([1,len(first),len(second)])
    need((cubic,trianglefree,squarefree)==(70,10,0),'complete six-point cubic obstruction')
    return {'all_nine_edge_sets':5005,'cubic':cubic,'trianglefree_cubic':trianglefree,'girth_at_least_five_cubic':squarefree,'petersen_all10layer_counts':layer_counts,'closed_graph_minimum10_is_classical_Moore_bound_not_a_packing_construction':True}


def compute(stars):
    rows=marks(stars);templates=boundaries(rows)
    exceptions=[r for r in rows if r['old_margin']<0]
    need(len(rows)==426 and len(exceptions)==8 and all((r['e'],r['k'],r['q'],r['g1'],r['psi'],r['I5'],r['old_margin'],r['margin'])==(0,5,4,0,0,1,-3,0) for r in exceptions),'all actual five-hub failures retained')
    return {'rows':rows,'boundaries':templates,'graphs':graph_checks(),'exceptions':exceptions,
            'old418_scope':sum(r['k']<=4 for r in rows),'distinct_categories':len({category(r) for r in rows})}
