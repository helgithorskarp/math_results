"""Packed original cubes and exact tag producer for the B21 reduction."""
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations
import json
import os
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
SOURCE = Path(os.environ.get('SORTING_SOURCE_ROOT', ROOT.parents[2]))
FIXTURE_SHA = '55ca31b47ea19de70eb7a61bfc0201fca736417b971c984c1e242ac572688fcf'
PROFILE_SHA = 'dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719'


def need(test, message):
    if not test: raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def tags(mask, gate, high=True):
    a,b = gate
    hit = int(bool(mask&((1<<a)|(1<<b))))
    if high and mask>>a&1 and not mask>>b&1:
        mask ^= (1<<a)|(1<<b)
    if not high and mask>>b&1 and not mask>>a&1:
        mask ^= (1<<a)|(1<<b)
    return mask,hit


def unary(word, high):
    result = []
    for p in range(13):
        mask,d = 1<<p,0
        for gate in word:
            mask,hit = tags(mask,gate,high); d += hit
        result.append([p,mask.bit_length()-1,d])
    return result


def high_events(leaves):
    result = []
    for a,b in combinations(range(13),2):
        after = {}
        for p,label in leaves.items():
            hit = p==a or p==b
            q = b if hit else p
            after[q] = max(after.get(q,-1),label+int(hit))
        units = sum(1<<(label-35) for label in after.values())
        result.append([a,b,[[p,label] for p,label in sorted(after.items())],units,
                       int(a in leaves or b in leaves),int(units<=512)])
    return result


def suffix(mask, cost, word):
    for gate in word:
        mask,hit = tags(mask,gate);cost += hit
    return [mask,cost]


def selected_controls():
    baseline = [(1536,4),(2560,4),(4608,5)]
    rows,overflow,shadows = [],[],[]
    for r in list(range(9))+[10]:
        K = [sorted([r,9]),[max(r,9),11],[11,12]]
        values = [suffix(mask,d,K) for mask,d in baseline]
        need(sorted(values)==[[4608,7],[5120,7],[6144,8]],'baseline terminal differs')
        rows.append({'r':r,'K':K,'terminal':values,'mass':sum(1<<d for _,d in values)})
        for a in range(9):
            charged = []
            for mask,d in baseline:
                mask,hit = tags(mask,[a,10]);charged.append(suffix(mask,d+hit,K))
            mass = sum(1<<d for _,d in charged)
            need(mass==640,'stationary10 overflow differs')
            overflow.append([r,a,charged,mass])
        for q in range(5,9):
            out,delta = suffix((1<<q)|(1<<12),0,K)
            need(out==((1<<11)|(1<<12) if q==r else (1<<q)|(1<<12)), 'shadow terminal differs')
            need(delta==(3 if q==r else 1),'shadow future charge differs')
            shadows.append([r,q,out,delta])
    closure = []
    for gate in combinations(range(9),2):
        mapping = []
        for q in range(5,9):
            out,hit = tags((1<<q)|(1<<12),gate)
            p = (out^(1<<12)).bit_length()-1
            need(p in range(5,9),'shadow escaped its closed port set')
            mapping.append([q,p,hit])
        fibres = {}
        for q,p,hit in mapping:fibres.setdefault(p,[]).append([q,hit])
        need(all(len(v)<=2 and (len(v)==1 or all(hit for _,hit in v)) for v in fibres.values()),
             'selected-subset mass transport premise differs')
        closure.append([list(gate),mapping])
    return {'baseline_terminal':rows,'stationary10_overflow':overflow,
            'shadow_terminal':shadows,'shadow_closed_maps':closure,
            'initial_shadow_mass':96,'collided_shadow_cost_floor':7,
            'collided_terminal_cost_floor':10,'ordinary_ceiling':512}


def boolean_image(word):
    columns = [sum(1<<x for x in range(8192) if x>>q&1) for q in range(13)]
    for a,b in word:columns[a],columns[b] = columns[a]&columns[b],columns[a]|columns[b]
    values = [sum(((c>>x)&1)<<q for q,c in enumerate(columns)) for x in range(8192)]
    counts = Counter(values);full = sorted(counts)
    core_counts = Counter(r>>1&2047 for r in values);core = sorted(core_counts)
    correct = [q for q in range(13) if all((r>>q&1)==int(q>=13-r.bit_count()) for r in full)]
    return {'full_image':full,'full_multiplicities':[counts[r] for r in full],
            'full_image_sha256':digest(full),'core_wires':list(range(1,12)),
            'core_states':core,'core_multiplicities':[core_counts[r] for r in core],
            'core_states_sha256':digest(core),'core_weight_counts':[sum(r.bit_count()==w for r in core) for w in range(12)],
            'correct_output_wires':correct,'target_gate_budget':21}


