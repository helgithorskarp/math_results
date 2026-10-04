"""Complete finite lattice census by integer specialization and Horner evaluation."""
from pathlib import Path
from math import gcd, isqrt
import argparse
import hashlib
import json
import sys
import time
import context


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ceil_sqrt(n):
    root = isqrt(n)
    return root + (root * root != n)


def decode(rows):
    return {tuple(power): int(value) for power, value in rows}


def specialize(poly, k):
    degree = max(i for i, j in poly)
    powers = [k ** j for j in range(max(j for i, j in poly) + 1)]
    coefficients = [0] * (degree + 1)
    for (i, j), value in poly.items():
        coefficients[i] += value * powers[j]
    return coefficients


def horner(coefficients, q):
    result = 0
    for value in reversed(coefficients):
        result = result * q + value
    return result


def census():
    raw_N, raw_D = (decode(rows) for rows in context.defining_fields())
    content = 0
    for value in list(raw_N.values()) + list(raw_D.values()):
        content = gcd(content, value)
    require(content == 65536, 'Whole original positive integer content')
    N, D = ({power: value // content for power, value in poly.items()} for poly in (raw_N, raw_D))
    require(all(N[a] * content == v for a, v in raw_N.items())
            and all(D[a] * content == v for a, v in raw_D.items()),
            'Every coefficient content division multiplied back')
    rows, counts, exceptions, zero_points, controls = [], [], [], [], {}
    for k in range(7, 128):
        tail = (6 * k - 25 + ceil_sqrt(28 * k * k + 36 * k + 81) + 1) // 2 - 2
        formula = 3 * k - 14 + ceil_sqrt(7 * k * k + 36)
        require(3 * k <= formula <= tail, 'Whole integer classification and credited tail domain')
        n, d = specialize(N, k), specialize(D, k)
        signs, positives = [], []
        for q in range(3 * k, tail):
            numerator, denominator = horner(n, q), horner(d, q)
            require(denominator > 0, 'Every complete finite original denominator positive')
            sign = (numerator > 0) - (numerator < 0)
            norm = (q - 3 * k + 14) ** 2 - 7 * k * k
            row = [k, q, str(numerator), str(denominator), sign, norm]
            rows.append(row)
            signs.append(sign)
            if sign > 0:
                positives.append(q)
            if sign == 0:
                zero_points.append([k, q])
            if (sign > 0) != (q >= formula):
                exceptions.append({'k': k, 'q': q, 'norm': norm,
                                   'actual_residual_sign': sign, 'formula_predicts_positive': q >= formula})
            if (k, q) in ((7, 26), (7, 27), (8, 32)):
                controls[str(k) + ',' + str(q)] = sign
        first = min(positives, default=tail)
        require(signs == sorted(signs), 'Complete finite sign sequence has no hole')
        counts.append({'k': k, 'tail_start': tail, 'proposed_cutoff': formula,
                       'first_positive_q_including_credited_tail': first,
                       'finite_q_start': 3 * k, 'finite_q_stop_exclusive': tail,
                       'finite_pair_count': len(signs), 'negative': signs.count(-1),
                       'zero': signs.count(0), 'positive': signs.count(1),
                       'entire_finite_sign_sequence_nondecreasing': True})
    require(controls == {'7,26': -1, '7,27': 1, '8,32': -1}, 'Prior exact finite controls reproduced')
    require(len(rows) == 19969 and len(counts) == 121, 'Complete declared finite coverage')
    bad_counts = sorted({row['k'] for row in exceptions})
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
            'entire_original_numerator': [[list(a), str(v)] for a, v in sorted(N.items())],
            'entire_original_denominator': [[list(a), str(v)] for a, v in sorted(D.items())],
            'entire_pair_rows_schema': ['k', 'q', 'normalized_original_numerator', 'normalized_original_denominator', 'residual_sign', 'integer_norm'],
            'entire_pair_rows': rows, 'entire_count_classifications': counts,
            'pair_count': len(rows), 'count_count': len(counts),
            'all_original_finite_denominators_positive': True,
            'all_finite_count_sign_sequences_nondecreasing': True,
            'all_zero_residual_pairs': zero_points, 'all_formula_deviations': exceptions,
            'all_deviating_counts': bad_counts,
            'candidate_least_valid_integer_onset_relative_to128_theorem': max(bad_counts, default=6) + 1,
            'prior_baseline_controls': controls,
            'no_absence_inferred_from_zero': True, 'separate_arithmetic_check_pending': True,
            'independent_person_review': False, 'ordinary_original_space_and_tail_bridges_unformalized': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    result = census()
    require(not any(n == 'sympy' or n.startswith('sympy.') for n in sys.modules), 'No CAS in exact census')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, separators=(',', ':'), sort_keys=True) + '\n'
    args.out.write_text(payload)
    print(json.dumps({'completed': result['completed'], 'pairs': result['pair_count'],
                      'counts': result['count_count'], 'all_zero_residual_pairs': result['all_zero_residual_pairs'],
                      'all_formula_deviations': result['all_formula_deviations'],
                      'candidate_least_onset': result['candidate_least_valid_integer_onset_relative_to128_theorem'],
                      'whole_record_SHA256': hashlib.sha256(payload.encode()).hexdigest(),
                      'whole_record_bytes': len(payload.encode()), 'seconds': time.monotonic() - start}), flush=True)


if __name__ == '__main__':
    main()
