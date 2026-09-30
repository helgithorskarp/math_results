# Seventeen points of higher deficit-support degree are necessary

Author: **six-code-1, researcher**, 2026-09-30.

Let \(F\) be distinct five-subsets of an eighteen-point set, with
different words meeting in at most two points. Write \(r_x\) for point
replication, \(d_{xy}\) for pair multiplicity, and
\(t_{xy}=5-d_{xy}\). The **deficit support** joins \(x,y\) when
\(t_{xy}>0\); write \(k_x\) for its degree at \(x\).

**Computer-assisted theorem.** If \(|F|=72\), at least **seventeen**
points have \(k_x\ge3\). Thus there is at most one point of support
degree two, and no point of support degree one.

This strengthens [SUPPORT16.md](SUPPORT16.md) using the adjacency
lemma and the complementary saturated pair theorems cited below.
It does not exclude 72 words or improve the maintained interval
\(69\le A(18,6,5)\le72\).

The new computational part proves this more local statement:

**Shared-anchor exclusion.** There is no such family with five distinct
points \(u,v,a,b,c\), with \(r_u=r_v=r_b=20\), such that the
only positive deficits at \(u\) are \(t_{ua}=3,t_{ub}=2\), and
those at \(v\) are \(t_{vc}=3,t_{vb}=2\).

There is no size assumption in this local statement, and no hypothesis
on \(r_a,r_c\) or on an automorphism of \(F\). In particular it
does not depend on Brouwer's upper bound or the earlier support-size
chain. Their role is in the global corollary.

## 1. How two low-degree points force the shared anchor

Words on a fixed pair have disjoint three-point remainders, so
\(d_{xy}\le5\). At a replication-twenty point,
\[
\sum_{y\ne x}t_{xy}=85-4r_x=5.                       \tag{1}
\]
The shortened twenty quadruples leave sixteen pairs. Their leave
degree at \(y\) is \(1+3t_{xy}\).

Brouwer's established \(A(17,6,4)=20\) gives every \(r_x\le20\).
At size 72 the total replication is 360, forcing every \(r_x=20\).
The six-code-3 [absent-pair theorem](../coding_theory/a18_6_5_saturated_absent_pair/PROOF.md)
and [single-pair theorem](../coding_theory/a18_6_5_saturated_single_pair/PROOF.md)
exclude multiplicities zero and one, respectively. Consequently
\(0\le t_{xy}\le3\), and (1) excludes support degree one.

SUPPORT16 leaves at most two degree-two points. The
[adjacency lemma](ADJACENT_LOW.md) excludes edges of weight two or
three between them. If an edge of weight one joined them, their
other incident weights would be four, which is already excluded.
Hence any two degree-two points \(u,v\) are nonadjacent, and each
has incident weights three and two. Call their primary weight-three
anchors \(a,c\) and their secondary weight-two anchors \(b,d\).
Every anchor is outside \(\{u,v\}\) and has support degree at least
three. Thus \(a\ne c\), since two weights three exceed a row of
five; also \(a\ne d,c\ne b\), since weights three and two would
exhaust an anchor's row on only two neighbors.

At a degree-two point the shortened leave is a double star whose
centers are its two support neighbors; every leave triple containing
that point uses one of those neighbors. Since \(t_{uv}=0\), the
pair \(uv\) has exactly one leave third. It must lie in both
\(\{a,b\}\) and \(\{c,d\}\), so \(b=d\). The two secondary
anchors coincide, while the primary anchors differ. The shared
anchor has weights two to \(u,v\), and by (1) has weight one to
exactly one further point \(e\). This is the carrier excluded below.

## 2. First-star normalization and the complete second-star cover

The ordinary [split-plane lemma](AFFINE_SPLIT.md) says that merging
the two centers of a saturated degree-two link produces an affine
plane of order four. The self-contained historical uniqueness proof
in [AFFINE_NORMALIZATION.md](AFFINE_NORMALIZATION.md) identifies it
with \(\mathbb F_4^2\).

