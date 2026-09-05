#!/usr/bin/env python3
"""Canonical necessary selector after the four proved omissions."""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def instance(old):
    card=load('prefix_threshold',REPO/'hadwiger_nelson_parts509_degree7_extension610/cardinality.py')
    family=[set(row['D']) for row in old['family']]
    minimal=[i for i,D in enumerate(family) if not any(E<D for E in family)]
    free=old['free'];mapping={v:i+1 for i,v in enumerate(free)}
    b=card.Builder(len(free))
    hitting=[i for i in minimal if i not in [245,316]]
    for i in hitting:b.clause(*(mapping[v] for v in sorted(family[i])))
    for v in [13,24,129,518]:b.clause(-mapping[v])
    b.clause(b.neg(b.threshold(list(mapping.values()),57)))
    cnf=b.dimacs()
    meta=dict(free_vertices=free,omitted_vertices=[13,24,129,518],missing_rows=[245,316],
              hitting_rows=hitting,maximum_free_vertices=56,variables=b.variables,
              clauses=len(b.rows),cnf_sha256=sha256(cnf).hexdigest())
    return cnf,meta


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cnf-out',type=Path,required=True)
    ap.add_argument('--meta-out',type=Path);args=ap.parse_args()
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    cnf,meta=instance(old);args.cnf_out.write_bytes(cnf)
    if args.meta_out:args.meta_out.write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n')
    print(json.dumps(meta,indent=2,sort_keys=True))


if __name__=='__main__':main()
