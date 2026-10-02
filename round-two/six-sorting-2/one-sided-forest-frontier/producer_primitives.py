"""Credited packed primitives from native-binary-barrier, sourcea1e3686.
No inner/nested solver or old negative certificate is imported.
"""
import hashlib,json
from functools import lru_cache
from itertools import combinations,product
import profile as s

def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def pairings(xs):
    if not xs:
        yield []
    else:
        for j in range(1, len(xs)):
            for tail in pairings(xs[1:j]+xs[j+1:]):
                yield [(xs[0], xs[j])]+tail


def profile_step(state, gate, high):
    result = {}
    for port, cost in state:
        target = gate[1] if high else gate[0]
        if port not in gate:
            target = port
        result[target] = max(result.get(target, -1), cost+(port in gate))
    return sorted(result.items())


def record_for(gates,low,high):
    free=[q for q in range(13) if not (low|high)>>q&1]
    columns=iter(s.truth_columns(len(free)))
    values=[s.LOW if low>>q&1 else s.HIGH if high>>q&1 else next(columns) for q in range(13)]
    d=r=mask=0
    for t,(a,b) in enumerate(gates):
        hit,inactive=s.transition(values,a,b)
        d+=hit;r+=inactive
        if inactive:mask|=1<<t
    return [low,high,*s.marked_ports(values),d,r,mask]


def prune(gates, record):
    """Remove marked touches and inactive free gates, tracking free carriers."""
    low, high = record[:2]
    free = [p for p in range(13) if not ((low | high) >> p) & 1]
    columns = s.truth_columns(len(free))
    values = [s.LOW if (low >> p) & 1 else
              s.HIGH if (high >> p) & 1 else columns[free.index(p)]
              for p in range(13)]
    carriers = [None if ((low | high) >> p) & 1 else free.index(p)
                for p in range(13)]
    retained, d, r, redundant_mask, touched_mask = [], 0, 0, 0, 0
    for t, (a, b) in enumerate(gates):
        if isinstance(values[a], str) or isinstance(values[b], str):
            d += 1
            touched_mask |= 1 << t
            order = lambda z: -1 if z == s.LOW else 1 if z == s.HIGH else 0
            if order(values[a]) > order(values[b]):
                values[a], values[b] = values[b], values[a]
                carriers[a], carriers[b] = carriers[b], carriers[a]
        else:
            if values[a] & ~values[b]:
                retained.append([carriers[a], carriers[b]])
            else:
                r += 1
                redundant_mask |= 1 << t
            values[a], values[b] = values[a] & values[b], values[a] | values[b]
    lp, hp = s.marked_ports(values)
    if [low, high, lp, hp, d, r, redundant_mask] != record:
        raise ValueError("pruning record does not match the complete conditional domain")
    output_free = [p for p in range(13) if carriers[p] is not None]
    rename = {carriers[p]: j for j, p in enumerate(output_free)}
    return {"outer_record": record, "marked_touch_mask": touched_mask,
            "input_free_wires": free, "output_free_wires": output_free,
            "input_to_output_wire": [rename[j] for j in range(len(free))],
            "retained_prefix": [[rename[a], rename[b]] for a, b in retained]}


def leaf(p):return ('L',p)


def node(a,b):return ('N',*sorted([a,b]))


def tree_word(t,high):
    if t[0]=='L':return [],t[1]
    lw,a=tree_word(t[1],high);rw,b=tree_word(t[2],high)
    return lw+rw+[[min(a,b),max(a,b)]],max(a,b) if high else min(a,b)


def trees(small,large):
    answer=[]
    if len(large)==2:
        for u,b in product(small,large):
            other=sorted(set(small)-{u});other_big=next(q for q in large if q!=b)
            unequal=node(leaf(u),leaf(b))
            equal=node(node(*map(leaf,other)),leaf(other_big))
            answer.append(node(unequal,equal))
        for u in small:
            other=sorted(set(small)-{u})
            answer.append(node(node(leaf(u),node(*map(leaf,other))),node(*map(leaf,large))))
    elif len(large)==1:
        b=large[0]
        for u in small:
            rest=sorted(set(small)-{u})
            for pairs in pairings(rest):
                answer.append(node(node(leaf(u),leaf(b)),node(*(node(*map(leaf,p)) for p in pairs))))
            for pair in combinations(rest,2):
                other=sorted(set(rest)-set(pair))
                unequal=node(leaf(u),node(*map(leaf,pair)))
                equal=node(leaf(b),node(*map(leaf,other)))
                answer.append(node(unequal,equal))
    else:raise ValueError('unexpected native inventory')
    if len(set(answer))!=len(answer):raise ValueError('duplicate genealogies')
    return sorted(answer)
