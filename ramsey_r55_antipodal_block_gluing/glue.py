"""Exact conditional K5 lifting across three vertex-disjoint bipartite holes.

No solver or symmetry assumption. Budgets return INCOMPLETE, never NO_LIFT.
This generic oracle takes ALL visible colors as input; it does not search
for a visible R55 assignment and is not a verdict for the fixed H92 family.
"""
import argparse
import itertools as it
import json
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


class BudgetExceeded(Exception):
    pass


class Budget:
    def __init__(self, limit):
        need(type(limit) is int and limit >= 0, 'nonnegative work limit')
        self.limit = limit; self.used = 0

    def tick(self):
        self.used += 1
        if self.used > self.limit:
            raise BudgetExceeded


def prepare(data):
    n = data['n']; need(type(n) is int and n >= 5, 'graph order')
    blocks = data['blocks']; need(len(blocks) == 3, 'exactly three holes')
    vertices = []; edges = []; margins = []
    for k, block in enumerate(blocks):
        need(len(block) == 2, 'two block sides'); L,R = block
        need(L and R and all(type(v) is int and 0 <= v < n for v in L+R), 'block labels')
        need(L == sorted(L) and R == sorted(R), 'canonical side order')
        vertices.extend(L+R)
        edges.append([tuple(sorted((u,v))) for u in L for v in R])
        a,b = data['row_margins'][k],data['column_margins'][k]
        need(len(a) == len(L) and len(b) == len(R), 'margin lengths')
        need(all(type(x) is int and 0 <= x <= len(R) for x in a) and
             all(type(x) is int and 0 <= x <= len(L) for x in b), 'margin bounds')
        margins.append((a,b))
    need(len(vertices) == len(set(vertices)), 'vertex-disjoint hole blocks')
    owner = {e:(k,i) for k,block in enumerate(edges) for i,e in enumerate(block)}
    red_input = data['red_visible_edges']; red = set()
    for e in red_input:
        need(type(e) is list and len(e) == 2 and all(type(v) is int for v in e), 'red pair type')
        u,v = e; need(0 <= u < v < n and (u,v) not in owner, 'visible canonical red pair')
        need((u,v) not in red, 'duplicate red pair'); red.add((u,v))
    need(red_input == sorted(red_input), 'canonical visible edge order')
    return n,blocks,edges,margins,owner,red


def constraints(n, owner, red):
    """All visible colors have been fixed. Unlisted visible pairs are blue."""
    active = set(); first_fixed_bad = None
    for S in it.combinations(range(n),5):
        masks = [0,0,0]; visible_colors = set()
        for e in it.combinations(S,2):
            if e in owner:
                k,i = owner[e]; masks[k] |= 1 << i
            else:
                visible_colors.add(e in red)
        if len(visible_colors) > 1:
            continue
        need(visible_colors, 'a five-set cannot lie wholly in bipartite holes')
        color = visible_colors.pop(); support = tuple((k,m) for k,m in enumerate(masks) if m)
        need(len(support) <= 2, 'five-set block support')
        if not support:
            if first_fixed_bad is None:
                first_fixed_bad = {'vertices':list(S),'color':'red' if color else 'blue'}
        else:
            active.add((color,support))
    return sorted(active),first_fixed_bad


def violates(color, mask, state):
    return state & mask == mask if color else state & mask == 0


def domain(L,R,a,b,restrictions,budget):
    if sum(a) != sum(b):
        return []
    result = []; width = len(R)
    def visit(row, remaining, bits):
        budget.tick()
        if row == len(L):
            if all(x == 0 for x in remaining) and not any(violates(c,m,bits) for c,m in restrictions):
                result.append(bits)
            return
        slots = len(L)-row-1
        for chosen in it.combinations(range(width),a[row]):
            chosen = set(chosen); following = [x-(j in chosen) for j,x in enumerate(remaining)]
            if any(x < 0 or x > slots for x in following):
                continue
            new = bits | sum(1 << (row*width+j) for j in chosen)
            assigned = (1 << ((row+1)*width))-1
            if any(m & ~assigned == 0 and violates(c,m,new) for c,m in restrictions):
                continue
            visit(row+1,following,new)
    visit(0,list(b),0)
    return sorted(result)


def decide(data, work_limit=1000000):
    need(type(work_limit) is int and work_limit >= 0, 'nonnegative work limit')
    n,blocks,edges,margins,owner,red = prepare(data)
    active,fixed_bad = constraints(n,owner,red)
    report = {'n':n,'active_conditional_clauses':len(active), 'work_limit':work_limit,
              'scope':'one fully specified visible coloring and three prescribed pairs of margins'}
    if fixed_bad:
        return dict(report,status='NO_LIFT_VISIBLE_K5',witness=fixed_bad,work_used=0)
    budget = Budget(work_limit); domains = []; relations = {}
    try:
        for k,(L,R) in enumerate(blocks):
            restrictions = [(c,s[0][1]) for c,s in active if len(s) == 1 and s[0][0] == k]
            domains.append(domain(L,R,*margins[k],restrictions,budget))
        report['domains'] = domains
        if not all(domains):
            return dict(report,status='NO_LIFT_EMPTY_BLOCK',work_used=budget.used)
        for a,b in it.combinations(range(3),2):
            restrictions = [(c,s[0][1],s[1][1]) for c,s in active
                            if len(s) == 2 and (s[0][0],s[1][0]) == (a,b)]
            rel = []
            for A,B in it.product(domains[a],domains[b]):
                budget.tick()
                if not any(violates(c,ma,A) and violates(c,mb,B) for c,ma,mb in restrictions):
                    rel.append([A,B])
            relations[f'{a}-{b}'] = rel
        report['relations'] = relations
        ab = {tuple(x) for x in relations['0-1']}
        ac = {tuple(x) for x in relations['0-2']}
        bc = {tuple(x) for x in relations['1-2']}
        for A,B,C in it.product(*domains):
            budget.tick()
            if (A,B) in ab and (A,C) in ac and (B,C) in bc:
                graph = sorted(red | {e for block,state in zip(edges,(A,B,C))
                                      for i,e in enumerate(block) if state >> i & 1})
                return dict(report,status='LIFT_FOUND',states=[A,B,C],
                            graph={'n':n,'red_edges':[list(e) for e in graph]},work_used=budget.used)
        return dict(report,status='NO_LIFT_PAIRWISE_JOIN',work_used=budget.used)
    except BudgetExceeded:
        return dict(report,status='INCOMPLETE',work_used=budget.used)


def main():
    p = argparse.ArgumentParser(); p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True); p.add_argument('--work-limit',type=int,default=1000000)
    a = p.parse_args(); report = decide(json.loads(a.input.read_text()),a.work_limit)
    with a.output.open('x') as f:
        json.dump(report,f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps(report),flush=True)


if __name__ == '__main__':
    main()
