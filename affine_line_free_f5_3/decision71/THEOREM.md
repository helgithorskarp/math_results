# The exact line-free maximum in F_5^3

**Complete exact computer-assisted author proof; independent review of
this exact-value theorem is pending.** All 109,676 lift formulas have
verified UNSAT certificates, and the complete evidence corpus has been
audited against regenerated inputs.

**Theorem.** The maximum cardinality of a subset of $\mathbb F_5^3$
containing no complete five-point affine line is

\[
r_5(\mathbb F_5^3)=70.
\]

Equivalently, the minimum cardinality of a set meeting every affine line
of $\operatorname{AG}(3,5)$ is 55. The known 70-point construction is
checked directly. For the upper bound, suppose a line-free set $S$ has
size 71. Sections 1–5 put it into one of exactly 109,676 direct point
formulas; Section 6 excludes every formula by a checked certificate.
Any larger line-free set would contain a 71-point subset, so the proof
does not require the earlier 72-point exclusion.

There are two complete routes to the pair cover used below. The team's
[two-low-plane theorem](../low_pair71/THEOREM.md), due to Team A
researcher 3, forces two nonparallel planes of size at most nine. Its
fourteen exact moment/incidence certificates give the stronger bound
$a_7+a_8+a_9\ge117641713/100000000>1$. This supplies fifteen pair
types, all contained in our fixed twenty-type family. The public verifier
replays that theorem and checks the containment explicitly.

Sections 1 and 2 give an alternative, weaker counting argument sufficient
for the same twenty-type cover. It was developed for this proof run before
the stronger teammate result was available. Keeping the fixed complete
family preserves every running proof input and also gives a separate
reduction route. None of the extra five types is used to assume a symmetry
or discard an unexamined candidate.

## 1. Exact plane spectra and the incidence system

Every line-free plane has at most 16 points. Both planar programs in this
package verify this by excluding every 17-subset. Hence each plane section
of $S$ has size between seven and 16: its four parallel companions
contain at most 64 points.

If a line meets $S$ in $k$ points, the six planes containing it have
total section size $71+5k$. Each line point is counted six times and
every other point once. Therefore a section of size $m$ containing that
line satisfies

\[
71+5k\le m+80. \tag{1}
\]

In particular a section of size at most ten contains no four-point line.

Write a planar spectrum as $s=(m,n_0,\ldots,n_4)$, where $n_k$
counts planar lines meeting the section in $k$ points. Enumerate all
planar subsets with $7\le m\le16$, no full line, and (1). There are
exactly 91 spectra. The first program visits all $2^{25}$ subsets using
bit masks; the second separately backtracks over fixed-size subsets and
updates six incident line occupancies on insertion of each point. Their
complete spectra and labeled multiplicities agree entry by entry.

For every actual $S$, form nonnegative integer variables:

* $X_s$: planes with spectrum $s$;
* $P_p$: parallel classes with sorted section-size profile $p$, of
  length five, entries in $[7,16]$, and sum 71;
* $Y_{k,t}$: lines with $k$ selected points and sorted containing-plane
  profile $t$, of length six, sum $71+5k$, and entries in
  $[\max(7,5k-9),16]$.

These variables satisfy a 67-row, 636-column integer system $Mu=b$:

\[
\begin{aligned}
\sum_sX_s&=155,& \sum_s mX_s&=31\cdot71,&
\sum_s\binom m2X_s&=6\binom{71}{2},\\
\sum_pP_p&=31,&
\sum_{s:m(s)=m}X_s&=\sum_p c_m(p)P_p,\\
\sum_{s:m(s)=m}n_k(s)X_s&=\sum_t c_m(t)Y_{k,t},\\
\sum_{k,t}Y_{k,t}&=775,&
\sum_{k,t}kY_{k,t}&=31\cdot71,&
\sum_{k,t}\binom k2Y_{k,t}&=\binom{71}{2}.
\end{aligned} \tag{2}
\]

Here $c_m$ is the multiplicity of $m$ in a profile. The middle
incidence equations range over $m=7,\ldots,16$ and $k=0,\ldots,4$.
Every plane contains 30 affine lines; every point lies on 31 lines and
31 planes; every pair of points lies on one line and six planes. These
facts give every row of (2); no sufficiency assertion about (2) is used.

## 2. Low planes and the unique-low-plane obstruction

Let $a_m=\sum_{s:m(s)=m}X_s$, and $a_{\le j}=\sum_{m\le j}a_m$.
The two certificates in [basic_certificates.json](basic_certificates.json)
give integer $z$, positive $D$, and the objective vector $q_j$ with

\[
M^Tz\le Dq_j.
\]

Their exact lower bounds are

\[
a_{\le9}\ge\frac{31}{200}>0,\qquad
a_{\le10}\ge\frac{78461}{62500}>1.
\]

Since the counts are integers,

\[
a_{\le9}\ge1,\qquad a_{\le10}\ge2. \tag{3}
\]

