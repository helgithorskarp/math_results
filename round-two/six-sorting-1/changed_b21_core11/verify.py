"""Standalone scalar certificate and decoder audit; no producer imports."""
from collections import Counter
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
FIXTURE_SHA = '55ca31b47ea19de70eb7a61bfc0201fca736417b971c984c1e242ac572688fcf'
PROFILE_SHA = 'dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719'


def need(test,message):
    if not test:raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def simulate(values,word):
    row = list(values)
    touches = 0
    for a,b in word:
        if row[a]<0 or row[a]>1 or row[b]<0 or row[b]>1:touches += 1
        if row[a]>row[b]:row[a],row[b] = row[b],row[a]
    return row,touches


def numeric_family(word,low):
    records = []
    for original in combinations(range(13),2):
        free = [p for p in range(13) if p not in original]
        touch_mask = final = None
        active_mask = 0
        for x in range(2048):
            values = [0]*13
            for j,p in enumerate(original):values[p] = j-2 if low else j+2
            for j,p in enumerate(free):values[p] = x>>j&1
            touched = 0
            for t,(a,b) in enumerate(word):
                mark = values[a]<0 or values[a]>1 or values[b]<0 or values[b]>1
                if mark:touched |= 1<<t
                if values[a]>values[b]:
                    if not mark:active_mask |= 1<<t
                    values[a],values[b] = values[b],values[a]
            positions = [sum(1<<p for p,v in enumerate(values) if v<0),
                         sum(1<<p for p,v in enumerate(values) if v>1)]
            if final is None:touch_mask,final = touched,positions
            need(touched==touch_mask and positions==final,'free-dependent marker route')
        redundant = ((1<<len(word))-1)&~(touch_mask|active_mask)
        mask = sum(1<<p for p in original)
        records.append([mask if low else 0,0 if low else mask,*final,
                        touch_mask.bit_count(),redundant.bit_count(),redundant])
    records.sort()
    classes = {}
    for _,_,lo,hi,d,r,_ in records:
        old_d,old_c = classes.get((lo,hi),(-1,-1))
        classes[lo,hi] = max(old_d,d),max(old_c,d+r)
    return {'low_count':2 if low else 0,'high_count':0 if low else 2,'records':records,
            'envelope':[[lo,hi,d,c] for (lo,hi),(d,c) in sorted(classes.items())]}


def unary_routes(word,high):
    records = []
    for p in range(13):
        values = [0]*13;values[p] = 2 if high else -1
        output,touches = simulate(values,word)
        records.append([p,output.index(2 if high else -1),touches])
    return records


def first_events(leaves):
    result = []
    for a,b in combinations(range(13),2):
        after = {}
        for p,label in leaves.items():
            initial = [0]*13;initial[p] = 2
            row,touches = simulate(initial,[(a,b)])
            q = row.index(2)
            after[q] = max(after.get(q,-1),label+touches)
        units = sum(2**(label-35) for label in after.values())
        result.append([a,b,[[p,label] for p,label in sorted(after.items())],units,
                       int(any(p in (a,b) for p in leaves)),int(units<=512)])
    return result


def marked_result(mask,cost,word):
    values = [0]*13
    for rank,p in enumerate(p for p in range(13) if mask>>p&1):values[p] = rank+2
    row,touches = simulate(values,word)
    return [sum(1<<p for p,v in enumerate(row) if v>1),cost+touches]


def branch_controls():
    baseline = [(1536,4),(2560,4),(4608,5)]
    terminal,overflow,shadows = [],[],[]
    for r in [0,1,2,3,4,5,6,7,8,10]:
        K = [sorted([r,9]),[max(r,9),11],[11,12]]
        rows = [marked_result(mask,d,K) for mask,d in baseline]
        need(sorted(rows)==[[4608,7],[5120,7],[6144,8]],'selected baseline does not saturate')
        terminal.append({'r':r,'K':K,'terminal':rows,'mass':sum(2**d for _,d in rows)})
        for a in range(9):
            rows = [marked_result(mask,d,[[a,10]]+K) for mask,d in baseline]
            mass = sum(2**d for _,d in rows)
            need(mass==640,'preparation10 touch does not overflow')
            overflow.append([r,a,rows,mass])
        for q in range(5,9):
            mask,touches = marked_result((1<<q)|(1<<12),0,K)
            expected = ((1<<11)|(1<<12)) if q==r else ((1<<q)|(1<<12))
            need(mask==expected and touches==(3 if q==r else 1),'shadow terminal dichotomy failed')
            shadows.append([r,q,mask,touches])
    closure = []
    for a,b in combinations(range(9),2):
        mapping = []
        for q in range(5,9):
            values = [0]*13;values[q],values[12] = 2,3
            row,touches = simulate(values,[(a,b)])
            p = row.index(2)
            need(p in range(5,9) and row[12]==3,'arbitrary preparation port closure failed')
            mapping.append([q,p,touches])
        for p in range(5,9):
            preimages = [r for r in mapping if r[1]==p]
            need(len(preimages)<=2 and (len(preimages)<2 or all(r[2]==1 for r in preimages)),
                 'charged-double-fibre premise failed')
        closure.append([[a,b],mapping])
    need(2**6<96<=2**7 and 7+3==10 and 2**10>512,'shadow arithmetic failed')
    return {'baseline_terminal':terminal,'stationary10_overflow':overflow,'shadow_terminal':shadows,
            'shadow_closed_maps':closure,'initial_shadow_mass':96,'collided_shadow_cost_floor':7,
            'collided_terminal_cost_floor':10,'ordinary_ceiling':512}


