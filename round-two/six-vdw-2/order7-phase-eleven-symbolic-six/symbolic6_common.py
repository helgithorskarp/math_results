"""Entire portable source gates before mathematical imports."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).absolute().parent
PUBLIC=ROOT/'credited'
BASE=PUBLIC
COMMIT='945d7579577bc0080b19b19ec0be69ea0c13e7fb'
VARIABLES=348


def require(condition,message):
    if not condition:raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path,value):
    Path(path).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def pins():
    raw=(ROOT/'symbolic6-source-pins.json').read_bytes()
    frozen=json.loads((ROOT/'symbolic6-freeze.json').read_text())
    require(hashlib.sha256(raw).hexdigest()==frozen['manifest_sha256'],'whole frozen source manifest changed')
    new=json.loads(raw)
    require(new['agent']=='six-vdw-2' and new['role']=='researcher' and new['variables']==348
            and new['backgrounds']==[0,1] and new['numerical_premises']==[8664,8787,9069]
            and new['private_following_gap_cut'] is False and new['native_conflicts']==50000
            and new['native_seconds']==30,'source scope or resource cap changed')
    for name,digest in new['files'].items():
        require(sha(ROOT/name)==digest,'whole portable source or provenance changed: '+name)
    credit=json.loads((ROOT/'CREDITED_SOURCES.json').read_text())
    require(credit['source_commit']==COMMIT and credit['private_gap_cut'] is False
            and credit['foreign_family_cut'] is False,'credited mathematical source or scope changed')
    require([p['height'] for p in credit['numerical_premises']]==[8664,8787,9069]
            and [p['height'] for p in credit['ordinary_exhaustiveness']]==[10044,10093],
            'credited hypothesis/dependency set changed')
    originals={name:record['sha256'] for name,record in credit['whole_credited_sources'].items()}
    require(set(originals)=={'encode.py','solve.py','check_rup_lrat.py'},'entire credited source closure differs')
    for name,digest in originals.items():
        require(sha(BASE/name)==digest,'whole credited source differs: '+name)
    # These bookkeeping sets are empty for a fresh portable reproduction. They
    # are not mathematical premises. Campaign failures/ledgers are not inputs.
    old=dict(published_files=originals,private_files={},provenance_files={},
             frozen_prior_cnfs=[],completed_previous_cnfs=[])
    return old,new


def imported(filename,name):
    pins()
    spec=importlib.util.spec_from_file_location(name,BASE/filename)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


pins()
