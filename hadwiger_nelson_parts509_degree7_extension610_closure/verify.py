#!/usr/bin/env python3
"""Close the fixed extension using four disjoint sets and a 19-byte RUP."""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import rup

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
BASE=REPO/'hadwiger_nelson_parts509_degree7_extension610'


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def compute():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    for name,key in [('certificate.json','certificate_sha256'),('residual.rup','rup_sha256')]:
        require(sha256((HERE/name).read_bytes()).hexdigest()==manifest[key],('certificate hash',name))

    # This replays exact geometry and all 875 positive witnesses. Its old PB
    # bound and mathematical reduction remain explicit imported theorems.
    sys.path.insert(0,str(BASE))
    try:
        spec=importlib.util.spec_from_file_location('lifting_verifier',BASE/'verify.py')
        lifting=importlib.util.module_from_spec(spec);spec.loader.exec_module(lifting)
        facts,_,cnf,_=lifting.compute()
    finally:
        sys.path.pop(0)
    require(facts==json.loads((BASE/'expected.json').read_text()),'imported positive replay')
    require(sha256(cnf).hexdigest()==manifest['residual_cnf_sha256'],'residual formula hash')

    # A direct combinatorial refutation, independent of threshold variables
    # and of the solver's proof format.
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    lift=json.loads((BASE/'certificate.json').read_text())
    meta=json.loads((BASE/'residual_instance.json').read_text())
    cert=json.loads((HERE/'certificate.json').read_text())
    require(meta['fixed_omitted_original_vertices']==cert['fixed_omitted_originals']==[15,23],
            'fixed missing original vertices')
    require(meta['fixed_added_point']==610 and meta['exact_additions']==3,'residual support')
    require(cert['maximum_selected_old_pool_points']==meta['exact_additions'],'pool quota')
    groups=[]
    for i in cert['killing_rows']:
        require(0<=i<len(old['family']) and i not in lift['excluded_killing_indices'],
                ('unverified killing row',i))
        D=set(old['family'][i]['D'])
        remaining=D-set(cert['fixed_omitted_originals'])
        require(remaining and remaining<=set(old['pool']),('pool-only requirement',i))
        groups.append(sorted(remaining))
    require(groups==cert['required_pool_groups'],'displayed pool groups')
    require(sum(map(len,groups))==len(set().union(*map(set,groups))),
            'required pool groups are not pairwise disjoint')
    require(len(groups)==cert['minimum_required_old_pool_points']>meta['exact_additions'],
            'no cardinality contradiction')

    # Addition-only reverse unit propagation independently verifies the SAT
    # refutation. No native solver or proof checker is needed for this replay.
    variables,rows=rup.parse_dimacs(cnf)
    proof=[rup.parse_clause(line,variables) for line in (HERE/'residual.rup').read_text().splitlines()]
    additions=rup.check(rows,proof)
    result=dict(status='CLOSED THROUGH 508; MINIMUM FIVE-CHROMATIC SUBGRAPH ORDER 509',
                host_vertices=facts['vertices'],host_unit_edges=facts['unit_edges'],
                exact_geometry_and_positive_witnesses_replayed=True,
                positive_witnesses=facts['forced_vertices_verified']+facts['killing_sets_verified'],
                disjoint_killing_rows=cert['killing_rows'],disjoint_required_pool_groups=groups,
                required_old_pool_points=len(groups),allowed_old_pool_points=meta['exact_additions'],
                direct_disjoint_set_refutation=True,residual_cnf_sha256=sha256(cnf).hexdigest(),
                residual_variables=variables,residual_clauses=len(rows),
                rup_additions=additions,rup_bytes=(HERE/'residual.rup').stat().st_size,
                rup_sha256=manifest['rup_sha256'],rup_verified=True,
                minimum_five_chromatic_subgraph_order=509,record_improvement=False,
                imported_degree7_PB_bound_rechecked=False,
                imported_reduction_contribution=manifest['imported_reduction_contribution'])
    return result,cnf


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cnf-out',type=Path)
    ap.add_argument('--drat-trim',type=Path);args=ap.parse_args()
    result,cnf=compute()
    require(result==json.loads((HERE/'expected.json').read_text()),'expected result differs')
    if args.cnf_out:
        args.cnf_out.write_bytes(cnf)
    if args.drat_trim:
        with tempfile.TemporaryDirectory(prefix='extension610-rup-') as directory:
            path=Path(directory)/'residual.cnf';path.write_bytes(cnf)
            check=subprocess.run([str(args.drat_trim.resolve()),str(path),str(HERE/'residual.rup'),'-U'],
                                 capture_output=True,text=True)
        require(check.returncode==0 and 's VERIFIED' in check.stdout,'external RUP check rejected')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