def image(word):
    outputs = []
    for x in range(8192):
        row,_ = simulate([x>>p&1 for p in range(13)],word)
        outputs.append(sum(v<<p for p,v in enumerate(row)))
    counts = Counter(outputs);full = sorted(counts)
    core_counts = Counter(r>>1&2047 for r in outputs);core = sorted(core_counts)
    correct = [p for p in range(13) if all((r>>p&1)==int(p>=13-r.bit_count()) for r in full)]
    packet = {'full_image':full,'full_multiplicities':[counts[r] for r in full],
              'full_image_sha256':digest(full),'core_wires':list(range(1,12)),
              'core_states':core,'core_multiplicities':[core_counts[r] for r in core],
              'core_states_sha256':digest(core),'core_weight_counts':[sum(r.bit_count()==w for r in core) for w in range(12)],
              'correct_output_wires':correct,'target_gate_budget':21}
    need(len(full)==179 and len(core)==177 and correct==[0,12],'complete original image/partition differs')
    need(sum(packet['full_multiplicities'])==sum(packet['core_multiplicities'])==8192,'original input multiplicity coverage failed')
    return packet,outputs


def decoder_control(image,known35):
    rows = [[x>>p&1 for p in range(11)] for x in image['core_states']]
    kept = []
    for a,b in [(10-b,10-a) for a,b in known35]:
        if any(row[a]>row[b] for row in rows):
            kept.append([a,b])
            for row in rows:
                if row[a]>row[b]:row[a],row[b] = row[b],row[a]
    need(all(row==sorted(row) for row in rows),'positive core control failed')
    return {'core_suffix':kept,'core_suffix_length':len(kept),'full_sorter_size':23+len(kept)}


