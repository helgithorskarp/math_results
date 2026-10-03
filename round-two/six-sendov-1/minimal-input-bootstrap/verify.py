"""Portable whole-record verifier; actual six-sendov-1 / researcher."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("bootstrap_arithmetic", BASE / "arithmetic.py")
arithmetic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arithmetic)
VerificationError = arithmetic.VerificationError
SOURCE_FILES = (
    ".gitignore", "PROOF.md", "README.md", "LITERATURE.md", "dependencies.json",
    "arithmetic.py", "verify.py", "validate.py", "EXPECTED.json",
)


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise VerificationError("nonfinite JSON constant: " + value)


def load_record(raw):
    try:
        return json.loads(raw, object_pairs_hook=no_duplicates, parse_constant=reject_constant)
    except (ValueError, UnicodeError) as error:
        raise VerificationError("malformed external record") from error


def compare_record(actual, expected, path="record"):
    """Require the complete recursively typed record, including every coefficient."""
    if type(actual) is not type(expected):
        raise VerificationError("record type differs at " + path)
    if isinstance(actual, dict):
        if actual.keys() != expected.keys():
            raise VerificationError("record keys differ at " + path)
        for key in actual:
            compare_record(actual[key], expected[key], path + "." + key)
    elif isinstance(actual, list):
        if len(actual) != len(expected):
            raise VerificationError("record length differs at " + path)
        for index, (left, right) in enumerate(zip(actual, expected)):
            compare_record(left, right, path + "[" + str(index) + "]")
    elif actual != expected:
        raise VerificationError("record value differs at " + path)


def verify_sources(base=BASE):
    manifest = load_record((base / "MANIFEST.json").read_bytes())
    if type(manifest) is not dict or manifest.get("schema") != 1:
        raise VerificationError("manifest schema")
    files = manifest.get("files")
    if type(files) is not dict or set(files) != set(SOURCE_FILES):
        raise VerificationError("manifest file census")
    for name in SOURCE_FILES:
        raw = (base / name).read_bytes()
        wanted = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        compare_record(wanted, files[name], "manifest." + name)


def validation_batch(record):
    """Mathematical failures use no fixture; external checks use the normal API."""
    math_rejections = {}
    for name in arithmetic.DAMAGE_CASES:
        try:
            arithmetic.build_record(name)
        except VerificationError as error:
            math_rejections[name] = str(error)
        else:
            raise VerificationError("mathematical damage accepted: " + name)

    mutations = {}
    def variant(name, change):
        damaged = copy.deepcopy(record)
        change(damaged)
        mutations[name] = canonical(damaged)

    variant("last-identity-coefficient", lambda x: x["algebra"]["identities"][-1]["left"][-1].__setitem__(1, "0"))
    variant("missing-last-identity", lambda x: x["algebra"]["identities"].pop())
    variant("missing-last-margin", lambda x: x["scalars"]["margins"].pop("a3_loss_eta4_coefficient"))
    variant("extra-field", lambda x: x.__setitem__("unproved", True))
    variant("wrong-type-count", lambda x: x["algebra"].__setitem__("identity_count", 13.0))
    variant("bool-is-not-int", lambda x: x["algebra"].__setitem__("identity_count", True))
    variant("margin-bool-is-not-int", lambda x: x["scalars"]["margins"]["direct_W5"].__setitem__("positive", 1))
    variant("fraction-is-not-float", lambda x: x["scalars"]["margins"]["final_mean_exact_square"].__setitem__("value", 0.0))
    variant("removed-failed-target", lambda x: x["scalars"]["rejected_receiving_targets"].pop("OLD_W5_tau1over60_squared"))
    variant("changed-domain", lambda x: x.__setitem__("domain", "unproved larger interval"))
    mutations.update({
        "empty-object": b"{}", "top-list": b"[]", "invalid-json": b"{",
        "duplicate-key": b'{"schema":1,"schema":1}', "nonfinite": b'{"schema":NaN}',
        "null": b"null", "invalid-UTF8": b"\xff",
    })
    external_rejections = {}
    for name, raw in mutations.items():
        try:
            compare_record(record, load_record(raw))
        except VerificationError as error:
            external_rejections[name] = str(error)
        else:
            raise VerificationError("external damage accepted: " + name)

    # The entire source census is copied; only one pin is then altered.
    with tempfile.TemporaryDirectory(prefix="bootstrap-pins-") as directory:
        temporary = Path(directory)
        for name in SOURCE_FILES + ("MANIFEST.json",):
            shutil.copyfile(BASE / name, temporary / name)
        verify_sources(temporary)
        target = temporary / "arithmetic.py"
        target.write_bytes(target.read_bytes() + b"\n")
        try:
            verify_sources(temporary)
        except VerificationError:
            source_pin_rejected = True
        else:
            raise VerificationError("source-byte damage accepted")
    return {
        "mathematical_rejections": math_rejections,
        "external_rejections": external_rejections,
        "source_pin_rejected": source_pin_rejected,
        "scope": "Same-author implementation validation, not independent review or formal proof",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=BASE / "EXPECTED.json")
    parser.add_argument("--emit-record", action="store_true")
    parser.add_argument("--validation-batch", action="store_true")
    parser.add_argument("--damage", choices=arithmetic.DAMAGE_CASES)
    args = parser.parse_args()
    try:
        verify_sources()
        record = arithmetic.build_record(args.damage)
        compare_record(record, load_record(args.fixture.read_bytes()))
        if args.validation_batch:
            record = {"record": record, "validation": validation_batch(record)}
        if args.emit_record:
            print(canonical(record).decode())
        else:
            print(json.dumps({
                "whole_record_sha256": hashlib.sha256(canonical(record)).hexdigest(),
                "whole_typed_match": True, "scalar_margins": 35,
                "whole_identities": 13, "left_monomials": 117,
                "status": "Ordinary alternative proof; unformalized, independently unreviewed",
            }, sort_keys=True))
    except (VerificationError, OSError) as error:
        print("Verification rejected: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
