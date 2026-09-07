#!/usr/bin/env python3
"""Verify the positive-colouring certificate and its finite set-cover proof."""

import base64
from functools import lru_cache
import hashlib
from itertools import combinations
import json
import struct
import zlib


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decode_blob(record):
    require(record["encoding"] == "base85(zlib(binary))", "unknown blob encoding")
    compressed = base64.b85decode(record["data"])
    require(len(compressed) == record["compressed_bytes"], "compressed length")
    decoder = zlib.decompressobj()
    raw = decoder.decompress(compressed) + decoder.flush()
    require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail, "invalid zlib stream")
    require(len(raw) == record["raw_bytes"] and digest(raw) == record["raw_sha256"], "raw blob digest")
    return raw


def unpack_colours(data, offset, active, host_vertices=769):
    count = (len(active) + 3) // 4
    require(offset + count <= len(data), "truncated colour row")
    values = [
        (byte >> shift) & 3
        for byte in data[offset:offset + count]
        for shift in (0, 2, 4, 6)
    ]
    require(all(value == 0 for value in values[len(active):]), "nonzero colour padding")
    word = [-1] * host_vertices
    for vertex, colour in zip(active, values):
        word[vertex] = colour
    return word, offset + count


def check_word(word, active, edges):
    active_set = set(active)
    require(len(active_set) == len(active), "duplicate active vertex")
    require(all(0 <= vertex < len(word) and word[vertex] in range(4) for vertex in active), "colour domain")
    require(
        all(word[left] != word[right] for left, right in edges if left in active_set and right in active_set),
        "monochromatic unit edge",
    )


def minimal_clauses(clauses):
    ordered = sorted(set(clauses), key=lambda clause: (clause.bit_count(), clause))
    kept = []
    for clause in ordered:
        if any(previous & clause == previous for previous in kept):
            continue
        kept.append(clause)
    return tuple(kept)


def uncovered_set(masks, budget, universe_size=260):
    universe = (1 << universe_size) - 1
    clauses = minimal_clauses(tuple(universe ^ mask for mask in masks))

    @lru_cache(maxsize=None)
    def search(remaining, left):
        if not remaining:
            return ()
        if left == 0 or remaining[0] == 0:
            return None
        clause = min(remaining, key=int.bit_count)
        choices = clause
        while choices:
            chosen = choices & -choices
            choices -= chosen
            reduced = minimal_clauses(tuple(other for other in remaining if not other & chosen))
            result = search(reduced, left - 1)
            if result is not None:
                return (chosen.bit_length() - 1,) + result
        return None

    return search(clauses, budget)


def verify(certificate, edges):
    require(certificate["schema"] == 1, "certificate schema")
    require(certificate["host_vertices"] == 769 and certificate["seed_vertices"] == 509, "host order")
    require(certificate["added_vertices"] == 260 and certificate["host_edges"] == len(edges) == 3560, "host size")
    edge_data = json.dumps(edges, separators=(",", ":")).encode()
    require(digest(edge_data) == certificate["host_edges_sha256"], "certificate host digest")

    residual = certificate["residual_seed_vertices"]
    require(
        residual == [113, 114, 184, 186, 346, 349, 366, 367],
        "residual seed boundary",
    )
    residual_set = set(residual)
    pair_boundary = certificate["pair_boundary"]
    require(pair_boundary == [[184, 349], [186, 346]], "pair boundary")
    pairs = [set(pair) for pair in pair_boundary]

    positive = certificate["positive_boundary"]
    ordinary = positive["ordinary_singletons"]
    require(
        ordinary == sorted(set(range(509)) - residual_set)
        and positive["minimal_pairs"] == pair_boundary
        and positive["row_count"] == 503,
        "positive boundary metadata",
    )
    raw = decode_blob(positive["data"])
    offset = 0
    positive_checked = 0
    for deleted in ordinary:
        active = [vertex for vertex in range(769) if vertex != deleted]
        word, offset = unpack_colours(raw, offset, active)
        check_word(word, active, edges)
        positive_checked += 1
    for deleted in pair_boundary:
        deleted_set = set(deleted)
        active = [vertex for vertex in range(769) if vertex not in deleted_set]
        word, offset = unpack_colours(raw, offset, active)
        check_word(word, active, edges)
        positive_checked += 1
    require(offset == len(raw), "unused positive-boundary bytes")

    residual_cases = sorted(
        [
            set(deleted)
            for size in range(1, len(residual) + 1)
            for deleted in combinations(residual, size)
            if not any(pair <= set(deleted) for pair in pairs)
        ],
        key=lambda deleted: (len(deleted), sorted(deleted)),
    )
    maximal = sorted(
        [
            sorted(deleted)
            for deleted in residual_cases
            if not any(deleted < other for other in residual_cases)
        ]
    )
    require(
        len(residual_cases) == 143
        and maximal == sorted(certificate["maximal_residual_patterns"]),
        "residual pattern formula",
    )

    cover = certificate["target_covers"]
    require(cover["case_count"] == len(residual_cases) and cover["row_count"] == len(cover["rows"]) == 15, "cover metadata")
    cover_raw = decode_blob(cover["data"])
    cover_offset = 0
    decoded_rows = []
    universe = set(range(260))
    for metadata in cover["rows"]:
        deleted = metadata["deleted_seed"]
        require(
            deleted == sorted(set(deleted))
            and set(deleted) <= residual_set
            and set(deleted) in residual_cases,
            "cover source deletion",
        )
        require(cover_offset < len(cover_raw), "truncated cover row")
        missing_count = cover_raw[cover_offset]
        cover_offset += 1
        header_bytes = 2 * missing_count
        require(cover_offset + header_bytes <= len(cover_raw), "truncated cover mask")
        missing = list(struct.unpack(f">{missing_count}H", cover_raw[cover_offset:cover_offset + header_bytes]))
        cover_offset += header_bytes
        require(missing == sorted(set(missing)) and set(missing) <= universe, "cover mask domain")
        retained = sorted(universe - set(missing))
        active = [vertex for vertex in range(509) if vertex not in set(deleted)]
        active += [509 + value for value in retained]
        word, cover_offset = unpack_colours(cover_raw, cover_offset, active)
        check_word(word, active, edges)
        decoded_rows.append((set(deleted), sum(1 << value for value in retained)))
    require(cover_offset == len(cover_raw), "unused cover bytes")

    case_checks = []
    for deleted in residual_cases:
        budget = len(deleted) - 1
        masks = [mask for source, mask in decoded_rows if source <= deleted]
        require(masks, "residual case without an applicable row")
        witness = uncovered_set(masks, budget)
        require(witness is None, f"uncovered added-vertex set for {sorted(deleted)}: {witness}")
        case_checks.append(
            {
                "deleted_seed": sorted(deleted),
                "added_vertex_budget": budget,
                "applicable_rows": len(masks),
            }
        )

    result = {
        "all_checks": True,
        "theorem": certificate["theorem"],
        "host_vertices": 769,
        "host_edges": len(edges),
        "positive_rows_checked": positive_checked,
        "ordinary_singleton_rows_checked": len(ordinary),
        "pair_rows_checked": len(pair_boundary),
        "residual_seed_vertices": residual,
        "residual_cases_checked": len(residual_cases),
        "cover_rows_checked": len(decoded_rows),
        "maximum_added_vertex_budget": max(row["added_vertex_budget"] for row in case_checks),
        "target_order": 508,
        "target_found": False,
        "solver_or_unsat_proof_inputs": 0,
    }
    return result
