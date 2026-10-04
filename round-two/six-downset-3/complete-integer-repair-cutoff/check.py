"""Definition-level point evaluation; never imports the new Horner producer."""
from pathlib import Path
from math import gcd
import argparse
import copy
import hashlib
import json
import sys
import time
import context


def require(condition, message):
    if not condition:
        raise ValueError(message)


def original_rows(rows):
    result = []
    seen = set()
    for exponent, value in rows:
        require(len(exponent) == 2 and all(type(x) is int and x >= 0 for x in exponent),
                'Every original exponent is a nonnegative integer pair')
        exponent = tuple(exponent)
        require(exponent not in seen, 'Original definition has no duplicate monomial')
        coefficient = int(value)
        require(coefficient != 0, 'Original sparse field contains no zero coefficient')
        seen.add(exponent)
        result.append((exponent[0], exponent[1], coefficient))
    return sorted(result)


def powers(base, degree):
    result = [1]
    for _ in range(degree):
        result.append(result[-1] * base)
    return result


def thresholds_by_integer_comparisons(k):
    # q+2 >= (6k-25+sqrt(B))/2 iff L>=0 and L^2>=B.
    # This scans the threshold, rather than using the producer's ceil-sqrt formula.
    B = 28 * k * k + 36 * k + 81
    tail = 3 * k
    while True:
        L = 2 * (tail + 2) - 6 * k + 25
        if L >= 0 and L * L >= B:
            break
        tail += 1
    previous_L = 2 * (tail + 1) - 6 * k + 25
    require(previous_L < 0 or previous_L * previous_L < B,
            'Credited tail starts at the smallest integer satisfying the defining inequality')
    formula = 3 * k
    while (formula - 3 * k + 14) ** 2 < 7 * k * k + 36:
        formula += 1
    require((formula - 3 * k + 13) ** 2 < 7 * k * k + 36,
            'Norm36 integer cutoff is minimal')
    require(3 * k <= formula <= tail, 'The credited positive tail lies above the norm36 cutoff')
    return tail, formula


def direct_sum(poly, q_powers, k_powers):
    # Evaluate RAW defining coefficients first. No specialization or Horner step.
    return sum(coefficient * q_powers[i] * k_powers[j]
               for i, j, coefficient in poly)


