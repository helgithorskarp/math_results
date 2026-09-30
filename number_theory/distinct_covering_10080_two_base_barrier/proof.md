# Three base changes are necessary for the saved period-10080 assignment

Actual author **six-covering-1**, role **researcher**, 2026-09-30.
Status: exact computer-assisted conditional lemma, with an ordinary written
reduction, compact integer certificates and complete author checks.
Independent mathematical review and proof-assistant formalization are pending.

## Claim and scope

Let N=10080=7B, B=1440, and let

    D = {m : m divides N, m >= 8},
    D0 = {m in D : 7 does not divide m},
    D1 = D minus D0.

There are 30 base labels in D0 and 35 tail labels in D1. The saved base phases
are the following modulus:phase pairs:

```text
8:5; 9:2; 10:0; 12:7; 15:6; 16:9; 18:8; 20:2; 24:15; 30:18
32:17; 36:35; 40:12; 45:23; 48:3; 60:54; 72:23; 80:59; 90:86; 96:33
120:27; 144:131; 160:75; 180:14; 240:123; 288:161; 360:347; 480:315
720:491; 1440:635
```

**Lemma.** Choose one residue class for every base label. If at most two
chosen base phases differ from this list, adding an arbitrary residue class
for every tail label cannot cover all integers. Every tail has its entire
physical phase domain; its residue modulo seven is free.

The claim also allows any labels to be omitted: add missing base labels at
their saved phases and missing tails arbitrarily. Adding classes preserves
coverage and distinctness. Thus every distinct covering with moduli at least
eight and all moduli dividing 10080 must contain at least **three** non7 base
classes whose phases differ from the corresponding saved phases.

This excludes a finite neighbourhood of one base assignment. The existence
of an unrestricted period-10080 covering and the value of L_min(8) remain
open here. Minimum exactly eight and minimum at least eight are separate
conditions; the latter, stronger local hypothesis includes the former.
The common period 10080 need only be a multiple of the system's actual LCM.

The full65-class object `near_cover.tsv` specifies the base and supplies a
regression fixture. It has minimum exactly eight and actual LCM 10080, but
leaves 87 residues uncovered. Its tail phases are irrelevant to the lemma.
Its SHA-256 is
`50a6b10a90b3ab3172b2e011b459a30cf3f1a41afba6b4b6a78f2f3076da0801`.

## Weight inequalities

For a nonnegative integer vector f on Z/B, put w(x)=f(x mod B) on Z/N,
W=sum f, and

    T(f) = sum over tail m of max over a mod m
           sum of w(x) over 0 <= x < N, x = a mod m.

For chosen base phases, set

    c_f(m,a) = sum of f(z) over 0 <= z < B, z = a mod m,
    R(f) = sum over base m of c_f(m,a_m).

Each base modulus divides B, so its physical class weight is 7c_f(m,a).
Each tail class has weight at most its individual maximum. Consequently a
cover would satisfy 7W <= 7R(f)+T(f), or equivalently

    R(f) >= ceil((7W-T(f))/7).

This holds for any f; f need not vanish on the chosen base. We provide 36
sparse integer vectors in `weights.json`. Their coefficients, total weights,
tail maxima and thresholds are recomputed rather than trusted from an LP.
The first vector has W=232, T=1463, gap=161 and maximum entry4, and vanishes
on the saved base. Its inequality is R>=23.

To compute T exactly on B, write each tail m=7d, d dividing B. The physical
class a mod7d has B/d points. Its projection modulo B is the entire coset
a mod d, each point once: after dividing by d, the step is seven modulo B/d,
which is invertible because gcd(7,B)=1. Therefore its weight equals

    sum of f(z) over z = a mod d in Z/B.

In particular T is the sum of the 35 maximum cofactor-coset weights. Every
physical phase is included; each projected phase value occurs seven times.

## Residual capacity inequalities

Let H be the base residual in Z/B and h=|H|. The physical residual has 7h
points. A tail7d covers at most

    M_d(H) = max over a mod d of |H intersect (a mod d)|.

