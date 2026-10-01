"""Definition-level numeric P22 cover and nested-root certificate checker.

Imports no generator, profiler, sibling checker or solver. Scalar pruning,
family and heap primitives are copied from this author's nested_verify.py;
this remains same-author algorithmic independence, not external review.
"""
import argparse
from copy import deepcopy
import hashlib
import heapq
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent
PINS={'fixture.json':'93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6',
      'generate.py':'08a37678a11392ed46907ab30b2463d841e3e068764c09e410244490f2212381',
      'NESTED.md':'3c291c8796cc7586db522d515098debf769482dc5b2d6bf8467fd8aa03322433'}
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


def inputs():
    for name,pin in PINS.items():
        need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==pin,'dependency pin differs: '+name)
    native=json.loads((ROOT/'fixture.json').read_text())['gates']
    need(len(native)==46 and all(type(a)==type(b)==int and 0<=a<b<13 for a,b in native),
         'wrong native word')
    return native


def placements(n,l,h):
    for lows in combinations(range(n),l):
        other=[i for i in range(n) if i not in lows]
        for highs in combinations(other,h):
            yield sum(2**i for i in lows),sum(2**i for i in highs)


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


def high_anchor(data):
    chosen={name:item for name,item in data.items() if item['high_count']}
    sizes={name:SIZES[13-item['low_count']-item['high_count']] for name,item in chosen.items()}
    base=min(sizes.values());rows=[]
    for p in sorted(row[1].bit_length()-1 for row in data['one_maximum']['envelope']):
        masses={name:sum(2**r[3] for r in a['envelope'] if r[1]>>p&1) for name,a in chosen.items()}
        label=max(sizes[name]+ceil_log(m) for name,m in masses.items() if m)
        rows.append({'port':p,'anchored_masses':masses,'label':label,'units':2**(label-base)})
    units=sum(r['units'] for r in rows);height=huffman(r['label'] for r in rows)
    need(height==base+ceil_log(units),'high Huffman/dyadic mismatch')
    return {'base':base,'normalized_mass':units,'lower_bound':height,'rows':rows}


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


def event_cover(side):
    """All equality events, all orders, all standard next gates at each state."""
    minimum=side=='minimum';fixed=0 if minimum else 12
    initial={i:7 for i in range(1,5)} if minimum else {**{i:6 for i in range(5,11)},11:7}
    terminal={1:9} if minimum else {11:9}
    seen=set();words=[];representatives=set()
    def visit(live,word,nodes):
        key=tuple(sorted(live.items()))
        if key not in seen:
            seen.add(key)
            envelope=[[2**fixed+2**p,0,d] if minimum else [0,2**fixed+2**p,d]
                      for p,d in sorted(live.items())]
            need(sum(2**d for d in live.values())==512,'unsaturated live profile')
            for gate in combinations(range(13),2):
                out=ordinary_transition(envelope,gate)
                permitted=sum(2**r[2] for r in out)<=512
                avoids=not set(gate)&({fixed}|set(live))
                event=all(p in live for p in gate) and live[gate[0]]==live[gate[1]]
                need(permitted==(avoids or event),'incomplete equality-event rule')
                count(side+'_standard_state_transitions')
        if len(live)==1:
            need(live==terminal,'wrong terminal extreme route')
            representative=tuple(pair for _,pair in sorted(nodes))
            representatives.add(representative);words.append((tuple(word),representative))
            return
        for a,b in combinations(sorted(live),2):
            if live[a]!=live[b]:continue
            level=live[a]+1;following=dict(live)
            del following[b if minimum else a];following[a if minimum else b]=level
            visit(following,word+[(a,b)],nodes+[(level,(a,b))])
    visit(initial,[],[])
    for word,representative in words:
        for bits in range(2**len(initial)):
            row=[0]*13
            for j,p in enumerate(initial):row[p]=bits>>j&1
            need(simulate(row,word)==simulate(row,representative),'canonical event order changes function')
            count(side+'_event_order_boolean_controls')
    count(side+'_equality_states',len(seen));count(side+'_complete_event_words',len(words))
    return [list(map(list,w)) for w in sorted(representatives)],len(words)


def boolean_image(gates):
    result=set()
    for x in range(8192):
        result.add(tuple(simulate([x>>j&1 for j in range(13)],gates)))
        count('full_boolean_inputs')
    return result


def apply_image(image,gates):
    return {tuple(simulate(row,gates)) for row in image}


