"""Standalone independent numeric original-cube and bottom-up cover checker.
No producer, sibling module, solver or graph import is used. Numeric pruning,
profile and heap-Huffman primitives are adapted with credit from six-sorting-2
changed-b28-barrier/verify.py, source7f0c4f85a073c697803d580d3d04d4cba2aed07e.
Bottom-up genealogy differs from production's top-down tree enumeration;
full scalar free cubes differ from production's packed Boolean columns.
Same executing researcher; no external-person review is claimed.
"""
from functools import lru_cache
from copy import deepcopy
import hashlib
import heapq
from itertools import combinations, permutations
import json
from pathlib import Path
import resource
import time
ROOT=Path(__file__).resolve().parent
FIXTURE_SHA256='7dc82cad50dd461d6f19cb24d8b5f0d4f68ee0d62fffa0122bd4e4aa173de60f'
SIZES=(0,0,1,3,5,9,12,16,19,25,29,35,39,44)
FAMILIES=(("one_minimum",1,0),("one_maximum",0,1),("two_minima",2,0),
          ("two_maxima",0,2),("mixed_pair",1,1))
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


def summary(records, l, h):
    records.sort()
    classes = {}
    for row in records:
        key = tuple(row[2:4])
        d, c = classes.get(key, (0, 0))
        classes[key] = max(d, row[4]), max(c, row[4] + row[5])
    envelope = [[lo, hi, d, c] for (lo, hi), (d, c) in sorted(classes.items())]
    return {"low_count": l, "high_count": h, "envelope": envelope,
            "records_sha256": digest(records),
            "summary": {"ordinary_mass": sum(2 ** row[2] for row in envelope),
                        "semantic_mass": sum(2 ** row[3] for row in envelope),
                        "maximum_deletions": max(row[4] for row in records),
                        "maximum_semantic_deletions": max(row[4] + row[5] for row in records),
                        "maximum_redundancies": max(row[5] for row in records),
                        "port_classes": len(envelope)}}


def profiles(n, gates, level="inner"):
    result = {}
    for name, l, h in FAMILIES:
        if l + h > n:
            continue
        records = []
        for lows in combinations(range(n), l):
            other = [i for i in range(n) if i not in lows]
            for highs in combinations(other, h):
                low, high = sum(2 ** i for i in lows), sum(2 ** i for i in highs)
                records.append(family(n, gates, low, high, level))
        result[name] = summary(records, l, h)
    return result


def ceil_log(mass):
    need(mass > 0, "empty dyadic mass")
    e = 0
    while 2 ** e < mass:
        e += 1
    return e


def huffman(labels):
    heap = list(labels)
    need(bool(heap), "empty route set")
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, 1 + max(a, b))
    return heap[0]


def anchor_bounds(n, data):
    result = {}
    for side, column, count_name, unary in (("low", 0, "low_count", "one_minimum"),
                                          ("high", 1, "high_count", "one_maximum")):
        chosen = {name: item for name, item in data.items() if item[count_name]}
        sizes = {name: SIZES[n - item["low_count"] - item["high_count"]]
                 for name, item in chosen.items()}
        base = min(sizes.values())
        reachable = sorted(row[column].bit_length() - 1 for row in data[unary]["envelope"])
        rows = []
        for p in reachable:
            masses = {name: sum(2 ** row[3] for row in item["envelope"] if row[column] >> p & 1)
                      for name, item in chosen.items()}
            label = max(sizes[name] + ceil_log(mass) for name, mass in masses.items() if mass)
            rows.append({"port": p, "anchored_masses": masses, "label": label,
                         "units": 2 ** (label - base)})
        units = sum(row["units"] for row in rows)
        b = huffman(row["label"] for row in rows)
        need(b == base + ceil_log(units), "Huffman and dyadic formulas differ")
        result[side] = {"base": base, "normalized_mass": units, "lower_bound": b, "rows": rows}
    return result


def bound(n, gates, level="control"):
    if n < 2:
        return 0
    return max(x["lower_bound"] for x in anchor_bounds(n, profiles(n, gates, level)).values())


