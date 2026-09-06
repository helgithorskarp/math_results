# Ramsey(5,5;43) forbids substitution blocks even after exceptional attachments

Let G be a simple graph on43 vertices with no clique and no independent set
of order5. Then:

1. Every induced subgraph on at least36 vertices is **prime**: it has no
   module M with 2 <= |M| < |V(H)|.
2. Every induced subgraph on at least28 vertices has **no proper module of
   size at least3**. Size2 modules are not excluded at this order.
3. Every pair has at least8 outside distinguishing vertices. Every triple
   has at least17, and a monochromatic triple has at least18.

A module is a vertex set M such that each vertex outside M is adjacent to
all of M or to none of M. A vertex **distinguishes** M if its contacts to M
use both colors. Statements1 and2 equivalently concern any deletion of at
most7 or15 vertices, respectively. The exceptional vertices and all their
incident edges are arbitrary. No automorphism, group action, degree
profile, chosen core graph, catalog, or Ramsey43 existence assumption is
part of the *excluded construction family*.

This is a universal structural obstruction to exceptional extensions of
substitution constructions, not a target graph or an improved Ramsey
number bound. The proof below is finite and analytic; executable evidence
checks its arithmetic and extracts a physical monochromatic five-set from
any supplied member of the stated family. No historical priority or
sharpness in actual Ramsey graphs is claimed.

## Small Ramsey inputs and local bounds

Use red for edges and blue for nonedges. We use only the classical upper
bounds R(3,3)<=6, R(3,4)<=9, R(3,5)<=14, R(4,4)<=18, R(4,5)<=25 and
R(2,s)=s, R(1,s)=1. Their earlier proofs are imported, not recomputed here.
In a hypothetical G, in either color:

* every degree lies between18 and24: a neighborhood has no same-color K4
  or opposite-color K5;
* a same-color edge has at most13 common neighbors of its color;
* a same-color triangle has at most4 common neighbors of its color.

For the second fact,14 common neighbors give a triangle of that color or
an opposite K5. For the third, the common neighborhood contains no edge
of that color, so five of its vertices would form an opposite K5.

## Pair and triple signature identities

For an internally red pair u,v, write a for the number of common red
neighbors and D for the number of outside distinguishing vertices. Every
such vertex contributes exactly one red contact. Thus

    D = d_red(u) + d_red(v) - 2 - 2a >= 18+18-2-26 = 8.

The internal color of any pair can be renamed red, so this covers all pairs.

For a red triangle Q, let a be its common red-neighbor count and D its
number of distinguishers. The sum of the three red degrees is at least54.
Internal edges contribute6, uniform red contacts contribute3a, and each
distinguishing vertex contributes at most2. Therefore

    54 <= 6 + 3a + 2D <= 18 + 2D,
    D >= 18.

For a nonmonochromatic triple, rename colors and vertices so its red edges
are01 and02 and its blue edge is12. Let C01,C02 be the common red-neighbor
counts and C12 the common blue-neighbor count. No third vertex of the triple
is counted in these three quantities. For each outside vertex with red
contact bits x0,x1,x2, the literal identity

    x0*x1 + x0*x2 + (1-x1)*(1-x2)
      = 1_{x0=x1=x2} + x0

holds. Summing over the40 outside vertices gives

    C01 + C02 + C12 = (40-D) + (d_red(0)-2).

All three common-neighbor counts are at most13. Consequently

    D >= d_red(0)-1 >= 17.

These are direct physical identities, not assumptions about realizability
of a signature-count relaxation. `bounds.py` checks all8 triple and4 pair
signatures. It also records two integer count vectors meeting the elementary
triple inequalities at17 and18. Those vectors specify no edges among the
outside vertices; they are **not graphs or Ramsey feasibility witnesses**.

## A module capacity table

Let H be any (5,5)-good induced subgraph, M a proper module, and
k=omega(H[M]), l=alpha(H[M]). Neither exceeds4. Partition H-M into its
red-uniform part A and blue-uniform part B. Put

    c(1)=24, c(2)=13, c(3)=4, c(4)=0.

