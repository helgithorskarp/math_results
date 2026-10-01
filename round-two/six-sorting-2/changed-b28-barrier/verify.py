"""Standalone numeric complete P28 event cover and selected nested certificate.
Imports no producer, profiler, sibling checker or solver. General numeric
primitives are copied from this author's p22_verify.py at source bc3d409.
This is distinct same-author algorithmic evidence, not external review.
"""
from copy import deepcopy
import hashlib
import heapq
from itertools import combinations
import json
from pathlib import Path
import resource
import time
ROOT=Path(__file__).resolve().parent
FIXTURE_SHA256='b46d8382fc40a39ffcaad6ed7396318d8efb7efc03692b8bc160568e76dba1bb'
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


def ordinary(records):
    entries=sorted(r[:5] for r in records)
    groups={}
    for row in entries:
        z=tuple(row[2:4]);groups[z]=max(groups.get(z,-1),row[4])
    return {'records_sha256':digest(entries),
            'envelope':[[*z,d] for z,d in sorted(groups.items())],
            'mass':sum(2**d for d in groups.values())}


def continue_ordinary(records,gates):
    result=[]
    for row in records:
        lo,hi,newlo,newhi,d=row[:5]
        tags=[-1 if newlo>>i&1 else 2 if newhi>>i&1 else 0 for i in range(13)]
        for a,b in gates:
            d+=marked(tags[a]) or marked(tags[b])
            if tags[a]>tags[b]:tags[a],tags[b]=tags[b],tags[a]
        result.append([lo,hi,*ports(tags),d])
        count('ordinary_history_continuations')
    return result


def ordinary_transition(envelope,gate):
    grouped={};a,b=gate
    for lo,hi,d in envelope:
        tags=[-1 if lo>>p&1 else 2 if hi>>p&1 else 0 for p in range(13)]
        hit=marked(tags[a]) or marked(tags[b])
        if tags[a]>tags[b]:tags[a],tags[b]=tags[b],tags[a]
        target=tuple(ports(tags));grouped.setdefault(target,[]).append((d+hit,hit))
    out=[]
    for z,fibre in sorted(grouped.items()):
        need(len(fibre)<=2,'marker fibre larger than two')
        if len(fibre)==2:need(all(hit for _,hit in fibre),'uncharged double fibre')
        out.append([*z,max(d for d,_ in fibre)])
    return out


def nested_row(gates,low,high):
    need(low.bit_count()==high.bit_count()==3,'selected original counts differ')
    record=family(13,gates,low,high,'outer')
    pruned=pruning(13,gates,record)
    need(len(pruned['input_free_wires'])==7,'wrong free dimension')
    data=profiles(7,pruned['retained_prefix'],'inner');anchors=anchor_bounds(7,data)
    b=max(16,*(a['lower_bound'] for a in anchors.values()))
    return {'pruning':pruned,'inner_records_sha256':{name:a['records_sha256'] for name,a in data.items()},
            'inner_anchor_leaves':{side:[[r['port'],r['label']] for r in a['rows']] for side,a in anchors.items()},
            'inner_anchor_bounds':{side:a['lower_bound'] for side,a in anchors.items()},
            'inner_bound':b,'prefix_cost':record[4]+record[5],'nested_label':record[4]+record[5]+b}



