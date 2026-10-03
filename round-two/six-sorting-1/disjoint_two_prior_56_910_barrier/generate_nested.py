"""Packed actual-original nested9007 proposal for the one remaining P32.

All inner profiles use actual oriented Q. The separate scalar checker
reconstructs outer128 cubes, Q, inner domains and every anchor weight.
"""
import importlib.util
import hashlib
import json
from pathlib import Path
import resource
import time

from controls import operations_allow

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def need(test,message):
    if not test:
        raise ValueError(message)


def canonical(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def word_hash(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def load(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    operations_allow()
    started = time.monotonic()
    fixture = json.loads((ROOT/'nested-fixture.json').read_text())
    prefix = fixture['literal_prefix']
    need(len(prefix)==32 and word_hash(prefix)==fixture['prefix_sha256'], 'Actual literal final prefix differs')
    profile = load('fresh_nested_packed_profile',ROOT/'prior/profile.py')
    pruning = load('fresh_nested_packed_pruning',ROOT/'prior/pruning.py')
    anchors = load('fresh_nested_packed_anchors',ROOT/'prior/anchors.py')
    values = list(profile.truth_columns(13))
    for a,b in prefix:
        values[a],values[b] = values[a]&values[b],values[a]|values[b]
    image = sorted({sum((values[p] >> assignment & 1) << (p-2) for p in range(2,11))
                    for assignment in range(8192)})
    need(len(image)==72 and word_hash(image)==fixture['nine_core_sha256'], 'Full original9-core image differs')
    rows,tags,labels = [],set(),[]
    for low,high,claimed in fixture['original_domains']:
        operations_allow()
        need(time.monotonic()-started < 45, 'Incomplete nested packed selection; no negative inference')
        need(low.bit_count()==high.bit_count()==3 and not low&high and (low|high)<8192,
             'An actual original3+3 domain is required')
        pruned = pruning.pruning(prefix,low,high,profile)
        outer = pruned['outer_record']
        current = tuple(outer[2:4])
        need(current not in tags, 'Distinct actual outer tag classes required')
        tags.add(current)
        raw_inner = profile.analyze(7,pruned['retained_prefix'])
        anchored = anchors.both(7,raw_inner)
        # The credited packed profiler exposes raw original records and
        # auxiliary prefix traces; its scalar counterpart exposes the hash
        # of every full original record. Align that mathematical schema.
        # No record field, envelope, anchored mass or label is omitted.
        inner = {name:{'low_count':data['low_count'],'high_count':data['high_count'],
                       'envelope':data['envelope'],'records_sha256':word_hash(data['records']),
                       'summary':data['summary']} for name,data in raw_inner.items()}
        lower = max(16,*(r['lower_bound'] for r in anchored.values()))
        need(lower>=claimed, 'Actual inner anchored bound does not prove the claimed floor')
        label = outer[4]+outer[5]+claimed
        labels.append(label)
        rows.append({'original_record':outer,'actual_oriented_pruning':pruned,
                     'inner_profiles':inner,'inner_anchors':anchored,
                     'claimed_B7':claimed,'proven_B7':lower,'label':label})
    mass = sum(1 << label for label in labels)
    need(labels==fixture['expected_labels'] and mass==fixture['expected_selected_mass'] and
         mass > fixture['strict_size44_mass']==1<<44, 'Strict actual four-original nested inequality differs')
    finite = {'schema':fixture['schema'],'literal_prefix_sha256':fixture['prefix_sha256'],
              'whole8192_Boolean_image_sha256':word_hash(image),'original_outer_domains':4,
              'actual_outer_labels':labels,'actual_original_nested_records_sha256':canonical(rows),
              'selected_mass':mass,'strict_size44_mass':1<<44,
              'full_original_outer_assignments':4*128,
              'full_actual_inner_assignments':4*3584,
              'arbitrary_suffix_depth':True,'global_size44_exclusion_claimed':False}
    result = {'agent':'six-sorting-1','role':'researcher',
              'status':'PACKED_ACTUAL_FOUR_ORIGINAL_NESTED_PROPOSAL_NEEDS_SCALAR_REPLAY',
              'finite':finite,'finite_sha256':canonical(finite),'records':rows,
              'seconds':time.monotonic()-started,
              'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (WORK/'nested-proposal.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)


if __name__=='__main__':
    main()