def main():
    start = time.monotonic()
    raw = (ROOT/'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==FIXTURE_SHA,'literal source fixture differs')
    fixture = json.loads(raw)
    need(fixture['schema']=='changed-b21-core11-fixture-v1' and fixture['n']==13 and fixture['target_total_size']==44,
         'target fixture parameters differ')
    B = fixture['B21'];high_word = fixture['forced_high_word']
    need(len(B)==21 and B[-2:]==[[4,8],[3,6]] and high_word==[[9,11],[11,12]],'literal prefix differs')
    words = {'B21':B,'B23':B+high_word}
    need(all(type(a)==type(b)==int and 0<=a<b<13 for word in words.values() for a,b in word),'standard gate shape differs')
    stages = []
    for name,word in words.items():
        families = {'two_minima':numeric_family(word,True),'two_maxima':numeric_family(word,False)}
        maximum,minimum = unary_routes(word,True),unary_routes(word,False)
        ports = sorted({r[1] for r in maximum})
        masses = [[p,sum(2**d for _,hi,d,_ in families['two_maxima']['envelope'] if hi>>p&1)] for p in ports]
        stages.append({'name':name,'word':word,'families':families,'unary_high_routes':maximum,
                       'unary_low_routes':minimum,'ordinary_high_anchored_masses':masses,
                       'ordinary_low_mass':sum(2**d for _,_,d,_ in families['two_minima']['envelope']),
                       'ordinary_high_mass':sum(2**d for _,_,d,_ in families['two_maxima']['envelope'])})
    need(stages[0]['ordinary_high_anchored_masses']==[[9,64],[11,80],[12,192]],'initial max budgets differ')
    need(all(2**r*mass<=512<2**(r+1)*mass for (_,mass),r in zip(stages[0]['ordinary_high_anchored_masses'],[3,2,1])),
         'ordinary anchored passage capacity differs')
    last = stages[1]
    need(last['ordinary_low_mass']==last['ordinary_high_mass']==448,'frozen port budget differs')
    need({r[1] for r in last['unary_low_routes']}=={0} and {r[1] for r in last['unary_high_routes']}=={12},
         'outer unary candidates differ')
    need(all(lo&1 for lo,_,_,_ in last['families']['two_minima']['envelope']) and
         all(hi>>12&1 for _,hi,_,_ in last['families']['two_maxima']['envelope']) and 2*448>512,
         'outer-wire anchored freeze premises failed')
    records = stages[0]['families']['two_maxima']['records']
    selected = [next(r for r in records if r[1]==mask) for mask in [768,257,258,10,130,6]]
    need([[r[3],r[4]] for r in selected]==[[1536,4],[2560,4],[4608,5],[4128,5],[4160,5],[4224,5]],
         'six changed-prefix histories differ')
    im,outputs = image(words['B23'])
    decoder = decoder_control(im,fixture['known11_35'])
    expected = {'schema':'changed-b21-core11-reduction-v1','agent':'six-sorting-1','role':'researcher',
                'fixture_sha256':FIXTURE_SHA,'production_profile_sha256':PROFILE_SHA,
                'imported_S11_lower_bound':35,'total_budget':44,'stages':stages,
                'remaining_max_route_touch_bounds':[[9,3],[11,2],[12,1]],
                'high_event_controls':[{'name':name,'leaves':[[p,c] for p,c in sorted(leaves.items())],
                                       'controls':first_events(leaves)} for name,leaves in
                    [('initial',{9:41,11:42,12:43}),('single9_stationary',{9:42,11:42,12:43}),
                     ('single9_to10',{10:42,11:42,12:43}),('after_first_merge',{11:43,12:43})]],
                'selected_original_high_records':selected,'singleton_branch_controls':branch_controls(),
                'B23_boolean_image':im,'positive_decoder_control':decoder,
                'scope':'Standard total<=44 existence for exact B21 is equivalent to sorting the complete177-state eleven-wire image with<=21 gates; arbitrary suffix order/depth/preparations.'}
    packet = json.loads((ROOT/'certificate.json').read_text())
    need(packet==expected,'certificate differs from independent full scalar reconstruction')
    damages = []
    for index in (1,4,5,6):
        bad = deepcopy(packet);bad['stages'][0]['families']['two_maxima']['records'][0][index] += 1;damages.append(bad)
    bad = deepcopy(packet);bad['high_event_controls'][0]['controls'].pop();damages.append(bad)
    bad = deepcopy(packet);bad['singleton_branch_controls']['stationary10_overflow'][0][-1] = 512;damages.append(bad)
    bad = deepcopy(packet);bad['singleton_branch_controls']['shadow_terminal'].pop();damages.append(bad)
    bad = deepcopy(packet);bad['B23_boolean_image']['core_states'].pop();damages.append(bad)
    bad = deepcopy(packet);bad['B23_boolean_image']['correct_output_wires'] = [0,11,12];damages.append(bad)
    bad = deepcopy(packet);bad['B23_boolean_image']['target_gate_budget'] = 22;damages.append(bad)
    bad = deepcopy(packet);bad['selected_original_high_records'][3][4] -= 1;damages.append(bad)
    for bad in damages:
        try:need(bad==expected,'damaged certificate')
        except ValueError:pass
        else:raise ValueError('damaged certificate accepted')
    known = fixture['known11_35']
    need(len(known)==35 and all(0<=a<b<11 for a,b in known),'known11 control shape differs')
    positive11 = 0
    for word in (known,[[10-b,10-a] for a,b in known]):
        for x in range(2048):
            row,_ = simulate([x>>p&1 for p in range(11)],word)
            need(row==sorted(row),'known11 positive control failed');positive11 += 1
    suffix = [[a+1,b+1] for a,b in decoder['core_suffix']]
    for x,r in enumerate(outputs):
        row,_ = simulate([r>>p&1 for p in range(13)],suffix)
        need(row==sorted(row) and sum(row)==x.bit_count(),'positive thirteen-input decoder failed')
    need(decoder['core_suffix_length']==30 and decoder['full_sorter_size']==53,'positive control size differs')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher','status':'B21_CORE11_SCALAR_CERTIFICATE_VERIFIED',
                      'original_pair_domains':312,'original_pair_free_assignments':312*2048,
                      'unary_tag_routes':52,'standard_high_event_controls':312,
                      'baseline_terminal_histories':30,'stationary10_overflow_cases':90,
                      'shadow_terminal_cases':40,'shadow_closed_maps':144,
                      'original_boolean_prefix_inputs':8192,'full_image_size':179,'core_image_size':177,
                      'core_states_sha256':im['core_states_sha256'],'target_gate_budget':21,
                      'known11_positive_inputs':positive11,'positive13_decoder_inputs':8192,
                      'positive13_sorter_size':53,'damages_rejected':len(damages),
                      'certificate_sha256':hashlib.sha256((ROOT/'certificate.json').read_bytes()).hexdigest(),
                      'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':main()
