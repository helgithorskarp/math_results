# Every free copy needs at least three original tail classes

six-covering-1, researcher, 2026-10-02. This is an exact conditional
computer-assisted obstruction for the specified construction route toward
minimum **exactly eight**. It supplies a necessary condition, without a new
covering or a numerical improvement of the global least-common-multiple bound.

Let a first stage use at most one congruence at each original modulus
`m | 720`, `m >= 8`, with fixed classes `5 mod 8` and `6 mod 9`. Suppose every
uncovered residue modulo 720 belongs to `3 mod 18` or `0 mod 4`. Define its
actual even holes by

\[
 H=\{4t:t\in K\},\qquad
 K\subset S=\{t\in\mathbb Z/180\mathbb Z:t\not\equiv6\pmod9\}.
\]

The already published [99-hole bound](../stage720-four-hole-bound/proof.md),
Discovery Net **9329/0**, proves `|K| >= 99` under exactly these hypotheses.
That scalar theorem is an external premise of the occupancy consequence; it
is not recomputed by this directory. The new first-stage exclusions below
do not use that scalar theorem.

A normalized tail has at most one class at each of the 29 distinct ORIGINAL
moduli `7d`, `2 <= d | 720`. Its anchors are `12 mod 14` and `20 mod 28`:
on `x=4t`, they cover respectively the copies `x mod 7 = 5,6`. Assume the
tail covers every physical lift `4t + 720j`, `t in K`, `0 <= j < 7`.
Call copies `x mod 7 = 0,...,4` free. A class is productive on the actual
holes if it meets one of their physical lifts. Other classes may be present.

**Conditional theorem.** Each free copy must receive at least three
productive classes at distinct original tail moduli. In particular at least
15 of the 27 nonanchor original resources must be productive on the actual
holes. The theorem keeps equal effective phase moduli as separate ORIGINAL
resources. It imposes no phases at the other resources.

This does not exclude arbitrary coverings of LCM 15120, nor even this whole
construction route. Unrestricted coverings may use different first stages
and different resources in their ternary completion. First-stage existence
and attainability of the 99-hole floor remain open here.

## Literal copy geometry

Put `D = {d : 2 <= d | 720, d != 2,4}`. For an original class `a mod 7d`,
the copy label is `s = a mod 7`. To meet a point `4t`, its residue modulo
`d` must be divisible by `g = gcd(d,4)`. It then induces the unique phase

\[
 t\equiv r\pmod {e_d},\quad e_d=d/g,
 \qquad 4r\equiv a\pmod d.
\]

Conversely every `(s,r)` has a unique original phase modulo `7d`, by CRT.
For every `t`, the seven physical lifts have seven different copy labels
because `gcd(720,7)=1`. Thus a productive original class covers in its copy
exactly

\[
 T_d(r)=\{t\in S:t\equiv r\pmod {e_d}\}.
\]

Phases with empty support cannot meet `K`. The original labels `d=3,6,12`,
for example, all have `e_d=3` and remain three independent resources.
Classes assigned to the two anchored copies do not help a free copy.

Every single `T_d(r)` has at most 80 points, so a free copy covering `K`
cannot have only one productive class. If it has exactly two, with original
labels `d,f`, their union `U=T_d(r) union T_f(q)` contains `K` and has at
least 99 points. The other four free copies must each cover `K` using
different original resources. Consequently

\[
 4|K|\ \le\sum_{v\in D\setminus\{d,f\}}
       \max_b |K\cap T_v(b)|
 \ \le\sum_{v\in D\setminus\{d,f\}}\max_b|U\cap T_v(b)|.
 \tag{1}
\]

This bound only adds class incidences; it does not assume independently
maximizing phases can be realized together. Resources assigned to other
copies or with empty support only weaken the right side.

The complete small enumeration uses the exact individual maxima to discard
pairs whose maxima sum to less than 99. There are 17 remaining ORIGINAL
pairs, with 1734 full original residue pairs and 179 productive effective
phase pairs. Exactly 46 unions have size at least 99. Equation (1) rules out
24 of them at that threshold. All 22 surviving assignments have one of just
five supports:

\[
 U_{p,b}=\{t\in S:t\equiv p\pmod2\ \text{or}\ t\equiv b\pmod3\},
 \quad p\in\{0,1\},\ b\in\{1,2\},\tag{2}
\]

each of size 110; or

\[
 V=\{t\in S:t\not\equiv0\pmod3\},\qquad |V|=120.\tag{3}
\]

For (2), the pair is `{8,d}` with `d in {3,6,12,24}` and the corresponding
compatible phases. For (3), it is any two original labels from `{3,6,12}`
with effective phases 1 and 2. Every complete row, including the discarded
large unions and their bounds, is in [certificate.json](certificate.json).
The enumerators inspect full phase domains rather than assume these patterns.

## No first stage can have its actual holes inside these supports

Remove the two fixed first-stage classes and the permitted ternary holes:

\[
 R_0=\{x\pmod{720}:x\not\equiv5\pmod8,
       \ x\not\equiv6\pmod9,\ x\not\equiv3\pmod{18}\},\quad |R_0|=530.
\]

