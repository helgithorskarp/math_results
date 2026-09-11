"""Independent integer, coverage, terminal and rational-certificate checks."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import csv
import hashlib
import json
import sys

SOURCE=Path(__file__).resolve().parent
PROFILE=SOURCE.parent/'p82_profiles'
sys.path.append(str(PROFILE))
from checks import digest,same,sidon,rows


def input_check(inputs):
    expected=json.loads((PROFILE/'validation.json').read_text())['hashes']
    result={}
    for name in ['orbit11.txt','full_0.bin','full_1.bin']:
        value=digest(inputs/name)
        assert value==expected[name],(name,value)
        result[name]=value
    same(inputs/'full_0.bin',inputs/'full_1.bin')
    assert (inputs/'full_0.bin').stat().st_size==172495800
    return result


def fractional_check(path):
    reports=[]
    for certificate in json.loads(path.read_text()):
        assert certificate['n']==82 and certificate['reflection_average']
        coverage=[Fraction(0)]*82;counts=Counter()
        for row in certificate['classes']:
            points=row['points'];k=row['k']
            assert points==sorted(set(points))and len(points)==k and all(0<=x<82 for x in points)
            assert sidon(points)
            value=Fraction(row['numerator'],row['denominator']);assert value>0
            counts[k]+=value
            for x in points:
                coverage[x]+=value/2
                coverage[81-x]+=value/2
        assert coverage==[1]*82 and counts==Counter(certificate['profile'])
        reports.append(dict(profile=certificate['profile'],positive_rows=len(certificate['classes']),exact_point_equalities=82,exact_class_multiplicities=True))
    return reports


def verify_run(work,inputs,jobs,minimum=0):
    weights=list(map(int,(PROFILE/'weights.txt').read_text().split()))
    orbit=rows(inputs/'orbit11.txt');all_rows=[];examples=[];terminal_count=0
    terminal_hash=hashlib.sha256();stream_bytes=0;records=0;options_audited=0;largest=0;shards=[]
    for shard in range(jobs):
        tables=[]
        for method in [0,1]:
            pre=work/f'global_{method}_{shard}'
            assert pre.with_suffix('.done').read_text()=='complete\n'
            report=json.loads(pre.with_suffix('.out').read_text());assert report['complete']and report['found']==0
            assert not pre.with_suffix('.err').read_text()
            table=[{k:int(v)for k,v in row.items()}for row in csv.DictReader(pre.with_suffix('.csv').open())]
            assert all(row['orbit']%jobs==shard and row['orbit']>=minimum for row in table)
            assert [row['orbit']for row in table]==sorted(set(row['orbit']for row in table),reverse=True)
            assert report['packings']==sum(row['packings']for row in table)
            assert all(0<=value<2**64 for row in table for value in row.values())
            assert all(a['trace_end']<=b['trace_end']and a['terminal_end']<=b['terminal_end']for a,b in zip(table,table[1:]))
            tables.append(table)
        assert tables[0]==tables[1]
        table=tables[0];all_rows+=table
        comparison=json.loads((work/f'global_pair_{shard}_comparison.json').read_text())
        audit=json.loads((work/f'global_pair_{shard}_comparison_audit.json').read_text())
        assert comparison['complete']and audit['verified']
        expected_bytes=table[-1]['trace_end']if table else 0
        assert comparison['compared_bytes']==audit['bytes']==expected_bytes
        assert audit['options']==sum(row['options']for row in table)
        assert audit['records']<=sum(row['queries']for row in table)
        stream_bytes+=expected_bytes;records+=audit['records'];options_audited+=audit['options'];largest=max(largest,audit['largest_option_list'])
        same(work/f'global_0_{shard}.jsonl',work/f'global_1_{shard}.jsonl')
        terminal_path=work/f'global_0_{shard}.jsonl'
        assert terminal_path.stat().st_size==(table[-1]['terminal_end']if table else 0)
        count=0
        with terminal_path.open('rb')as f:
            for line in f:
                terminal_hash.update(line);item=json.loads(line)
                ids=item['ids'];chosen=item['chosen'];last=item['residual']
                assert len(ids)==3 and ids==sorted(set(ids))and ids[0]%2==0 and (ids[0]//2)%jobs==shard
                assert all(0<=i<len(orbit)for i in ids)
                elevens=[orbit[i]for i in ids]
                assert len(chosen)==4 and all(len(a)==10 for a in chosen)and len(last)==9
                assert all(sidon(a)for a in elevens+chosen)and not item['sidon']and not sidon(last)
                assert sorted(x for a in elevens+chosen+[last]for x in a)==list(range(82))
                values=[sum(weights[x]for x in a)for a in chosen]
                assert values==sorted(values,reverse=True)and max(values)<=4000000
                assert sum(weights[x]for x in last)<=3776423
                if len(examples)<4:examples.append(item)
                count+=1
        assert count==sum(row['leaves']for row in table)
        terminal_count+=count
        shards.append(dict(shard=shard,comparison=comparison,audit=audit))
    all_rows.sort(key=lambda row:row['orbit'])
    expected=[{k:int(v)for k,v in row.items()}for row in csv.DictReader((PROFILE/'cases_3.csv').open())if int(row['orbit'])>=minimum]
    assert [(r['orbit'],r['packings'])for r in all_rows]==[(r['orbit'],r['packings'])for r in expected]
    keys=['packings','calls','queries','options','leaves','found']
    totals={k:sum(r[k]for r in all_rows)for k in keys}
    assert totals['found']==0 and totals['calls']==totals['packings']+totals['options']
    assert totals['leaves']==terminal_count and totals['options']==options_audited and max(totals.values())<2**64
    integer_call_bound=totals['packings']+stream_bytes//16
    assert totals['calls']<=integer_call_bound<2**64
    compact=[{k:r[k]for k in ['orbit']+keys}for r in all_rows]
    with (work/'cases_3_completed.csv').open('w')as f:
        writer=csv.DictWriter(f,fieldnames=['orbit']+keys,lineterminator='\n');writer.writeheader();writer.writerows(compact)
    (work/'terminal_examples.json').write_text(json.dumps(examples,indent=2)+'\n')
    return dict(verified=True,integer_call_bound=integer_call_bound,minimum_orbit=minimum,eligible_cases=len(all_rows),nonempty_cases=sum(r['packings']>0 for r in all_rows),totals=totals,exact_compared_bytes_per_method=stream_bytes,nonempty_query_records=records,largest_option_list=largest,terminal_checks=terminal_count,terminal_sha256_in_shard_order=terminal_hash.hexdigest(),cases_sha256=digest(work/'cases_3_completed.csv'),shards=shards)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);parser.add_argument('--inputs',type=Path,required=True);parser.add_argument('--jobs',type=int,default=3);parser.add_argument('--minimum',type=int,default=0);args=parser.parse_args()
    print(json.dumps(dict(inputs=input_check(args.inputs),verification=verify_run(args.work,args.inputs,args.jobs,args.minimum),fractional=fractional_check(SOURCE/'fractional_profiles.json')),indent=2))
