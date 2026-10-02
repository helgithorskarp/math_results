"""Packed exact producer for native H21 BOTH-FIRST-BINARY exclusion.

Explicit one-unequal-node genealogies and selected original input cubes.
Copied primitives are credited in SOURCE-CREDITS.md; no depth bound or solver.
"""
import hashlib,json,resource,time
from collections import Counter
from functools import lru_cache
from itertools import combinations,product
from pathlib import Path
import anchors
s=anchors.semantic
ROOT=Path(__file__).resolve().parent

def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def pairings(xs):
    if not xs:
        yield []
    else:
        for j in range(1, len(xs)):
            for tail in pairings(xs[1:j]+xs[j+1:]):
                yield [(xs[0], xs[j])]+tail


def profile_step(state, gate, high):
    result = {}
    for port, cost in state:
        target = gate[1] if high else gate[0]
        if port not in gate:
            target = port
        result[target] = max(result.get(target, -1), cost+(port in gate))
    return sorted(result.items())


def record_for(gates,low,high):
    free=[q for q in range(13) if not (low|high)>>q&1]
    columns=iter(s.truth_columns(len(free)))
    values=[s.LOW if low>>q&1 else s.HIGH if high>>q&1 else next(columns) for q in range(13)]
    d=r=mask=0
    for t,(a,b) in enumerate(gates):
        hit,inactive=s.transition(values,a,b)
        d+=hit;r+=inactive
        if inactive:mask|=1<<t
    return [low,high,*s.marked_ports(values),d,r,mask]


def prune(gates, record):
    """Remove marked touches and inactive free gates, tracking free carriers."""
    low, high = record[:2]
    free = [p for p in range(13) if not ((low | high) >> p) & 1]
    columns = s.truth_columns(len(free))
    values = [s.LOW if (low >> p) & 1 else
              s.HIGH if (high >> p) & 1 else columns[free.index(p)]
              for p in range(13)]
    carriers = [None if ((low | high) >> p) & 1 else free.index(p)
                for p in range(13)]
    retained, d, r, redundant_mask, touched_mask = [], 0, 0, 0, 0
    for t, (a, b) in enumerate(gates):
        if isinstance(values[a], str) or isinstance(values[b], str):
            d += 1
            touched_mask |= 1 << t
            order = lambda z: -1 if z == s.LOW else 1 if z == s.HIGH else 0
            if order(values[a]) > order(values[b]):
                values[a], values[b] = values[b], values[a]
                carriers[a], carriers[b] = carriers[b], carriers[a]
        else:
            if values[a] & ~values[b]:
                retained.append([carriers[a], carriers[b]])
            else:
                r += 1
                redundant_mask |= 1 << t
            values[a], values[b] = values[a] & values[b], values[a] | values[b]
    lp, hp = s.marked_ports(values)
    if [low, high, lp, hp, d, r, redundant_mask] != record:
        raise ValueError("pruning record does not match the complete conditional domain")
    output_free = [p for p in range(13) if carriers[p] is not None]
    rename = {carriers[p]: j for j, p in enumerate(output_free)}
    return {"outer_record": record, "marked_touch_mask": touched_mask,
            "input_free_wires": free, "output_free_wires": output_free,
            "input_to_output_wire": [rename[j] for j in range(len(free))],
            "retained_prefix": [[rename[a], rename[b]] for a, b in retained]}


@lru_cache(None)
def inner(word):
    data=s.analyze(7,word)
    ab=anchors.both(7,data)
    return {'inner_records_sha256':{k:digest(v['records']) for k,v in data.items()},
            'inner_anchor_leaves':{k:[[r['port'],r['label']] for r in a['rows']] for k,a in ab.items()},
            'inner_anchor_bounds':{k:a['lower_bound'] for k,a in ab.items()},
            'inner_bound':max(16,*(a['lower_bound'] for a in ab.values()))}


def leaf(p):return ('L',p)


def node(a,b):return ('N',*sorted([a,b]))


def tree_word(t,high):
    if t[0]=='L':return [],t[1]
    lw,a=tree_word(t[1],high);rw,b=tree_word(t[2],high)
    return lw+rw+[[min(a,b),max(a,b)]],max(a,b) if high else min(a,b)


def trees(small,large):
    answer=[]
    if len(large)==2:
        for u,b in product(small,large):
            other=sorted(set(small)-{u});other_big=next(q for q in large if q!=b)
            unequal=node(leaf(u),leaf(b))
            equal=node(node(*map(leaf,other)),leaf(other_big))
            answer.append(node(unequal,equal))
        for u in small:
            other=sorted(set(small)-{u})
            answer.append(node(node(leaf(u),node(*map(leaf,other))),node(*map(leaf,large))))
    elif len(large)==1:
        b=large[0]
        for u in small:
            rest=sorted(set(small)-{u})
            for pairs in pairings(rest):
                answer.append(node(node(leaf(u),leaf(b)),node(*(node(*map(leaf,p)) for p in pairs))))
            for pair in combinations(rest,2):
                other=sorted(set(rest)-set(pair))
                unequal=node(leaf(u),node(*map(leaf,pair)))
                equal=node(leaf(b),node(*map(leaf,other)))
                answer.append(node(unequal,equal))
    else:raise ValueError('unexpected native inventory')
    if len(set(answer))!=len(answer):raise ValueError('duplicate genealogies')
    return sorted(answer)

