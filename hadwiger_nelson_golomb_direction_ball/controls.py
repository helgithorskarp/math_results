#!/usr/bin/env python3
"""Negative controls for the Golomb direction-ball certificate verifier."""

import copy
import json

import verify as V


def rejected(certificate):
    try:
        V.verify(certificate)
    except (KeyError, TypeError, ValueError):
        return True
    return False


certificate = json.loads((V.HERE / "certificate.json").read_text())

bad = copy.deepcopy(certificate)
bad["source_extensions"] = bad["source_extensions"][:-1]
V.require(rejected(bad), "incomplete source relation was accepted")

bad = copy.deepcopy(certificate)
bad["equal_cover_words"][0] = "0" * 163
V.require(rejected(bad), "improper equality word was accepted")

bad = copy.deepcopy(certificate)
bad["separating_cover_words"] = bad["separating_cover_words"][:1]
V.require(rejected(bad), "incomplete separation cover was accepted")

bad = copy.deepcopy(certificate)
bad["source_extensions"][0]["word"] = bad["source_extensions"][1]["word"]
V.require(rejected(bad), "wrong source projection was accepted")

print("all four malformed-certificate controls rejected")
