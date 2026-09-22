"""Non-rigorous decimal diagnostics from exact finite counts; not proof bounds."""

from fractions import Fraction
import json
from math import exp, pi, sqrt

from counts import catalan, distance_count, distance_terms, joint_count


def exact_tv(n, d):
    m = d-1
    terms = distance_terms(n, d)
    f = sum(b*g for _, b, g in terms)
    q = 2**(2*m-1)
    # P and Q have the same conditional law of (X,Y) given S. Therefore
    # TV of the pairs equals TV of the one-dimensional S marginal.
    return Fraction(sum(b*abs(q*g-f) for _, b, g in terms), 2*f*q)


def nearest_parity(value, parity):
    return 2*round((value-parity)/2)+parity


def main():
    rows = []
    for n in (100, 400, 1600, 6400):
        for nominal_r in (0.5, 1.0, 2.0):
            d = round(nominal_r*sqrt(n))
            m, length = d-1, n-d-1
            r = d/sqrt(n)
            cat = catalan(n)
            distance_probability = float(Fraction(distance_count(n, d), cat))
            distance_prediction = r*r*exp(-r*r)/(4*sqrt(pi*n))
            local = []
            for nominal_h, nominal_k in ((0, 0), (1, 0), (1, -1)):
                h = nearest_parity(nominal_h*n**0.25, length % 2)
                k = nearest_parity(nominal_k*n**0.25, n % 2)
                x, y = (m+k+h)//2, (m+k-h)//2
                u, v = h/n**0.25, k/n**0.25
                actual = float(Fraction(joint_count(n, d, x, y), cat))
                prediction = r*exp(-r*r-(u*u+v*v)/r)/(pi**1.5*n)
                local.append({"h": h, "k": k,
                              "finite_atom_feasible": actual > 0,
                              "actual_over_local_prediction": round(actual/prediction, 9)})
            tv = float(exact_tv(n, d))
            rows.append({"n": n, "d": d,
                         "total_variation": round(tv, 12),
                         "sqrt_n_times_total_variation": round(sqrt(n)*tv, 9),
                         "distance_actual_over_prediction": round(
                             distance_probability/distance_prediction, 9),
                         "local_atoms": local})
    print(json.dumps({"status": "FLOATING_POINT_DIAGNOSTICS_NOT_PROOF",
                      "description": "Exact integer counts converted to ordinary decimals; no interval enclosures.",
                      "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