def fronts(f):
    prefix=f['prefix19']+f['maximum_word'];joint=f['joint_zero_gate']
    lt,ht=trees([3,4,8],[1,2]),trees([5,6,7,9,10],[11])
    if (len(lt),len(ht))!=(9,45):raise ValueError('native tree cover differs')
    lw=[tree_word(t,False)[0] for t in lt];hw=[tree_word(t,True)[0] for t in ht]
    for profile,words,high in [([(1,7),(2,7),(3,6),(4,6),(8,6)],lw,False),
                               ([(5,6),(6,6),(7,6),(9,6),(10,6),(11,7)],hw,True)]:
        for word in words:
            state=profile
            for gate in word:
                if not set(gate)<={q for q,_ in state}:raise ValueError('not a binary event')
                state=profile_step(state,gate,high)
                if sum(1<<d for _,d in state)>512:raise ValueError('mass exceeds512')
            if state!=[(11 if high else 1,9)]:raise ValueError('terminal class differs')
    initial=set()
    for x in range(8192):
        for a,b in prefix:
            if x>>a&1 and not x>>b&1:x^=(1<<a)|(1<<b)
        initial.add((x>>1)&2047)
    columns=[sum(((x>>q)&1)<<x for x in range(8192)) for q in range(13)]
    for a,b in prefix+[joint]:columns[a],columns[b]=columns[a]&columns[b],columns[a]|columns[b]
    held={q:sum(1<<x for x in range(8192) if x.bit_count()>=13-q) for q in [0,1,11,12]}
    roots=[]
    for i,j in product(range(9),range(45)):
        word=[joint]+lw[i]+hw[j];v=list(columns)
        for a,b in lw[i]+hw[j]:v[a],v[b]=v[a]&v[b],v[a]|v[b]
        if any(v[q]!=held[q] for q in held):raise ValueError('held ranks fail on full cube')
        image=set()
        for x in initial:
            for a,b in word:
                a-=1;b-=1
                if x>>a&1 and not x>>b&1:x^=(1<<a)|(1<<b)
            image.add((x>>1)&511)
        image=sorted(image)
        roots.append({'id':45*i+j,'low_genealogy':i,'high_genealogy':j,'word':word,
            'prefix_length':31,'remaining_budget':13,'image_size':len(image),'image_sha256':digest(image)})
    return lw,hw,roots

def build(f):
    prefix=f['prefix19']+f['maximum_word'];lw,hw,roots=fronts(f)
    pool=sorted(set(map(tuple,f['proposal_original_clampings'])))
    exclusions=[];unclosed=[]
    for root in roots:
        gates=prefix+root['word'];records=[record_for(gates,lo,hi) for lo,hi in pool]
        classes={}
        for i,r in enumerate(records):
            label=r[4]+r[5]+16;tag=tuple(r[2:4])
            if label>classes.get(tag,(-1,None,None))[0]:classes[tag]=(label,i,16)
        mass=sum(1<<v[0] for v in classes.values())
        if mass<=1<<44:
            first=sorted({v[1] for v in classes.values()},key=lambda i:(-(records[i][4]+records[i][5]),records[i][:2]))
            rest=sorted(set(range(len(records)))-set(first),key=lambda i:(-(records[i][4]+records[i][5]),records[i][:2]))
            for i in first+rest:
                r=records[i];pruned=prune(gates,r)
                b=inner(tuple(map(tuple,pruned['retained_prefix'])))['inner_bound']
                label=r[4]+r[5]+b;tag=tuple(r[2:4])
                if label>classes[tag][0]:
                    old=classes[tag][0];classes[tag]=(label,i,b);mass+=(1<<label)-(1<<old)
                if mass>1<<44:break
        if mass<=1<<44:
            unclosed.append(root['id']);continue
        domains=[];rows=[];selected_mass=0
        for tag,(label,i,b) in sorted(classes.items(),key=lambda v:(-v[1][0],v[0])):
            domains.append([*records[i][:2],b]);rows.append([*records[i],b]);selected_mass+=1<<label
            if selected_mass>1<<44:break
        exclusions.append({'root_id':root['id'],'prefix_sha256':digest(gates),
            'selected_mass':selected_mass,'total_lower_bound':(selected_mass-1).bit_length(),
            'domains':domains,'selected_records_sha256':digest(rows)})
    if unclosed or len(exclusions)!=405:
        raise ValueError('Incomplete sufficient certificate; no exclusion inference')
    return {'schema':'native-both-first-binary-certificate-v1','agent':'six-sorting-2','role':'researcher',
        'n':13,'size_budget':44,'fixture_sha256':hashlib.sha256((ROOT/'fixture.json').read_bytes()).hexdigest(),
        'low_words':lw,'high_words':hw,'roots':roots,'exclusions':exclusions}

def main():
    start=time.monotonic();f=json.loads((ROOT/'fixture.json').read_text())
    for name,pin in f['primitive_source_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=pin:raise ValueError('primitive bytes differ')
    data=build(f);raw=json.dumps(data,separators=(',',':'))+'\n'
    (ROOT/'certificate.json').write_text(raw)
    print(json.dumps({'status':'COMPLETE405_NATIVE_BINARY_CERTIFICATE_GENERATED','agent':'six-sorting-2',
        'role':'researcher','fronts':405,'selected_domains':sum(len(e['domains']) for e in data['exclusions']),
        'nested_domains':sum(d[2]>16 for e in data['exclusions'] for d in e['domains']),
        'minimum_selected_mass':min(e['selected_mass'] for e in data['exclusions']),
        'certificate_bytes':len(raw.encode()),'certificate_sha256':hashlib.sha256(raw.encode()).hexdigest(),
        'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))
if __name__=='__main__':main()
