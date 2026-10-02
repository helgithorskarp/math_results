"""Standalone numeric-cube and bottom-up forest checker.

Imports no producer/profiler/sibling module or solver. Same author, different
algorithms; universal bridges remain unformalized. See SOURCE-CREDITS.md.
"""
from collections import Counter,deque
from functools import lru_cache
from copy import deepcopy
import hashlib,heapq,json,resource,time
from itertools import combinations,product
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FAMILIES=(("one_minimum",1,0),("one_maximum",0,1),("two_minima",2,0),("two_maxima",0,2),("mixed_pair",1,1))
SIZES=(0,0,1,3,5,9,12,16,19,25,29,35,39)
METRICS={}
N19=[[0,11],[1,7],[2,4],[3,5],[8,9],[10,12],[0,2],[3,6],[4,12],[5,7],[8,10],[0,8],[1,3],[2,5],[4,9],[6,11],[7,12],[0,1],[2,10]]
EXPECTED_LOW=((1,7),(2,7),(3,5),(4,6),(6,5),(8,6))
EXPECTED_HIGH=((3,5),(5,6),(6,5),(7,6),(9,6),(10,6),(11,7))

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
def inner(word):
    data=profiles(7,word,'selected_inner')
    anchors=anchor_bounds(7,data)
    return {'inner_records_sha256':{name:item['records_sha256'] for name,item in data.items()},
            'inner_anchor_leaves':{side:[[r['port'],r['label']] for r in a['rows']] for side,a in anchors.items()},
            'inner_anchor_bounds':{side:a['lower_bound'] for side,a in anchors.items()},
            'inner_bound':max(16,*(a['lower_bound'] for a in anchors.values()))}


def require_rejection(test,name):
    try:test()
    except (ValueError,KeyError,IndexError,TypeError):return name
    raise ValueError('damaged control accepted: '+name)


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

def fixture_check(f):
    need(f['schema']=='native-both-first-binary-v1' and f['agent']=='six-sorting-2' and
         f['role']=='researcher' and f['n']==13 and f['size_budget']==44,'wrong fixture scope')
    need(f['prefix19']==N19 and f['maximum_word']==[[9,11],[11,12]] and
         f['joint_zero_gate']==[3,6],'wrong literal H21')
    need(f['imported_size_bounds']=={'5':9,'6':12,'7':16,'11':35},'wrong imported size premise')
    pool=f['proposal_original_clampings']
    need(len(pool)==97 and pool==[list(p) for p in sorted(set(map(tuple,pool)))],'proposal pool differs')
    need(all(lo.bit_count()==hi.bit_count()==3 and not lo&hi and 0<=lo<(1<<13)
             and 0<=hi<(1<<13) for lo,hi in pool),'invalid proposal domain')

@lru_cache(None)
def baseline(prefix):
    low,high=ordinary_initial(prefix,False),ordinary_initial(prefix,True)
    need((low,high)==(EXPECTED_LOW,EXPECTED_HIGH),'original H21 classes differ')
    images=set()
    for x in range(8192):
        row=simulate([x>>j&1 for j in range(13)],prefix);images.add(tuple(row))
        need(row[0]==min(row) and row[12]==max(row),'H21 held extremes differ')
        count('H21_original_Boolean_assignments')
    need(len(images)==246 and len({r[1:12] for r in images})==244,'H21 exact image differs')
    return low,high,frozenset(images)

@lru_cache(None)
def first_binary_profile_audit(initial):
    """All necessary profile transitions, allowing unlimited identity preparations.

    This finite projection checks invariants, not preparation-function coverage.
    The universal disjoint-commutation bridge is proved in PROOF.md.
    """
    start=(*initial,False);queue=deque([start]);seen={start};terminals=0;edges=0
    gates=list(combinations(range(1,12),2))
    first_pairs=set()
    while queue:
        low,high,jdone=state=queue.popleft();old=(mass(low),mass(high))
        supports=[{q for q,_ in low},{q for q,_ in high}]
        need(all(m in [448,512] for m in old),'binary-first path reaches intermediate mass')
        if len(low)==len(high)==1:
            need(jdone and old==(512,512) and low==((1,9),) and high==((11,9),),
                 'terminal binary profile differs');terminals+=1
        for gate in gates:
            new=(passage(low,gate,False),passage(high,gate,True))
            weights=tuple(map(mass,new));hits=[len(set(gate)&u) for u in supports]
            count('binary_first_profile_next_gates')
            need(all(weights[k]>=old[k] for k in [0,1]),'profile mass decreased')
            if max(weights)>512:continue
            if any(old[k]==448 and weights[k]>448 and hits[k]!=2 for k in [0,1]):continue
            joint=not jdone and gate==(3,6)
            if not jdone and not joint:
                need(not set(gate)&{3,6},'a pre-J gate meets a future J endpoint')
            if jdone:
                need(not supports[0]&supports[1],'post-J supports overlap')
                need(hits in ([0,0],[2,0],[0,2]),'post-J event is singleton or crosses supports')
                need(all({q for q,_ in new[k]}<=supports[k] for k in [0,1]),
                     'binary event resurrects a released port')
            if old==(448,448) and weights!=old:first_pairs.add(weights)
            child=(*new,jdone or joint)
            if child==state:
                need(hits==[0,0],'identity preparation touches a live candidate');continue
            edges+=1
            if child not in seen:seen.add(child);queue.append(child)
    need(first_pairs=={(448,512),(512,448)},'first-global-binary mass pairs differ')
    need(terminals==1,'complete binary profile projection has wrong terminals')
    return {'binary_first_profile_states':len(seen),'binary_first_profile_edges':edges,
            'binary_first_profile_terminal_states':terminals,
            'binary_first_global_mass_pairs':[list(p) for p in sorted(first_pairs)]}

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

