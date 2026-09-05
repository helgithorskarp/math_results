"""Exact row-domain backtracking for a regular rooted Ramsey(4,4) graph."""
from collections import Counter
from itertools import combinations


def search(H,B):
    """H is the root's red side, B its blue side; desired degree is len(H).

    Returns every labeled cross matrix as a tuple of original-order row masks.
    No graph isomorphism or symmetry assumption is made during this search.
    """
    n=len(H);m=len(B);degree=n;full=(1<<m)-1
    red_triples=[sum(1<<v for v in vs) for vs in combinations(range(m),3)
                 if all(B[a]>>b&1 for a,b in combinations(vs,2))]
    blue_triples=[sum(1<<v for v in vs) for vs in combinations(range(m),3)
                  if all(not(B[a]>>b&1) for a,b in combinations(vs,2))]
    col_targets=[degree-b.bit_count() for b in B]
    domains=[]
    for h in H:
        need=degree-1-h.bit_count()
        domains.append([t for t in range(1<<m) if t.bit_count()==need
                        and not any(t&r==r for r in red_triples)
                        and not any(not(t&r) for r in blue_triples)])
    order=sorted(range(n),key=lambda i:(len(domains[i]),i))
    nodes=Counter();solutions=[]

    def visit(rows,columns):
        depth=len(rows);nodes[depth]+=1
        if depth==n:
            if columns==col_targets:
                original=[0]*n
                for i,t in zip(order,rows):original[i]=t
                solutions.append(tuple(original))
            return
        i=order[depth]
        for t in domains[i]:
            new=[columns[b]+int(t>>b&1) for b in range(m)]
            if any(new[b]>col_targets[b] or new[b]+n-depth-1<col_targets[b] for b in range(m)):
                continue
            good=True
            for previous,s in enumerate(rows):
                j=order[previous];red=bool(H[i]>>j&1)
                common=t&s if red else full^(t|s)
                vertices=[v for v in range(m) if common>>v&1]
                if any(bool(B[a]>>b&1)==red for a,b in combinations(vertices,2)):
                    good=False;break
            if not good:continue
            # H is triangle-free. A possible 3-H + 1-B blue K4 is the
            # only remaining mixed four-set after the row and pair checks.
            for previous,j in enumerate(order[:depth]):
                if H[i]>>j&1:continue
                for earlier,jj in enumerate(order[:previous]):
                    if (H[i]>>jj&1) or (H[j]>>jj&1):continue
                    if (t|rows[previous]|rows[earlier])!=full:good=False;break
                if not good:break
            if good:visit(rows+[t],new)

    visit([],[0]*m)
    return {'domain_sizes':list(map(len,domains)),'row_order':order,
            'nodes_by_depth':[nodes[i] for i in range(n+1)],
            'solutions':sorted(solutions)}