def decoder_control(image, known35):
    states = image['core_states']
    columns = [sum(1<<j for j,x in enumerate(states) if x>>q&1) for q in range(11)]
    kept = []
    for a,b in [(10-b,10-a) for a,b in known35]:
        if columns[a]&~columns[b]:
            kept.append([a,b]);columns[a],columns[b] = columns[a]&columns[b],columns[a]|columns[b]
    need(all(not(columns[q]&~columns[q+1]) for q in range(10)), 'positive decoder control failed')
    return {'core_suffix':kept,'core_suffix_length':len(kept),'full_sorter_size':23+len(kept)}


def main():
    start = time.monotonic()
    raw = (ROOT/'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==FIXTURE_SHA,'literal fixture pin differs')
    fixture = json.loads(raw)
    path = SOURCE/'round-two/six-sorting-2/semantic-pruning/profile.py'
    need(hashlib.sha256(path.read_bytes()).hexdigest()==PROFILE_SHA,'production profile pin differs')
    spec = importlib.util.spec_from_file_location('b21_profile',path)
    profile = importlib.util.module_from_spec(spec);spec.loader.exec_module(profile)
    words = {'B21':fixture['B21'],'B23':fixture['B21']+fixture['forced_high_word']}
    stages = []
    for name,word in words.items():
        families = {}
        for family,l,h in [('two_minima',2,0),('two_maxima',0,2)]:
            data = profile.analyze_family(13,word,l,h)
            families[family] = {k:data[k] for k in ('low_count','high_count','records','envelope')}
        maximum = unary(word,True);minimum = unary(word,False)
        ports = sorted({r[1] for r in maximum})
        masses = [[p,sum(1<<d for _,hi,d,_ in families['two_maxima']['envelope'] if hi>>p&1)] for p in ports]
        stages.append({'name':name,'word':word,'families':families,'unary_high_routes':maximum,
                       'unary_low_routes':minimum,'ordinary_high_anchored_masses':masses,
                       'ordinary_low_mass':sum(1<<d for _,_,d,_ in families['two_minima']['envelope']),
                       'ordinary_high_mass':sum(1<<d for _,_,d,_ in families['two_maxima']['envelope'])})
    need(stages[0]['ordinary_high_anchored_masses']==[[9,64],[11,80],[12,192]],'B21 passage masses differ')
    need(stages[1]['ordinary_low_mass']==stages[1]['ordinary_high_mass']==448,'B23 frozen-port mass differs')
    originals = [768,257,258,10,130,6]
    records = stages[0]['families']['two_maxima']['records']
    selected = [next(r for r in records if r[1]==mask) for mask in originals]
    need([[r[3],r[4]] for r in selected]==[[1536,4],[2560,4],[4608,5],[4128,5],[4160,5],[4224,5]],
         'changed-prefix original witnesses differ')
    image = boolean_image(words['B23'])
    need(len(image['core_states'])==177 and len(image['full_image'])==179 and image['correct_output_wires']==[0,12],
         'complete projected image differs')
    packet = {'schema':'changed-b21-core11-reduction-v1','agent':'six-sorting-1','role':'researcher',
              'fixture_sha256':FIXTURE_SHA,'production_profile_sha256':PROFILE_SHA,
              'imported_S11_lower_bound':35,'total_budget':44,'stages':stages,
              'remaining_max_route_touch_bounds':[[9,3],[11,2],[12,1]],
              'high_event_controls':[
                  {'name':name,'leaves':[[p,c] for p,c in sorted(leaves.items())],'controls':high_events(leaves)}
                  for name,leaves in [('initial',{9:41,11:42,12:43}),
                                      ('single9_stationary',{9:42,11:42,12:43}),
                                      ('single9_to10',{10:42,11:42,12:43}),
                                      ('after_first_merge',{11:43,12:43})]],
              'selected_original_high_records':selected,'singleton_branch_controls':selected_controls(),
              'B23_boolean_image':image,
              'positive_decoder_control':decoder_control(image,fixture['known11_35']),
              'scope':'Standard total<=44 existence for exact B21 is equivalent to sorting the complete177-state eleven-wire image with<=21 gates; arbitrary suffix order/depth/preparations.'}
    path = ROOT/'certificate.json'
    path.write_text(json.dumps(packet,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher','status':'B21_CORE11_CERTIFICATE_GENERATED',
                      'original_pair_domains':312,'core_image_size':177,'target_gate_budget':21,
                      'certificate_bytes':path.stat().st_size,'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                      'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':main()
