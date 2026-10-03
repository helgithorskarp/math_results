"""Independent full scalar input image and all original LOW/HIGH pair cubes."""
import json
from itertools import combinations
from pathlib import Path
import numeric

ROOT = Path(__file__).resolve().parent


def main():
    f = json.loads((ROOT/'fixture.json').read_text())
    word = f['B23']+f['LOW_suffixes']['4']
    states = set()
    for x in range(8192):
        row = numeric.simulate([x>>p&1 for p in range(13)],word)
        numeric.need(row[0] == int(x == 8191) and row[1] == int(x.bit_count() >= 12) and
                     row[12] == int(x != 0), 'Held original ranks differ')
        states.add(sum(row[p]<<(p-2) for p in range(2,12)))
    states = sorted(states)
    supplied = json.loads((ROOT/'work/low26-partner4-construction-pilot.json').read_text())
    numeric.need(states == supplied['core_states'] and len(states) == 157, 'Full scalar image differs')
    low, high = [], []
    for a,b in combinations(range(13),2):
        mask = (1<<a)|(1<<b)
        low.append(numeric.family(13,word,mask,0,'base_LOW'))
        high.append(numeric.family(13,word,0,mask,'base_HIGH'))
    low_summary, high_summary = numeric.summary(low,2,0), numeric.summary(high,0,2)
    numeric.need(low_summary['envelope'] == [[3,0,9,9]], 'Frozen tight LOW class differs')
    actual = []
    for lo,hi,d,c in high_summary['envelope']:
        numeric.need(lo == 0 and hi.bit_count() == 2 and hi>>12&1, 'Held HIGH rank differs')
        actual.append([(hi^(1<<12)).bit_length()-1,d])
    numeric.need(actual == f['initial_HIGH'] and sum(1<<d for p,d in actual) == 448,
                 'Original HIGH weighted classes differ')
    tight = sorted(r[0] for r in low if r[4] == 9)
    supplied_domains = json.loads((ROOT/'work/low26-partner4-activity-pilot.json').read_text())['all39_original_domains']
    numeric.need(tight == [r['original_LOW_mask'] for r in supplied_domains] and len(tight) == 39,
                 'Original tight LOW masks differ')
    pool = f['selected_original_pool']
    numeric.need(len(pool) == len({tuple(p) for p in pool}) == 99 and pool == sorted(pool) and
                 all(lo.bit_count() == hi.bit_count() == 3 and not lo&hi and lo|hi < 8192 for lo,hi in pool),
                 'Selected original3+3 proposal pool differs')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher','status':'ALL_ORIGINAL_BASE_DOMAINS_AND_GLOBAL_IMAGE_VERIFIED',
                      'full_Boolean_inputs':8192,'core_image_sha256':numeric.digest(states),
                      'complete_LOW_records_sha256':numeric.digest(low),
                      'complete_HIGH_records_sha256':numeric.digest(high),
                      'original_tight_LOW_masks':tight,'initial_HIGH':actual,'metrics':numeric.METRICS},sort_keys=True))


if __name__ == '__main__':
    main()
