"""Independent packed-rank reachable-set audit, no researcher imports.

Every original marked family remains separate.  Exact duplicate states are
removed after each gate, never by shared marker locations between families.
Kernel trees are built backwards by capacity splits, then linearized.
"""
import argparse
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


FAMILIES = [('one_minimum', 1, 0), ('one_maximum', 0, 1),
            ('two_minima', 2, 0), ('two_maxima', 0, 2), ('mixed_pair', 1, 1)]
SIZES = {11: 35, 12: 39}  # Imported published theorems, not re-proved here.
METRICS = {'original_assignments': 0, 'state_gate_steps': 0,
           'family_histories': 0, 'kernel_linearizations': 0,
           'kernel_function_controls': 0}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(obj):
    return sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def gate(row, a, b):
    va, vb = (row >> (2*a)) & 3, (row >> (2*b)) & 3
    if va > vb:
        row ^= (va ^ vb) << (2*a)
        row ^= (va ^ vb) << (2*b)
    return row


def marker_ports(row, n, lo):
    low = high = 0
    for i in range(n):
        value = (row >> (2*i)) & 3
        if value < lo:
            low |= 1 << i
        elif value > lo+1:
            high |= 1 << i
    return low, high


def initial_family(n, low, high):
    lo = len(low)
    free = [i for i in range(n) if i not in low and i not in high]
    template = sum(lo << (2*i) for i in free)
    template += sum(j << (2*i) for j, i in enumerate(low))
    template += sum((lo+2+j) << (2*i) for j, i in enumerate(high))
    # Set expansion supplies every free assignment, including both extremes.
    states = {template}
    for i in free:
        bit = 1 << (2*i)
        states |= {row+bit for row in states}
    require(len(states) == 1 << len(free), 'input assignment coverage')
    METRICS['original_assignments'] += len(states)
    METRICS['family_histories'] += 1
    return [sum(1 << i for i in low), sum(1 << i for i in high),
            sum(1 << i for i in low), sum(1 << i for i in high), 0, 0, 0], states


def advance(history, word, offset, lo, n=13):
    record, states = history
    r = list(record)
    for t, (a, b) in enumerate(word, offset):
        marked = bool((r[2] | r[3]) & ((1 << a) | (1 << b)))
        active = False
        image = set()
        for row in states:
            va, vb = (row >> (2*a)) & 3, (row >> (2*b)) & 3
            require(marked == (va < lo or va > lo+1 or vb < lo or vb > lo+1),
                    'marker topology depends on free values')
            if va > vb:
                active = True
                row ^= ((va ^ vb) << (2*a)) | ((va ^ vb) << (2*b))
            image.add(row)
        if marked:
            r[4] += 1
        elif not active:
            r[5] += 1
            r[6] |= 1 << t
        port_set = {marker_ports(row, n, lo) for row in image}
        require(len(port_set) == 1, 'nonconstant final marker topology')
        r[2], r[3] = port_set.pop()
        METRICS['state_gate_steps'] += len(states)
        states = image
    return r, states


def clamped_prefix(word):
    result = {}
    for name, lo, hi in FAMILIES:
        members = []
        for low in combinations(range(13), lo):
            other = [i for i in range(13) if i not in low]
            for high in combinations(other, hi):
                h = initial_family(13, low, high)
                members.append(advance(h, word, 0, lo))
        result[name] = members
    return result


def extend(data, word, offset):
    return {name: [advance(h, word, offset, lo) for h in data[name]]
            for name, lo, hi in FAMILIES}


