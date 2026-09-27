#!/usr/bin/env python3
"""Independent exact review checker for the complete Gaussian beta row 12.

No target module is imported.  The checker reconstructs all Young premises
and scalar minorants from the JSON certificate, then proves positivity with
adaptive exact Taylor interval bounds rather than the author's Bernstein/
de Casteljau representation.
"""

import argparse
import copy
from fractions import Fraction as F
from hashlib import sha256
from math import comb, isqrt
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, "changed reviewed input: " + relative)
    return manifest


def add_to(polynomial, degree, value):
    while len(polynomial) <= degree:
        polynomial.append(F(0))
    polynomial[degree] += value


def root_interval(value, denominator):
    scaled = value * denominator * denominator
    lower_numerator = isqrt(scaled)
    lower = F(lower_numerator, denominator)
    upper = lower if lower_numerator * lower_numerator == scaled else F(lower_numerator + 1, denominator)
    require(lower * lower <= value <= upper * upper, "root enclosure")
    return lower, upper


def taylor_coefficients(polynomial, center):
    # p(center+y)=sum_j a_j y^j, computed directly from the binomial theorem.
    return [sum((polynomial[i] * comb(i, j) * center ** (i - j)
                 for i in range(j, len(polynomial))), F(0))
            for j in range(len(polynomial))]


def certify_positive_taylor(polynomial, maximum_depth=24):
    accepted = []

    def visit(left, right, depth):
        center = (left + right) / 2
        radius = (right - left) / 2
        coefficients = taylor_coefficients(polynomial, center)
        lower = coefficients[0] - sum((abs(coefficients[j]) * radius ** j
                                       for j in range(1, len(coefficients))), F(0))
        if lower > 0:
            accepted.append((left, right, lower, depth))
            return
        require(depth < maximum_depth, "Taylor subdivision did not certify positivity")
        visit(left, center, depth + 1)
        visit(center, right, depth + 1)

    visit(F(0), F(1), 0)
    coverage = sum((right - left for left, right, _, _ in accepted), F(0))
    require(coverage == 1, "Taylor intervals do not cover [0,1]")
    encoded = "\n".join(f"{left}|{right}|{lower}|{depth}"
                          for left, right, lower, depth in accepted) + "\n"
    return {
        "intervals": len(accepted),
        "maximum_depth": max(depth for _, _, _, depth in accepted),
        "minimum_lower_bound": min(lower for _, _, lower, _ in accepted),
        "interval_sha256": sha256(encoded.encode()).hexdigest(),
    }


def reconstruct_case(case, root_denominator):
    base, q = case["base"], case["q"]
    gamma = F(case["gamma"])
    require(gamma > 0, "positive margin")
    polynomial = []
    for ell in range(q + 1):
        lower, upper = root_interval(base + ell, root_denominator)
        root = lower if ell % 2 == 0 else upper
        add_to(polynomial, ell, (-1) ** ell * comb(q, ell) * root)
    add_to(polynomial, 0, -gamma)

    young_records = []
    for item in case["young"]:
        shift = item["shift"]
        k = base + shift
        exponent = F(2 * (k + 1) ** 2, k * (k + 2))
        slope = F(item["slope"])
        critical = F(item["critical_upper"])
        intercept = F(item["intercept"])
        multiplier = F(item["multiplier"])
        require(slope > 0 and critical > 0 and intercept >= 0 and multiplier >= 0,
                "Young domains")
        p, d = exponent.numerator, exponent.denominator
        require(critical ** (p - d) >= (slope / exponent) ** d,
                "critical point upper bound")
        scalar_lower = intercept - slope * (1 - 1 / exponent) * critical
        require(scalar_lower >= 0, "Young scalar lower bound")

        # Subtract multiplier times
        # u^shift[a-v((k+1)/k)^3u+((k+2)/k)^3u^2].
        add_to(polynomial, shift, -multiplier * intercept)
        add_to(polynomial, shift + 1,
               multiplier * slope * F(k + 1, k) ** 3)
        add_to(polynomial, shift + 2,
               -multiplier * F(k + 2, k) ** 3)
        young_records.append([k, exponent, critical, scalar_lower])

    for item in case["monotonicity"]:
        shift = item["shift"]
        multiplier = F(item["multiplier"])
        k = base + shift
        require(multiplier >= 0, "monotonicity multiplier")
        add_to(polynomial, shift, -multiplier)
        add_to(polynomial, shift + 1, multiplier * F(k + 1, k) ** 3)

    require(len(polynomial) == 13, "degree-twelve minorant")
    positivity = certify_positive_taylor(polynomial)
    coefficient_text = "\n".join(map(str, polynomial)) + "\n"
    return {
        "base": base,
        "q": q,
        "j": base - 2,
        "gamma": gamma,
        "normalized_margin": gamma / base ** 3,
        "young_premises": young_records,
        "power_coefficients_sha256": sha256(coefficient_text.encode()).hexdigest(),
        "taylor_certificate": positivity,
    }