def move(classes, gate, low):
    a, b = gate
    target = a if low else b
    result = {}
    for p, d in classes:
        hit = p in gate
        q = target if hit else p
        result[q] = max(result.get(q, -1), d+int(hit))
    return tuple(sorted(result.items()))


def mass(classes):
    return sum(2**d for _, d in classes)


@lru_cache(None)
def reachable(classes, low):
    """Merge currently live blocks, memoizing forests and cluster genealogies."""
    initial = tuple((1 << p, p, d) for p, d in classes)
    initial = (tuple(sorted(initial)), ())
    todo, visited, terminal = [initial], {initial}, set()
    local_gates = 0
    equality_count = 0
    while todo:
        forest, history = todo.pop()
        current = tuple(sorted((p, d) for _, p, d in forest))
        old_mass = mass(current)
        need(old_mass <= 512, 'reachable forest exceeds ordinary ceiling')
        live = {p for p, _ in current}
        for gate in combinations(range(1, 12), 2):
            new_mass = mass(move(current, gate, low))
            hits = len(live.intersection(gate))
            need(new_mass >= old_mass, 'ordinary mass decreased')
            if hits == 0:
                need(new_mass == old_mass, 'free preparation changed class mass')
            if hits == 1:
                need(new_mass > old_mass, 'singleton does not strictly increase mass')
            if hits == 2:
                ds = [d for p, d in current if p in gate]
                need((new_mass == old_mass) == (ds[0] == ds[1]),
                     'equal-cost characterization failed')
                equality_count += int(ds[0] == ds[1])
            local_gates += 1
        if len(forest) == 1:
            need(forest[0][2] == 9 and old_mass == 512,
                 'terminal root is not exactly saturated')
            terminal.add(history)
            continue
        for i, j in combinations(range(len(forest)), 2):
            mask1, p1, d1 = forest[i]
            mask2, p2, d2 = forest[j]
            block = mask1 | mask2
            port = min(p1, p2) if low else max(p1, p2)
            d = max(d1, d2)+1
            future_mass = old_mass-2**d1-2**d2+2**d
            if future_mass > 512:
                continue
            need(not(mask1 & mask2), 'two forest blocks overlap')
            fresh = tuple(sorted([row for k, row in enumerate(forest) if k not in (i, j)]
                                 +[(block, port, d)]))
            next_history = tuple(sorted(history+(block,)))
            state = (fresh, next_history)
            if state not in visited:
                visited.add(state)
                todo.append(state)
    return tuple(sorted(terminal)), len(visited), local_gates, equality_count


def decode(history, classes, low):
    blocks = set(history) | {1 << p for p, _ in classes}
    full = sum(1 << p for p, _ in classes)
    def visit(block):
        if block & (block-1) == 0:
            return [], block.bit_length()-1
        proper = [b for b in blocks if b != block and b & block == b]
        children = [b for b in proper if not any(b != c and b & c == b for c in proper)]
        need(len(children) == 2 and children[0] ^ children[1] == block,
             'cluster hierarchy has invalid direct children')
        children.sort(key=lambda b: (b & -b).bit_length())
        wl, p = visit(children[0])
        wr, q = visit(children[1])
        return wl+wr+[sorted((p, q))], min(p, q) if low else max(p, q)
    return visit(full)


def packed_image(full, suffix):
    columns = [sum(1 << j for j, x in enumerate(full) if x >> p & 1) for p in range(13)]
    for a, b in suffix:
        columns[a], columns[b] = columns[a] & columns[b], columns[a] | columns[b]
    for p in (0, 1, 11, 12):
        expected = sum(1 << j for j, x in enumerate(full) if p >= 13-x.bit_count())
        need(columns[p] == expected, 'four held outputs are not correct')
    return sorted({sum((columns[p] >> j & 1) << (p-2) for p in range(2, 11))
                   for j in range(len(full))})



@lru_cache(None)
def inner_checked(word):
    data=profiles(7,[list(g) for g in word],'inner')
    anchors=anchor_bounds(7,data)
    lower=max(16,*(a['lower_bound'] for a in anchors.values()))
    return lower,data,anchors


