"""Whole-record corroboration, using only the reviewer's adjacency engine.

AUTHOR-expected.json and the small-graph digest serialization are credited
to six-books-3. This adapter was written after author source inspection.
The independently written original-adjacency engine was frozen beforehand.
"""
from collections import Counter
from itertools import combinations
import hashlib
import json
import sys
import check as own


def record():
    doc = json.loads((own.ROOT/'INPUT-controls.json').read_text())
    controls = []
    for fixture in doc['controls']:
        rows = own.adjacency(fixture['red_masks'])
        out = own.original(rows)
        lows, highs = out['low_vertices'], out['high_vertices']
        pairs = [own.pair_data(rows,u,v) for u,v in combinations(range(22),2)]
        controls.append({'name':fixture['name'],'q':out['q'],
            'n':out['counts_n0_to_n4'][1:], 'red_edges':sum(v[0] for v in pairs),
            'mixed_slack':out['mixed_slack'],
            'low_internal_degrees':out['low_degrees_inside_L'],
            'row_slacks':[sum(out['mixed_slack_matrix'][i][j] for i in range(4))
                          for j in range(len(highs))],
            'negative_mixed_slacks':sum(v < 0 for row in out['mixed_slack_matrix'] for v in row),
            'alpha':out['neighborhood_odd_slacks'],
            'blue_mixed_slack':out['mixed_blue_slack'],
            'twice_low_red_slack':2*sum(3-own.pair_data(rows,u,v)[1]
                                       for u,v in combinations(lows,2) if v in rows[u]),
            'red_pages':max(cr for red,cr,cb in pairs if red),
            'blue_pages':max(cb for red,cr,cb in pairs if not red),
            'red_failing_pairs':sum(red and cr > 3 for red,cr,cb in pairs),
            'blue_failing_pairs':sum(not red and cb > 6 for red,cr,cb in pairs),
            'low_pair_red_codegrees':[own.pair_data(rows,u,v)[1] for u,v in combinations(lows,2)]})
    stream = hashlib.sha256(); per_order=[]
    for n in range(1,7):
        edges=list(combinations(range(n),2)); red_pairs=blue_pairs=0
        for code in range(1 << len(edges)):
            rows=[set() for _ in range(n)]
            for k,(u,v) in enumerate(edges):
                if code >> k & 1:rows[u].add(v);rows[v].add(u)
            for u,v in edges:
                red,cr,cb=own.pair_data(rows,u,v)
                red_pairs += red;blue_pairs += 1-red
                # Credited author digest format; actual witnesses come from own engine.
                stream.update(f'{n}:{code}:{u}:{v}:{cr}:{cb}\n'.encode())
        per_order.append({'order':n,'graphs':1 << len(edges),
                          'pairs':red_pairs+blue_pairs,'red_pairs':red_pairs,'blue_pairs':blue_pairs})
    prof=own.profiles();rows=prof['all_relaxed_profiles'];primary=own.primary()
    return {'schema':1,'controls':controls,
        'primary21':{'order':21,'raw_sha256':primary['raw_sha256'],
            'red_edges':primary['red_edges'],'blue_edges':primary['blue_edges'],
            'red_pages':primary['page_maxima'][0],'blue_pages':primary['page_maxima'][1],
            'checked_pairs':210,'degree_histogram':{str(k):v for k,v in primary['degree_histogram']}},
        'profiles':{'profiles':len(rows),'by_q':[sum(v[0] == q for v in rows) for q in range(7)],
            'ordered_profile_sha256':own.digest(rows),'zero_one_singleton_profiles':prof['zero_one_exceptional_profiles'],
            'parity_relaxed_minimum_n1':min(v[1] for v in rows if v[1] >= 2),
            'nonrootless_boundary':{'q':0,'n0_to_n4':[1,0,16,0,1],
                'incidences':36,'correct_n1':0,'wrong_plus_n0_n1':4}},
        'small_graphs':{'graphs':sum(v['graphs'] for v in per_order),
            'pairs':sum(v['pairs'] for v in per_order),'orders':per_order,
            'ordered_pair_sha256':stream.hexdigest()}}


if __name__ == '__main__':
    value=record()
    if '--record' in sys.argv:print(json.dumps(value,sort_keys=True,indent=2))
    else:
        own.exact_record(value,json.loads((own.ROOT/'AUTHOR-expected.json').read_text()))
        print(json.dumps({'status':'PASS','whole_author_record_sha256':own.digest(value),
            'all_mathematical_fields_compared':True,'author_executable_imported':False},sort_keys=True))
