#!/usr/bin/env python3
"""Malformed-evidence controls for the exact checker."""

from copy import deepcopy
import json

from verify import HERE, verify


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    expected = json.loads((HERE / "expected.json").read_text())
    verify(certificate, expected)
    rejected = []

    def reject(name, certificate_mutation=None, expected_mutation=None):
        bad_certificate = deepcopy(certificate)
        bad_expected = deepcopy(expected)
        if certificate_mutation:
            certificate_mutation(bad_certificate)
        if expected_mutation:
            expected_mutation(bad_expected)
        try:
            verify(bad_certificate, bad_expected)
        except ValueError as error:
            rejected.append({"case": name, "reason": str(error)})
        else:
            raise ValueError("accepted malformed evidence: " + name)

    reject("monochromatic relation word",
           certificate_mutation=lambda x: x["centre_relation"].update(
               {"000": "0" * 33}))
    reject("wrong centre pattern",
           certificate_mutation=lambda x: x["centre_relation"].update(
               {"001": x["centre_relation"]["000"]}))
    reject("nontriangle",
           certificate_mutation=lambda x: x.update({"triangle": [0, 1, 2]}))
    reject("wrong physical order",
           expected_mutation=lambda x: x.update({"physical_points": 34}))
    reject("wrong edge hash",
           expected_mutation=lambda x: x.update({"edge_sha256": "0" * 64}))
    print(json.dumps({"verified": True, "rejected": rejected,
                      "rejection_count": len(rejected)},
                     sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()

