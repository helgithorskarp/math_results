"""Optional public comparison to the pinned producer's quantitative record."""
import argparse
import hashlib
import json
from pathlib import Path
import check as own

HERE=Path(__file__).resolve().parent
PIN='912305f5e88e747ebaffebf5d0b2446ab33ba118e351c9fe5ad8610190ae5060'


def compare(data):
    own.need(hashlib.sha256(data).hexdigest()==PIN,'pinned producer expected bytes')
    native=json.loads(data);result=json.loads((HERE/'expected.json').read_text())
    labels=json.loads((HERE/'../mirror-rigidity-audit/inputs.json').read_text())['author_label_to_independent']
    fields=[('moment_excess_planar_trace','moment_trace'),('moment_excess_planar_determinant','moment_determinant'),
            ('minimum_nonequatorial_boundary_height_squared','height2'),
            ('minimum_equatorial_separation_squared','separation2'),('basis_Gram_determinant','basis_gram_determinant')]
    for a,b in zip(native['singleton_profiles'],result['singleton_profiles']):
        own.need(a['axis']==b['axis'] and sorted(labels[i] for i in a['equatorial_original_indices'])==b['singletons'],
                 'actual four-original profiles')
        for left,right in fields:own.need(own.C.scalar(a[left])==own.C.scalar(b[right]),'physical singleton scalar')
    own_maps={(x['source_axis'],x['receiver_axis'],tuple(zip(x['source_indices'],x['target_indices'])),x['catalogue_index'])
              for x in result['correspondence']['isometries']}
    native_maps=set()
    for a in native['Gram_catalogue']['isometries']:
        q=native['singleton_profiles'][a['source_axis']]['equatorial_original_indices']
        pairs=tuple(sorted((labels[i],labels[j]) for i,j in zip(q,a['target_original_ordering'])))
        native_maps.add((a['source_axis'],a['receiver_axis'],pairs,a['catalogue_index']))
    own.need(native_maps==own_maps and len(own_maps)==22,'complete actual marked correspondence')
    return {'physical_singleton_scalars':30,'actual_correspondence_records':22}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('producer_expected',type=Path);args=parser.parse_args()
    print('PASS',json.dumps(compare(args.producer_expected.read_bytes()),sort_keys=True))
