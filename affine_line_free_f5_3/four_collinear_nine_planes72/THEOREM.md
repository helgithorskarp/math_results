# Four collinear nine-plane normals in every 72-point candidate

**Theorem.** Let \(S\subseteq\mathbb F_5^3\) have 72 points and contain no
complete affine line. Then at least twelve affine planes meet \(S\) in
exactly nine points. Four of their normal directions lie on one projective
line. After an affine change of coordinates, four nine-point planes are
one of the following two arrangements:

\[
\begin{array}{c|llll}
T&y=0&y=x&y=2x&y=3x+1\\
Q&y=0&y=x&y=2x+1&y=3x+1 .
\end{array}
\]

The coordinate \(z\) is free in these plane equations. In case \(T\), the
first three planes meet in an affine line disjoint from \(S\). In case
\(Q\), no three of the four planes meet in an affine line.

This is a global necessary-condition theorem. It excludes neither case
and does not determine whether a 71- or 72-point line-free set exists.
The interval remains \(70\le r_5(\mathbb F_5^3)\le72\).

## 1. Dependencies

The [global low-plane theorem](../low_planes72/README.md) supplies the
complete 61-equation incidence system used below and excludes five
collinear normal directions of planes with at most nine points.
The [weighted incidence certificate](../nine_plane_frame72/THEOREM.md)
gives \(3a_8+a_9\ge11\), where \(a_m\) counts the \(m\)-point planes.
Team A researcher 2's
[complete eight-plane exclusion](../no_eight_planes72/THEOREM.md) gives
\(a_8=0\). Hence \(a_9\ge11\) before the new argument.

The eight-plane exclusion is an imported computer-assisted theorem:
its mixed-plane lifting proofs and the earlier two-eight-plane proofs
have separate DRAT replay packages. The new certificate here does not
replace or independently re-prove that dependency.

## 2. Pair-of-plane identities

Use the prior nonnegative integer variables \(X_s,P_p,Y_{k,t}\).
Here \(X_s\) counts planes of planar line spectrum
\(s=(m,n_0,\ldots,n_4)\); \(P_p\) counts parallel classes with size
multiset \(p\); and \(Y_{k,t}\) counts \(k\)-point lines whose six containing
planes have size multiset \(t\). Write \(c_m(v)\) for the multiplicity of
\(m\) in a multiset \(v\).

Two different affine planes either belong to one parallel class or
intersect in exactly one affine line. Consequently, for \(m\ne n\),

\[
a_ma_n=
\sum_p c_m(p)c_n(p)P_p+
\sum_{k,t}c_m(t)c_n(t)Y_{k,t},                                      \tag{1}
\]

and, for \(m=n\),

\[
\binom{a_m}{2}=
\sum_p\binom{c_m(p)}2P_p+
\sum_{k,t}\binom{c_m(t)}2Y_{k,t}.                                  \tag{2}
\]

These are 45 additional identities for \(8\le m\le n\le16\).
Every unordered pair of planes is counted once. Equivalently, if the
size-count vector of each parallel class or line pencil is \(t_B\),

\[
\sum_B t_Bt_B^{\mathsf T}=aa^{\mathsf T}+30\operatorname{diag}(a).
\]

The diagonal correction uses the fact that a plane belongs to thirty
line pencils and one parallel class.

Suppose \(a_9=11\). Append \(a_8=0\), \(a_9=11\), and the nine identities
(1)–(2) involving size nine to the prior 61 equations. For \(m\ne9\)
their right sides are \(11a_m\), so the enlarged system is linear.
Call it \(Nu=b\); it has 72 equations and the original 463 columns.
Its last nine rows have right side zero except for the \(9,9\) row,
whose right side is 55.

[certificate.json](certificate.json) contains 72 integer multipliers
\(z\), with the row names. Exact integer multiplication gives

\[
N^{\mathsf T}z\ge0,\qquad b^{\mathsf T}z=-181596<0.                  \tag{3}
\]