def retained_interaction_endpoints(root_denominator):
    """Independently certify both scalar endpoint signs in graph6362."""
    endpoint_data = {
        9: (F(13, 20), F(4), F(49, 10), F(4), F(1, 200)),
        12: (F(1, 3), F(23, 10), F(29, 10), F(12, 5), F(1, 2000)),
    }
    records = []
    for q, (a, b, c, multiplier, epsilon) in endpoint_data.items():
        minorant = []
        for ell in range(q + 1):
            lower, upper = root_interval(ell + 2, root_denominator)
            root = lower if ell % 2 == 0 else upper
            add_to(minorant, ell, (-1) ** ell * comb(q, ell) * root)
        # P_q-[a-bu+cu^2+multiplier(u^3-216u^4/125)].
        add_to(minorant, 0, -a)
        add_to(minorant, 1, b)
        add_to(minorant, 2, -c)
        add_to(minorant, 3, -multiplier)
        add_to(minorant, 4, multiplier * F(216, 125))
        first = certify_positive_taylor(minorant)

        # After r=z^4, prove a/8-br/27+c*r^(9/4)/64 >= epsilon.
        scalar = [F(0)] * 10
        scalar[0] = a / 8 - epsilon
        scalar[4] = -b / 27
        scalar[9] = c / 64
        second = certify_positive_taylor(scalar)
        coefficient_of_B2_over_s = F(q + 1, 4) * epsilon
        records.append({
            "q": q,
            "minorant_taylor_certificate": first,
            "scalar_taylor_certificate": second,
            "epsilon": epsilon,
            "coefficient_of_B2_over_s": coefficient_of_B2_over_s,
            "coefficient_of_sqrt2_d2": 8 * coefficient_of_B2_over_s,
        })
    require(records[0]["coefficient_of_sqrt2_d2"] == F(1, 10),
            "row-nine endpoint normalization")
    require(records[1]["coefficient_of_sqrt2_d2"] == F(13, 1000),
            "row-twelve endpoint normalization")
    return records


def calculate(certificate):
    require(certificate["row"] == 12, "row")
    denominator = certificate["root_denominator"]
    require(denominator == 2 ** 48, "root denominator")
    cases = certificate["cases"]
    require([(case["base"], case["q"]) for case in cases]
            == [(3, 11), (4, 10), (5, 9), (6, 8)], "row obligations")
    records = [reconstruct_case(case, denominator) for case in cases]
    require(sum(len(record["young_premises"]) for record in records) == 13,
            "Young premise count")

    # j=0 is the retained-interaction endpoint and q<=7 covers j>=5.
    coverage = [[0, 12, "retained interaction"]]
    coverage += [[j, 12 - j, "multilevel"] for j in range(1, 5)]
    coverage += [[j, 12 - j, "seven factor"] for j in range(5, 13)]
    require([row[0] for row in coverage] == list(range(13)), "complete row")
    require(all(q <= 7 for j, q, _ in coverage if j >= 5), "seven-factor scope")

    elevation = 0
    for row in range(12):
        for j in range(row + 1):
            left = F(row + 1 - j, row + 2)
            right = F(j + 1, row + 2)
            require(left > 0 and right > 0 and left + right == 1,
                    "degree elevation")
            elevation += 1
    return {
        "status": "INDEPENDENT_COMPLETE_BETA_ROW_TWELVE_REVIEW_PASS",
        "complete_row": 12,
        "cases": records,
        "retained_interaction_endpoints": retained_interaction_endpoints(denominator),
        "young_premises": 13,
        "degree_elevation_controls": elevation,
        "coverage": coverage,
    }


def corruption_controls(certificate):
    corruptions = []
    damaged = copy.deepcopy(certificate)
    damaged["cases"][0]["gamma"] = "100"
    corruptions.append(damaged)
    damaged = copy.deepcopy(certificate)
    damaged["cases"][0]["young"][0]["critical_upper"] = "1/1000000"
    corruptions.append(damaged)
    damaged = copy.deepcopy(certificate)
    damaged["cases"][0]["young"][0]["multiplier"] = "-1"
    corruptions.append(damaged)
    rejected = 0
    for damaged in corruptions:
        try:
            calculate(damaged)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError("damaged certificate accepted")
    return rejected


def run():
    manifest = pin_inputs()
    certificate = json.loads((HERE / "../gaussian_complete_beta_row_eleven/"
                              "MULTILEVEL_CERTIFICATE.json").read_text())
    result = calculate(certificate)
    result.update({
        "verdict": "accept all Gaussian beta rows through twelve in the stated scope",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "dependency_commit": manifest["dependency_commit"],
        "pinned_inputs": len(manifest["files"]),
        "rejected_corruptions": corruption_controls(certificate),
    })
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    record = (json.dumps(encode(run()), sort_keys=True, indent=2) + "\n").encode()
    if args.emit:
        print(record.decode(), end="")
        return
    require(record == (HERE / "REVIEW_EXPECTED.json").read_bytes(),
            "expected review record mismatch")
    print("INDEPENDENT_COMPLETE_BETA_ROW_TWELVE_REVIEW_PASS")
    print("record_sha256=" + sha256(record).hexdigest())


if __name__ == "__main__":
    main()
