"""Separate definition-level gluing audit: build actual adjacency matrices."""
from collections import Counter
from itertools import combinations


def search(red_side,blue_side):
    """Inputs are lists of sets, not the production search's bit masks.

    Always append red-side vertices in natural order. At each addition,
    inspect every literal new four-set. All feasible cross matrices are kept.
    """
    n=len(red_side);m=len(blue_side);root=n+m
    adj=[[False]*(root+1) for _ in range(root+1)]
    for a in range(m):
        for b in blue_side[a]:adj[n+a][n+b]=True
    targets=[n-len(s) for s in blue_side]
    nodes=Counter();attempts=0;solutions=[]

    def visit(rows,columns):
        nonlocal attempts
        i=len(rows);nodes[i]+=1
        if i==n:
            if columns==targets:
                solutions.append(tuple(sum(1<<b for b in S) for S in rows))
            return
        old=list(range(i))+list(range(n,root+1))
        triples=list(combinations(old,3))
        for chosen in combinations(range(m),n-1-len(red_side[i])):
            attempts+=1;S=set(chosen)
            new=[columns[b]+int(b in S) for b in range(m)]
            if any(new[b]>targets[b] or new[b]+n-i-1<targets[b] for b in range(m)):continue
            for j in old:
                color=(j==root or (j<i and j in red_side[i]) or (n<=j<root and j-n in S))
                adj[i][j]=adj[j][i]=color
            good=True
            for a,b,c in triples:
                color=adj[i][a]
                if (adj[i][b]==color and adj[i][c]==color and adj[a][b]==color
                        and adj[a][c]==color and adj[b][c]==color):
                    good=False;break
            if good:visit(rows+[S],new)

    visit([],[0]*m)
    return {'nodes_by_depth':[nodes[i] for i in range(n+1)],'attempted_rows':attempts,
            'solutions':sorted(solutions)}
