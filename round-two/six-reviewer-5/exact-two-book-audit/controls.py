"""Separate literal-set page oracle, full-subset domain census and damages."""
import ast
import copy
import hashlib
from itertools import combinations
from pathlib import Path
from common import require, points
from replay import coverage, case_replay
from propagate import compatible


def full_subset_control(context):
    examined = 0; comparisons = 0
    for index, profile in enumerate(context.profiles):
        catalog = {}
        for x, own in enumerate(profile['types']):
            by_exception = {}
            for choice in combinations([v for v in range(18) if v != x], 10-own.bit_count()):
                examined += 1
                mask = sum(1 << v for v in choice); exceptional = 0; accepted = True
                for i, row in enumerate(profile['low_masks']):
                    count = (mask & row).bit_count()
                    if own >> i & 1:
                        if count not in (2, 3): accepted = False; break
                        if count == 2: exceptional |= 1 << i
                    elif count != 5: accepted = False; break
                if accepted: by_exception.setdefault(exceptional, []).append(mask)
            catalog[x] = {e: tuple(sorted(row)) for e, row in by_exception.items()}
        for exception in context.exceptions[index]:
            for x, row in enumerate(context.initial(index, exception)):
                mask = sum(1 << i for i, selected in enumerate(exception) if selected == x)
                require(row == catalog[x].get(mask, ()), 'entire MITM/full-subset domain disagreement')
                comparisons += 1
    require(examined == 2567136 and comparisons == 1476, 'complete raw star coverage')
    return {'raw_subsets': examined, 'whole_domain_comparisons': comparisons}


def set_compatible(profile, x, sx, y, sy, blue_caps=True, k4=True):
    rx = set(points(sx << 4)) | set(points(profile['types'][x]))
    ry = set(points(sy << 4)) | set(points(profile['types'][y]))
    if ((y+4) in rx) != ((x+4) in ry): return False
    if y+4 in rx:
        pages = rx & ry
        if len(pages) > 3: return False
        if k4:
            for i in pages & set(range(4)):
                if any(v-4 in points(profile['low_masks'][i]) for v in pages if v >= 4): return False
    elif blue_caps:
        bx = set(range(22)) - rx - {x+4}; by = set(range(22)) - ry - {y+4}
        if len(bx & by) > 6: return False
    return True


