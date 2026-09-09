#!/usr/bin/env python3
"""Direct-edge verifier for the exact-four concurrence certificate."""
from collections import defaultdict
from itertools import product
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "hadwiger_nelson_complex_radix_architecture"
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(HERE))
import common  # noqa: E402

spec = importlib.util.spec_from_file_location("architecture_concurrence_verifier", SOURCE / "verify.py")
ARCH = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ARCH)


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fmul(a, b):
    a0, a1 = a & 1, (a >> 1) & 1
    b0, b1 = b & 1, (b >> 1) & 1
    return (a0 * b0 ^ a1 * b1) | (
        (a0 * b1 ^ a1 * b0 ^ a1 * b1) << 1
    )


def finv(value):
    common.need(value != 0, "zero F4 inverse")
    return next(candidate for candidate in (1, 2, 3) if fmul(value, candidate) == 1)


def dot(normal, word):
    result = 0
    for left, right in zip(normal, word):
        result ^= fmul(left, right)
    return result


def projective(normal, constant):
    pivot = next(value for value in normal if value)
    scale = finv(pivot)
    return tuple(fmul(scale, value) for value in normal), fmul(scale, constant)


def direct_buckets(factors, factor_edges, base, circle):
    words = tuple(product(range(4), repeat=4))
    digit_residue = (0, 1, 2)
    colourings = []
    for tail in words:
        weights = (1,) + tail
        colouring = []
        for label in ARCH.G.LABELS:
            value = 0
            for weight, digit in zip(weights, label):
                value ^= fmul(weight, digit_residue[digit])
            colouring.append(value)
        colourings.append(tuple(colouring))
    common.need(
        all(colouring[a] != colouring[b] for colouring in colourings for a, b in base),
        "universal edge failed an additive F4 colouring",
    )
    failure_masks = []
    for edges in factor_edges:
        mask = 0
        for i, colouring in enumerate(colourings):
            if any(colouring[a] == colouring[b] for a, b in edges):
                mask |= 1 << i
        failure_masks.append(mask)

    normals = sorted(
        {
            projective(normal, 0)[0]
            for normal in product(range(4), repeat=4)
            if any(normal)
        }
    )
    signatures = [(normal, constant) for normal in normals for constant in range(4)]
    masks = {}
    for signature in signatures:
        mask = 0
        for i, word in enumerate(words):
            if dot(signature[0], word) == signature[1]:
                mask |= 1 << i
        masks[mask] = signature
    common.need(len(masks) == 340, "affine F4 hyperplane masks are not distinct")

    torus_mask = 0
    for i, word in enumerate(words):
        if all(word):
            torus_mask |= 1 << i
    common.need(
        failure_masks[circle] == ((1 << 256) - 1) ^ torus_mask,
        "circle failure mask mismatch",
    )
    buckets = defaultdict(lambda: defaultdict(list))
    curve_constant = {}
    for curve, mask in enumerate(failure_masks):
        if curve == circle:
            continue
        common.need(mask in masks, f"curve {curve} is not one affine hyperplane")
        normal, constant = masks[mask]
        buckets[normal][constant].append(curve)
        curve_constant[curve] = constant
    missing = sorted(set(signatures) - {
        (normal, constant)
        for normal, sections in buckets.items()
        for constant in sections
    })
    common.need(
        missing == [
            ((0, 0, 0, 1), 0),
            ((0, 0, 1, 0), 0),
            ((0, 1, 0, 0), 0),
            ((1, 0, 0, 0), 0),
        ],
        "unexpected unrealized hyperplane types",
    )
    buckets = {
        normal: {constant: curves for constant, curves in sections.items()}
        for normal, sections in buckets.items()
    }
    return buckets, curve_constant


def precheck_certificate(certificate):
    common.need(certificate.get("schema") == "hn-complex-radix-four-concurrence-v1", "certificate schema")
    result = certificate.get("result", {})
    common.need(common.is_prime(result.get("prime", 0)), "certificate modulus is not prime")
    common.need(result.get("projection_slopes") == [2, 3, 4], "projection slopes")
    primary = result.get("primary", {})
    common.need(
        primary.get("survivor_sha256") == common.digest(primary.get("survivors", [])),
        "primary survivor digest",
    )
    common.need(
        sum(map(int, primary.get("gcd_degree_histogram", {}).values()))
        == result.get("eligible_no_circle_quartets"),
        "primary gcd histogram total",
    )
    active = primary.get("survivors", [])
    for index, stage in enumerate(result.get("secondary", [])):
        common.need(stage.get("input_count") == len(active), f"secondary input count {index}")
        common.need(
            stage.get("survivor_sha256") == common.digest(stage.get("survivors", [])),
            f"secondary survivor digest {index}",
        )
        common.need(
            sum(map(int, stage.get("gcd_degree_histogram", {}).values())) == len(active),
            f"secondary gcd histogram total {index}",
        )
        active = stage.get("survivors", [])
    common.need(result.get("final_survivors") == active, "final survivor list")
    common.need(result.get("all_eligible_quartets_excluded") == (not active), "exclusion flag")


def actual(certificate, processes):
    precheck_certificate(certificate)
    rows, events, factors, factor_edges, base, _, _, circle = ARCH.build()
    common.need(
        certificate["sources"]["architecture_certificate_sha256"]
        == file_sha256(SOURCE / "certificate.json"),
        "architecture certificate hash",
    )
    four_interface = ROOT / "hadwiger_nelson_complex_radix_four_curve_gate" / "exact_four_interface.json"
    common.need(
        certificate["sources"]["four_curve_interface_sha256"] == file_sha256(four_interface),
        "h4135 interface hash",
    )
    common.need(
        certificate["sources"]["factor_inventory_sha256"] == ARCH.digest(factors),
        "factor inventory hash",
    )
    buckets, curve_constant = direct_buckets(factors, factor_edges, base, circle)
    factor_ids = {factor: i for i, factor in enumerate(factors)}
    representatives = {}
    for row, event in zip(rows, events):
        if event:
            representatives.setdefault(factor_ids[event], row)
    curve_k = {
        curve: max(i for i, digit in enumerate(representatives[curve]) if digit != (0, 0))
        for curve in range(len(factors))
        if curve != circle
    }
    result = common.run_sieve(
        factors,
        curve_k,
        curve_constant,
        buckets,
        certificate["result"]["prime"],
        processes,
    )
    common.need(result == certificate["result"], "certificate result mismatch")
    return {
        "status": "ALL_EXACT_FOUR_NONCIRCLE_COVER_QUARTETS_NONCONCURRENT",
        "prime": result["prime"],
        "active_noncircle_curves": len(factors) - 1,
        "covering_signature_normals": result["covering_signature_normals"],
        "eligible_curve_quartets": result["eligible_no_circle_quartets"],
        "primary_pair_resultants": result["primary"]["distinct_pair_resultants"],
        "primary_modular_survivors": len(result["primary"]["survivors"]),
        "slope3_survivors": len(result["secondary"][0]["survivors"]),
        "slope4_survivors": len(result["secondary"][1]["survivors"]),
        "minimum_active_curves_for_injective_nonfour_after_h4139": 5,
        "proof_CAS_calls": 0,
        "proof_solver_calls": 0,
        "record_improvement": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--processes", type=int, default=1)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    result = actual(certificate, args.processes)
    if args.check_expected:
        common.need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
