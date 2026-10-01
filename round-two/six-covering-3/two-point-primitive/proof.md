# Two-point charges on a primitive 2 × 3 × 5 block

Actual author: **six-covering-3**, role **researcher**, 2026-10-01.
Status: a proved structural lemma and an exact linear-time phase maximum,
with rational certificates and same-author exact checks. This does not
exclude either entire period 10080 or 15120 and does not improve the current
numerical bounds on `L_min(8)`. No independent review or formalization is
claimed.

## 1. The local lemma

Identify `Z/30` with `X = {0,1} × {0,1,2} × {0,1,2,3,4}` by CRT.
Let `V` be the real span of functions on `Z/30` having a proper-divisor
period. Equivalently, each spanning function is independent of at least
one coordinate. Constants belong to `V`.

For a set `H` of at most two points, define `kappa(H)` as follows:

| H | kappa(H) |
|---|---:|
| empty or singleton | 0 |
| two points differing only in the binary coordinate | 2 |
| two points differing only in the ternary coordinate | 1 |
| every other pair | 0 |

**Lemma.** If `f in V`, `f >= -1` on `H`, and `f >= 0` outside `H`, then

    sum_(x in X) f(x) >= -kappa(H).                       (1)

The constants are sharp for these hypotheses on the signed function `f`.
This sharpness does not assert that a distinct covering realizes them.

**Proof.** Let `omega >= 0` have sum 2, 3, and 5 on every axis-parallel
line of lengths 2, 3, and 5, respectively. For any function independent of
one coordinate, summing along that coordinate proves

    sum omega*f = sum f.

By linearity this holds for every `f in V`. Therefore

    sum f >= -sum_(x in H) omega(x).                     (2)

It remains to give such an array with mass `kappa(H)` on `H`.
Coordinate permutations take a pair to `(0,0,0)` and `(d2,d3,d5)`,
where each `di` is zero or one according as the two coordinates agree
or differ. For a singleton use all three `di=0`.

Use `omega(0,j,k)=1+h(j,k)` and `omega(1,j,k)=1-h(j,k)`.
It suffices that the 3-by-5 matrix `h` has zero row and column sums and
entries between -1 and 1. The following are explicit matrices. Each
semicolon separates rows; omitted entries are zero.

| `(d2,d3,d5)` | rows of h |
|---|---|
| `(1,0,0)` | zero matrix |
| `(0,1,0)` | `(-1/2,1/8,1/8,1/8,1/8); (-1/2,1/8,1/8,1/8,1/8); (1,-1/4,-1/4,-1/4,-1/4)` |
| `(0,0,1)` | `(-1,-1,2/3,2/3,2/3); (1/2,1/2,-1/3,-1/3,-1/3); (1/2,1/2,-1/3,-1/3,-1/3)` |
| `(1,1,0)` | `(-1,1/4,1/4,1/4,1/4); (1,-1/4,-1/4,-1/4,-1/4); zero` |
| `(1,0,1)` | `(-1,1,0,0,0); (1/2,-1/2,0,0,0); (1/2,-1/2,0,0,0)` |
| `(0,1,1)` | `(-1,1,0,0,0); (1,-1,0,0,0); zero` |
| `(1,1,1)` | `(-1,0,1,0,0); (0,1,-1,0,0); (1,-1,0,0,0)` |

For the singleton use `h(j,k)=-a_j*b_k`, with
`a=(1,-1/2,-1/2)` and `b=(1,-1/4,-1/4,-1/4,-1/4)`.
This gives zero mass at the singleton. The empty case uses `omega=1`.
The displayed row/column sums, ranges, and two-point masses establish
(1) by (2). They are the rational arrays in `primitive_weights.json`.

These arrays also minimize the permitted mass on `H`: a binary pair is
an entire length-two line, hence always has mass 2. For a ternary pair,
the third point has mass at most 2, because its binary line has mass 2;
the ternary line has mass 3, so the pair has mass at least 1. All other
cases have lower bound zero, attained above.

For sharpness of (1), take `f=0` in the zero-charge cases. For the binary
pair `(0,0,0),(1,0,0)`, take `f=-1_(j=0,k=0)`, independent of the binary
coordinate; its total is -2. For the ternary pair
`(0,0,0),(0,1,0)`, take

    f(a,j,k) = -1_(a=0,k=0) + 1_(j=2,k=0).

Both summands have proper period. Its only negative values are -1 at the
two marked points, and its total is -1. This completes the proof. QED.

## 2. Lift to actual congruences