def base_image(gates):
    columns=[sum(1<<x for x in range(8192) if x>>p&1) for p in range(13)]
    for a,b in gates:
        need(0<=a<b<13,'base comparator is not standard')
        columns[a],columns[b]=columns[a]&columns[b],columns[a]|columns[b]
    for p in (0,12):
        expected=sum(1<<x for x in range(8192) if p>=13-x.bit_count())
        need(columns[p]==expected,'B23 outer output rank differs')
    count('base_boolean_inputs',8192)
    return sorted({sum((columns[p]>>x&1)<<p for p in range(13)) for x in range(8192)})


def initial_classes(gates):
    result=[]
    for side in ('low','high'):
        records=[]
        for a,b in combinations(range(13),2):
            mask=(1<<a)+(1<<b)
            records.append(family(13,gates,mask if side=='low' else 0,
                                  mask if side=='high' else 0,'base_pair'))
        item=summary(records,2 if side=='low' else 0,2 if side=='high' else 0)
        current=[]
        for lo,hi,d,_ in item['envelope']:
            z=lo if side=='low' else hi
            held=0 if side=='low' else 12
            need(z>>held&1 and z.bit_count()==2,'ordinary pair held marker differs')
            p=(z^(1<<held)).bit_length()-1; current.append((p,d))
        current=tuple(sorted(current));need(mass(current)==448,'base ordinary mass differs')
        result.append(current)
    return result


def zero_slack_closure(classes,low):
    todo=[classes];seen={classes}
    while todo:
        state=todo.pop()
        for (p,d),(q,e) in combinations(state,2):
            if d!=e: continue
            child=move(state,tuple(sorted((p,q))),low)
            need(mass(child)==448,'equal event consumed first slack')
            if child not in seen:seen.add(child);todo.append(child)
    return sorted(seen)


def simultaneous_first_slack_controls(low,high):
    ls=zero_slack_closure(low,True);hs=zero_slack_closure(high,False)
    options=set(); tested=0; simultaneous=0
    for lc in ls:
        for hc in hs:
            need(not({p for p,_ in lc}&{p for p,_ in hc}),'pre-slack supports overlap')
            for gate in combinations(range(1,12),2):
                lm=mass(move(lc,gate,True));hm=mass(move(hc,gate,False));tested+=1
                if lm>448 and hm>448 and max(lm,hm)<=512:
                    lp=[(p,d) for p,d in lc if p in gate];hp=[(p,d) for p,d in hc if p in gate]
                    need(lp==[(3,6)] and len(hp)==1 and hp[0][1]==6,
                         'first simultaneous slack is not original light-leaf cross')
                    need(list(gate)==[3,hp[0][0]],'first simultaneous slack gate differs')
                    options.add(gate);simultaneous+=1
    need(options=={(3,h) for h in (5,6,7,9,10)},'first simultaneous-slack branch set differs')
    return {'pre_slack_low_states':len(ls),'pre_slack_high_states':len(hs),
            'pre_slack_gate_controls':tested,'simultaneous_first_slack_controls':simultaneous}


def rebuild_cover(low,high,full,partners):
    expected={};audit=[]
    for h in partners:
        gate=(3,h);lc=move(low,gate,True);hc=move(high,gate,False)
        need(mass(lc)==mass(hc)==512,'joint gate not saturated')
        lhist,ls,lg,le=reachable(lc,True);hhist,hs,hg,he=reachable(hc,False)
        need((len(lhist),len(hhist))==(3,9),'bottom-up joint cover count differs')
        audit.append({'h':h,'low_forests':ls,'high_forests':hs,'live_gate_controls':lg+hg,
                      'equal_cost_controls':le+he})
        for lh in lhist:
            lw,lp=decode(lh,lc,True)
            for hh in hhist:
                hw,hp=decode(hh,hc,False);suffix=[[3,h]]+lw+hw
                need(lp==1 and hp==11 and len(suffix)==9,'terminal live root differs')
                image=packed_image(full,suffix);key=tuple(tuple(g) for g in suffix)
                need(key not in expected,'duplicate canonical root')
                expected[key]=(len(image),digest(image))
    need(len(expected)==135,'independent cover is incomplete')
    return expected,audit


