"""Independent full scalar originals/Q/inner profiles/heap anchor replay.

No packed producer or packed primitive import. The written9007/8604
bridges and known S5/S6/S7 floors are explicit mathematical premises.
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


def main():
    operations_allow()
    started = time.monotonic()
    fixture = json.loads((ROOT/'nested-fixture.json').read_text())
    prefix = fixture['literal_prefix']
    need(len(prefix)==32 and word_hash(prefix)==fixture['prefix_sha256'], 'Literal scalar final prefix differs')
    proposed = json.loads((WORK/'nested-proposal.json').read_text())
    need(canonical(proposed['finite'])==proposed['finite_sha256'] and
         canonical(proposed['records'])==proposed['finite']['actual_original_nested_records_sha256'],
         'Packed nested transport binding differs')
    spec = importlib.util.spec_from_file_location('fresh_actual_scalar_nested',ROOT/'prior/numeric.py')
    numeric = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numeric)
    images = set()
    for original in range(8192):
        row = numeric.simulate([original >> p & 1 for p in range(13)],prefix)
        ones = original.bit_count()
        need([row[p] for p in (0,1,11,12)]==[int(ones>=13),int(ones>=12),int(ones>=2),int(ones>=1)],
             'Full8192 input held original ranks differ')
        images.add(sum(row[p] << (p-2) for p in range(2,11)))
    image = sorted(images)
    need(len(image)==72 and word_hash(image)==fixture['nine_core_sha256'], 'Complete72 actual scalar images differ')
    rows,tags,labels = [],set(),[]
    for low,high,claimed in fixture['original_domains']:
        operations_allow()
        need(time.monotonic()-started < 45, 'Incomplete scalar nested replay; no negative inference')
        need(low.bit_count()==high.bit_count()==3 and not low&high and (low|high)<8192,
             'Not an actual immutable original3+3 domain')
        outer = numeric.family(13,prefix,low,high,'outer')
        pruned = numeric.pruning(13,prefix,outer)
        current = tuple(outer[2:4])
        need(current not in tags, 'Nested actual outer marker classes overlap')
        tags.add(current)
        lower,inner,anchored = numeric.inner_checked(tuple(map(tuple,pruned['retained_prefix'])))
        need(lower>=claimed, 'Scalar actual inner bound does not justify the chosen floor')
        label = outer[4]+outer[5]+claimed
        labels.append(label)
        rows.append({'original_record':outer,'actual_oriented_pruning':pruned,
                     'inner_profiles':inner,'inner_anchors':anchored,
                     'claimed_B7':claimed,'proven_B7':lower,'label':label})
    mass = sum(1 << label for label in labels)
    need(labels==fixture['expected_labels'] and mass==fixture['expected_selected_mass'] and
         mass > fixture['strict_size44_mass']==1<<44, 'Actual scalar nested inequality is not strict')
    need(rows==proposed['records'], 'Entire actual-original nested records differ between algorithms')
    finite = {'schema':fixture['schema'],'literal_prefix_sha256':fixture['prefix_sha256'],
              'whole8192_Boolean_image_sha256':word_hash(image),'original_outer_domains':4,
              'actual_outer_labels':labels,'actual_original_nested_records_sha256':canonical(rows),
              'selected_mass':mass,'strict_size44_mass':1<<44,
              'full_original_outer_assignments':4*128,
              'full_actual_inner_assignments':4*3584,
              'arbitrary_suffix_depth':True,'global_size44_exclusion_claimed':False}
    need(finite==proposed['finite'], 'Entire scalar/packed nested mathematical records differ')
    result = {'agent':'six-sorting-1','role':'researcher',
              'status':'ENTIRE_ACTUAL_ORIGINAL_NESTED_RECORDS_AND_STRICT_MASS_SCALAR_VERIFIED',
              'finite':finite,'finite_sha256':canonical(finite),'metrics':numeric.METRICS,
              'seconds':time.monotonic()-started,
              'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'independent_person_review_claimed':False}
    suffix = '-O' if not __debug__ else ''
    (WORK/f'nested-checked{suffix}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