For \(u\ge0\), (3) contradicts
\(0\le u^{\mathsf T}N^{\mathsf T}z=b^{\mathsf T}z\).
Thus \(a_9\ne11\), and the imported \(a_9\ge11\) proves
\(\boxed{a_9\ge12}\).

Floating-point optimization only discovered the certificate. The
multipliers were rounded to integers and their column slacks repaired
using the three counting rows. All 463 final inequalities and the negative
right side are checked exactly; no optimizer verdict or tolerance enters
the proof.

## 3. Twelve projective points force four collinear points

Here is an elementary fact about \(\operatorname{PG}(2,5)\).
Suppose a twelve-point set \(R\) has at most three points on every line.
At a point of \(R\), its eleven other points lie on six lines, with at
most two on each. The only distribution is \(2,2,2,2,2,1\).
Thus every point of \(R\) lies on exactly one 2-secant and five 3-secants.
There are six 2-secants and no 1-secants. No two 2-secants meet in \(R\).

At an outside point, let \(r_i\) count the incident lines meeting \(R\)
in \(i\) points. Then

\[
r_0+r_2+r_3=6,\qquad 2r_2+3r_3=12.
\]

It follows that \(r_2\in\{0,3,6\}\), so
\(\binom{r_2}{2}\ge r_2\).
All pairwise intersections of the six 2-secants lie outside \(R\).
Counting their pairs and their incidences with outside points gives

\[
15=\binom62=\sum_{P\notin R}\binom{r_2(P)}2
\ \ge\ \sum_{P\notin R}r_2(P)=6\cdot4=24,
\]

a contradiction. Any larger set contains a twelve-point subset, so it
also has four collinear points.

Two nine-point planes of \(S\) cannot be parallel: such a parallel class
would contain at most \(9+9+3\cdot16=66\) points. Their normals are
therefore distinct projective points. Applying the preceding fact to
twelve of them proves the required four collinear normals. The imported
five-normal exclusion says there are exactly four nine-plane normals on
this particular projective line.

## 4. Two complete affine arrangement types

The projective line of normals is the annihilator of a one-dimensional
direction \(d\). Project along \(d\) to \(\operatorname{AG}(2,5)\).
The four nine-point planes become four lines with distinct directions.
Any four directions can be sent to slopes \(0,1,2,3\): the two omitted
directions can be sent to the vertical direction and slope four, since
an invertible linear map acts transitively on ordered pairs of different
projective directions.

Write the four lines as \(y=ax+b_a\), \(a=0,1,2,3\).
A translation makes \(b_0=b_1=0\). The four cannot be concurrent.
Otherwise their inverse images share a line \(\ell\), and its pencil gives

\[
72+5|S\cap\ell|
\le4\cdot9+2\cdot16=68,
\]

which is impossible. Hence \((b_2,b_3)\ne(0,0)\).
A common nonzero dilation of both coordinates reduces this pair to
\((0,1)\) or \((1,t)\), \(t=0,1,2,3,4\).

The following invertible affine maps send these six possibilities to
the two displayed representatives. All entries are in \(\mathbb F_5\).
The map is \((x,y)\mapsto(ax+by+t_x,cx+dy+t_y)\).

| \((b_2,b_3)\) | \((a,b,c,d,t_x,t_y)\) | Target |
|---|---|---|
| \((0,1)\) | \((1,0,0,1,0,0)\) | \(T\) |
| \((1,0)\) | \((1,1,1,4,0,0)\) | \(T\) |
| \((1,1)\) | \((1,0,0,1,0,0)\) | \(Q\) |
| \((1,2)\) | \((1,1,3,4,2,2)\) | \(T\) |
| \((1,3)\) | \((1,1,1,4,0,0)\) | \(Q\) |
| \((1,4)\) | \((3,3,1,2,4,3)\) | \(T\) |

