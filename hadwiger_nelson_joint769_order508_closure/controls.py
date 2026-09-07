#!/usr/bin/env python3
"""Small positive and negative controls for the compact certificate decoder."""

import copy
import hashlib
import json
from pathlib import Path
import zlib
import base64

import verify


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rejected(operation):
    try:
        operation()
    except Exception:
        return True
    return False


def encoded(raw):
    compressed = zlib.compress(raw, 9)
    return {
        "encoding": "base85(zlib(binary))",
        "raw_bytes": len(raw),
        "compressed_bytes": len(compressed),
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "data": base64.b85encode(compressed).decode(),
    }


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    positive = certificate["positive_boundary"]["data"]
    require(len(verify.decode_blob(positive)) == 96576, "positive decode control")

    bad_digest = copy.deepcopy(positive)
    bad_digest["raw_sha256"] = "0" * 64
    require(rejected(lambda: verify.decode_blob(bad_digest)), "bad digest accepted")
    bad_length = copy.deepcopy(positive)
    bad_length["raw_bytes"] += 1
    require(rejected(lambda: verify.decode_blob(bad_length)), "bad length accepted")
    require(
        rejected(lambda: verify.unpack_colours(bytes([4]), 0, [0])),
        "nonzero padding accepted",
    )

    # With three ground elements, these two retained masks have disjoint
    # one-point complements, so no one-point set can evade both rows.
    require(verify.uncovered_set([0b110, 0b101], 1, 3) is None, "cover control")
    witness = verify.uncovered_set([0b110, 0b100], 1, 3)
    require(witness == (0,), "uncovered-set witness control")

    trailing = encoded(b"control")
    trailing["data"] = base64.b85encode(base64.b85decode(trailing["data"]) + b"tail").decode()
    trailing["compressed_bytes"] += 4
    require(rejected(lambda: verify.decode_blob(trailing)), "trailing zlib data accepted")

    result = {
        "all_checks": True,
        "positive_decode": True,
        "malformed_digest_rejected": True,
        "malformed_length_rejected": True,
        "nonzero_padding_rejected": True,
        "finite_cover_positive_control": True,
        "finite_cover_negative_control": True,
        "trailing_data_rejected": True,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
