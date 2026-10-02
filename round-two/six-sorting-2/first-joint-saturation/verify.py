"""Standalone numeric and bottom-up forest checker for405 native fronts.

Imports no producer, profiler, sibling mathematics, solver or graph package.
Copied numeric primitives are credited in SOURCE-CREDITS.md. Universal
pruning/commutation bridges and imported sizes remain author proof premises.
"""
from collections import Counter,deque
from functools import lru_cache
from copy import deepcopy
import hashlib
import heapq
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent
FAMILIES = (("one_minimum", 1, 0), ("one_maximum", 0, 1),
            ("two_minima", 2, 0), ("two_maxima", 0, 2), ("mixed_pair", 1, 1))
SIZES = (0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39)
METRICS = {}


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


N19=[[0,11],[1,7],[2,4],[3,5],[8,9],[10,12],[0,2],[3,6],
     [4,12],[5,7],[8,10],[0,8],[1,3],[2,5],[4,9],[6,11],[7,12],
     [0,1],[2,10]]
EXPECTED_LOW=((1,7),(2,7),(3,5),(4,6),(6,5),(8,6))
EXPECTED_HIGH=((3,5),(5,6),(6,5),(7,6),(9,6),(10,6),(11,7))

def fixture_check(f):
    need(f['n']==13 and f['size_budget']==44,'wrong scope')
    need(f['prefix19']==N19 and f['maximum_word']==[[9,11],[11,12]] and
         f['joint_zero_gate']==[3,6],'wrong literal native prefix')
    need(f['imported_size_bounds']=={'5':9,'6':12,'7':16,'11':35},'wrong imported size bounds')
    for lo,hi in f['proposal_original_clampings']:
        need(lo.bit_count()==hi.bit_count()==3 and not lo&hi and lo|hi<8192,
             'invalid proposal domain')
    for gate in f['prefix19']+f['maximum_word']+f['native46_control']:
        need(len(gate)==2 and 0<=gate[0]<gate[1]<13,'invalid standard gate')

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

def zero_profile_audit(initial):
    queue=deque([initial]);seen={initial};edges={};pairs=Counter()
    gates=list(combinations(range(1,12),2))
    max_dead=0;both=0
    while queue:
        state=queue.popleft();out=[]
        live={q for f in state for q,_ in f}
        max_dead=max(max_dead,11-len(live))
        for gate in gates:
            new=(passage(state[0],gate,False),passage(state[1],gate,True))
            weights=tuple(map(mass,new));count('joint_next_gate_controls')
            need(all(w>=448 for w in weights),'ordinary mass decreased')
            if weights==(448,448) and new!=state:
                need(all({q for q,_ in new[k]}<={q for q,_ in state[k]} for k in [0,1]),
                     'zero event resurrected a secondary port')
                out.append(new)
                if new not in seen:seen.add(new);queue.append(new)
            elif weights==(448,448):
                need(not set(gate)&live,'zero preparation meets live support')
            elif max(weights)<=512:
                pairs[weights]+=1
                if weights==(512,512):
                    both+=1
                    need(set(gate)<=live,'simultaneous saturation needs a prepared operand')
                    need(all(len(set(gate)&{q for q,_ in f})==1 for f in state),
                         'simultaneous saturation is not singleton on each side')
                    need(all(next(d for q,d in f if q in gate)==6 for f in state),
                         'simultaneous saturation uses a cost other than6')
                    if {q for q,_ in state[0]}&{q for q,_ in state[1]}:
                        need(not set(gate)&{3,6},'pre-joint saturation intersects joint gate')
        edges[state]=out
    @lru_cache(None)
    def lengths(state):
        answer=Counter({0:1})
        for child in edges[state]:
            for n,v in lengths(child).items():answer[n+1]+=v
        return answer
    polynomial=lengths(initial)
    need(set(pairs)=={(448,512),(480,480),(512,448),(512,512)},'first-strict mass support differs')
    need(len(seen)==828 and max_dead==5,'zero profile closure differs')
    need([polynomial[i] for i in range(7)]==[1,9,62,414,2436,11200,31680] and
         sum(polynomial.values())==45802,'complete zero-word polynomial differs')
    return {'zero_profiles':len(seen),'zero_words':sum(polynomial.values()),
            'zero_word_polynomial':[polynomial[i] for i in range(7)],
            'simultaneous_strict_profile_edges':both,'first_mass_pairs':[[*p,n] for p,n in sorted(pairs.items())]}

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
            need(forest[0][1]==9,'terminal forest has wrong dyadic cost')
            terminal.add(forest[0][2]);continue
        for i,j in combinations(range(len(forest)),2):
            p,d,t=forest[i];q,e,u=forest[j]
            count('binary_forest_pair_controls')
            if d!=e:continue
            children=sorted([t,u])
            node=(max(p,q) if high else min(p,q),d+1,('N',*children))
            child=tuple(sorted([v for k,v in enumerate(forest) if k not in (i,j)]+[node]))
            if child not in seen:seen.add(child);todo.append(child)
    support=sorted(p for p,_ in profile)
    functions={full_family_function(tree_word(t,high)[0],support) for t in terminal}
    count('binary_forest_states',len(seen));count('binary_terminal_forests',len(terminal))
    need(len(functions)==len(terminal),'terminal genealogies share a full function')
    return functions

