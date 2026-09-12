"""Endpoint checker: imports the preceding literal checker, never the producer."""
from pathlib import Path
from itertools import combinations
import argparse
import json
import sys
PREVIOUS = Path(__file__).resolve().parent.parent/'ramsey_r55_core_exchange_normal_form'
sys.path.insert(0,str(PREVIOUS))
from verify_destination import verify, matrix, require


def check(source, packet, data):
    require(packet['new_original_task_verdict'] is False,'verdict scope')
    if packet['status'] == 'MONOCHROMATIC_FIVE':
        a = matrix(source); bad = packet['physical_five_in_input_labels']; S=bad['vertices']; c=bad['color']
        require(len(S)==len(set(S))==5 and all(isinstance(v,int) and 0<=v<43 for v in S),'five-set')
        require(c in (0,1) and all(a[u][v]==c for u,v in combinations(S,2)),'literal five')
        return dict(status='PHYSICAL_MONOCHROMATIC_FIVE_VERIFIED',new_original_task_verdict=False)
    require(packet['status']=='GLOBAL_REDIRECT_NOT_ORIGINAL_TASK_UNSAT','redirect scope')
    result = verify(source,packet,data)
    r = len(packet['packing']['red']); q = r+len(packet['packing']['blue'])
    require(q!=7 or r==7,'excluded mixed q7 destination')
    return dict(result,status='REDUCED_COMPLETE_CARRIER_DESTINATION_VERIFIED')


if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('catalog_directory');p.add_argument('source');p.add_argument('packet')
    args=p.parse_args()
    print(json.dumps(check(json.loads(Path(args.source).read_text()),json.loads(Path(args.packet).read_text()),args.catalog_directory),sort_keys=True))
