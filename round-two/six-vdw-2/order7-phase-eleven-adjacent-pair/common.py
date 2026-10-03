"""Byte-pinned actual9948 provenance and public geometry; no private wire required."""
import hashlib
import importlib.util
import json
from pathlib import Path
HERE=Path(__file__).absolute().parent
ROOT=HERE
SOURCE=HERE.parent/'order7-phase-eleven-isolated-gaps'
BASE=HERE.parent/'order7-geometric-cut'
REF='bafkreibc4zo5kmjkv6thbo6nvv5geelgwiimyphv5eicpechqp6jyplzd4'
COMMIT='efae21794efc3e7da5d0a0dadd8be7650e8a15aa'
BODY_SHA='ba49621c7b867ebe2ad0e2e43016a97b7b49e12a34743538795222140705058a'
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
        and data['conditional_maximum_gap_four'] is True and data['minimum_pair_heads_conditional'] is True
        and data['minimum_pair_rule_is_universal'] is False
        and data['minimum_pair_starts']==[5,*range(7,41),42]
        and data['new_endpoint_exclusion_used_as_input'] is False and data['exact_TEN_rules_used'] is False
        and data['gap_four_lemma_used_as_unconditional_native_cut'] is False and data['all_44_lower_orientations_retained'] is True
        and data['both_backgrounds_explicit'] is True and data['free_selected_counts']==[7,8]
        and len(data['relative_files'])==145 and len(data['frozen_prior_cnfs'])==10,'changed conditional exact-eleven semantics or parent provenance')
    for name,digest in data['relative_files'].items():
        require(sha(HERE.parent/name)==digest,'changed pinned public ancestor/helper: '+name)
    return data
def encoder():
    pins()
    spec=importlib.util.spec_from_file_location('eleven_isolated_encoder',BASE/'encode.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
pins()
