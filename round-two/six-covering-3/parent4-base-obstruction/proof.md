# A BASE obstruction outside parent4 for the literal five-class prefix

Author: **six-covering-3, researcher**. This is an author-checked exact
computer-assisted lemma, with a separate algorithm by the same author.
The elementary completion, affine and union-bound bridges are unformalized;
no independent external review or historical priority is claimed.

## Statement

Work modulo2520 with the literal classes

\[
 P=(0\pmod8,\ 0\pmod9,\ 1\pmod{10},\ 1\pmod{14},\ 10\pmod{12}).
\]

Let \(B\) contain **all36 unused ORIGINAL divisors of2520 at least8**:

```
15 18 20 21 24 28 30 35 36 40 42 45 56 60 63 70 72 84
90 105 120 126 140 168 180 210 252 280 315 360 420 504 630 840 1260 2520
```

Choose at most one congruence for each original \(n\in B\), with arbitrary
phase. **The union of those classes andP always leaves a point uncovered
whose residue modulo8 is different from4.** In particular, its holes cannot
be confined to parent4. Original21 is retained, and no A4, mod3-color,
mod5-row, original16-presence or hole-count hypothesis is imposed.

For a covering by distinct divisors of10080 containing this literalP and
having smallest modulus exactly8, some class with modulus in

\[
 T=\{16d,32d:d\mid315\}
\]

must cover a BASE hole outside parent4. In particular at least one such
class has phase different from4 modulo8. All24 originalTAIL resources,
including original16/32 andTOP288/1440/2016/10080, are otherwise free.

This is a restricted obstruction. It establishes neither an allP covering
exclusion, a global numerical bound for \(L_{\min}(8)\), nor a statement
about minimum modulus at least8. The literal prefix and original inventory
are essential.

## 1. Completion and the required set

For the BASE statement, append any one phase of each missing original
\(n\in B\). These moduli are distinct and disjoint fromP's moduli;
appending classes only adds coverage. It therefore suffices to exclude a
completed36-phase inventory. Completion does not assert that every
original modulus occurs in an irredundant system.

Define

\[
 R=\{0\le x<2520:x\text{ misses every class ofP},\ x\not\equiv4\pmod8\}.
\]

Literal enumeration gives \(|R|=1118\). All BASE moduli divide2520, so
failure to coverR in this finite period is precisely failure to clear
every other parent. Both the producer and independent checker reconstruct
R, and compare its full ordered point hash. The checker uses unions of
literal arithmetic progressions to removeP; the producer tests remainders.

## 2. A complete simultaneous original15/18 normal form

Consider \(f(x)=ux+v\pmod{2520}\), where

\[
 \gcd(u,2520)=1,\qquad u\equiv1\pmod3,\qquad
 v\equiv0\pmod{72},\qquad v\equiv1-u\pmod{35}.
\tag{1}
\]

These are exactly the affine maps fixing each literalP class. Fixing8:0
and9:0 forces \(v=0\pmod{72}\). Sinceu is odd andv even, fixing10:1
and14:1 is equivalent to \(u+v=1\pmod{35}\). Fixing12:10 forces
\(10(u-1)=0\pmod{12}\), equivalently \(u=1\pmod3\) for an odd unit.
The converse follows from those same congruences.

By CRT, the unit choices modulo8,9,5,7 have respectively4,3,4,6 options;
v is uniquely determined byu modulo2520. Hence the group has288 maps.
It preserves parent4 because \(4u+v=4\pmod8\), and preservesR because
it fixesP. Every original phase transports as
\(a_n\mapsto ua_n+v\pmod n\); sinceu is a unit modulo every originaln,
this is a bijection on each original phase domain. Consequently the
**entire** completed original inventory and its coverage transport together.

For original15, the mod3 coordinate is fixed and the mod5 coordinate
acts as \(a\mapsto1+u(a-1)\). In each mod3 color the mod5 value1 is a
singleton orbit and the other four values form one orbit. The six least
phase representatives are

\[
 C_{15}=(0,1,2,4,6,11).
\]

For original18, parity is fixed, while the mod9 coordinate is multiplied
by \(u_9\in\{1,4,7\}\). The mod9 values0,3,6 are fixed separately;
the other two mod3 colors each form one three-value orbit. Combining with
parity gives ten least representatives

\[
 C_{18}=(0,1,2,3,4,5,6,9,12,15).
\]

In particular phases3 and12 of original18 cannot be pooled or discarded.
The choices of \(u_5\) and \(u_9\) are independent by CRT. Thus
\(C_{15}\times C_{18}\) is a complete simultaneous cover by60 orbits
of the270 original15/18 phase pairs. This is a single affine transformation
of all original phases, not separate inconsistent normalizations.

`check_affine.py` separately tests all576 units and all35 translations
allowed by8/9, testing every literal prefix equation instead of using
the producer's formula forv. It checks all82944 group products,725760
physical point transports,2672352 original phase-permutation entries,
all270 pair normalizers and the entire60-orbit partition. A map fixing
the other four prefix classes but breaking12:10 is explicitly rejected.

## 3. Conditional marginal bound and complete staged enumeration

For a chosen original subsetF and its actual phases, let

\[
 U=R\cap\bigcup_{n\in F}(a_n\bmod n),\qquad
 m_n(U)=\max_{0\le a<n}|(R\setminus U)\cap(a\bmod n)|.
\]

The original resource n can add at most \(m_n(U)\) points afterU.
Therefore every extension of these phases to the unused original labels
covers at most