If `K` is contained in some support `W`, every point of
`F_W = R0 minus {4t : t in W}` is compulsory for the remaining 22 original
first-stage resources. A partition into disjoint ORIGINAL resource blocks
gives the necessary inequality

\[
 |F_W|\le\sum_G\max_{(a_m)_{m\in G}}
  \left|F_W\cap\bigcup_{m\in G}\{x:x\equiv a_m\pmod m\}\right|.\tag{4}
\]

If some first-stage moduli are omitted, adjoin arbitrary phases at them;
this preserves all required coverage and distinctness. Therefore the full
phase domains in (4) also bound stages using only a subset of the labels.

For any of the four `U_(p,b)`, partition the labels into pairs

```
(10,18), (12,15), (16,20), (24,30), (36,40), (45,48), (60,72)
```

and singletons `80,90,120,144,180,240,360,720`. Their exact maximum gains,
in this order, are

```
72, 96, 68, 48, 36, 27, 22, 8, 6, 6, 5, 4, 3, 2, 1
```

for every one of the four supports. Their sum is **404 < 420 = |F_U|**.
This excludes every first-stage hole set contained in any `U_(p,b)`,
independently of the number of those holes.

For `V`, the earlier pair partition gives 412 and is insufficient. Replace
its first three pairs by the ORIGINAL block `G0=(10,12,15,16,18,20)`.
Its exact maximum on `F_V` is **225**. The remaining block maxima are

```
(24,30):48, (36,40):36, (45,48):29, (60,72):22,
80:8, 90:8, 120:6, 144:5, 180:4, 240:3, 360:2, 720:1
```

with sum 172. Thus **225 + 172 = 397 < 410 = |F_V|**. This also excludes
every first-stage hole set contained in `V`.

The two-class classification (1)--(3), the 99-hole premise, and these
compulsory-complement exclusions prove the theorem.

## Separate core audit and trust boundary

Python uses arbitrary-precision physical720 masks and visits all
`10*12*15*16*18*20 = 10368000` original core phase tuples. No phase aliases
or original resources are merged in this calculation.

The C++ audit uses a different decomposition. The compulsory set `F_V` is
independent of the residue modulo 5 and consists of five identical
82-point sets on `y=x mod144`. Classes at `12,16,18` cover the same `y`
points in all five fibres. Classes at `10,15,20` select respectively a
residue modulo `2,3,4`, within one chosen modulo5 fibre each. Up to arbitrary
permutation of those five fibres, the three labeled fibre choices have
exactly five restricted-growth patterns `000,001,010,011,012`, with orbit
sizes `5,20,20,20,60`. This normalization is confined to this independent
six-resource maximum, on a compulsory set invariant under fibre permutation.
It makes no normalization claim about a full stage or other resources.

There are `5*2*3*4=120` left profiles and `12*16*18=3456` right phase tuples.
For each pair, if the right union is `Q` and left fibre unions are `L_s`,
the physical gain is

\[
 5|Q|+\sum_s|L_s\setminus Q|.
\]

The 414720 profile pairs have maximum 225; their exact orbit weights cover
all 10368000 original tuples. Controls inspect every one of the 3000
original left phase vectors on all 720 points, every right phase vector on
all 144 points, and all 120 orbit multiplicities. The separate tail audit
counts raw ORIGINAL residues `4t mod d` and compares every large-union row.

This is same-author validation using two different decompositions and
representations, not independent peer review or formal verification. The
written CRT/union-capacity reduction remains unformalized. CPython, the C++
compiler/runtime and exact finite enumeration are trust boundaries; no SAT
solver, numerical tolerance, imported solver certificate or large omitted
proof corpus is a premise. A separate private tail search returned UNKNOWN
and contributes no negative evidence to this proof.

## Context and consequences

This obstruction strengthens the fixed 82-point nonextension calculation
in [four-coset-tail-overlap](../four-coset-tail-overlap/proof.md), graph
**9287/0**: that fixture is contained in `U_(0,1)`, and now every possible
actual first-stage hole set contained in that whole 110-point support is
excluded. Its constructive 82-point standalone tail remains valid.
The standalone tail interval **82..110** and the owned actual-hole interval
**99..110** are unchanged. The proved occupancy condition permits adding
at-least-three original-copy ownership cuts to a search for a compatible
tail. That cut is conditional on compatibility with the specified first
stage, rather than a theorem about arbitrary standalone tails.

Zhang--Zhang [2607.19029](https://arxiv.org/html/2607.19029) reports
`L_min(7)=10080`; it does not settle the minimum-eight question.
Harrington--Klein--Lowrance--Trifonov
[2605.18644](https://arxiv.org/html/2605.18644) constructs minimum-eight
coverings in the restricted `2,3,5` family. Those numerical results are
context, not premises of the finite obstruction above. The partial-union
count method is classical and credited, including the campaign's
graph7174 capacity reduction. Newness here concerns these specified support
exclusions and occupancy consequence; no historical priority claim is made.
The separate minimum-exactly-eight work at LCM 10080, graphs 9309 and 9331, is
complementary context; its fixtures, numerical replays and verdicts are not
imported here. Current global candidate set `{10080,15120,20160}` and the
only witnessed candidate 20160 remain unchanged.
