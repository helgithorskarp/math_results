"""Standalone original-cube/pruning and abstract-route checker.
Numeric primitives are adapted from our actual9285 checker,
source2b8d0d2b5766ecb8775c72db231fa5eb06ee512a; original peer source
7f0c4f85a073c697803d580d3d04d4cba2aed07e is credited. No producer or
sibling module is imported. Normalization uses abstract cost transitions;
original identities and retained functions use every numeric free input.
Same-author algorithmic independence is not external-person review.
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
FIXTURE_SHA256='c75eb6b8d98d94f824def44c6ce13a7d09700e04d7422fea6c70522c99c3b43f'
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



def mass(state):return sum(1<<d for p,d in state)
def move(state,gate):
    a,b=gate;result={}
    for p,d in state:
        hit=p in gate;q=a if hit else p
        result[q]=max(result.get(q,-1),d+int(hit))
    return tuple(sorted(result.items()))

def normalization(initial):
    states={initial};todo=[initial];parents={initial:[]};first=[];tests=0
    while todo:
        current=todo.pop();need(mass(current)==448,'pre-slack mass differs')
        for a,b in combinations(range(1,12),2):
            gate=(a,b);after=move(current,gate);tests+=1;hits=sum(p in gate for p,d in current)
            need(mass(after)>=448,'ordinary mass decreased')
            if hits==0:need(after==current,'preparation changed LOW class')
            if hits==1:need(mass(after)>448,'LOW singleton did not increase mass')
            if mass(after)==448 and hits:
                need(hits==2 and len({d for p,d in current if p in gate})==1,'zero-cost event not equal binary')
                if after not in states:states.add(after);todo.append(after);parents[after]=parents[current]+[[a,b]]
            if hits==2 and 448<mass(after)<=512:
                operands={p:d for p,d in current if p in gate};need(operands.get(3)==6 and sorted(operands.values())==[6,7],'first LOW binary costs differ')
                p=next(p for p in operands if p!=3);prior=parents[current]
                need(p in (1,2,4) and all(p not in g and 3 not in g for g in prior),'first LOW original endpoint touched')
                current2=move(initial,gate);commuted=current2
                for earlier in prior:commuted=move(commuted,earlier)
                need(commuted==after,'earlier LOW binary does not commute')
                tail=[]
                while len(current2)>1:
                    equal=[(q,s) for (q,cq),(s,cs) in combinations(current2,2) if cq==cs]
                    need(len(equal)==1,'forced LOW equality pair not unique')
                    g=list(sorted(equal[0]));current2=move(current2,tuple(g));tail.append(g)
                need(current2==((1,9),) and len(tail)==2,'coalescent LOW node differs')
                need(not prior or tail[:len(prior)]==prior,'earlier LOW event dropped')
                first.append({'prior_LOW_word':prior,'first_binary':[a,b],'partner':p,'canonical_suffix':[[a,b]]+tail})
    first.sort(key=lambda x:(len(x['prior_LOW_word']),x['prior_LOW_word'],x['first_binary']))
    need(len(states)==4 and len(first)==6 and tests==220,'first-binary completeness differs')
    return {'zero_slack_states':[list(map(list,c)) for c in sorted(states)],'local_gate_controls':tests,'first_binary_cases':first}


def full_image(gates):
    columns=[sum(1<<x for x in range(8192) if x>>p&1) for p in range(13)]
    for a,b in gates:
        need(0<=a<b<13,'literal comparator is not standard')
        columns[a],columns[b]=columns[a]&columns[b],columns[a]|columns[b]
    for p in (0,1,12):
        expected=sum(1<<x for x in range(8192) if p>=13-x.bit_count())
        need(columns[p]==expected,'three held outputs differ')
    full={sum((columns[p]>>x&1)<<p for p in range(13)) for x in range(8192)}
    image=sorted({(x>>2)&1023 for x in full});count('prefix_boolean_inputs',8192)
    return len(full),image


def audit_case_cover(packet,expected,fixture):
    cases=packet['canonical_cases'];need([x['partner'] for x in cases]==[1,2,4],'missing/duplicate normal form')
    need(packet['normalization']==expected,'complete first LOW binary cover differs')
    for case in cases:
        p=case['partner'];need(case['suffix_after_B23']==fixture['suffixes'][str(p)],'canonical suffix differs')
        need(case['prefix_sha256']==digest(fixture['B23']+case['suffix_after_B23']),'literal prefix hash differs')


def independent_pruning(gates,stored,expected_mask):
    need(stored['outer_record'][:2]==[expected_mask,0],'original LOW mask differs')
    row=family(13,gates,expected_mask,0,'selected');need(row==stored['outer_record'],'complete numeric original domain differs')
    actual=pruning(13,gates,row);del actual['marked_touch_mask']
    need(actual==stored,'retained whole-domain pruning map differs')
    return row,actual


def obstruction(packet,fixture):
    p26=fixture['B23']+fixture['suffixes']['2'];p25=p26[:25]
    selected=packet['earliest_selected_pruning'];need(len(selected)==2,'selected early classes missing')
    records=[independent_pruning(p25,s,m)[0] for s,m in zip(selected,fixture['selected_original_LOW'])]
    need(len({tuple(s[2:4]) for s in records})==2,'selected early classes overlap')
    w=sum(1<<sum(s[4:6]) for s in records)
    need(w==packet['earliest_selected_mass']==768 and packet['ordinary_pair_size44_ceiling']==512,'strict selected inequality differs')
    need(w>512,'early semantic mass is not strict')
    row,pruned=independent_pruning(p26,packet['single_C10_pruning'],40)
    need(row==[40,0,3,0,9,1,1<<24] and len(pruned['retained_prefix'])==16,'single C10 domain differs')
    need(packet['size_lower_bound_of_middle_stem']==fixture['imported_S11_lower_bound']+row[4]+row[5]==45,'lower bound differs')
    control,cpruned=independent_pruning(p25,packet['same_configuration_active_pruning'],5)
    need(control==[5,0,5,0,8,0,0],'current-port-only deletion was accepted')
    initial,free=template(13,5,0);x=fixture['same_configuration_active_control']['assignment']
    for j,p in enumerate(free):initial[p]=x>>j&1
    actual=simulate(initial,p25[:-1]);need(actual==packet['same_configuration_active_row'] and actual[1]>actual[4]>=0,'active conditional control differs')
    need(packet['excluded_first_LOW_binary']==[2,3] and packet['remaining_first_LOW_binary_partners']==[1,4],'claimed branch scope differs')
    return pruned


def identity_formula(fixture):
    prefix=fixture['B23']+[[2,3]];initial,free=template(13,40,0)
    for x in range(2048):
        row=initial.copy()
        for j,p in enumerate(free):row[p]=x>>j&1
        actual=simulate(row,prefix)
        a0=min(row[0],row[11],row[2],row[4]);a8=min(row[8],row[9],row[10],row[12]);a=min(a0,a8)
        b4=min(max(row[2],row[4]),max(row[10],row[12]))
        b9=max(row[8],row[9]);b=min(b4,b9,max(a0,a8))
        need(actual[1]==a and actual[4]==b and 0<=a<=b,'ordered identity formula differs')
        count('identity_formula_inputs')


def positives(fixture,pruned):
    sorter=fixture['known11_35'];need(len(sorter)==35,'S11 positive control size differs')
    for x in range(2048):
        row=[x>>p&1 for p in range(11)]
        need(simulate(row,sorter)==sorted(row),'known35 sorter fails')
        need(simulate(simulate(row,pruned['retained_prefix']),sorter)==sorted(row),'pruned orientation/port decoder control fails')
        count('positive11_inputs')
    control=fixture['known10_29'];need(len(control)==29,'ten-core positive control size differs')
    for x in range(1024):
        row=[x>>p&1 for p in range(10)];need(simulate(row,control)==sorted(row),'known29 sorter fails');count('positive10_inputs')
    for p in (1,2,4):
        word=fixture['B23']+fixture['suffixes'][str(p)]+[[a+2,b+2] for a,b in control]
        need(len(word)==55,'above-budget full control size differs')
        for x in range(8192):
            row=[x>>q&1 for q in range(13)];need(simulate(row,word)==sorted(row),'full13 core-decoder control fails');count('positive13_inputs')


def rejected(fn):
    try:fn()
    except ValueError:return 1
    raise ValueError('damaged mathematical certificate accepted')


def damages(packet,fixture,normal):
    total=0
    bad=deepcopy(packet);bad['canonical_cases'].pop();total+=rejected(lambda:audit_case_cover(bad,normal,fixture))
    bad=deepcopy(packet);bad['normalization']['first_binary_cases'].pop();total+=rejected(lambda:audit_case_cover(bad,normal,fixture))
    bad=deepcopy(packet);bad['single_C10_pruning']['outer_record'][5]=0;total+=rejected(lambda:obstruction(bad,fixture))
    bad=deepcopy(packet);bad['single_C10_pruning']['outer_record'][6]=1<<23;total+=rejected(lambda:obstruction(bad,fixture))
    bad=deepcopy(packet);bad['single_C10_pruning']['retained_prefix'][0].reverse();total+=rejected(lambda:obstruction(bad,fixture))
    bad=deepcopy(packet);bad['single_C10_pruning']['input_to_output_wire'][0]=1;total+=rejected(lambda:obstruction(bad,fixture))
    bad=deepcopy(packet);bad['same_configuration_active_pruning']['outer_record'][5:]=[1,1<<24];total+=rejected(lambda:obstruction(bad,fixture))
    bad=deepcopy(packet);bad['size_lower_bound_of_middle_stem']=44;total+=rejected(lambda:obstruction(bad,fixture))
    return total


def main():
    start=time.monotonic();raw=(ROOT/'fixture.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==FIXTURE_SHA256,'fixture changed');fixture=json.loads(raw)
    raw=(ROOT/'certificate.json').read_bytes();packet=json.loads(raw)
    need(packet['schema']=='first-low-binary-semantic-barrier-v1' and packet['fixture_sha256']==FIXTURE_SHA256,'certificate scope differs')
    records=[]
    for a,b in combinations(range(13),2):records.append(family(13,fixture['B23'],(1<<a)+(1<<b),0,'base_LOW'))
    data=summary(records,2,0)
    need(data['records_sha256']==packet['base_LOW_records_sha256'] and data['envelope']==packet['base_LOW_envelope'],'initial complete LOW histories differ')
    initial=[]
    for lo,hi,d,c in data['envelope']:
        need(hi==0 and lo&1 and lo.bit_count()==2,'global LOW0 marker is not held')
        initial.append(((lo^1).bit_length()-1,d))
    initial=tuple(sorted(initial));need([list(x) for x in initial]==fixture['initial_LOW'] and mass(initial)==448,'initial LOW classes differ')
    normal=normalization(initial);audit_case_cover(packet,normal,fixture)
    for case in packet['canonical_cases']:
        full,image=full_image(fixture['B23']+case['suffix_after_B23'])
        need(full==case['full_image_size'] and image==case['ten_core_image'] and digest(image)==case['ten_core_image_sha256'],'full image/decoder differs')
        need(len(image)==case['ten_core_image_size'] and case['ten_core_budget']==18,'ten-core budget differs')
    pruned=obstruction(packet,fixture);identity_formula(fixture);proof=dict(METRICS)
    positives(fixture,pruned);damaged=damages(packet,fixture,normal)
    result={'agent':'six-sorting-1','role':'researcher','status':'FIRST_LOW_BINARY_SEMANTIC_BARRIER_VERIFIED',
      'certificate_sha256':hashlib.sha256(raw).hexdigest(),'first_LOW_binary_cases':6,'canonical26_stems':3,
      'excluded_first_LOW_binary':[2,3],'remaining_first_LOW_binary_partners':[1,4],
      'strict_P25_mass':768,'P26_original_domain_C':10,'middle_stem_minimum_size':45,
      'core_image_sizes':[c['ten_core_image_size'] for c in packet['canonical_cases']],
      'proof_metrics':proof,'total_metrics':METRICS,'damages_rejected':damaged,
      'same_author_algorithmic_independence':True,'external_person_review_claimed':False,
      'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
