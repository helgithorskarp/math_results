"""Entire n28 rational witness, populations and exact controls; stdlib only.

Actual author six-downset-2, researcher. The complete original lift and
harmonic bridges are ordinary, unformalized mathematics. No numerical
proposal, solver status, expected output or external executable is a premise.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from math import comb
import os
from pathlib import Path
import platform
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model import require, specification, table, check_table, sectors
from core_check import verify, affine_audit, credited_control, reject, exact
from original_forms import original_form
from audit import audit_basis, literal_control, dense_congruence, triangular_star_audit

THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')
SOURCE = ('verify.py', 'model.py', 'core_check.py', 'original_forms.py',
          'audit.py', 'CERTIFICATE.json', 'credited/affine.py',
          'credited/model.py', 'credited/exact.py', 'credited/matrices.py')


def rational(v):
    require(type(v) is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', v),
            'Exact rational string, never a decimal or float')
    return Q(v)


def encode(v):
    if type(v) is Q:
        return str(v)
    raise TypeError('Unencoded type: '+type(v).__name__)


def decode(seed):
    require(seed['agent'] == 'six-downset-2' and seed['role'] == 'researcher'
            and seed['original_ground_complements'] is True,
            'Actual author, role and entire original complement domain')
    require(type(seed['n']) is int and seed['n'] == 28, 'Only the claimed fixed order')
    require(seed['active'] == [9, 10, 11, 12, 13], 'The exact ordered five active classes')
    spec = specification(28, (9, 10, 11, 12, 13))
    require(seed['names'] == spec['names'], 'Complete ordered affine coordinates')
    values = [rational(v) for v in seed['values']]
    floor = rational(seed['original_upper_floor'])
    require(floor > 0, 'Positive exact original upper floor')
    # This checks BOTH algorithms on every complete untransformed C/U block,
    # with zero floor: a core metric is not substituted for the original one.
    result = verify(spec, values, Q(0))
    require(type(seed['expected_lower_rank']) is int and
            type(seed['expected_upper_rank']) is int and
            result['lower_rank'] == seed['expected_lower_rank'] and
            result['upper_rank'] == seed['expected_upper_rank'],
            'Claimed complete original ranks')
    require(result['actual_empty']['loop'] == rational(seed['actual_empty_loop']) and
            result['actual_empty']['row'] == [rational(v) for v in seed['actual_empty_rows']],
            'All actual empty-row entries and the original loop')
    original = [original_form(spec, b) for b in sectors(spec, result['table'])]
    raw_mean = sectors(spec, result['table'])[0]
    for side in ('lower', 'upper'):
        require(original[0][side] == dense_congruence(raw_mean[side], raw_mean['gram']),
                'Entire certificate mean congruence, independent dense multiplication')
    floors = []
    for block in original:
        for side in ('lower', 'upper'):
            full_rank=len(block['layers'])-len(block['kernels']) if side=='lower' else len(block['layers'])
            exact.both(block[side],full_rank)
            keep = block['lower_keep'] if side == 'lower' else list(range(len(block['layers'])))
            shifted = [[block[side][i][k]-floor*block['gram'][i][k]
                        for k in keep] for i in keep]
            exact.both(shifted, len(keep))
            floors.append(dict(j=block['j'], side=side, dimension=len(keep),
                               original_metric_floor=floor,
                               scope='chosen complementary plane only' if side == 'lower'
                                     else 'entire original harmonic sector',
                               two_exact_algorithms=True, positive_definite=True,
                               full_unshifted_original_rank=full_rank))
    require(len(floors) == 30, 'All fifteen original degrees and both endpoints')
    return spec, values, result, floors


def population_bound(spec):
    """All4096 subsets of twelve original noncentral classes; arithmetic only.

    PROOF.md supplies the all-real count/rank bridge. No original-vertex
    enumeration or real PSD infeasibility is inferred from this control.
    """
    n,middle=spec['n'],spec['middle']
    classes=list(range(2,middle))
    populations={a:comb(n,a) for a in classes}
    populations[middle]=comb(n,middle)//2
    require(sum(comb(n,a) for a in range(n-1))==spec['N'],'All original layers')
    require(sum(populations.values())==spec['s']-1,'All original unordered complement pairs')
    budget=spec['s']//spec['gap']
    rows,seven_absent,low_present=[],[],[]
    for absent_count in range(len(classes)+1):
        for absent in combinations(classes,absent_count):
            q=sum(populations[a] for a in absent)
            present_count=len(classes)-absent_count
            allowed=q<=budget
            row=dict(absent=list(absent),present_count=present_count,
                     unavoidable_saturated_pairs=q,passes_necessary_count_bound=allowed)
            rows.append(row)
            if present_count<=4 and allowed:low_present.append(row)
            if present_count==5 and allowed:seven_absent.append(row)
    require(len(rows)==4096 and not low_present,'Every at-most-four-class pattern excluded')
    require(len(seven_absent)==1 and seven_absent[0]['absent']==list(range(2,9)),
            'Unique possible seven absent classes at five present classes')
    q=sum(comb(n,a) for a in range(2,9))
    eight=q+comb(n,9)
    second=sum(comb(n,a) for a in range(2,8))+comb(n,9)
    require((q,eight,second,budget)==(4791294,11698194,8590089,4971025),
            'Exact least-seven, least-eight, second-least-seven and budget')
    require(q==spec['saturated_pairs'] and spec['N']-n-q==263644105,
            'Greatest constrained all-real rank ceiling')
    return dict(order=n,vertices=spec['N'],complementary_populations=populations,
                whole_size_class_subsets=len(rows),complete_subsets=rows,
                published_count_budget=budget,least_eight_absent_population=eight,
                second_least_seven_absent_population=second,
                unique_seven_absent_classes=seven_absent[0]['absent'],
                saturated_pairs_at_class_minimum=q,minimum_noncentral_classes=5,
                greatest_lower_rank_at_class_minimum=263644105,
                arithmetic_scope='class subsets only; all-real PSD/rank bridges are ordinary proof')


def damages(seed, spec, values):
    def modified(key, value):
        bad = json.loads(json.dumps(seed))
        bad[key] = value
        return bad
    tests = [
        (lambda:decode(modified('values', seed['values'][:-1])), 'Missing exact free coordinate'),
        (lambda:decode(modified('values', [float(Q(seed['values'][0]))]+seed['values'][1:])),
         'Floating coefficient input'),
        (lambda:decode(modified('active', [10, 9, 11, 12, 13])), 'Reordered original active classes'),
        (lambda:decode(modified('names', seed['names'][1:]+seed['names'][:1])),
         'Permuted affine coefficient semantics'),
        (lambda:decode(modified('actual_empty_loop', str(Q(seed['actual_empty_loop'])+1))),
         'Wrong original empty loop'),
        (lambda:decode(modified('actual_empty_rows',
                  [str(Q(seed['actual_empty_rows'][0])+1)]+seed['actual_empty_rows'][1:])),
         'Wrong original empty row'),
        (lambda:decode(modified('original_upper_floor', '-1')), 'Negative original cap floor'),
        (lambda:decode(modified('expected_lower_rank', seed['expected_lower_rank']+1)),
         'Wrong whole original lower rank')]
    negative, zero = values[:], values[:]
    negative[0], zero[0] = Q(-1), Q(0)
    tests.extend([
        (lambda:verify(spec, negative, Q(0)), 'Negative complement deficit'),
        (lambda:verify(spec, zero, Q(0)), 'Zero active deficit with a surviving proper coupling')])
    B = table(spec, values)
    B[1][1] += 1
    tests.append((lambda:check_table(spec, B), 'Damaged original star equation'))
    ordinary = sectors(spec, table(spec, [Q(0)]*len(values)))
    tests.append((lambda:exact.both(ordinary[0]['upper']),
                  'Omitted full mean cap would miss the rejected ordinary baseline'))
    high = table(spec, values)
    high[spec['middle']][spec['middle']] = Q((-1)**spec['middle']*(-spec['s']-1))
    highest = sectors(spec, high)[spec['middle']]['lower']
    tests.append((lambda:exact.both(highest), 'Highest middle parity cone'))
    return [reject(f, label) for f,label in tests]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--certificate', default=str(HERE/'CERTIFICATE.json'))
    p.add_argument('--output', help='write the complete regenerated mathematical record')
    p.add_argument('--mode', help='write actual runtime flags and whole local source hashes')
    p.add_argument('--check', help='compare every summary field and the entire-record hash')
    a = p.parse_args()
    require(all(os.environ.get(k) == '1' for k in THREADS), 'All six native thread limits one')
    raw = Path(a.certificate).read_bytes()
    seed = json.loads(raw)
    spec, values, result, floors = decode(seed)
    population = population_bound(spec)
    require(result['lower_rank'] == population['greatest_lower_rank_at_class_minimum'],
            'Greatest constrained lower rank is attained')
    audits = dict(original_coordinate_affine=audit_basis(),
                  separate_full_star_triangular=triangular_star_audit(spec),
                  literal_original_mean=literal_control(),
                  literal_original_entries_and_stars=credited_control())
    damaged = damages(seed, spec, values)
    out = dict(agent='six-downset-2', role='researcher',
               status='exact rational original cap attaining five classes and constrained rank263644105 at n28',
               source_status='ordinary author proof; independent review pending; real bridges unformalized',
               rational_certificate_sha256=hashlib.sha256(raw).hexdigest(),
               zero_core_floor_result=result, original_floor_tests=floors,
               original_upper_gap_at_least=rational(seed['original_upper_floor'])/spec['h'],
               lower_floor_scope='chosen complementary planes, not full-space lower eigenvalue floors',
               populations=population, audits=audits, rejected_damages=damaged,
               numerical_proposal_input=False, solver_status_premise=False,
               operational_failure_is_nonexistence=False)
    output = json.dumps(out, indent=2, default=encode)+'\n'
    if a.output:
        Path(a.output).write_text(output)
    summary = dict(agent='six-downset-2', role='researcher', record_bytes=len(output.encode()),
                   record_sha256=hashlib.sha256(output.encode()).hexdigest(),
                   order=28, noncentral_classes=5, saturated_classes=spec['saturated'],
                   saturated_pairs=spec['saturated_pairs'], lower_rank=result['lower_rank'],
                   upper_rank=result['upper_rank'], actual_empty_loop=str(result['actual_empty']['loop']),
                   original_upper_gap_at_least=str(out['original_upper_gap_at_least']),
                   complete_degrees=len(result['sectors']), original_endpoint_floor_tests=len(floors),
                   whole_size_class_subsets=population['whole_size_class_subsets'],
                   unique_seven_absent_classes=population['unique_seven_absent_classes'],
                   affine_audits=audits, rejected_damages=len(damaged),
                   solver_input=False, independently_reviewed=False, real_bridges_formalized=False)
    if a.check:
        require(summary == json.loads(Path(a.check).read_text()),
                'Every expected summary field and the entire regenerated record must match')
    mode = dict(agent='six-downset-2', role='researcher', python=platform.python_version(),
                optimize=sys.flags.optimize, isolated=sys.flags.isolated,
                native_threads={k:os.environ[k] for k in THREADS},
                record_bytes=len(output.encode()), record_sha256=hashlib.sha256(output.encode()).hexdigest(),
                source_sha256={f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in SOURCE})
    if a.mode:
        Path(a.mode).write_text(json.dumps(mode, indent=2)+'\n')
    print(json.dumps(dict(ok=True, expected_checked=bool(a.check), summary=summary,
                         optimize=mode['optimize'], isolated=mode['isolated'])))


if __name__ == '__main__':
    main()
