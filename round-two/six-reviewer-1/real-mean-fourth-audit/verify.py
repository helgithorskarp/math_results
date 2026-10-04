"""Preimport core seals, strict entire-record comparison, isolated Python."""
import argparse,hashlib,json,sys
from pathlib import Path


def need(ok,message):
    if not ok:raise ValueError(message)


def whole(actual,expected,path='root'):
    need(type(actual)is type(expected),'whole-record type mismatch '+path)
    if type(actual)is dict:
        need(actual.keys()==expected.keys(),'whole-record keys mismatch '+path)
        for k in actual:whole(actual[k],expected[k],path+'.'+k)
    elif type(actual)is list:
        need(len(actual)==len(expected),'whole-record length mismatch '+path)
        for j,(a,b)in enumerate(zip(actual,expected)):whole(a,b,path+'.'+str(j))
    else:need(actual==expected,'whole-record value mismatch '+path)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--expected');a=p.parse_args()
    root=Path(__file__).resolve().parent
    seal=json.loads((root/'PRIMARY_SEAL.json').read_text())
    names={'field.py','intervals.py','check.py','refine.py','EXPECTED.json','verify.py'}
    need(type(seal)is dict and type(seal.get('files'))is dict and set(seal['files'])==names,'primary source census')
    for name,digest in seal['files'].items():
        need(type(digest)is str and hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'PREIMPORT source mismatch '+name)
    expected=json.loads((Path(a.expected)if a.expected else root/'EXPECTED.json').read_text())
    sys.path.insert(0,str(root))
    from refine import refine
    actual=refine();whole(actual,expected)
    raw=json.dumps(actual,sort_keys=True,separators=(',',':')).encode()
    if a.output:Path(a.output).write_bytes(raw)
    print(json.dumps({'complete':True,'all_six_core_seals':True,'whole_record_compared':True,
                     'base_checks_each':len(actual['baseline']['check_names']),
                     'new_checks':len(actual['refinement_check_names']),
                     'tau_R':actual['tau_R_integer_coefficients'],'tau_16':actual['tau_16'],
                     'whole_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
