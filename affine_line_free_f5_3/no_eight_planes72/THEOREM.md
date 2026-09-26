# Every plane section of a 72-point line-free set has at least nine points

**Exact computer-assisted theorem.** Let \(S\subseteq\mathbb F_5^3\)
have 72 points and contain no complete affine line. Then every affine
plane meets \(S\) in at least nine points.

**Corollary.** Write \(a_m\) for the number of plane sections of size
\(m\). Then \(a_8=0\). Combining this with the newly published
[weighted incidence bound](../nine_plane_frame72/THEOREM.md) gives
\(a_9\ge11\). Only BBB remains in the
previous [global four-case cover](../low_planes72/README.md), where
\(B=(9,15,16,16,16)\). This theorem does not decide the existence of a
72-point set or change the numerical interval \(70\le r_5(\mathbb F_5^3)\le72\).

## 1. Dependencies and reduction to mixed planes

Every line-free subset of an affine plane of order five has at most 16
points. The finite [planar check](../plane_caps.cpp) exhausts all
1,081,575 17-subsets and finds none without a complete line. A larger
line-free subset would contain such a 17-subset. Therefore a section of
\(S\) has size at least \(72-4\cdot16=8\).

We use two previously published results with their own exact certificates:

1. The [two-eight-plane lemma](../two_eight_planes72/THEOREM.md) says
   that \(S\) has at most one eight-point plane. Its 164 lifting proofs
   were checked separately by DRAT-trim.
2. The [global low-plane theorem](../low_planes72/README.md) gives
   \(a_8+a_9\ge5\), and says that these low-plane normals span the
   three-dimensional dual vector space. Its bounds have integer-checkable
   dual certificates. Only the inequality is needed for the new theorem;
   the spanning assertion is used for the BBB corollary.

For the stronger count in the corollary, we also use Team A researcher 1's
[nine-plane-frame theorem](../nine_plane_frame72/THEOREM.md), which proves
\(3a_8+a_9\ge11\) by an integer dual certificate. That independent
advance arrived during this computation. It already makes BBB an exhaustive
normal form, even when an eight-point plane might exist. The new result
here excludes the presence of every eight-point plane; it is stronger than
simply choosing a BBB coordinate description. The weighted bound is needed
only for the consequence \(a_9\ge11\), not for the mixed exclusion.

If an eight-point plane exists, these results supply a nine-point plane.
The two are nonparallel, since parallel ones would give at most
\(8+9+3\cdot16=65\) points in total. We will exclude **every** such
mixed pair. No other structural conjecture about a 72-point set is assumed.

## 2. Normalized projection and necessary bounds

Choose affine coordinates putting the eight-point plane at \(x=0\)
and the nine-point plane at \(y=0\). Project along their intersection
direction, and set

\[
w_{xy}=|\{z:(x,y,z)\in S\}|\in\{0,1,2,3,4\}.
\]

The row profile is \(A=(8,16,16,16,16)\). The four companions of
the nine-point plane have total 63, so their sizes are 15,16,16,16.
Scaling the \(y\) coordinate makes the unique 15-plane have label one.
The column profile is therefore \(B=(9,15,16,16,16)\).

Every quotient affine line has weight at most 16, as its inverse image
is an affine plane. For any affine line meeting \(S\) in \(k\) points,
its six containing planes have total section size \(72+5k\). Thus

\[
72+5w_{00}\le8+9+4\cdot16=81,\qquad w_{00}\le1.
\]

A fiber in either low plane satisfies
\(72+5k\le9+5\cdot16=89\), hence \(k\le3\). All entries in the
zero row or zero column are consequently at most three.

## 3. Complete enumeration by two different parameterizations

Set \(d_{xy}=4-w_{xy}\). Its row and column sums are respectively

\[
R=(12,4,4,4,4),\qquad C=(11,5,4,4,4).
\]

Its total is 28. The interior \(4\times4\) block determines every
remaining entry. If its sum is \(T\), then

\[
\begin{aligned}
d_{x0}&=R_x-\sum_{y=1}^4d_{xy} &&(x>0),\\
d_{0y}&=C_y-\sum_{x=1}^4d_{xy} &&(y>0),\\
d_{00}&=R_0+C_0-28+T=T-5.
\end{aligned}
\]

Since \(d_{00}\in\{3,4\}\), we have \(T\in\{8,9\}\).
Every interior entry lies in \([0,4]\); each interior row or column
sum is at most its corresponding margin minus one. The inferred axis
entries must all lie in \([1,4]\). The upper endpoint needs an explicit
check, especially for the column with deficit margin five.

[deficit_enumeration.cpp](deficit_enumeration.cpp) exhausts these small
integer interior blocks, reconstructs the axes, and checks that each
quotient line has deficit at least four. All vertical lines already
satisfy their prescribed margins. Conversely, every mixed projection
arising from a hypothetical \(S\) appears in this enumeration. It
retains exactly **5,428** distinct weight matrices.

