# Independent review of the order-10 multiplier obstruction at 541

This directory audits the exact lemma in the sibling
[`schur6_cyclic541_multiplier_obstruction`](../schur6_cyclic541_multiplier_obstruction)
directory. The target says that an order-10 multiplicative-subgroup-invariant
sum-free subset of `F_541\{0}` has at most 80 residues; all 378 maximum sets
form seven scalar-multiplication classes. It follows that six individually
H-invariant colour classes cannot partition the 540 nonzero residues.

## Verdict and scope

**Accepted with high confidence as a finite, restricted classification.**
For a strictly reflection-symmetric classical six-colouring of `[1,540]`,
the colour-preserving multiplier group consequently has order 2 or 4.
Reflection makes each integer-sum-free colour class modularly sum-free:
a wrapping equality `x+y=z+541` reflects to
`(541-x)+(541-y)=541-z`. The group contains `-1`. If its order is divisible
by 3, its sixth roots include the monochromatic modular triple
`1+129=130`; if divisible by 5, it contains the excluded order-10 subgroup.
The remaining even divisors of `540=4*27*5` are 2 and 4.

This does **not** rule out an unrestricted colouring of `[1,537]`, an
arbitrary colouring of `[1,540]`, order-4 colour-preserving symmetry, or a
multiplier action that permutes colour labels. It gives no new bound for
classical `S(6)`.

## Independent exhaustive audit

`audit.py` imports none of the author's checkers. It constructs the 54
order-10 cosets directly, generates forbidden coset supports from every
nonzero modular equation `x+y=z` with `x<=y`, and recursively visits every
increasing independent coset-index list containing coset 0 up to size 9.
At each extension, it tests every forbidden support containing the new index.
The recursion uses **no size pruning** and visits 13,931 nodes. It finds
56 normalized independent eight-coset sets and no nine-coset set. Scaling
normalizes every nonempty H-invariant set to one containing coset 0; hence
no larger set exists.

The audit separately checks each 80-residue union by literal modular
addition, enumerates all scalar images, obtains 378 different maximum sets
in seven orbits of size 54, and compares their seven canonical
representatives to the published compact fixture. It also checks primality
of 541, the exact subgroup elements, the sixth-root triple, and the
order-4 subgroup generator. The author's `verify.py` agrees in normal and
optimized Python runs and includes a separate residue-sumset enumeration
and seven exhaustive small-instance controls.

## Reproduce

CPython 3.11 or later, standard library only. From this directory:

```sh
python3 -B audit.py
python3 -B -O audit.py
```

Both commands print:

```text
PASS independent_cyclic541 edges=0,216,4392 normalized=56 maximum_cosets=8 all_maximum_sets=378 scaling_types=7 nodes=13931
```

From the sibling source directory, `python3 -B verify.py` and
`python3 -B -O verify.py` reproduce `expected.json`. The author's full
normalized catalog SHA-256 is
`50c65ca00d9e47fe891c97c430453e9078696661d38ab905c8bed817f5eba6c6`.
Our audit uses explicit exception checks, so the optimized run still checks
all assertions of the mathematical result.

The [Fredricksen--Sweet paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
introduced the 536-colouring and scalar equivalence of symmetric partitions.
The [July 2026 shifted S-templates preprint](https://arxiv.org/abs/2607.15034)
still uses `S(6)>=536`. Targeted searches found no prior publication of
this exact modulus-541 order-10 classification; this is search-relative
evidence for potential novelty, not a historical priority claim.

## Strengthening and improvement opportunities

1. The remaining order-4 colour-preserving subgroup has 135 cosets. An exact
   classification or a checkable partition-exclusion certificate could close
   the strictly symmetric, label-preserving multiplier route at `[1,540]`.
2. Colour-label-permuting multiplier actions require a separate orbit model
   for both residues and the palette. The present per-colour size bound
   cannot be applied to such actions without that bridge.
3. Reaching unrestricted `S(6)` requires a verified 537-colouring or a
   global exclusion of all 537-colourings. The reflection and multiplier
   hypotheses here supply no reduction to those unrestricted cases.

## Trust boundary

The result depends on the displayed coset reduction, exhaustive finite
searches, and exact Python arithmetic. The independent audit shares the
mathematical normalization at coset 0 but uses a different recursion without
the author's candidate filtering. No SAT solver, floating point, external
dataset, or omitted large certificate is needed. The theorem is not
formalized in a proof assistant.
