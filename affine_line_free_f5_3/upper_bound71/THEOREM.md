# No 72-point line-free subset of AG(3,5)

**Exact computer-assisted theorem.** A subset of \(\mathbb F_5^3\)
containing no complete affine line has at most 71 points. Consequently

\[
70\le r_5(\mathbb F_5^3)\le71.
\]

The existence of a 71-point set remains unresolved in this work. No exact
value is claimed. The proof is not a proof-assistant formalization and
independent peer review is pending.

The proof excludes every 72-point candidate by a complete finite cover.
It uses the earlier exact low-plane counting certificate, two different
enumerations of quotient weights, a complete affine partition, and 4,332
independently checked UNSAT proofs. Each formula has only the 125 point
variables, with explicit cardinality clauses. The earlier AA and AB SAT
lemmas, the weighted nine-plane-frame theorem, and the previous upper
bound 72 are not premises of this consolidated exclusion.

## 1. The low-plane counting input

An affine plane of order five has 25 points. The existing
[planar enumeration](../plane_caps.cpp) visits all 1,081,575 17-subsets
and finds that each contains a complete five-point line. Therefore every
line-free plane section has size at most 16.

Suppose for contradiction that \(|S|=72\) and \(S\) is line-free.
The four parallel companions of any plane contain at most 64 points,
so every plane section has size between eight and 16.

We use just the following consequence of the
[global low-plane counting theorem](../low_planes72/README.md):

\[
a_8+a_9\ge5, \tag{1}
\]

where \(a_m\) counts affine plane sections of size \(m\). That
package defines a nonnegative incidence vector \(u\), an integer
61-by-463 matrix \(M\), and \(Mu=b\), with columns for allowed plane
spectra, parallel-class size profiles and six-plane pencils. Its complete
planar enumeration supplies all 70 allowed section spectra. If \(q\)
selects planes of size at most nine, its exact certificate gives integer
\(z\) and positive \(D\) with

\[
M^Tz\le Dq,\qquad b^Tz/D=88133/20000>4.
\]

Multiplying by \(u\ge0\) proves \(a_8+a_9>4\), hence (1).
The definition of the incidence system, proof that every actual set
produces such a vector, integer multipliers, complete enumeration and
column-by-column verification are in the cited package. Our verifier
replays that exact certificate. No floating-point optimization or
sufficiency assertion about the incidence system is used.

Choose two planes of sizes eight or nine. They cannot be parallel:
two such sections and the other three parallel sections would contain
at most \(18+3\cdot16=66<72\) points. We only need two low planes;
no independent triple of normals or prescribed section shape is assumed.

## 2. All three normalized pair profiles

Put the selected planes at \(x=0\) and \(y=0\), and project along
their intersection direction. Define

\[
w_{xy}=|\{z:(x,y,z)\in S\}|,\qquad 0\le w_{xy}\le4.
\]

Their total is 72. Every affine line of the quotient plane has weight
at most 16, since its inverse image is an affine plane of the original
space. If a zero plane has size eight, its four companions must all
have size 16. If it has size nine, the companions have sizes 15,16,16,16.
Multiply that coordinate by the inverse of the label of its unique
15-plane to put this companion at label one. Exchanging the two
coordinates if needed leaves the three ordered profile pairs

| Type | Row profile | Column profile |
|---|---|---|
| 0: AA | \(A=(8,16,16,16,16)\) | \(A\) |
| 1: AB | \(A\) | \(B=(9,15,16,16,16)\) |
| 2: BB | \(B\) | \(B\) |

All changes here are affine transformations over \(\mathbb F_5\).
Arbitrary permutations of the five coordinate labels are not allowed.

For a line meeting \(S\) in \(k\) points, its six containing planes
have total section size \(72+5k\). The line points are counted six
times and all other points once. Applying this identity to a fiber in
a selected low plane gives \(72+5k\le9+5\cdot16=89\), so every
zero-axis weight is at most three. For the intersection fiber it gives

