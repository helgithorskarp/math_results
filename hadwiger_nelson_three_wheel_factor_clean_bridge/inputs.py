"""Pinned shared inputs for the residual factor-clean bridge."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "hadwiger_nelson_three_wheel_architecture"
SYMMETRY = ROOT / "hadwiger_nelson_three_wheel_symmetry_frontier"
VIABILITY = ROOT / "hadwiger_nelson_three_wheel_exact_viability"
CLOSURE = ROOT / "hadwiger_nelson_three_wheel_closure"

SOURCE_CERTIFICATE_SHA256 = "7d3813350faffa9e6710cddc44d528a93ece7a1405db28c799974afd38c96e49"
SYMMETRY_CERTIFICATE_SHA256 = "14e2a5e3fc00af36d4ef57b6a8fdd964450633b0ab76f0f2783094172ec69132"
VIABILITY_CERTIFICATE_SHA256 = "a38615f0e6833abe371e7004184db867d8e284979e0468ddfd53e0aff267b4bf"
VIABILITY_VERIFIER_SHA256 = "7431bcda3d460a906efc64e0cbd2d39d64115c6f2a15a92bc89a03b56126383a"
CLOSURE_CERTIFICATE_SHA256 = "301ca9a0ee089dfa10ba1b7d29f4e0a23d2e446a2592101dcd60e6cf2a1e6385"
SURVIVOR_INTERFACE_SHA256 = "5257d702c15b992a4f945aa078cea68545e5b4d1a854c12adde4ae3bcda2a46c"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_symmetry_verifier():
    sys.path.insert(0, str(SYMMETRY))
    spec = importlib.util.spec_from_file_location(
        "hn_factor_clean_symmetry_verify", SYMMETRY / "verify.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def encoded_original_words(source):
    return ["".join(map(str, word)) for _, word in source.colour_words()]


def word_bad_factors(word, allowed, base, inventory):
    need(type(word) is str and len(word) == 343 and set(word) <= set("0123"),
         "four-colour word schema")
    need(all(word[a] != word[b] for a, b in base),
         "word must colour all Cartesian edges")
    bad = set()
    for a, b, factor_ids in inventory:
        if word[a] == word[b]:
            bad.update(factor_ids)
    return bad & allowed


def graph_edges(base, inventory, factor_pair):
    selected = set(factor_pair)
    edges = sorted(base + [(a, b) for a, b, factor_ids in inventory
                           if factor_ids & selected])
    need(len(edges) == len(set(edges)), "distinct reconstructed graph edges")
    return edges


def load():
    dependencies = {
        "source_certificate_sha256": SOURCE_CERTIFICATE_SHA256,
        "symmetry_certificate_sha256": SYMMETRY_CERTIFICATE_SHA256,
        "viability_certificate_sha256": VIABILITY_CERTIFICATE_SHA256,
        "viability_verifier_sha256": VIABILITY_VERIFIER_SHA256,
        "closure_certificate_sha256": CLOSURE_CERTIFICATE_SHA256,
        "survivor_interface_sha256": SURVIVOR_INTERFACE_SHA256,
    }
    checks = {
        SOURCE / "certificate.json": SOURCE_CERTIFICATE_SHA256,
        SYMMETRY / "certificate.json": SYMMETRY_CERTIFICATE_SHA256,
        VIABILITY / "certificate.json": VIABILITY_CERTIFICATE_SHA256,
        VIABILITY / "verify.py": VIABILITY_VERIFIER_SHA256,
        CLOSURE / "certificate.json": CLOSURE_CERTIFICATE_SHA256,
    }
    for path, expected in checks.items():
        need(file_sha256(path) == expected, "dependency hash: " + str(path))

    symmetry_certificate = json.loads((SYMMETRY / "certificate.json").read_text())
    viability_certificate = json.loads((VIABILITY / "certificate.json").read_text())
    closure_certificate = json.loads((CLOSURE / "certificate.json").read_text())
    need(viability_certificate.get("schema") == "hn-three-wheel-exact-viability-v1",
         "viability schema")
    need(closure_certificate.get("version") == 1, "closure schema")

    symmetry = load_symmetry_verifier()
    source, factors, active, _, _ = symmetry.source_state()
    alignment = symmetry.alignment_ids(factors)
    allowed = set(active) - alignment
    need(len(factors) == 990 and len(alignment) == 16 and len(allowed) == 972,
         "factor domains")

    displacements, polynomials = source.input_polynomials()
    source_certificate = json.loads((SOURCE / "certificate.json").read_text())
    factors_again, decomposition = source.factor_check(source_certificate, polynomials)
    need(factors_again == factors, "consistent factor reconstruction")
    base, inventory = source.pair_inventory(displacements, decomposition)
    need(len(base) == 1764 and len(inventory) == 56889, "complete pair inventory")

    words = closure_certificate.get("words")
    need(type(words) is list and len(words) == 62 and len(set(words)) == 62,
         "62 distinct closure words")
    original_words = encoded_original_words(source)
    need(len(original_words) == 13 and words[:13] == original_words,
         "closure extends the original thirteen words")
    bad_sets = [word_bad_factors(word, allowed, base, inventory) for word in words]

    pairs = symmetry_certificate.get("pair_orbit_representatives")
    pair_rows = viability_certificate.get("pair_rows")
    need(type(pairs) is list and type(pair_rows) is list
         and len(pairs) == len(pair_rows) == 800, "800-system dependency interface")
    survivors = []
    for pair_index, (pair, row) in enumerate(zip(pairs, pair_rows)):
        need(row.get("pair") == pair, "viability pair order")
        for component in row.get("components", []):
            if component.get("outcome") != "survivor":
                continue
            need(component.get("zero_factor_ids") == pair,
                 "survivor defining-factor interface")
            survivors.append({
                "pair_index": pair_index,
                "factor_pair": list(pair),
                "shear": row["shear"],
                "relation_a": row["relation_a"],
                "relation_b": row["relation_b"],
                "polynomial": component["polynomial"],
                "real_intervals": component["intervals"],
            })
    need(len(survivors) == 15 and sum(len(row["real_intervals"])
                                     for row in survivors) == 48,
         "15-component 48-embedding survivor interface")
    need(len({row["pair_index"] for row in survivors}) == 15,
         "one survivor component per pair system")
    return {
        "dependencies": dependencies,
        "factors": factors,
        "allowed": sorted(allowed),
        "base": base,
        "inventory": inventory,
        "words": words,
        "bad_sets": bad_sets,
        "survivors": survivors,
    }
