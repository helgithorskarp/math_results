"""Portable entry for the already checked43-word lower supply; no new domain."""
from pathlib import Path
import argparse
from fractions import Fraction
import hashlib
import json
import os
import resource
import sys
import time

from check_seed43_mass864_v1 import shape, all_boxes

ROOT=Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')

def fp(path):
    raw=Path(path).read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def main(out):
    assert not out.exists(),'Use a fresh output path; no hidden overwrite or retry'
    assert all(os.environ.get(k)=='1' for k in THREADS),'one native thread'
    original=ROOT/'check_seed43_mass864_v1.py'
    assert fp(original)=={'bytes':6385,'sha256':'769c68b3680246f90f9de7a363ef14a257045cc18a5759008181199f667be66c'}
    seed=ROOT/'seed43.txt'
    assert fp(seed)=={'bytes':607,'sha256':'4809641cdfbe02fa33b1ed49d68eed6bfa5fee3854821666c414b1fdc666a4e8'}
    reference=ROOT/'evidence/all43_seed_membership_v1.ndjson'
    assert fp(reference)=={'bytes':5107,'sha256':'bef94fd6d7f955914196dc811d893f6fe67939d783cd2024fa58e4a2e460dd61'}
    lines=seed.read_text().splitlines()
    assert lines[0]=='7 43' and len(lines)==44
    words=[tuple(map(int,line.split())) for line in lines[1:]]
    assert len(set(words))==43 and all(sorted(w)==list(range(1,8)) for w in words)
    expected=[json.loads(line) for line in reference.read_text().splitlines()]
    assert len(expected)==43
    started=time.monotonic();out.mkdir();rows=[];quadruples=0
    try:
        for i,word in enumerate(words):
            assert time.monotonic()-started<10,'internal10s cap; incomplete is failure'
            height,leaves=shape(word);boxes,count=all_boxes(word)
            assert height==3 and not boxes
            row={'kind':'input_words','record':{'index':i,'word':list(word),
              'leaf_value_set':sorted(leaves),'full_literal_boxes':boxes}}
            assert row==expected[i],('complete record mismatch',i)
            rows.append(row);quadruples+=count
        assert quadruples==1505
        wire=b''.join((json.dumps(row,sort_keys=True,separators=(',',':'))+'\n').encode() for row in rows)
        assert wire==reference.read_bytes()
        bases=((1,3,2),(2,3,1))
        family=sorted(tuple(3+x for x in a)+(7,)+b for a in bases for b in bases)
        assert len(set(family))==4 and all(w in words for w in family)
        bad=Fraction(4,43)**2;good=1-bad
        assert bad==Fraction(16,1849) and good==Fraction(1833,1849)
        assert time.monotonic()-started<10,'internal10s cap'
        seconds=time.monotonic()-started;rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        cert=out/'all43_seed_membership_v1.ndjson'
        with cert.open('xb') as f:f.write(wire)
        report={'status':'complete exact43-word lower-supply portability replay',
          'existing_seed_words':43,'quadruples_visited':1505,'all43_record_fields_equal':True,
          'certificate':fp(cert),'bad_mass_upper_h3':[bad.numerator,bad.denominator],
          'complement_mass_lower_h3':[good.numerator,good.denominator],
          'original_mathematical_source':fp(original),'portable_entry':fp(Path(__file__)),
          'python':sys.version.split()[0],'native_threads':1,'processes':1,
          'thread_environment':{k:os.environ[k] for k in THREADS},'internal_cap_seconds':10,
          'seconds_before_report_serialization':seconds,'peak_RSS_KiB_before_report_serialization':rss,
          'seed_completeness_proved_by_this_check':False,'new_input_domain_generated':False,
          'old_census_DP_or_pair_table_replayed':False,'full_target_solved':False}
        with (out/'report.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
        print(json.dumps(report,sort_keys=True))
    except Exception as e:
        with (out/'FIRST_FAILURE.json').open('x') as f:json.dump({'type':type(e).__name__,'message':str(e)},f,indent=2);f.write('\n')
        raise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);args=p.parse_args();main(Path(args.out))
