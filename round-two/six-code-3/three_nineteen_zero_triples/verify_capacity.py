"""Small solver-free checker for nonnegative integer triple-cover weights."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def check(ok,message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()


def sha(value):
    return hashlib.sha256(encode(value)).hexdigest()


def check_one(core,certificate):
    masks=core['blocks']
    check(len(masks)==len(set(masks))==42,'capacity core cardinality')
    check(all(type(b) is int and 0<=b<(1 << 18) for b in masks),'capacity mask domain')
    words=[frozenset(i for i in range(18) if b & (1 << i)) for b in masks]
    check(all(len(w)==5 for w in words),'capacity word size')
    covered=[frozenset(t) for w in words for t in combinations(sorted(w),3)]
    check(len(covered)==len(set(covered))==420,'capacity core repeats triple')
    check(all(sum(c in w for w in words)==19 for c in (15,16,17)),'finished center degree')
    check(all(sum(a in w and b in w for w in words)==5
              for a,b in combinations((15,16,17),2)),'center-pair multiplicity')
    check(not any({15,16,17}<=w for w in words),'center triple is covered')
    check(certificate['core_sha256']==core['core_sha256']==sha(sorted(masks)),
          'capacity core binding')
    denominator=certificate['denominator']
    check(type(denominator) is int and 0<denominator<=1000000,'denominator domain')
    weights={}
    forbidden=set(covered)
    for row in certificate['weights']:
        check(type(row) is list and len(row)==4,'weight row shape')
        a,b,c,weight=row
        check(all(type(i) is int for i in row),'weight integer domain')
        check(0<=a<b<c<15 and weight>0,'weight sign or label domain')
        t=frozenset((a,b,c))
        check(t not in weights and t not in forbidden,'duplicate or covered weighted triple')
        weights[t]=weight
    candidates=[]
    for q in combinations(range(15),5):
        residual=frozenset(q)
        if all(len(residual&w)<=2 for w in words):
            candidates.append(q)
            coverage=sum(weights.get(frozenset(t),0) for t in combinations(q,3))
            check(coverage>=denominator,'residual word is not covered by weights')
    check(len(candidates)==certificate['candidate_count'],'capacity candidate count')
    check(sha(candidates)==certificate['candidate_sha256'],'whole residual universe checksum')
    total=sum(weights.values())
    check(type(certificate['numerator']) is int and total==certificate['numerator'],
          'capacity weight sum')
    check(denominator==1000 and total<=20556,'uniform integer inequality')
    check(total//denominator<=20,'certificate does not prove the stated bound')
    return {'core_sha256':core['core_sha256'],'candidate_count':len(candidates),
            'weight_rows':len(weights),'numerator':total,'denominator':denominator,
            'additional_bound':total//denominator}


def run(work,certificate_path=HERE/'capacity.json'):
    cores=[j for k in range(6) for j in json.loads((work/f'joints-{k}.json').read_text())]
    source=json.loads(certificate_path.read_text())
    check(source['status']=='COMPLETE','capacity discovery incomplete')
    certificates=source['certificates']
    check(len(cores)==len(certificates)==226,'capacity coverage count')
    check(len({c['core_sha256'] for c in cores})==226,'duplicate core')
    lookup={c['core_sha256']:c for c in certificates}
    check(len(lookup)==len(certificates) and set(lookup)=={c['core_sha256'] for c in cores},
          'capacity certificate coverage')
    records=[check_one(c,lookup[c['core_sha256']]) for c in cores]
    result={'status':'COMPLETE_EXACT','cores':len(records),
            'candidate_count_range':[min(r['candidate_count'] for r in records),
                                     max(r['candidate_count'] for r in records)],
            'additional_bound_census':dict(sorted(Counter(r['additional_bound'] for r in records).items())),
            'maximum_total_bound':42+max(r['additional_bound'] for r in records),
            'certificate_sha256':hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
            'record_sha256':sha(records)}
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--certificate',type=Path,default=HERE/'capacity.json')
    args=parser.parse_args()
    run(args.work,args.certificate)
