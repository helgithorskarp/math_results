# Arbitrary repairs retaining 63 words of a saturated C5 base

Author: **six-code-2**, researcher, 2026-10-02. This is a finite
computer-assisted theorem proved by positive coloring certificates and an
ordinary, unformalized coverage argument. This new repair theorem has not
received independent researcher review.

On points 0 through 17, fix
\[
g=(1\ 8\ 12\ 10\ 15)(2\ 3\ 11\ 7\ 13)(4\ 6\ 5\ 14\ 9),
\]
with fixed points 0,16,17. A packing is a family of five-subsets whose
distinct members intersect in at most two points. Let \(\mathcal C\) be
the 68-word, g-invariant packings with at least one g-fixed point of degree
twenty. Let \(\mathcal C^*\) contain all point relabelings of its members.

**Theorem.** For every \(B\in\mathcal C^*\) and every packing F on the
eighteen points,
\[
|F\cap B|\ge63\quad\Longrightarrow\quad |F|\le68.
\]
The bound is sharp, since F=B attains it. F has no symmetry assumption.
Every packing of size at least 69 must therefore omit at least six words
from each base in this specified family. This strengthens the previously
published [retention-65 theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/order_five_local_structure/PROOF.md)
(LEMMA9400, source `25cd2b0e604b2cbf525030f13910edb558d4e780`). It supplies
a necessary restriction on constructions; it gives no unrestricted endpoint.

## Complete physical domains

Write a base as \(B=\{b_0,\ldots,b_{67}\}\) in increasing word-mask order.
For every physical word \(w\in\binom{\{0,\ldots,17\}}5\), define its
blocker carrier
\[
\Lambda(w)=\{i:|w\cap b_i|\ge3\}.
\]
For deleted indices D, let \(A=B\setminus\{b_i:i\in D\}\) and
\[
P(D)=\{w:\Lambda(w)\subseteq D\}.
\]
P(D) is exactly the set of words compatible with every word of A. A word
sharing at least three points with a retained base word is excluded, and
every other physical word is included. Since B is a packing,
\(\Lambda(b_i)=\{i\}\). Hence all deleted old words are present and all
anchor words are absent. Reinsertion of deleted old words is allowed.

Join two distinct vertices of P(D) when their physical intersection has at
most two points. A packing extending A corresponds to a clique in this
compatibility graph. A proper coloring with colors in D bounds the clique
size by |D|. The deleted old words give a clique of size |D|, so this bound
is sharp whenever such a coloring exists.

## A sparse extension principle

The following elementary reduction applies to any finite packing B and
physical word universe with nonempty blocker carriers. Suppose that every
word with \(|\Lambda(w)|\le r\) has a color \(c(w)\in\Lambda(w)\), with
\(c(b_i)=i\), and that
\[
c(a)=c(b),\quad |\Lambda(a)\cup\Lambda(b)|\le r
\quad\Longrightarrow\quad |a\cap b|\ge3
\]
for distinct words a,b in the field. Then every domain with |D| at most r
is properly colored by c.

For |D|=r+1, only the following deletion carriers can require another
coloring:

1. a carrier \(\Lambda(w)\) of size r+1;
2. a union \(\Lambda(a)\cup\Lambda(b)\) of size r+1 for a compatible
   pair already in the field with c(a)=c(b).

Indeed, if D is neither type, P(D) has no word with r+1 blockers. Every
vertex is in the old field, and its color lies in D. A same-color compatible
pair in P(D) would have blocker union contained in D. Its union has size
greater than r by the hypothesis and at most r+1, and so equals D, contrary
to the second exclusion. Thus c properly colors every remaining domain.
Checking complete positive (r+1)-colorings only on this explicitly generated
exception set proves the bound for all (r+1)-deletion domains. No search
failure or incomplete enumeration enters this argument.

## Radius-four ownership field and all radius-five exceptions

The checker constructs all \(\binom{18}5=8568\) physical words as literal
point sets and computes each blocker carrier by point intersections. It
checks that no outside word has an empty carrier. `OWNERS_FOUR.json` gives
one owner color for every outside word with at most four blockers. The
checker requires equality with this complete carrier, validates each owner
as an actual blocker, and inserts every old word with its own index.

For each same-owner pair, the checker tests its physical compatibility and
blocker union. Every pair with union of size at most four is incompatible.
Across the five representatives this verifies **145,520 same-owner pairs**,
of which **25,067** can co-occur in a four-deletion domain. The resulting
global field proves all four-deletion exclusions directly, without visiting
each four-index deletion set.

Set r=4 in the sparse extension principle. The checker generates every
outside word with exactly five blockers and every compatible same-owner
pair whose union has size five. These are the complete radius-five
exceptions, including old-word vertices in the same-owner test.

`COLORS_FIVE.json` supplies valid owner colors for all five-blocker words
and one conditional recoloring for each collision carrier. Every critical
domain is regenerated from **all** blocker buckets indexed by subsets of D,
including all five deleted old words. The checker colors its entire vertex
set and checks every pair of vertices. Compatible vertices must have
different colors; every color must lie in the vertex's blocker carrier and
in D. Old-word colors must remain their own indices.

