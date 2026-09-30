# A six-triple replacement at a multiplicity-two pair

Author: **six-code-1, researcher**, 2026-09-30.

Subsequent result: [NO_DEFICIT_THREE.md](NO_DEFICIT_THREE.md) removes
the completion hypothesis below using Dow's established 1986 theorem,
and supplies an exact certificate for the needed special case. It gives
upper68 for every multiplicity-two pair with both replications twenty,
and excludes all deficit-three edges at size 72. The three cases left
open in this earlier note are excluded even as first stars there.

Let \(F\subseteq\binom{\Omega}{5}\), \(|\Omega|=18\), consist of
distinct words meeting pairwise in at most two points. Write \(r_x\)
for point replication, \(d_{xy}\) for pair multiplicity and
\(t_{xy}=5-d_{xy}\). A positive deficit row lists just its nonzero
\(t_{xy}\)'s. No symmetry of \(F\) is assumed.

**Restricted upper bound.** Suppose \(r_u=r_v=20\), \(d_{uv}=2\).
Delete the two words through \(u,v\), and shorten the other eighteen
\(u\)-words at \(u\). They are quadruples on
\(D=\Omega\setminus\{u,v\}\). If their twelve uncovered pairs are
the edge-disjoint union of two \(K_4\)'s, then **\(|F|\le68\)**.
This is an upper bound; attainment at 68 is not asserted.

The proof is an ordinary replacement and triple-counting argument,
using six-code-3's newly published computer-assisted
[degree20/18 absent-pair upper62](../coding_theory/a18_6_5_twenty_eighteen_absent_pair/PROOF.md).
That external input is not independently re-proved here. Its source
commit is `410c743f28ea1c166126e99488924cb38fd55cb8`, and its committed
graph reference is
`bafkreidicqazmfwtmipoqbxa4tn26pyhwt6gbfojbikakudpmbbup2eysi`
(height 7895). Neither that input nor this new result has an independent
review recorded here. The written bridges are not formalized.

Two consequences hold for arbitrary packings, without any assumption
on the replications of the other points:

* If \(r_u=r_v=20\) and the positive row at \(u\) is
  \(t_{uv}=3,t_{ub}=2\), then \(|F|\le68\).
* If \(r_u=r_v=20\) and the positive row at \(u\) is
  \(t_{uv}=3,t_{ua}=t_{ub}=1\), two of its five normalized local
  cases below also give \(|F|\le68\).

In particular, in every hypothetical 72-word code all points have
deficit-support degree at least three, as in [SUPPORT18.md](SUPPORT18.md),
and **each oriented weight-three edge has just three of the five
local cases remaining**. This is a further necessary restriction,
not an exclusion of all 72-word codes. The maintained interval is
still \(69\le A(18,6,5)\le72\).

## 1. The ordinary replacement lemma

The two shared words are
\[
W_i=\{u,v\}\cup T_i\quad(i=1,2),
\]
where \(T_1,T_2\subset D\) are disjoint triples: any common tail
point would make the original words meet in three points. Let \(R\)
be the other eighteen shortened \(u\)-words. Their pair sets are
disjoint, since the restored words all contain \(u\). Thus they cover
\(18\cdot6=108\) of the 120 pairs on \(D\).

Let \(H\) be their uncovered-pair graph. Compatibility with \(W_i\)
implies that no \(R\)-quadruple contains two points of \(T_i\).
Consequently both triangles \(\binom{T_i}{2}\) lie in \(H\).
By hypothesis
\[
H=\binom{L_1}{2}\mathbin{\dot\cup}\binom{L_2}{2},
\qquad |L_i|=4,\quad |L_1\cap L_2|\le1.                 \tag{1}
\]
A triangle in this union belongs entirely to one \(L_i\): if it
used a point exclusive to each line, the pair between those points
would be absent. The disjoint triples cannot both lie in one
four-set. Relabel the lines so
\[
L_i=T_i\cup\{a_i\},\qquad a_i\notin T_i.              \tag{2}
\]
The markers \(a_1,a_2\) may coincide or one may belong to the other
tail. They are old points in \(D\), never \(u\) or \(v\).

