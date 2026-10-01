# Order-seven geometric and antipodal restrictions

Let F=F_617 and H=<3^88>, of order seven. A binary coloring of F^* is
admissible if every AP `a,a+d,...,a+6d`, `d!=0`, with all seven terms
nonzero has both colors. Assume c is H-invariant.

**Lemma.** The word `y_i=c(3^i)`, `i mod88`, has maximum monochromatic
cyclic run at most six. Its antipodal phase vector
`s_i=y_i XOR y_(i+44)`, `i mod44`, has weight K different from 1,43,44.

**Corollaries.** Each color occupies 13..75 H-cosets, hence 91..525
nonzero points. For a nonquadratic admissible coloring, importing the
published order>=11 classification, `2<=K<=42`; the numbers of points
with `c(-x)=c(x)` and with `c(-x)!=c(x)` each lie in 28..588.
No existence at the surviving profiles or complete H7 classification
is asserted.

## Quotient and exact AP encoding

The prime 617 and primitive root 3 are checked directly. The cyclic
multiplicative group has order `616=7*88`. Thus H-invariance is exactly
a binary cyclic quotient word of length 88. Each retained AP gives a
support E of quotient indices; repeated indices repeat the same color.
Its constraint is the conjunction of the two disjunctions

```
OR_{i in E} y_i,    OR_{i in E} NOT y_i.
```

The direct auditor enumerates all 380072 ordered pairs `(a,d)`, removing
the 4312 APs through zero and retaining 375760. It labels cosets using
`x->x^7`, with kernel H, and finds 26488 distinct supports: 88 of rank
5, 5280 of rank 6, and 21120 of rank 7. The generator instead uses
primitive-power labels, spacing-one APs and all quotient shifts. This
is exact because division by the nonzero difference normalizes an AP
to spacing one, and multiplication adds a quotient coordinate. Complete
clause multisets are compared, rather than support counts alone.

Every support contains an even and an odd index. As 3 is a nonsquare
and H consists of squares, the two alternating quotient words are
exactly the two QR orientations, and both satisfy every retained AP.

## Complete cover of the claimed run exclusions

The actual AP `(a,d)=(418,2)` has terms
`418,420,422,424,426,428,430`. Its coordinates are
`32,0,27,5,1,13,17`, supported on `{0,1,5,13,17,27,32}`.
Multiplication by `3^j` rotates this support, and all 88 scaled APs are
independently checked. A monochromatic cyclic run of length at least
33 contains one shifted support, so it gives a forbidden AP. Therefore
the maximum run L of an admissible word is at most 32.

Suppose L>=7. Rotate a longest run to position zero and exchange colors
so it is zero. These operations preserve H-invariance and every field
AP constraint. The normalized word has

```
y_0=...=y_(L-1)=0,    y_87=y_L=1.
```

All cyclic windows of length L+1 have both colors. Conversely, this
prefix, its neighbors and the window clauses impose maximum run exactly
L. Hence every putative counterexample to the run bound has a normalized
representative in one of the **26 cases L=7,...,32**. Every case has 88
variables and `53154+L` clauses: 52976 field clauses, 176 window clauses,
and L+2 normalization units.

All 26 cases have exact positive-RUP refutations, totaling 108427
checked additions and 1576701 propagation hints. Thus L>=7 is impossible.
Nothing in this proof requires solving L=2,...,6. Those five cases
returned UNKNOWN in the recorded bounded probes and establish no
exclusion. L=1 consists of the two retained alternating QR orientations;
constant words have already been excluded by the actual AP.

## Geometric and color-size consequences

For any x in F^*, the colors on `x,3x,...,3^6x` are seven consecutive
cyclic quotient colors. The run bound makes this sequence nonmonochromatic.
If a ratio belongs to 3H, H-invariance cancels its H factors; ratios in
`3^(-1)H` give the same seven-position sets in reverse order. The two
cosets are disjoint, since 3^2 is not in H, and together contain fourteen
ratios. This is a geometric consequence of AP constraints under the
explicit H-invariance hypothesis, not a claim about arbitrary field
colorings.

