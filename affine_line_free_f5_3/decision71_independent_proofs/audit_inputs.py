"""Audit every published input with the reviewer's independent point geometry.

This never infers UNSAT from author logs, record labels, or proof digests.
Native proof checking is a separate obligation in check_saved.py.
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import json
import time

import check_saved as review


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--domain',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--corpus',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--workers',type=int,default=8)
    a=p.parse_args();begun=time.monotonic()
    review.need(1<=a.workers<=32,'worker count')
    review.need(review.sha(a.domain.read_bytes())==review.DOMAIN_SHA,'domain provenance')
    review.need(review.sha(a.manifest.read_bytes())==review.MANIFEST_SHA,'manifest provenance')
    domain=json.loads(a.domain.read_text());manifest=json.loads(a.manifest.read_text())
    review.need(len(domain)==review.COUNT,'domain count')
    blocks=manifest['blocks']
    review.need(blocks[0]['start']==0 and blocks[-1]['stop']==review.COUNT
                and all(b['stop']==c['start'] for b,c in zip(blocks,blocks[1:])),
                'published complete index cover')
    formula=review.Formula();types=Counter();summaries=[]
    # Formula is immutable; every construction and file read is case-local.
    # executor.map returns results in input order, regardless of I/O timing.
    def one(i):return review.case_input(i,domain,a.corpus,formula)[2]
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        for block in blocks:
            records=list(pool.map(one,range(block['start'],block['stop'])))
            types.update(r['type'] for r in records)
            review.validate_records(records,block,domain)
            summaries.append(block)
            print(json.dumps({'input_audit_next_index':block['stop'],
                              'seconds':time.monotonic()-begun}),flush=True)
    review.need(sum(types.values())==review.COUNT
                and [types[i] for i in range(20)]==manifest['counts_by_type'],
                'complete type cover')
    result={'status':'COMPLETE_INDEPENDENT_FORMULA_AND_INPUT_AUDIT_PASSED',
            'independently_reconstructed_formulas':review.COUNT,
            'matched_stored_cnf_bytes':review.COUNT,
            'author_record_integrity_checks':review.COUNT,
            'fresh_native_proof_checks_in_this_audit':0,
            'global_unsat_accepted':False,
            'lines_constructed_from_point_pairs':len(formula.lines),
            'counts_by_type':[types[i] for i in range(20)],
            'checked_manifest_blocks':len(blocks),
            'proof_bytes_hashed':sum(b['proof_bytes'] for b in blocks),
            'domain_sha256':review.DOMAIN_SHA,'author_manifest_sha256':review.MANIFEST_SHA,
            'formula_source_sha256':review.sha(Path(review.__file__).read_bytes()),
            'audit_source_sha256':review.sha(Path(__file__).read_bytes()),
            'seconds':time.monotonic()-begun,'io_workers':a.workers,'blocks':summaries}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    review.atomic(a.out,result)
    print(json.dumps({k:v for k,v in result.items() if k!='blocks'},indent=2),flush=True)


if __name__=='__main__':main()
