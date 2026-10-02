"""Regenerate the compact complete joint-saturated B23 certificate.
Top-down labeled trees and packed Boolean original domains are the producer.
Carrier pruning is adapted from six-sorting-1 three_touch_prefix_barrier,
source df4e3aa03d6bf96c21e7bdab1330b98db7e0fad2. Inner packed profiles
and dyadic anchors are credited hash-pinned six-sorting-2 sources.
No solver or unrestricted-prefix exclusion is claimed.
"""
from functools import lru_cache
import hashlib
import importlib.util
from itertools import combinations
import json
import os
from pathlib import Path
import resource
import time
ROOT=Path(__file__).resolve().parent
SOURCE=Path(os.environ.get('SORTING_SOURCE_ROOT',ROOT.parents[2]))
PINS={
 'profile.py':'dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719',
 'anchors.py':'0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902'}
FIXTURE_PIN='7dc82cad50dd461d6f19cb24d8b5f0d4f68ee0d62fffa0122bd4e4aa173de60f'

def need(test,message):
    if not test: raise ValueError(message)

@lru_cache(None)
def trees(leaves):
    if len(leaves) == 1:
        return (leaves[0],)
    result = []
    for n in range(1, len(leaves)):
        for rest in combinations(leaves[1:], n-1):
            left = (leaves[0],)+rest
            right = tuple(p for p in leaves if p not in left)
            for a in trees(left):
                for b in trees(right):
                    result.append((a, b))
    return tuple(result)


def depths(tree, depth=0):
    if isinstance(tree, int):
        return {tree: depth}
    return depths(tree[0], depth+1) | depths(tree[1], depth+1)


def word(tree, low):
    if isinstance(tree, int):
        return [], tree
    left, a = word(tree[0], low)
    right, b = word(tree[1], low)
    return left+right+[sorted([a, b])], min(a, b) if low else max(a, b)


def scalar(row, gates):
    values = list(row)
    touches = 0
    for a, b in gates:
        if values[a] < 0 or values[a] > 1 or values[b] < 0 or values[b] > 1:
            touches += 1
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values, touches


def profile(rows, gates, low):
    classes = {}
    for mask, cost in rows:
        values = [0]*13
        ports = [p for p in range(13) if mask >> p & 1]
        need(len(ports) == 2, 'two-marker configuration required')
        for j, p in enumerate(ports):
            values[p] = j-2 if low else j+2
        values, extra = scalar(values, gates)
        out = sum(1 << p for p, v in enumerate(values) if v < 0 or v > 1)
        classes[out] = max(classes.get(out, -1), cost+extra)
    return sorted(classes.items())


def mass(rows):
    return sum(2**d for _, d in rows)


def digest(data):
    return hashlib.sha256(json.dumps(data, separators=(',', ':')).encode()).hexdigest()


def pruning(gates, low, high, semantic):
    free = [i for i in range(13) if not (low | high) >> i & 1]
    columns = iter(semantic.truth_columns(len(free)))
    values = ["L" if low >> i & 1 else "H" if high >> i & 1 else next(columns) for i in range(13)]
    carrier = [free.index(i) if i in free else None for i in range(13)]
    word, d, r, redundant = [], 0, 0, 0
    for t, (a, b) in enumerate(gates):
        x, y = values[a], values[b]
        if isinstance(x, str) or isinstance(y, str):
            rank = lambda z: -1 if z == "L" else 1 if z == "H" else 0
            d += 1
            if rank(x) > rank(y):
                values[a], values[b] = y, x
                carrier[a], carrier[b] = carrier[b], carrier[a]
        else:
            if not x & ~y:
                r += 1
                redundant |= 1 << t
            else:
                word.append([carrier[a], carrier[b]])
            values[a], values[b] = x & y, x | y
    current = semantic.marked_ports(values)
    output = [i for i in range(13) if isinstance(values[i], int)]
    rename = {carrier[i]: j for j, i in enumerate(output)}
    return {"outer_record": [low, high, *current, d, r, redundant],
            "input_free_wires": free, "output_free_wires": output,
            "input_to_output_wire": [rename[i] for i in range(len(free))],
            "retained_prefix": [[rename[a], rename[b]] for a, b in word]}



def boolean_image(gates):
    states=[]
    for x in range(8192):
        values,_=scalar([x>>p&1 for p in range(13)],gates)
        need(values[0]==min(values) and values[12]==max(values),'global held output differs')
        states.append(sum(v<<p for p,v in enumerate(values)))
    return sorted(set(states))