def selected_check(gates,e):
    need(e['prefix_sha256']==digest(gates),'selected literal prefix binding differs')
    tags=set();rows=[];m=0
    need(bool(e['domains']),'empty selected original family')
    for domain in e['domains']:
        need(len(domain)==3,'invalid selector tuple')
        lo,hi,b=domain
        need(lo.bit_count()==hi.bit_count()==3 and not lo&hi and 0<=lo<(1<<13)
             and 0<=hi<(1<<13),'selected original clamping is not3+3')
        r=family(13,gates,lo,hi,'selected_outer');tag=tuple(r[2:4])
        need(tag not in tags,'current class double counted');tags.add(tag)
        if b==16:count('constant_selected_domains')
        else:
            need(isinstance(b,int) and b>16,'invalid nested lower bound')
            pruned=pruning(13,gates,r)
            actual=inner(tuple(map(tuple,pruned['retained_prefix'])))['inner_bound']
            need(b==actual,'selected exact nested bound differs');count('nested_selected_domains')
        rows.append([*r,b]);m+=1<<(r[4]+r[5]+b)
    need(m>1<<44,'selected mass does not strictly exceed size44 ceiling')
    expected={'root_id':e['root_id'],'prefix_sha256':digest(gates),'selected_mass':m,
        'total_lower_bound':ceil_log(m),'domains':e['domains'],'selected_records_sha256':digest(rows)}
    need(e==expected,'derived original records or exclusion metadata differs')
    return m

def cover_check(data,f):
    fixture_check(f)
    need(data['schema']=='native-both-first-binary-certificate-v1' and data['agent']=='six-sorting-2'
         and data['role']=='researcher' and data['n']==13 and data['size_budget']==44,'certificate scope differs')
    need(data['fixture_sha256']==hashlib.sha256((ROOT/'fixture.json').read_bytes()).hexdigest(),
         'fixture byte binding differs')
    prefix=f['prefix19']+f['maximum_word'];lo,hi,images=baseline(tuple(map(tuple,prefix)))
    control=first_binary_profile_audit((lo,hi))
    lo,hi=passage(lo,[3,6],False),passage(hi,[3,6],True)
    low_support,high_support=sorted(q for q,_ in lo),sorted(q for q,_ in hi)
    need(not set(low_support)&set(high_support),'J did not separate supports')
    need(mass(lo)==mass(hi)==448,'J did not preserve both448 masses')
    low_functions,high_functions=forest_cover(lo,False),forest_cover(hi,True)
    need((len(low_functions),len(high_functions))==(9,45),'complete native9x45 genealogy cover differs')
    lw,hw=data['low_words'],data['high_words']
    need(len(lw)==9 and len(hw)==45,'declared family inventory differs')
    need(all(len(w)==4 and all(a<b and a in low_support and b in low_support for a,b in w) for w in lw),
         'LOW word does not use four standard gates on native support')
    need(all(len(w)==5 and all(a<b and a in high_support and b in high_support for a,b in w) for w in hw),
         'HIGH word does not use five standard gates on native support')
    lf=[full_family_function(w,low_support) for w in lw]
    hf=[full_family_function(w,high_support) for w in hw]
    need(len(set(lf))==9 and set(lf)==low_functions and len(set(hf))==45 and set(hf)==high_functions,
         'declared canonical functions do not equal full bottom-up forest cover')
    prior_low=[[[4,8]]+w for w in [ [[1,3],[2,4],[1,2]], [[2,3],[1,4],[1,2]], [[3,4],[1,2],[1,3]] ]]
    prior_functions={full_family_function(w,low_support) for w in prior_low}
    need(len(prior_functions)==3 and prior_functions<=low_functions,'credited B23 three-LOW cover is not included')
    inherited=[i for i,v in enumerate(lf) if v in prior_functions]
    roots=data['roots'];exclusions=data['exclusions']
    need(len(roots)==len(exclusions)==405 and [r['id'] for r in roots]==[e['root_id'] for e in exclusions]==list(range(405)),
         'incomplete root/exclusion coverage')
    all_images=set();sizes=Counter();covered=set()
    for i,j in product(range(9),range(45)):
        rid=45*i+j;r=roots[rid];word=[[3,6]]+lw[i]+hw[j]
        target=set()
        for before in images:
            after=simulate(before,word);ranks=sorted(before)
            need(all(after[q]==ranks[q] for q in [0,1,11,12]),'front does not hold four extreme ranks')
            target.add(sum(after[q]<<(q-2) for q in range(2,11)))
            count('exact_H21_image_front_assignments');count('exact_front_gate_evaluations',10)
        image=tuple(sorted(target));all_images.add(image);sizes[len(image)]+=1;covered.add((lf[i],hf[j]))
        expected={'id':rid,'low_genealogy':i,'high_genealogy':j,'word':word,'prefix_length':31,
            'remaining_budget':13,'image_size':len(image),'image_sha256':digest(image)}
        need(r==expected,'literal front/image/remaining-budget metadata differs')
    need(len(all_images)==403,'exact image quotient is not403 (405 roots remain separately certified)')
    need(covered==set(product(low_functions,high_functions)),'binary family product cover is incomplete')
    need(set(data)=={'schema','agent','role','n','size_budget','fixture_sha256','low_words','high_words','roots','exclusions'},
         'unvalidated certificate field')
    return {'fronts':405,'distinct_images':len(all_images),'image_sizes':dict(sorted(sizes.items())),
        'prior_B23_low_genealogies':inherited,'credited_prior_function_fronts':135,**control}

