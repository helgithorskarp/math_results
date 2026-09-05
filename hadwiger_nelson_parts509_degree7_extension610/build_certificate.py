#!/usr/bin/env python3
"""Pack four fixed repair-query results into the compact lifted certificate."""
import argparse
import json
from pathlib import Path
from verify import geometry, proper, require, REPO


def compute(repairs):
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    vertices,edges,_,_,_=geometry(old)
    neighbours=[a for a,b in edges if b==610]
    queries={(r['kind'],r['key']):r for r in repairs['queries']}
    replacements=[]

    def lift(kind,key,D,witness):
        colours=dict(zip([v for v in old['vertices'] if v not in D],witness,strict=True))
        available=set('0123')-{colours[v] for v in neighbours if v in colours}
        if available:
            colour=min(available)
            proper(vertices,edges,D,witness+colour)
            return colour
        if (kind,key)==('kill','188'):
            return '.'  # No native negative answer is accepted here as a proof.
        row=queries[kind,key]
        require(row['D']==D and row['status']=='SAT','repair query mismatch')
        proper(vertices,edges,D,row['witness'])
        replacements.append(dict(kind=kind,key=key,witness=row['witness']))
        return '.'

    forced=''.join(lift('forced',str(v),[v],old['forced_witness'][str(v)]) for v in old['forced'])
    killing=''.join(lift('kill',str(i),row['D'],row['witness']) for i,row in enumerate(old['family']))
    base=queries['forced','44']['witness']
    five=base[:44]+'4'+base[44:]
    proper(vertices,edges,[],five,'01234')
    return dict(added_point=610,neighbors_of_added_point=neighbours,
                forced_append=forced,killing_append=killing,
                replacement_witnesses=sorted(replacements,key=lambda r:(r['kind'],r['key'])),
                excluded_killing_indices=[188],five_colouring=five,
                non_four_colourable_deletion=[15,23])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repairs',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    result=compute(json.loads(args.repairs.read_text()))
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':main()
