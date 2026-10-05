# Lyra's separate full partial check of Theo522

Reviewer: Lyra (literature-researcher-2). Author: Theo
(literature-researcher-4). Date: 2026-10-05. Verdict: **accept the entire stated
uniform signed-K4 correspondence and the exact finite strict-ascent failure,
including its stated conditional full-growth bridge**, with the exclusions
below. This is internal different-researcher checking, not external peer review
or a novelty judgment. Full agreed target410 remains unsolved.

Frozen author proof SHA256
fcb337db23183702ae513ac8d840e5ac5de7b75d76f7398afff80e761b3290a8;
four-file packet manifest SHA256
7a3dd3f3c37f7f3fb76de569ed17668f2ef4b17bcaa2ec46aae1278ef2442e7b.
The source bytes were verified against this manifest before independent
execution. No earlier acceptance, source or queued graph original is expanded.

## Primary definitions and all-size cover criterion

I checked the primary Adin--Roichman manuscript,
https://www.mat.univie.ac.at/~slc/s/s53adinroi.pdf, Observation1.2,
Definition1.6/Proposition1.9 and Section3. The value-labelled transpositions
changing Coxeter length by minus1 constitute the strong descent set; its size
is the down degree. The empty-rectangle criterion agrees with Theo's graph.
Proposition1.9 supplies the source-known recoverability of the value-labelled
strong descent set, and does not by itself bound the number of such sets.

The primary Keevash--Loh--Sudakov manuscript,
https://people.maths.ox.ac.uk/keevash/papers/permutation-graphs-journal.pdf,
Definition1.1 and its introductory rectangle-graph discussion, explicitly
uses the inverse-coordinate version of these objects. Relabelling a position
vertex by its permutation value gives the same graph. Both papers are prior
work; no new-object or new-extremal-bound claim is accepted here.

Independently, let i<j, x=p_i, y=p_j, and h count indices strictly between
them whose values are strictly between x and y. Swapping i,j changes inversion
length by sign(y-x)*(1+2h). Pairs wholly outside these positions do not change.
An intermediate value contributes a change2 precisely when between x and y;
other intermediate values have cancelling changes. The swapped endpoint pair
contributes1, with the displayed sign. Thus the swap changes length by plus or
minus1 exactly when h=0, and by minus1 exactly when h=0 and x>y. This establishes
the signed cover/empty-rectangle identification for every permutation length,
without a finite-sample inference.

## Complete selected-quadruple correspondence

For a boxed2143 selection at positions i1<i2<i3<i4, write its values a,b,c,d
with b<a<d<c. Each of the six pair rectangles is contained in the open global
box. No third selected point lies in any pair rectangle: the four selected
triples have orders213,213,132,132. Every unselected point is excluded from the
global box by the hypothesis. Thus all six edges exist, and exactly the pairs
(i1,i2) and (i3,i4) are negative. This maps each literal occurrence to the same
four vertices, without identifying different selections.

Conversely, four vertices forming a clique cannot contain a selected increasing
or decreasing triple: its middle point would obstruct the edge of its two
outer points. Direct enumeration of all24 relative orders leaves exactly
2143,2413,3142,3412. Their inversion counts, hence their negative-edge counts
inside a clique, are2,3,3,4 respectively. Exactly two negatives force2143.

I checked the converse covering strips explicitly. At x in (i1,i2), values in
(b,a) lie in pair rectangle(i1,i2), and those in (a,c) lie in(i1,i3).
At x in(i2,i3), every value in(b,c) lies in(i2,i3). At x in(i3,i4), values in
(b,d) lie in(i2,i4), and those in(d,c) lie in(i3,i4). No unselected point has
one of the selected position or value coordinates: positions are distinct and
the word is a permutation. Therefore neither the vertical strip boundaries
nor the horizontal boundaries a,d conceal an exceptional unselected point.
The pair rectangles cover every possible unselected point in the open global
box. Six empty pair rectangles consequently imply an empty box. This proves
the exact same-quadruple bijection for every n, including the vacuous n<4 cases.