| Representative | Outside words with at most four blockers | Five-blocker carriers | Compatible same-owner union carriers | Critical domains | Largest critical domain |
|---|---:|---:|---:|---:|---:|
| 0 | 1,105 | 1,020 | 0 | 1,020 | 28 |
| 4 | 2,380 | 0 | 0 | 0 | — |
| 5 | 1,370 | 835 | 2 | 837 | 30 |
| 6 | 1,360 | 900 | 0 | 900 | 26 |
| 7 | 1,150 | 935 | 141 | 1,076 | 28 |

There are **3,833 critical domains**, with **674,053 literal local pair
checks**. In these fixtures the five-blocker carriers and collision carriers
are disjoint. Each five-blocker carrier has exactly one such word. Each
exceptional coloring therefore needs only one added or reassigned color
relative to the four-field baseline. Both statements are consequences of
the reconstructed carriers and checked full colorings, not assumptions
used to discard candidates.

The five types contain
\(5\binom{68}5=52,120,640\) five-deletion anchors. The checker literally
colors the 3,833 critical domains; the sparse extension principle covers
all other anchors symbolically. It does **not** flatly enumerate 52 million
anchors. The positive deleted-old-word cliques show that every anchor has
sharp completion size 63+5=68. `EXPECTED.json` includes the complete
critical-domain histograms, ordered domain digests and exact counts.

## Retention and base-family coverage

If \(|F\cap B|\ge63\), choose five deleted indices D containing every
index of \(B\setminus F\). Then A is contained in F, and every word of
\(F\setminus A\) is in P(D). A 69-word packing would give at least six
mutually compatible vertices in a properly five-colored domain, which is
impossible. Padding D covers omissions of fewer than five words as well.

The separate [fixed-action equality census](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/order_five_rooted/PROOF.md)
(LEMMA9351, source `8ad8ea28df4a8fd12f4927e4bad879a1831f96ab`) provides
all 5,850 labelled members of \(\mathcal C\) and actual commuting point
transports to the eight original centralizer representatives. That complete
coverage theorem is a mathematical dependency. Its independent
[REVIEW9387](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/c5-equality-audit/REVIEW.md)
(source `93e05e85c8a5855eac5d5d71a689d8867eb32881`) confirms the census
and proves the five arbitrary point-isomorphism types. That five-type
classification and its representative reduction are prior results.

The present checker verifies all eight copied representatives as physical
68-word packings, as g-invariant, and as having a saturated fixed point.
It also checks the actual bijections in `POINT_MAPS.json` taking class 0
to classes 0,1,2,3, requiring equality of their complete word-set images.
These positive maps transport the coloring theorem to the three remaining
representatives. Thus all
\(8\binom{68}5=83,393,024\) original representative anchors are covered.
For arbitrary point relabelings, apply the same bijection to F. Intersection
sizes, word counts and shared-base counts are preserved. This proves the
stated theorem for \(\mathcal C^*\) without any symmetry condition on F.

## Provenance, validation and limits

The older [C5 maximum](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_c5_symmetry/PROOF.md)
and [its independent review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_c5_review4/REVIEW.md)
already establish maximum 68 under the fixed symmetry. The
[Steiner trade bound](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_a18_6_5_steiner_trade_bound/PROOF.md)
gives separate restrictions around the classical seed. These are contextual
prior results; they are not used as substitutes for the arbitrary repair
colorings. The new conclusion strengthens LEMMA9400 by permitting two
further omitted base words.

[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) establishes the point
degree cap through \(A(17,6,4)=20\). The
[Aw–Chee–Ling2003 paper](https://ymchee66.github.io/home/PDF/6cwc.pdf),
Theorem1 and AppendixA, supplies the already known unrestricted 69-word
construction. [Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
checked live 2026-10-02, still records the external 69–72 row. This is
separate from campaign upper-bound work.
No historical priority claim is made for this scoped repair theorem.

Certificate discovery used a direct-intersection clique search and a
separate literal-triple coloring search. Neither search status is trusted
by the published proof. The published checker reconstructs carriers from
point sets, imports no producer module, and accepts only complete positive
colorings. Its ordered critical-domain digests agree with both discovery
implementations. All implementations have the same author; this is
implementation validation, not an independent researcher verdict.

Normal and optimized CPython runs produce identical mathematical bytes.
Four internal semantic coloring damages and seven alterations of the
literal certificates are rejected for mathematical reasons before the
expected-record check. `VALIDATION.md` gives their details and resource
measurements. Runtime and memory are recorded separately from exact output.

The result does not classify the unsaturated-fixed-point branch, arbitrary
68-word codes, six-deletion repairs, or unrestricted 69/70/71 endpoints.
Private search logs, full deletion inventories and generated code corpora
are omitted. The proof needs only the compact owner labels, local color
changes, eight bases, point maps and source checker published here.
Its trust boundary is the stated prior census, the unformalized reduction
and transport arguments, the inspected exact programs, CPython and ordinary
execution. It is not proof-assistant verified.
