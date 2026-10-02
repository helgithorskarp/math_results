"""Packed producer for a complete simultaneous first-slack exclusion.

Canonical pair partitions and exact original free-input cubes. No solver,
preparation-length bound, private input, or enumeration cap is a premise.
See SOURCE-CREDITS.md for unchanged and copied published primitives.
"""
import hashlib, json, resource, time
from collections import Counter
from functools import lru_cache
from itertools import product
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

def family_words(profile, high):
    small = [q for q, d in profile if d == 6]
    large = [q for q, d in profile if d == 7]
    choose = max if high else min
    words = []
    for lower_pairs in pairings(small):
        first = [sorted(p) for p in lower_pairs]
        roots = sorted(large+[choose(p) for p in lower_pairs])
        if len(roots) != 4:
            raise ValueError('unexpected saturated dyadic inventory')
        for upper_pairs in pairings(roots):
            second = [sorted(p) for p in upper_pairs]
            word = first+second+[sorted(choose(p) for p in upper_pairs)]
            state = profile
            for gate in word:
                state = profile_step(state, gate, high)
            if len(state) != 1 or state[0][1] != 9:
                raise ValueError('canonical genealogy does not finish at cost9')
            words.append(word)
    return sorted(words)

def boolean_core(prefix):
    image=set()
    for x in range(8192):
        value=x
        for a,b in prefix:
            if (value>>a)&1 and not (value>>b)&1:
                value^=(1<<a)|(1<<b)
        image.add((value>>1)&2047)
    return sorted(image)

def fronts(fixture):
    prefix = fixture['prefix19']+fixture['maximum_word']
    initial_core=boolean_core(prefix)
    low = [(1,7),(2,7),(3,5),(4,6),(6,5),(8,6)]
    high = [(3,5),(5,6),(6,5),(7,6),(9,6),(10,6),(11,7)]
    joint = fixture['joint_zero_gate']
    low = profile_step(low, joint, False)
    high = profile_step(high, joint, True)
    if set(q for q,_ in low) & set(q for q,_ in high):
        raise ValueError('joint event failed disjoint-support reduction')
    crosses = sorted(sorted([a,b]) for a,d in low if d==6
                     for b,e in high if e==6)
    roots = []
    columns = [sum(((x >> q) & 1) << x for x in range(8192)) for q in range(13)]
    expected_held = {q:sum(1<<x for x in range(8192) if x.bit_count()>=13-q)
                     for q in [0,1,11,12]}
    for a,b in prefix+[joint]:
        columns[a],columns[b] = columns[a]&columns[b],columns[a]|columns[b]
    for cross in crosses:
        lp, hp = profile_step(low,cross,False), profile_step(high,cross,True)
        if any(sum(1<<d for _,d in f)!=512 for f in [lp,hp]):
            raise ValueError('cross did not saturate both families')
        if set(q for q,_ in lp) & set(q for q,_ in hp):
            raise ValueError('cross created support intersection')
        lw,hw=family_words(lp,False),family_words(hp,True)
        if (len(lw),len(hw))!=(3,9):
            raise ValueError('incomplete 3x9 canonical genealogy inventory')
        for i,j in product(range(3),range(9)):
            suffix=[joint,cross]+lw[i]+hw[j]
            if len(suffix)!=11:
                raise ValueError('canonical front length is not32')
            values=list(columns)
            for a,b in [cross]+lw[i]+hw[j]:
                values[a],values[b]=values[a]&values[b],values[a]|values[b]
            if any(values[q]!=expected_held[q] for q in expected_held):
                raise ValueError('full8192 columns do not hold four extreme ranks')
            states=set()
            for original in initial_core:
                value=original
                for a,b in suffix:
                    a-=1;b-=1
                    if (value>>a)&1 and not (value>>b)&1:
                        value^=(1<<a)|(1<<b)
                states.add((value>>1)&511)
            states=sorted(states)
            roots.append({'id':len(roots),'cross':cross,'low_genealogy':i,
                          'high_genealogy':j,'word':suffix,'prefix_length':32,
                          'remaining_budget':12,'nine_core_states':states,
                          'image_sha256':digest(states)})
    if len(roots)!=405:
        raise ValueError('complete simultaneous cover is not405 fronts')
    return roots

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

