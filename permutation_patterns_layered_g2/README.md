# Layered patterns minimize the codimension-two upper shadow

## Result

Write \(\operatorname{st}(w)\) for the standardization of a word with
distinct entries.  For \(\beta\in S_m\), let

\[
g_2(\beta)=\left|\{\pi\in S_{m+2}:\pi\text{ contains }\beta\}\right|.
\]

Ray and West proved that

\[
g_2(\beta)=\frac{m^4+2m^3+m^2+4m+4-2j(\beta)}2,
\qquad 0\leq j(\beta)\leq m-1. \tag{1}
\]

They did not give an intrinsic formula for \(j\).  Vatter recently restated
finding such a formula as an open problem.

This note gives a structural partial answer.

**Theorem.**  If \(\beta\) is layered or colayered, then

\[
j(\beta)=m-1
\quad\text{and}\quad
g_2(\beta)=\frac{m^4+2m^3+m^2+2m+6}{2}. \tag{2}
\]

Consequently every layered and colayered \(m\)-permutation minimizes
\(g_2\) among all \(m\)-permutations.

Here a layered permutation is

\[
\delta_{a_1}\oplus\cdots\oplus\delta_{a_k},
\qquad \delta_s=s(s-1)\cdots1,
\]

for a composition \((a_1,\ldots,a_k)\) of \(m\).  A colayered permutation
is the complement of a layered permutation (equivalently, a skew sum of
increasing permutations).

The result is only a partial answer to Vatter's problem.  It does not give
\(j(\beta)\) for an arbitrary permutation.

## Proof

We use Ray and West's insertion notation.  A two-point insertion triple is
written

\[
(\rho;R,C),
\]

where \(\rho\in S_2\), and \(R,C\) are nondecreasing two-element
multisets of grid sites in \([m+1]\).  Their Corollary 8.6 and Theorem 8.7
have the following consequence:

- \(j(\beta)\) is the number of active left-hand triples arising from
  synonymities of pattern (C) and its dihedral translates;
- at most one such triple arises from each of the \(m-1\) adjacent column
  pairs of \(\beta\).

It therefore suffices to exhibit a distinct active pattern-(C) synonymity
for every boundary between positions \(q\) and \(q+1\).

### Boundaries inside a layer

Suppose the boundary is internal to a decreasing layer.  Then for some
\(v\),

\[
\beta(q)=v+1,\qquad \beta(q+1)=v.
\]

The two triples

\[
(21;(v,v),(q,q))
\quad\text{and}\quad
(21;(v+2,v+2),(q+2,q+2)) \tag{3}
\]

are synonymous.  Indeed, both insertions replace the interval \(21\) by
\(2143\), with the same shifts outside that interval.  The first triple is
left-hand because \((v,v)<(v+2,v+2)\) lexicographically.  Its only
insertion site is \((v,q)\); this is active because the unique point in row
\(v\) lies in column \(q+1\), whereas a site \((r,c)\) is inactive only
when row \(r\) has its point in column \(c-1\) or \(c\).  The row and
column multigrids in (3) are separated, so this is pattern (C), including
its allowed degeneracies.

### Boundaries between two layers

Now suppose the boundary separates consecutive layers.  Let the preceding
layer occupy positions and values \(p+1,\ldots,q\), and let the next layer
occupy positions and values \(q+1,\ldots,r\).  Put

\[
R=(p+1,q),\qquad C=(q+2,r+1).
\]

Then

\[
(12;R,C)
\quad\text{and}\quad
(12;C,R) \tag{4}
\]

are synonymous.  The first triple is left-hand, and its two insertion sites
are \((p+1,q+2)\) and \((q,r+1)\).  Row \(p+1\) has its point in column
\(q\), while row \(q\) has its point in column \(p+1\), so both sites are
active.  Also \(\max R=q<q+2=\min C\); thus (4) has the separated row and
oppositely separated column multigrids of a dihedral translate of pattern
(C).

For completeness, synonymity in (4) can be checked locally.  Put
\(a=q-p\) and \(b=r-q\), discard the common offset \(p\), and ignore the
unchanged direct-sum factors before and after the two layers.  Inserting
either side of (4) into \(\delta_a\oplus\delta_b\) gives the same word

\[
(a+2),a,(a-1),\ldots,2,(a+b+2),1,
(a+b+1),(a+b),\ldots,(a+3),(a+1), \tag{5}
\]

with an indicated decreasing range omitted when it is empty.  This proves
the claimed equality directly from the insertion definition.

Every one of the \(m-1\) position boundaries is either internal to a layer
or between two layers.  Equations (3) and (4) give distinct active
left-hand pattern-(C) triples for all of them.  Ray and West's upper bound
therefore forces \(j(\beta)=m-1\).  Substitution in (1) gives (2).

Complementation is an automorphism of the permutation-pattern poset and
takes layered permutations to colayered permutations.  Hence it preserves
\(g_2\), and (1) then preserves \(j\), proving the colayered case.  Finally,
the universal bound \(j\leq m-1\) in (1) shows that the value in (2) is the
minimum possible.  \(\square\)

## Exact verification

The scripts use only exact Python integers and tuples and have no external
dependencies.

Run the insertion-based verifier:

```bash
python3 permutation_patterns_layered_g2/verify_layered_g2.py --max-n 9
```

It checks all \(2^{n-1}\) layered permutations for every \(1\leq n\leq9\),
checks the explicit witness at every boundary, enumerates all active
two-point insertion images, and compares their number with (2).  Expected
final line:

```text
verified 511 layered patterns through n=9; all witnesses and g2 values agree
```

Run the independent definition-level verifier:

```bash
python3 permutation_patterns_layered_g2/independent_check.py --max-n 6
```

It instead enumerates every permutation of length \(n+2\), standardizes all
of its \(n\)-subsequences, and counts which layered and colayered patterns
occur.  It does not use insertion triples or active sites.  Expected final
line:

```text
independently verified layered and colayered g2 values through n=6
```

Tested with CPython 3.11.2.  The computation is corroborative: the theorem
rests on the finite case distinction and explicit identities (3)--(5),
together with Ray and West's published identification of \(j\).

## Sources and novelty scope

- N. Ray and J. West, *Posets of matrices, and permutations with forbidden
  subsequences*, Annals of Combinatorics **7** (2003), 55--88.
  <https://eprints.maths.manchester.ac.uk/609/>
- V. Vatter, *An assortment of problems in permutation patterns:
  unimodality, equivalence, derangements, and sorting* (2026), especially
  the problems asking for a statistic for \(j\) and a formula for \(g_3\).
  <https://arxiv.org/abs/2602.16355>

The theorem above appears new in targeted searches of the cited papers,
their terminology, and the committed Discovery Net graph as of 2026-09-02.
This is a search-relative novelty assessment, not a priority claim.