\[
w_{00}\le\left\lfloor\frac{m_1+m_2+64-72}{5}\right\rfloor
=\begin{cases}1&\text{AA or AB},\\2&\text{BB}.\end{cases} \tag{2}
\]

## 3. Complete enumeration of 16,192 typed quotients

Set \(d_{xy}=4-w_{xy}\). Its total is 28; its margins are chosen
from \(A'=(12,4,4,4,4)\) and \(B'=(11,5,4,4,4)\).
Let \(R,C\) be the chosen deficit margins and let \(T\) be the
sum of the interior \(4\times4\) block. Its remaining entries are
forced:

\[
d_{x0}=R_x-\sum_{y=1}^4d_{xy},\quad
d_{0y}=C_y-\sum_{x=1}^4d_{xy},\quad
d_{00}=R_0+C_0-28+T. \tag{3}
\]

Every interior entry is an integer in \([0,4]\). The omitted axis
entries lie in \([1,4]\), so interior row and column sums are at most
their margins minus one. Both endpoints of the inferred axis bounds
must be checked. Equation (2) implies these complete interior-total ranges:

| Type | \(d_{00}\) | \(T\) |
|---|---|---|
| AA | \(T-4\in\{3,4\}\) | 7 or 8 |
| AB | \(T-5\in\{3,4\}\) | 8 or 9 |
| BB | \(T-6\in\{2,3,4\}\) | 8, 9 or 10 |

[deficit_enumeration.cpp](deficit_enumeration.cpp) exhausts these interior
blocks, reconstructs (3), and checks that every remaining quotient line
has deficit at least four. It therefore includes every projection of a
72-point candidate with the selected pair of low planes.

[row_enumeration.cpp](row_enumeration.cpp) independently enumerates
weights directly. It generates all rows of size 15 or 16 whose first
entry is at most three, chooses rows 1 through 4 with their prescribed
sizes, and infers row zero from the column margins. It checks all boundary
and line inequalities. This parameterization has no interior-deficit sum.

The two sorted typed outputs agree entry by entry:

| Type | Labeled weight matrices |
|---|---:|
| AA | 4,442 |
| AB | 5,428 |
| BB | 6,322 |
| Total | 16,192 |

The output format is `type`, one space, 25 weight digits in row-major
order, then a newline. Its SHA256 is

```text
7ad44f1b9e1244da30d0ac28d29eb9f84e441323285b62cd21454827579fcb7f
```

Enumeration arithmetic uses small integers, with all sums at most 80.
There is no randomized pruning or solver in these enumerations.

## 4. Complete affine quotient across all three types

For a retained matrix, choose an ordered pair of nonparallel low quotient
lines \(u\cdot p=b\), \(v\cdot p=c\), putting the smaller size
first. Apply

\[
p\longmapsto\bigl(s(u\cdot p-b),t(v\cdot p-c)\bigr). \tag{4}
\]

For an eight-line the corresponding scale runs through all four nonzero
field elements. For a nine-line, if its unique parallel 15-line has label
\(f\), the corresponding scale is forced to be \((f-b)^{-1}\)
(or \((f-c)^{-1}\) for the second coordinate).

These are precisely all affine images lying in the normalized typed
catalogue. For the converse, the preimages of the two zero coordinate
lines must be the selected low lines. Their affine forms are unique up
to scale, and a nine-line's scale is determined by the companion label.
Thus (4) misses no affine equivalence between normalized matrices.

[quotients.py](quotients.py) partitions the entire typed catalogue into
disjoint orbits, checking coverage entry by entry. It chooses the least
pair `(type, word)` in each orbit; types are ordered AA, AB, BB. There
are **4,332** representatives, classified by their least type as
164 AA, 1,252 AB and 2,916 BB. An orbit may contain normalized matrices
of more than one type. No type or matrix is discarded using the earlier
SAT lemmas. [orbits.json](orbits.json) records the complete representatives
and multiplicities.

