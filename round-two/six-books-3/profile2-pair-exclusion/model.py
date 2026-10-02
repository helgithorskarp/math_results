"""Type-word/equality matrix census and direct high-subset inventory.

These are producer algorithms. The physical checker separately uses actual
row weak multisets and binary-half subset generation. No private inputs.
"""
import collections
import hashlib
import itertools
import json

COUNTS = (0,0,3,1,2,3,0,2,2,1,1,1,1,1,0)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def configuration():
    types = tuple(m for m,n in enumerate(COUNTS,1) for _ in range(n))
    low_masks = [sum(1<<x for x,t in enumerate(types) if t & (1<<i)) for i in range(4)]
    budget = [72-sum(10-types[x].bit_count() for x in range(18) if low_masks[i] & (1<<x)) for i in range(4)]
    require(len(types)==18 and all(m.bit_count()==9 for m in low_masks), 'Degree margins')
    require(budget==[2,2,1,1], 'Exact mixed budgets')
    return list(COUNTS), types, budget

def partitions(length,capacity):
    def visit(code):
        if len(code)==length:
            yield tuple(code);return
        for k in range(min(capacity,max(code,default=-1)+2)):
            yield from visit(code+[k])
    yield from visit([])

def templates(types,budget):
    cells={m:[x for x,t in enumerate(types) if t==m] for m in sorted(set(types))}
    words=0;symmetric_words=0;matrices=set(); branches=[]
    for alpha in itertools.product(*([1,3] if d==3 else [1] for d in budget)):
        roles=[(i,red) for i in range(4) for red,n in [(True,alpha[i]),(False,budget[i]-alpha[i])] for _ in range(n)]
        require(len(roles)==6,'six units')
        choices=[[m for m in cells if bool(m&(1<<i))==red] for i,red in roles]
        before=len(matrices);wcount=0;scount=0
        for word in itertools.product(*choices):
            words+=1;wcount+=1
            walk=[[sum(bool(m&(1<<j)) for m,(r,_) in zip(word,roles) if r==i) for j in range(4)] for i in range(4)]
            if any(walk[i][j]!=walk[j][i] for i in range(4) for j in range(i)):
                continue
            symmetric_words+=1;scount+=1
            groups=[(m,[r for r,t in enumerate(word) if t==m]) for m in sorted(set(word))]
            for codes in itertools.product(*(list(partitions(len(indices),len(cells[m]))) for m,indices in groups)):
                columns=[0]*18
                for (m,indices),code in zip(groups,codes):
                    for role,label in zip(indices,code):
                        i,_=roles[role];columns[cells[m][label]]+=1<<(2*i)
                canonical=[]
                for m,indices in cells.items():canonical.extend(sorted(columns[x] for x in indices))
                matrices.add(tuple(canonical))
        branches.append({'red_row_sums':list(alpha),'type_words':wcount,'symmetric_type_words':scount,'new_templates':len(matrices)-before})
    return sorted(matrices),{'type_words':words,'symmetric_type_words':symmetric_words,'branches':branches}

def domains(types,budget):
    masks=[sum(1<<x for x,t in enumerate(types) if t&(1<<i)) for i in range(4)]
    rows=collections.defaultdict(list);examined=0
    for x,tx in enumerate(types):
        caps=[3 if tx&(1<<i) else 5 for i in range(4)]
        bounds=[(3 if budget[i]==3 else 1) if tx&(1<<i) else budget[i]-1 for i in range(4)]
        for neighbors in itertools.combinations([y for y in range(18) if y!=x],10-tx.bit_count()):
            examined+=1;star=sum(1<<y for y in neighbors)
            slack=[caps[i]-(star&masks[i]).bit_count() for i in range(4)]
            if any(not 0<=d<=bound for d,bound in zip(slack,bounds)):continue
            signature=sum(d<<(2*i) for i,d in enumerate(slack))
            rows[(x,signature)].append(star)
    return {k:tuple(sorted(v)) for k,v in rows.items()},examined,masks


def build():
    counts, types, budget = configuration()
    matrices, matrix_census = templates(types,budget)
    inventory, raw, masks = domains(types,budget)
    return dict(counts=counts,types=types,budget=budget,matrices=matrices,
                matrix_census=matrix_census,domains=inventory,raw_stars=raw,
                stored_stars=sum(len(v) for v in inventory.values()))
