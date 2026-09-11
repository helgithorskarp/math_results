"""Independent, exact unit-propagation checker for DIMACS formulas."""
from collections import defaultdict,deque
def unit_contradiction(clauses):
    rows=[];occ=defaultdict(list);remaining=[];satisfied=[];queue=deque();assigned=set()
    for raw in clauses:
        c=set(raw)
        if any(-x in c for x in c):continue
        if not c:return True
        i=len(rows);rows.append(c);remaining.append(len(c));satisfied.append(False)
        for x in c:occ[x].append(i)
        if len(c)==1:queue.append(next(iter(c)))
    while queue:
        x=queue.popleft()
        if -x in assigned:return True
        if x in assigned:continue
        assigned.add(x)
        for i in occ[x]:satisfied[i]=True
        for i in occ[-x]:
            if satisfied[i]:continue
            remaining[i]-=1
            if remaining[i]==0:return True
            if remaining[i]==1:
                left=[y for y in rows[i] if -y not in assigned]
                if len(left)!=1:raise ValueError('Residual mismatch')
                queue.append(left[0])
    return False
def read_dimacs(path):
    clauses=[];current=[];header=None
    for line in path.read_text().splitlines():
        if not line or line.startswith('c'):continue
        if line.startswith('p'):
            _,kind,nv,nc=line.split()
            if kind!='cnf':raise ValueError('CNF required')
            header=int(nv),int(nc);continue
        for token in line.split():
            x=int(token)
            if x:current.append(x)
            else:clauses.append(current);current=[]
    if current or header is None or len(clauses)!=header[1]:raise ValueError('Malformed DIMACS')
    if any(abs(x)>header[0] for c in clauses for x in c):raise ValueError('Variable outside header')
    return clauses
