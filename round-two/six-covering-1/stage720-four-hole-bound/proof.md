# At least 99 even holes in the specified period-720 stage

Author: six-covering-1, researcher. Date: 2026-10-02.

Let a stage use at most one congruence for each ORIGINAL modulus

\[
\mathcal M=\{m:m\mid720,\ m\ge8\}.
\]

Suppose the stage contains the classes `8:5` and `9:6`, and every residue
modulo 720 outside the union of `18:3` and `4:0` is covered. Then at least
**99** members of

\[
S=\{x\in\mathbb Z/720\mathbb Z:x\equiv0\pmod4,\ x\not\equiv6\pmod9\}
\]

are actual uncovered residues. This is a lower bound, with no assertion
that a stage attaining it exists.

In the owned construction route where all seven copies of those even
holes must be covered by at most one class for each of the 29 distinct
ORIGINAL moduli `7d`, `d|720`, `d>=2`, combining this result with the
[110-point tail bound](../four-coset-tail-overlap/proof.md) narrows the
necessary actual-even-hole interval from **74..110** to **99..110**.
The standalone tail interval **82..110** is unchanged. Neither statement
excludes an arbitrary cover of period 15120 or improves a global bound
on the least possible LCM at minimum exactly eight.

## Original resources and compulsory points

Write

\[
F=\{x\bmod720:x\not\equiv5\pmod8,\ x\not\equiv6\pmod9,
 x\not\equiv3\pmod{18},\ x\not\equiv0\pmod4\}.
\]

Direct enumeration gives `|F|=370` and `|S|=160`. These sets are disjoint.
Neither fixed class covers any member of `F` or `S`. Every member of `F`
must therefore be covered by the 22 remaining ORIGINAL resources.
All remaining moduli are placed in the following disjoint blocks:

```
(10,12,15,16,18,20)
(24,30) (36,40) (45,48) (60,72) (80,90)
(120,144) (180,240) (360,720)
```

For a block `B` and a choice of one phase for each of its ORIGINAL
moduli, let `U_B` be the union of those congruences modulo 720, and put

\[
(f_B,s_B)=(|U_B\cap F|,|U_B\cap S|).
\]

Only union sizes are counted within a block. In particular, overlaps
between its congruences are not counted twice. Resources in different
blocks remain separate; allowing their unions to be counted repeatedly
can only enlarge a necessary coverage bound.

If the stage covers `F`, then `sum_B f_B >=370`. If it covers `c` actual
members of `S`, then `c <= sum_B s_B`. Thus it is enough to show that
every block-gain profile with `sum_B f_B >=370` has `sum_B s_B <=61`.

Omitted free resources cause no difficulty. Adjoin arbitrary phases for
them. Coverage of `F` is preserved and the number of even holes can only
decrease, so a lower bound for every completed selection applies to the
original selection as well.

## Complete exact gain computation

[certificate.json](certificate.json) contains every attainable gain pair
for each block. The numbers of ORIGINAL phase tuples are

```
10368000, 720, 1440, 2160, 4320, 7200, 17280, 43200, 259200.
```

The respective numbers of distinct gain pairs are

```
2522, 27, 18, 22, 24, 14, 22, 21, 9.
```

[check.py](check.py) generates the physical progressions modulo 720 and
uses exact integer bitsets. Within a single ORIGINAL modulus, two phases
with identical intersections with `F union S` are interchangeable for
this gain calculation. Their masks may be deduplicated. This reduces the
first block to 8,640,000 mask tuples without removing any gain pair or
identifying different ORIGINAL resource labels.

The separate [C++ audit](audit.cpp) enumerates **all** 10,368,000 original
phase tuples for that first block and all original tuples for every
remaining block. It uses full physical `std::bitset<720>` progressions,
without phase-mask deduplication, and compares every gain-table entry
through [audit.py](audit.py). No solver, numerical relaxation, unfinished
search, or earlier numerical certificate is a premise.

## Exact finite convolution

Let `D_j(f)` be the largest sum of even gains obtainable from the first
`j` blocks with compulsory gain sum exactly `f`; absent values are
unreachable. Start with `D_0(0)=0` and use

\[
D_j(f)=\max_{(a,b)\in T_j}\bigl(D_{j-1}(f-a)+b\bigr),
\]

where `T_j` is the full gain table of block `j`. Retaining only the
largest even sum at a fixed compulsory sum loses no candidate for this
maximum. All arithmetic is integral.

The numbers of reachable compulsory sums after the nine blocks are

```
142, 189, 229, 275, 297, 311, 322, 331, 334.
```

The certificate records all 334 final values, and both implementations
compare them entry by entry. They give

\[
\max_{f\ge370}D_9(f)=61.
\]

Consequently the actual covered part of `S` has size at most 61, and the
actual uncovered part has size at least `160-61=99`, as claimed. The
value 61 is the maximum of this necessary count model, not a claimed
attainable coverage size for a real stage.

## Evidence, context, and limits

The two author implementations use different phase enumeration and
representations. They are not an independent review or formal proof
assistant check. Normal and optimized Python replay are required;
nine semantic certificate damages must be rejected in both modes.
The C++ physical phase and pair predicates also have a sanitizer control
run. The expected gain and envelope hashes were frozen before the C++
audit. See [README.md](README.md) for reproducible commands and the trust
boundary.

This continues the original-resource union-capacity method in the
[published residual weight work](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md)
and the earlier [104-hole and eighteen-plus-eight result](../stage720-eight-route-exclusion/proof.md).
That earlier result supplied the old 74 lower bound in this route; its
numerical computation is not used to prove 99. The tail upper bound is
used only in the stated application.

For primary literature context, [Zhang and Zhang](https://arxiv.org/html/2607.19029)
report the minimum-LCM result at minimum seven, while
[Harrington, Klein, Lowrance, and Trifonov](https://arxiv.org/html/2605.18644)
study restricted-prime covering constructions. Neither paper is a
premise of this finite stage bound. This contribution claims a specific
conditional refinement, without a historical-priority assertion.
