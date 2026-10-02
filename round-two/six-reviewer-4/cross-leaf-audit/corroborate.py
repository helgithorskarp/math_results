#!/usr/bin/env python3
"""Later author-source replay, split at unchanged mathematical stage boundaries.

This is corroboration after the independent seal, not independent proof evidence.
Pass --author-dir pointing to the nine pinned target files documented in README.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
import sys
from reproduce import stage, require, canonical

def freeze(value):
    return tuple(freeze(v) for v in value) if isinstance(value, list) else value

def child(name, author, out):
    spec = importlib.util.spec_from_file_location('audited_author', author/'derive.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    def read(n):
        return freeze(json.loads((out/(n+'.json')).read_text()))
    if name == 'X':
        value = m.x_domain()[1]
    elif name == 'Y_endpoints':
        xs=read('X'); value=m.y_domain(xs,[m.known16(x) for x in xs])
    elif name == 'XY_rows':
        xs=read('X'); value=m.row_domain(read('Y_endpoints'),[m.known16(x) for x in xs])
    elif name == 'XY_joins':
        xs=read('X');value=m.join_domain(xs,read('Y_endpoints'),read('XY_rows'),[m.known16(x) for x in xs])
    elif name == 'red_books':
        xs=read('X');value=m.witnesses(xs,read('Y_endpoints'),read('XY_joins'),[m.known16(x) for x in xs])
    else:
        raise ValueError('unknown author stage')
    print(m.canonical(value))

def parent(author, out):
    out.mkdir(parents=True,exist_ok=True)
    timings={}
    for name in ['X','Y_endpoints','XY_rows','XY_joins','red_books']:
        run=stage([sys.executable,str(Path(__file__).resolve()),'--child',name,
                   '--author-dir',str(author),'--out',str(out)], author)
        (out/(name+'.json')).write_text(run['stdout'])
        timings[name]={k:v for k,v in run.items() if k!='stdout'}
    values={n:json.loads((out/(n+'.json')).read_text()) for n in ['X','Y_endpoints','XY_rows','XY_joins']}
    values['red_books'],tags=json.loads((out/'red_books.json').read_text())
    from itertools import product
    flags=[l for l in product(range(2),repeat=5) if sum(l)<=3]
    bytag=Counter((r,tuple(low)) for r,low,*_ in values['X'])
    coverage=[{'repeated_SX':r,'low_T0_T1_T2_SY0_SY1':l,'ordinary_Y_low_count':3-sum(l),
               'labeled_ordinary_Y_choices':comb(6,3-sum(l)),'X_interfaces':bytag[r,l]}
              for r in range(2) for l in flags]
    def digest(v):return hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest()
    record={'schema':1,'agent':'six-books-1','role':'researcher',
            'scope':'specified one-nine leaf; red degrees 9^4,10^18; cross-repeated omission',
            'normalized_repeated_SX_choices':2,'flag_words_per_core':len(flags),
            'labeled_low_placements_per_core':sum(comb(6,3-sum(l)) for l in flags),
            'tag_coverage':coverage,'canonical_ordered_SX_pairs':((15,51),(15,23)),
            'labeled_SX_pair_orbit_sizes':(90,120),
            'counts':{k:len(v) for k,v in values.items()},'domain_sha256':{k:digest(v) for k,v in values.items()},
            'domains':values,'join_tag_histogram':tags,'unblocked_partial_joins':len(values['XY_joins'])-len(values['red_books']),
            'internal_Y_edges_used_in_witnesses':0}
    content=(json.dumps(record,separators=(',',':'))+'\n').encode()
    summary={k:v for k,v in record.items() if k!='domains'}
    summary['red_book_witnesses']=values['red_books']
    require(canonical(summary)==canonical(json.loads((author/'EXPECTED.json').read_text())), 'author whole fixture differs')
    require(hashlib.sha256(content).hexdigest()=='8b39a65ce59cb832f1bd4f07b615fa2f2c3d43e625681a98ba5be041e180d4a4',
            'author entire record hash differs')
    (out/'author-full.json').write_bytes(content)
    receipt={'complete':True,'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),
             'original_functions_unmodified':True,'guard_seconds_per_stage':60,'runs':timings}
    (out/'receipt.json').write_bytes(canonical(receipt))
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--child');ap.add_argument('--author-dir',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    if a.child:child(a.child,a.author_dir.resolve(),a.out.resolve())
    else:parent(a.author_dir.resolve(),a.out.resolve())
