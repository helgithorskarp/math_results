# Even-length middle-quadratic compression for `SQN`

This directory proves and checks a global reduction for the exact integer
formulation of maximum non-overlapping codes introduced by Stanovnik, Moškon,
and Mraz.

For every even length `n=2m`, fix all feasible `SQN` data below level `m` and
fix the pure upper-layer orientations guaranteed for an optimum by the source
paper.  If `t=x_m` and `y_m=s_m-t`, then the final code size is exactly

```
Q(t) = -t^2 + B*t + C.
```

It follows that the source algorithm's loop over all `s_m+1` middle splits can
be replaced, on **every** lower prefix, by at most two integer vertex
candidates.  See [proof.md](proof.md) for the complete argument and precise
scope.

This does not determine `S(2,30)`.  It is a complete branch-independent
reduction of the retained exact problem.  On the full binary length-24 tree it
reduces 321,286,030 middle-loop leaves to 6,706,281 vertex candidates, a factor
of about 47.91, while recovering the published optimum 147,312.
An additional complete length-26 run reduces 30,699,841,782 leaves to
321,286,030 vertex candidates, a factor of about 95.55, and recovers the
published optimum 547,337 in 893.775 seconds on one campaign core.

## Files

- `proof.md`: theorem, proof, source dependency, and scope.
- `middle_quadratic.cpp`: optimized exact binary enumerator for even lengths
  through 30.  It propagates affine coefficients symbolically and checks that
  each upper layer is affine and the objective has leading coefficient `-1`.
- `verify.py`: independent Python arbitrary-precision checker.  It enumerates
  every middle value on every binary lower prefix through length 20, verifies
  all second differences, and separately checks deterministic C++ summaries
  and displayed `SQN` witnesses through length 24.

## Reproduction

Required tools are Python 3.11 or later and a C++20 compiler.  No third-party
packages are used.

```sh
make check
make sanitize
```

`make check` performs the independent exhaustive Python calculation and then
checks the optimized enumerator through length 24.  On the reference machine
it takes roughly 45 seconds.  The final JSON object begins with

```json
{
  "status": "PASS"
}
```

and its length-24 C++ record is

```json
{
  "n": 24,
  "best": 147312,
  "prefixes": 6001931,
  "original_middle_leaves": 321286030,
  "vertex_candidates": 6706281
}
```

`make sanitize` compiles with GCC AddressSanitizer and UndefinedBehaviorSanitizer
and checks the complete length-20 tree.

For an individual production run:

```sh
./middle_quadratic 24
```

The enumeration is deterministic and single-threaded.  On GCC 12.2.0 with
`-O3`, the complete length-24 run took about 14 seconds on one campaign core.
The optional length-26 run takes about 15 minutes on the same machine and is
not part of `make check`.

## Trust boundary

All arithmetic is integral.  Python uses arbitrary-precision integers.  The
optimized C++ program uses signed and unsigned 128-bit integers and is limited
to binary `n<=30`; layer cardinalities are at most `2^i`, and the indexed
recurrences keep the checked intermediates far below the 128-bit boundary at
this scope.  The program fails visibly if its symbolic degree assertions or
certificate instantiation fail.

The mathematical proof does not rely on matching timings or aggregate counts.
The C++ enumeration depends on the published backwards orientation condition;
the Python implementation rederives it independently but shares the source
paper as a mathematical dependency.  Both implementations validate against
the published exact binary values.  No solver, floating point, randomness, or
external data is used.

## Primary source

Lidija Stanovnik, Miha Moškon, and Miha Mraz, *In search of maximum
non-overlapping codes*, Designs, Codes and Cryptography 92 (2024), 1299--1326,
[doi:10.1007/s10623-023-01344-z](https://doi.org/10.1007/s10623-023-01344-z),
[arXiv:2307.12593v2](https://arxiv.org/abs/2307.12593).
