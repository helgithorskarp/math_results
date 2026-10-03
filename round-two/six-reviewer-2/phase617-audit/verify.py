"""Separate Euler-character/literal assignment verifier; imports no producer."""
from pathlib import Path
from itertools import product
import sys,json
P=617
R=(0,1,4)

def need(ok,why):
    if not ok:raise ValueError(why)

def data(N):
    need(all(P%r for r in range(2,25)),'prime')
    chi=[None]
    for r in range(1,P):
        z=pow(r,308,P);need(z in (1,616),'Euler dichotomy');chi.append(int(z==616))
    return tuple(None if n%P in R else (chi[n%P],chi[(n-1)%P],chi[(n-4)%P])for n in range(N))

def progression(N,a,d):
    need(type(a)is int and type(d)is int and a>=0 and d>0 and a+6*d<N,'actual AP bounds')
    return tuple(a+j*d for j in range(7))

def row_check(x):
    N=x['N'];D=data(N);sets=[{}for _ in range(6)];allcount=retained=0
    for a in range(N):
        for d in range(6,(N-1-a)//6+1,6):
            allcount+=1;ps=progression(N,a,d)
            if any(D[n]is None for n in ps):continue
            retained+=1;s=a%6;ks=frozenset(4*D[n][0]+2*D[n][1]+D[n][2]for n in ps);leaf=[a+6*d,a,d]
            if ks not in sets[s]or leaf<sets[s][ks]:sets[s][ks]=leaf
    expected=[]
    for s in range(6):
        row=[]
        for t in range(256):
            bad=[]
            for ks,leaf in sets[s].items():
                colors={int(bool(t&(1<<k)))for k in ks}
                if len(colors)==1:bad.append(leaf)
            row.append(min(bad)if bad else None)
        expected.append(row)
    need(expected==x['whole_witnesses'],'EVERY canonical table witness')
    need((allcount,retained)==(x['phase_ap_count'],x['root_free_count']),'entire AP count')
    pats=[sorted(sum(1<<k for k in ks)for ks in v)for v in sets]
    need(pats==x['pattern_sets'],'entire pattern-set entries')
    cutoffs=[max(w[0]+1 for w in row if w is not None)for row in expected]
    need(cutoffs==x['phase_cutoffs'],'every phase cutoff')
    permitted=sorted(t for t,w in enumerate(expected[0])if w is None)
    need(permitted==x['projection_bytes'],'exact projection byte convention')
    unique={(w[1],w[2])for row in expected for w in row if w is not None}
    need(len(unique)==x['unique_witness_count']and max(d for a,d in unique)==x['largest_witness_step'],'complete witness metadata')
    return dict(status='ALL_ROWS_LITERAL_CHECKED',phase_actual_APs=allcount,root_free=retained,table_entries=1536)

def sync_check(x):
    D=data(x['N']);leaves=x['eliminating_progressions'];survivors=[];full=0;rejections=[];cut_counts=[0]*len(leaves)
    actual_leaves=[]
    for leaf in leaves:
        ps=progression(x['N'],leaf['a'],leaf['d'])
        need(all(D[n]is not None for n in ps),'every actual rootfree leaf')
        actual_leaves.append(ps)
    for choice in product(range(6),repeat=6):
        full+=1;failed=None
        for index,ps in enumerate(actual_leaves):
            colors={D[n][choice[n%6]//2]^(choice[n%6]%2)for n in ps}
            if len(colors)==1:failed=index;break
        if failed is None:survivors.append(list(choice))
        else:rejections.append([list(choice),failed]);cut_counts[failed]+=1
    need(sorted(survivors)==sorted(x['survivors'])and full==6**6,'complete Cartesian phase-domain enumeration')
    need(survivors==[[i]*6 for i in range(6)],'exact synchronized domain')
    need(all((r['end']==r['a']+6*r['d'])for r in leaves),'every actual history endpoint')
    alive=full
    for leaf,cnt in zip(leaves,cut_counts):
        need(leaf['before']==alive and leaf['after']==alive-cnt,'every literal elimination history count');alive-=cnt
    return dict(status='ALL_PHASE_CHOICES_LITERAL_CHECKED',full_choices=full,rootfree_leaves=len(leaves),survivors=survivors)

_root_references={}

def root_reference(N):
    # Cache only the whole freshly reconstructed independent reference within
    # this process. There is no input cache or producer record trusted here.
    if N in _root_references:return _root_references[N]
    D=data(N);roots=tuple(n for n in range(N)if D[n]is None)
    index={n:i for i,n in enumerate(roots)};Cs=[{}for _ in range(6)];count=0
    for d in range(1,(N-1)//6+1):
        for a in range(N-6*d):
            count+=1;ps=progression(N,a,d);vs=tuple(index[n]for n in ps if D[n]is None)
            for choice in range(6):
                colors=set()
                for n in ps:
                    if D[n]is not None:colors.add(D[n][choice//2]^(choice%2))
                if len(colors)>1:continue
                for forbidden in (0,1):
                    if colors and forbidden not in colors:continue
                    leaf=[a+6*d,a,d];key=(vs,forbidden)
                    if key not in Cs[choice]or leaf<Cs[choice][key]:Cs[choice][key]=leaf
    _root_references[N]=(roots,Cs,count)
    return roots,Cs,count

def root_check(x):
    N=x['N'];roots,Cs,count=root_reference(N)
    need(list(roots)==x['root_positions'],'every independent actual root occurrence')
    need(x['phase_options']==[[j,b]for j in range(3)for b in range(2)],'all six phase options')
    need(count==x['all_actual_aps'],'every original AP')
    results=[]
    for choice,rec in enumerate(x['records']):
        C=Cs[choice];whole=[[list(vs),c,leaf]for (vs,c),leaf in sorted(C.items())]
        need(rec['choice']==choice and rec['coordinate']==choice//2 and rec['palette']==choice%2,'choice/coordinate correspondence')
        need(whole==rec['leaves']and len(C)==rec['all_distinct_root_clauses'],'ENTIRE root-clause/physical-leaf multiset')
        known={}
        for step in rec['implications']:
            vs=tuple(step['variables']);c=step['forbidden_color'];need(C.get((vs,c))==step['leaf'],'literal implication leaf')
            need(not any(v in known and known[v]!=c for v in vs),'unit premise not already satisfied')
            unknown=[v for v in vs if v not in known]
            need(unknown==[step['variable']]and step['value']==1-c,'complete unit implication');known[unknown[0]]=1-c
        need(sorted([v,c]for v,c in known.items())==rec['fixed'],'ENTIRE actual fixed root assignment')
        conflict=rec['conflict']
        if conflict is not None:
            vs=tuple(conflict['variables']);c=conflict['forbidden_color'];need(C.get((vs,c))==conflict['leaf'],'literal contradiction leaf');need(all(known.get(v)==c for v in vs),'actual checked contradiction')
            results.append(dict(choice=choice,count=0));continue
        remaining=sorted({(tuple(v for v in vs if v not in known),c)for vs,c in C if not any(v in known and known[v]!=c for v in vs)})
        need([[list(vs),c]for vs,c in remaining]==rec['residual_clauses'],'EVERY residual clause')
        free=[v for v in range(len(roots))if v not in known];good=0
        for word in product((0,1),repeat=len(free)):
            full={**known,**dict(zip(free,word))}
            if all(any(full[v]!=c for v in vs)for vs,c in C):good+=1
        results.append(dict(choice=choice,count=good,free_root_occurrences=[roots[v]for v in free]))
    need(sum(r['count']for r in results)=={3702:384,3703:252,3704:0}[N],'complete actual coloring counts')
    return dict(status='ALL_ROOT_CLAUSES_LITERAL_CHECKED',N=N,all_actual_APs=count,root_occurrences=len(roots),results=results,total=sum(r['count']for r in results))

if __name__=='__main__':
    kind=sys.argv[1];x=json.loads(Path(sys.argv[2]).read_text());out={'rows':row_check,'sync':sync_check,'roots':root_check}[kind](x);print(json.dumps(out,sort_keys=True,separators=(',',':')))
