# Certified upper bound `S(2,30) <= 8,794,991`

This directory proves a new unrestricted upper bound for the maximum size of a
binary length-30 non-overlapping code:

```
7,555,935 <= S(2,30) <= 8,794,991.
```

The lower endpoint is the construction reported by Stanovnik, Moškon, and
Mraz.  Their previous upper endpoint was 13,390,727.  The proof leaves four
lower recurrence layers symbolic, enumerates every compatible pure-upper
orientation pattern, and bounds each resulting exact quadratic over a
certified integer box.  See [proof.md](proof.md).

## Files

- `quadratic_box_bound.cpp`: exact symbolic recurrence enumerator.  It supports
  deterministic prefix-ordinal shards.
- `verify.py`: independent Python interpolation and definition-level checker.
- `run_shards.py`: launches, parses, validates, and merges disjoint proof
  shards.
- `expected_n30.json`: compact complete coverage ledger and shard maxima.
- `proof.md`: mathematical reduction, inequality, coverage proof, result, and
  scope.

## Quick verification

Python 3.11 or later and a C++20 compiler are required; no third-party package
is used.

```sh
make check
make sanitize
```

The quick check exhausts generic quadratic boxes, independently reconstructs
complete smaller recurrence cases, validates C++ summaries through length 28,
and verifies a small monolithic-versus-sharded identity.  The sanitizer target
uses GCC AddressSanitizer and UndefinedBehaviorSanitizer on a complete tree.

## Full length-30 proof

```sh
make proof30
```

This launches twelve process-isolated shards and checks their merged output
against `expected_n30.json`.  On the campaign machine (six physical cores,
twelve logical CPUs, GCC 12.2.0), the final proof replay took about 5.5 minutes
wall time.
Each shard traverses 6,001,931 canonical prefixes, evaluates its ordinal class
modulo 12, and emits output only on completion.  Peak state per process is
small and no generated proof log is needed.

A slower monolithic five-free-layer cross-check is

```sh
./quadratic_box_bound 30 5
```

It covers 192,656 prefixes and 3,082,496 orientation polynomials and returns
the valid but weaker bound 9,433,919.

## Trust boundary

All claimed arithmetic is exact.  C++ uses 128-bit integers and is restricted
to binary even lengths at most 30; the recurrence cardinalities and polynomial
coefficients are far below that range, while undefined-overflow sanitization
provides an execution check.  Python uses arbitrary-precision integers.

The source's upper-half theorem is a mathematical dependency.  Matching known
small cases is regression evidence, not the proof of the new bound.  The proof
rests on the documented finite reduction, termwise box inequality, complete
prefix/orientation coverage, exact implementation, and independent checker.
There is no solver, floating point, randomness, or external runtime data.

## Primary source

Lidija Stanovnik, Miha Moškon, and Miha Mraz, *In search of maximum
non-overlapping codes*, Designs, Codes and Cryptography 92 (2024), 1299--1326,
[doi:10.1007/s10623-023-01344-z](https://doi.org/10.1007/s10623-023-01344-z),
[arXiv:2307.12593v2](https://arxiv.org/abs/2307.12593).