Let k be the number of quotient positions of one color. Between its k
occurrences, all runs of the other color have length at most six, so
`88-k<=6k` and k>=13. Apply the same argument to the other color to get
k<=75. Every H-coset has seven elements, yielding field color sizes
between 91 and 525.

## Three complete antipodal phase models

In the quotient, negation adds 44, since `-1=3^308` and `308 mod88=44`.
Pair positions i and i+44, and define

```
X_i=y_i,    s_i=y_i XOR y_(i+44),    i=0,...,43.
```

For a fixed phase vector s, substitute `y_(i+44)=X_i XOR s_i` into each
field clause. A positive occurrence of y_i becomes `+X_i`; a positive
occurrence in its opposite coset becomes `+X_i` when s_i=0 and `-X_i`
when s_i=1. The complementary clause negates every substituted literal.
Opposite signs on the same variable make a clause tautological, which
can be removed; duplicate clauses can also be removed. No other
constraint is discarded.

The following normalized profiles cover the respective whole classes:

* K=44: all phases one. Color exchange fixes X_0=0.
* K=1: the unique opposed pair is moved to index zero by scalar rotation.
  Color exchange fixes X_0=0; phases are one at zero and zero elsewhere.
* K=43: the unique agreed pair is moved to zero in the same way, giving
  zero phase at zero and ones elsewhere, with X_0=0.

The phase is periodic modulo44. Scalar rotation shifts it modulo44,
including when the lower/upper representatives interchange. Global
color exchange leaves it unchanged. The remaining X_i are free, so
the above normalizations lose no colorings. This covers
`(1+44+44)*2^44=1565704557953024` labeled quotient words in the three
phase classes, before normalization; it does not cover all 2^88 words.

The independent signed auditor uses explicit multiplication of H-cosets
and their negatives to partition all 616 nonzero elements into 44 pairs
of seven-element cosets. It does not import the generator or its Euler
labels. It enumerates all field APs again, performs the semantic signed
substitution, and compares the complete clause sets plus normalization.
The three 44-variable CNFs have respectively 21121, 29509 and 24595
clauses. Their exact refutations total 15246 checked additions and
173812 propagation hints. Therefore K=44,1,43 are impossible.

## Imported nonquadratic corollary

When K=0, c is invariant under -1 as well as H. Their generated subgroup
has order 14 because H has odd order seven. The published order>=11
classification forces the quadratic-residue coloring up to global color
exchange. This earlier theorem is explicitly imported, with source and
graph references in README.md. Our new computational cuts alone leave
K=0 as an allowed phase weight.

For a nonquadratic admissible coloring, K>=1; exclusion of 1,43,44 now
gives `2<=K<=42`. Each opposed pair accounts for fourteen field points
at which `c(-x)!=c(x)`, and every agreed pair accounts for fourteen
points with equality. Thus the two counts are `14K` and `14(44-K)`,
each between 28 and 588.

## Refutation trust boundary

For every clause added by the RUP checker, temporarily negate all its
literals and replay active unit/conflicting hint clauses to contradiction.
The addition follows from active clauses. Clause deletion does not
affect the induction that the initial CNF implies all active additions;
an accepted empty clause therefore proves the original CNF UNSAT.
Tautological additions are valid directly. Unknown/deleted hints used
in propagation, unsupported negative RAT hints, malformed syntax,
out-of-range literals and missing empty conclusions are rejected.

All 29 exact traces total **123673 additions and 1750513 propagation
hints**. They are replayed in normal and optimized Python; guards use
explicit requirements and remain active under -O. The solver and
converter merely propose traces and are not soundness premises.
The soundness boundary comprises the published source and exact
auditors/checker, Python/runtime, the elementary quotient/cover argument,
and the prior theorem for the explicitly imported corollary. Budget
exhaustion, missing traces and incomplete coverage never prove a
negative result. This is not a formalized or independently peer-reviewed
proof, and it gives no interval upper bound for W(2,7).