@lru_cache(None)
def inner(word):
    data=profiles(7,word,'selected_inner')
    anchors=anchor_bounds(7,data)
    return {'inner_records_sha256':{name:item['records_sha256'] for name,item in data.items()},
            'inner_anchor_leaves':{side:[[r['port'],r['label']] for r in a['rows']] for side,a in anchors.items()},
            'inner_anchor_bounds':{side:a['lower_bound'] for side,a in anchors.items()},
            'inner_bound':max(16,*(a['lower_bound'] for a in anchors.values()))}

def selected_check(gates,entry):
    classes=set();mass_value=0
    for row in entry['selected_domains']:
        lo,hi=row['original']
        need(lo.bit_count()==hi.bit_count()==3 and not lo&hi,'invalid selected original3+3 domain')
        record=family(13,gates,lo,hi,'selected_outer')
        need(row['outer_record']==record and row['current']==record[2:4],
             'selected original conditional record differs')
        tag=tuple(record[2:4])
        need(tag not in classes,'duplicate current class double counted');classes.add(tag)
        base={'original':[lo,hi],'current':record[2:4],'outer_record':record,
              'constant_only':row['constant_only']}
        if row['constant_only']:
            expected=base|{'inner_bound':16,'nested_label':record[4]+record[5]+16}
        else:
            pruned=pruning(13,gates,record)
            w=inner(tuple(map(tuple,pruned['retained_prefix'])))
            expected=base|{'pruning':pruned,**w,
                           'nested_label':record[4]+record[5]+w['inner_bound']}
        need(row==expected,'nested witness or exact inner function data differs')
        mass_value+=1<<expected['nested_label']
    need(mass_value>1<<44,'selected nested mass does not exclude size44')
    need(entry=={'root_id':entry['root_id'],'prefix_sha256':digest(gates),
                 'selected_mass':mass_value,'total_lower_bound':ceil_log(mass_value),
                 'selected_domains':entry['selected_domains']},'exclusion summary differs')
    return mass_value

@lru_cache(None)
def baseline(prefix):
    low,high=ordinary_initial(prefix,False),ordinary_initial(prefix,True)
    need((low,high)==(EXPECTED_LOW,EXPECTED_HIGH),'original H21 ordinary profile differs')
    audit=zero_profile_audit((low,high))
    outputs=set()
    for x in range(8192):
        row=simulate([x>>j&1 for j in range(13)],prefix)
        outputs.add(tuple(row));count('H21_original_Boolean_assignments')
    need(len(outputs)==246,'complete H21 image differs')
    need(len({r[1:12] for r in outputs})==244,'H21 core image differs')
    return low,high,audit,frozenset(outputs)

