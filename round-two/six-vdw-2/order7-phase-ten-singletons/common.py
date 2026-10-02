"""Byte-pinned geometry and actual committed exact-ten singletons/triple premise."""
import hashlib
import importlib.util
import json
from pathlib import Path
HERE=Path(__file__).absolute().parent
ROOT=HERE
SOURCE=HERE.parent/'order7-phase-ten-singletons-triple'
BASE=HERE.parent/'order7-geometric-cut'
REF='bafkreiasclwdnwtz2b5lhxt6bwausvdi6stisnnvxox3ag5qllcsmpwg3m'
COMMIT='31f916dbd41ec2b486d3b6208d30f17881fa2aaa'
BODY_SHA='499038360195e56fc8fc340b5017ffed11caa0145456cf2d85b14f601bde4d91'
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pins():
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        require(sha(HERE/name)==digest,'changed compact source: '+name)
    data=json.loads((HERE/'SOURCE_PINS.json').read_text())
    require(data['premise']['artifact_ref']==REF and data['premise']['source_commit']==COMMIT
        and data['premise']['body_sha256']==BODY_SHA and data['actual_singletons_or_unique_triple_assumed'] is True
        and data['actual_triple_following_background_one_assumed'] is True
        and data['proposed_global_no_adjacency_assumed'] is False and data['new_no_triple_exclusion_assumed'] is False,
        'changed actual parent semantics')
    for name,digest in data['relative_files'].items():
        require(sha(HERE.parent/name)==digest,'changed pinned parent/helper: '+name)
    return data
def encoder():
    pins()
    spec=importlib.util.spec_from_file_location('singletons_encoder',BASE/'encode.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
pins()
