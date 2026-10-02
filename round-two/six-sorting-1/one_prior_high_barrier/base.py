"""Generate exact L4 image and all original tight LOW cubes from the fixture."""
import hashlib
from itertools import combinations
import json
from pathlib import Path
import minimum_packed as packed

ROOT = Path(__file__).resolve().parent


def main():
    work = ROOT/'work'
    work.mkdir(exist_ok=True)
    f = json.loads((ROOT/'fixture.json').read_text())
    prefix = f['B23']+f['LOW_suffixes']['4']
    packed.need(len(prefix) == 26 and f['total_budget'] == 44, 'Literal budget differs')
    columns = packed.packed(prefix)[0]
    states = sorted({sum((columns[p]>>x&1)<<(p-2) for p in range(2,12)) for x in range(8192)})
    packed.need(len(states) == 157, 'Complete ten-core image differs')
    index = {x:i for i,x in enumerate(states)}
    domains = []
    for a,b in combinations(range(13),2):
        lo = (1<<a)|(1<<b)
        values, data = packed.packed(prefix,lo)
        record = data['outer_record']
        if record[4] != 9:
            continue
        packed.need(record == [lo,0,3,0,9,0,0], 'Tight original LOW record differs')
        image = sorted({sum((values[p]>>x&1)<<(p-2) for p in range(2,12)) for x in range(2048)})
        packed.need(set(image) <= set(states), 'Conditional image outside full threshold image')
        domains.append({'original_LOW_mask':lo,
                        'core_image_index_mask':sum(1<<index[x] for x in image)})
    domains.sort(key=lambda r:r['original_LOW_mask'])
    packed.need(len(domains) == 39, 'Complete original tight LOW family differs')
    (work/'low26-partner4-construction-pilot.json').write_text(json.dumps({'core_states':states})+'\n')
    (work/'low26-partner4-activity-pilot.json').write_text(json.dumps({'all39_original_domains':domains})+'\n')
    (work/'low26-HIGH-binary-selected-screen.json').write_text(json.dumps({'selected_original_pool':f['selected_original_pool']})+'\n')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher','prefix_sha256':packed.digest(prefix),
                      'core_states':157,'core_image_sha256':packed.digest(states),
                      'original_tight_LOW_cubes':39,'domain_index_sha256':packed.digest(domains)},sort_keys=True))


if __name__ == '__main__':
    main()
