"""All remaining K18 minimum words, at arbitrary depth and order.

six-sorting-2, researcher. Reuses7671/source4be17abc, changing only the
minimum-language callback and honest metadata; published files unchanged.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

import language

HERE = Path(__file__).resolve().parent
PUBLIC = HERE.parent / 'sorting13_K_minimum_two_unaries'
sys.path.insert(0, str(PUBLIC))
spec = importlib.util.spec_from_file_location('published_K18_driver', PUBLIC / 'search.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def source_check():
    import hashlib
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    for name, expected in manifest['files'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, name
    base.source_check()


def make(path, frozen=None):
    source_check()
    captured = {}
    original = base.minimum_dfa
    def replacement(w, choices, pairs, gates):
        phases = language.encode(w, choices, pairs, gates)
        captured['minimum_phase'] = phases
        return phases
    base.minimum_dfa = replacement
    try:
        meta = base.make(path, frozen)
    finally:
        base.minimum_dfa = original
    meta['extra'].update(minimum_dfa_states=11,
                         minimum_kernel_class='exactly two unary, complete36 words',
                         complete_minimum_word_count=36,
                         minimum_phase=captured['minimum_phase'],
                         parent_source_commit='4be17abc650f757d8cd03b99c9ebedfba45b967d',
                         parent_graph='bafkreibhpxtdzaws5ybf6ljhui2pxexjnnllm6si7blj7g2g3pytjves64',
                         complete_K18_coverage_uses_parent_exclusion=True)
    if meta['gates'] == 18:
        assert meta['variables'] == 40891 and meta['clauses'] == 1300995
    path.with_suffix('.meta.json').write_text(json.dumps(meta, indent=2)+'\n')
    return meta


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=('generate', 'solve'))
    p.add_argument('--path', required=True, type=Path)
    p.add_argument('--freeze', type=Path)
    p.add_argument('--conflicts', type=int, default=30000)
    p.add_argument('--seconds', type=float, default=40)
    args = p.parse_args()
    if args.command == 'generate':
        frozen = json.loads(args.freeze.read_text()) if args.freeze else None
        meta = make(args.path, frozen)
        info = {k:v for k,v in meta.items() if k not in ('states','choices','pairs')}
        info['extra'] = {k:v for k,v in info['extra'].items()
                         if k not in ('minimum_phase','interval_cuts','activity_states','activity_flags')}
        print(json.dumps(info), flush=True)
    else:
        assert 0 < args.conflicts <= 30000 and 0 < args.seconds <= 40
        base.solve(args.path, args.conflicts, args.seconds)


if __name__ == '__main__':
    main()