def snapshot(data):
    families = {}
    for name, lo, hi in FAMILIES:
        records = sorted(r for r, _ in data[name])
        classes = {}
        for r in records:
            lp, hp = r[2:4]
            d, c = classes.get((lp, hp), (0, 0))
            classes[lp, hp] = max(d, r[4]), max(c, r[4]+r[5])
        env = [[lp, hp, d, c] for (lp, hp), (d, c) in sorted(classes.items())]
        families[name] = {'low_count': lo, 'high_count': hi, 'envelope': env,
                          'records_sha256': digest(records), 'summary': {
            'ordinary_mass': sum(1 << x[2] for x in env),
            'semantic_mass': sum(1 << x[3] for x in env),
            'maximum_deletions': max(r[4] for r in records),
            'maximum_semantic_deletions': max(r[4]+r[5] for r in records),
            'maximum_redundancies': max(r[5] for r in records),
            'port_classes': len(env)}}
    anchors = {}
    for direction, col, count, unary in [('low', 0, 'low_count', 'one_minimum'),
                                       ('high', 1, 'high_count', 'one_maximum')]:
        items = {name: x for name, x in families.items() if x[count]}
        reachable = sorted(r[col].bit_length()-1 for r in families[unary]['envelope'])
        rows = []
        for p in reachable:
            masses = {name: sum(1 << r[3] for r in x['envelope'] if r[col] & (1 << p))
                      for name, x in items.items()}
            label = max(SIZES[13-x['low_count']-x['high_count']] + (masses[name]-1).bit_length()
                        for name, x in items.items() if masses[name])
            rows.append({'port': p, 'anchored_masses': masses, 'label': label,
                         'units': 1 << (label-35)})
        units = sum(x['units'] for x in rows)
        anchors[direction] = {'base': 35, 'normalized_mass': units,
                              'lower_bound': 35+(units-1).bit_length(), 'rows': rows}
    return {'families': families, 'anchors': anchors}


def simulate_bool(x, word):
    # A second representation for literal images and kernel controls.
    for a, b in word:
        if x & (1 << a) and not x & (1 << b):
            x ^= (1 << a) | (1 << b)
    return x


def image(word):
    return {simulate_bool(x, word) for x in range(8192)}


def sorted_bool(x, n):
    return ((1 << x.bit_count())-1) << (n-x.bit_count())


def target(states, start, stop):
    rows = sorted({(x >> start) & ((1 << (stop-start))-1) for x in states})
    return {'n': stop-start, 'original_wires': list(range(start, stop)),
            'size': len(rows), 'image': rows, 'image_sha256': digest(rows),
            'weight_counts': [sum(x.bit_count() == w for x in rows) for w in range(stop-start+1)]}


def reverse_capacity_trees():
    """Leaves 5..10 have capacity one; leaf 11 has capacity two.

    Split every capacity 2^j node into two equal 2^(j-1) children.
    Require the least labelled leaf to be in the first child only to
    remove the child exchange; no merge-order DFS is used.
    """
    def capacity(leaves):
        return sum(2 if i == 11 else 1 for i in leaves)

    @lru_cache(None)
    def trees(leaves):
        if len(leaves) == 1:
            return ((leaves[0], ()),)
        total = capacity(leaves)
        require(total & (total-1) == 0, 'non-dyadic node capacity')
        answer = []
        for width in range(1, len(leaves)):
            for rest in combinations(leaves[1:], width-1):
                left = tuple(sorted((leaves[0],)+rest))
                if capacity(left)*2 != total:
                    continue
                right = tuple(i for i in leaves if i not in left)
                for (lp, ln), (rp, rn) in product(trees(left), trees(right)):
                    a, b = sorted((lp, rp))
                    # All descendant gates must precede their parent; listing
                    # every descendant is harmless and avoids a decoder bridge.
                    descendants = tuple(sorted(x[0] for x in ln+rn))
                    node = ((a, b), 6+(total.bit_length()-1), descendants)
                    answer.append((b, ln+rn+(node,)))
        return tuple(answer)
    reps = {}
    for endpoint, nodes in trees(tuple(range(5, 12))):
        require(endpoint == 11 and len(nodes) == 6, 'tree root')
        canonical = tuple(x[0] for x in sorted(nodes, key=lambda x: (x[1], x[0])))
        require(canonical not in reps, 'duplicate capacity tree')
        reps[canonical] = nodes
    return reps


