#!/usr/bin/env python3
"""Malformed-certificate controls for the twisted F29 checker."""

from copy import deepcopy
import json

from verify import HERE, verify_data


def main():
    original = json.loads((HERE / "certificate.json").read_text())
    verify_data(original)
    cases = []

    def add(name, mutate):
        damaged = deepcopy(original)
        mutate(damaged)
        cases.append((name, damaged))

    add("bad_whole_word", lambda d: d.__setitem__("four_colour_word", "0" * 58))
    add("missing_interface_word", lambda d: d["active_interface_extension_words"].pop("011020"))
    add("bad_interface_word", lambda d: d["active_interface_extension_words"].__setitem__("011020", "0" * 58))
    add("bad_point_hash", lambda d: d.__setitem__("points_sha256", "0" * 64))
    add("bad_edge_hash", lambda d: d.__setitem__("edges_sha256", "0" * 64))
    add("bad_cross_edge", lambda d: d["extra_edge_rows"].pop())
    add("bad_interface_edge", lambda d: d["active_interface_edges"].pop())
    add("bad_frame", lambda d: d["w"][0][0].__setitem__(0, -2))
    add("bad_order", lambda d: d.__setitem__("physical_vertices", 57))
    add("bad_neutrality", lambda d: d.__setitem__("active_interface_neutral", False))

    rejected = []
    for name, damaged in cases:
        try:
            verify_data(damaged)
        except (ValueError, KeyError, TypeError, IndexError):
            rejected.append(name)
        else:
            raise RuntimeError(f"malformed control accepted: {name}")

    result = {
        "status": "VERIFIED_TWISTED_F29_CONTROLS",
        "valid_certificate_accepted": True,
        "malformed_controls": len(cases),
        "malformed_rejected": rejected,
    }
    expected = json.loads((HERE / "CONTROLS_EXPECTED.json").read_text())
    if result != expected:
        raise ValueError("control headline mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