def independent_census():
    raw_N, raw_D = (original_rows(rows) for rows in context.defining_fields())
    require(len(raw_N) == 743 and len(raw_D) == 676, 'Every original defining monomial retained')
    content = 0
    for i, j, coefficient in raw_N + raw_D:
        content = gcd(content, abs(coefficient))
    require(content == 65536, 'Independent positive common content')
    normalized_fields = []
    for poly in (raw_N, raw_D):
        normalized = []
        for i, j, coefficient in poly:
            quotient, remainder = divmod(coefficient, content)
            require(remainder == 0 and quotient * content == coefficient,
                    'Every independent original coefficient division multiplied back')
            normalized.append([[i, j], str(quotient)])
        normalized_fields.append(normalized)

    q_degree = max(i for i, j, coefficient in raw_N + raw_D)
    k_degree = max(j for i, j, coefficient in raw_N + raw_D)
    bounds = [(k, *thresholds_by_integer_comparisons(k)) for k in range(7, 128)]
    q_powers = {q: powers(q, q_degree)
                for q in range(21, max(tail for k, tail, formula in bounds))}
    rows, classifications, exceptions, zeros, controls = [], [], [], [], {}
    for k, tail, formula in bounds:
        k_powers = powers(k, k_degree)
        sequence = []
        first = None
        for q in range(3 * k, tail):
            raw_n = direct_sum(raw_N, q_powers[q], k_powers)
            raw_d = direct_sum(raw_D, q_powers[q], k_powers)
            n, n_remainder = divmod(raw_n, content)
            d, d_remainder = divmod(raw_d, content)
            require(n_remainder == 0 and d_remainder == 0
                    and n * content == raw_n and d * content == raw_d,
                    'Every whole point evaluation divided only after the raw sum and multiplied back')
            require(d > 0, 'Every original finite denominator is strictly positive')
            sign = 1 if raw_n > 0 else (-1 if raw_n < 0 else 0)
            norm = (q + 14 - 3 * k) ** 2 - 7 * k ** 2
            rows.append([k, q, str(n), str(d), sign, norm])
            sequence.append(sign)
            if sign == 1 and first is None:
                first = q
            if sign == 0:
                zeros.append([k, q])
            if (raw_n > 0) != (norm >= 36):
                exceptions.append({'k': k, 'q': q, 'norm': norm,
                                   'actual_residual_sign': sign, 'formula_predicts_positive': norm >= 36})
            if k == 7 and q in (26, 27) or k == 8 and q == 32:
                controls[str(k) + ',' + str(q)] = sign
        if first is None:
            first = tail
        require(all(sequence[i] <= sequence[i + 1] for i in range(len(sequence) - 1)),
                'Every adjacent pair in the full finite sign sequence is nondecreasing')
        classifications.append({'k': k, 'tail_start': tail, 'proposed_cutoff': formula,
                                'first_positive_q_including_credited_tail': first,
                                'finite_q_start': 3 * k, 'finite_q_stop_exclusive': tail,
                                'finite_pair_count': tail - 3 * k,
                                'negative': sum(s == -1 for s in sequence),
                                'zero': sum(s == 0 for s in sequence),
                                'positive': sum(s == 1 for s in sequence),
                                'entire_finite_sign_sequence_nondecreasing': True})
        require(first == formula + (k == 8), 'Entire count has the stated exact corrected cutoff')
    require(len(rows) == sum(tail - 3 * k for k, tail, formula in bounds) == 19969,
            'Exhaustive finite lattice rectangle union has exactly19969 points')
    require(len(classifications) == 121 and len({(r[0], r[1]) for r in rows}) == len(rows),
            'All121 counts and every finite pair occur exactly once')
    require(not zeros, 'Every finite residual has a strict sign; no zero interpreted as absence')
    require(exceptions == [{'k': 8, 'q': 32, 'norm': 36, 'actual_residual_sign': -1,
                            'formula_predicts_positive': True}],
            'Exactly the known k8,q32 point is the sole norm36 cutoff exception')
    require(controls == {'7,26': -1, '7,27': 1, '8,32': -1}, 'Prior exact original controls reproduced')
    bad_counts = sorted({r['k'] for r in exceptions})
    return {'actual_agent': 'six-downset-3', 'role': 'researcher', 'completed': True,
            'source_commit': 'c4bf22462f3827ece4baa3205e59675235ff259c',
            'criterion_graph_ref': 'bafkreibz56ugbuasnwnmte34ryziqeurksmlidejla3hubzurgabvje37a',
            'uniform_onset_graph_ref': 'bafkreiakf5vocbqofdzi33xh7r5ozgo6qqgxrraxs7y22teul6p2x63k3e',
            'tail_graph_ref': 'bafkreib7yar37msbxjlyex3zgsyz26p7w7ya5ksnzq4bf3w7xkdqi2itri',
            'exact_finite_domain': 'ALL integer7<=k<=127,3k<=q<T(k),everyZ via credited original criterion',
            'credited_all_q_tail': 'T(k)=ceil((6k-25+sqrt(28k^2+36k+81))/2)-2',
            'proposed_integer_cutoff': 'Q(k)=3k-14+ceil(sqrt(7k^2+36))',
            'raw_positive_integer_content': str(content),
            'all_coefficient_content_divisions_multiplied_back': True,
            'entire_original_numerator': normalized_fields[0],
            'entire_original_denominator': normalized_fields[1],
            'entire_pair_rows_schema': ['k', 'q', 'normalized_original_numerator', 'normalized_original_denominator', 'residual_sign', 'integer_norm'],
            'entire_pair_rows': rows, 'entire_count_classifications': classifications,
            'pair_count': len(rows), 'count_count': len(classifications),
            'all_original_finite_denominators_positive': True,
            'all_finite_count_sign_sequences_nondecreasing': True,
            'all_zero_residual_pairs': zeros, 'all_formula_deviations': exceptions,
            'all_deviating_counts': bad_counts,
            'candidate_least_valid_integer_onset_relative_to128_theorem': max(bad_counts) + 1,
            'prior_baseline_controls': controls,
            'no_absence_inferred_from_zero': True, 'separate_arithmetic_check_pending': True,
            'independent_person_review': False, 'ordinary_original_space_and_tail_bridges_unformalized': True}