def verify(data,f):
    fixture_check(f)
    need(data['schema']=='native-first-joint-saturation-certificate-v1' and
         data['agent']=='six-sorting-2' and data['role']=='researcher' and
         data['n']==13 and data['size_budget']==44,'certificate scope differs')
    need(data['fixture_sha256']==hashlib.sha256((ROOT/'fixture.json').read_bytes()).hexdigest(),
         'fixture byte binding differs')
    prefix=f['prefix19']+f['maximum_word']
    low,high,audit,original_outputs=baseline(tuple(map(tuple,prefix)))
    low,high=passage(low,[3,6],False),passage(high,[3,6],True)
    need(not {q for q,_ in low}&{q for q,_ in high},'joint event did not separate supports')
    crosses=sorted(sorted([a,b]) for a,d in low if d==6 for b,e in high if e==6)
    need(data['cross_gates']==crosses and len(crosses)==15,'complete cross gate cover differs')
    roots=data['roots'];exclusions=data['exclusions']
    need(len(roots)==len(exclusions)==405,'incomplete405 front cover')
    need([r['id'] for r in roots]==[e['root_id'] for e in exclusions]==list(range(405)),
         'root IDs do not cover every canonical front')
    all_images=set();masses=[];sizes=Counter()
    for cross_index,cross in enumerate(crosses):
        lp,hp=passage(low,cross,False),passage(high,cross,True)
        need(mass(lp)==mass(hp)==512,'cross does not saturate both families')
        need(not {q for q,_ in lp}&{q for q,_ in hp},'saturated supports overlap')
        low_functions,high_functions=forest_cover(lp,False),forest_cover(hp,True)
        need((len(low_functions),len(high_functions))==(3,9),'complete forest counts differ')
        group=roots[27*cross_index:27*(cross_index+1)]
        low_words=sorted({tuple(map(tuple,r['word'][2:6])) for r in group})
        high_words=sorted({tuple(map(tuple,r['word'][6:])) for r in group})
        need(len(low_words)==3 and len(high_words)==9,'declared family words incomplete')
        lf={w:full_family_function(w,sorted(q for q,_ in lp)) for w in low_words}
        hf={w:full_family_function(w,sorted(q for q,_ in hp)) for w in high_words}
        need(set(lf.values())==low_functions and set(hf.values())==high_functions,
             'pair-partition words fail complete forest function coverage')
        covered=set()
        for local_index,r in enumerate(group):
            i,j=divmod(local_index,9)
            expected_word=[[3,6],cross]+[list(g) for g in low_words[i]+high_words[j]]
            need(r['word']==expected_word and r['cross']==cross and
                 r['low_genealogy']==i and r['high_genealogy']==j,
                 'canonical word metadata differs')
            covered.add((lf[low_words[i]],hf[high_words[j]]))
            target=set()
            for before in original_outputs:
                after=simulate(before,r['word']);rank=sorted(before)
                need(all(after[q]==rank[q] for q in [0,1,11,12]),'front does not hold four ranks')
                target.add(sum(after[q]<<(q-2) for q in range(2,11)))
                count('exact_H21_image_front_assignments');count('exact_front_gate_evaluations',11)
            image=tuple(sorted(target));all_images.add(image);sizes[len(image)]+=1
            expected={'id':27*cross_index+local_index,'cross':cross,'low_genealogy':i,
                      'high_genealogy':j,'word':expected_word,'prefix_length':32,
                      'remaining_budget':12,'image_sha256':digest(image),'image_size':len(image)}
            need(r==expected,'exact nine-core image or budget differs')
            masses.append(selected_check(prefix+r['word'],exclusions[r['id']]))
        need(covered=={(a,b) for a in low_functions for b in high_functions},
             'conditional binary product cover incomplete')
    need(len(all_images)==405,'nine-core images are not405 distinct targets')
    need(set(data)=={'schema','agent','role','n','size_budget','fixture_sha256',
                     'cross_gates','roots','exclusions'},'unvalidated certificate fields')
    return {'fronts':405,'selected_domains':sum(len(e['selected_domains']) for e in exclusions),
            'minimum_selected_mass':min(masses),'distinct_inner_words':inner.cache_info().currsize,
            'image_sizes':dict(sorted(sizes.items())),**audit}

def require_rejection(test,name):
    try:test()
    except (ValueError,KeyError,IndexError,TypeError):return name
    raise ValueError('damaged control accepted: '+name)

