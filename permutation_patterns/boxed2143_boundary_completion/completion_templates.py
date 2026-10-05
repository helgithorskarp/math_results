"""Minimal word utilities for the reviewed completion/obstruction replays.

The two function bodies are copied unchanged from the frozen dependency.
Unused exploratory template rules are omitted; see PORTABILITY_EDITS.json.
"""

from __future__ import annotations
from collections.abc import Sequence
from definition_checker import validate_permutation


def standardize(values: Sequence[int]) -> tuple[int, ...]:
    if len(set(values)) != len(values):
        raise ValueError("standardize needs distinct entries")
    ranks = {value: rank + 1 for rank, value in enumerate(sorted(values))}
    return tuple(ranks[v] for v in values)


def interleave(p: Sequence[int], rho: Sequence[int]) -> tuple[int, ...]:
    p = validate_permutation(p)
    rho = validate_permutation(rho)
    if not p or len(rho) != len(p) - 1:
        raise ValueError("Need m>=1 and rho in S_(m-1)")
    result = []
    for i, value in enumerate(p):
        result.append(2 * value - 1)
        if i < len(rho):
            result.append(2 * rho[i])
    result = tuple(result)
    validate_permutation(result)
    # Recovery uses every other position and odd ranks; it does not assume that
    # an arbitrary deletion from a boxed avoider preserves avoidance.
    if tuple((v + 1) // 2 for v in result[::2]) != p:
        raise RuntimeError("Completion lost recovery of its input")
    return result