def linearizations(nodes):
    def visit(done, word):
        if len(word) == len(nodes):
            yield tuple(word)
            return
        for pair, level, deps in nodes:
            if pair not in done and all(x in done for x in deps):
                yield from visit(done | {pair}, word+[pair])
    yield from visit(set(), [])


def verify_local_and_small_controls():
    tests = 0
    for a, b in combinations(range(3), 2):
        for row in product(range(4), repeat=3):
            x = sum(v << (2*i) for i, v in enumerate(row))
            expect = list(row);expect[a], expect[b] = min(row[a],row[b]),max(row[a],row[b])
            require(gate(x,a,b) == sum(v << (2*i) for i,v in enumerate(expect)), 'rank decoder')
            tests += 1
    small = [(0,1),(2,3),(0,2),(1,3),(1,2)]
    for x in range(16):
        require(simulate_bool(x,small) == sorted_bool(x,4), 'known small sorter')
    # Compression must preserve activity and every redundancy, not only output.
    for lo, hi in [(1,0),(0,1),(2,0),(0,2),(1,1)]:
        for low in combinations(range(4),lo):
            for high in combinations([i for i in range(4) if i not in low],hi):
                raw = initial_family(4,low,high)
                words = [small,small+[(1,2)],list(reversed(small))]
                for word in words:
                    calculated,_ = advance(raw,word,0,lo,4)
                    d=r=mask=0
                    rows=list(raw[1])
                    for t,(a,b) in enumerate(word):
                        touched={(((x>>(2*a))&3)<lo or ((x>>(2*a))&3)>lo+1 or
                                  ((x>>(2*b))&3)<lo or ((x>>(2*b))&3)>lo+1) for x in rows}
                        require(len(touched)==1,'small marker trajectory')
                        hit=touched.pop()
                        moved=[gate(x,a,b) for x in rows]
                        if hit: d+=1
                        elif rows==moved: r+=1;mask |= 1 << t
                        rows=moved
                    require(calculated[4:]==[d,r,mask],'deduplication changes activity')
                    tests+=1
    return tests


def local_marker_transport():
    """Exhaust all local tag fibres, including oriented anchor transport.

    The proof for arbitrary n reduces to these endpoint configurations;
    unaffected outside ports are retained in this enumeration as controls.
    Costs remain symbolic: injectivity with a charged gate gives doubling,
    and a double fibre with both costs charged gives max(2u,2v)>=u+v.
    """
    tests = 0
    for n in range(2, 6):
        configs = list(product(range(3), repeat=n))
        for a in range(n):
            for b in range(n):
                if a == b:
                    continue
                transitions = {}
                for x in configs:
                    y = list(x)
                    y[a], y[b] = min(x[a], x[b]), max(x[a], x[b])
                    charged = x[a] != 1 or x[b] != 1
                    transitions[x] = tuple(y), charged
                fibres = {}
                for x, (y, charge) in transitions.items():
                    fibres.setdefault(y, []).append((x, charge))
                for fibre in fibres.values():
                    require(len(fibre) <= 2, 'marker fibre bigger than two')
                    if len(fibre) == 2:
                        require(all(charge for _, charge in fibre), 'uncharged double fibre')
                    tests += 1
                for tag, destination in [(0, a), (2, b)]:
                    for p in range(n):
                        restricted = {x: value for x, value in transitions.items() if x[p] == tag}
                        target_p = destination if p in [a, b] else p
                        require(all(y[target_p] == tag for y, charge in restricted.values()),
                                'anchor membership lost')
                        subfibres = {}
                        for x, (y, charge) in restricted.items():
                            subfibres.setdefault(y, []).append(charge)
                        if p in [a, b]:
                            require(all(len(v) == 1 and v[0] for v in subfibres.values()),
                                    'touched anchor lacks charged injectivity')
                        else:
                            require(all(len(v) <= 2 and (len(v) == 1 or all(v))
                                        for v in subfibres.values()), 'untouched anchor loses mass')
                        tests += len(restricted)
    return tests


