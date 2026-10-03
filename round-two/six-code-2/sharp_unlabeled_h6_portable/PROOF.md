# Sharp unlabeled-cap profiles on four fixed-parent image families

Author: **six-code-2**, researcher. Complete ordinary author proof and exact
author certificates; ordinary restriction, restoration, gluing, incidence,
label/link and transport bridges remain unformalized. Independent-person review
is pending; historical priority is unclaimed. Reader-facing source is this directory; the mathematical claim states its exact source commit and graph references.

Fix $V=\{0,\ldots,16\}$, $y=17$ and the literal 68-parent Steiner partition
$D\subset\binom V5$ in `PARENT.json`. Its SHA256 is
`32e66195e3252e2a50a2d6c55ed7d9af9a8693e7f7121276aeca1474f80c3758`.
Every triple of $V$ occurs in exactly one parent, physically checked. Decimal
masks encode subsets; bit $v$ denotes point $v$.

Let $F\subset\binom{V\cup\{y\}}5$ have pairwise word intersections at most
two. There is exactly one noncontained four-tail, $Q=\{0,1,2,3\}$ (mask 15),
and $Q\cup\{y\}\in F$. Every other word containing $y$ has its four-tail
contained in a parent of $D$. Put $R=D\setminus F$, and let $P\subset R$
be the represented parents of these contained tails. In each declared case,
the exact empty-parent set is

$$
H=R\setminus P=\{61,334,32907,81927\}\cup\{E_1,E_2\},
$$

where the two extras are one of the four pairs in the table below. The four
fixed parents are precisely the $Q$-triple blockers. There is no restriction
on optional contained tails or other retained parents. A represented parent
has exactly one tail, since two different four-subsets meet in three points.
With $a=|P|$ and $s$ new caps in $\binom V5\setminus D$, $|R|=a+6$ and

$$
|F|=68-(a+6)+a+1+s=63+s.
$$

Each cap $C$ meets $Q$ in at most two points and every nonempty parent in at
most three. If $|C\cap B|=3$ for $B\notin H$, that parent must be removed
and represented by a tail $B\setminus\{p\}$ with $p\in C\cap B$. The tail
must meet $Q$ in at most one point. Required tails meet each other in at most
one point. The complete core carrier lists every cap and every assignment of
all its required tails. The independent physical MRV audit reconstructs the
complete zero/nonzero prefixes and every assignment key.

Two cores are adjacent exactly when their distinct caps and required tails
are mutually compatible. Identical tails can be shared; different tails of
one parent are incompatible. Every packing restricts to an $s$-clique.
Conversely, a clique glues to a packing by removing $H$ and its represented
parents, then adding its caps, assigned tails with $y$, and $Q\cup\{y\}$.
Optional tails can be restored to their parents without changing size. This
restriction/restoration does not classify all optional tails or equality codes.

The fourth literal case, extras `4808,6440`, has 2,187 prospective caps,
1,581 zero-core caps, 6,400 cores, and 26,447 edges. Its physically complete
census has 28,368 triangles, 13,642 four-cliques, 2,594 five-cliques, two
six-cliques and zero seven-cliques, in 1,607,504 incidence states. The original
known neighbor 33 has $s=6,a=18,|R|=24$; original and normalized 69-word
packings pass all 2,346 pairs and 690 triples. The generic coloring routine
uses **seven** colors in this case and is not used to prove the sharp bound
69. The separate parent-label certificate below supplies a positive proper
**six**-coloring, checked on every physical edge. Thus the fourth literal
boundary has sharp maximum 69, also certified by the complete seven-clique
census and the elementary fact that any larger clique contains a seven-clique.

For any cap, at most one parent meets it in four points: two such parents
would share at least $4+4-5=3$ points, contrary to the Steiner partition. Such
a parent must be in $H$, since it can neither be retained nor own a compatible
four-tail. Label a core by this unique empty parent if it exists; otherwise
the core is **unlabeled**. Two caps with the same label share at least three
points. Consequently the labeled subgraph has a proper coloring by $H$.

The four complete graphs have independent unlabeled induced subgraphs. Every
unlabeled core's entire neighbor set uses at most two parent labels. These are
physically verified hypotheses on these cases, not assumptions on unseen h6
boundaries. Giving each unlabeled vertex a parent color missing from its
neighbors extends the proper six-coloring. A clique containing an unlabeled
vertex has that one unlabeled vertex and at most two labeled neighbors, hence
at most three caps. More generally independence and at most $k<h$ neighbor
labels imply $\omega(G)\le\max(h,k+1)$.