def check_cover(packet,expected,fixture):
    records=packet['root_records']
    need(len(records)==135,'missing or extra root')
    actual={}
    for i,case in enumerate(records):
        need(case['root_id']==i,'root identifier changed')
        key=tuple(tuple(g) for g in case['suffix_after_B23'])
        need(key not in actual,'root word repeats')
        actual[key]=(case['core_image_size'],case['core_image_sha256'])
        need(case['joint_gate']==case['suffix_after_B23'][0],'joint gate differs')
        need(digest(fixture['B23']+case['suffix_after_B23'])==fixture['root_selectors'][i]['prefix_sha256'],
             'literal selector prefix differs')
    need(actual==expected,'bottom-up exact root/image cover differs')


def replay_case(case,fixture):
    i=case['root_id'];gates=fixture['B23']+case['suffix_after_B23'];replay=[];seen=set();total=0
    selector=fixture['root_selectors'][i]['original_clampings']
    need(len(case['selected_records'])==len(selector),'selected original-domain cover differs')
    for row,masks in zip(case['selected_records'],selector):
        need(len(row)==8 and row[:2]==masks,'selected original domain differs')
        lo,hi=masks;need(lo.bit_count()==hi.bit_count()==3 and not lo&hi,'invalid original domain')
        original=family(13,gates,lo,hi,'outer');need(original==row[:7],'original numeric profile differs')
        pruned=pruning(13,gates,original)
        # This extra numeric field is checked above, but excluded from the producer transcript schema.
        del pruned['marked_touch_mask']
        q=tuple(tuple(g) for g in pruned['retained_prefix'])
        b,data,anchors=inner_checked(q)
        need(b==row[7],'independent inner lower bound differs')
        z=tuple(original[2:4]);need(z not in seen,'selected current class repeats');seen.add(z)
        label=sum(original[4:6])+b;total+=1<<label
        replay.append({'root_id':i,'original_low':lo,'original_high':hi,
            'outer_record':original,'retained_prefix':pruned['retained_prefix'],
            'pruning_sha256':digest(pruned),
            'inner_records_sha256':{name:r['records_sha256'] for name,r in data.items()},
            'inner_anchor_bounds':{side:r['lower_bound'] for side,r in anchors.items()},
            'inner_bound':b,'nested_label':label})
    need(total==case['selected_mass'] and total>1<<44,'strict selected mass inequality failed')
    return replay


def rejected(fn):
    try: fn()
    except ValueError:return 1
    raise ValueError('damaged mathematical certificate accepted')


def controls(fixture,packet,expected):
    sorter=fixture['positive7'];need(len(sorter)==16,'seven-wire control size differs')
    for x in range(128):
        row=[x>>p&1 for p in range(7)]
        need(simulate(row,sorter)==sorted(row),'seven-wire sorter control fails')
    need(max(16,bound(7,sorter,'positive_inner'))==16,'inner bound rejects optimal sorter')
    count('positive7_inputs',128)
    for perm in permutations(range(4)):
        gates=[[0,3],[2,1]];renamed=[[perm[a],perm[b]] for a,b in gates]
        need(bound(4,gates)==bound(4,renamed),'inner bound changes under global permutation')
        count('wire_permutation_controls')
    # Complete original-clamping positive control: a guaranteed full sorter above target size.
    tail=[[j-1,j] for i in range(1,13) for j in range(i,0,-1)]
    for lo,hi in fixture['root_selectors'][0]['original_clampings'][:2]:
        r=family(13,tail,lo,hi,'positive_outer');q=pruning(13,tail,r)['retained_prefix']
        for x in range(128):
            v=[x>>p&1 for p in range(7)]
            need(simulate(v,q)==sorted(v),'complete pruned positive sorter fails')
            count('pruned_positive_inputs')
        need(max(16,bound(7,q,'positive_inner'))<=len(q),'nested bound rejects pruned positive sorter')
    damages=0
    bad=deepcopy(packet);bad['root_records'].pop()
    damages+=rejected(lambda:check_cover(bad,expected,fixture))
    bad=deepcopy(packet);bad['root_records'][0]['suffix_after_B23'][1]=[1,4]
    damages+=rejected(lambda:check_cover(bad,expected,fixture))
    bad=deepcopy(packet);bad['root_records'][0]['core_image_size']+=1
    damages+=rejected(lambda:check_cover(bad,expected,fixture))
    for column in (4,5,6,7):
        bad=deepcopy(packet['root_records'][0]);bad['selected_records'][0][column]+=1
        damages+=rejected(lambda:replay_case(bad,fixture))
    bad=deepcopy(packet['root_records'][0]);bad['selected_mass']=1<<44
    damages+=rejected(lambda:replay_case(bad,fixture))
    return damages


