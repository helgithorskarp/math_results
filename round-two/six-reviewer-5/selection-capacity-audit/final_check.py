"""Run the unchanged first independent core, then post-seal comparisons."""
import argparse
import hashlib
import json
from pathlib import Path
import check
from literal import require,canonical
from corroborate import compare
from extended import controls,append_bridge

ROOT = Path(__file__).resolve().parent


def compute():
    seal = json.loads((ROOT/'first-seal.json').read_text())
    for name,sha in seal['source_sha256'].items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == sha, 'first independently sealed mathematical source unchanged')
    core = check.compute()
    require(canonical(core) == canonical(json.loads((ROOT/'first-record.json').read_text())), 'entire first independently sealed result unchanged')
    extra = controls()
    original = compare({'rejected_primary_damages':extra['original_four_primary_damages_rejected'],
                        'enlarged_q1_positive_control':extra['enlarged_q1_positive_control']})
    return {'unchanged_independent_core':core,'post_seal_controls':extra,
            'credited_original_full_record_comparison':original,'explicit_upper71_append_bridge':append_bridge()}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--check',type=Path); args = p.parse_args()
    result = compute()
    if args.check: require(canonical(result) == canonical(json.loads(args.check.read_text())), 'entire final frozen record')
    print(canonical(result))


if __name__ == '__main__':main()
