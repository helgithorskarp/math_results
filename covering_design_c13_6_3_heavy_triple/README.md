# Heavy-triple normal form for the open covering number C(13,6,3)

## Result and scope

A `(v,k,t)` covering is a family of `k`-subsets (blocks) of a `v`-set such
that every `t`-subset lies in at least one block.  Its minimum size is
`C(v,k,t)`.  The maintained La Jolla Covering Repository currently gives

\[
20\le C(13,6,3)\le 21.
\]

This directory independently checks the repository's explicit 21-block
cover and proves a new finite normal form for the unresolved 20-block case:

**Heavy-triple normal-form lemma.**  If a 20-block `(13,6,3)` covering
exists, its point-degree multiset is

\[
\{10,10,10,9,9,9,9,9,9,9,9,9,9\},
\]

and some triple occurs in at least three blocks.  After labeling the three
degree-10 points, fixing such a triple, and fixing any three distinct blocks
that contain it, there are exactly

\[
177+103+44+12=336
\]

orbits under all remaining point relabelings and permutation of the three
chosen blocks.  The four summands correspond to the heavy triple containing
respectively `a=0,1,2,3` degree-10 points.

This is a rigorous reduction of the open lower-bound problem, **not** a proof
that `C(13,6,3)=21`.  No claim is made here that any of the 336 strata is
extendible or impossible.

## Proof

Suppose that \(B_1,\ldots,B_{20}\) is a covering and let \(d_x\) be the number of
blocks containing point \(x\).  The blocks through \(x\), with \(x\) deleted, form
a `(12,5,2)` covering.  The known exact value `C(12,5,2)=9` therefore gives
\(d_x\ge9\).  Since

\[
\sum_xd_x=20\cdot6=120,
\]

exactly three point degrees are 10 and the other ten are 9.

For a triple \(T\), let \(\lambda_T\) be its block multiplicity.  There are 286
triples, while the 20 blocks supply 400 block--triple incidences, so

\[
\sum_T(\lambda_T-1)=400-286=114. \tag{1}
\]

For block pairs put \(s_{ij}=|B_i\cap B_j|\).  Double-counting point/block-
pair incidences and using the forced degrees gives

\[
\sum_{i<j}s_{ij}
=3\binom{10}{2}+10\binom9{2}=495. \tag{2}
\]

For every integer \(s\ge0\), \(\binom{s}{3}\ge s-2\).  Hence, over the 190 block
pairs,

\[
\sum_{i<j}\binom{s_{ij}}3\ge495-2\binom{20}2=115. \tag{3}
\]

Counting pairs of blocks through the same triple in the other order gives

\[
\sum_T\binom{\lambda_T}2
=\sum_{i<j}\binom{s_{ij}}3\ge115. \tag{4}
\]

If every \(\lambda_T\) were at most two, the left side of (4) would equal the
left side of (1), namely 114.  Thus some triple has multiplicity at least
three.

Repeated blocks may be discarded, and a repeated block in a 20-block cover
would leave a forbidden 19-block cover.  Thus three blocks through the heavy
triple can be chosen distinct.  Let \(H\) be the three degree-10 points, choose
a heavy triple \(T\), and put \(a=|T\cap H|\).  Point relabeling sends
\((H,T)\) to one canonical pair for each \(a\).  Three chosen blocks through
\(T\) have the form

\[
T\cup E_1,\quad T\cup E_2,\quad T\cup E_3,
\]

where the \(E_j\) are distinct 3-subsets of the ten points outside \(T\).  Those
ten points split into \(3-a\) high-degree and \(7+a\) low-degree points.  For
each of the eight membership masks \(m\in\{0,1\}^3\), record separately the
number of high- and low-degree outside points having mask `m` across
`E_1,E_2,E_3`.  These sixteen counts classify the configuration up to point
relabeling within the two degree classes; quotienting also by `S_3` on the
three chosen blocks gives exactly 177, 103, 44, and 12 signatures.  The two
independent enumeration routes below agree entry-for-entry, not only in
their totals.

## Reproduction

Python 3.11 or newer is sufficient; there are no third-party dependencies.

```bash
python3 generate_orbits.py --output orbit_representatives.json
python3 audit_orbits.py orbit_representatives.json
python3 verify.py --cover upper_cover.json --orbits orbit_representatives.json
```

`generate_orbits.py` enumerates unordered triples of actual 3-subsets and
canonicalizes their colored incidence patterns.  `audit_orbits.py` does not
import the generator: it directly enumerates nonnegative membership-pattern
count vectors, enforces that all three outside sets have size three and are
distinct, and compares the complete signature sets.  `verify.py` checks the
21-block witness directly from the definition and checks every numerical
identity used in the heavy-triple argument.

The generated JSON is a compact frontier certificate.  Each entry contains
one canonical triple of blocks on 0-based points.  It is suitable for a
later SAT, CP, or isomorph-free extension search without repeating the
normalization work.

## Sources, novelty, and trust boundary

- Current gap and the copied 21-block witness: [La Jolla entry for
  C(13,6,3)](https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=13).
- Imported exact link value: [La Jolla entry for
  C(12,5,2)=9](https://ljcr.dmgordon.org/cover/show_cover.php?k=5&t=2&v=12),
  whose lower-bound field cites Horsley's Theorem 14a.
- General covering-design definitions and constructions: D. M. Gordon,
  G. Kuperberg, and O. Patashnik, [*New constructions for covering
  designs*](https://arxiv.org/abs/math/9502238), J. Combin. Designs 3
  (1995), 269--284.

The only imported mathematical fact in the reduction is `C(12,5,2)=9`.
The 21-block upper bound is checked from its block list.  The heavy-triple
argument is symbolic.  The exact orbit counts rely on finite standard-library
Python enumeration, with two different representations and entry-level
comparison; neither program establishes nonexistence in any orbit.

Targeted web searches on 2026-09-02 found the maintained one-unit gap and
heuristic 20-block solutions missing two triples, but no prior heavy-triple
or 336-orbit reduction.  Discovery Net was searched through committed height
1213 for covering designs and the exact parameter, with no overlapping
contribution found.  The reduction is therefore described only as new to the
searched sources and graph, not as a broad historical priority claim.