def main():
    start=time.monotonic();raw=(ROOT/'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==FIXTURE_SHA256,'fixed fixture differs')
    fixture=json.loads(raw);raw=(ROOT/'certificate.json').read_bytes();packet=json.loads(raw)
    need(packet['schema']=='b23-joint-saturation-certificate-v1','certificate schema differs')
    need(packet['agent']=='six-sorting-1' and packet['role']=='researcher','signer attribution differs')
    need(packet['fixture_sha256']==FIXTURE_SHA256 and fixture['total_budget']==44,'proof scope differs')
    full=base_image(fixture['B23'])
    need(len(full)==packet['base_image_size']==179 and digest(full)==packet['base_image_sha256'],'base image differs')
    low,high=initial_classes(fixture['B23'])
    need([list(r) for r in low]==fixture['initial_low'] and [list(r) for r in high]==fixture['initial_high'],
         'initial independent ordinary classes differ')
    first=[]
    for gate in combinations(range(1,12),2):
        lm=mass(move(low,gate,True));hm=mass(move(high,gate,False))
        if max(lm,hm)<=512:first.append([*gate,lm,hm])
    need(first==packet['first_necessary_gate_map'] and len(first)==32,'first-gate map differs')
    first_controls=simultaneous_first_slack_controls(low,high)
    expected,audit=rebuild_cover(low,high,full,fixture['joint_partners']);check_cover(packet,expected,fixture)
    replay=[]
    for case in packet['root_records']:replay.extend(replay_case(case,fixture))
    need(len(replay)==packet['selected_domain_occurrences']==488,'selected domain census differs')
    need(inner_checked.cache_info().currsize==packet['distinct_inner_words']==269,'inner word census differs')
    need(digest(replay)==packet['replay_records_sha256'],'complete replay transcript differs')
    minimum=min(r['selected_mass'] for r in packet['root_records'])
    need(minimum==packet['minimum_selected_mass'] and packet['total44_mass_ceiling']==1<<44,'mass summary differs')
    need(packet['literal_joint_prefixes_excluded']==135 and packet['simultaneous_first_slack_branches_excluded']==5,
         'summary scope differs')
    proof_metrics=dict(METRICS);damages=controls(fixture,packet,expected)
    result={'agent':'six-sorting-1','role':'researcher','status':'COMPLETE_JOINT_SATURATION_CERTIFICATE_VERIFIED',
      'certificate_sha256':hashlib.sha256(raw).hexdigest(),'literal_roots':135,'joint_gates':5,
      'selected_original_domains':488,'unique_proof_inner_words':269,
      'replay_records_sha256':digest(replay),'minimum_selected_mass':minimum,'ceiling':1<<44,
      'proof_metrics':proof_metrics,'control_metrics':{k:v-proof_metrics.get(k,0) for k,v in METRICS.items() if v!=proof_metrics.get(k,0)},
      'first_slack_controls':first_controls,'forest_audit':audit,'damages_rejected':damages,
      'same_author_algorithmic_independence':True,'external_review_claimed':False,
      'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