The new full-link checker determines when the three-cap bound is attained.
For every unlabeled vertex it exhausts every set bit in its complete graph
row and every pair of its neighbors. It recomputes each candidate pair's
compatibility from literal cap and required-tail point sets, agrees with both
directed graph bits, and saves every full link. The earlier physical carrier
and every-row graph audits are explicit pinned dependencies; this new check
does not regenerate their completeness proofs.

| extras | unlabeled cores | all candidate link pairs | triangles with an unlabeled core | sharp maximum words with an unlabeled cap | all-cap labeling forced from |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1432,33572 | 1,121 | 74 | 2 | 66 | 67 |
| 2258,51234 | 1,020 | 32 | 8 | 66 | 67 |
| 2258,57608 | 1,014 | 48 | 4 | 66 | 67 |
| 4808,6440 | 936 | 26 | 0 | 65 | 66 |

Unlabeled independence makes every counted triangle have exactly one unlabeled
vertex. Because its neighbors use at most two labels, the first three cases
have exact maximum three caps in a clique containing an unlabeled vertex. In
the fourth case the absence of any link edge forbids such a triangle. Active
unlabeled vertices do exist, so its exact maximum is two caps. Formula $63+s$
therefore gives the displayed upper bounds.

Every bound is attained by a saved original-coordinate packing: three
66-word packings and one 65-word packing. Each has an explicitly unlabeled
cap, the exact prescribed $Q,H,t=1,h=6$ boundary, distinct weight-five words,
and all pair/triple conditions checked (2,145 pairs/660 triples for size 66;
2,080 pairs/650 triples for size 65). The complete link/witness packet is
233,481 bytes, SHA256
`c2b2ca79b7d95412c3a6c712f6374d4de14b482fc0b109d96846ecf660fd9559`.
It and the entire exact result agree byte for byte in normal and optimized
Python. The earlier merely sufficient maximum-degree-five gate remains a
preserved failed route on the first case; its six-neighbor exception does
not invalidate these full neighbor-label and link results.

It follows that every packing of at least 67 words in any of the four cases
labels all its caps injectively by empty parents. In the fourth case this
already holds from 66 words. The positive witnesses prove these thresholds
are sharp. Every 69-word packing has six caps in bijection with the six empty
parents. Each labeled cap is $(B\setminus\{p\})\cup\{x\}$ for its unique
$B\in H$, $p\in B$, $x\in V\setminus B$.

The credited four actual $D/y$-fixed generators yield 16,320 point maps. Each
map is physically checked on all 68 parents, all six holes and $Q$. The
four image families have respectively 16,320, 8,160, 8,160 and 8,160 distinct
boundaries. Exact boundary keys are $(Q,E_1,E_2)$, the first three fields of
each saved target row; the fourth field is a representative-map index and
is excluded. All projected domain hashes match the independent physical
point audits. The four domains are disjoint, giving **40,800** boundaries,
20 extra pairs per each of the 2,040 noncontained $Q$'s. No full automorphism
order or minimal-orbit assumption is used. Point transport preserves the
parent labels, packing, exact empty set and unlabeled positive witnesses.

Thus maximum 69 and cap rigidity from 67 hold on all 40,800 boundaries. The
sharp unlabeled maximum 66 holds on the first 32,640; the sharp maximum 65
and stronger cap rigidity from 66 hold on the last 8,160. At $Q=15$, the
fourth family's extras are `[4808,6440], [5204,28708], [38146,77954], [53761,71697]`.
Four of ten retained seed pairs are covered; six remain unrun.

The original 69-word code is credited to
[Aw, Chee and Ling, Theorem 1/Appendix A](https://ymchee66.github.io/home/PDF/6cwc.pdf).
Its exact reproduction is validation. The freshly opened
[maintained table](https://aeb.win.tue.nl/codes/Andw.html) still lists 69–72.
The new results are conditional structural profiles, not a new known69
construction or an unrestricted endpoint. Review9657 and peer P23 results
do not supply a verdict on these new proofs.

All sixteen new mathematical children completed successfully with native
threads one, serial jobs, unchanged 1CPU/2GiB and original 60-second,
2,000,000-state/60-second-child guards. No earlier carrier/graph/census was
rerun; the new link property uses their retained complete graphs. Nine
validated research files remain unchanged. Sixty new semantic damages
were rejected. No timeout, UNKNOWN, kill, incomplete guard or escalation.
The adjacent replay regenerates the complete carrier, every-row graph, census,
parent labels, full unlabeled links, original positive packings and actual
point-image domains from compact literal fixtures. Whole prior expectations
are checked, with explicit execution-hash normalization. This reproduction is
validation, not another discovery. The fifth literal pair `4808,18708` remains
wholly unrun.
