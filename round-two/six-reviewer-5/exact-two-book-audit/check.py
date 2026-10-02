"""Cold independent complete replay, weaker certificate, and exact controls."""
import argparse
import hashlib
import json
from pathlib import Path
from common import require
from replay import Context, audit, canonical, WEAKER_CLAIM
from controls import full_subset_control, literal_controls, baseline, damages


def compute():
    base = Path(__file__).resolve().parent; context = Context()
    original = json.loads((base/'credited-certificate.json').read_text())
    summary, raw = audit(original, context)
    require(summary == json.loads((base/'credited-expected.json').read_text()), 'whole credited summary')
    raw_sha = hashlib.sha256(raw).hexdigest()
    require(len(raw) == 2597741 and raw_sha == 'a96d9587b8de30653a02ffd94a847475343eef8ee2e7abdb468c330aab285586', 'every original regenerated star and deletion')
    weaker = json.loads((base/'no-high-blue-certificate.json').read_text())
    weaker_summary, weaker_raw = audit(weaker, context, blue_caps=False, claim=WEAKER_CLAIM)
    require(weaker_summary['templates'] == 82, 'complete weaker census')
    return {'agent': 'six-reviewer-5', 'role': 'independent mathematical reviewer', 'original': summary,
            'original_full_record_bytes': len(raw), 'original_full_record_sha256': raw_sha,
            'weaker': weaker_summary, 'weaker_full_record_bytes': len(weaker_raw),
            'weaker_full_record_sha256': hashlib.sha256(weaker_raw).hexdigest(),
            'full_subset_control': full_subset_control(context), 'literal_controls': literal_controls(context),
            'damaged_certificates': damages(original, context), 'primary21': baseline(base/'primary21.txt')}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', type=Path)
    args = parser.parse_args(); result = compute()
    if args.check: require(canonical(result) == canonical(json.loads(args.check.read_text())), 'entire frozen record mismatch')
    print(canonical(result))


if __name__ == '__main__': main()