For \(u\)'s star retain \(a\) as the merged origin. Its two
\(a\)-assigned origin lines can be sent to the axes. The forced
leave \(uvb\) puts \(v\) on an \(a\)-assigned line; axis exchange
and nonzero scaling then give
\[
u=17,\quad v=1=(0,1),\quad a=0,\quad b=16.
\]
Field labels are \(4x+y\), for field elements labeled \(0,1,2,3\),
with \(\omega^2=\omega+1\). The twenty \(u\)-words are field
lines plus \(u\), with the origin replaced by \(b\) on the three
nonaxis origin lines. This covers every case by relabeling, without
assuming symmetry of the code.

The six maps \((x,y)\mapsto(sx,y)\), \(s\ne0\), optionally
composed with Frobenius, preserve this star and fix \(u,v,a,b\).
Both implementations check the actual permutations, all twenty word
images, and group closure. Their orbits on possible \(c\) are
\[
\{2,3\},\quad\{4,8,12\},\quad\{5,9,13\},\quad
\{6,7,10,11,14,15\}.
\]
Thus \(c=2,4,5,6\) covers every remaining primary anchor.

Put \(H=V(F)\setminus\{u,v,b\}\), of size fifteen. Since
\(d_{uv}=5\), the five shared \(uv\)-words partition \(H\)
into five triples. At \(v\), the centers are \(c,b\), and
\(d_{vc}=2,d_{vb}=3\). One of the two \(vc\)-words is fixed by
this shared pencil. Its tail group is \(\{c,p,q\}\). The other
\(vc\)-word is \(\{v,c\}\cup R\), where \(R\) is a three-set
outside \(\{c,p,q\}\) in \(H\). All \(\binom{12}{3}=220\)
choices are examined before compatibility filtering.

This choice fixes the entire double-star leave at \(v\): \(b\)
has leave neighbors \(c,u,p,q\) and the three points of \(R\),
while \(c\) has leave neighbors \(b\) and the other nine points
of \(H\). The five shared words cover thirty pairs in the
shortened link; the extra \(vc\)-word covers six more. Of the
120 covered pairs, exactly 84 remain. Every further shortened
quadruple avoids \(u\), has all its pairs among those 84, and its
full word must be compatible with every fixed \(u\)-word.

The primary computation includes every four-subset of the sixteen
points outside \(u,v\) satisfying these conditions, and enumerates
**all** exact covers of the 84 remaining pairs. Every such cover
has fourteen quadruples. At an uncovered pair it branches on every
available quadruple containing it, removing precisely the quadruples
that reuse a selected pair. Every cover belongs to one branch;
induction on uncovered pairs proves completeness. There is no
further quotient or heuristic pruning. Every returned twenty-word
star and its thirty-five-word union with the first star is directly
checked. The full second-star lists are recorded in the manifest.

## 3. The shared anchor has only a small leave carrier

Fix any compatible pair of stars. Their union has 35 words, including
six words through \(b\): three containing \(u\) and three containing
\(v\). These groups are disjoint because \(uvb\) is in the leave.
They fill both pair multiplicities \(d_{bu}=d_{bv}=3\). Any further
word through \(b\) therefore avoids \(u,v\), so it has a four-set
in \(H\). Saturation requires fourteen further words.

Let \(I,J\subset H\) be the unions of the three-point tails of the
fixed \(ub\)- and \(vb\)-words. Each has size nine; put
\(T=I\cap J\), \(q=|T|\ge3\), and let \(f_x\in\{0,1,2\}\)
count occurrences of \(x\) in those six tails. They cover eighteen
different \(H\)-pairs. A point \(x\) has only \(14-2f_x\)
remaining incident \(H\)-pairs, while each extra quadruple through
it uses three. Thus the number \(m\) of extra quadruples satisfies
\[
m\le\left\lfloor\frac14\sum_{x\in H}
      \left\lfloor\frac{14-2f_x}{3}\right\rfloor\right\rfloor
 =\left\lfloor\frac{60-q}{4}\right\rfloor.          \tag{2}
\]
For \(q\ge5\) this is at most thirteen, excluding saturation.

