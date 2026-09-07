"""Produce the complete separator arithmetic certificate; no graph solver."""
import json

ORDER = {1: 4, 2: 13, 3: 24}
CONTACT = {10: 24, 11: 13, 12: 4, 13: 0}


def certificate():
    rows = []
    for s in range(21):
        for a in range(2, (43 - s) // 2 + 1):
            b = 43 - s - a
            for p in range(1, 4):
                for q in range(1, 5 - p):
                    if a > ORDER[p] or b > ORDER[q]:
                        continue
                    row = dict(s=s, a=a, b=b, alpha_a=p, alpha_b=q)
                    if p == 1 or q == 1:
                        k = a if p == 1 else b
                        if k < 4:
                            common = k * (18 - k + 1) - (k - 1) * s
                            limit = {2: 13, 3: 4}[k]
                            if common <= limit:
                                raise ValueError("unresolved clique case")
                            row.update(status="EXCLUDED", rule="common_neighbors",
                                       lower=common, upper=limit)
                        else:
                            lower = 2 * 18 - 14
                            if s >= lower:
                                raise ValueError("unresolved K4 case")
                            row.update(status="EXCLUDED", rule="K4_contact_types",
                                       required_separator=lower)
                    else:
                        capacity = CONTACT[a] + CONTACT[b]
                        if capacity < s:
                            row.update(status="EXCLUDED", rule="contact_cover",
                                       capacity=capacity)
                        else:
                            if (s, a, b) != (20, 10, 13):
                                raise ValueError("unexpected residual profile")
                            row.update(status="NECESSARY_RESIDUAL_ONLY",
                                       rule="contact_cover_and_degree",
                                       capacity=capacity, maximum_minimum_degree=264 // 13)
                    rows.append(row)
    return {"n": 43, "maximum_separator": 20,
            "external_bound": "R(4,5)<=25", "cases": rows}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