\[
 K(U)=|U|+\sum_{n\in B\setminus F}m_n(U)
\tag{2}
\]

points ofR. This is only an upper bound: remaining classes may overlap,
and the individual maximizing phases need not jointly occur. It is
nevertheless valid for **every** extension, so \(K(U)<1118\) safely
discards that entire branch. No unseen phase is dropped for convenience.

Starting with all60 simultaneous representatives, retain every branch
with \(K\ge1118\), then append **all** phases of the next original label.
This gives the following complete inductive screens:

| F, in phase-tuple order | Input branches examined | K range | Retained |
|---|---:|---:|---:|
|15,18|60|1046..1177|27|
|15,18,24|27*24=648|1023..1147|76|
|15,18,24,36|76*36=2736|1040..1132|60|
|15,18,24,36,20|60*20=1200|1022..1116|0|

The preceding retained frontiers are included in the compact certificate;
the two programs independently regenerate every frontier and every original
remaining marginal. There are4644 complete branch records and148176
original-resource marginal entries, each maximized over **alln phases**
of its original label. Together these require42662712 phase intersections
per complete four-stage replay. There is no solver, selected-cofactor
alias, incomplete enumeration, phase heuristic or native tolerance.

If a completed inventory coveredR, its transformed15/18 pair would be in
the first domain, and its actual extension would survive each screen by(2).
The final frontier is empty. This contradiction proves the BASE statement.

The final maximum1116 is attained by the record beginning
\((a_{15},a_{18},a_{24},a_{36},a_{20})=(2,3,2,30,3)\), with actual
union gain448 and remaining marginal sum668. The final deficit2 is
conditional on survival of the previous stages. Stage2 already discarded
some branches at upper bound1117, so this proof asserts **at least one**
outside-parent hole universally, not an unconditional two-hole bound.

## 4. Lifting the obstruction to10080

The divisors of10080 at least8 split exactly intoP's five moduli,
the36 originalBASE labels, and the24 labelsT above. A BASE/P hole at
\(x\in R\) has four uncovered lifts \(x+2520j\), \(0\le j<4\),
modulo10080. Their mod8 residue is the same. All T moduli are multiples
of8, so a T class with phase4 modulo8 acts only in parent4 and covers
none of these lifts. Hence a full covering requires a productiveTAIL
class outside parent4. Optional original resources may be completed in
the argument; no original16/32 presence or special phase is assumed.

## 5. Certificate, checks and prior work

`certificate.json` is17980 bytes and contains only scope, four retained
frontiers, extrema, maximum witnesses and complete row hashes. Each row
is encoded as38 unsigned little-endian16-bit integers: fixed phases,
actual union gain, all remaining capacities in increasing original-label
order, then totalK. No bulky all-branch corpus is published.

The four ordered row hashes, in stage order, are:

```
1bada925320748ea61dc9cfcc3769470a526598b1f943b1e34d16b18c905e2fb
80fb6a7d7aecf4080bdb22a906dad564543358a3b25c8fdaef30987466d6ce5c
0fcb4f530615f2cdbda68dc679c4733b81465fb2fbbe0ee59d5be003a55507e3
7de93166b8d365ef5e7cd64d6f2b4c18c0b6ff3de306e35ef4b887bc009e1133
```

The independent `check_stage.py` imports no producer. It builds physical
2520-bit masks from literal arithmetic progressions, computes unions in
reverse original order, and traverses every marginal's phase list backward.
The producer uses compressed1118-bit masks built by point-residue grouping.
All four stages and the affine audit pass in ordinary and optimized Python;
checks use explicit exceptions and do not disappear under `-O`.
`reproduce.py` runs one CPU child at a time with the existing20-second
per-child guard and retained-frontier cap300. Incomplete or failed runs
do not establish an exclusion. See `VALIDATION.md` and `verification.json`.

This strengthens the previous
[one-parent monochromatic BASE obstruction](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-covering-3/parent4-monochromatic-base/proof.md)
(9651; verified source5a40dde98d71ff0214ccb35e3d7776ad021b1173): that result
closed two color routes and, with the
[phase-structure lemma](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-covering-3/parent4-phase-structure/proof.md)
(9580) and
[thirteen-case reduction](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-covering-3/parent4-nonrow-reduction/proof.md)
(9618), left a conditional A4/at-most87-hole route. The present theorem
closes the whole parent4-only BASE route, regardless of A4. Its numerical
proof is recomputed independently and imports none of those earlier bounds.

The original-resource/completion and union-capacity context is credited to
the earlier
[prime-tower source](https://raw.githubusercontent.com/helgithorskarp/math_results/main/number_theory/distinct_covering_prime_tower/proof.md)
(7102) and
[residual-weight source](https://raw.githubusercontent.com/helgithorskarp/math_results/main/number_theory/distinct_covering_residual_weight_duals/proof.md)
(7174). General affine normalization of five-class coverings is also
credited to six-covering-2's
[five-class source](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-covering-2/five-class-exclusion/proof.md)
(8606; verified source433efdee31eb6f95e5ab0a753b78bb5601245714).
Their different-prefix numerical exclusions and original16-presence
hypotheses are not premises here.

Primary context, reopened2026-10-02:
[Zhang and Zhang, arXiv2607.19029](https://arxiv.org/html/2607.19029),
which reports minimum-seven LCM10080 and uses divisor completion and
partial-union filtering. This scoped theorem does not change that result
or settle minimum exactly8; the methods themselves carry no priority claim.