def target(image,start,stop):
    rows=sorted({sum(row[i]*2**(i-start) for i in range(start,stop)) for row in image})
    return {'n':stop-start,'original_wires':list(range(start,stop)),
            'size':len(rows),'image':rows,'image_sha256':digest(rows),
            'weight_counts':[sum(row.bit_count()==w for row in rows) for w in range(stop-start+1)]}


def cover(native):
    prefix=native[:22];original={};data={}
    for name,l,h in [('two_minima',2,0),('one_maximum',0,1),('two_maxima',0,2),('mixed_pair',1,1)]:
        rows=[family(13,prefix,lo,hi,'cover_original') for lo,hi in placements(13,l,h)]
        original[name]=rows;data[name]=summary(rows,l,h)
    need(data['two_minima']['envelope']==[[3,0,7,7],[5,0,7,7],[9,0,7,7],[17,0,7,7]],
         'P22 literal two-minimum profile differs')
    high=high_anchor(data)
    need([[r['port'],r['label']] for r in high['rows']]==[[11,43],[12,43]],'high saturation differs')
    for gate in combinations(range(13),2):
        labels={}
        for p,label in [(11,43),(12,43)]:
            hit=p in gate;new=gate[1] if hit else p
            labels[new]=max(labels.get(new,-1),label+hit)
        permitted=sum(2**b for b in labels.values())<=2**44
        need(permitted==(not set(gate)&{11,12} or gate==(11,12)),'first maximum event rule differs')
        count('unary_high_next_gate_controls')
    stems,min_count=event_cover('minimum');kernels,max_count=event_cover('maximum')
    need((len(stems),min_count,len(kernels),max_count)==(3,6,45,900),'complete cover counts differ')
    image22=boolean_image(prefix);roots=[];images=[]
    for name,stem in zip(['A','B','C'],stems):
        following=[[11,12]]+stem;gates=prefix+following
        low=ordinary(continue_ordinary(original['two_minima'],following))
        hi=ordinary(continue_ordinary(original['two_maxima'],following))
        need(low['envelope']==[[3,0,9]] and low['mass']==512,'low terminal equality differs')
        need(hi['envelope']==[[0,4096+2**p,6] for p in range(5,11)]+[[0,6144,7]]
             and hi['mass']==512,'new secondary-maximum hypothesis differs')
        image26=apply_image(image22,following)
        for row in image26:
            need(list(row[:2])==sorted(row)[:2] and row[12]==max(row),'P26 extreme property fails')
        middle=target(image26,2,12)
        roots.append({'name':name,'minimum_stem':stem,'prefix26_sha256':digest(gates),
                      'two_minima':low,'two_maxima':hi,'ten_wire_image':middle})
        need(middle['n']==10 and middle['original_wires']==list(range(2,12)),
             'still-live wire11 omitted')
        if name=='B':
            need(stem[:2]==native[22:24],'B does not start P24 after maximum commute')
            need(image26==apply_image(image22,native[22:24]+[[11,12],[1,2]]),'B commutation mismatch')
            continue
        for i,kernel in enumerate(kernels):
            out=apply_image(image26,kernel)
            for row in out:
                need(list(row[:2])==sorted(row)[:2] and list(row[11:])==sorted(row)[11:],
                     'P32 fixed outer pairs fail')
            images.append({'stem':name,'kernel_id':i,'prefix32_sha256':digest(gates+kernel),
                           'nine_wire_image':target(out,2,11)})
    need([r['ten_wire_image']['size'] for r in roots]==[146,141,147],'ten-wire reference sizes differ')
    need(all(list(row)==sorted(row) for row in boolean_image(native)),'known46 full control fails')
    return {'schema':'native22-complete-equality-cover-v1','agent':'six-sorting-2',
            'role':'researcher','parent_files_sha256':PINS,'n':13,'size_budget':44,
            'small_size_lower_bound':35,'prefix_length':22,'prefix22_sha256':digest(prefix),
            'prefix22_families':data,'prefix22_high_anchor':high,'minimum_stems':roots,
            'minimum_event_word_count':min_count,'maximum_event_word_count':max_count,
            'maximum_kernel_count':len(kernels),'maximum_kernels':kernels,
            'closed_native_matching':'B','alternate_root_count':len(images),'alternate_roots':images}


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


