"""Independent scalar verification of all retained oriented continuations.

The verifier imports no producer, profiler, sibling checker, search, or solver.
It explicitly retains the 128 numeric assignments of each ORIGINAL clamping.
Every next comparator, on every ordered pair of different thirteen-input ports,
is considered at each node below the total-size budget. No depth bound is used.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
FIXTURE_SHA256 = 'b4c5bf4dab6468b9443b63518d10a4316d4e2d8a9a584fe071961054a6fa0995'
COUNTS = {'scalar_comparator_evaluations':0,'conditional_identity_assignments':0,
          'oriented_transitions':0,'retained_nodes':0,'proof_root_assignments':0}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def fixture_from(raw):
    need(hashlib.sha256(raw).hexdigest()==FIXTURE_SHA256,'fixture pin differs')
    f = json.loads(raw)
    need((f['n'],f['l'],f['h'],f['free_inputs'],f['size_budget'],f['small_size_lower_bound'])
         ==(13,3,3,7,44,16),'mathematical parameters differ')
    kernels = {9:[[5,7],[6,8],[9,10],[7,8],[10,11],[8,11]],
               21:[[5,8],[6,9],[7,10],[8,9],[10,11],[9,11]]}
    need(f['forced_word']==[[11,12],[1,2]],'forced gates differ')
    need(f['native_prefix24']==f['known46'][:24],'native source prefix differs')
    need([c['kernel_id'] for c in f['cases']]==[9,21],'target IDs differ')
    for c in f['cases']:
        need(c['kernel']==kernels[c['kernel_id']],'literal kernel differs')
        need(c['prefix']==f['native_prefix24']+f['forced_word']+c['kernel'],
             'literal prefix components differ')
        need(len(c['prefix'])==32,'prefix size differs')
        need(len(c['original_clampings'])=={9:15,21:18}[c['kernel_id']],
             'selected original-domain count differs')
        need(len({tuple(x) for x in c['original_clampings']})==len(c['original_clampings']),
             'original domains repeated')
        for low,high in c['original_clampings']:
            need(0<=low<8192 and 0<=high<8192 and not low&high
                 and low.bit_count()==high.bit_count()==3,'invalid original domain')
    ids = [2,3,4,5,6,7,8,9,10,12,15,16,18,20,21,24,25,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42]
    need(f['parent_remaining_nine_wire_ids']==ids,'parent frontier differs')
    need(f['remaining_nine_wire_ids']==[i for i in ids if i not in (9,21)],'new frontier differs')
    for word in (f['known45'],f['known46'],*[c['prefix'] for c in f['cases']]):
        need(all(type(a)==type(b)==int and 0<=a<b<13 for a,b in word),'bad source comparator')
    need(len(f['known45'])==45 and len(f['known46'])==46,'positive control sizes differ')
    return f


def extreme(value):
    return value<0 or value>1


def ports(values):
    return (sum(2**p for p,x in enumerate(values) if x<0),
            sum(2**p for p,x in enumerate(values) if x>1))


def original_domain(low, high):
    lows = [p for p in range(13) if low>>p&1]
    highs = [p for p in range(13) if high>>p&1]
    free = [p for p in range(13) if not (low|high)>>p&1]
    assignments = []
    for assignment in range(128):
        row = [0]*13
        for j,p in enumerate(lows):row[p]=j-3
        for j,p in enumerate(highs):row[p]=j+2
        for j,p in enumerate(free):row[p]=(assignment>>j)&1
        assignments.append(row)
    return {'assignments':assignments,'touch':0,'redundancy':0}


def continued(domain, a, b, t):
    values = []
    touches = []
    active = False
    for before in domain['assignments']:
        hit = extreme(before[a]) or extreme(before[b])
        touches.append(hit)
        after = before[:]
        if before[a]>before[b]:
            after[a],after[b] = before[b],before[a]
            if not hit:active=True
        values.append(after)
        COUNTS['scalar_comparator_evaluations']+=1
    need(len(set(touches))==1,'touch depends on original free assignment')
    configurations = {ports(v) for v in values}
    need(len(configurations)==1,'marker configuration depends on original free assignment')
    return {'assignments':values,
            'touch':domain['touch']+(2**t if touches[0] else 0),
            'redundancy':domain['redundancy']+(2**t if not touches[0] and not active else 0)}


def root_domains(case):
    domains = []
    summaries = []
    for low,high in case['original_clampings']:
        row = original_domain(low,high)
        COUNTS['proof_root_assignments']+=128
        for t,(a,b) in enumerate(case['prefix']):row=continued(row,a,b,t)
        lo,hi = ports(row['assignments'][0])
        d,r = row['touch'].bit_count(),row['redundancy'].bit_count()
        summaries.append({'original_low_mask':low,'original_high_mask':high,
                          'current_low_mask':lo,'current_high_mask':hi,
                          'marked_touch_mask':row['touch'],'redundancy_mask':row['redundancy'],
                          'D':d,'R':r,'C':d+r})
        domains.append(row)
    return domains,summaries


def lower_envelope(domains):
    result = {}
    for row in domains:
        key = ports(row['assignments'][0])
        c = row['touch'].bit_count()+row['redundancy'].bit_count()
        if key not in result or c>result[key]:result[key]=c
    return result


def next_lower_weight(domains,a,b):
    # A rejected edge needs only its exact C and new marker configuration.
    # Activity is read on the complete original cube, never on a merged image.
    grouped = {}
    for domain in domains:
        representative = domain['assignments'][0]
        hit = extreme(representative[a]) or extreme(representative[b])
        c = domain['touch'].bit_count()+domain['redundancy'].bit_count()
        after = representative[:]
        if after[a]>after[b]:after[a],after[b]=after[b],after[a]
        if hit:c+=1
        else:
            is_identity = True
            for values in domain['assignments']:
                COUNTS['conditional_identity_assignments']+=1
                if values[a]>values[b]:is_identity=False
            if is_identity:c+=1
        key = ports(after)
        grouped[key] = max(grouped.get(key,0),c)
    return sum(2**c for c in grouped.values())


def reconstructed(f):
    result = {'schema':'joint-six-extreme-complete-oriented-tree-v1',
              'agent':'six-sorting-1','role':'researcher',
              'fixture_sha256':FIXTURE_SHA256,'n':13,'l':3,'h':3,
              'free_inputs':7,'small_size_lower_bound':16,'size_budget':44,
              'cap':268435456,'oriented_comparators':156,
              'remaining_nine_wire_ids':f['remaining_nine_wire_ids'],'cases':[]}
    for case in f['cases']:
        domains,roots = root_domains(case)
        need(sum(2**c for c in lower_envelope(domains).values())==268435456,'root is not saturated')
        need(len(lower_envelope(domains))==len(domains),'initial configurations are repeated')
        frontier = [([],domains)]
        cursor = 0
        nodes = []
        while cursor<len(frontier):
            word,states = frontier[cursor]
            cursor+=1
            need(len(word)<=12,'retained word exceeds size budget')
            grouped = lower_envelope(states)
            bad = next((j for j,s in enumerate(states) if ports(s['assignments'][0])!=(7,7168)),None)
            need(bad is not None,'retained prefix has no marked output obstruction')
            witness = states[bad]['assignments'][0]
            need(witness!=sorted(witness),'retained prefix sorts the alleged negative input')
            node = {'word':word,'selected_mass':sum(2**c for c in grouped.values()),
                    'configurations':len(grouped),'nonterminal_original_domain':bad,
                    'at_size_budget':len(word)==12,'allowed_next':[],
                    'blocked_minimum_mass':None,'transition_mass_sha256':None}
            need(node['selected_mass']<=268435456,'invalid retained branch')
            if len(word)<12:
                weights,blocked = [],[]
                for a in range(13):
                    for b in range(13):
                        if a==b:continue
                        weight = next_lower_weight(states,a,b)
                        weights.append(weight)
                        COUNTS['oriented_transitions']+=1
                        if weight<=268435456:
                            node['allowed_next'].append([a,b])
                            nxt = [continued(s,a,b,32+len(word)) for s in states]
                            need(sum(2**c for c in lower_envelope(nxt).values())==weight,
                                 'scalar continuation and transition weight disagree')
                            frontier.append((word+[[a,b]],nxt))
                        else:blocked.append(weight)
                need(len(weights)==156 and blocked,'transition census incomplete')
                node['blocked_minimum_mass'] = min(blocked)
                text = ','.join(str(x) for x in weights).encode('ascii')
                node['transition_mass_sha256'] = hashlib.sha256(text).hexdigest()
            nodes.append(node)
            COUNTS['retained_nodes']+=1
        need(len(nodes)=={9:47,21:1}[case['kernel_id']],'retained tree census differs')
        result['cases'].append({'kernel_id':case['kernel_id'],'prefix_size':32,'suffix_budget':12,
                                'selected_original_domains':roots,'nodes':nodes,
                                'nodes_checked':len(nodes),
                                'oriented_transitions_checked':156*sum(not n['at_size_budget'] for n in nodes)})
    return result


def match(candidate, expected):
    need(candidate==expected,'complete reconstructed certificate differs')


def frontier_control(f):
    joined = json.loads((ROOT/'frontier.json').read_text())
    need(joined['parent32_ids']==f['parent_remaining_nine_wire_ids'],'joined parent differs')
    need(joined['own_new_literal_exclusions']==[9,21],'joined own exclusions differ')
    need(joined['own_remaining30_ids']==f['remaining_nine_wire_ids'],'joined own frontier differs')
    need(joined['peer_exclusions']==[3,4,5,12,27,28],'imported peer exclusions differ')
    peer = [i for i in joined['parent32_ids'] if i not in joined['peer_exclusions']]
    need(joined['peer_remaining26_ids']==peer and len(peer)==26,'peer frontier arithmetic differs')
    expected = sorted(set(peer)&set(f['remaining_nine_wire_ids']))
    need(joined['joint_remaining24_ids']==expected and len(expected)==24,'joint frontier arithmetic differs')
    need(joined['peer_graph_ref']=='bafkreibfvq5abfuzrwlq7byncp32ro3r7i2eptegh75of6dxaowubiffwe'
         and joined['peer_graph_height']==8909,'imported graph provenance differs')
    need(joined['peer_source_commit']=='e260dd848eb8616697a952840c0027965e5851c3'
         and joined['peer_certificate_sha256']=='04bcf3e1617c3ae2ce026149d1c76f620c8acf6e38bdc448719e26fa3ecd2455',
         'imported source provenance differs')
    need(joined['own_certificate_sha256']==hashlib.sha256((ROOT/'certificate.json').read_bytes()).hexdigest(),
         'joined own certificate pin differs')
    # This checks the finite intersection arithmetic and provenance. The six
    # imported mathematical exclusions are dependencies, not re-proved here.


def boolean_sorter_control(n, word):
    for x in range(2**n):
        values = [(x>>p)&1 for p in range(n)]
        for a,b in word:
            if values[a]>values[b]:values[a],values[b]=values[b],values[a]
        need(values==sorted(values),'positive Boolean sorter fails')
        COUNTS['scalar_comparator_evaluations']+=len(word)


def main():
    begin = time.monotonic()
    f = fixture_from((ROOT/'fixture.json').read_bytes())
    raw = (ROOT/'certificate.json').read_bytes()
    candidate = json.loads(raw)
    expected = reconstructed(f)
    match(candidate,expected)
    frontier_control(f)
    positive = []
    for name in ('known45','known46'):
        word = f[name]
        boolean_sorter_control(13,word)
        for case in f['cases']:
            states = []
            for low,high in case['original_clampings']:
                s = original_domain(low,high)
                for t,(a,b) in enumerate(word):s=continued(s,a,b,t)
                need(all(v==sorted(v) for v in s['assignments']),'positive clamping control fails')
                states.append(s)
            weight = sum(2**c for c in lower_envelope(states).values())
            need(weight<=2**(len(word)-16),'selected lower potential rejects a known sorter')
            positive.append({'size':len(word),'kernel_witness_set':case['kernel_id'],'mass':weight})
    sorter7 = [[0,6],[2,3],[4,5],[0,2],[1,4],[3,6],[0,1],[2,5],
               [3,4],[1,2],[4,6],[2,3],[4,5],[1,2],[3,4],[5,6]]
    boolean_sorter_control(7,sorter7)
    damaged = [deepcopy(candidate) for _ in range(7)]
    damaged[0]['cases'][0]['selected_original_domains'][0]['redundancy_mask']^=1
    damaged[1]['cases'][0]['nodes'][0]['allowed_next'].pop()
    damaged[2]['cases'][1]['nodes'][0]['allowed_next'].append([2,3])
    damaged[3]['cases'][0]['nodes'].pop()
    damaged[4]['cases'][0]['nodes'][0]['transition_mass_sha256']='0'*64
    damaged[5]['cap']+=1
    damaged[6]['remaining_nine_wire_ids'].pop()
    for item in damaged:
        try:match(item,expected)
        except ValueError:pass
        else:raise ValueError('damaged certificate accepted')
    try:fixture_from((ROOT/'fixture.json').read_bytes()+b' ')
    except ValueError:pass
    else:raise ValueError('damaged fixture pin accepted')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher',
                      'status':'ALL_JOINT_EXTREME_ORIENTED_TREE_CHECKS_PASSED',
                      'kernel_ids':[9,21],'tree_nodes':[47,1],
                      'remaining_targets':30,'joint_remaining_targets':24,'minimum_sorter_total':45,
                      'full_boolean_positive_inputs':16384,'seven_wire_positive_inputs':128,
                      'positive_clamping_assignments':2*33*128,
                      'positive_lower_masses':positive,'corruptions_rejected':8,
                      'certificate_sha256':hashlib.sha256(raw).hexdigest(),**COUNTS,
                      'seconds':time.monotonic()-begin,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':
    main()
