"""Join the standard four range audits; hashes do not replace DRAT checking."""
import argparse
from collections import Counter
import json
from pathlib import Path

from evidence import COUNT, DOMAIN_SHA256, atomic_json, blocks, load_domain


def merge(domain, parts):
    parts=sorted(parts,key=lambda p:p['start'])
    cursor=0
    for p in parts:
        if (p['start']!=cursor or p['stop']<=p['start'] or p['stop']>COUNT
            or p['verified_records']!=p['stop']-p['start']
            or p['domain_sha256']!=DOMAIN_SHA256
            or p['status'] not in ('PARTIAL_CORPUS_AUDITED','COMPLETE_CERTIFICATE_CORPUS_AUDITED')):
            raise ValueError('range audits overlap, omit cases, or describe incompatible evidence')
        cursor=p['stop']
    if cursor!=COUNT:
        raise ValueError('range audits do not cover the complete family')
    joined=[b for p in parts for b in p['blocks']]
    if [(b['start'],b['stop']) for b in joined]!=blocks(0,COUNT):
        raise ValueError('unexpected digest block coverage')
    if any(b['count']!=b['stop']-b['start'] for b in joined):
        raise ValueError('incorrect digest block count')
    counts=[sum(p['counts_by_type'][i] for p in parts) for i in range(20)]
    expected=Counter(r['type'] for r in domain)
    if counts!=[expected[i] for i in range(20)]:
        raise ValueError('typed coverage differs from the verified domain')
    checker_counts=Counter()
    for p in parts:checker_counts.update(p['checker_counts'])
    hardest=max((p['maximum_conflicts'],p['hardest_index']) for p in parts)
    return {
        'status':'COMPLETE_CERTIFICATE_CORPUS_AUDITED','complete_family':True,
        'start':0,'stop':COUNT,'verified_records':COUNT,'domain_sha256':DOMAIN_SHA256,
        'proof_format':'binary DRAT','proofs_rechecked_by_this_audit':False,
        'hash_rule':parts[0]['hash_rule'],'blocks':joined,
        'proof_bytes':sum(b['proof_bytes'] for b in joined),
        'checker_counts':dict(sorted(checker_counts.items())),
        'counts_by_type':counts,'maximum_conflicts':hardest[0],'hardest_index':hardest[1],
        'clause_range':[min(p['clause_range'][0] for p in parts),max(p['clause_range'][1] for p in parts)],
        'summed_solver_seconds':sum(p['summed_solver_seconds'] for p in parts),
        'summed_solver_checker_seconds':sum(p['summed_solver_checker_seconds'] for p in parts),
        'range_audits':[{'start':p['start'],'stop':p['stop']} for p in parts],
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--domain',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('audits',type=Path,nargs='+')
    args=parser.parse_args()
    result=merge(load_domain(args.domain),[json.loads(p.read_text()) for p in args.audits])
    atomic_json(args.out,result)
    print(json.dumps({k:v for k,v in result.items() if k!='blocks'},indent=2))


if __name__=='__main__':main()
