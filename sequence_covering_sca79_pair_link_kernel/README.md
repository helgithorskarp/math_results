# Ordered-pair link kernel for `SCA(5040;7,9)`

## Result and scope

This directory determines the complete linear kernel of an ordered-pair link
in a hypothetical `PSCA(9,7,1)`, equivalently an `SCA(5040;7,9)`.  It then
constructs and uniquely classifies the maximally symmetric integral pair-link
relaxation with the boundary projections inherited from the uniform point
link.

The main conclusions are:

1. an ordered-pair link has 2,187 cells and 5,103 exact five-coordinate
   marginal equations of rank 1,611;
2. the homogeneous kernel has dimension 576;
3. the two point-link boundary projections expose 16 of those dimensions, so
   fixing both projections leaves an affine space of dimension 560;
4. under full `S_7` symmetry of the remaining symbols and `S_3` symmetry of
   the three regions, there is a unique nonnegative integral solution with
   uniform boundary projections; and
5. that local solution cannot be assigned to every ordered symbol pair in a
   global array; but
6. an explicit asymmetric profile and its six region relabellings form a
   72-profile bundle meeting every global composition total exactly.  Thus
   any further obstruction must retain coordinate labels or higher-order
   coupling, not only position compositions.

This is a structural pair-link milestone, not a construction or nonexistence
proof for the original open problem.  It builds on the complete point-link
flow relaxation in
[`sequence_covering_sca79_point_link_flow`](../sequence_covering_sca79_point_link_flow/).
The open status and exact frontier are documented by Gentle, Horsley and
Wanless, [*Excess Coverage Arrays and Levenshtein's
Conjecture*](https://arxiv.org/abs/2411.17145), Designs, Codes and Cryptography
(2025), [DOI 10.1007/s10623-025-01722-9](https://doi.org/10.1007/s10623-025-01722-9).

## Ordered-pair links

Fix distinct symbols `w,x` and retain the 2,520 permutations in which `w`
precedes `x`.  Each of the other seven symbols lies in one of three regions:

```text
0: before w,
1: between w and x,
2: after x.
```

For a word `z in {0,1,2}^7`, let `P_wx(z)` be the number of retained
permutations with exactly that region assignment.

Fix five coordinates of `z`, with `r_i` assigned to region `i`, and sum over
the two omitted coordinates.  There are exactly

```text
r_0! r_1! r_2!
```

orders of the seven chosen symbols consistent with the prescribed regions
around `w,x`.  Perfect sequence coverage therefore gives all

```text
binom(7,2) * 3^5 = 5103                                      (1)
```

exact marginal equations.

## The 576-dimensional kernel

On one ternary coordinate, split the three-dimensional function space into a
constant direction and two zero-sum contrasts.  Tensor products are indexed
by their **support**, the coordinates carrying a contrast.  Marginalising an
omitted coordinate kills a tensor precisely when that coordinate is in its
support.

A homogeneous table lies in the kernel of every two-coordinate marginal if
and only if its support meets every two-subset of the seven coordinates.  Its
support therefore has size six or seven.  The kernel dimension is

```text
binom(7,6) * 2^6 + binom(7,7) * 2^7 = 448 + 128 = 576.        (2)
```

Hence the marginal rank is

```text
3^7 - 576 = 1611.                                            (3)
```

The verifier independently obtains rank 1,611 over `F_2`.  This is a lower
bound on the rational rank, while (2) supplies the matching upper bound.

## Projection to the point links

The first binary projection groups the ternary levels as

```text
0 | {1,2};
```

it records the exact predecessor set of `w` in the half where `x` follows
`w`.  The second groups them as

```text
{0,1} | 2;
```

and records the predecessor set of `x`, apart from the already included
symbol `w`.

Choose one-coordinate basis vectors

```text
c=(1,1,1),  p=(1,-1,0),  q=(0,1,-1).
```

Under the first projection their images are `(1,2)`, `(1,-1)`, and `(0,0)`;
under the second they are `(2,1)`, `(0,0)`, and `(1,-1)`.  Thus the first
projection sees exactly the eight support-six-or-seven tensors made solely
from `p`, and the second sees the analogous eight tensors made solely from
`q`.  These sets are disjoint and independent.  The combined projection has
rank 16 on the 576-dimensional kernel, leaving

```text
576 - 16 = 560                                                (4)
```

free dimensions after both boundary projections are fixed.

This calculation explains exactly what the point-link theorem cannot see:
560 pair-correlation directions survive even after both boundary halves are
specified.

## Unique maximally symmetric integral fixture

Impose invariance under permuting the seven coordinates and under permuting
the three regions.  A cell value then depends only on the unordered
composition of seven into three parts.  There are eight orbit variables.  In
the following table, `abc` denotes the sorted composition `(a,b,c)`.

| composition | cell multiplicity |
| --- | ---: |
| `700` | 70 |
| `610` | 10 |
| `520` | 5 |
| `511` | 0 |
| `430` | 1 |
| `421` | 1 |
| `331` | 1 |
| `322` | 0 |

Assigning these values to all `3^7` words gives total multiplicity 2,520,
satisfies every equation in (1), and has both boundary projections equal to
the corresponding halves of the uniform point-link vector

```text
(560,70,20,10,8,10,20,70,560).
```

The symmetric linear system has rank seven.  With
`t = x_322`, its complete rational solution is

```text
x_700 = 70,
x_610 = 10,
x_520 = 5 - 5t,
x_511 = 5t,
x_430 = 1 + 3t,
x_421 = 1 - t,
x_331 = 1 - 3t/2,
x_322 = t.                                                     (5)
```

For an integral nonnegative table, `t` is a nonnegative integer, while
`x_331 >= 0` gives `t <= 2/3`.  Hence `t=0`, proving uniqueness of the table
above without a solver.

## Forced global symmetry breaking

For an ordered composition `(a,b,c)` with sum seven, every permutation has
exactly one ordered symbol pair occupying the positions with `a` symbols
before the first, `b` between, and `c` after the second.  Consequently every
hypothetical global array obeys

```text
sum over all ordered pairs and all labelled (a,b,c)-partitions P_wx = 5040.
                                                                    (6)
```

If the symmetric fixture were assigned to all 72 ordered symbol pairs, the
left side of (6) for composition `(5,1,1)` would be zero, because its cell
multiplicity is zero.  The right side is 5,040.  Therefore the unique local
symmetric fixture cannot repeat globally: even at the uniform point-link
profile, any candidate `PSCA(9,7,1)` must use genuinely asymmetric ordered-pair
links.

More generally, dividing (6) by the number of cells shows that the global
average cell value at composition `(a,b,c)` is

```text
a! b! c! / 72.
```

These averages are often nonintegral, another direct expression of the
required heterogeneity.

## The composition-level relaxation remains feasible

The symmetry breaking above is unavoidable, but it is sufficient at the
composition level.  The compact certificate
[`ASYMMETRIC_PROFILE.tsv`](ASYMMETRIC_PROFILE.tsv) gives a second link whose
cell value depends on the **ordered** composition
`(before,between,after)`.  It is invariant under `S_7` on coordinates but not
under `S_3` on regions.  Direct checking shows that it satisfies all 5,103
marginal equations, has total multiplicity 2,520, and has the same two uniform
boundary projections as the symmetric fixture.

Let `R` denote this asymmetric profile and let `sigma R` run through its six
region relabellings.  For every ordered composition `(a,b,c)`, the following
exact identity holds:

```text
36 Q_(a,b,c) + 6 * sum_{sigma in S_3} (sigma R)_(a,b,c)
    = a! b! c!.                                                  (7)
```

Thus the multiset

```text
36 copies of Q, plus six copies of each of the six sigma R
```

contains exactly 72 ordered-pair profiles and satisfies (6) for every one of
the 36 ordered compositions.  Every member separately satisfies the full
local pair-link equations and the uniform point boundaries.

Equation (7) is a constructive feasibility certificate for the global
composition relaxation.  It does not assign the profiles to common
permutations or enforce labelled region partitions.  Its mathematical value
is to locate the next missing information precisely: a successful obstruction
must distinguish which named symbols occupy the three regions, or couple
three or more marked symbols.

## Reproduction and trust boundary

The artifact uses only Python 3.11 standard-library exact integers and
`Fraction` arithmetic.

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

[`verify.py`](verify.py) checks all 5,103 defining marginals and all 256
boundary cells directly for both `Q` and `R`, computes the full marginal rank
over `F_2`, checks the 16-dimensional projection image, reconstructs (5) by
exact row reduction, verifies the global `(5,1,1)` mismatch, and checks all 36
instances of (7).  No floating point, random choice, third-party package, or
solver verdict enters the result.

The universal dimension statements use the tensor-support argument above;
the executable supplies exact finite checks of the ranks and the explicit
fixture.  The remaining target requires coupling asymmetric pair links and
then enforcing the internal orders that the ternary regions forget.

## Next milestone

Lift (7) from ordered compositions to named region partitions.  The immediate
objective is to decide whether its 72 local profiles admit labelled refinements
whose projections agree on every named point-link cell.  Failure would provide
a finite global obstruction; success would give a concrete pair-link bundle
for a subsequent three-symbol or internal-order search.