[row_enumeration.cpp](row_enumeration.cpp) uses a different direct
parameterization. It generates the 35 possible rows of weight 16 whose
first entry is at most three, chooses four such rows, and infers the
zero row from the column profile \(B\). It checks the zero-row bounds,
the intersection bound and every remaining quotient line. The two sorted
outputs agree entry by entry, with SHA256

```text
765937a860439729986f457b6cad703d362aa87a71ae6b3cb30631fbe5038792
```

All integer magnitudes in these enumeration loops are at most 80.
There is no numerical tolerance, randomized pruning or solver in this step.

## 4. Complete affine partition and inherited exclusions

Exactly 144 of the 5,428 matrices have two quotient lines of weight eight.
They cannot lift, by the prior two-eight-plane lemma. The remaining
**5,284** matrices have exactly one weight-eight line.

For each remaining matrix, choose its weight-eight line
\(u\cdot p=b\) and any weight-nine line \(v\cdot p=c\).
They are nonparallel. Let \(f\) be the label of the unique 15-line
parallel to the second line. For each \(s\in\mathbb F_5^\times\),
apply the invertible affine map

\[
p\longmapsto\bigl(s(u\cdot p-b),\ (f-c)^{-1}(v\cdot p-c)\bigr). \tag{1}
\]

This gives every affine image with the normalized profiles \(A,B\).
Indeed, the preimages of the zero coordinate lines must be an eight-line
and a nine-line. Their defining affine forms are unique up to scaling,
and the second scaling is forced by the 15-line having label one.

[quotients.py](quotients.py) partitions the 5,284 matrices under (1),
checks disjointness and exact coverage, and obtains **1,252** orbits.
[orbits.json](orbits.json) records the lexicographically least
representatives and multiplicities. A further control explicitly tries
all 12,000 maps in \(\operatorname{AGL}(2,5)\) on representatives of
every occurring pair consisting of the number of nine-lines and orbit size.
These independently filtered affine images agree with (1).

Every affine quotient transformation lifts to an affine transformation of
\(\mathbb F_5^3\). It is therefore enough to exclude lifts of all
1,252 representatives, together with the already excluded 144 matrices.

## 5. The lifting formulas and the three-hole normalization

[model.py](model.py) uses Boolean variables \(X_{xyz}\), numbered
\(1+25x+5y+z\), for point membership. For each representative it requires:

1. None of the 775 affine lines is completely selected.
2. Every one of the 155 affine planes contains at most 16 selected points.
3. Each fiber contains exactly its prescribed number \(w_{xy}\) of points.

These constraints are necessary for a lift. Conversely, a satisfying
assignment directly supplies a line-free set of 72 points with that
projection. Cardinalities use the sequential-counter encoding of the
pinned Python-SAT version; auxiliary variables are existential.

The interior deficit total is at most nine. At least seven of its 16
entries are zero, so at least seven fibers have weight four. They cannot
all lie on a five-point quotient line. Choose the first noncollinear
triple of weight-four fibers in lexicographic order. Each has one missing
height, say \(h_1,h_2,h_3\). A unique affine function \(\ell(x,y)\)
interpolates those heights. The affine shear

\[
(x,y,z)\longmapsto(x,y,z-\ell(x,y))
\]

preserves every fiber weight and sends the three holes to height zero.
We may therefore add three unit clauses excluding those height-zero points.
This is a proved normalization, independent of any solver behavior.

## 6. Checked lifting exclusion and conclusion

CaDiCaL 1.9.5 through Python-SAT 1.9.dev15 returns UNSAT for each of
the 1,252 formulas. Every resulting proof is checked by a separate
DRAT-trim process against the exact generated CNF. Every check exits
successfully and reports `s VERIFIED`. The compact
[certificate manifest](certificates.jsonl) records the input and proof
hashes, proof sizes, normalization triples and checked status for every
case, in the same order as the representatives.

[verify.py](verify.py) regenerates every proof input from the published
source and matches its SHA256 to the checked input. [replay.py](replay.py)
regenerates and independently checks the proofs themselves. A changed CNF,
UNKNOWN, SAT, or failed proof check is an error, not an exclusion.

Thus no normalized mixed projection lifts. Section 1 shows that every
72-point line-free set with an eight-point plane would have such a
projection. This proves that no eight-point plane exists. Since every
plane section has size at least eight, the theorem follows. The global
low-plane theorem gives the BBB corollary. Substituting \(a_8=0\) into
the teammate's weighted inequality gives \(a_9\ge11\).

The trust boundary consists of the written reductions, the cited prior
certificates, the ordinary C++ enumerations, the affine canonicalizer,
the Python-SAT cardinality encoder, and DRAT-trim. UNSAT solver verdicts
alone are not premises. This is not a proof-assistant formalization,
and no independent peer review is claimed.
