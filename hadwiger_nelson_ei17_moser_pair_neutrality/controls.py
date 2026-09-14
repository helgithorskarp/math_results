"""Rejection controls for the independent certificate checker."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

from verify import HERE, need, verify_certificate


def rejected(certificate, label):
    try:
        verify_certificate(certificate)
    except (ValueError, KeyError, TypeError):
        return label
    raise ValueError(f"control accepted: {label}")


def main():
    source = json.loads((HERE / "certificate.json").read_text())
    labels = []

    damaged = deepcopy(source)
    damaged["graph_sha256"] = "0" * 64
    labels.append(rejected(damaged, "graph_hash"))

    damaged = deepcopy(source)
    damaged["dependency_sha256"]["seed.py"] = "0" * 64
    labels.append(rejected(damaged, "dependency_hash"))

    damaged = deepcopy(source)
    damaged["collision_classes"][0][0] += 1
    labels.append(rejected(damaged, "collision_class"))

    damaged = deepcopy(source)
    damaged["words"] = damaged["words"][:-1]
    labels.append(rejected(damaged, "missing_relation_word"))

    damaged = deepcopy(source)
    word = list(damaged["words"][0])
    a, b = (0, 1)
    word[b] = word[a]
    damaged["words"][0] = "".join(word)
    labels.append(rejected(damaged, "monochromatic_unit_edge"))

    print(json.dumps({"rejected_controls": len(labels), "labels": labels}, sort_keys=True))


if __name__ == "__main__":
    main()
