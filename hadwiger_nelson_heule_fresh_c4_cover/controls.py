#!/usr/bin/env python3
"""Negative controls for the fresh-C4 certificate checker."""
from copy import deepcopy
from pathlib import Path
import base64
import json

import verify


HERE = Path(__file__).resolve().parent


def rejected(data):
    try:
        verify.validate(data)
    except (ValueError, TypeError, KeyError):
        return True
    return False


def main():
    source = json.loads((HERE / "certificate.json").read_text())
    controls = []

    data = deepcopy(source)
    data["centre_ids"][0] = 0
    controls.append(rejected(data))

    data = deepcopy(source)
    data["packed_singleton_words"].pop()
    controls.append(rejected(data))

    data = deepcopy(source)
    words = [
        verify.decode_packed(row, data["vertices"])
        for row in data["packed_singleton_words"]
    ]
    _, edges, _, _ = verify.source_graph()
    a, b = next((a, b) for a, b in edges if 0 not in (a, b))
    corrupt = list(words[0])
    corrupt[b] = corrupt[a]
    words[0] = tuple(corrupt)
    data["packed_singleton_words"][0] = verify.pack(corrupt)
    data["word_stream_sha256"] = verify.word_hash(words)
    controls.append(rejected(data))

    data = deepcopy(source)
    raw = bytearray(base64.b64decode(data["packed_singleton_words"][0]))
    raw[-1] |= 0x10
    data["packed_singleton_words"][0] = base64.b64encode(raw).decode("ascii")
    controls.append(rejected(data))

    if not all(controls):
        raise AssertionError(controls)
    print(json.dumps({"status": "PASS", "malformed_controls_rejected": len(controls)}, sort_keys=True))


if __name__ == "__main__":
    main()