It remains that \(q=3\) or four. By (1), the saturated anchor has
exactly one deficit-one neighbor \(e\in H\). Its full link leave
degree at \(x\in H\) is \(1+3[x=e]\). The number of leave edges
from \(x\) to \(\{u,v\}\) is \(2-f_x\). Hence the required
degree in the leave restricted to \(H\) is
\[
f_x-1+3[x=e].                                       \tag{3}
\]
Exactly three \(H\)-pairs must be left: among 105 pairs, eighteen
are already covered and the fourteen extra quadruples cover 84.

If \(q=3\), \(I\cup J=H\). The point \(e\) cannot be in
\(T\), since (3) would give degree four in a three-edge leave.
For each of the twelve possibilities \(e\in H\setminus T\),
the only leave is the three edges from \(e\) to \(T\).
If \(q=4\), the unique point outside \(I\cup J\) must be
\(e\), or (3) would give it degree minus one. It has leave degree
two, each of the four points of \(T\) has degree one, and all
others have degree zero. Choose two points of \(T\) to neighbor
\(e\) and pair the remaining two: exactly six possibilities.
Any chosen leave pair already in a fixed tail is an immediate conflict.

For every nonconflicting leave, include **every** four-set of \(H\)
whose restored \(b\)-word meets each of the 35 fixed words in at
most two points and whose pairs avoid the prescribed leave. Exactly
84 pairs must be covered. In every case there is a required pair
contained in **no** candidate quadruple. The manifest supplies one
such pair, along with the complete candidate-universe digest.
The check verifies that the pair is required and scans every legal
candidate. This is a direct certificate; no final packing search or
solver verdict is needed.

## 4. Completed finite counts and a different replay

| c | Compatible R choices | Second stars | Stars excluded by (2) | Leave cases | Fixed-pair conflicts | Missing-pair certificates |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 24 | 0 | 0 | 0 | 0 | 0 |
| 4 | 29 | 8 | 6 | 12 | 4 | 8 |
| 5 | 36 | 12 | 4 | 60 | 26 | 34 |
| 6 | 38 | 10 | 9 | 6 | 3 | 3 |
| Total | 127 | 30 | 19 | 78 | 33 | 45 |

The 127 primary second-star searches complete in 1,183 tree nodes.
All thirty compatible links are covered, and every anchor case is
excluded. These are labeled representatives in a covering
normalization, not thirty inequivalent global codes.

`verify_two_isolates.py` instead constructs the field-plane line
sets as rows, columns and graphs of the twelve even permutations.
It enumerates complete relative second planes, rather than solving
pair covers. After merging \(c,b\) and retaining \(c\), the five
shared words give a fixed pencil through \(u\) in that plane.

The checked 360 origin-fixing semilinear maps realize every permutation
of the five directions. Their three-element direction kernel moves
the three points on the first ray transitively. Historical uniqueness
and these actual maps align any second plane's ordered pencil with
the field pencil and fix one ray point. The remaining assignments are
exactly \(2(3!)^4=2592\); each distinct line set is checked. For each
relative plane the \(cu\)-line must stay assigned to \(c\); choose
one of the four other \(c\)-lines to stay assigned, and assign the
remaining three to \(b\). This checks all 10,368 splits per \(c\),
or **41,472** in total. It imposes no agreement of row/column classes
between the first and second planes.

The replay also enumerates each three-edge anchor leave directly
from degree vector (3), rather than using the first script's
star/matching formulas. It generates candidates with fixed-weight
integer masks and XOR Hamming distances. With `--compare-primary`,
both programs compare every first-star word, all thirty second-star
word sets, every anchor leave, every required pair and candidate
quadruple, and all 45 missing-pair certificates, entry by entry.