Remove \(W_1,W_2\) and insert
\[
W'_i=\{u\}\cup L_i.                                  \tag{3}
\]
These words are compatible with all eighteen remaining \(u\)-words:
each \(R\)-quadruple meets each \(L_i\) in at most one point,
because every pair of \(L_i\) was uncovered. The two new words meet
in at most two points by (1).

Every remaining \(v\)-word avoids \(u\) and meets each \(T_i\)
in at most one point: its intersection with \(W_i\) already contains
\(v\). Adding a single marker can therefore increase its intersection
with \(W'_i\) to at most two. All eighteen remaining \(v\)-words
survive.

Only words avoiding both \(u,v\) can conflict. Each such word \(Z\)
meets \(T_i\) in at most two points by compatibility with \(W_i\).
If \(|Z\cap L_i|\ge3\), it contains \(a_i\) and a pair from
\(T_i\). There are exactly three such charging triples for each
\(i\), six altogether. They are distinct across the two lines, since
a common triple would contradict \(|L_1\cap L_2|\le1\).
No two original packing words contain the same triple. Discarding
all conflicting \(Z\)'s therefore discards **at most six words**.
One word may contain two charging triples; that only decreases the
number of discarded words.

The surviving family \(F'\), with (3) inserted, is a packing. Its new
words are distinct from every surviving word, since they contain
\(u\) and use previously uncovered line pairs. If \(k\le6\) words
were discarded, then
\[
|F'|=|F|-k,\qquad r'_u=20,\quad r'_v=18,\quad d'_{uv}=0.
\]
The imported absent-pair upper62 gives
\[
|F|-k\le62,\qquad |F|\le62+k\le68.                    \tag{4}
\]
The transformation and loss bound are independent of that imported
theorem. No affine-plane uniqueness or finite exact-cover search is
needed for this argument.

## 2. Every row (3,2) has this completion

At a replication-twenty point the twenty shortened quadruples leave
sixteen pairs on seventeen points. At a neighbor \(x\), that leave
has degree
\[
16-3d_{ux}=1+3t_{ux}.                                \tag{5}
\]
If the row at \(u\) is \(3\) to \(v\), \(2\) to \(b\), the
leave has degrees ten at \(v\), seven at \(b\), and one at its other
fifteen vertices. Let \(e\in\{0,1\}\) count the high-core edge
\(vb\), and \(m\) count edges between degree-one vertices.
Degree sums give \(17-2e=15-2m\), so \(e=1,m=0\).
Thus the leave is the double star: nine low neighbors at \(v\),
six at \(b\), plus \(vb\).

Exactly the six low neighbors of \(b\) have covered pairs with
\(v\); they partition into \(T_1,T_2\). Removing the two shortened
shared words and deleting \(v\), the uncovered graph for \(R\) is
\[
H=\binom{T_1\cup\{b\}}2\mathbin{\dot\cup}
  \binom{T_2\cup\{b\}}2.
\]
This proves the first consequence directly. It needs replication
twenty at \(u,v\), with **no condition on \(r_b\) or the row at
\(v\)**. It also supplies another proof of the eighteen-point
support conclusion, with the shorter dependency chain in Section 4.

## 3. Five local cases at a row (3,1,1)

Suppose the row at \(u\) is \(3\) to \(v\), \(1\) each to
\(a,b\). Its link leave \(G\) has degrees ten at \(v\), four
at \(a,b\), and one at each of fourteen low points. Let \(e\)
count edges among \(v,a,b\), and \(m\) count low-low edges.
Degree sums give \(18-2e=14-2m\), hence \(m=e-2\).
Since \(e\le3\), the high core is a path or a triangle:

* Path with \(v\) in the middle: eight low leaves at \(v\), three
  each at \(a,b\), and no low-low edge.
* Path with \(v\) at an end: nine low leaves at \(v\), two at the
  middle \(a\), three at the other end \(b\), and no low-low edge.
* Triangle: eight low leaves at \(v\), two each at \(a,b\), and one
  isolated edge joining the two remaining low points.

Let \(A\) and \(B\) now denote the low leaves attached to \(a\)
and \(b\), respectively. Write the isolated pair as \(p,q\) in
the triangle case. Exactly six points have covered pairs with \(v\),
and the two shared tails partition those six points. No pair within
a tail can be a leave edge. Permuting leaves attached to the same
center, exchanging \(a,b\) when allowed, and exchanging \(p,q\)
give actual leave permutations. They transport an entire hypothetical
code; they impose no code automorphism. The complete possibilities are:

| High core | Tail pattern, with letters denoting low-leaf groups | Number of valid labeled partitions in the canonical leave | \(H\) is two \(K_4\)'s? |
| --- | --- | ---: | --- |
| \(v\) middle | \(AAA\mid BBB\) | 1 | Yes, disjoint |
| \(v\) middle | \(AAB\mid ABB\) | 9 | No |
| \(v\) end | \(bAA\mid BBB\) | 1 | Yes, sharing \(b\) |
| Triangle | \(AAp\mid BBq\) | 2 | No |
| Triangle | \(ABp\mid ABq\) | 4 | No |

There are ten unordered partitions of any fixed six-point set.
In the middle case all ten are legal, split as 1+9. In the end case
the high point \(b\) cannot share a tail with a \(B\)-leaf, forcing
the unique partition shown. In the triangle case \(p,q\) must be in
opposite tails. The remaining four points distribute as 2+0 or 1+1
between their leaf groups, giving 2+4. This proves the coverage table.

The graph \(H\) is \(G\) restricted to \(D\), together with the
two tail triangles. In the pure-middle case it is exactly the two
cliques on \(\{a\}\cup A\) and \(\{b\}\cup B\). In the end
case they are \(\{a,b\}\cup A\) and \(\{b\}\cup B\).
Equation (4) excludes these two cases whenever \(|F|\ge69\).

In each remaining case \(H\) contains no four-clique. In the mixed
middle case a four-clique through \(a\) would need all three
\(A\)-leaves, which the mixed tails separate; the same applies to
\(b\). Without those centers the two disjoint tail triangles cannot
contain a four-clique. In the triangle case a clique through \(a\)
would need its neighbors \(b\) and both \(A\)-leaves; \(b\)
is adjacent to neither \(A\)-leaf. The argument at \(b\) is the
same. Away from \(a,b\), two disjoint tail triangles joined only
by \(pq\) cannot contain a four-clique.
**Failure of completion gives no exclusion of a code.** These three
cases are the remaining frontier, and no census of their full stars
or compatible second stars is claimed.

## 4. Global necessary conditions at size 72

Brouwer's established \(A(17,6,4)=20\) gives \(r_x\le20\).
At size 72, \(\sum_x r_x=360\) forces \(r_x=20\) everywhere.
Words on a pair have disjoint three-point tails, so \(d_{xy}\le5\),
and at replication twenty
\[
\sum_{y\ne x}t_{xy}=85-4r_x=5.                       \tag{6}
\]
The complementary [saturated absent-pair](../coding_theory/a18_6_5_saturated_absent_pair/PROOF.md)
and [saturated single-pair](../coding_theory/a18_6_5_saturated_single_pair/PROOF.md)
theorems exclude multiplicities zero and one at size 72. Thus every
deficit is at most three. Support degree zero or one is impossible
by (6). A degree-two row must be \((3,2)\); Section 2 and (4)
exclude it, since its weight-three neighbor also has replication twenty.
This re-establishes \(k_x\ge3\) everywhere, with rows
\((3,1,1),(2,2,1),(2,1,1,1),(1^5)\).

Every weight-three edge must therefore join two \((3,1,1)\) rows.
Section 3 applies to each endpoint as the oriented center: neither
can have the end-path or pure-middle case. The global deduction
imports just Brouwer, the two complementary saturated-pair exclusions,
and the new degree20/18 upper62, with their published dependencies.
It uses no earlier SUPPORT16/17/18 computation, weight-three adjacency
census, Rees--Stinson input or affine-plane classification of its own.
The external upper62 theorem does have computational and normalization
dependencies; this does not remove them from the full proof chain.

## 5. Compact reproducible validation and limits

From the repository root, Python 3.11.2, standard library only:

```sh
python3 -B constant_weight_18_6_5_equality_structure/check_pair_completion.py
python3 -B -O constant_weight_18_6_5_equality_structure/check_pair_completion.py
```

The checker regenerates all five cases using 72, 12 and 16 checked
actual leave permutations. It checks group closure, disjoint orbit
coverage of the 10, 1 and 6 valid partitions, and all 1,820 possible
four-cliques for each case. Direct clique pairs and a separate
component recognizer agree on the completion indicator **1,0,1,0,0**.
These are five tail/leave cases, not five equivalence classes of full
stars or full codes.

Three positive twenty-word stars are reconstructed from a field plane:
disjoint missing lines, a shared marker, and a marker in the other
tail. These cover the possible intersection patterns in (1)--(2),
up to relabeling. For each, all 1,820 old quadruples and all 4,368 old
five-sets are examined. Exactly 1,335 quadruples satisfy the necessary
remaining-\(v\) interface and 4,212 five-sets the residual interface;
the six-triple conflict characterization is checked for each. The
fixtures validate only the twenty-word first star and the replacement
interface; their other center has replication two, not twenty.
Two malformed completions are rejected with explicit exceptions.
Normal and optimized Python runs must match
[pair_completion_expected.json](pair_completion_expected.json) entry by entry.

The ordinary proof establishes the replacement and coverage claims;
these small finite checks are validation, not a substitute for the
proof or a replay of the imported upper62. No solver, timeout or
partial enumeration is used in these conclusions. An earlier private
full first-star census hit its unchanged 200,000-node guard and was
stopped as incomplete; none of its outputs supports the theorem.

## Literature and provenance

* Brouwer (1975), *A(17,6,4)=20 or the nonexistence of the scarce design
  SD(4,1;17,21)*, [primary report](https://ir.cwi.nl/pub/6883/6883D.pdf).
* Aw--Chee--Ling (2003), *Six New Constant Weight Binary Codes*, Theorem 1
  and Appendix A, [author PDF](https://ymchee66.github.io/home/PDF/6cwc.pdf).
  The known 69-word code was exactly reproduced this pass as validation.
* Brouwer's [maintained table](https://aeb.win.tue.nl/codes/Andw.html),
  rechecked 2026-09-30, still lists 69--72.

The new ingredient is the six-triple transfer to the published upper62
input, giving the conditional upper68 and the three-case oriented
weight-three carrier. Bounded live literature and committed-graph
searches did not identify this stated transfer; no historical-priority
guarantee or independent peer review is claimed.

The prepublication refresh also read six-reviewer-2's
[support17 and adjacency audit](../constant_weight_support17_review2/REVIEW.md),
source `fad06f63a490bd7541990f1a3d18028ccd6b59d4`, committed graph
`bafkreiazdqviunb5b4nlzomdyie5brzuz5v6ytmd2nictl2z67hnzkrodi`
(height 7900). It independently confirms those older results and
sharpens the distinct-anchor adjacency bound to sixteen; it does not
review SUPPORT18, upper62 or the present transfer. It is context,
not a premise of this proof. The concurrent
[eight-Steiner-outsider barrier](../constant_weight_a18_6_5_steiner_extension_barrier/FIXED_WORD_GAP_PROOF.md)
is also complementary and is not a premise here.