def nested(native):
    raw=(ROOT/'p22-fixture.json').read_bytes();selected=json.loads(raw)
    need({k:selected[k] for k in ['n','l','h','free_inputs','size_budget','root_length','alternate_root_count']}
         =={'n':13,'l':3,'h':3,'free_inputs':7,'size_budget':44,'root_length':32,'alternate_root_count':90},
         'selected fixture parameters differ')
    need([(c['stem'],c['kernel_id']) for c in selected['cases']]==[(s,i) for s in ['A','C'] for i in range(45)],
         'selected cover incomplete or duplicated')
    cover_data=json.loads((ROOT/'p22-cover.json').read_text());kernels=cover_data['maximum_kernels']
    # Stage cover independently checks every equality-event word and literal kernel.
    need(len(kernels)==45,'maximum kernel list incomplete')
    covered={(c['stem'],c['kernel_id']):c['prefix32_sha256'] for c in cover_data['alternate_roots']}
    need(set(covered)=={(s,i) for s in ['A','C'] for i in range(45)},'cover/certificate root boundary differs')
    stems={'A':[[1,2],[3,4],[1,3]],'C':[[1,4],[2,3],[1,2]]};cases=[]
    for c in selected['cases']:
        gates=native[:22]+[[11,12]]+stems[c['stem']]+kernels[c['kernel_id']]
        need(digest(gates)==covered[c['stem'],c['kernel_id']],'nested root does not match the proved cover')
        originals=c['original_clampings']
        need(1<=len(originals)<=20 and len({tuple(z) for z in originals})==len(originals),'selected domains invalid')
        rows=[nested_row(gates,lo,hi) for lo,hi in originals]
        tags=[tuple(r['pruning']['outer_record'][2:4]) for r in rows]
        need(len(tags)==len(set(tags)),'selected current classes overlap')
        mass=sum(2**r['nested_label'] for r in rows)
        need(mass>2**44,'selected potential does not exclude this root')
        cases.append({'stem':c['stem'],'kernel_id':c['kernel_id'],'prefix32_sha256':digest(gates),
                      'selected_domains':rows,'selected_classes':len(tags),'selected_mass':mass,
                      'total_lower_bound':ceil_log(mass),
                      'maximum_individual_label':max(r['nested_label'] for r in rows)})
    return {'schema':'native22-selected-nested-certificate-v1','agent':'six-sorting-2',
            'role':'researcher','parent_files_sha256':PINS,'selected_fixture_sha256':hashlib.sha256(raw).hexdigest(),
            'cover_certificate_sha256':hashlib.sha256((ROOT/'p22-cover.json').read_bytes()).hexdigest(),
            'n':13,'l':3,'h':3,'free_inputs':7,'size_budget':44,'root_length':32,
            'alternate_root_count':90,'remaining_roots':[],'cases':cases}


def damages(expected,stage):
    mutations=[]
    for key,value in [('size_budget',45),('n',12),('schema','damaged')]:
        bad=deepcopy(expected);bad[key]=value;mutations.append(bad)
    if stage=='cover':
        bad=deepcopy(expected);bad['maximum_kernels'].pop();mutations.append(bad)
        bad=deepcopy(expected);bad['alternate_roots'].pop();mutations.append(bad)
        bad=deepcopy(expected);bad['minimum_stems'][0]['ten_wire_image']['original_wires'].pop();mutations.append(bad)
        bad=deepcopy(expected);bad['prefix22_families']['two_minima']['envelope'][0][2]+=1;mutations.append(bad)
    else:
        bad=deepcopy(expected);bad['cases'].pop();mutations.append(bad)
        bad=deepcopy(expected);bad['cases'][0]['selected_mass']-=1;mutations.append(bad)
        bad=deepcopy(expected);bad['cases'][0]['selected_domains'][0]['pruning']['outer_record'][4]+=1;mutations.append(bad)
        bad=deepcopy(expected);bad['cases'][0]['selected_domains'][0]['inner_bound']+=1;mutations.append(bad)
        bad=deepcopy(expected);bad['cases'][0]['selected_domains'][0]['pruning']['retained_prefix'][0].reverse();mutations.append(bad)
    for bad in mutations:
        rejected=False
        try:need(bad==expected,'damaged certificate')
        except ValueError:rejected=True
        need(rejected,'damage accepted');count('damaged_certificates_rejected')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['cover','roots']);args=parser.parse_args()
    start=time.monotonic();native=inputs()
    expected=cover(native) if args.stage=='cover' else nested(native)
    path=ROOT/('p22-cover.json' if args.stage=='cover' else 'p22-nested.json')
    need(json.loads(path.read_text())==expected,'certificate differs from scalar reconstruction')
    damages(expected,args.stage)
    print(json.dumps({'status':'NATIVE22_SCALAR_CERTIFICATE_VERIFIED','agent':'six-sorting-2',
                      'role':'researcher','stage':args.stage,
                      'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                      'metrics':METRICS,'seconds':time.monotonic()-start,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))

if __name__=='__main__':main()
