"""Credited distinct-rank/bottom-up primitives from native-binary-barrier.
No producer/profiler import. Same-author independent algorithms, not review.
"""
import hashlib,json
from functools import lru_cache
from itertools import combinations
METRICS={}

def need(test, message):
    if not test:
        raise ValueError(message)


def count(name, amount=1):
    METRICS[name] = METRICS.get(name, 0) + amount


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def marked(value):
    return value < 0 or value > 1


def ports(row):
    return [sum(2 ** i for i, v in enumerate(row) if v < 0),
            sum(2 ** i for i, v in enumerate(row) if v > 1)]


def simulate(row, gates):
    values = list(row)
    for a, b in gates:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def template(n, low, high):
    need(low >= 0 and high >= 0 and not low & high and (low | high) < 2 ** n,
         "invalid original marker masks")
    lows = [i for i in range(n) if low >> i & 1]
    highs = [i for i in range(n) if high >> i & 1]
    free = [i for i in range(n) if not (low | high) >> i & 1]
    row = [0] * n
    for rank, i in enumerate(lows):
        row[i] = rank - len(lows)
    for rank, i in enumerate(highs):
        row[i] = rank + 2
    return row, free


def family(n, gates, low, high, level):
    initial, free = template(n, low, high)
    touches = final = None
    active = 0
    for x in range(2 ** len(free)):
        row = list(initial)
        for j, i in enumerate(free):
            row[i] = x >> j & 1
        hit_mask = 0
        for t, (a, b) in enumerate(gates):
            hit = marked(row[a]) or marked(row[b])
            if hit:
                hit_mask |= 2 ** t
            if row[a] > row[b]:
                if not hit:
                    active |= 2 ** t
                row[a], row[b] = row[b], row[a]
        if touches is None:
            touches, final = hit_mask, ports(row)
        need(touches == hit_mask and final == ports(row), "free-dependent marker route")
        count(level + "_free_assignments")
        count(level + "_gate_evaluations", len(gates))
    redundant = (2 ** len(gates) - 1) & ~(touches | active)
    return [low, high, *final, touches.bit_count(), redundant.bit_count(), redundant]


def pruning(n, gates, record):
    low, high = record[:2]
    reference, free = template(n, low, high)
    carrier = [free.index(i) if i in free else None for i in range(n)]
    word, touches = [], 0
    for t, (a, b) in enumerate(gates):
        if marked(reference[a]) or marked(reference[b]):
            touches |= 2 ** t
            need(not record[6] >> t & 1, "marked gate also deleted as free identity")
            if reference[a] > reference[b]:
                reference[a], reference[b] = reference[b], reference[a]
                carrier[a], carrier[b] = carrier[b], carrier[a]
        elif not record[6] >> t & 1:
            word.append([carrier[a], carrier[b]])
    output_free = [i for i in range(n) if not marked(reference[i])]
    rename = {carrier[i]: j for j, i in enumerate(output_free)}
    need(sorted(rename) == list(range(len(free))), "nonbijective free-carrier routing")
    result = {"outer_record": record, "marked_touch_mask": touches,
              "input_free_wires": free, "output_free_wires": output_free,
              "input_to_output_wire": [rename[i] for i in range(len(free))],
              "retained_prefix": [[rename[a], rename[b]] for a, b in word]}
    need(touches.bit_count() == record[4] and record[6].bit_count() == record[5],
         "deletion count differs")
    need(len(word) + record[4] + record[5] == len(gates), "gates not partitioned")
    for x in range(2 ** len(free)):
        full = list(template(n, low, high)[0])
        small = [0] * len(free)
        for j, i in enumerate(free):
            full[i] = small[rename[j]] = x >> j & 1
        actual = simulate(full, gates)
        need([actual[i] for i in output_free] == simulate(small, result["retained_prefix"]),
             "conditional pruning function differs")
        count("pruning_function_assignments")
    return result


def ordinary_initial(prefix,high):
    by_port={}
    anchor=4096 if high else 1
    for pair in combinations(range(13),2):
        mask=sum(1<<q for q in pair)
        row=family(13,prefix,0 if high else mask,mask if high else 0,'ordinary_original')
        current=row[3] if high else row[2]
        need(current&anchor and current.bit_count()==2,'extreme anchor missing')
        port=(current^anchor).bit_length()-1
        by_port[port]=max(by_port.get(port,-1),row[4])
    return tuple(sorted(by_port.items()))


def passage(profile,gate,high):
    grouped={}
    anchor=12 if high else 0
    for port,cost in profile:
        row=[0]*13
        row[anchor]=3 if high else -2
        row[port]=2 if high else -1
        a,b=gate
        touched=marked(row[a]) or marked(row[b])
        row=simulate(row,[gate])
        mask=ports(row)[1 if high else 0]^(1<<anchor)
        need(mask.bit_count()==1,'secondary marker route not unary')
        p=mask.bit_length()-1
        grouped[p]=max(grouped.get(p,-1),cost+int(touched))
        count('numeric_profile_class_passages')
    return tuple(sorted(grouped.items()))


def mass(profile):return sum(1<<d for _,d in profile)


def tree_word(tree,high):
    if tree[0]=='L':return [],tree[1]
    left,lp=tree_word(tree[1],high);right,rp=tree_word(tree[2],high)
    return left+right+[[min(lp,rp),max(lp,rp)]],max(lp,rp) if high else min(lp,rp)


def full_family_function(word,support):
    outputs=[]
    for x in range(1<<len(support)):
        row=[0]*13
        for j,q in enumerate(support):row[q]=x>>j&1
        row=simulate(row,word)
        outputs.append(sum(row[q]<<j for j,q in enumerate(support)))
        count('binary_family_function_assignments')
    return tuple(outputs)


@lru_cache(None)
def forest_cover(profile,high):
    initial=tuple((p,d,('L',p)) for p,d in profile)
    todo=[initial];seen={initial};terminal=set()
    while todo:
        forest=todo.pop()
        if len(forest)==1:
            need(forest[0][1]==9,'terminal genealogy cost differs')
            terminal.add(forest[0][2]);continue
        for i,j in combinations(range(len(forest)),2):
            p,d,t=forest[i];q,e,u=forest[j];count('binary_forest_pair_controls')
            node=(max(p,q) if high else min(p,q),1+max(d,e),('N',*sorted([t,u])))
            child=tuple(sorted([v for k,v in enumerate(forest) if k not in (i,j)]+[node]))
            if sum(1<<v[1] for v in child)>512:continue
            if child not in seen:seen.add(child);todo.append(child)
    support=sorted(p for p,_ in profile)
    functions={full_family_function(tree_word(t,high)[0],support) for t in terminal}
    need(len(functions)==len(terminal),'different terminal trees have equal full functions')
    count('binary_forest_states',len(seen));count('binary_terminal_forests',len(terminal))
    return functions
