"""Check selected actual APs and their coverage of every requested cut row.

Direct gap-cell bit flips derive the rectangles, without the proposer or its
consecutive-color formula. A covered cut has a checked monochromatic AP.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import sys
import time


class InvalidCertificate(ValueError):
    pass


def require(ok, reason):
    if not ok:
        raise InvalidCertificate(reason)


class Budget:
    def __init__(self):
        self.cases = 0

    def add(self, count=1):
        self.cases += count
        if self.cases > 200000:
            raise RuntimeError('Unchanged200000-case operational limit')


def verify(data, word, start, count, budget, require_covered=False):
    n = len(word)
    budget.add(n + 3)
    require(type(data) is dict and set(data) == {'length', 'term_count', 'base_bits_sha256', 'APs'}, 'cover certificate schema')
    require(type(data['length']) is int and data['length'] == n, 'base word length')
    require(type(data['term_count']) is int and data['term_count'] == 7, 'seven-term scope')
    require(data['base_bits_sha256'] == hashlib.sha256(word.encode()).hexdigest(), 'base word digest')
    APs = data['APs']
    require(type(APs) is list and 1 <= len(APs) <= 289, 'selected AP count bound')
    rectangles, used, original_mono = [], set(), 0
    for ap in APs:
        budget.add(12)
        require(type(ap) is list and len(ap) == 2 and all(type(x) is int for x in ap), 'integer AP geometry')
        a, d = ap
        require(a >= 1 and d >= 1 and a + 6 * d <= n, 'actual AP in base interval')
        require((a, d) not in used, 'duplicate selected AP')
        used.add((a, d))
        positions = [a + k * d for k in range(7)]
        colors = [int(word[position - 1]) for position in positions]
        original_mono += len(set(colors)) == 1
        endpoints = [0] + positions + [n + 1]
        for left_gap in range(8):
            for right_gap in range(left_gap, 8):
                flipped = [bit ^ int(left_gap <= k < right_gap) for k, bit in enumerate(colors)]
                budget.add(8)
                if len(set(flipped)) == 1:
                    rectangles.append((endpoints[left_gap], endpoints[left_gap + 1] - 1,
                                       endpoints[right_gap], endpoints[right_gap + 1] - 1))
                    budget.add(4)
    require(original_mono <= 1, 'selected original-mono count bound')
    # The checked bound gives at most9 for the single original-mono AP and
    # at most2 for each other pattern; this is also independently observed.
    require(len(rectangles) <= 2 * len(APs) + 7, 'derived rectangle bound')
    uncovered, domain, best_gap = 0, 0, None
    rows = []
    for left in range(start, start + count):
        active = []
        for llo, lhi, rlo, rhi in rectangles:
            budget.add()
            if llo <= left <= lhi:
                lo, hi = max(rlo, left + 1), min(rhi, n)
                budget.add(2)
                if lo <= hi:
                    active.append((lo, hi))
        cursor, row_uncovered, gaps = left + 1, 0, 0
        for lo, hi in sorted(active):
            budget.add(2)
            if hi < cursor:
                continue
            if lo > cursor:
                gap = [left, cursor, lo - 1]
                row_uncovered += lo - cursor
                gaps += 1
                if best_gap is None or (gap[2] - gap[1], -gap[0], -gap[1]) > (
                        best_gap[2] - best_gap[1], -best_gap[0], -best_gap[1]):
                    best_gap = gap
            cursor = max(cursor, hi + 1)
        if cursor <= n:
            gap = [left, cursor, n]
            row_uncovered += n - cursor + 1
            gaps += 1
            if best_gap is None or (gap[2] - gap[1], -gap[0], -gap[1]) > (
                    best_gap[2] - best_gap[1], -best_gap[0], -best_gap[1]):
                best_gap = gap
        row_domain = n - left
        require(0 <= row_uncovered <= row_domain, 'row domain accounting')
        uncovered += row_uncovered
        domain += row_domain
        rows.append({'left': left, 'cut_intervals': row_domain, 'uncovered': row_uncovered, 'gaps': gaps})
    if require_covered:
        require(uncovered == 0, 'uncovered cut')
    return {'status': 'ALL_CUTS_IN_ROW_SLICE_HAVE_A_CHECKED_MONO_AP' if uncovered == 0 else
                      'EXACT_ROW_SLICE_HAS_UNCOVERED_CUTS_NO_EXCLUSION',
            'row_start': start, 'row_stop_exclusive': start + count, 'rows': rows, 'cut_intervals_checked': domain,
            'uncovered_intervals': uncovered, 'witness_gap': best_gap,
            'suggested_cut': None if best_gap is None else [best_gap[0], (best_gap[1] + best_gap[2]) // 2],
            'selected_APs': len(APs), 'selected_original_mono_APs': original_mono,
            'derived_rectangles': len(rectangles), 'gap_cells_checked': 36 * len(APs),
            'actual_term_color_cases': 7 * 36 * len(APs), 'complete_full_cut_domain': start == 0 and count == n,
            'all3704_interval_exclusion_from_single_slice': False, 'new_W_bound': None}


CONTROLS = {'empty_APs': 'selected AP count bound', 'over_cap_APs': 'selected AP count bound',
            'boolean_start': 'integer AP geometry', 'zero_step': 'actual AP in base interval',
            'negative_start': 'actual AP in base interval', 'outside_word': 'actual AP in base interval',
            'duplicate_AP': 'duplicate selected AP', 'wrong_length': 'base word length',
            'wrong_digest': 'base word digest', 'unsupported_terms': 'seven-term scope',
            'extra_hypothesis': 'cover certificate schema', 'drop_to_seed_false_cover': 'uncovered cut'}


def corrupt(data, control):
    changed = copy.deepcopy(data)
    if control == 'empty_APs':
        changed['APs'] = []
    elif control == 'over_cap_APs':
        changed['APs'] = changed['APs'][:1] * 290
    elif control == 'boolean_start':
        changed['APs'][0][0] = True
    elif control == 'zero_step':
        changed['APs'][0][1] = 0
    elif control == 'negative_start':
        changed['APs'][0][0] = -1
    elif control == 'outside_word':
        changed['APs'][0][0] = changed['length']
    elif control == 'duplicate_AP':
        if len(changed['APs']) >= 2:
            changed['APs'][-1] = copy.deepcopy(changed['APs'][0])
        else:
            changed['APs'].append(copy.deepcopy(changed['APs'][0]))
    elif control == 'wrong_length':
        changed['length'] -= 1
    elif control == 'wrong_digest':
        changed['base_bits_sha256'] = '0' * 64
    elif control == 'unsupported_terms':
        changed['term_count'] = 8
    elif control == 'extra_hypothesis':
        changed['roots_fixed'] = True
    else:
        changed['APs'] = changed['APs'][:1]
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--row-start', type=int, required=True)
    parser.add_argument('--row-count', type=int, required=True)
    parser.add_argument('--require-covered', action='store_true')
    parser.add_argument('--control', choices=list(CONTROLS))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.monotonic()
    require(not args.output.exists(), 'Existing evidence cannot be overwritten')
    word = args.word.read_text().strip()
    require(7 <= len(word) <= 3704 and set(word) <= {'0', '1'}, 'binary base word')
    require(0 <= args.row_start < len(word) and 1 <= args.row_count <= 32 and
            args.row_start + args.row_count <= len(word), 'declared row slice')
    data = json.loads(args.certificate.read_text())
    budget = Budget()
    if args.control:
        changed = corrupt(data, args.control)
        try:
            result = verify(changed, word, args.row_start, args.row_count, budget,
                            args.require_covered or args.control == 'drop_to_seed_false_cover')
        except InvalidCertificate as error:
            require(str(error) == CONTROLS[args.control], 'Control hit the wrong defect:' + str(error))
            result = {'status': 'MATHEMATICAL_CORRUPTION_REJECTED', 'control': args.control, 'reason': str(error)}
        else:
            raise RuntimeError('Corruption passed cover verification')
    else:
        result = verify(data, word, args.row_start, args.row_count, budget, args.require_covered)
    result.update(agent='six-vdw-1', role='researcher', checked_at=datetime.now(timezone.utc).isoformat(),
                  certificate_sha256=hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
                  word_file_sha256=hashlib.sha256(args.word.read_bytes()).hexdigest(),
                  word_bits_sha256=hashlib.sha256(word.encode()).hexdigest(),
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  interpreter_optimization=sys.flags.optimize, conservative_combined_cases=budget.cases,
                  seconds=time.monotonic() - began, maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  threads=1, mathematical_full_family_exclusion=False, new_W_bound=None)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'cases': budget.cases,
                      'uncovered': result.get('uncovered_intervals')}), flush=True)


if __name__ == '__main__':
    main()
