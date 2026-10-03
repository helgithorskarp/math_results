"""Whole-entry comparison of two distinct finite inventory algorithms."""
import hashlib
import json
import argparse
from pathlib import Path

import model
import physical


def run(out=None):
    producer = model.build()
    counts,types,low_rows,budget,matrices,census,domains,raw = physical.build()
    physical.require(producer['counts']==counts and producer['types']==types
        and producer['budget']==budget, 'Inventories differ in exact scope')
    physical.require(producer['matrices']==matrices, 'Entire canonical matrix lists differ')
    physical.require({k:list(v) for k,v in producer['domains'].items()}==domains,
                     'Entire high-star inventories differ')
    physical.require(producer['raw_stars']==raw, 'Raw subset census differs')
    whole = dict(matrices=matrices,domains=[[x,c,list(r)] for (x,c),r in sorted(domains.items())])
    encoded = json.dumps(whole,sort_keys=True,separators=(',',':')).encode()
    if out is not None:
        out.write_bytes(encoded)
    return dict(agent='six-books-3',role='researcher',
        status='WHOLE_DISTINCT_INVENTORIES_EQUAL', counts=counts, types=list(types),
        mixed_row_budgets=budget, producer_matrix_census=producer['matrix_census'],
        producer_inventory_work_units=producer['inventory_work_units'],
        physical_matrix_census=census, matrices=len(matrices), raw_stars=raw,
        stored_stars=sum(len(r) for r in domains.values()),
        whole_inventory_bytes=len(encoded),whole_inventory_sha256=hashlib.sha256(encoded).hexdigest())


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path)
    print(json.dumps(run(parser.parse_args().out),sort_keys=True,separators=(',',':')))