Joining a maximum monochromatic clique in M to one in A or B proves

    |A| <= c(k),  |B| <= c(l),
    |M| <= R(k+1,l+1)-1.

No value of R(5,5) is needed: if k=l=4, then A=B=empty, contradicting
properness. The case k=l=1 has |M|=1 and is not a nontrivial module.
The remaining cases, up to color reversal, are:

| (k,l) | maximum module order | red-uniform cap | blue-uniform cap | maximum core order |
|---|---:|---:|---:|---:|
| (1,2) | 2 | 24 | 13 | 39 |
| (1,3) | 3 | 24 | 4 | 31 |
| (1,4) | 4 | 24 | 0 | 28 |
| (2,2) | 5 | 13 | 13 | 31 |
| (2,3) | 8 | 13 | 4 | 25 |
| (2,4) | 13 | 13 | 0 | 26 |
| (3,3) | 17 | 4 | 4 | 25 |
| (3,4) | 24 | 4 | 0 | 28 |

The maxima are upper bounds, not assertions of simultaneous attainment.
In particular |H|<=31 for a proper module of size>=3, and |H|<=28 for
one of size>=6. Equality28 in the latter statement forces, up to color
reversal, |M|=24, (k,l)=(3,4), |A|=4 and B=empty.

## Coupling the module with the exceptional vertices

Write T=V(G)-V(H). Every distinguisher of a subset Q of M belongs either
to M-Q or to T; every vertex of H-M has uniform contacts to Q.

If |T|<=7 and |M|=2, the pair bound8 is impossible. If |M|>=3 then
|H|>=36 contradicts the module table's bound31. This proves statement1.

For statement2 suppose |T|<=15 and |M|>=3.

* For |M|=3, the triple bound17 exceeds |T|.
* For |M|=4, choose any triple Q in M. It has at most |T|+1<=16
  distinguishers, again too few.
* For |M|=5, sum the distinguishing counts over all10 triples Q in M.
  The triple lemma requires a sum of at least170. Vertices of M contribute
  at most20 in total. Any outside vertex has at least three contacts of
  one color to M, so it fails to distinguish at least one triple and
  contributes at most9. Vertices of H-M contribute0. Thus

      170 <= 20 + 9|T| <= 155,

  a contradiction. In fact this calculation forces |T|>=17 for a size5
  module, since even20+9*16=164<170.
* For |M|>=6, |H|>=28 and the table force the sole equality case above.
  Thus |M|=24 and the four vertices A are all red to M. Each already has
  red degree24, so the global degree upper bound forces every edge within
  A and between A and T to be blue. T has15 vertices. Any vertex of T,
  together with all four vertices of A, is a blue K5.

All cases contradict the Ramsey hypothesis. The equality case is why the
bound extends from14 exceptional vertices to15; merely reading the table
would not justify that extra step. The proof also gives the separate
size3 threshold16 exceptions (17 for a monochromatic triple), which the
extractor accepts.

## The complete construction family

The extractor accepts a graph on43 vertices and disjoint sets M,T with
2<=|M|<43-|T| and M a module of G-T. It covers the union of:

* |T|<=7, any such M;
* |T|<=15, |M|>=3;
* |T|<=16, |M|=3; or |T|<=17 with M monochromatic.

All internal edges of M and of the rest of the core are arbitrary, as are
all edges touching T. Cross contacts from a core vertex to M must be
uniform, but different core vertices choose their colors independently.
For fixed labeled M of size3 and T of size16 this leaves

    choose(43,2) - (3-1)*(43-3-16) = 855

free edge bits, hence exactly2^855 excluded labeled graphs in that one
subfamily alone. This count makes no claim about a disjoint union over
different embeddings, and no maximality claim about the covered family.
The whole family has no imposed automorphism of G. It is not an assertion
that arbitrary Ramsey43 candidates contain a module after these deletions.

## Physical certificates and reproduction