def damages(data,f):
    rejected=[]
    for name,mutate in [
        ('root omitted',lambda d:d['roots'].pop()),
        ('cross omitted',lambda d:d['cross_gates'].pop()),
        ('wrong free budget',lambda d:d['roots'][0].__setitem__('remaining_budget',13)),
        ('false complete image',lambda d:d['roots'][0].__setitem__('image_size',1)),
        ('wrong canonical gate',lambda d:d['roots'][0]['word'].__setitem__(2,[1,4])),
    ]:
        d=deepcopy(data);mutate(d)
        # Cheap rejection of finite cover metadata is still semantic validation.
        rejected.append(require_rejection(lambda:verify(d,f),name))
    entry=data['exclusions'][0];gates=f['prefix19']+f['maximum_word']+data['roots'][0]['word']
    for name,mutate in [
        ('outer deletion count',lambda e:e['selected_domains'][0]['outer_record'].__setitem__(4,0)),
        ('original domain',lambda e:e['selected_domains'][0]['original'].__setitem__(0,e['selected_domains'][0]['original'][0]^1)),
        ('false strict mass',lambda e:e.__setitem__('selected_mass',1<<44)),
        ('duplicate class with repaired mass',None),
    ]:
        e=deepcopy(entry)
        if mutate is None:
            e['selected_domains'].append(deepcopy(e['selected_domains'][0]))
            e['selected_mass']+=1<<e['selected_domains'][0]['nested_label']
            e['total_lower_bound']=ceil_log(e['selected_mass'])
        else:mutate(e)
        rejected.append(require_rejection(lambda:selected_check(gates,e),name))
    nested=next((e,d) for e in data['exclusions'] for d in e['selected_domains'] if not d['constant_only'])
    for name,field in [('pruned orientation','pruning'),('false inner lower bound','inner_bound')]:
        e=deepcopy(nested[0]);row=next(d for d in e['selected_domains'] if not d['constant_only'])
        if field=='pruning':row['pruning']['retained_prefix'][0].reverse()
        else:row['inner_bound']+=1
        gates=f['prefix19']+f['maximum_word']+data['roots'][e['root_id']]['word']
        rejected.append(require_rejection(lambda:selected_check(gates,e),name))
    for name,field,value in [('wrong prefix','prefix19',[[0,10]]+N19[1:]),
                             ('wrong size bound','imported_size_bounds',{'5':9,'6':12,'7':16,'11':34})]:
        changed=deepcopy(f);changed[field]=value
        rejected.append(require_rejection(lambda:fixture_check(changed),name))
    return rejected

def positive_controls(f):
    for n,field,size in [(7,'control7',16),(11,'control11',35),(13,'native46_control',46)]:
        gates=f[field];need(len(gates)==size,'positive sorter size differs')
        for x in range(1<<n):
            row=[x>>j&1 for j in range(n)]
            need(simulate(row,gates)==sorted(row),'positive full sorter fails')
            count('positive_sorter_assignments')
    for cut in range(17):
        need(bound(7,f['control7'][:cut])<=16,'valid7 sorter prefix falsely excluded')
    need(bound(7,f['control7'])==16,'full7 sorter anchor differs')
    for low,high in [(7,328),(7168,224)]:
        gates=f['native46_control'];record=family(13,gates,low,high,'positive_outer')
        pruned=pruning(13,gates,record);word=tuple(map(tuple,pruned['retained_prefix']))
        for x in range(128):
            row=[x>>j&1 for j in range(7)]
            need(simulate(row,word)==sorted(row),'guaranteed pruned sorter fails')
        need(inner(word)['inner_bound']<=46-record[4]-record[5],
             'inner operator falsely excludes guaranteed pruned sorter')

def main():
    started=time.monotonic()
    f=json.loads((ROOT/'fixture.json').read_text())
    data=json.loads((ROOT/'certificate.json').read_text())
    summary=verify(data,f)
    positive_controls(f)
    before=dict(METRICS)
    rejected=damages(data,f)
    result={'status':'COMPLETE405_FOREST_NUMERIC_AND_NESTED_CERTIFICATE_VERIFIED',
            'agent':'six-sorting-2','role':'researcher',**summary,
            'certificate_sha256':hashlib.sha256((ROOT/'certificate.json').read_bytes()).hexdigest(),
            'damaged_controls_rejected':rejected,'metrics_before_damages':before,
            'seconds':time.monotonic()-started,
            'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'boundary':'Same-author distinct scalar/forest algorithms. Commutation, pruning transport and imported exact size bounds are unformalized author premises, not external review.'}
    print(json.dumps(result,sort_keys=True),flush=True)

if __name__=='__main__':main()
