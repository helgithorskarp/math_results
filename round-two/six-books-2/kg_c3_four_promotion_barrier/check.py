"""Check complete cold comparison, all positive graphs and boundary markers.

This consumes a freshly executed compare.py receipt, binds its input streams,
and checks the previously frozen mathematical fixture. It cannot replace
either census or their completeness arguments in PROOF.md.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import resource
import time
import literal
import model as m
import saturation as sat
from compare import integer, subset, digest

HERE = Path(__file__).resolve().parent


def ordered(values, size, high):
    m.need(type(values) is list and len(values) == size, 'recipe size')
    for x in values:
        integer(x, 0, high-1)
    m.need(values == sorted(set(values)), 'recipe ordered uniqueness')


def validate_positive(item, cases, geometry):
    m.need(set(item) == {'index','J','P','D','weight','red_bad','degrees',
                        'degree_sequence','red_pages','blue_pages'}, 'positive schema')
    index = integer(item['index'], 0, len(cases)-1)
    ordered(item['J'], 3, 7); ordered(item['P'], 4, 35)
    q = len(item['D'])
    m.need(q in (8,9), 'positive deletion size')
    ordered(item['D'], q, 35)
    integer(item['weight'], 1, 6); integer(item['red_bad'], 0, 231)
    m.need(type(item['degrees']) is bool, 'positive degree predicate')
    case = cases[index]
    m.need(item['J'] == case[1:4] and item['P'] == case[4:8] and
           item['weight'] == case[8], 'positive case identity')
    rows = literal.rows(geometry, item['J'], item['P'], item['D'])
    s = m.literal_summary(rows)
    m.need(not any(v[2] == 'blue' for v in s['violations']) and s['edges'] == 126-3*q,
           'positive literal blue cap/edges')
    m.need(item['red_bad'] == len(s['violations']) and
           item['degrees'] == all(7 <= d <= 10 for d in s['degrees']) and
           item['degree_sequence'] == s['degrees'], 'positive literal red count/degrees')
    for name in ('red_pages','blue_pages'):
        m.need(item[name] == {str(k):v for k,v in s[name].items()}, 'positive literal page histogram')
    return (index,q,tuple(item['D']))


def inventory(entries):
    h = hashlib.sha256()
    previous = None
    counts = Counter()
    for x in sorted(entries,key=lambda z:(z['index'],len(z['D']),z['D'])):
        q = len(x['D'])
        key = (x['index'],q,tuple(x['D']))
        m.need(previous is None or previous < key, 'complete inventory duplicate')
        previous = key; counts[q] += 1
        value = (x['index'],q,x['D'],x['red_bad'],x['degrees'],x['J'],x['P'],x['weight'],
                 x['degree_sequence'],x['red_pages'],x['blue_pages'])
        h.update((json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode())
    return dict(records=sum(counts.values()),q8_records=counts[8],q9_records=counts[9],sha256=h.hexdigest())


def controls():
    lines = (HERE/'primary21.rows').read_text().splitlines()
    m.need(len(lines) == 21 and all(len(s) == 21 and set(s) <= {'0','1'} for s in lines),
           'primary21 fixture domain')
    primary = [{v for v,b in enumerate(s) if b == '1'} for s in lines]
    geo = literal.geometry()
    kg = [{v for v in range(21) if geo[0][u].isdisjoint(geo[0][v])} for u in range(21)]
    out = {'primary21':m.literal_summary(primary), 'KG21':m.literal_summary(kg)}
    for name,e in (('primary21',93),('KG21',105)):
        m.need(out[name]['edges'] == e and not out[name]['violations'], 'baseline exact caps')
    recipes = {
        'q8_minimum':([0,1,2],[2,25,32,34],[4,6,8,10,17,23,25,34],18),
        'q9_minimum':([0,1,6],[1,10,23,25],[0,4,6,7,10,11,19,26,29],36)}
    for name,(J,P,D,bad) in recipes.items():
        s = m.literal_summary(literal.rows(geo,J,P,D))
        m.need(s['edges'] == 126-3*len(D) and len(s['violations']) == bad and
               all(x[2] == 'red' for x in s['violations']), 'sharp control')
        out[name] = dict(J=J,P=P,D=D,summary=s)
    return out


def main(args):
    started = time.monotonic()
    work = args.work; producer = work/'producer'; native = work/'native'
    frozen = json.loads((HERE/'expected.json').read_text())
    receipt = json.loads((work/'comparison.json').read_text())
    m.need(receipt['status'] == 'COMPLETE_ENTRYWISE_TWO_ALGORITHM_AGREEMENT', 'complete entry comparison')
    fields = ('first','next','total','producer_representatives','terminal_counts','terminal_red_hist',
              'observed_orbit_counts','manifest_sha256','checked_bases_and_full_pools',
              'checked_complete_terminal_lists','transport_sha256')
    for k in fields:
        m.need(receipt[k] == frozen[k], 'frozen complete comparison field: '+k)
    m.need(receipt['sources'] == {'compare.py':digest(HERE/'compare.py'),'model.py':digest(HERE/'model.py')},
           'comparison source identity')
    m.need(digest(producer/'cases.txt') == frozen['manifest_sha256'], 'case manifest frozen bytes')
    cases = [list(map(int,s.split())) for s in (producer/'cases.txt').read_text().splitlines()]
    m.need(len(cases) == 305874 and sum(c[8] for c in cases) == 1832600, 'complete case weights')
    for collection,directory in (('producer_inputs',producer),('native_inputs',native)):
        for part in receipt[collection]:
            m.need(digest(directory/part['file']) == part['sha256'], 'compared phase stream bytes')
    entries = []
    geometry = literal.geometry()
    m.need(geometry[1] == [m.geometry()[2],m.geometry()[3]], 'independent orbit numbering')
    for part in receipt['producer_inputs']:
        name = 'positive-'+part['file'].split('-')[1]
        path = producer/name
        m.need(digest(path) == part['positive_sha256'], 'compared complete positive stream')
        for line in path.open():
            x = json.loads(line); validate_positive(x,cases,geometry); entries.append(x)
    inv = inventory(entries)
    m.need(all(inv[k] == frozen['positive_inventory'][k] for k in inv), 'entire frozen positive inventory')
    marker_bytes = (producer/'saturation-markers.json').read_bytes()
    m.need(marker_bytes == (HERE/'saturation-markers.json').read_bytes(), 'cold/frozen boundary marker bytes')
    m.need(hashlib.sha256(marker_bytes).hexdigest() == frozen['saturation']['markers_sha256'], 'frozen marker hash')
    markers = json.loads(marker_bytes)
    def recipe_key(x):
        return (x['index'],tuple(x['J']),tuple(x['P']),tuple(x['D']),x['weight'])
    m.need({recipe_key(x) for x in markers} == {recipe_key(x) for x in entries if len(x['D']) == 9},
           'boundary markers bind the COMPLETE q9 inventory')
    m.need(sat.check(markers) == frozen['saturation']['counts'], 'expanded boundary saturation')
    damages = []
    control = deepcopy(entries[0])
    mutations = {
        'truncated-deletions':lambda x:x['D'].pop(),
        'Boolean-index':lambda x:x.update(index=True),
        'wrong-case-weight':lambda x:x.update(weight=5),
        'forged-red-count':lambda x:x.update(red_bad=x['red_bad']+1),
        'forged-degree-flag':lambda x:x.update(degrees=not x['degrees']),
        'forged-page-histogram':lambda x:x.update(blue_pages={}),
        'duplicate-deletion':lambda x:x['D'].__setitem__(0,x['D'][1]),
        'forged-pass-flag':lambda x:x.update(verified=True)}
    for name,change in mutations.items():
        bad = deepcopy(control); change(bad)
        try: validate_positive(bad,cases,geometry)
        except (ValueError,KeyError,TypeError,IndexError): damages.append(name)
        else: raise ValueError('corrupted positive accepted: '+name)
    m.need(inventory(entries[:-1])['sha256'] != inv['sha256'], 'omitted inventory record was invisible')
    try: inventory(entries+[deepcopy(entries[-1])])
    except ValueError: damages.append('duplicate-inventory-record')
    else: raise ValueError('duplicate positive inventory accepted')
    damages.append('omitted-inventory-record')
    out = dict(status='COMPLETE_FROZEN_P4_CHECK',comparison={k:receipt[k] for k in fields},
               positive_inventory=inv,saturation=frozen['saturation']['counts'],
               controls=controls(),damage_controls=damages)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=out['status'],positive_inventory=inv,damage_controls=damages,
                         seconds=time.monotonic()-started,
                         peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)),flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    main(ap.parse_args())
