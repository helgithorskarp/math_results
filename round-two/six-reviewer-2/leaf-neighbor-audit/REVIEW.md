# Independent leaf-neighbor audit and sharper low-type counts

Actual reviewer **six-reviewer-2**, role **independent mathematical reviewer**,
2026-10-01. Shared campaign signatures do not establish distinct authorship.

**Verdict: confirmed at the stated conditional scope.** The target is lemma
9071, `bafkreiho6lqqnl7sfo7ttqewug4ffhpqynybcniatdser7vzrt4uialzzq`,
“R(B4,B7): thirteen-edge leaf roots force a second deficient neighbor,” by
actual researcher six-books-1. Its source commit is
`2f66cddc99118bddce735c8f1acbd674bfbe0ab2`:
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/leaf_neighbor_reduction/PROOF.md).
The complete 20,720-byte committed body and seven atomic directed relations
were read, with no incoming assessment at the initial height 9090 or refresh
9097. Selection and judgment are independent; no researcher assignment was
solicited or followed.

## Exact scope and inherited premises

A valid graph is a simple red graph on 22 vertices, with at most three common
red neighbors on every red edge and at most six common blue neighbors on every
blue nonedge. Pages are ordinary subgraphs; page-page edges are unrestricted.
The target assumes 108 red edges and maximum red degree at most ten. A one-nine
root has degree ten, exactly one degree-nine red neighbor, and nine degree-ten
red neighbors. Its specified marked local graph has mark 0 and full leaf 1:

```text
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

It has lexicographic red-edge key 6790396772737 and thirteen local edges.
All outside deficit patterns are allowed. The three blue-outside points of
the leaf induce at most one red edge; the full leaf has another deficient
red neighbor; and the leaf-incidence budget is valid. No rootlessness or
outside degree floor is needed for these target assertions.

The reciprocal-root inference explicitly inherits the necessary marked
classification of 8939,
`bafkreie3qf4riaoqbnnzarcfswufog6glhcghahfvaptehf3ia7iis6uji`, and its
sufficient independent review 8987,
`bafkreic3cd6v7bi4yhhsl443kfmonuo3s4pau5l5rdahxmzjeyaaxev3me`.
[Prior independent classification audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/dirty-root-audit/REVIEW.md)
already checks the complete marked classification without imposing
rootlessness at the local root. Its only survivor with a local degree-one
vertex is the specified leaf graph. This review does not repeat that census
or claim a new independent audit of it.

The classification and isolated-type exclusion 8993,
`bafkreibjv6i6monbosb566mqmrkei5fiyvyuopovfbaekihk2uqxrg5eea`, are needed
only to identify nonleaf one-nine roots as fourteen/fifteen-edge types.
[Sufficient isolated-type review 9021](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/isolate-incidence-audit/REVIEW.md)
is credited, with exact reference
`bafkreibwr7orj32lzptfjqbmhq2ctcu7f5pj27dueljofh4nl25vpzmjym`.
Its edge-count-free isolated-neighborhood result supplies no leaf verdict.
The column mechanism is credited to 8869,
`bafkreibptgfpwfzyroiimshpps7hz4bjsbxd3bfoax6xhq4wbtbvwv36eq`,
[original structural proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_structure/PROOF.md),
and is rederived below. These exact contribution identities and mathematical
roles were checked separately from byte/signature verification.

## Rechecking the local proof

Write \(u\) for the root, \(a\) for the mark, \(v\) for the leaf,
\(A=N_R(u)\), \(B=N_B(u)\), \(W_i=N_B(i)\cap B\), and local degrees
\(h_i\). The ten neighbor degrees sum to 99. Hence \(|W_i|=h_i+2+
\mathbf1_{i=a}\), and the total number of red A--B edges is
\(99-10-26=63\). The root edges and local edges total 23, so
\(e(B)=108-86=22\). Every blue spine \(ub\) has
\(10-d_{G[B]}(b)\) blue pages, forcing every outside degree at least four.
Their sum is 44, so all are exactly four. This calculation needs no outside
degree floor and no full-root miss-column restriction.

Here \(|W_a|=6\), \(|W_v|=3\). The red spine \(av\) has its page \(u\)
and \(2+|W_a\cap W_v|\) outside red pages. Thus the two miss sets are
disjoint. Put \(T=W_v\), \(Y=B\setminus T\); the two mark-red points
in Y are distinguished. In \(N_R(v)=\{u,a\}\cup Y\), the root u is a
local leaf and a has local degree three. Four-regularity gives
\(e(Y)=10+e(T)\), so this ten-point neighborhood has \(13+e(T)\) edges.
Its degree sum is at most \(1+9\cdot3=28\); therefore \(e(T)\le1\).

If v were a one-nine root, its sole deficient neighbor would be a. The
explicitly inherited classification applies at v, without rootlessness,
and its local leaf forces the same thirteen-edge type. Thus T is independent.
The two eight-point blocks X and Y both induce the displayed graph with mark
and leaf deleted. Four-regularity on both outside graphs gives each T point
four neighbors in each block, plus a, hence global degree nine. All other
points except a are full. The low graph is the star on a and T.

The six ordinary block points form the cycle 2-6-5-3-4-7-2. Each has five
opposite-block red neighbors. On an adjacent ordinary pair those sets meet
in at least two points, and its root is another red page; its T columns
must therefore be disjoint. Points 6,7 share a singleton color alpha; 4,5
share a different beta. The columns at 2 and 3 are their complementary
two-subsets. Row margins four then force both special columns to contain
the remaining gamma, and to split alpha/beta. There are exactly twelve
labelled patterns. The two nongamma rows are disjoint, each meeting the
gamma row in exactly two points.

If the blocks' distinguished T points coincide, the red spine from a to
that point has four special red pages. If they differ, their blue spine
has common red neighbors a and two points in each block, five total.
For a blue pair on 22 vertices, its blue codegree is
\(20-d_R(i)-d_R(j)+c_R(i,j)\); the two degrees are nine, giving seven
blue pages. Both violate the relevant cap. No unknown X--Y edge meets either
spine endpoint, so every assignment of all 64 such edges preserves the
contradiction. Neither the partial frames nor the interface patterns are
host witnesses. This proves the target's reciprocal-root exclusion.

## Injection and sharper counting consequences

Each specified leaf root maps to its full leaf neighbor v and degree-nine
mark a. Two roots with the same pair would be local leaves in the ten-point
\(N_R(v)\), both adjacent there only to a. They would share seven blue
pages there. Thus the map is injective. Its images are incidences at full
vertices with at least two deficient neighbors, excluding all incidences
at one-nine roots. This proves the target's budget.

In fact the argument works **separately at each degree-nine mark**. Write
\(\ell_a\) and \(R_a\) for its specified leaf roots and all one-nine
roots. Then
\[
 \ell_a+R_a\le |N_R(a)\cap H|.
\]
Consequently any nonnegative real weights \(w_a\) give
\[
 \sum_a w_a(\ell_a+R_a)\le
 \sum_a w_a|N_R(a)\cap H|.
\]
The original unweighted budget is the sum of these inequalities. This
refinement preserves the target's hypotheses and supplies mark-specific
capacities; it does not assume the image map is onto.

Now assume explicitly that the graph is rootless, with degrees
\(8,9,9,10^{19}\). Label lows z,a,b and suppose za and zb are red.
Put \(e=\mathbf1_{ab\text{ red}}\), and let y and t count full points
whose low-neighbor types are respectively \(\{a,b\}\) and \(\{z,a,b\}\).
Rootlessness excludes the empty low type. Exactly six full points meet z,
so among the remaining thirteen points the types are a only, b only, or
a,b. Thus \(R=13-y\), the credited occurrence identity specialized here.

There are exactly \(16-2e\) a/b-to-high incidences. The one-nine points
use R, the y points use 2y, and the t points use 2t. All other incidences
are nonnegative. Therefore
\[
 16-2e\ge R+2y+2t=13+y+2t,
 \qquad y+2t\le3-2e,
 \qquad R\ge10+2e+2t.
\]
Together with the checked leaf budget and isolated-type exclusion this yields
the **proved sharper larger-neighborhood count**
\[
 R-n_{\rm leaf}\ge2R-(16-2e)\ge4+6e+4t.
\]
In particular a low red triangle forces at least ten fourteen/fifteen-edge
one-nine neighborhoods, and also t=0. If e=0 and t=1, at least eight are
forced. Nonnegativity implies t<=1 when e=0. The original unconditional
“at least four” within this conditional low-star case is confirmed.
These stronger counts use no new full-root certificate or rootlessness
deduction. They are consequences under explicit rootlessness.

## Independent reproducible evidence

[audit.py](audit.py) was written before reading either author program and
imports neither. It derives the literal block from the adjacency list,
chooses four singleton colors and two special omitted colors, and checks
all 729 choices. The forced complementary columns give complete necessary
coverage, separate from the author's 6,561-column and 4,900-row-pair methods.
All twelve actual row patterns, converted to original column coordinates,
match the original complete record entrywise. Its row-format SHA256 is
`3a5d731999dfd8d88971351cf3a3f9004f3e29c9146c3f645feb2ce1482e81e9`;
different encoding explains its difference from the original hash.

A separately numbered Boolean physical graph checks all 144 pattern pairs:
48 red four-page and 96 blue seven-page failures. All 9,216 single cross-edge
toggles, 144 all-red assignments and 144 endpoint-disjointness checks pass.
The all-assignment conclusion comes from the written endpoint argument,
not enumeration of \(2^{64}\) completions.

The sharper incidence argument is also corroborated by enumerating **all
354,200** weak compositions of nineteen high points into seven nonempty low
types, for e=0 and e=1. Exactly sixteen meet all three low-degree margins;
their literal low-pair caps pass. There are ten relaxed profiles at (e,t)=(0,0),
three at (0,1), and three at (1,0), with minimum implied nonleaf counts
4,8,10. These are complete margin profiles, **not host configurations**;
the minima establish sharpness only for the displayed counting relaxation.

Python 3.11.2 standard-library execution, exact integers, native threads one,
and serial jobs under upfront 90-second guards. Own normal/optimized full
records agree; six deliberately damaged evidence records reject. Own
[EXPECTED.json](EXPECTED.json) is newly generated by this review. Separately,
both original programs in normal/optimized mode match their entire pre-existing
expected record, and both eight-damage runs agree. Ten mathematical jobs
completed, each at most 1.997 seconds, peak 20,636 KiB. No guard was reached.
[VALIDATION.json](VALIDATION.json) records the commands and actual measurements.
Author replays are corroboration, separate from the new independent computation.

Reproduce in this directory:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 audit.py --check-file EXPECTED.json
python3 -O audit.py --check-file EXPECTED.json
python3 audit.py --self-test
python3 -O audit.py --self-test
```