def literal_controls(context):
    comparisons = 0; high_blue_only = 0; k4_only = 0; red_cap_only = 0
    for index, profile in enumerate(context.profiles):
        exception = next(e for e in context.exceptions[index] if all(context.initial(index, e)))
        rows = context.initial(index, exception)
        for x, y in combinations(range(18), 2):
            # A fixed broad, bounded sample, not an enumeration of hosts.
            left = rows[x][::max(1, len(rows[x])//8)][:9]
            right = rows[y][::max(1, len(rows[y])//8)][:9]
            for sx in left:
                for sy in right:
                    for blue, k4 in [(True, True), (False, True), (True, False), (False, False)]:
                        result = compatible(profile, x, sx, y, sy, blue, k4)
                        require(result == set_compatible(profile, x, sx, y, sy, blue, k4), 'literal physical page mismatch')
                        require(result == compatible(profile, y, sy, x, sx, blue, k4), 'pair reciprocity of compatibility')
                        comparisons += 1
                    if compatible(profile, x, sx, y, sy, False, True) and not compatible(profile, x, sx, y, sy): high_blue_only += 1
                    if compatible(profile, x, sx, y, sy, True, False) and not compatible(profile, x, sx, y, sy): k4_only += 1
                    if bool(sx >> y & 1) == bool(sy >> x & 1) and sx >> y & 1:
                        if ((sx & sy).bit_count()+(profile['types'][x] & profile['types'][y]).bit_count()) > 3: red_cap_only += 1
    require(high_blue_only > 0 and k4_only > 0 and red_cap_only > 0, 'independent active cut controls')
    return {'literal_set_bit_comparisons': comparisons, 'high_blue_only_rejections': high_blue_only,
            'k4_only_rejections': k4_only, 'red_cap_rejections': red_cap_only}


def baseline(path):
    raw = Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55', 'credited primary matrix bytes')
    text = raw.decode(); matrix = ast.literal_eval(text[:text.index(']]')+2]); n = len(matrix)
    require(n == 21 and all(len(row) == n for row in matrix), 'primary size')
    require(all(type(value) is int and value in (0, 1) for row in matrix for value in row), 'matrix entries')
    require(all(matrix[i][i] == 0 for i in range(n)) and all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)), 'simple reciprocal matrix')
    # The original matrix's 1-color is BLUE. Test the color orientation explicitly.
    blue = [{j for j in range(n) if matrix[i][j]} for i in range(n)]
    red = [set(range(n)) - row - {i} for i, row in enumerate(blue)]
    red_edges = 0; blue_edges = 0; max_red = 0; max_blue = 0
    for i, j in combinations(range(n), 2):
        if j in red[i]:
            pages = len(red[i] & red[j]); max_red = max(max_red, pages); red_edges += 1
            require(pages <= 3, 'primary red ordinary book')
        else:
            pages = len(blue[i] & blue[j]); max_blue = max(max_blue, pages); blue_edges += 1
            require(pages <= 6, 'primary blue ordinary book')
    require((red_edges, blue_edges, max_red, max_blue) == (93, 117, 3, 6), 'known prior baseline')
    return {'order': n, 'red_edges': red_edges, 'blue_edges': blue_edges, 'red_pages_max': max_red,
            'blue_pages_max': max_blue, 'spines': red_edges+blue_edges, 'novel': False}


def damages(packet, context):
    failures = []
    def reject(label, change, run):
        value = copy.deepcopy(packet); change(value)
        try: run(value)
        except (ValueError, KeyError, TypeError, IndexError): failures.append(label); return
        raise ValueError('mathematical damage accepted: '+label)
    check = lambda value: coverage(value, context)
    reject('missing-last-profile', lambda p:p['profiles'].pop(), check)
    reject('duplicate-profile', lambda p:p['profiles'].__setitem__(1, copy.deepcopy(p['profiles'][0])), check)
    reject('boolean-schema', lambda p:p.__setitem__('schema', True), check)
    reject('false-claim-scope', lambda p:p.__setitem__('claim', 'all108 excluded'), check)
    reject('false-incidence-tag', lambda p:p['profiles'][0]['types'].__setitem__(0, 3), check)
    reject('boolean-profile', lambda p:p['profiles'][0]['profile'].__setitem__(0, False), check)
    reject('missing-template', lambda p:p['profiles'][0]['cases'].pop(), check)
    reject('duplicate-template', lambda p:p['profiles'][0]['cases'].__setitem__(1, copy.deepcopy(p['profiles'][0]['cases'][0])), check)
    reject('invalid-exception', lambda p:p['profiles'][0]['cases'][0]['exceptions'].__setitem__(0, 1), check)
    reject('boolean-domain-size', lambda p:p['profiles'][0]['cases'][0]['domain_sizes'].__setitem__(0, True), check)
    case_index = next(i for i, c in enumerate(packet['profiles'][0]['cases']) if c['kind'] == 'static')
    def selected(p): return p['profiles'][0]['cases'][case_index]
    def replay(p):
        coverage(p, context)
        c = selected(p); case_replay(c, context.profiles[0], context.initial(0, c['exceptions']))
    reject('wrong-initial-count', lambda p:selected(p)['domain_sizes'].__setitem__(0, 1), replay)
    reject('narrowed-domain-fingerprint', lambda p:selected(p).__setitem__('domain_sha256', '0'*64), replay)
    reject('false-empty', lambda p:(selected(p).__setitem__('kind', 'empty'), selected(p).__setitem__('steps', [])), replay)
    reject('wrong-batch-count', lambda p:selected(p)['steps'][0].__setitem__(2, selected(p)['steps'][0][2]+1), replay)
    reject('self-support', lambda p:selected(p)['steps'][0].__setitem__(1, selected(p)['steps'][0][0]), replay)
    reject('skipped-batch', lambda p:selected(p)['steps'].pop(0), replay)
    reject('repeated-batch', lambda p:selected(p)['steps'].insert(1, copy.deepcopy(selected(p)['steps'][0])), replay)
    reject('false-deletion-fingerprint', lambda p:selected(p).__setitem__('deletions_sha256', 'f'*64), replay)
    reject('false-final-target', lambda p:selected(p).__setitem__('empty_target', (selected(p)['empty_target']+1)%18), replay)
    return {'count': len(failures), 'rejected': failures}