`extract.py` validates the supplied family membership. Its exact bitset
clique search first exploits low degrees or excessive same-color edge/
triangle common neighborhoods. It then checks the module capacities and
the24-plus4 equality case. Every result consists of five literal vertex
labels and a color. A violation of an imported small Ramsey bound produces
a hard error, never a feasibility verdict.

`verify.py` imports no extractor, table, graph catalog, solver or small
Ramsey result. It reconstructs a dense Boolean adjacency matrix and checks
all ten physical pairs of the supplied five-set. Family membership is
unnecessary for this certificate check. The guaranteed success of extraction
on every admitted input rests on the displayed universal proof.

Input fields are exactly `n:43`, sorted distinct `red_edges` with0<=u<v<43,
and sorted distinct vertex lists `module` and `deleted`. No other implicit
edges exist: omitted pairs are blue. `fixture.json` is an expressly
non-Ramsey graph demonstrating the triangle-common-neighborhood branch.

With Python3.11.2, standard library only, run:

```sh
python3 -B reproduce.py
python3 -B extract.py fixture.json
python3 -B verify.py fixture.json fixture_certificate.json
```

Expected full status: `REPRODUCED_MODULE_RESILIENCE_PACKAGE`. The full run
checks every manifest hash and compares all outputs byte-for-byte in both
normal and assertion-disabled Python. Controls check130 deterministic
full-family graphs (both colors and permuted labels), every graph on five
vertices against literal clique enumeration in both colors and all five
clique sizes (10,240 comparisons), and rejection of10 malformed/wrong-family
inputs and6 corrupt certificates. The130 fixtures exercise the degree,
edge-common and triangle-common extraction branches; they do not constitute
exhaustive coverage of all extractor branches or graphs. The remaining
branches are justified by the proof and inspected source. No peer review
or proof-assistant formalization of this result is claimed.

Only `compare.py` has a repository-relative input: the21 packed graphs in
`../ramsey_r55_c5_semidirect_c8_cayley_obstruction/novelty_fixtures.json`.
Its SHA-256 is recorded in `comparison.json`. It computes all903 pair and
12,341 triple distinguishing counts per saved graph. All saved graphs pass
the new local bounds, including the known two- and seven-defect graphs.
These checks do not establish whole-family isomorphism separation, search
basin novelty, or Ramsey feasibility; the broader module family is not
recognized automatically. Finding M,T is outside the extractor's interface.
The proof and physical extractor require none of these comparison fixtures.

## Provenance and limits

The small Ramsey inputs are classical: Greenwood--Gleason,
[*Combinatorial Relations and Chromatic Graphs*](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/combinatorial-relations-and-chromatic-graphs/BF0DEBC881488344266BCD77CBBCD86B),
and McKay--Radziszowski,
[*R(4,5)=25*](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The [Angeltveit--McKay paper](https://arxiv.org/html/2409.15709v2)
also states the general degree window n-25<=d<=24. These are imported
theorems; the historical computations for R(4,5) are not replayed here.

An early live search returned an indexed prior statement on `kenan.works`
that every (5,5)-good graph of order at least40 is prime. The underlying
page could not be retrieved (HTTP502 and DNS failure), so it is recorded
as an unresolved priority lead, not a verified proof source or a dependency.
We explicitly claim no novelty for that weaker theorem or for the standard
module-capacity argument. The contribution supplies the stronger
deletion-resilience statements, the mixed-triple identity, their coupled
proof and executable physical certificate route. Limited searches do not
establish historical priority for those refinements either.

The earlier sparse-motion involution/order-three theorem uses the same
classical local caps. Its numerical motion bounds are not reproved as new
here; the present statements impose no automorphism and treat arbitrary
exceptional attachments. The independently accepted Cayley40 obstruction
is different campaign context, not a premise. No Cayley or switching ladder,
catalog extension, global degree-profile exclusion, or parked solver is
reopened. The17-class/9,153-label residual symmetry frontier is not claimed
smaller. No graph below seven defects or43-vertex Ramsey graph is produced.
