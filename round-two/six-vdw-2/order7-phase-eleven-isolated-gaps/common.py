"""Byte-pinned actual9910 provenance and public geometry; no private wire required."""
import hashlib
import importlib.util
import json
from pathlib import Path
HERE=Path(__file__).absolute().parent
ROOT=HERE
SOURCE=HERE.parent/'order7-phase-eleven-close-pair'
BASE=HERE.parent/'order7-geometric-cut'
REF='bafkreib7hwuyauebvr7xtqfhy6vrfy3ohpatla223ptti5xnaxjroj6rcq'
COMMIT='ba27ac449922910dab4751949c166078f835406d'
BODY_SHA='99488cb7ac1998830583f7a8b1ee53957e1567bc33e4761ebb83aea44b78031d'
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def pins():
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        require(sha(HERE/name)==digest,'changed compact source: '+name)
    data=json.loads((HERE/'SOURCE_PINS.json').read_text())
    require(data['premise']['artifact_ref']==REF and data['premise']['source_commit']==COMMIT
        and data['premise']['body_sha256']==BODY_SHA and data['phase_weights']==[11,33]
        and data['conditional_all_selected_isolated'] is True and data['isolation_rule_is_universal'] is False
        and data['conditional_maximum_gap_normalization'] is True
        and data['maximum_gap_rule_is_global_phase_restriction'] is False
        and data['maximum_gaps_certified']==[7,6,5] and data['maximum_gap_four_refuted'] is False
        and data['new_endpoint_exclusion_used_as_input'] is False and data['exact_TEN_rules_used'] is False
        and data['close_pair_lemma_used_as_native_cut'] is False and data['all_44_lower_orientations_retained'] is True
        and data['both_backgrounds_explicit'] is True and data['free_selected_count']==9
        and len(data['relative_files'])==132,'changed conditional exact-eleven semantics or parent provenance')
    for name,digest in data['relative_files'].items():
        require(sha(HERE.parent/name)==digest,'changed pinned public ancestor/helper: '+name)
    return data
def encoder():
    pins()
    spec=importlib.util.spec_from_file_location('eleven_isolated_encoder',BASE/'encode.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
pins()
