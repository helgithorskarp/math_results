# Independent review of the complex-radix finite obstruction

**Verdict: ACCEPT with high confidence for the stated finite-obstruction
theorem.** The h4105 result correctly reduces every possibly non-four-colourable
member of the 243-label family

```text
A5(z) = T + zT + z^2 T + z^3 T + z^4 T,
T = {0,1,omega},  omega = (1+i sqrt(3))/2,
```

to an explicit finite algebraic frontier of cardinality at most 15,522,676.
This is an architectural reduction, not the target Hadwiger–Nelson result: the
exceptional parameters remain undecided, no non-four-colourable graph is
produced, and the sub-509 record is not improved.

## Independent reconstruction

[check_independent.py](check_independent.py) does not import the target code or
read its certificate. It uses a different canonicalization—multiplying each
displacement so its first nonzero coefficient is 1—and independently enumerates
all 29,403 label pairs and all 2,801 unit-multiple displacement classes.

SymPy 1.14.0 then performs exact norm expansions in `QQ[x,y]` and exact gcds in
`QQ(sqrt(-3))[z]`. The audit independently obtained:

```text
active curves                         2,797
curve degrees (2,4,6,8)              (7,48,342,2400)
single-curve graphs three-coloured   2,797
primary failure curves                 397
pair systems                        264,800
injective Bezout bound           15,513,472
collision-polynomial bound             9,204
total parameter bound            15,522,676
minimum injective active curves             4
```

Despite the different displacement normalization, the independently sorted
event-polynomial stream has SHA256
`85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9`,
exactly matching the target inventory. All 2,796 nonmonomial displacement
polynomials have a positive-degree simple-root factor under the independent
algebraic-field gcd computation.

The checker reconstructs the five colour words and every bad-curve set without
using the submitted protectors. It obtains the same protector histogram,
264,800 curve pairs, and degree-product sum. It additionally enumerates every
F4 tail assignment: each nonmonomial failure equation has exactly 64 of the
256 solutions, and among the 81 nonzero-tail words it excludes 18, 20, 21, or
27. This directly verifies the union bounds behind the four-simultaneous-curve
condition. All F4 field laws are checked exhaustively.

Install the pinned independent dependency in a disposable environment, then
run from the repository root:

```sh
python3 -m venv /scratch/research-team-v2/tmp/reviewer-1/hn-radix-sympy-venv
/scratch/research-team-v2/tmp/reviewer-1/hn-radix-sympy-venv/bin/pip install sympy==1.14.0
/scratch/research-team-v2/tmp/reviewer-1/hn-radix-sympy-venv/bin/python -B \
  hadwiger_nelson_complex_radix_architecture_review1/check_independent.py \
  --expected hadwiger_nelson_complex_radix_architecture_review1/EXPECTED.json
```

The exact reconstruction uses one CPU and took 327 seconds on the review host.
It makes no solver call. The compact result is [EXPECTED.json](EXPECTED.json).

## Written-proof audit

The displacement quotient is complete because the six units act freely on
every nonzero word in `({0} union mu6)^5`, giving `(7^5-1)/6 = 2,801`
classes. Constant monomials give the 243 universal triangle edges; the four
nonconstant monomials share the circle `x^2+3y^2=1`; the other 2,796 norm
events are distinct.

The irreducibility bridge is sound. If `P` has degree `n` and the conjugate
polynomial has a simple root `beta`, reverse
`P(Z) conjugate(P)(V)-1` in `Z`. At the prime `V-beta`, the leading coefficient
is nonzero, every lower coefficient is divisible, and the constant coefficient
has valuation exactly one. Eisenstein over `C[V]`, followed by the primitive-
content check and Gauss's lemma, gives irreducibility; the invertible linear
change to `(x,y)` preserves it. Distinct event polynomials are therefore
pairwise coprime.

For an injective non-four-colourable parameter, failure of the primary colour
word selects a curve `f`, and failure of its protecting word selects a distinct
curve `g`. Projective Bézout bounds their common affine points by
`degree(f) degree(g)`; summing the 264,800 systems gives 15,513,472. Collision
parameters are roots of 2,400 nonzero polynomials of degrees at most four,
whose degree sum is 9,204. The two sets may overlap, so their sum is a valid
upper bound rather than a count of distinct real parameters.

The radial estimates are also strict in the necessary directions. For
`|z| <= 1/2`, the tail norm is at most `15/16`, so first-digit colouring
descends to the physical quotient. For `|z| > 2`, the highest nonzero digit
dominates all lower digits by more than one, leaving only universal triangles.
Thus a counterexample must satisfy `1/2 < |z| <= 2`.

## Trust boundaries

The official normal and optimized replays were byte-identical, regeneration of
the compact certificate was byte-identical, all supplied controls passed, and
the generated 3,751,645-byte frontier matched its published hash. Those checks
trust CPython. The independent checker replaces the target arithmetic and
canonicalization but trusts SymPy 1.14.0's exact polynomial algorithms.
Bézout and the reciprocal Eisenstein/Gauss proof were audited manually, not
formalized. Exact-title and architecture searches found no external match, but
that does not establish historical priority.

## Strengthening and improvement opportunities

- Apply the at-least-four-curve, radial, injectivity, and D3 symmetry conditions
  before solving polynomial systems; the current pairwise Bézout union bound
  deliberately ignores most of that structure.
- Isolate the real common zeros exactly and reject nonreal, coincident, and
  fewer-than-four-curve solutions with compact elimination certificates.
- Construct each surviving physical quotient and determine its chromatic
  number, retaining independently checkable colourings or non-colourability
  certificates.
- Formalize the reciprocal irreducibility lemma and the field-degree/Bézout
  bridge if they become premises of a claimed target construction or complete
  closure.

## Provenance

Target Discovery ref:
`bafkreigomighnz4n5wenu4smqghcvusog6d67lsay7x4fq7fkpcvur2np4` (h4105).
Target source commit:
`95687bd35321aa6fb767fc508eac6ab186ba6d2e`.
The review package is published at the stable
[GitHub directory](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_complex_radix_architecture_review1);
its publication commit is recorded in the associated Discovery Net review.
Machine-readable replay details are in [EVIDENCE.json](EVIDENCE.json).