def main():
    start=time.monotonic()
    raw=(ROOT/'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==FIXTURE_PIN,'fixture differs')
    f=json.loads(raw)
    source=SOURCE/'round-two/six-sorting-2/semantic-pruning'
    for name,pin in PINS.items():
        need(hashlib.sha256((source/name).read_bytes()).hexdigest()==pin,'credited source differs')
    spec=importlib.util.spec_from_file_location('joint_selected_anchors',source/'anchors.py')
    anchors=importlib.util.module_from_spec(spec);spec.loader.exec_module(anchors)
    @lru_cache(None)
    def inner(word):
        data=anchors.semantic.analyze(7,[list(g) for g in word])
        bounds=anchors.both(7,data)
        return max(16,*(v['lower_bound'] for v in bounds.values())),data,bounds
    base=f['B23']; full=boolean_image(base)
    need(len(base)==23 and len(full)==179,'literal base differs')
    low=[[1+(1<<p),d] for p,d in f['initial_low']]
    high=[[(1<<p)+(1<<12),d] for p,d in f['initial_high']]
    first=[]
    for gate in combinations(range(1,12),2):
        lm=mass(profile(low,[gate],True));hm=mass(profile(high,[gate],False))
        if max(lm,hm)<=512:first.append([*gate,lm,hm])
    joint=[[a,b] for a,b,lm,hm in first if lm==hm==512]
    need(len(first)==32 and joint==[[3,h] for h in f['joint_partners']],'first-gate map differs')
    ltrees=trees((1,2,3,4));htrees=trees((5,6,7,9,10,11))
    need(len(ltrees)==15 and len(htrees)==945,'unfiltered tree grammar differs')
    roots=[]; replay=[]; root_id=0
    for h in f['joint_partners']:
        lcost={p:7 for p in (1,2,3,4)}
        hcost={p:7 if p in (h,11) else 6 for p in (5,6,7,9,10,11)}
        lt=[t for t in ltrees if max(lcost[p]+d for p,d in depths(t).items())<=9]
        ht=[t for t in htrees if max(hcost[p]+d for p,d in depths(t).items())<=9]
        need((len(lt),len(ht))==(3,9),'joint tree count differs')
        for ltree in lt:
            lw,lp=word(ltree,True)
            for htree in ht:
                hw,hp=word(htree,False)
                suffix=[[3,h]]+lw+hw;gates=base+suffix
                selector=f['root_selectors'][root_id]
                need(selector['root_id']==root_id and digest(gates)==selector['prefix_sha256'],'root selector differs')
                need(lp==1 and hp==11 and len(gates)==32,'terminal route differs')
                need(mass(profile(low,suffix,True))==mass(profile(high,suffix,False))==512,'terminal mass differs')
                image=[]
                for x in full:
                    values,_=scalar([x>>p&1 for p in range(13)],suffix)
                    ordered=sorted(values)
                    need(all(values[p]==ordered[p] for p in (0,1,11,12)),'four frozen outputs differ')
                    image.append(sum(values[p]<<(p-2) for p in range(2,11)))
                image=sorted(set(image)); selected=[]; classes=set(); total=0
                for lo,hi in selector['original_clampings']:
                    need(lo.bit_count()==hi.bit_count()==3 and not lo&hi,'selected domain invalid')
                    pruned=pruning(gates,lo,hi,anchors.semantic);r=pruned['outer_record']
                    key=tuple(r[2:4]);need(key not in classes,'selected marker class repeats');classes.add(key)
                    q=tuple(tuple(g) for g in pruned['retained_prefix'])
                    b,data,ib=inner(q);label=sum(r[4:6])+b
                    selected.append(r+[b]);total+=1<<label
                    replay.append({'root_id':root_id,'original_low':lo,'original_high':hi,
                       'outer_record':r,'retained_prefix':pruned['retained_prefix'],
                       'pruning_sha256':digest(pruned),
                       'inner_records_sha256':{name:digest(v['records']) for name,v in data.items()},
                       'inner_anchor_bounds':{side:v['lower_bound'] for side,v in ib.items()},
                       'inner_bound':b,'nested_label':label})
                need(total>1<<44,'selected strict negative inequality failed')
                roots.append({'root_id':root_id,'joint_gate':[3,h],'suffix_after_B23':suffix,
                    'core_image_size':len(image),'core_image_sha256':digest(image),
                    'selected_records':selected,'selected_mass':total})
                root_id+=1
    need(root_id==135 and len(replay)==488,'complete joint cover differs')
    packet={'schema':'b23-joint-saturation-certificate-v1','agent':'six-sorting-1','role':'researcher',
       'fixture_sha256':FIXTURE_PIN,'base_image_size':len(full),'base_image_sha256':digest(full),
       'first_necessary_gate_map':first,'root_records':roots,
       'selected_domain_occurrences':len(replay),'distinct_inner_words':inner.cache_info().currsize,
       'replay_records_sha256':digest(replay),'total44_mass_ceiling':1<<44,
       'minimum_selected_mass':min(r['selected_mass'] for r in roots),
       'literal_joint_prefixes_excluded':135,'simultaneous_first_slack_branches_excluded':5}
    target=ROOT/'certificate.json';target.write_text(json.dumps(packet,separators=(',',':'))+'\n')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher','status':'JOINT_SATURATION_CERTIFICATE_REGENERATED',
      'certificate_bytes':target.stat().st_size,'certificate_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
      'roots':135,'selected_domains':len(replay),'distinct_inner_words':inner.cache_info().currsize,
      'minimum_selected_mass':packet['minimum_selected_mass'],'replay_records_sha256':digest(replay),
      'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':main()