Let `B=2^{a_2}*3^{a_3}*5^{a_5}` with all three exponents positive, let `p>5` be a
prime, put `N=Bp` and `T=B/30`, and take a positive integer `b0|T`.
Use CRT coordinates `(t mod B,z mod p)`.

Let `P` be prescribed congruences with distinct moduli dividing `N`.
Let `R` be permitted unplaced divisors of `N`, with no modulus already in
`P`. A completion may use any subset of `R`, once per modulus. Assume
the two top resources `S={B,N}` belong to `R`; thus neither is prescribed.
No irredundancy or exact ambient-LCM assumption is required.

Let `u>=0` on `Z/N` vanish on every prescribed class. Let `v>=0` be
`b0*p`-periodic; it may be positive on prescribed classes. Write

    D(w) = sum_(x mod N) w(x),
    Phi_(n,a)(w) = sum_(x=a mod n) w(x),
    C_n(w) = max_(a mod n) Phi_(n,a)(w).

Write `u_r(t)=u(t,r)` and `v_r(t)=v(t mod b0,r)`, and set
`A(t)=sum_(r mod p) u_r(t)`. Define a function on `Z/B` by

    chi(delta) = 2,  if delta=B/2;
                 1,  if delta=B/3 or 2B/3;
                 0,  otherwise.                         (3)

**Proposition.** Every covering completion satisfies

    D(u+v) - sum_((n,a) in P) Phi_(n,a)(v)
      <= sum_(n in R outside S) C_n(u+v) + K(u,v),        (4)

where

    K(u,v) = max_(alpha,beta mod B, r mod p)
        [A(alpha) + u_r(beta)
                   + chi(beta-alpha)*v_r(alpha)].        (5)

In particular, a strict reverse inequality in (4) excludes every completion
of that prefix with those permitted divisors. This is a necessary constraint,
not an equivalence or a sufficient condition for existence.

**Proof.** Adjoin omitted top classes at arbitrary phases; coverage and
distinctness persist. Their B-coordinate points are `alpha` for modulus B
and `beta` for modulus N, with the latter active only at some `z=r`.
Fix a cofactor coordinate `z` and a primitive block

    {q+T*j mod B : j mod 30},  q mod T.

The weight `v` is constant on this block. Every class outside `S` has a
proper B-part `m=gcd(B,n)<B`. Some prime `ell` in `{2,3,5}` satisfies
`m|B/ell`. On this block its indicator is invariant under
`j -> j+30/ell`, or is identically zero. Thus its local indicator has a
proper-divisor period and lies in `V`.

Let `f` be the sum of all used outside indicators minus 1. Because the
whole system covers, `f>=0` off the set `H` of distinct active top points,
and `f>=-1` on `H`. Apply (1) and multiply by the block's nonnegative
constant weight. Empty or singleton `H` has no top charge. A pair can
occur only at `z=r`, when the two top points are in the same block.
They differ only in the binary coordinate of that block exactly when
`beta-alpha=B/2`, and only in its ternary coordinate exactly when
`beta-alpha=B/3` or `2B/3`. These follow from CRT modulo 2,3,5 in `j`.
All other configurations have charge zero. The total top charge for `v`
is consequently precisely the expression in (3), times `v_r(alpha)`.

Summing blocks gives the v-demand bounded by all actual outside
v-footprints, including prescribed footprints, and that top charge.
Ordinary nonnegative counting for `u`, which vanishes on `P`, adds the
actual free outside u-footprints and the top footprints
`A(alpha)+u_r(beta)`. Combine u and v before maximizing each free outside
resource. Omitted outside resources have nonnegative capacities and may
be added to the bound. Move the known v-footprints to the left and maximize
over actual top phases. This proves (4). QED.

## 3. The exact top maximum takes linear time

Define

    K0 = max_t A(t) + max_(s,r) u_r(s),
    K2 = max_(t,r) [A(t)+u_r(t+B/2)+2*v_r(t)],
    K3 = max_(t,r,epsilon in {1,2})
                       [A(t)+u_r(t+epsilon*B/3)+v_r(t)].

Then

    K(u,v) = max(K0,K2,K3).                              (6)

All B-coordinates are reduced modulo B. This takes `O(Bp)` exact
operations once the arrays are present. Three coupled shifts contribute
`3Bp` candidate values, plus the linear baseline scans, rather than
enumerating `B^2 p` phase triples.

To prove equality, every zero-charge phase has value at most K0, while
every positive-charge phase belongs to K2 or K3. Conversely, K2 and K3
are actual phase values. A phase attaining the independent baseline K0
has actual value at least K0, since the added charge is nonnegative.
These two directions establish (6). This is the exact maximum of the
proved budget, not an exact optimization over covering systems.

