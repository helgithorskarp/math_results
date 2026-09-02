# An intrinsic rooted-lens formula for the Ray--West correction

## Result

For a permutation \(\beta\in S_m\), let

\[
g_2(\beta)=|\{\pi\in S_{m+2}:\pi\text{ contains }\beta\}|.
\]

Ray and West proved

\[
g_2(\beta)=
\frac{m^4+2m^3+m^2+4m+4-2j(\beta)}2,
\qquad 0\leq j(\beta)\leq m-1, \tag{1}
\]

but described \(j\) through active insertion synonymities rather than as a
statistic of \(\beta\).  This note gives an intrinsic formula.

A **permutation interval** is a consecutive set of positions whose values are
also consecutive.  For the boundary between positions \(i\) and \(i+1\), let
\(I_i\) be the least permutation interval containing those two positions.  Let
\((\gamma_i,k_i)\) be its standardization, rooted at the corresponding local
boundary.

We next define a family of rooted **lenses**.  Choose

\[
a,c\geq0,\qquad h,w\geq1,\qquad
w\leq\min(a+h,h+c),
\]

and put

\[
n=a+2h+c,\qquad d=h+c-w,\qquad f=a+h-w.
\]

The notation \(x^r\) below means a word of \(r\) copies of \(x\).  Form two
paths of plot points (coordinates are position, value):

* the upper path starts at \((d+2,1)\); its successive value increments are
  \(1^a2^{h-1}\), and its simultaneous position increments are
  \(2^{w-1}1^f\);
* the lower path starts at \((1,a+2)\); its successive value increments are
  \(2^{h-1}1^c\), and its simultaneous position increments are
  \(1^d2^{w-1}\).

The paired words have the same lengths because
\(a+h=w+f\) and \(h+c=d+w\).  Their union has exactly one point in every row
and column of an \(n\)-square, so it defines a permutation
\(\Lambda(a,h,c,w)\).  Root it at boundary \(d+1\).  A rooted lens is this
rooted permutation or its position reversal (rooted at boundary
\(n-d-1\)).

**Theorem (intrinsic lens formula).**  For every \(\beta\in S_m\),

\[
j(\beta)=
\#\{i\in\{1,\ldots,m-1\}:(\gamma_i,k_i)
\text{ is a rooted lens}\}. \tag{2}
\]

Thus (1) can be evaluated using only interval closure inside \(\beta\).  No
permutation of length \(m+2\), insertion grid, synonymity class, or track
matrix needs to be constructed.

For example, the three contributing boundaries of \(14523\) are 2, 3, and
4.  Their least rooted intervals are respectively \((12,1)\),
\((3412,2)\), and \((12,1)\), all lenses.  Boundary 1 has least rooted interval
\((14523,1)\), which is not a lens, so \(j(14523)=3\).

## Proof

We translate Ray--West Proposition 8.5 and Corollary 8.6 into intrinsic
permutation language.  Two elementary details of that translation are
recorded explicitly.

### 1. Same-endpoint track matrices are precisely lenses

Normalize an active pattern-(C) synonymity so its two row multigrids and its
two column multigrids occur in the same order.  In Ray--West's notation, the
same-endpoint case has central block height \(2h\), central block width
\(2w\), and outer heights and widths

\[
(h_1,h_3,w_1,w_3)=(a,c,d,f).
\]

Proposition 8.5 gives the two track types

\[
1^a2^{h-1}:2^{w-1}1^f,
\qquad
2^{h-1}1^c:1^d2^{w-1}. \tag{3}
\]

Equality of the lengths on the two sides of each colon is exactly
\(a+h=w+f\) and \(h+c=d+w\).  Starting the two tracks at the southwest ends
of their respective blocks turns (3) word-for-word into the two paths in the
definition of \(\Lambda\).  Conversely those paths have precisely the two
types in (3).

This can also be checked directly at the insertion level.  Put
\(\lambda=\Lambda(a,h,c,w)\).  The two active triples

\[
\begin{aligned}
 &(21;(1,a+1),(1,d+1)),\\
 &(21;(a+2h+1,n+1),(d+2w+1,n+1))
\end{aligned} \tag{4}
\]

have the same insertion value.  Along each of the two paths, (4) merely
moves the distinguished inserted point from the path's southwest end to its
northeast end.  Every intermediate point is shifted to its neighbor because
of (3), and all other entries are unchanged.  Hence every rooted lens
produces an active pattern-(C) synonymity at its distinguished boundary.

### 2. Passing to the least interval removes terminal padding

For pattern (C), the track matrix is a contiguous permutation submatrix, and
therefore a permutation interval containing the adjacent source boundary.
Besides (3), Proposition 8.5 has two mixed-endpoint cases, transposes of one
another.  In the first, the track types are