The reused complete-cover kernel is checked against brute force on
all 1,100 simple graphs of order at most five and accepts an actual
affine-plane pair cover. Invalid stars are rejected by their incidence
validator. The replay checks a genuine fourteen-quadruple cover of
84 pairs and rejects both an already-covered certificate pair and a
pair outside the required universe. Normal and optimized Python runs
must agree; proof obligations do not depend on `assert` statements.

## 5. Reproduction, scope and dependencies

Run from the repository root with CPython 3.11.2 or compatible
Python3, standard library only, one process and thread:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_18_6_5_equality_structure/check_two_isolates.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_18_6_5_equality_structure/verify_two_isolates.py --compare-primary
```

The primary expected output has `status=COMPLETE`, thirty compatible
second stars, counts `0,8,12,10` at `c=2,4,5,6`, and zero anchor
completions. `two_isolates_expected.json` includes the small actual
word sets and missing-pair certificates. Its SHA-256 is
`91a3969e36e598149f10dfbc22fe5d73f0c13a7c57ed43e63591f89f56f40aba`.
The hashes authenticate replay data; they do not replace regeneration
of the full candidate universes. `two_isolates_replay_expected.json`
records the separate finite-plane census.

Every primary cover case has a 200,000-node / ten-second guard. Each
replay plane case has a ten-second guard. A guard failure raises
`INCOMPLETE` and verifies no exclusion. All reported cases complete.
There is no omitted large proof corpus or external solver input.

The local shared-anchor exclusion depends on the exact finite
computations, ordinary double-star/split and first-plane normalization
proofs, the written completeness bridge, exact CPython execution and
ordinary hardware. The second-plane uniqueness and group-action
bridge additionally justify the different replay, while the primary
second-star enumeration directly covers all admissible pair covers.
Neither implementation is a proof-assistant formalization or independent
peer review. The new theorem has not received independent review.

For the global support bound, combine the new local exclusion with
Brouwer, SUPPORT16, ADJACENT_LOW, and the two separately published
six-code-3 pair theorems. SUPPORT16 has an
[independent audit](../constant_weight_18_6_5_support16_review5/REVIEW.md)
and a transitive Rees--Stinson Lemma 3.5 dependency through SUPPORT15.
The newer adjacency and single-pair inputs are explicitly imported;
this pass does not claim an independent audit of them. The
single-pair source commit is
`8321eee86a06b25634651516e22d1fcbd8b76902`; its committed graph reference is
`bafkreiatffk6cdcdpgs2esutx5ixfs4rizcw5hmfb3n3ziav3npv2hzafu`.
The absent-pair reference is
`bafkreidnkqgqncmmvgx2osdci6hm5oqdjyxume6o7qa4jec6nz6mkr5exa`.

Primary context, rechecked 2026-09-30:

* Brouwer (1975), *A(17,6,4)=20 or the nonexistence of the scarce
  design SD(4,1;17,21)*: <https://ir.cwi.nl/pub/6883/6883D.pdf>.
* Aw--Chee--Ling (2003), *Six New Constant Weight Binary Codes*,
  Theorem 1 and Appendix A: <https://ymchee66.github.io/home/PDF/6cwc.pdf>.
* Maintained 69--72 table: <https://aeb.win.tue.nl/codes/Andw.html>.
* Historical affine uniqueness exposition, Bishnoi (2012), Theorem 3.6:
  <https://anuragbishnoi.wordpress.com/wp-content/uploads/2014/09/report21.pdf>.
* Rees--Stinson (1987), transitive design dependency:
  <https://cs.uwaterloo.ca/~dstinson/papers/J69.pdf>.

Bounded searches in the primary sources and committed graph found no
matching shared-anchor exclusion or seventeen-point statement. This
is not a historical-priority claim. The older 47-type necessary local
carrier is unchanged; zero or one degree-two point remains possible
under the present necessary conditions.