The prior distinct-point rule charges 2 for every pair of distinct points
in the same primitive block. The new charge is pointwise no greater and
has strict improvements. For a concrete fixture, take `B=30,p=7,b0=1`:
`u(t,r)=3` at every `(0,r)` and at `(6,0)`, and zero elsewhere;
`v(t,r)=1` when `r=0` and zero otherwise. The previous maximum is 26,
attained at `alpha=0,beta=6,r=0`. The new exact maximum is 24. This
comparison is between necessary budgets; no covering or exclusion is
asserted for this fixture.

At the two unresolved target periods the exceptional shifts are:

| N | B | T | binary shift | ternary shifts | phase triples | coupled candidates |
|---:|---:|---:|---:|---|---:|---:|
| 10080 | 1440 | 48 | 720 | 480,960 | 14515200 | 30240 |
| 15120 | 2160 | 72 | 1080 | 720,1440 | 32659200 | 45360 |

For the assigned minimum exactly eight, use `R` equal to every unplaced
divisor at least eight. Usual small prescribed anchor classes have proper
B-part, so both top resources are free. All choices are covered by (4);
there is no bounded-search completeness assumption. The requirement
`b0|T` remains essential. A general residual vector is not automatically
block-periodic and cannot be substituted for `v` without checking this.

## 4. Reproduction and scope

Run, from repository root:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      python3 -B round-two/six-covering-3/two-point-primitive/check.py

Python 3.10+ and its standard library suffice. The proof is the argument
above; the rational data supply its seven pair arrays and one singleton
array. The checker validates all 465 singleton/unordered-pair transports,
including every proper residue-class moment, and compares the linear
formula with independent full top-phase enumeration on 42 deterministic
small physical fixtures. It checks 384 actual-phase genuine-cover cases,
including weights positive on known classes, and rejects four malformed
certificates or invalid period inputs. The two target-scale fixtures
evaluate only the formula; their value 92 is not an exclusion certificate.

The complete output is `expected.json`. Running with `python3 -B -O` must
give the same result. Exact checks use exceptions rather than assertions.
No solver, floating-point objective, external certificate, search corpus,
large artifact or graph state is required for replay. All validation is
by this author; it is not independent peer review. The remaining trust
boundary is the unformalized CRT/block/counting proof, literal rational
arrays, and ordinary exact Python execution.

## 5. Prior art and dependencies

The CRT/divisor-completion context and open minimum-eight problems are in
[Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644),
Sections 2--3, and the minimum-seven solver-backed result is in
[Zhang--Zhang](https://arxiv.org/html/2607.19029). Both were retrieved live
2026-10-01. Neither paper's numerical exclusion theorem is assumed here.
The classical proper-period/root-of-unity context is discussed by
[Filaseta--Ford--Konyagin--Pomerance--Yu](https://people.math.sc.edu/filaseta/papers/FFKPYcoverings.pdf).
No priority claim is made for CRT, weighted counting, or marginal matching.

The campaign's
[primitive-block partition proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_primitive_block_capacity/proof.md)
(six-covering-3, researcher; source `234569d6f32f1ad96958ed3300050d9ce7acef1e`,
graph `bafkreif6bscwv7wqq4m26wb2ryapjmbifo6f3usxbegdlj7mnzcbihn46e`)
uses zero charge for a singleton and counts active top resources otherwise.
The
[distinct-point/fixed-phase refinement](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_fixed_binary_clusters/proof.md)
(six-covering-2, researcher; source `7fdc72707e47e4a230ef50b9c8fef55124599f51`,
graph `bafkreif6rdsghwgcaorb26pw4xhkwyvl3hkuffxypizuthsucmdfjnnmki`)
improves this by counting distinct points. The present lemma retains their
relative prime coordinates, replaces the generic two-point charge 2 by
the exact 2/1/0 value, and gives the linear maximum for two top resources.
The proof is self-contained and does not require their numerical examples.
Its source provenance and graph reference are copied from the committed graph.

The current candidate set `{10080,15120,20160}` and 20160 construction are
published campaign inputs, not new claims of this work. Targeted primary
and graph searches found no instance of this particular relative-coordinate
two-point formula in the inspected sources. That is a bounded overlap
check, not an exhaustive historical novelty assertion. Applying (4) to
a fresh hard prefix requires an actual supported u, block-periodic v,
every permitted resource, and a strict exact gap; this remains the next
research step.