def fixture_inputs():
    raw=(ROOT/'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==FIXTURE_SHA256,'literal fixture pin differs')
    f=json.loads(raw)
    need((f['schema'],f['n'],f['size_budget'],f['prefix_length'],f['l'],f['h'],f['free_inputs'])
         ==('changed-b28-fixed-fixture-v1',13,44,28,3,3,7),'fixture parameters differ')
    gates=f['prefix']+f['forced_maximum_word']
    need(len(f['prefix'])==28 and len(f['forced_maximum_word'])==3,
         'literal word lengths differ')
    need(all(type(a)==type(b)==int and 0<=a<b<13 for a,b in gates),'invalid standard gate')
    need(f['forced_maximum_word']==[[7,9],[9,11],[10,11]],'forced word differs')
    originals=f['original_clampings']
    need(1<=len(originals)<=20 and len({tuple(z) for z in originals})==len(originals),
         'selected original domains invalid')
    need(all(type(lo)==type(hi)==int and lo>=0 and hi>=0 and not lo&hi
             and (lo|hi)<2**13 and lo.bit_count()==hi.bit_count()==3 for lo,hi in originals),
         'invalid original clamping')
    return f,gates

def image_summary(rows):
    rows=sorted(set(rows))
    correct=[q for q in range(13)
             if all(((r>>q)&1)==int(q>=13-r.bit_count()) for r in rows)]
    return {'input_count':8192,'output_count':len(rows),'image_sha256':digest(rows),
            'correct_output_wires_on_all_boolean_inputs':correct,
            'weight_counts':[sum(r.bit_count()==w for r in rows) for w in range(14)]}

def cover_structure(f,low,high,root_image,terminal_image,middle):
    need(low['mass']==high['mass']==512,'P28 ordinary masses are not saturated')
    need(low['envelope']==[[3,0,9]],'P28 minimum envelope differs')
    need(high['envelope']==[[0,4224,6],[0,4608,6],[0,5120,8],[0,6144,7]],
         'P28 maximum envelope differs')
    states=[];lo=low['envelope'];hi=high['envelope']
    for cut in range(4):
        controls=[];events=[];preps=[]
        live_mask=0
        for l,h,d in lo+hi:live_mask|=l|h
        for a,b in combinations(range(13),2):
            gate=[a,b]
            nxt_lo=ordinary_transition(lo,gate)
            nxt_hi=ordinary_transition(hi,gate)
            lm=sum(2**r[2] for r in nxt_lo)
            hm=sum(2**r[2] for r in nxt_hi)
            if lm>512 or hm>512:
                kind='forbidden'
            elif nxt_hi!=hi:
                kind='event';events.append(gate)
            else:
                kind='preparation';preps.append(gate)
                need(not ((1<<a)|(1<<b))&live_mask,'preparation touches a live endpoint')
                need(nxt_lo==lo,'preparation changes saturated minimum data')
            controls.append([a,b,lm,hm,kind])
            count('standard_next_gate_controls')
        expected=[f['forced_maximum_word'][cut]] if cut<3 else []
        need(events==expected,'complete next-event list differs')
        free=[q for q in range(13) if not live_mask>>q&1]
        need(preps==[list(z) for z in combinations(free,2)],'preparation list incomplete')
        states.append({'cut':28+cut,'low_envelope':lo,'high_envelope':hi,
                       'allowed_event_gates':events,'preparation_wires':free,
                       'preparation_gate_count':len(preps),'next_gate_controls':controls})
        if cut<3:
            gate=f['forced_maximum_word'][cut]
            lo=ordinary_transition(lo,gate);hi=ordinary_transition(hi,gate)
    need(lo==[[3,0,9]] and hi==[[0,6144,9]],'terminal frozen envelope differs')
    need(middle['size']==80 and middle['image_sha256']
         =='1eb1f208b305e646f34963308548c950af5769446a247a1f7601af313db5e152',
         'literal peer target differs')
    need(all(q in terminal_image['correct_output_wires_on_all_boolean_inputs']
             for q in [0,1,11,12]),'terminal outer output controls fail')
    return {'prefix28_sha256':digest(f['prefix']),'small_size_lower_bound':35,
            'ordinary_ceiling_for_size44':512,'prefix28_low2':low,'prefix28_high2':high,
            'complete_event_states':states,'event_word_count':1,'forced_event_word':f['forced_maximum_word'],
            'prefix28_boolean_image':root_image,'prefix31_sha256':digest(f['prefix']+f['forced_maximum_word']),
            'prefix31_boolean_image':terminal_image,'middle9':middle}

def finish_certificate(f,cover,rows):
    tags=[tuple(r['pruning']['outer_record'][2:4]) for r in rows]
    need(len(tags)==len(set(tags)),'selected current tag classes overlap')
    mass=sum(2**r['nested_label'] for r in rows)
    need(mass>2**44,'selected nested mass is not an exclusion')
    return {'schema':'changed-b28-nested-barrier-v1','agent':'six-sorting-2','role':'researcher',
            'fixture_sha256':FIXTURE_SHA256,'n':13,'size_budget':44,'l':3,'h':3,'free_inputs':7,
            'cover':cover,'selected_original_domains':rows,'selected_classes':len(tags),
            'selected_mass':mass,'total_lower_bound':(mass-1).bit_length(),
            'maximum_individual_label':max(r['nested_label'] for r in rows)}

def boolean_rows(gates):
    rows=[]
    for x in range(8192):
        values=simulate([(x>>q)&1 for q in range(13)],gates)
        rows.append(sum(v<<q for q,v in enumerate(values)))
        count('boolean_input_controls')
        count('boolean_gate_evaluations',len(gates))
    return rows

def build():
    f,gates=fixture_inputs()
    low=ordinary([family(13,f['prefix'],sum(1<<p for p in pair),0,'cover')
                  for pair in combinations(range(13),2)])
    high=ordinary([family(13,f['prefix'],0,sum(1<<p for p in pair),'cover')
                   for pair in combinations(range(13),2)])
    root=image_summary(boolean_rows(f['prefix']))
    terminal_rows=boolean_rows(gates);terminal=image_summary(terminal_rows)
    image=sorted({(r>>2)&511 for r in terminal_rows})
    middle={'n':9,'original_wires':list(range(2,11)),'size':len(image),
            'image':image,'image_sha256':digest(image),
            'weight_counts':[sum(r.bit_count()==w for r in image) for w in range(10)]}
    cover=cover_structure(f,low,high,root,terminal,middle)
    rows=[nested_row(gates,lo,hi) for lo,hi in f['original_clampings']]
    return finish_certificate(f,cover,rows)

def damages(expected):
    changes=[]
    for k,v in [('n',12),('size_budget',45),('selected_mass',expected['selected_mass']-1)]:
        bad=deepcopy(expected);bad[k]=v;changes.append(bad)
    bad=deepcopy(expected);bad['cover']['complete_event_states'][0]['allowed_event_gates']=[]
    changes.append(bad)
    bad=deepcopy(expected);bad['selected_original_domains'][0]['pruning']['outer_record'][4]+=1
    changes.append(bad)
    bad=deepcopy(expected);bad['selected_original_domains'][0]['pruning']['retained_prefix'][0].reverse()
    changes.append(bad)
    bad=deepcopy(expected);bad['selected_original_domains'][0]['inner_bound']+=1
    changes.append(bad)
    bad=deepcopy(expected);bad['selected_original_domains'][0]['inner_records_sha256']['two_minima']='damaged'
    changes.append(bad)
    for bad in changes:
        rejected=False
        try:need(bad==expected,'damaged certificate')
        except ValueError:rejected=True
        need(rejected,'damaged certificate accepted')
        count('damaged_certificates_rejected')

def main():
    start=time.monotonic()
    expected=build();path=ROOT/'certificate.json'
    need(json.loads(path.read_text())==expected,'certificate differs from full numeric reconstruction')
    damages(expected)
    print(json.dumps({'status':'CHANGED_B28_SCALAR_CERTIFICATE_VERIFIED','agent':'six-sorting-2',
                      'role':'researcher','certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                      'selected_domains':expected['selected_classes'],'selected_mass':expected['selected_mass'],
                      'total_lower_bound':expected['total_lower_bound'],'metrics':METRICS,
                      'seconds':time.monotonic()-start,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))
if __name__=='__main__':main()
