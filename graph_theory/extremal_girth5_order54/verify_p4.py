"""Exact complete-cover checks and all-P4 positive graph control."""
from itertools import combinations,combinations_with_replacement,product
from collections import Counter
from p4_cases import cases,roles,endpoint_roles,CASES
from forest_profiles import profiles

def direct_rows(a,b):
    # Choose five concrete six-vertices; derive histograms only afterward.
    values=[c for c,n in enumerate(a) for _ in range(n)];out=set()
    for inds in combinations(range(17),5):
        cs=[values[i] for i in inds]
        if 0 in cs:continue
        for c7,n in enumerate(b):
            if n and c7>=1 and sum(cs)+c7==15:
                counts=Counter(cs);out.add((tuple(counts[c] for c in range(7)),c7))
    return out

def check():
    tallies=[]
    for i,(a,b) in enumerate(profiles(5,2)):
        R=direct_rows(a,b);expected=set()
        for U,V in product(R,repeat=2):
            if any(x+y>n for x,y,n in zip(U[0],V[0],a)):continue
            if U[1]==V[1] and b[U[1]]<2:continue
            expected.add(tuple(sorted((U,V))))
        if expected!=set(cases(i)):raise AssertionError(('case cover',i))
        for j,(U,V) in enumerate(cases(i)):
            S,T,groups=roles(i,j)
            if any(len(x)!=5 for x in S) or S[0]&S[1] or len(set(T))!=2:raise AssertionError('center roles')
            cs={v:c for v,c in enumerate([c for c,n in enumerate(a) for _ in range(n)]+[c for c,n in enumerate(b) for _ in range(n)],13)}
            for j0 in (0,1):
                if sum(cs[v] for v in S[j0])+cs[T[j0]]!=15:raise AssertionError('pair sum')
            vertices=[v for G in groups for v in G]+list(T)
            if sorted(vertices)!=list(range(13,54)):raise AssertionError('role partition')
            for G in groups:
                colors={(6 if v<30 else 7,cs[v],int(v in S[0]),int(v in S[1])) for v in G}
                if len(colors)>1:raise AssertionError('row symmetry')
        tallies.append(len(expected))
    return {'profiles':len(tallies),'center_case_counts':tallies,'total_cases':sum(tallies),'empty_profiles':[i for i,n in enumerate(tallies) if not n]}


def endpoint_check():
    triples=[T for T in combinations_with_replacement((1,2,3),3) if sum(T)==5]
    if triples!=[(1,1,3),(1,2,2)]:raise AssertionError('endpoint triples')
    pairs={tuple(sorted((U,V))) for U,V in product(triples,repeat=2) if all((Counter(U)+Counter(V))[c]<=n for c,n in [(1,4),(2,15),(3,3)])}
    if len(pairs)!=3:raise AssertionError('endpoint pair coverage')
    return {'endpoint_types':[list(T) for T in triples],'unordered_type_pairs':len(pairs),'remaining_six_role_sizes':[1,3,3]}


from verify import graph,hoffman_singleton_edges,check_girth_and_identities

def positive_control():
    G=graph(50,hoffman_singleton_edges());edges=check_girth_and_identities(G)
    masks=[sum(1<<u for u in N) for N in G];count=0;partitions=0
    for a in range(50):
        for b in G[a]:
            for x in G[a]-{b}:
                for y in G[b]-{a}:
                    H={x,a,b,y}
                    if len(H)!=4:raise AssertionError('induced path distinctness')
                    A=G[a]-H;B=G[b]-H;I=A|B
                    if A&B or len(I)!=10 or any(G[u]&I for u in I):raise AssertionError('independent neighborhoods')
                    if (G[x]|G[y])&I:raise AssertionError('endpoint exclusion')
                    MA=sum(1<<u for u in A);MB=sum(1<<u for u in B)
                    for v in set(range(50))-H-I:
                        if (masks[v]&MA).bit_count()+(x in G[v])!=1:raise AssertionError('first-center partition')
                        if (masks[v]&MB).bit_count()+(y in G[v])!=1:raise AssertionError('second-center partition')
                        partitions+=2
                    count+=1
    if count!=12600:raise AssertionError('all oriented paths')
    return {'graph':'Hoffman-Singleton','vertices':50,'edges':edges,'oriented_induced_P4':count,'individual_partition_checks':partitions}


def histogram_check():
    from verify_forest_reduction import independent_rows
    expected={(a,b) for q,a in independent_rows(6,17,49,5) for r,b in independent_rows(7,24,45,5) if q+r==5}
    actual={(tuple(a),tuple(b)) for a,b in profiles(5,2)}
    if expected!=actual or len(actual)!=15:raise AssertionError('whole histogram cover')
    return len(actual)

def endpoint_role_check():
    a,b=profiles(5,2)[1];cs={v:c for v,c in enumerate([c for c,n in enumerate(a) for _ in range(n)]+[c for c,n in enumerate(b) for _ in range(n)],13)}
    S7,T7,_=roles(1,0)
    for e in range(3):
        S,T,G=endpoint_roles(e)
        if any(len(U)!=4 for U in S) or len(S[0]&S[1])!=1:raise AssertionError('endpoint six roles')
        if any(len(U)!=3 for U in T) or T[0]&T[1]:raise AssertionError('endpoint seven roles')
        if any(sum(cs[v] for v in S[i]|T[i])!=17 for i in range(2)):raise AssertionError('endpoint high coverage')
        members=[v for group in G for v in group]
        if len(set(members))!=len(members):raise AssertionError('row group overlap')
        for group in G:
            colors={(6 if v<30 else 7,cs[v],v in S7[0] or v==T7[0],v in S7[1] or v==T7[1],v in S[0] or v in T[0],v in S[1] or v in T[1]) for v in group}
            if len(colors)>1:raise AssertionError('endpoint row symmetry')
    return 3

def main():
    import json
    result={'center_cover':check(),'complete_histograms':histogram_check(),'endpoint_cover':endpoint_check(),'endpoint_role_cases':endpoint_role_check(),'positive_control':positive_control(),'sat_cases':len(CASES)}
    if len(CASES)!=52 or len(set(CASES))!=52:raise AssertionError('final case cover')
    print(json.dumps(result,sort_keys=True));return result

if __name__=='__main__':main()
