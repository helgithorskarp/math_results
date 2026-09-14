#!/usr/bin/env python3
"""Cross-representation and certificate-corruption controls."""

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


producer = load("reciprocal_producer", HERE / "produce.py")
checker = load("reciprocal_checker", HERE / "verify.py")


def rejected(certificate, expected):
    try:
        checker.verify(certificate, expected)
    except (ValueError, TypeError, KeyError, IndexError):
        return True
    return False


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    expected = json.loads((HERE / "expected.json").read_text())
    checker_report = checker.verify(certificate, expected)

    points, producer_addresses, producer_edges, producer_terminals = producer.geometry()
    checker_addresses, checker_edges, checker_terminals = checker.geometry()
    if producer_addresses != checker_addresses:
        raise ValueError("address-order disagreement")
    if producer_edges != checker_edges:
        raise ValueError("entry-level edge disagreement")
    if producer_terminals != checker_terminals:
        raise ValueError("terminal disagreement")
    encoded = [producer.encode_field(point) for point in points]
    if encoded != certificate["coordinates"]:
        raise ValueError("coordinate disagreement")

    regenerated = producer.produce()
    if regenerated != certificate:
        raise ValueError("certificate is not byte-structurally reproducible")

    corruptions = []
    bad = copy.deepcopy(certificate)
    bad["coordinates"][1][0][0] += 1
    corruptions.append(rejected(bad, expected))
    bad = copy.deepcopy(certificate)
    first = str((int(bad["three_colour_word"][0]) + 1) % 3)
    bad["three_colour_word"] = first + bad["three_colour_word"][1:]
    corruptions.append(rejected(bad, expected))
    bad = copy.deepcopy(certificate)
    bad["terminal_rows"][0]["word"] = "0" * 211
    corruptions.append(rejected(bad, expected))
    bad = copy.deepcopy(certificate)
    bad["terminal_rows"].pop()
    corruptions.append(rejected(bad, expected))
    if not all(corruptions):
        raise ValueError("accepted corrupted certificate")

    report = {
        "all_checks": True,
        "cross_representation_vertices": len(points),
        "cross_representation_edges": len(producer_edges),
        "entry_level_edge_agreement": True,
        "byte_structural_regeneration": True,
        "corruptions_rejected": sum(corruptions),
        "checker_report": checker_report,
    }
    print(checker.dump(report), end="")


if __name__ == "__main__":
    main()