There is a further useful restriction. Suppose $a_{\le9}=1$. For a
parallel or pencil profile $t$, let $L(t)=\sum_{m=7}^9c_m(t)$.
Every pair of affine planes is either parallel or meets in exactly one
affine line. Consequently

\[
\sum_p\binom{L(p)}2P_p+\sum_{k,t}\binom{L(t)}2Y_{k,t}=0, \tag{4}
\]

and for $m=10,\ldots,16$,

\[
\sum_p L(p)c_m(p)P_p+\sum_{k,t}L(t)c_m(t)Y_{k,t}=a_m. \tag{5}
\]

The right side of (5) is $a_{\le9}a_m=a_m$. These are linear
identities under the stated uniqueness assumption.

Append $a_{\le9}=1$, (4), (5), and $a_8=1$ to (2). The resulting
77-row system is denoted $N_8u=b_8$. The supplied integer certificate
satisfies

\[
N_8^Tz_8\ge0,\qquad b_8^Tz_8=-991805<0.
\]

Likewise, with $a_9=1$, the other certificate gives

\[
N_9^Tz_9\ge0,\qquad b_9^Tz_9=-992009<0.
\]

Nonnegativity of $u$ makes both systems impossible. Thus if there is
exactly one plane of size at most nine, it must have size seven.
All multipliers and every column inequality are checked with integers.
Floating-point optimization was only used to discover the certificates.

## 3. Twenty complete normalized pair types

If $S$ has a seven-point plane, combine it with another plane of size
at most ten, supplied by (3). If it has none, the preceding obstruction
and (3) imply at least two planes of size at most nine. Two sections of
size at most ten cannot be parallel, since $20+3\cdot16=68<71$.

We may therefore choose nonparallel planes $x=0,y=0$ whose sizes are
both at most nine, or whose sizes are seven and ten. A parallel class
containing a section of size at most ten has every other section in
$[13,16]$. Indeed, any companion has size at least $71-10-3\cdot16=13$.

Put the low section at label zero and multiply the coordinate by a
nonzero field element. The ten normalized profiles are:

| Index | Profile |
|---|---|
| 0 | (7,16,16,16,16) |
| 1 | (8,15,16,16,16) |
| 2 | (9,14,16,16,16) |
| 3 | (9,15,15,16,16) |
| 4 | (9,15,16,16,15) |
| 5 | (10,13,16,16,16) |
| 6 | (10,14,15,16,16) |
| 7 | (10,14,16,15,16) |
| 8 | (10,14,16,16,15) |
| 9 | (10,15,15,15,16) |

These are exactly the orbits under the four legal scalar relabelings,
not under arbitrary permutations of the five labels. Exhausting the
1, 4, 10 and 20 raw profiles with low entry seven, eight, nine and ten
independently checks the list. In particular the two different placements
of the repeated 15 entry at size nine are retained.

Order the two profile indices $i\le j$. The complete pair cover is

\[
0\le i\le j<5,\qquad\text{or}\qquad i=0,\quad5\le j<10.
\]

There are twenty types. Coordinate exchange and scalar multiplication
are affine maps, so these normalizations preserve line-freeness.

## 4. Complete quotient enumeration and affine partition

Set $w_{xy}=|\{z:(x,y,z)\in S\}|$. Every weight lies in $[0,4]$,
their total is 71, and every quotient line has weight at most 16. Its
inverse image is an affine plane. Equation (1) gives weight at most
three on either zero axis. At the intersection fiber, the two selected
planes and four other planes give

\[
w_{00}\le\left\lfloor\frac{m_1+m_2-7}{5}\right\rfloor. \tag{6}
\]

Put $d=4-w$, with total 29. Let $R,C$ be its row and column margins,
obtained by subtracting the selected size profiles from 20. The interior
$4\times4$ block determines all remaining entries:

\[
d_{x0}=R_x-\sum_{y=1}^4d_{xy},\quad
d_{0y}=C_y-\sum_{x=1}^4d_{xy},\quad
d_{00}=R_0+C_0-29+T,
\]

where $T$ is the interior sum. Equivalently, $T+w_{00}=m_1+m_2-7$.
Every retained pair has $m_1+m_2\le18$, so $T\le11$.
Interior deficits lie in $[0,4]$,
and all inferred zero-axis deficits lie in $[1,4]$. Equation (6) gives
the lower endpoint for $d_{00}$. Both endpoints of every inferred
entry are checked. The other quotient lines must have deficit at least
four. These conditions are necessary for every hypothetical candidate.

The deficit recursion and an independent recursion choosing four weight
rows and inferring the zero row give exactly **309,611** typed matrices,
with identical sorted output, including labeled multiplicities. Each
matrix is generated once in each method. The catalogue SHA256 is

```text
a6d7af5e3cb1c4b6069892164453fed01da96e7ec1718d2333ace123a6909291
```

For each matrix, select every ordered pair of nonparallel quotient lines
that can supply one of the twenty types. If their equations are
$u\cdot p=b,v\cdot p=c$, apply

\[
p\longmapsto(s(u\cdot p-b),t(v\cdot p-c))
\]

