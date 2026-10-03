"""Exact byte-pinned public inputs and actual9865 provenance; no private protocol required."""
import hashlib
import importlib.util
import json
from pathlib import Path
HERE=Path(__file__).absolute().parent
ROOT=HERE
SOURCE=HERE.parent/'order7-phase-eleven'
BASE=HERE.parent/'order7-geometric-cut'
REF='bafkreie6qhal45svhbsgkvqhouwutfwp5cxnbqggubgctp6txsjemuiadu'
COMMIT='7d528cf2d6024800c8fbb199044b8371e1922694'
BODY_SHA='26e1dd7ce43a09d71424a80bda69f141c1abd8bc76f0bb9aa97b69a65c02b67d'
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pins():
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        require(sha(HERE/name)==digest,'changed compact mathematical source: '+name)
    data=json.loads((HERE/'SOURCE_PINS.json').read_text())
    require(data['premise']['artifact_ref']==REF and data['premise']['source_commit']==COMMIT
        and data['premise']['body_sha256']==BODY_SHA and data['phase_weights']==[11,33]
        and data['normalized_minimum_distance_heads']==[4,3]
        and data['conditional_minimum_distance_three_normalization'] is True
        and data['minimum_distance_rule_is_universal'] is False
        and data['exact_TEN_rules_used'] is False
        and data['regular_spacing_exclusion_used_as_input'] is False
        and data['new_endpoint_exclusion_used_as_input'] is False
        and data['all_44_lower_orientations_retained'] is True
        and data['both_backgrounds_explicit'] is True and len(data['relative_files'])==117,
        'changed exact-eleven input semantics or whole committed parent provenance')
    for name,digest in data['relative_files'].items():
        require(sha(HERE.parent/name)==digest,'changed pinned public parent/helper: '+name)
    return data
def encoder():
    pins()
    spec=importlib.util.spec_from_file_location('eleven_spacing_encoder',BASE/'encode.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
pins()