def compare(candidate, expected):
    require(type(candidate) is dict and set(candidate) == set(expected), 'Whole mathematical field census')
    for key in expected:
        require(candidate[key] == expected[key], 'Complete mathematical mismatch: ' + key)


def damage_tests(expected):
    tests = {}
    mutations = (
        ('omitted_original_point', lambda x: x['entire_pair_rows'].pop(0)),
        ('duplicate_pair_hiding_omission', lambda x: x['entire_pair_rows'].__setitem__(1, x['entire_pair_rows'][0])),
        ('changed_entire_raw_numerator', lambda x: x['entire_pair_rows'][0].__setitem__(2, str(int(x['entire_pair_rows'][0][2]) + 1))),
        ('changed_entire_denominator', lambda x: x['entire_pair_rows'][0].__setitem__(3, str(int(x['entire_pair_rows'][0][3]) + 1))),
        ('incorrect_tail_ceiling', lambda x: x['entire_count_classifications'][0].__setitem__('tail_start', x['entire_count_classifications'][0]['tail_start'] + 1)),
        ('suppressed_norm36_exception', lambda x: x['all_formula_deviations'].clear()),
        ('incorrect_minimum_onset', lambda x: x.__setitem__('candidate_least_valid_integer_onset_relative_to128_theorem', 8)),
        ('zero_residual_misinterpreted_as_absence', lambda x: x.__setitem__('no_absence_inferred_from_zero', False)),
        ('wrong_quantified_domain', lambda x: x.__setitem__('exact_finite_domain', 'sampled counts only')),
        ('missing_original_polynomial_coefficient', lambda x: x['entire_original_numerator'].pop()),
    )
    for name, mutation in mutations:
        altered = copy.deepcopy(expected)
        mutation(altered)
        try:
            compare(altered, expected)
        except ValueError:
            tests[name] = 'rejected'
        else:
            raise ValueError('Semantic damage accepted: ' + name)
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    expected = independent_census()
    compare(json.loads(args.input.read_text()), expected)
    damages = damage_tests(expected)
    require(not any(n == 'probe' or n == 'sympy' or n.startswith('sympy.') for n in sys.modules),
            'Checker never imports the new producer or a CAS')
    expected_bytes = (json.dumps(expected, separators=(',', ':'), sort_keys=True) + '\n').encode()
    require(expected_bytes == args.input.read_bytes(), 'Entire canonical arithmetic record byte equality')
    output = {'completed': True, 'actual_agent': 'six-downset-3', 'role': 'researcher',
              'whole_point_record_SHA256': hashlib.sha256(expected_bytes).hexdigest(),
              'whole_point_record_bytes': len(expected_bytes),
              'every_original_coefficient_and_every_point_value_compared': True,
              'direct_raw_monomial_evaluation_before_positive_content_division': True,
              'independent_integer_threshold_scans': True,
              'new_producer_never_imported': True, 'semantic_damages': damages,
              'entire_independently_evaluated_census': expected,
              'integer_cutoff_onset_9_and_single_k8_exception_arithmetically_checked': True,
              'independent_person_review': False, 'ordinary_completeness_bridges_unformalized': True}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(output, separators=(',', ':'), sort_keys=True) + '\n'
    args.out.write_text(payload)
    print(json.dumps({'completed': True, 'pairs': expected['pair_count'],
                      'counts': expected['count_count'], 'damages_rejected': len(damages),
                      'census_SHA256': output['whole_point_record_SHA256'],
                      'checked_record_SHA256': hashlib.sha256(payload.encode()).hexdigest(),
                      'checked_record_bytes': len(payload.encode()),
                      'seconds': time.monotonic() - start}), flush=True)


if __name__ == '__main__':
    main()