def build(fixture):
    prefix=fixture['prefix19']+fixture['maximum_word']
    roots=fronts(fixture)
    pool=sorted(set(map(tuple,fixture['proposal_original_clampings'])))
    excluded=[];not_excluded=[];calls=0;bounds=Counter()
    for root in roots:
        gates=prefix+root['word']
        records=[record_for(gates,lo,hi) for lo,hi in pool]
        classes={}
        for i,row in enumerate(records):
            label=row[4]+row[5]+16;tag=tuple(row[2:4])
            if label>classes.get(tag,(-1,None,None))[0]:classes[tag]=(label,i,None)
        mass=sum(1<<r[0] for r in classes.values());constant=mass
        if mass<=1<<44:
            first=sorted({v[1] for v in classes.values()},key=lambda i:(-(records[i][4]+records[i][5]),records[i][:2]))
            rest=sorted(set(range(len(records)))-set(first),key=lambda i:(-(records[i][4]+records[i][5]),records[i][:2]))
            for i in first+rest:
                row=records[i];pruned=prune(gates,row)
                w={'pruning':pruned,**inner(tuple(map(tuple,pruned['retained_prefix'])))}
                label=row[4]+row[5]+w['inner_bound'];calls+=1;bounds[w['inner_bound']]+=1
                tag=tuple(row[2:4])
                if label>classes[tag][0]:
                    old=classes[tag][0];classes[tag]=(label,i,w);mass+=(1<<label)-(1<<old)
                if mass>1<<44:break
        if mass>1<<44:
            selected=[];selected_mass=0
            for tag,(label,i,w) in sorted(classes.items(),key=lambda item:(-item[1][0],item[0])):
                selected.append({'original':records[i][:2],'current':list(tag),
                                 'outer_record':records[i],
                                 'constant_only':w is None,
                                 'inner_bound':16 if w is None else w['inner_bound'],
                                 'nested_label':label,**({} if w is None else w)})
                selected_mass+=1<<label
                if selected_mass>1<<44:break
            excluded.append({'root_id':root['id'],'prefix_sha256':digest(gates),
                             'selected_mass':selected_mass,
                             'total_lower_bound':(selected_mass-1).bit_length(),
                             'selected_domains':selected})
        else:
            not_excluded.append({'root_id':root['id'],'constant_mass':constant,
                                 'best_selected_mass':mass})
    if not_excluded or len(excluded)!=405:
        raise ValueError('Incomplete sufficient certificate; do not infer exclusion')
    compact_roots=[{k:v for k,v in root.items() if k!='nine_core_states'}|{'image_size':len(root['nine_core_states'])} for root in roots]
    return {'schema':'native-first-joint-saturation-certificate-v1','agent':'six-sorting-2','role':'researcher',
            'n':13,'size_budget':44,'fixture_sha256':hashlib.sha256((ROOT/'fixture.json').read_bytes()).hexdigest(),
            'cross_gates':sorted({tuple(r['cross']) for r in roots}),
            'roots':compact_roots,'exclusions':excluded}

def main():
    started=time.monotonic()
    fixture=json.loads((ROOT/'fixture.json').read_text())
    for n,pin in fixture['primitive_source_sha256'].items():
        if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=pin:
            raise ValueError('published primitive changed: '+n)
    data=build(fixture)
    out=ROOT/'certificate.json'
    out.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':'COMPLETE405_SELECTED_NESTED_CERTIFICATE_REGENERATED','agent':'six-sorting-2','role':'researcher',
                     'fronts':len(data['roots']),'selected_domains':sum(len(r['selected_domains']) for r in data['exclusions']),
                     'certificate_bytes':out.stat().st_size,'certificate_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
                     'minimum_selected_mass':min(r['selected_mass'] for r in data['exclusions']),
                     'distinct_inner_words':inner.cache_info().currsize,'seconds':time.monotonic()-started,
                     'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))

if __name__=='__main__':main()