def damages(data,f):
    rejected=[]
    changes=[('missing root',lambda x:x['roots'].pop()),
             ('duplicate family word',lambda x:x['low_words'].__setitem__(1,x['low_words'][0])),
             ('wrong image size',lambda x:x['roots'][0].__setitem__('image_size',0)),
             ('wrong remaining budget',lambda x:x['roots'][0].__setitem__('remaining_budget',12)),
             ('wrong size budget',lambda x:x.__setitem__('size_budget',45))]
    for name,mutate in changes:
        changed=deepcopy(data);mutate(changed)
        rejected.append(require_rejection(lambda:cover_check(changed,f),name))
    gates=f['prefix19']+f['maximum_word']+data['roots'][0]['word']
    for name,mutate in [('invalid original domain',lambda e:e['domains'][0].__setitem__(0,0)),
                         ('wrong selected mass',lambda e:e.__setitem__('selected_mass',1<<44)),
                         ('insufficient strict mass',lambda e:e.__setitem__('domains',e['domains'][:1])),
                         ('duplicate current class',lambda e:e['domains'].append(e['domains'][0])),
                         ('wrong derived records',lambda e:e.__setitem__('selected_records_sha256','0'*64)),
                         ('wrong prefix binding',lambda e:e.__setitem__('prefix_sha256','0'*64))]:
        e=deepcopy(data['exclusions'][0]);mutate(e)
        rejected.append(require_rejection(lambda:selected_check(gates,e),name))
    idx=next(i for i,e in enumerate(data['exclusions']) if any(d[2]>16 for d in e['domains']))
    e=deepcopy(data['exclusions'][idx]);d=next(d for d in e['domains'] if d[2]>16);d[2]+=1
    gates=f['prefix19']+f['maximum_word']+data['roots'][idx]['word']
    rejected.append(require_rejection(lambda:selected_check(gates,e),'wrong exact inner bound'))
    for name,field,value in [('wrong H21','maximum_word',[[9,12],[11,12]]),
                              ('wrong imported sizes','imported_size_bounds',{'5':9,'6':12,'7':16,'11':34})]:
        changed=deepcopy(f);changed[field]=value
        rejected.append(require_rejection(lambda:fixture_check(changed),name))
    return rejected

def main():
    start=time.monotonic();f=json.loads((ROOT/'fixture.json').read_text())
    data=json.loads((ROOT/'certificate.json').read_text());summary=cover_check(data,f)
    masses=[selected_check(f['prefix19']+f['maximum_word']+r['word'],e)
            for r,e in zip(data['roots'],data['exclusions'])]
    selected_words=inner.cache_info().currsize
    positive_controls(f);before=dict(METRICS);rejected=damages(data,f)
    print(json.dumps({'status':'COMPLETE405_NATIVE_BINARY_FOREST_AND_ORIGINAL_CUBE_CERTIFICATES_VERIFIED',
        'agent':'six-sorting-2','role':'researcher',**summary,
        'selected_domains':sum(len(e['domains']) for e in data['exclusions']),
        'minimum_selected_mass':min(masses),'distinct_selected_inner_words':selected_words,
        'certificate_sha256':hashlib.sha256((ROOT/'certificate.json').read_bytes()).hexdigest(),
        'damaged_controls_rejected':rejected,'metrics_before_damages':before,
        'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'boundary':'Same-author distinct algorithms. Universal pruning/commutation bridges and imported sizes remain unformalized; no external review.'},sort_keys=True),flush=True)
if __name__=='__main__':main()
