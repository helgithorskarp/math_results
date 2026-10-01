"""Exact-column producer of a small, complete oriented continuation tree.

Only specified original clamping domains are retained. All 128 assignments of
each domain survive; equal current marker configurations are grouped only when
forming the lower potential. No solver, heuristic cache, or depth normal form
is used. The independent verifier uses scalar numeric ranks instead.
"""
from collections import deque
import hashlib
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
CAP = 2**28
ORIENTED = [(a,b) for a in range(13) for b in range(13) if a != b]


def original(low, high):
    if low & high or low.bit_count()!=3 or high.bit_count()!=3:
        raise ValueError('invalid original clamping')
    tags = tuple(-1 if low>>p&1 else 1 if high>>p&1 else 0 for p in range(13))
    free = [p for p in range(13) if not (low|high)>>p&1]
    columns = [0]*13
    for x in range(128):
        for j,p in enumerate(free):
            columns[p] |= ((x>>j)&1)<<x
    return tags,tuple(columns),0,0


def advance(row, gate, time_index):
    tags,columns,touch,redundancy = row
    tags,columns = list(tags),list(columns)
    a,b = gate
    if tags[a] or tags[b]:
        touch |= 1<<time_index
        if tags[a] > tags[b]:
            tags[a],tags[b] = tags[b],tags[a]
            columns[a],columns[b] = columns[b],columns[a]
    else:
        x,y = columns[a],columns[b]
        if not x & ~y:
            redundancy |= 1<<time_index
        columns[a],columns[b] = x&y,x|y
    return tuple(tags),tuple(columns),touch,redundancy


def config(row):
    return (sum(1<<p for p,t in enumerate(row[0]) if t<0),
            sum(1<<p for p,t in enumerate(row[0]) if t>0))


def envelope(rows):
    grouped = {}
    for row in rows:
        key = config(row)
        cost = row[2].bit_count()+row[3].bit_count()
        grouped[key] = max(grouped.get(key,0),cost)
    return grouped


def mass(rows):
    return sum(2**cost for cost in envelope(rows).values())


def digest(values):
    return hashlib.sha256(','.join(map(str,values)).encode('ascii')).hexdigest()


def certificate(fixture, fixture_hash):
    result = {'schema':'joint-six-extreme-complete-oriented-tree-v1',
              'agent':'six-sorting-1','role':'researcher',
              'fixture_sha256':fixture_hash,'n':13,'l':3,'h':3,
              'free_inputs':7,'small_size_lower_bound':16,'size_budget':44,
              'cap':CAP,'oriented_comparators':156,
              'remaining_nine_wire_ids':fixture['remaining_nine_wire_ids'],'cases':[]}
    for case in fixture['cases']:
        states = []
        roots = []
        for low,high in case['original_clampings']:
            row = original(low,high)
            for t,gate in enumerate(case['prefix']):
                row = advance(row,gate,t)
            states.append(row)
            roots.append({'original_low_mask':low,'original_high_mask':high,
                          'current_low_mask':config(row)[0],
                          'current_high_mask':config(row)[1],
                          'marked_touch_mask':row[2],'redundancy_mask':row[3],
                          'D':row[2].bit_count(),'R':row[3].bit_count(),
                          'C':row[2].bit_count()+row[3].bit_count()})
        if mass(states)!=CAP:
            raise ValueError('root is not at the cap')
        queue = deque([([],states)])
        nodes = []
        while queue:
            word,rows = queue.popleft()
            bad = next((j for j,row in enumerate(rows) if config(row)!=(7,7168)),None)
            if bad is None:
                raise ValueError('a retained branch has no marker obstruction')
            node = {'word':word,'selected_mass':mass(rows),
                    'configurations':len(envelope(rows)),
                    'nonterminal_original_domain':bad,
                    'at_size_budget':len(word)==12,'allowed_next':[],
                    'blocked_minimum_mass':None,'transition_mass_sha256':None}
            if len(word)<12:
                weights,blocked = [],[]
                for gate in ORIENTED:
                    after = [advance(row,gate,32+len(word)) for row in rows]
                    weight = mass(after)
                    weights.append(weight)
                    if weight<=CAP:
                        node['allowed_next'].append(list(gate))
                        queue.append((word+[list(gate)],after))
                    else:
                        blocked.append(weight)
                node['blocked_minimum_mass'] = min(blocked)
                node['transition_mass_sha256'] = digest(weights)
            nodes.append(node)
        result['cases'].append({'kernel_id':case['kernel_id'],
                                'prefix_size':32,'suffix_budget':12,
                                'selected_original_domains':roots,
                                'nodes':nodes,'nodes_checked':len(nodes),
                                'oriented_transitions_checked':156*sum(not n['at_size_budget'] for n in nodes)})
    return result


def main():
    begin = time.monotonic()
    raw = (ROOT/'fixture.json').read_bytes()
    fixture = json.loads(raw)
    result = certificate(fixture,hashlib.sha256(raw).hexdigest())
    data = (json.dumps(result,indent=2)+'\n').encode()
    (ROOT/'certificate.json').write_bytes(data)
    print(json.dumps({'agent':'six-sorting-1','role':'researcher',
                      'status':'JOINT_EXTREME_ORIENTED_TREE_REGENERATED',
                      'kernel_ids':[c['kernel_id'] for c in result['cases']],
                      'tree_nodes':[c['nodes_checked'] for c in result['cases']],
                      'oriented_transitions':sum(c['oriented_transitions_checked'] for c in result['cases']),
                      'certificate_sha256':hashlib.sha256(data).hexdigest(),
                      'seconds':time.monotonic()-begin,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':
    main()