An affine quotient map lifts to an affine map of \(\mathbb F_5^3\).
It is therefore enough to exclude lifts of all these representatives.
A symmetry of a quotient matrix is not imposed as a symmetry of its lift.

## 5. A direct formula with only 125 variables

Use variable \(X_{xyz}\), numbered \(1+25x+5y+z\), for membership
of each point. For every one of the 775 affine lines, include the clause
forbidding selection of all its points.

For a five-point fiber \(F\) of prescribed weight \(n\), include:

* \(\bigvee_{v\in U}\neg X_v\) for every \((n+1)\)-subset
  \(U\subseteq F\);
* \(\bigvee_{v\in V}X_v\) for every \((6-n)\)-subset
  \(V\subseteq F\).

The first family says at most \(n\) points are selected; the second
says at most \(5-n\) are absent. When \(n=0\), the second family
is empty, as required. These elementary clauses express exactly the
fiber cardinality, with no auxiliary variables or cardinality encoder.
The prescribed fiber weights already sum to 72. No plane-cardinality
clauses are added to this direct formula.

Finally, add a proved normalization. The interior deficit sum is at
most ten, so at least six of its 16 entries vanish. Their fibers have
weight four and a unique missing height. Six quotient points cannot all
lie on a five-point line. Choose the first noncollinear triple of
weight-four fibers. A unique affine function \(\ell(x,y)\) interpolates
their three missing heights. The affine shear

\[
(x,y,z)\longmapsto(x,y,z-\ell(x,y))
\]

preserves every fiber weight and puts all three holes at height zero.
The formula may therefore require those three points to be absent.

[model.py](model.py) generates exactly these clauses. Every hypothetical
candidate gives a satisfying assignment for one representative after
the two affine normalizations. Conversely, every model directly yields
a 72-point line-free set. This proves the required equivalence between
the mathematical question and the finite disjunction of formulas.

## 6. Checked exclusion and the numerical consequence

CaDiCaL 1.9.5 through Python-SAT 1.9.dev15 produces UNSAT proofs for
all **4,332** formulas. A separate DRAT-trim process checks every trace
against its exact generated CNF, requiring exit status zero and
`s VERIFIED`. The [compact manifest](certificates.csv) records the input
hash, proof hash and proof size of every checked case, in representative
order. Bulk proof traces are omitted from Git and can be regenerated.

[verify.py](verify.py) re-enumerates both catalogues, checks their exact
affine partition, compares selected-low-line normalization with all
12,000 affine maps on structural sample classes, independently generates
the affine lines from point pairs, checks the fiber clauses on all 160
cardinality/assignment combinations, regenerates every proof-input hash,
and replays the exact low-plane counting dependency. [replay.py](replay.py)
regenerates and independently checks all 4,332 proofs. UNKNOWN, SAT,
a changed input or a failed checker is never counted as an exclusion.

Every normalized representative is thus excluded. Sections 1–5 show
that any 72-point line-free set would supply one of those representatives
and a satisfying lift, a contradiction. Any larger line-free set would
contain a line-free 72-subset. Hence the global maximum is at most 71.
The known [70-point construction](../known70.json), directly checked by
the verifier, supplies the lower bound. A second existing 70-point
construction from [the teammate symmetry work](../odd_symmetry/README.md)
is an additional encoding control, not a new lower bound.

The trust boundary includes the written reduction, the cited exact
counting certificate and its planar enumeration, the two ordinary C++
quotient enumerations, affine canonicalization, the small direct CNF
generator, and DRAT-trim. The SAT solver's verdict alone is not a premise.
The lifting formulas do not rely on a cardinality-encoding library,
floating-point calculations, an external classification, or the earlier
AA/AB proof traces. This is author-certified computer-assisted evidence;
it does not claim independent peer review or formal verification.
