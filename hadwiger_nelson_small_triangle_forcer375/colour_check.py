"""Exact exhaustive four-colour search with singleton propagation."""
def solve(n, edges, pins=(), triples=()):
    adj = [set() for _ in range(n)]
    incident = [[] for _ in range(n)]
    for u,v in edges:
        adj[u].add(v);adj[v].add(u)
    for t in triples:
        for v in t:incident[v].append(t)
    adj=[sorted(a) for a in adj]
    nodes=0;conflicts=0
    def propagate(masks,queue):
        while queue:
            v=queue.pop();bit=masks[v]
            if not bit or bit & (bit-1):raise RuntimeError('Non-singleton queue')
            for u in adj[v]:
                old=masks[u]
                if old & bit:
                    new=old & ~bit
                    if not new:return False
                    masks[u]=new
                    if new & (new-1)==0:queue.append(u)
            for t in incident[v]:
                fixed=[u for u in t if masks[u]==bit]
                if len(fixed)>=2:
                    for u in t:
                        if u in fixed:continue
                        old=masks[u];new=old & ~bit
                        if not new:return False
                        if new!=old:
                            masks[u]=new
                            if new & (new-1)==0:queue.append(u)
                    if len(fixed)==3:return False
        return True
    def dfs(masks,queue):
        nonlocal nodes,conflicts
        nodes+=1
        if not propagate(masks,queue):conflicts+=1;return None
        choices=[v for v,m in enumerate(masks) if m & (m-1)]
        if not choices:return [m.bit_length()-1 for m in masks]
        v=min(choices,key=lambda v:(masks[v].bit_count(),-len(adj[v]),v))
        used=0
        for m in masks:
            if m & (m-1)==0:used|=m
        candidates=masks[v] & used
        unused=masks[v] & ~used
        if unused:candidates |= unused & -unused
        while candidates:
            bit=candidates & -candidates;candidates-=bit
            child=masks.copy();child[v]=bit
            answer=dfs(child,[v])
            if answer is not None:return answer
        return None
    masks=[15]*n
    for v,c in pins:
        if masks[v]!=15 and masks[v]!=(1<<c):return None,{'nodes':0,'conflicts':1}
        masks[v]=1<<c
    answer=dfs(masks,[v for v,c in pins])
    return answer,{'nodes':nodes,'conflicts':conflicts}