def reconstruct(fixture, certificate):
    word = fixture['gates']
    require(fixture['n']==13 and len(word)==46 and fixture['prefix_length']==24,'dimensions')
    require(all(isinstance(a,int) and isinstance(b,int) and 0<=a<b<13 for a,b in word),'standard gates')
    require(digest(word)=='9adf68d7c1185ae5601aa2336bae54a8a08b7e94a08e2574b8c89c24d8b092c6','literal word')
    p=word[:24]; forced=[(11,12),(1,2)]
    require(fixture['forced_gates']==[list(x) for x in forced],'forced fixture')
    data24=clamped_prefix(p);data25=extend(data24,[forced[0]],24);data26=extend(data25,[forced[1]],25)
    prefix_snapshots=[snapshot(x) for x in [data24,data25,data26]]
    require(prefix_snapshots==[certificate[k] for k in ['prefix24','prefix25','prefix26']],'prefix snapshots')
    # A proved dependency reduction: ordinary paired-extreme costs alone
    # supply both saturated initial anchors, using only S(11)>=35.
    paired_anchors={}
    for direction,col,paired,unary in [('low',0,'two_minima','one_minimum'),
                                     ('high',1,'two_maxima','one_maximum')]:
        family=prefix_snapshots[0]['families'][paired]
        ports=[r[col].bit_length()-1 for r in prefix_snapshots[0]['families'][unary]['envelope']]
        rows=[]
        for port in ports:
            mass=sum(1 << r[2] for r in family['envelope'] if r[col] & (1 << port))
            require(mass>0,'paired family fails to define a reachable anchor')
            rows.append({'port':port,'ordinary_paired_mass':mass,'label':35+(mass-1).bit_length()})
        require(sum(1 << r['label'] for r in rows)==1 << 44,'paired saturation')
        paired_anchors[direction]=rows
    img25=image(p+[forced[0]]);img26={simulate_bool(x,[forced[1]]) for x in img25}
    m11=target(img25,1,12);m10=target(img26,2,12)
    require(m11==certificate['middle11'] and m10==certificate['middle10'],'intermediate images')
    for t,key in [(m11,'middle11_upper21'),(m10,'middle10_upper20')]:
        n=t['n'];control=fixture[key]
        require(len(control)==n+10 and all(0<=a<b<n for a,b in control),'positive control word')
        require(all(simulate_bool(x,control)==sorted_bool(x,n) for x in t['image']),'positive control sorting')
    normalized=p+forced+[(a+2,b+2) for a,b in fixture['middle10_upper20']]
    for control in [word,normalized]:
        require(all(simulate_bool(x,control)==sorted_bool(x,13) for x in range(8192)),'full positive control')
    cover=reverse_capacity_trees()
    require(len(cover)==45,'capacity tree coverage')
    rebuilt=[];extras=[];survivor_sets={}
    for number,canonical in enumerate(sorted(cover)):
        for alternative in linearizations(cover[canonical]):
            for x in range(128):
                require(simulate_bool(x<<5,alternative)==simulate_bool(x<<5,canonical),'topological order changes function')
                METRICS['kernel_function_controls']+=1
            METRICS['kernel_linearizations']+=1
        continued=extend(data26,canonical,26);snap=snapshot(continued)
        rows=sorted(r for r,_ in continued['two_maxima'])
        bound=max(x['lower_bound'] for x in snap['anchors'].values())
        witness=next((r for r in rows if r[4]+r[5]>=10),None) if bound>44 else None
        require((bound>44)==(witness is not None),'exclusion witness completeness')
        middle={simulate_bool(x,canonical) for x in img26}
        for x in middle:
            sorted_x=sorted_bool(x,13)
            require((x & 6147)==(sorted_x & 6147),'outer pairs are not the sorted extremes')
        t=target(middle,2,11)
        case={'id':number,'kernel':[list(x) for x in canonical], 'snapshot':snap,'target':t,
              'excluded_at_44':bound>44,'two_maximum_exclusion_record':witness}
        require(case==certificate['kernels'][number],f'kernel {number} differs')
        rebuilt.append(case)
        if bound<=44:survivor_sets[number]=set(t['image'])
        else:extras.append({'id':number,'record':witness})
    require(METRICS['kernel_linearizations']==900,'linearization coverage')
    require(len({tuple(k['target']['image']) for k in rebuilt})==45,'distinct targets')
    remaining=sorted(survivor_sets)
    require(remaining==certificate['remaining_ids'] and len(remaining)==39,'remaining kernel identities')
    require([x['id'] for x in extras]==[1,13,22,35,43,44],'excluded identities')
    dual=lambda x:sum((1-((x>>i)&1))<<(8-i) for i in range(9))
    literal_inclusions=[(i,j) for i in remaining for j in remaining if i!=j and survivor_sets[i]<=survivor_sets[j]]
    dual_inclusions=[(i,j) for i in remaining for j in remaining if set(map(dual,survivor_sets[i]))<=survivor_sets[j]]
    require(not literal_inclusions and not dual_inclusions,'claimed residual antichain fails')
    actual={'schema':'native24-kernel-cover-certificate-v1','agent':'six-sorting-2','role':'researcher',
            'native_gate_list_sha256':digest(word),'budget':44,'prefix_length':24,
            'prefix24':prefix_snapshots[0],'prefix25':prefix_snapshots[1],'prefix26':prefix_snapshots[2],
            'middle11':m11,'middle10':m10,'kernel_count':len(rebuilt),'kernels':rebuilt,'remaining_ids':remaining}
    require(actual==certificate,'complete certificate equality')
    corruptions=[]
    bad=deepcopy(certificate);bad['kernels'][0]['target']['image'][1]=7;corruptions.append(bad)
    bad=deepcopy(certificate);bad['kernels'][1]['two_maximum_exclusion_record'][6]=0;corruptions.append(bad)
    bad=deepcopy(certificate);bad['prefix26']['families']['two_maxima']['envelope'].pop();corruptions.append(bad)
    bad=deepcopy(certificate);bad['remaining_ids'].append(44);corruptions.append(bad)
    require(all(actual!=x for x in corruptions),'damaged certificate accepted')
    return {'status':'INDEPENDENT_NATIVE24_AUDIT_PASSED','reviewer':'six-reviewer-5',
            'role':'independent mathematical reviewer','kernels':45,'survivors':remaining,
            'excluded_records':extras,'middle11_size':m11['size'],'middle10_size':m10['size'],
            'survivor_sizes':[rebuilt[i]['target']['size'] for i in remaining],
            'complete_reconstructed_certificate_sha256':digest(actual),'literal_inclusions':literal_inclusions,
            'reverse_complement_inclusions':dual_inclusions,'ordered_inclusion_comparisons':2*39*38+39,
            'ordinary_paired_anchors_using_only_S11':paired_anchors,
            'corruptions_rejected':len(corruptions)}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input-dir',required=True)
    args=parser.parse_args();root=Path(args.input_dir)
    raw=(root/'certificate.json').read_bytes()
    require(sha256(raw).hexdigest()=='21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06','pinned certificate')
    fixture_raw=(root/'fixture.json').read_bytes()
    require(sha256(fixture_raw).hexdigest()=='93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6','pinned fixture')
    controls=verify_local_and_small_controls()
    transport=local_marker_transport()
    # Controls have different workloads; main counts only the audited instance.
    for key in METRICS:METRICS[key]=0
    result=reconstruct(json.loads(fixture_raw),json.loads(raw))
    result['local_small_controls']=controls;result['metrics']=METRICS
    result['local_marker_transport_controls']=transport
    result['certificate_raw_sha256']=sha256(raw).hexdigest()
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
