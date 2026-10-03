"""Byte-pinned geometry and actual committed exact-ten singletons/triple premise."""
import hashlib
import importlib.util
import json
from pathlib import Path
HERE=Path(__file__).absolute().parent
ROOT=HERE
SOURCE=HERE.parent/'order7-phase-ten-singletons'
BASE=HERE.parent/'order7-geometric-cut'
REF='bafkreigat5d3eaewts6i36byttvxahkxndtep5yqofxp7i4bs4q2qpj22a'
COMMIT='9a8bcdf4f3d774ea696ef4cb88dad7edae8295a9'
BODY_SHA='796570ff5a05e32a7e56f6a23029032c9e00165609f9ec7138768b8967049b63'
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pins():
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        require(sha(HERE/name)==digest,'changed compact source: '+name)
    data=json.loads((HERE/'SOURCE_PINS.json').read_text())
    require(data['premise']['artifact_ref']==REF and data['premise']['source_commit']==COMMIT
        and data['premise']['body_sha256']==BODY_SHA and data['actual_selected_singletons_assumed'] is True
        and data['conditional_maximum_gap_normalization'] is True
        and data['global_phase_maximum_gap_rule_assumed'] is False
        and data['new_phase_endpoint_exclusion_assumed'] is False
        and data['both_backgrounds_explicit'] is True and len(data['relative_files'])==105,
        'changed actual parent semantics')
    for name,digest in data['relative_files'].items():
        require(sha(HERE.parent/name)==digest,'changed pinned parent/helper: '+name)
    return data
def encoder():
    pins()
    spec=importlib.util.spec_from_file_location('singletons_encoder',BASE/'encode.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
pins()