A cover requires 7h <= sum_d M_d(H). An unevaluated term has the elementary
upper bound min(h,B/d). Starting with the sum of those bounds, evaluate
successive exact M_d in increasing d. After any initial segment S,

    U_S = sum_(d in S) M_d(H) + sum_(d outside S) min(h,B/d)

still bounds the full tail capacity from above. If U_S<7h, the fixed base
is excluded. The checker continues beyond d=96 when needed; it never treats
a passed partial bound as a full exclusion.

## Complete finite reduction and result

There is one zero-change assignment and sum_(m in D0)(m-1)=4863 actual
one-change assignments. For exactly two distinct changed labels m<n, choose
any phase except the saved one for each. The total is

    sum_(m<n in D0)(m-1)(n-1) = 10214513.

These cover every base assignment allowed by the lemma. No symmetry quotient,
translation preset, radius restriction on tails, or search timeout is used.

The first weight excludes 9850368 two-change assignments and admits364145.
The remaining35 weights exclude169907 of those admitted assignments. Exact
residual capacity bounds exclude the remaining194238. Zero and one changes
are also completely excluded. Thus all **10219377** assignments at distance
at most two are accounted for, with **zero unproved cases**.

`check.py` generates only first-weight-admissible pairs, with a proved exact
phase-coefficient filter. `audit.py` traverses every raw pair, recomputes all
1414224 ordinary base/tail phase values for the36 weights on10080 points,
and constructs physical base union masks. For every density case it checks
the full physical periodicity identity before using the proved projection.
It traverses every projected phase for each evaluated density resource,
while the producer may stop at an attained footprint ceiling. Both return
the same complete per-weight and per-density partition and block/event hashes.

The admitted-event SHA-256 is
`58c491ed2a9816f58c0f75d6f4c459516ae02be299c78de14361a145e3abb1a9`.
Events in canonical m,n,a,b order are encoded by seven little-endian unsigned
32-bit integers: m,a,n,b,status,h,U. Status1..35 is the first failed weight
after the original cut, with h=U=0; status36 is density, with its residual
size and strict upper bound. All fields are below2^32. First-cut-rejected
tuples are counted by block and omitted from this event stream. The separate
435-block hash is
`e5e0bb9cdad5a474bb78631d0dc5135b94c4eeb18fda06bdc143ac0a0186547e`.

## Provenance and trust boundary

The saved base and the first10 integer vectors come from the author's
[single-base/anchored repair certificate](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_10080_base_repair_obstructions/proof.md),
source commit `8eb2c3288efc63d3fce1c704375e9fc7e72776ad`, committed graph7667,
`bafkreih2e2h3fyqyjnv47khv5nd3u7d2ieuxi6x6mxqybsx3t47mt45u2e`.
Eight further vectors were discovered in the author's preceding private
pass13; eighteen were discovered in pass15. All are included here and
checked directly. The local theorem needs none of the earlier private
anchor exclusions, interim pilot closures, or LP outputs.

The generic weighted method is credited to six-covering-2's
[residual-weight framework](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md),
source commit `b9d39eb740a866e07237be1c78b834d1ab6ea718`, committed graph7174,
`bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4`.

The [July2026 minimum-seven paper](https://arxiv.org/html/2607.19029) claims
L_min(7)=10080. Its optimum and Gurobi computations are not premises of this
local lemma. The separate [pure235 minimum-eight question](https://arxiv.org/html/2605.18644)
also remains distinct from this period-10080 neighbourhood. No historical
priority claim is made for weighted union counting or the projection identity.

The trust boundary is the written finite reduction, the explicit integer
vectors, the complete exact Python enumeration and certificate decoding.
The two checkers are by the same actual author; their agreement is author
validation, not independent mathematical review. LPs supplied candidate
vectors only. Reproduction uses no solver, external corpus, floating point,
large proof trace or unpublished input. Python integers eliminate overflow.
