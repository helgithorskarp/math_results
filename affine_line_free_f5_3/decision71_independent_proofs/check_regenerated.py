"""Independently check new proof traces for the fixed 109,676-case domain.

New valid traces need not have the historical proof hashes. This driver
does not compare those hashes and does not reuse old acceptance records.
It freshly checks every requested case. Only the complete default range
can produce complete_family=true; partial ranges are diagnostic only.
For resumable replay of the archived original corpus use check_saved.py.
"""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import time

import check_saved as review


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--domain',type=Path,required=True)
    p.add_argument('--corpus',type=Path,required=True)
    p.add_argument('--checker',type=Path,required=True)
    p.add_argument('--checker-source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--start',type=int,default=0)
    p.add_argument('--stop',type=int,default=review.COUNT)
    a=p.parse_args();begun=time.monotonic()
    review.need(review.sha(a.domain.read_bytes())==review.DOMAIN_SHA,'domain provenance')
    review.need(review.sha(a.checker_source.read_bytes())==review.SOURCE_SHA,'stock checker source')
    review.need(0<=a.start<a.stop<=review.COUNT,'range')
    domain=json.loads(a.domain.read_text())
    review.need(len(domain)==review.COUNT,'complete domain')
    formula=review.Formula();types=Counter()
    cnfs=hashlib.sha256();proofs=hashlib.sha256();logs=hashlib.sha256()
    proof_bytes=0;native_seconds=0;verified=0
    for i in range(a.start,a.stop):
        # This regenerates the whole formula, compares actual CNF bytes,
        # binds the proof to its record, then runs the unmodified checker.
        # It never tests the regenerated proof against a historical digest.
        record=review.check_case(i,domain,a.corpus,a.checker.resolve(),formula)
        cnfs.update(bytes.fromhex(record['cnf_sha256']))
        proofs.update(bytes.fromhex(record['proof_sha256']))
        logs.update(bytes.fromhex(record['log_sha256']))
        proof_bytes+=record['proof_bytes'];native_seconds+=record['checker_seconds']
        types[record['type']]+=1;verified+=1
        if verified%1000==0:
            print(json.dumps({'freshly_verified':verified,'next_index':i+1,
                              'complete_family':False,'seconds':time.monotonic()-begun}),flush=True)
    review.need(verified==a.stop-a.start,'complete requested range')
    complete=a.start==0 and a.stop==review.COUNT
    result={'status':'INDEPENDENT_REGENERATED_PROOFS_COMPLETE_RANGE_VERIFIED',
            'start':a.start,'stop':a.stop,'verified':verified,'complete_family':complete,
            'all_formulas_independently_reconstructed':True,
            'ordered_cnf_hashes_sha256':cnfs.hexdigest(),
            'ordered_proof_hashes_sha256':proofs.hexdigest(),
            'ordered_new_log_hashes_sha256':logs.hexdigest(),
            'proof_bytes':proof_bytes,'type_counts':dict(types),
            'domain_sha256':review.DOMAIN_SHA,'checker_source_sha256':review.SOURCE_SHA,
            'checker_sha256':review.sha(a.checker.read_bytes()),
            'core_source_sha256':review.sha(Path(review.__file__).read_bytes()),
            'driver_source_sha256':review.sha(Path(__file__).read_bytes()),
            'historical_proof_hashes_required':False,'reused_native_checks':0,
            'summed_native_checker_seconds':native_seconds,'seconds':time.monotonic()-begun}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    review.atomic(a.out,result)
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
