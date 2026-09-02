# Exact minimizers of the codimension-two permutation upper shadow

## Result

For a permutation \(\beta\in S_m\), let

\[
g_2(\beta)=|\{\pi\in S_{m+2}:\pi\text{ contains }\beta\}|.
\]

Ray and West proved

\[
g_2(\beta)=
\frac{m^4+2m^3+m^2+4m+4-2j(\beta)}2,
\qquad 0\leq j(\beta)\leq m-1. \tag{1}
\]

A permutation is **layered** if it is a direct sum of decreasing
permutations, and **colayered** if it is a skew sum of increasing
permutations.

**Theorem.** For every \(\beta\in S_m\),

\[
j(\beta)=m-1
\quad\Longleftrightarrow\quad
\beta\text{ is layered or colayered}. \tag{2}
\]

Equivalently, the minimizers of \(g_2\) are exactly

\[
\operatorname{Av}(231,312)\ \cup\ \operatorname{Av}(132,213).
\]

Their number is one for \(m=1\), and \(2^m-2\) for \(m\geq2\).  The
minimum is

\[
\min_{\beta\in S_m}g_2(\beta)
=\frac{m^4+2m^3+m^2+2m+6}{2}. \tag{3}
\]

This proves the converse to the previously established fact that every
layered or colayered permutation attains (3).

## Rooted lenses

We use the intrinsic formula for \(j\) from the companion note
`permutation_patterns_intrinsic_g2`.  For an adjacent position boundary of
\(\beta\), take the least permutation interval containing the two adjacent
positions and standardize it, retaining the local boundary.  The formula
says that \(j(\beta)\) is the number of these least rooted intervals which
are rooted **lenses**.

A base lens \(\Lambda(a,h,c,w)\) has

\[
a,c\geq0,\qquad h,w\geq1,\qquad
w\leq\min(a+h,h+c),
\]

and consists of the two northeast paths

\[
1^a2^{h-1}:2^{w-1}1^{a+h-w},
\qquad
2^{h-1}1^c:1^{h+c-w}2^{w-1}. \tag{4}
\]

Its distinguished boundary is between columns
\(h+c-w+1\) and \(h+c-w+2\).  The entry immediately to the right is 1.
A rooted lens is a base lens or its position reversal; in the reversed
orientation the entry immediately to the left of the root is 1.

We need the following direct consequence of (4).

**Lens cut lemma.**

1. A base lens is a skew sum across its root if and only if \(h=w=1\).
   In that case it is
   \(\iota_{c+1}\ominus\iota_{a+1}\).
2. A reversed base lens is a direct sum across its root if and only if
   \(h=w=1\).  In that case it is
   \(\delta_{a+1}\oplus\delta_{c+1}\).
3. For any fixed unrooted lens permutation, every possible lens root is
   adjacent to its entry 1, so there are at most two possible roots.

Here \(\iota_r=12\cdots r\) and \(\delta_r=r(r-1)\cdots1\).

To prove the first part, write \(d=h+c-w\), so the root follows column
\(d+1\).  The lower path takes its first \(d\) column steps with increment
1.  If \(w>1\), a later point of that increasing path lies to the right of
the root and above a point on the left, which is impossible at a skew-sum
cut.  Thus \(w=1\).  The lower and upper tracks are then separated by the
root.  If \(h>1\), their row sets alternate in the central zone: the lower
track contains row \(a+2\), while the upper track later contains row
\(a+3\).  This is again incompatible with every left value exceeding every
right value.  Hence \(h=1\), and (4) gives the stated two increasing blocks.
The converse is immediate.  Position reversal proves the second part, and
the position of 1 noted above proves the third.

## Proof of the theorem

Say that a permutation has property \(P\) when the least rooted interval at
every adjacent boundary is a lens.  By the intrinsic formula,

\[
P(\beta)\quad\Longleftrightarrow\quad j(\beta)=m-1. \tag{5}
\]

We show that \(P\) forces \(\beta\) to be layered or colayered.
The case \(m=1\) is immediate, so suppose \(m\geq2\).

First suppose that \(\beta\) is sum decomposable.  Write its canonical sum
decomposition

\[
\beta=\alpha_1\oplus\cdots\oplus\alpha_k, \tag{6}
\]

where \(k\geq2\) and every \(\alpha_i\) is sum indecomposable.  At the
boundary between \(\alpha_i\) and \(\alpha_{i+1}\), the least interval is
exactly \(\alpha_i\oplus\alpha_{i+1}\).  Indeed, their union is an interval.
Any smaller interval crossing the boundary has a value range crossing the
sum cut, so it contains the maximum value of \(\alpha_i\) and the minimum
value of \(\alpha_{i+1}\).  Its intersections with the two components would
give a proper terminal sum component of \(\alpha_i\), or a proper initial
sum component of \(\alpha_{i+1}\), contrary to their indecomposability.

