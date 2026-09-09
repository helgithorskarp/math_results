"""Reject altered tiny-core/deletion certificates; restore every scratch byte."""
from array import array
from pathlib import Path
import argparse
import hashlib
import json
import struct
import sys
import check_census

def run(cache,out):
    out=Path(out);rejected=[]
    def attempt(name,path,offset,replacement,check):
        before=hashlib.sha256(path.read_bytes()).hexdigest()
        with path.open('r+b') as f:
            f.seek(offset);saved=f.read(len(replacement));f.seek(offset);f.write(replacement)
        try:
            try:check()
            except ValueError:rejected.append(name)
            else:raise RuntimeError('accepted corrupted certificate: '+name)
        finally:
            with path.open('r+b') as f:f.seek(offset);f.write(saved)
        check_census.require(hashlib.sha256(path.read_bytes()).hexdigest()==before,'scratch restoration')
    tables=out/'tables'
    attempt('false-positive-empty-core',tables/'owners7.bin',0,struct.pack('<h',0),
            lambda:check_census.exhaustive_lookup(cache,tables,7))
    raw=(tables/'owners7.bin').read_bytes();owners=array('h');owners.frombytes(raw)
    if sys.byteorder!='little':owners.byteswap()
    first=next(i for i,x in enumerate(owners) if x>=0)
    attempt('out-of-range-core-permutation',tables/'perms7.bin',2*first,struct.pack('<H',65535),
            lambda:check_census.exhaustive_lookup(cache,tables,7))
    path=out/'deletions11.bin'
    attempt('wrong-source-core',path,0,struct.pack('<I',1),lambda:check_census.audit_deletions(cache,out,11))
    attempt('wrong-destination-core',path,5,struct.pack('<H',65535),lambda:check_census.audit_deletions(cache,out,11))
    first_record=path.read_bytes()[:14]
    attempt('duplicate-destination-position',path,7,first_record[8:9],lambda:check_census.audit_deletions(cache,out,11))
    return {'status':'CORE_CERTIFICATE_CORRUPTIONS_REJECTED','rejected':rejected,'count':len(rejected)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('out');args=p.parse_args()
    print(json.dumps(run(args.cache,args.out),sort_keys=True))