for every nonzero $s,t$ producing one of the listed normalized profiles.
These are exactly the affine images lying in the typed catalogue: the
preimages of the two zero coordinate lines determine the forms up to the
scales that are explicitly exhausted. Selecting the least pair `(type,word)`
partitions the entire catalogue into **109,676** classes.

An independent C++ program applies all 12,000 elements of
$\operatorname{AGL}(2,5)$ to **every** representative. It retains images
with one of the twenty normalized profiles, checks every orbit size and
canonical minimum, and verifies disjoint coverage of all 309,611 matrices.
This is a complete group-action check, not a sample.

Every quotient affine map lifts to an affine map in three dimensions.
No symmetry of a quotient is imposed on the point set itself.

## 5. Exact point formulas and certificate obligation

Use the 125 variables $X_{xyz}$, numbered $1+25x+5y+z$. Include one
negative clause for every complete affine line. For a fiber $F$ of
desired size $n$, include negative clauses on each $(n+1)$-subset
and positive clauses on each $(6-n)$-subset. These express exactly
$n$ selected points, including the empty positive family at $n=0$.
No auxiliary variables or cardinality-encoding library calls are used.

The interior deficit sum is at most eleven in every retained pair type.
Thus at least five interior fibers have weight four. They cannot all lie
on one quotient line, whose weight would then be at least 20, exceeding
16. Choose three noncollinear such fibers. Their missing heights determine
an affine function $\ell(x,y)$; the shear
$(x,y,z)\mapsto(x,y,z-\ell(x,y))$ puts all three holes at height zero.
Three negative unit clauses therefore give a valid normalization.

Every hypothetical 71-point set produces a satisfying assignment of one
representative formula after these affine changes. Conversely any model
of any formula is directly a 71-point line-free set. This proves the
equivalence needed for the finite decision.

## 6. Complete certificate exclusion and the exact value

Every one of the **109,676** formulas is UNSAT. CaDiCaL 1.9.5 generated
a binary DRAT trace for each input. A separate DRAT-trim process checked
each trace and had to exit zero and report `s VERIFIED`. SAT, UNKNOWN,
missing records, malformed inputs, and checker failures are not counted
as exclusions. The recorded run has no unresolved cases.

Four disjoint range audits cover all indices in $[0,109676)$. Each audit
regenerated every formula from the public source, compared the SHA256 of
its generated DIMACS bytes with the saved input hash, checked the record's
index, type, weights and gauge, and verified the saved proof hash, size
and acceptance log. The merge rejects
gaps, overlaps, incorrect type coverage, and incomplete digest blocks.
This source/evidence audit does not itself recheck DRAT inferences;
the separate checker invocations provide that part of the proof.

[CERTIFICATES.json](CERTIFICATES.json) identifies all 112 ordered blocks
of inputs and proofs. The original traces occupy 19,782,097,200 bytes;
the maximum conflict count is 84,295, below the per-case
budget of 500,000. The formulas have 125 variables and between
1,075 and 1,125 clauses. Source, commands, actual
checker identities, validation controls and compact evidence are public.
Raw traces are regenerated outside Git. Matching a historical trace hash
is unnecessary for a fresh proof, but every regenerated trace must pass
the checker against its specified input.

The first part of the production corpus used stock DRAT-trim. Later
proofs used the documented two-line allocation configuration in
[CHECKER.md](CHECKER.md). It changes initial capacity and buffer growth,
not proof rules or clause matching. The manifest records how many cases
each binary checked. All traces use the standard binary DRAT format and
can be replayed with the stock checker. This remaining checker trust is
stated explicitly; a hash manifest alone proves no UNSAT assertion.

Thus the assumed 71-point set cannot exist. Every larger line-free set
would contain one of size 71, giving the upper bound 70. The explicit
[known 70-point construction](../known70.json), due to Elsholtz et al.,
is checked against all 775 affine lines. This establishes the matching
lower bound and completes the exact determination.

The ordinary and optimized sanitizer runs agree on the entire finite
reduction, including every affine class. Three known 70-point sets pass
direct incidence and satisfiable-formula controls. The public pipeline
also rejects invalid proofs, altered records, missing cases and a
budget-one UNKNOWN. These checks are detailed in
[VALIDATION.json](VALIDATION.json).

The trust boundary consists of the written reduction, exact integer
certificates, exhaustive ordinary Python/C++ execution, direct CNF
semantics, and DRAT-trim with its documented allocation configuration.
The solver is only a proof-trace generator. This is not a proof-assistant
formalization. Independent acceptance of the earlier upper bound and
of the two-low-plane lemma does not constitute review of this new exact
theorem; its independent review remains pending.

The [independent geometric review](../decision71_geometry_audit/REVIEW.md)
accepts the complete equivalence used in Sections 1–5. It reconstructs
geometry, coordinate maps, profiles and gauge interpolation independently,
and replays the full author enumeration. Its twenty formula comparisons
cover all pair types; they are not a separate export of all 109,676 CNFs.
That review rechecks no global UNSAT proof. The mathematical source and
input family used here are unchanged from its reviewed snapshot.
