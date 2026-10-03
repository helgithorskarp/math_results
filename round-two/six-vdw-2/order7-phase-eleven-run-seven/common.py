"""Portable whole-source gates; no ledger, signer, account or campaign state."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = HERE = Path(__file__).absolute().parent
PUBLIC = HERE.parent
BASE = PUBLIC/'order7-geometric-cut'
REF = 'bafkreia7rt2kiycn7bjhfhjxfdzczdufth2syolrxsxvu65h6ne6sgxgqu'
COMMIT = 'd3b7d7f019d08a061d624b24023b0182f0f4783e'
BODY_SHA = '71f7288e4d7820694790b10fb224f474945da73868844fde3e5763fe53c5c47f'
FILES = {'common.py', 'generate.py', 'audit.py', 'guards.py', 'reproduce.py', 'EXPECTED.csv',
         'VERIFICATION.json', 'SOURCE_PINS.json', 'PROOF.md', 'README.md', '.gitignore'}
RELATIVE = {'order7-geometric-cut/encode.py', 'order7-geometric-cut/solve.py',
            'order7-geometric-cut/check_rup_lrat.py', 'order7-geometric-cut/PROOF.md',
            'order7-antipodal-geography/PROOF.md', 'order7-cluster-and-root57/PROOF.md',
            'order7-phase-eleven-adjacent-pair/PROOF.md'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def sha(path):
    return digest(Path(path).read_bytes())

def pins():
    manifest = {}
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        wanted, name = line.split('  ', 1)
        require(name not in manifest and name in FILES, 'unknown or repeated source manifest file')
        manifest[name] = wanted
    require(set(manifest) == FILES, 'incomplete entire contribution source manifest')
    for name, wanted in manifest.items():
        require(sha(HERE/name) == wanted, 'whole contribution source differs: '+name)
    data = json.loads((HERE/'SOURCE_PINS.json').read_text())
    require(set(data['relative_files']) == RELATIVE and len(data['frozen_prior_cnfs']) == 10
            and data['prior_adjacent_ref'] == REF and data['prior_source_commit'] == COMMIT
            and data['prior_full_body_sha256'] == BODY_SHA and data['prior_ref_used_as_numerical_cut'] is False
            and data['nonconstant_phase_weights'] == [11, 33]
            and data['fixed_phase_heads'] == 30 and data['independent_lower_colors'] == 44
            and data['preselected_definition_batches'] == 5 and data['heads_per_batch'] == 6
            and data['universal_field_cuts'] == [8664, 8787, 9069],
            'whole phase/source/coverage/import scope differs')
    for name, wanted in data['relative_files'].items():
        require(sha(PUBLIC/name) == wanted, 'whole published physical helper/premise differs: '+name)
    return data

def imported(filename, name):
    pins()
    spec = importlib.util.spec_from_file_location(name, BASE/filename)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

pins()
