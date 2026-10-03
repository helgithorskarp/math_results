"""Source-only reproduction, exact whole-record correspondence and semantic checks."""
from pathlib import Path
import hashlib, importlib.util, json, sys

ROOT=Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)

def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py'))
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    spec.loader.exec_module(module);return module

def main():
    seal=json.loads((ROOT/'SEAL.json').read_text())
    for name in('audit.py','semantic.py','controls.py'):
        raw=(ROOT/name).read_bytes();pin=seal['files'][name]
        need(len(raw)==pin['bytes']and hashlib.sha256(raw).hexdigest()==pin['sha256'],'before-import owned source pin '+name)
    audit=load('audit');semantic=load('semantic');controls=load('controls')
    first=None;validated=None;summary=None
    for mode in('incidence','physical'):
        record=audit.main(mode)
        raw=json.dumps(record,sort_keys=True,separators=(',',':')).encode()
        if first is None:
            first=raw;validated=semantic.verify(record);summary=record['summary']
        else:need(raw==first,'every primitive entry agrees between the two kernels')
    result={'status':'COMPLETE_SOURCE_ONLY_BINARY_TRIPLE_REVIEW','canonical_bytes':len(first),'canonical_sha256':hashlib.sha256(first).hexdigest(),'summary':summary,'semantic':validated,'controls':controls.main(),'target_native_imported':False,'ordinary_proof_formalized':False,'shared_primary_orchestration_schema':True}
    expected=json.loads((ROOT/'EXPECTED.json').read_text())
    need(result==expected,'complete compact output equals expected, after mathematical checks')
    return result
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,separators=(',',':')))
