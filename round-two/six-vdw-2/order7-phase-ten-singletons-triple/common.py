"""Byte-pinned full-field helpers and the committed exact-ten parent premise."""
import hashlib
import importlib.util
import json
from pathlib import Path
HERE=Path(__file__).absolute().parent
ROOT=HERE
SOURCE=HERE.parent/'order7-phase-ten-fourth-four'
BASE=HERE.parent/'order7-geometric-cut'
REF='bafkreihj3pebrgh5xo5l6cthjq6x5dyovqucuajraho2sgsdvcoampgvsy'
COMMIT='e22c31f21415f8f423708fffd1080add95ea84f8'
BODY_SHA='6021e93e701533254770bcff68b960c29c8e823be31fbf2f8a93ae12a7be87a0'
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pins():
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ')
        require(sha(HERE/name)==digest,'changed compact source: '+name)
    data=json.loads((HERE/'SOURCE_PINS.json').read_text())
    require(data['premise']['artifact_ref']==REF and data['premise']['source_commit']==COMMIT
        and data['premise']['body_sha256']==BODY_SHA and data['actual_at_most_one_long_run_assumed'] is True
        and data['new_exclusions_assumed_as_inputs'] is False,'changed committed parent semantics')
    for name,digest in data['relative_files'].items():
        require(sha(HERE.parent/name)==digest,'changed pinned source: '+name)
    return data
def encoder():
    pins()
    spec=importlib.util.spec_from_file_location('singletons_triple_encoder',BASE/'encode.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
pins()
