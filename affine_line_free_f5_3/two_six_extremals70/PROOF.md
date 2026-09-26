# Extremal constructions and a seven-plane intersection obstruction

All coordinates are over \(\mathbb F_5\). Cardinalities and deficits are
ordinary integers. A set is line-free if it contains no complete
five-point affine line.

## 1. Statements

Let \(C_1,C_2,C_3\) be the three explicit 70-point sets in
`seeds.json`, named `paper`, `order_three`, and `reflected`.

**Classification theorem.** A line-free 70-point set with at least two
six-point plane sections is affinely equivalent to exactly one of
\(C_1,C_2,C_3\).

Each \(C_i\) is inclusion-maximal and has coordinate sum zero. Therefore
the same holds for every set covered by the classification. Zero sum is
affine-invariant at cardinality 70, since
\(\sum(Ax+t)=A\sum x+70t=A\sum x\).
The three affine classes are distinct: their numbers of six-point
planes are respectively 5, 7, and 4.

**71-point corollary.** For any line-free \(S\) of size 71, its
seven-point plane sections are pairwise disjoint as subsets of \(S\).
Put \(f=\#\{H:|S\cap H|=7\}\), \(\mu=\sum_{x\in S}x\), and
\(\epsilon=1_{\{\mu\in S\}}\). Then
\[
 \boxed{f+3\epsilon\le4.}
\]

No affine symmetry of a hypothetical unknown set is assumed.
The classification covers the stated two-plane family, not all 70-point
sets. The corollary does not settle existence at cardinality 71.

## 2. Normalize two six-point planes

The planar bound is \(r_5(\mathbb F_5^2)=16\). For completeness,
`planar_cap.cpp` tests all \(\binom{25}{17}=1,081,575\)
17-subsets against the 30 planar lines and finds none line-free.
A 70-point line-free set therefore has every plane section between
6 and 16.

Two six-point planes cannot be parallel: their parallel class would
contain at most \(6+6+3\cdot16=60\) points. Choose affine coordinates
so they are \(x=0\) and \(y=0\). Project along their common direction,
and define
\[
 w_{xy}=|\{z:(x,y,z)\in S\}|.
\]
Every \(w_{xy}\) is between zero and four. The row and column sums
are both \((6,16,16,16,16)\). Every quotient line has total weight at
most sixteen.

For any line \(\ell\) with \(k=|S\cap\ell|\), its six incident planes
satisfy
\[
 \sum_{H\supset\ell}|S\cap H|=70+5k. \tag{1}
\]
If \(\ell\) is in a six-point plane, \(70+5k\le6+5\cdot16=86\),
so \(k\le3\). If it is the intersection of the two chosen planes,
\(70+5k\le6+6+4\cdot16=76\), so \(k\le1\).
Thus axis fibers have weight at most three and \(w_{00}\le1\).

Write \(d_{xy}=4-w_{xy}\). Their total is 30, their row and column
totals are both \((14,4,4,4,4)\), and their interior total is
\[
 U=\sum_{x,y\ne0}d_{xy}=30-14-14+d_{00}=2+d_{00}\in\{5,6\}.
\]
Conversely the sixteen interior entries determine the boundary:
\[
 d_{x0}=4-\sum_{y\ne0}d_{xy},\quad
 d_{0y}=4-\sum_{x\ne0}d_{xy},\quad d_{00}=U-2.
\]
Axis bounds require \(1\le d_{x0},d_{0y}\le4\).
Every quotient line must have deficit at least four.

## 3. Complete quotient domain and its affine classes

`deficit_quotients.cpp` enumerates every nonnegative interior
array with total five or six, enforcing the row and column boundary
bounds, reconstructs the boundary, and tests every quotient line.
Its recursion covers every allowed interior entry exactly once.

The independent `row_quotients.cpp` instead enumerates complete
weight rows: each of rows 1 through 4 has sum sixteen, first entry
at most three, and other entries at most four. Column sums determine
row zero, after which it checks all bounds and all lines. It does not
use the interior-deficit parameterization.

The two sorted catalogues agree entry by entry on **7,464** words.
The byte encoding is one 25-digit row-major weight word per line,
sorted lexicographically, with a trailing newline:

`4659cde5bfafcaec4bfb5b7deec5762fdbcc5d5010f62a87b2952b1848ef1d6c`.

To classify this normalized domain, choose any ordered pair of
nonparallel quotient lines of weight six, send them to the coordinate
axes, and independently scale the two normal coordinates by a nonzero
field element. These are exactly the affine changes that send a word
to another word in the normalized domain. Their images partition the
catalogue into **262** classes, choosing the lexicographically least
word in each.

The separate `full_affine.cpp` audit applies all 12,000 affine
maps of \(\mathbb F_5^2\) to every representative. Images belonging
to the normalized domain must have a unique owner. It verifies all
3,144,000 maps, disjoint coverage of all 7,464 words, the canonical
representatives, and every orbit size. This audit does not use the
two-low-line normalization algorithm.

## 4. Normalize heights without imposing symmetry

At most six of the sixteen interior deficits are nonzero. Hence at
least ten quotient positions have weight four. They cannot all lie
on one five-point line, so a noncollinear triple exists.

Choose the first such triple lexicographically. Each full fiber omits
one height. A unique affine-linear function of \((x,y)\) interpolates
these three missing heights. Subtracting this function from \(z\)
is an invertible affine coordinate change and makes all three holes
occur at height zero. This is the three-hole gauge.

It loses no equivalence class of sets, and it does not assert that
the set has an automorphism. Vertical scaling remains free; different
normalized objects related by it are deliberately retained.

## 5. Exact lifting formulas and the 48 positive objects

The formula has exactly 125 Boolean variables \(X_p\), one per affine
point. For every one of the 775 affine lines it includes
\(\bigvee_{p\in\ell}\neg X_p\). Every five-point vertical fiber of
weight \(w\) has all negative clauses on its \((w+1)\)-subsets
and all positive clauses on its \((6-w)\)-subsets. These impose
exactly \(w\) selected points. Empty families of subsets contribute
no clauses. Three negative unit clauses impose the height gauge.

Thus satisfying assignments correspond exactly to gauged line-free
lifts of that quotient. The verifier checks all 160 truth assignments
of the five possible fiber weights. Total cardinality is automatically
70, because the quotient weights sum to 70.

Exactly seven quotient classes have lifts:

| Row-major quotient word | Gauged lifts |
|---|---:|
| 0022204444242442442424442 | 4 |
| 0022204444242442443324433 | 4 |
| 0022204444244422442424244 | 16 |
| 0022214344244332443314344 | 8 |
| 0122114344233442443314434 | 4 |
| 0122114344234342434314434 | 8 |
| 0122114344234432442414344 | 4 |
| **Total** | **48** |

Every object is explicitly listed in `models.json`. For every
point list the verifier independently constructs affine lines from
all pairs of points, checks all 775 lines, the quotient, the gauge,
the coordinate sum, and every possible one-point extension.
Each object also supplies an invertible \(3\times3\) matrix and a
translation that carry one of the three named seeds onto it.
Applying these certificates verifies affine equivalence directly.
No inference from equal spectra is used.

For completeness, for each supplied 70-set \(T\) in its quotient
formula append \(\bigvee_{p\in T}\neg X_p\). Since every lift has
size 70, this excludes precisely \(T\). An independent DRAT-trim
process checks an UNSAT proof of the resulting formula in **each of
the 262 classes**. In the 255 empty classes there are no added
blocking clauses. In the seven positive classes the checked proof
excludes every unlisted object.

All positive objects plus all 262 checked exclusions establish the
classification. The seeds' distinct six-plane counts establish exactly
three affine types in this family. Direct point checks establish zero
sum and maximality. The three seeds have at least two six-point planes,
so all three types actually occur in the classified family.

## 6. Consequences at 71

Every plane section of a line-free 71-set has size 7 through 16.
If two seven-point planes had a common selected point \(p\), deletion
of \(p\) would produce a 70-set with two six-point planes. The
classification makes that set inclusion-maximal, contradicting its
extension by \(p\). Therefore the seven-point sections are pairwise
disjoint on the selected set.

Every seven-point plane \(v\cdot x=t_0\) contains
\(\mu=\sum_{x\in S}x\). Its parallel profile is
\((7,16,16,16,16)\), and
\[
 v\cdot\mu=16\sum_{t\in\mathbb F_5}t+(7-16)t_0=t_0
 \quad\text{in }\mathbb F_5.
\]
Consequently \(\mu\in S\) permits at most one seven-point plane.

The normal directions of the seven-point planes form an arc: if
three normals were collinear, their planes, all through \(\mu\),
would share a line \(\ell\). The pencil identity would give
\(71+5|S\cap\ell|\le3\cdot7+3\cdot16=69\), impossible.
In particular, the intersections with the other seven-point planes
are distinct lines through \(\mu\) in any fixed one of them.

If there are at least two seven-point planes, \(\mu\notin S\).
Fix one of these planes. Its \(f-1\) intersection lines contain
no selected point, by pairwise disjointness. Of the six lines in
the plane through \(\mu\), at most \(7-f\) remain available for
its seven selected points. A line in a seven-point plane has at
most three selected points, since the pencil identity gives
\(71+5k\le7+5\cdot16=87\).
Thus
\[
 7\le3(7-f),\qquad f\le4.
\]
Together with \(f\le1\) when \(\mu\in S\), this proves
\(f+3\epsilon\le4\). This proof needs neither the conic argument
nor the quartic enumeration from the earlier moment theorem.

There is also a useful construction target. Exactly \(71-7f\)
deletions avoid all seven-point sections, because these sections are
pairwise disjoint. They produce 70-sets with every plane section at
least seven. Deleting \(p\) gives coordinate sum \(\mu-p\), which
vanishes only for \(p=\mu\). If \(f\ge1\), that point belongs to the
seven-point planes and is already excluded from these deletions.
Thus the number of nonzero-sum deletions with no six-point plane is
\[
 71-7f-\epsilon\,1_{\{f=0\}}\ge43.
\]
These 70-sets are distinct. Conversely, the classification shows that
any nonzero-sum 70-set can have at most one six-point plane.
Neither statement asserts that such a 70-set actually exists.

## 7. Evidence boundary

This is an exact computer-assisted classification with a written
reduction. Integer counts are at most 3,144,000 in the group audit;
the enumerators use 64-bit counters, entries between zero and four,
and small bounded integer sums. Planar bit masks use 25 of 32 bits.
No floating-point optimization or heuristic search verdict enters
the proof.

The trust boundary is the mathematical reduction, the complete
enumerators and orbit audit, the formula encoding, the compiler,
and DRAT-trim. CaDiCaL supplies proof traces; its UNSAT verdict alone
is not a premise. Positive-model and affine-map checks are ordinary
exact programs. Sanitizers and independent algorithms reduce
implementation risk but do not make this a formalized proof.

The exploratory large-exchange and adaptive-penalty searches that
preceded this census found no new witness. They are not premises
and are not included as mathematical evidence.