This explicit table proves the cover. As a separate audit the checker
constructs all invertible two-dimensional linear maps and all translations.
With these four directions fixed, the 625 possible offset tuples split
into 25 fourfold-concurrent arrangements, 400 images of \(T\), and
200 images of \(Q\), with no omissions or overlaps.
Every quotient affine map lifts to an affine map of the original space.
The two quotient types need not be disjoint descriptions of a full
three-dimensional candidate, which may admit several choices of four planes.

In case \(T\), the first three planes share a line \(\ell\).
The pencil bound is
\(72+5|S\cap\ell|\le3\cdot9+3\cdot16=75\).
Its integer intersection size is therefore zero.

## 5. What this reduction does and does not close

In the resulting quotient put
\(w(x,y)=|\{z:(x,y,z)\in S\}|\).
These are integers between zero and four, with total 72.
The four distinguished lines have weight nine. Their parallel classes
each have profile \((9,15,16,16,16)\), with no prescribed ordering of
the companion labels. Every other quotient line has weight between ten
and sixteen: another nine-line would either violate the parallel total
or give five collinear nine-plane normals. The eight-plane exclusion
has already removed weights below nine.

Thus every candidate has some direction whose quotient contains four
distinct \(B\) profiles. This is an additional global filter on the
remaining two-nine-plane lifting families: it suffices to retain a
family covering quotients with four such profiles. The theorem asserts
the existence of this direction; other directions of the same candidate
may have fewer than four \(B\) profiles.

Two exact controls delimit the method.

* [incidence_control.json](incidence_control.json) is a nonnegative integer
  solution of all 61 old equations and all 45 identities (1)–(2), with
  \((a_8,\ldots,a_{16})=(0,16,0,0,14,8,12,32,73)\).
  It shows that these aggregate equations alone cannot exclude 72.
  The counts do not constitute a geometrically realizable point set.
* [quotient_controls.json](quotient_controls.json) supplies one integer
  weight assignment of total 72 for each of \(T,Q\), satisfying every
  stated quotient line bound and all four \(B\) profiles. Neither
  arrangement can be excluded solely by these quotient conditions.
  These weights do not specify a lift to 125 point variables.

The next step must use simultaneous compatibility of actual plane
sections or certified lifting exclusions. The new count and two-type
cover are global reductions; the controls do not establish existence.

There is also an immediate combination with Team A researcher 3's
concurrently published [quadratic moment theorem](../quadratic_moments72/THEOREM.md).
For the centered finite-field second-moment matrix \(M\), that theorem
gives three congruence types. Intersecting its bounds with \(a_9\ge12\)
leaves:

| Moment form | Consequence |
|---|---|
| \(\operatorname{diag}(1,0,0)\) | \(12\le a_9\le16\) |
| \(\operatorname{diag}(1,2,0)\) | \(a_9=12\), three radical pencils with occupancies \((4,4,4)\) |
| \(\operatorname{diag}(1,1,1)\) | \(a_9=12\), normals corresponding to \(K_6\) minus a perfect matching |

Thus its three other omitted-edge patterns, all belonging to \(a_9=11\),
are eliminated. This corollary uses the teammate's moment and normal-locus
theorem as an additional premise; the plane-pair certificate and
two-arrangement theorem above do not require it. A diagonal moment gauge
and either displayed affine arrangement cannot be imposed simultaneously
without a further change-of-coordinates argument.

## 6. Reproduction and trust boundary

Run the command in [README.md](README.md). The checker re-enumerates
all \(2^{25}\) planar subsets, regenerates the incidence matrix, checks
(3), verifies all 45 identities for the integer control, and audits
every one of the 11,935 affine plane pairs. It also checks the explicit
six-map table, the full affine arrangement cover, both quotient controls,
the known 70-point construction, and rejection of damaged certificates.

The proof trusts the written arguments, ordinary finite-geometry and
integer programs, and the cited previous structural theorems.
It is not a proof-assistant formalization or independent peer review.
