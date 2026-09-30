"""Solver-free RUP and optional exact full-formula membership checking.

Author/executing agent: six-sorting-2, researcher. Watched implementation
is reused with credit from six-sorting-1/source5ad75ecb/7452. Membership
checking continues own7356's reference derived from peer7306/sourcea65309eb.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time

from watched_rup import WatchedRUP, replay, self_check

HERE=Path(__file__).resolve().parent


def clauses(path):
    with path.open() as stream:
        head=stream.readline().split();assert head[:2]==['p','cnf']
        n,count=map(int,head[2:]);rows=[]
        for line in stream:
            values=list(map(int,line.split()))
            assert values and values[-1]==0 and all(0<abs(v)<=n for v in values[:-1])
            rows.append(tuple(sorted(set(values[:-1]))))
    assert len(rows)==count
    return n,rows


def source_membership(core,path,expected):
    needed=set(core);digest=hashlib.sha256();count=0
    with path.open('rb') as stream:
        head=stream.readline();digest.update(head)
        assert head.decode().strip()==f"p cnf {expected['variables']} {expected['clauses']}"
        for line in stream:
            digest.update(line);count+=1
            values=list(map(int,line.split()));assert values[-1]==0
            needed.discard(tuple(sorted(set(values[:-1]))))
    assert not needed and count==expected['clauses']
    assert digest.hexdigest()==expected['sha256']
    return count


def main():
    if not __debug__:raise RuntimeError('Run without -O')
    parser=argparse.ArgumentParser();parser.add_argument('--full',type=Path)
    args=parser.parse_args();start=time.monotonic()
    cert=json.loads((HERE/'certificate.json').read_text())
    corepath=HERE/'core.cnf';proofpath=HERE/'proof.rup'
    assert hashlib.sha256(corepath.read_bytes()).hexdigest()==cert['core_sha256']
    assert hashlib.sha256(proofpath.read_bytes()).hexdigest()==cert['rup_sha256']
    controls=self_check();n,core=clauses(corepath)
    assert n==cert['cnf']['variables'] and len(core)==cert['core_clauses']
    assert not WatchedRUP(n,core).entails_by_rup(())
    additions,deletions=replay(n,core,proofpath)
    assert additions==cert['proof_additions'] and deletions==0
    count=source_membership(core,args.full,cert['cnf']) if args.full else None
    print(json.dumps(dict(agent='six-sorting-2',role='researcher',status='RUP_VERIFIED',
                          core_clauses=len(core),proof_additions=additions,tiny_truth_controls=controls,
                          full_source_membership_verified=bool(args.full),full_cnf_clauses_checked=count,
                          premature_empty_rejected=True,seconds=time.monotonic()-start,
                          peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                          trust_boundary='Sequential encoder and mathematical marker/coverage bridges are checked separately')))


if __name__=='__main__':main()
