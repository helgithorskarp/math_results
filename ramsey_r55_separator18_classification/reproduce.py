#!/usr/bin/env python3
"""Replay exact evidence under both Python modes without writing generated state."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def main():
    lines=(HERE/'SHA256SUMS').read_text().splitlines()
    names=[]
    for line in lines:
        digest,name=line.split('  ',1)
        path=HERE/name
        if path.parent!=HERE or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise ValueError(('manifest mismatch',name))
        names.append(name)
    if len(names)!=len(set(names)):
        raise ValueError('duplicate manifest path')
    compared=[]
    for mode in ([],['-O']):
        for program,expected in (('derive.py','CERTIFICATE.json'),('check.py','INDEPENDENT.json'),('controls.py','CONTROLS.json'),('extract.py','fixture_certificate.json')):
            args=[sys.executable,*mode,'-B',str(HERE/program)]
            if program=='extract.py':args.append(str(HERE/'fixture.json'))
            result=subprocess.run(args,check=True,capture_output=True)
            if result.stderr or result.stdout!=(HERE/expected).read_bytes():
                raise ValueError(('replay mismatch',mode,program,result.stderr.decode()))
            compared.append([mode,program])
        result=subprocess.run([sys.executable,*mode,'-B',str(HERE/'verify_five.py'),str(HERE/'fixture.json'),str(HERE/'fixture_certificate.json')],check=True,capture_output=True)
        if json.loads(result.stdout)!={'status':'VERIFIED_LITERAL_FIVE','pairs_checked':10} or result.stderr:
            raise ValueError('literal certificate replay mismatch')
    print(json.dumps({'status':'REPRODUCED_SEPARATOR18_CLASSIFICATION','manifest_entries':len(names),'byte_equal_program_outputs':len(compared),'literal_certificate_checks':2,'good43_found':False},sort_keys=True))

if __name__=='__main__':main()