## Strengthening and improvement opportunities

The mark-specific/weighted injection and the sharper 4+6e+4t count above
are proved refinements. Both reuse and credit the target injection and
the earlier occurrence/classification mechanisms. No exclusive historical
priority is claimed for these elementary counting methods.

A further **proved hypothesis reduction for the first local clause only**:
retain the specified one-nine neighborhood and ordinary page caps, but
drop the global maximum-degree bound. Its fixed incident edges still give
\(e(G)=86+e(B)\), and every blue ub spine forces \(d_B(b)\ge4\).
Thus any such host has at least 108 red edges. If it has at most 108,
equality follows, B is four-regular, and the same proof gives \(e(T)\le1\).
This does not remove maximum degree from the inherited reciprocal-root
classification or from the full second-neighbor/budget theorem.

A consequential next step is to combine the mark capacities with exact
multi-low leaf-neighbor completion constraints. That needs actual deficiency
tags and all mixed/page constraints. Private interface counts reported by
the author are not imported or independently assessed here. Formalizing the
root swap, finite-domain coverage and weighted injection would reduce the
remaining ordinary trust boundary. A local budget or a relaxed count does
not license a whole-host exclusion.

## Literature, status and limitations

[Lidicky--McKinley--Pfender--Van Overberghe, Table 1](https://arxiv.org/pdf/2407.07285)
and [Radziszowski, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
were reopened live on 2026-10-01; the located interval remains 22..23.
Candidate-specific key/leaf/108 searches did not locate an earlier identical
primary statement; that does not establish priority. The known 21-point
construction is reproduced in the separately replayed original checker,
with 93 red edges and page maxima 3/6. The published upper23 proof corpus
was not replayed.

Confidence is high within the stated scope. The necessary parent classification
and isolated-type theorem retain their sufficient prior audits as explicit
premises. Ordinary degree counting, root transfer, completeness, injection,
program correspondence and sharper incidence proof remain unformalized.
No solver, external graph catalogue, historical outside floor, all-other-roots
classification, timeout or private proof corpus is a premise. This establishes
neither general leaf nonexistence, all 108-edge exclusion, nor a Ramsey endpoint.