\[
1^a2^{h-1}:2^{w-1},
\qquad
2^{h-1}1^c:1^d2^w1^f. \tag{5}
\]

The length constraints in (5) force \(w=a+h\) and
\(c=a+d+f+1\).  Reading the endpoints shows that its track permutation ends
in its maximum: it is \(\xi\oplus1\), with the distinguished boundary inside
\(\xi\).  If \(f>0\), deleting this terminal singleton replaces
\((c,f)\) by \((c-1,f-1)\) in (5).  If \(f=0\), the deletion instead leaves
the same-endpoint words (3), with \(c\) replaced by \(c-1\) and
\(w=a+h\).  Thus repeated deletion reaches (3).  The transpose is
\(\xi^{-1}\oplus1\), so the same argument applies to the other mixed case.

It remains only to check interval minimality inside (3).  The entry just to
the right of the distinguished boundary is 1.  Moreover, before reaching
the entry immediately to its left, the lower track has already passed
through its initial point in position 1.  Consequently every permutation
interval containing the distinguished boundary has value set
\(\{1,\ldots,k\}\) and position set \(\{1,\ldots,k\}\) for some \(k\): it is
a direct-sum prefix.  Equating the numbers of row and column increments used
on the two paths at such a cut in (3) shows that a proper cut after the
distinguished boundary is possible only when
\(a=c=0\) and \(h=w>1\).  (The cuts are then exactly after
\(2,4,\ldots,2h-2\).)  In that exceptional case
\(\Lambda=21\oplus21\oplus\cdots\oplus21\), and the least interval is the
first \(21=\Lambda(0,1,0,1)\).  Otherwise the least interval is the whole
track matrix.  Position reversal gives the identical statement for the
opposite orientation.  Thus the least rooted interval of every active
pattern-(C) configuration is a rooted lens.

### 3. Count the boundaries

Ray--West Corollary 8.6 associates at most one active left-hand pattern-(C)
triple to each adjacent position boundary and defines \(j(\beta)\) as the
number that succeed.  By Sections 1--2, a successful boundary has a least
rooted interval that is a lens.  Conversely, (4) gives a synonymity inside
every lens; if the lens is an interval of a larger permutation, both
insertions shift every exterior point identically, so the synonymity lifts
to the larger permutation.  The successful boundaries are therefore
exactly those counted in (2).  This proves the theorem.  \(\square\)

## Exact verification

The source uses exact Python integers, tuples, and sets, with no external
dependencies, randomness, solver, or floating point.  It was tested with
CPython 3.11.2.

Compute the statistic for one permutation:

```bash
python3 permutation_patterns_intrinsic_g2/intrinsic_g2.py "1 4 5 2 3"
```

Expected output:

```text
beta=(1, 4, 5, 2, 3)
lens_boundaries=(2, 3, 4)
j=3
```

Run the insertion-level exhaustive verifier:

```bash
python3 permutation_patterns_intrinsic_g2/verify_intrinsic_g2.py --max-n 7
```

It checks all 5,913 permutations through length 7.  For every permutation it
independently groups all active two-point insertion triples by their images,
extracts the separated-grid pattern-(C) boundaries, computes \(j\) from the
Ray--West formula, and compares both with the intrinsic statistic.  Expected
final line:

```text
verified 5913 permutations through n=7; intrinsic, separated-grid, and Ray-West j values agree
```

Run the definition-level independent checker:

```bash
python3 permutation_patterns_intrinsic_g2/independent_shadow_check.py --max-n 6
```

This checker does not use insertions, active sites, separated grids, or track
matrices.  It enumerates every permutation of length \(n+2\), standardizes
all its \(n\)-subsequences, obtains \(g_2\) directly from the definition for
all patterns through length 6, and compares the resulting \(j\) with (2).
Expected final line:

```text
definition-level upper-shadow counts agree with intrinsic j through n=6
```

The computation is corroborative.  The universal theorem rests on the
explicit path/insertion argument above and Ray--West's exhaustive
classification of codimension-two synonymity patterns.

## Sources and novelty scope

* N. Ray and J. West, *Posets of matrices, and permutations with forbidden
  subsequences*, Annals of Combinatorics **7** (2003), 55--88.
  <https://eprints.maths.manchester.ac.uk/609/>
* V. Vatter, *An assortment of problems in permutation patterns:
  unimodality, equivalence, derangements, and sorting* (2026), Problem 3.7.
  <https://arxiv.org/abs/2602.16355>

Targeted searches of the primary paper, the 2026 problem collection, their
terminology, and the committed Discovery Net graph found no earlier
intrinsic formula for \(j\).  The novelty assessment is relative to those
searches and is not a historical priority claim.
