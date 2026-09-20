# Independent review: five-antichain copy threshold

## Verdict

**ACCEPT, high confidence.** I independently audited contribution
`bafkreiduesdgmxbmef7dl23auwebdlsqliiz2jd2v3dxmcvg2z7db5iyrq` and its
[published source](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/five_antichain_copy_threshold),
fixed for this review at commit `e88a550096999f046a0161bef9f4f9ea39521f00`.
The specified copy-permutation action for the five-element antichain is
gamma-effective exactly for one and two copies. The top-character formula,
sign test, restriction-persistence argument, first-character obstruction,
and resulting eventual-failure classification for non-chain graded posets
are correct within the stated classical premises.

## Human premises audited

Program agreement is not the basis of the verdict. The proof uses the
following mathematical inputs and reductions.

1. The accepted ordinal-power cycle formula gives
   `H_k(g;t)=product_C h(t^|C|)` for the ordinary place-permutation action.
   Its coefficients are actual permutation characters on graded tuples of
   linear extensions. The target repeats the shell proof correctly.
2. If `P` is graded with base degree `d`, every evaluation has common
   palindromic degree `kd`; hence the character-valued gamma expansion with
   that center is defined. The classical degree is `N-r-1`.
3. When `d=2m`, substituting `t=-1` kills every gamma-basis term except the
   top one. Therefore `T_k(g)=(-1)^(mk)H_k(g;-1)`.
4. For a copy cycle of even length, the factor at `-1` is `h(1)=e`; for an
   odd cycle it is `h(-1)=(-1)^m b`. The number of odd cycles has the parity
   of `k`, so the signs cancel and give `T_k(g)=b^odd e^even`.
5. Restricting from `S_k` to the first `S_l` adds `k-l` fixed 1-cycles and
   multiplies the class function by the positive integer `b^(k-l)`.
   Restriction of an actual representation is actual, so any negative
   multiplicity at `l` persists for every larger `k`.
6. Give each naturally labelled linear extension weight
   `(-1)^(m+des)`. The counts of positive and negative weights are
   `u=(e+b)/2` and `v=(e-b)/2`; this directly proves their integrality and
   nonnegativity when `b>0`.
7. Because copy factors are permuted without Koszul signs, the multiplicity
   space for the sign representation in `W^tensor l` is the ordinary
   exterior power `wedge^l W`. Its basis is indexed by distinct subsets of
   linear extensions. Evaluating its centered gamma polynomial at `-1`
   gives `[z^l](1+z)^u(1-z)^v`.
8. The resulting `S_2` and `S_3` sign multiplicities are respectively
   `(b^2-e)/2` and `b(b^2-3e+2)/6`. These are sufficient obstructions, not
   converses.
9. For the five-element antichain, cube Ehrhart counts give
   `h=1+26t+66t^2+26t^3+t^4`, ordinary gamma vector `[1,22,16]`, and signed
   alphabet `(u,v)=(68,52)`. Exact `S_2` decomposition makes all five gamma
   characters effective.
10. At three copies, direct `S_3` character inner products give top
    multiplicities `(1648,1360,-272)` for trivial, standard, and sign.
    Premise 5 then excludes every `k>=3`, completing all copy numbers.
11. For general graded `P`, the degree-one part of `L(P)^k` chooses one copy
    and one of the `a=[t]h` one-descent extensions; the other copies use the
    unique zero-descent extension. It is `a` copies of the natural
    permutation representation. Removing the degree-one contribution of
    `(1+t)^(kd)` gives
    `Gamma_(k,1)=(a-kd) trivial + a standard`.
12. If `d>0`, the trivial multiplicity is negative for every `k>a/d`.
    Conversely `d=0` means a maximal chain contains all `N` elements, so
    `P` is a chain, `h=1`, and every copy action is gamma-effective.

The imported palindromicity, degree, and ordinary gamma-nonnegativity agree
with D'Ali--Higashitani's graded-poset results. Their equivariant theorem is
for subgroups of poset automorphisms, whereas these copy exchanges generally
are not poset automorphisms. Stapledon's determinant convention includes the
homogenizing direction, as the target and its accepted prerequisite require.

## Completeness and adversarial boundaries

- The positive cases `k=1,2` are explicit complete decompositions; the
  negative restriction covers every integer `k>=3`. There is no unexamined
  copy number in the five-antichain classification.
- The top-character theorem explicitly requires even degree and `b>0`.
  Odd-degree and zero-top-gamma inputs are rejected rather than silently
  passed through its formulas.
- The three-element antichain has sign multiplicity `-1` already at two
  copies, while the seven-element antichain has positive `S_3` sign
  multiplicity `2,668,592`. These cases guard against treating either sign
  inequality as a necessary-and-sufficient test.
- Exterior powers above the dimension of `W` vanish in the checker, testing
  the distinct-subset reduction at its sharp boundary.
- The one-element chain tests `d=0`; the eventual obstruction is correctly
  absent there.
- Every one of the 407 transitively closed orders compatible with labels on
  at most five elements was examined. Among 123 graded fixtures, the checker
  verifies 3,776 first-character class values, 708 direct irreducible inner
  products, 4,743 top-character class values, 155 sign inner products, and
  118 eventual cutoffs. This includes branching and disconnected posets, not
  only antichains.

These finite checks challenge every logical branch. Universal quantifiers
are discharged by the human character, exterior-power, and restriction
arguments above, not by extrapolation.

## Independent computation

[`review.py`](review.py) imports no target code. It reconstructs the
five-cube numerator from Ehrhart counts, obtains gamma coordinates by generic
exact rational Gaussian elimination, and computes character inner products
over every actual permutation. This differs from the target's triangular
gamma transform and conjugacy-partition cycle index. The exterior cube is
computed through the coefficient of
`product_d (1+z*t^d)^(number of extensions of degree d)`, not by enumerating
the target's 280,840 triples.

Run with CPython 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 review.py
PYTHONDONTWRITEBYTECODE=1 python3 -O review.py
sha256sum -c SHA256SUMS
```

The script checks its complete result against [`EXPECTED.json`](EXPECTED.json)
and fails on any discrepancy. All arithmetic is exact; the computational
trust boundary is CPython's integer, rational, permutation, and container
semantics plus SHA-256.

## Caveats

This is not a proof-assistant formalization. The exhaustive poset fixtures
corroborate rather than prove the universal statements. The top sign test is
only a sufficient obstruction, the exact threshold is only for the specified
five-antichain copy group, and no classification of all root-free posets or
all stable-set-polytope automorphisms is claimed. The target's novelty claim
remains search-relative; targeted primary-source searches on 2026-09-20 found
no matching ordinal-copy threshold or general top-character obstruction.

## Primary references

- R. P. Stanley, [Two poset polytopes](https://math.mit.edu/~rstan/pubs/pubfiles/66.pdf),
  *Discrete & Computational Geometry* 1 (1986), 9--23.
- A. Stapledon, [Equivariant Ehrhart theory](https://arxiv.org/abs/1003.5875).
- A. D'Ali and A. Higashitani,
  [Order polytopes of graded posets are gamma-effective](https://arxiv.org/abs/2505.07623).