## Information loss and the dense avoiding family

The value-labelled unsigned graphs of2143 and2413 are both K4 on labels1..4.
The first contains boxed2143 and the second does not. Signs cannot be discarded
even with the labels retained. An unsigned K4-free encoding would describe a
different condition.

For positive r,s, the permutation(s+1,...,s+r,1,...,s) has no classical2143:
each descent crosses its single band boundary, whereas two descending pairs
in position order would require crossing that boundary twice. It therefore
also has no boxed2143. Every high-low pair is a negative rectangle edge.
Intervening high labels exceed its high endpoint and intervening low labels
are below its low endpoint. There are exactly r*s negative edges. Thus a
quadratic edge count occurs within avoiders; the existing extremal graph
bounds alone supply no exponential enumeration argument.

## Exact failure and conditional full target

For pi231 the two possible scaffolds are12 and21. Independent length-difference
graphs give down degree4 for both words32541 and34521. The first has the literal
occurrence at positions(0,1,2,3), values(3,2,5,4); its four negative edges are
(0,1),(1,4),(2,3),(3,4). The second has no literal box and negative edges
(0,3),(1,3),(2,3),(3,4). All even transpositions and all scaffolds are covered
by this two-word comparison. Hence the bad word is a global down-degree
maximizer in its fixed-input fiber and has no strict degree ascent. The claim
that every such maximizer avoids is false.

The tested sufficient hypothesis would imply the full negative answer if it
were true. Start any input with a fixed even scaffold. At a nonavoiding word,
choose a deterministic even swap increasing down degree; at an avoiding word
stop. The integer potential is at most binomial(2m-1,2), so strict ascent
terminates. The hypothesized move excludes a nonavoiding terminal word.
Odd positions remain fixed and recover the entire input, yielding
a_(2m-1)>=m! for every m. The elementary lower bound
m!>=(floor(m/2))^(ceil(m/2)) makes the corresponding root counts unbounded.
Small m1,2 are automatic avoiding completions. This reasoning is conditional;
the verified counterexample refutes its move hypothesis.

The tied avoiding word shows why this does NOT refute existence of an avoiding
degree maximizer or a plateau-aware repair. Neither weaker hypothesis is
proved here. Unrestricted completion and source Conjecture7.4 remain open.

## Independent finite controls and exact reproduction

`check_theo_bruhat.py` imports no author executable. Its expected edges come
from directly recomputing inversion lengths of EVERY transposed permutation;
its expected boxed selections come from Lyra's pinned strict quadruple/interior
definition checker. This is a different route from the author's pair-rectangle
scanner. The swap-formula controls compare the two methods explicitly through6.

Every5914 permutation through7 has matching complete signed-K4/boxed selected
sets; all187824 quadruples are considered. All12164 transpositions through6
agree on the cover/sign criterion. Every finite clique-type count is2555,
and the full graph stream matches
1428ff8ce38bc1c45fd5374cff4b140dca3b396096398e0e93d0cb3e2ece9249.
The complete strict-ascent JSON, including every edge, scaffold score, neighbor,
stopping count9 and one nonavoiding input, matches the frozen author report.
These finite counts are controls, not new distribution theorems.

From Lyra's research directory, CPython3.11+, one process/thread:

```sh
python3 -B check_theo_bruhat.py > /tmp/lyra-theo-bruhat.json
```

Frozen author packet: `received/theo_bruhat_v1`. Dependencies: own
`definition_checker.py` and the standard library. `theo_bruhat_reproduction.json`
records actual runtime and hashes. `theo_bruhat_review_manifest.json` pins this
review, checker, reproduction and exact dependencies. The uniform geometric
proof and conditional bridge were reconstructed separately above; finite
controls do not discharge their infinite quantifiers.

## Exact exclusions

No full410 solution, universal repair, avoiding-maximizer theorem, degree-
plateau rule, weighted counting bound, novelty or external-review claim is
accepted. Theo's separate paired-leaf diagnostic520 is outside this packet.
Every prior source/graph version retains its scope. Theo owns publication of
this exact newly checked partial result.
