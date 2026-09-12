# Last-two-layer critical-set theorem for `SQN`

This directory proves and checks a constant-size exact reduction for the last
two free layers in the Stanovnik--Moškon--Mraz integer recurrence for maximum
non-overlapping codes.

For every even `n=2m>=8`, fix any feasible recurrence prefix through level
`m-2`.  Put `u=x_{m-1}` and `t=x_m`.  The upper orientation at level `m+1`
changes at most once as `u` varies, and on either orientation interval the
completed objective is

```
Q(u,t) = -t^2 + (a*u+b)*t + c*u^2 + e*u + f.
```

Exact clipping, parity subdivision, and one-dimensional quadratic
optimization leave at most eight pairs per orientation interval, hence at
most **sixteen `(u,t)` pairs per prefix**.  At least one unrestricted optimum
is retained.  See [proof.md](proof.md) for the theorem and proof.

This strengthens the earlier one-layer middle-quadratic reduction.  On the
complete binary length-26 tree it reduces 30,699,841,782 raw last-two-layer
leaves to 13,317,209 critical pairs, a factor of 2,305.276, and recovers the
published exact optimum 547,337.  It does not determine `S(2,30)`.

## Files

- `proof.md`: theorem, exact critical-set construction, proof, scope, and
  source dependency.
- `two_layer_critical.cpp`: optimized exact binary enumerator through length
  30.  It propagates bivariate coefficients, asserts the degree and `t^2`
  identities, checks the affine orientation condition, and evaluates only the
  proved critical set.
- `verify.py`: independent arbitrary-precision Python checker.  It tests the
  generic lattice optimizer on 309,729 small quadratics, interpolates rather
  than symbolically propagates recurrence polynomials, and exhausts every
  `(u,t)` pair on every binary prefix through length 18.

## Reproduction

Required tools are Python 3.11 or later and a C++20 compiler.  There are no
third-party dependencies.

```sh
make check
make sanitize
```

`make check` runs the independent Python suite and checks deterministic C++
summaries and displayed recurrence witnesses through length 24.  Its final
JSON object begins with `"status": "PASS"`.  `make sanitize` builds with GCC
AddressSanitizer and UndefinedBehaviorSanitizer and checks the complete
length-18 tree.

The slower definition-level extension through length 20 is

```sh
python3 verify.py --reference-max 20
```

and was also completed for the published source.

For the larger complete census:

```sh
./two_layer_critical 26
```

On the campaign machine with GCC 12.2.0, the final length-26 run used one core
and approximately 250 seconds.  It is deterministic and emits output only
after completing the entire tree.

## Trust boundary

All arithmetic is integral.  Python uses arbitrary-precision integers.  The
C++ program uses signed and unsigned 128-bit integers, supports binary
`8<=n<=30`, and fails visibly on a degree, interval, recurrence, candidate, or
witness inconsistency.  Sanitizers cover a complete smaller tree.  No solver,
floating point, randomness, or external data is used.

The proof does not depend on aggregate timings or known answers.  Both
implementations depend mathematically on the source's complete upper-half
orientation theorem.  Their candidate generation differs: C++ propagates
symbolic polynomials, while Python obtains coefficients by six definition-level
evaluations and compares against full enumeration.

## Primary source

Lidija Stanovnik, Miha Moškon, and Miha Mraz, *In search of maximum
non-overlapping codes*, Designs, Codes and Cryptography 92 (2024), 1299--1326,
[doi:10.1007/s10623-023-01344-z](https://doi.org/10.1007/s10623-023-01344-z),
[arXiv:2307.12593v2](https://arxiv.org/abs/2307.12593).