If \(P(\beta)\) holds, this two-component interval is a lens rooted at its
direct-sum cut.  The lens cut lemma makes both components decreasing.
Doing this at all \(k-1\) boundaries in (6) makes every \(\alpha_i\)
decreasing.  Hence \(\beta\) is layered.  The symmetric argument for the
canonical skew decomposition says that every skew-decomposable permutation
with property \(P\) is colayered.

It remains to exclude a permutation which is both sum and skew
indecomposable.  The standard substitution decomposition writes it as

\[
\beta=\sigma[\alpha_1,\ldots,\alpha_k], \tag{7}
\]

where \(\sigma\) is simple and \(k\geq4\).  Every permutation interval of
(7) which meets two inflation blocks is the whole of \(\beta\).  Here is a
short verification.  The blocks it meets project to consecutive positions
and consecutive values of \(\sigma\), and therefore to an interval of the
simple permutation \(\sigma\); the projection must be all of \(\sigma\).
The interval consequently contains every position-interior block.  In a
simple permutation of length at least four, neither the minimum nor maximum
entry is first or last, since deleting such an endpoint would leave a
nontrivial interval.  Thus the interval contains the entire minimum-value
and maximum-value blocks.  Its value range is all of \([m]\), so it is all
of \(\beta\).

In particular, the least interval at each of the \(k-1\geq3\) boundaries
between consecutive inflation blocks is \(\beta\) itself.  Property \(P\)
would make the same unrooted permutation \(\beta\) a lens rooted at all
these distinct boundaries.  The lens cut lemma permits roots only on the
two sides of entry 1, a contradiction.  Therefore every permutation with
\(P\) is sum or skew decomposable, and the preceding cases prove that it is
layered or colayered.

Conversely, at a boundary inside a decreasing layer the least rooted
interval is the size-two lens 21.  At a boundary between layers it is
\(\delta_r\oplus\delta_s\), a reversed lens with \(h=w=1\).  Thus every
layered permutation has \(P\); reversal of the argument gives the
colayered case.  This proves (2), and (3) follows from (1).

There are \(2^{m-1}\) compositions of \(m\), giving that many distinct
layered permutations, and the same number of colayered permutations.  For
\(m\geq2\), the two classes intersect only in the increasing and decreasing
permutations.  Indeed, a layered permutation with both a descent inside a
nonfinal layer and a later layer contains 213, whereas a descent inside its
final layer together with an earlier layer gives 132.  A colayered
permutation avoids both patterns.  Thus a permutation in the intersection
is increasing or has a single decreasing layer.  Inclusion-exclusion gives
\(2^m-2\).

## Exact validation

Both scripts use exact standard-library Python only.  They use no solver,
floating point, randomness, or external data.  They were tested with
CPython 3.11.2.

Run the intrinsic census:

```bash
python3 permutation_patterns_g2_minimizers/verify_extremal.py --max-n 9
```

This independently constructs every rooted lens from (4), computes every
least rooted interval, and checks (2) for all 409,113 permutations through
length 9.  It also audits the lens cut lemma through lens size 40.  Expected
final lines:

```text
n=9: checked 362880 permutations; extremals=510
verified 409113 permutations through n=9; exact extremal classification holds
lens cut lemma verified through size 40
```

Run the definition-level upper-shadow census:

```bash
python3 permutation_patterns_g2_minimizers/independent_upper_shadow.py --max-n 7
```

This checker contains no lens, interval-closure, insertion, track-matrix,
or synonymity code.  It enumerates every permutation of length \(m+2\),
deletes every pair of positions, standardizes the remaining word, and
counts \(g_2\) directly.  Expected final lines:

```text
n=7: direct minimum g2=1578; minimizers=126
direct upper-shadow census verified exact minimizers through n=7
```

The computations corroborate the theorem.  The universal claim rests on
the proof above, the intrinsic rooted-lens formula, and the standard
substitution decomposition theorem.

## Sources and novelty scope

- N. Ray and J. West, *Posets of matrices, and permutations with forbidden
  subsequences*, Annals of Combinatorics **7** (2003), 55--88:
  <https://eprints.maths.manchester.ac.uk/609/>
- M. H. Albert, M. D. Atkinson, and M. Klazar, *The enumeration of simple
  permutations*, Journal of Integer Sequences **6** (2003), Article 03.4.4:
  <https://cs.uwaterloo.ca/journals/JIS/VOL6/Albert/albert.html>
- V. Vatter, *An assortment of problems in permutation patterns:
  unimodality, equivalence, derangements, and sorting* (2026), Problem 3.7:
  <https://arxiv.org/abs/2602.16355>

Targeted searches of these primary sources, the terminology around the
Ray--West parameter, and the committed Discovery Net graph found no prior
classification of all equality cases in (1).  This is a search-relative
novelty assessment, not a priority claim.
