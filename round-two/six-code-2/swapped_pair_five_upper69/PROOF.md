# Sharp 69 at a swapped saturated pair of multiplicity five

six-code-2, role researcher. 2026-10-01. Author-checked exact computation
and ordinary unformalized proofs; independent review of this result and
historical priority are unassessed.

## Statement and context

Let F be a family of distinct five-subsets of an 18-element set V, with
|A intersect B| <= 2 for distinct A,B in F. For p,q in V put
r_p=|{A in F:p in A}| and lambda_pq=|{A in F:p,q in A}|.
Suppose an involution g preserves F, has eight transpositions and two
fixed points, and exchanges u,v with r_u=r_v=20 and lambda_uv=5.
Then **|F| <= 69**. The explicit construction below attains 69 under these
hypotheses and admits an order-four symmetry h with h^2=g.

This is a restricted theorem. It neither bounds all families preserved by
this cycle type nor improves the unrestricted 69-word lower record.
Aw, Chee and Ling, *Six New Constant Weight Binary Codes*, Ars Combinatoria
67 (2003), Theorem1/AppendixA, already give A(18,6,5)>=69:
[primary paper](https://ymchee66.github.io/home/PDF/6cwc.pdf),
[literal code](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69).
The [maintained table](https://aeb.win.tue.nl/codes/Andw.html) was freshly
checked on 2026-10-01 and still records 69..72; campaign upper71 is separate
prior work. The classical derived bound A(17,6,4)=20 appears in Brouwer,
*A(17,6,4) = 20 or the nonexistence of the scarce design SD(4,1;17,21)* (1975):
[primary report](https://ir.cwi.nl/pub/6883/6883D.pdf).
Both classical baselines are reproduced literally here.

## Imported generic 20-star coverage

Shortening the u-star removes u from its twenty words, yielding twenty
quadruples on seventeen points intersecting pairwise in at most one point.
The imported generic classification says this is point-isomorphic to one
of 23 fixtures. Its finite source is the generic part of
[free-involution source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-code-2/free_involution_upper68),
commit 69f2312bb468eb59b8ab3d8978fe19b3d86cf58a,
graph8720 `bafkreicxclg3upt7ppxmw2udcefdn2cqfxox7jr5ud7rjcyyxf3dcb234e`.
The preceding free-involution upper bound is not a premise here.

Independent generic classification review8933,
`bafkreic2wb2z6reycvrsrywbgjxdtjl5f7eqkbe2yk2xtco2su6tgn43aq`,
confirms fixture completeness and the actual full point-group fibres,
conditional on reviewed structure8323,
`bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`.
Sources:
[classification review](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-5/twenty-star-classification-audit),
commit 0509c3808f44b45fd3c333a10cf36bd329003450;
[structural review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md).

The present package includes byte-pinned copies of the fixtures, reviewed
all-root normalizer, native search kernel and reviewed EXPECTED data.
`groups.py` replays all literal automorphisms, compares both orders and
entrywise digests to the reviewed output, and verifies their actual action.
It does not rerun the whole earlier classification proof. The dependency
is an explicit imported mathematical premise, not an inference from a
hash or from unfilled legacy group fields.

## All actual involutions at the exchanged pair

Relabel the star center u as 17. Eligible mates v occur in exactly five
quadruples. The five common words have the form {u,v} union T_i, where
the five three-tails T_i are disjoint: otherwise two common words would
intersect in at least three points. Their union uses fifteen of the sixteen
other points. The unique complement point is fixed by g, since g exchanges
u,v and permutes the five tails.

The induced involution on five tails has an odd number of fixed tails.
Each fixed three-tail has an odd number of fixed points. Only one fixed
point is available after the complement point, so exactly one tail is fixed;
it contains one fixed point and a transposition. The other four tails form
two exchanged pairs. Every g is therefore determined by a fixed tail (5),
its fixed vertex (3), a matching of the other tails (3), and bijections
between the two tail pairs (6^2). There are exactly **1,620 actual maps**
per eligible mate, with no duplicate maps.

`carrier.tail_maps` generates exactly this product. The separate
`point_maps` pairs the first available point, propagating tail-image
domains; it checks all completed actual permutations and agrees entrywise.
All 302 eligible mates in all 23 fixtures are covered: **489,240 raw maps**.

For each map, the u-star determines the v-star by g. Each has twenty words
and their intersection consists of the five common words, so their union
has exactly 35 words. The only additional packing tests are literal
intersections between their private words. Exactly **6,334 compatible
unions** survive. Fixtures15/20/22 have none in this specified domain.

The actual fixture groups act on pairs (v,g) by (p(v),p g p^-1).
`quotient.py` partitions the complete valid carrier by this action and
records an actual eighteen-point transport for every valid map. Literal
words and conjugacy are checked for each transport. There are **619 rooted
cases**, not necessarily 619 full isomorphism classes. `evidence.py`
separately verifies exact coverage-key equality, every transport and every
root normalization against the complete labelled inventories.
Full group maximality is unnecessary for the reduction: an actual
automorphism subgroup plus complete positive coverage suffices.

## Exact completion reduction and two upper searches

For each rooted union relabel u,v to 0,1, the other transpositions to
(2,3),...,(14,15), and the two fixed points to16,17. This is checked
pointwise as a conjugacy to the standard involution.

Any further word avoids0,1, since the full two stars are already present.
It belongs to a whole g-orbit of one fixed word or two exchanged words.
Include an orbit exactly when distinct words within it and all its words
against the anchor intersect in at most two points. Fixed words are
eligible: no word is tested against itself. Two eligible orbits are
adjacent exactly when every pair of cross words meets in at most two points.
Thus complete invariant extensions are precisely cliques in this graph,
with vertex weight equal to orbit size (one or two).

The triple-resource model (`model.py`) and a separate literal-set orbit
enumeration agree entrywise on every residual vertex and edge of all619
graphs. `weighted.py` computes exact maximum weights with integer
branch-and-bound. Its proper coloring partitions any candidate pool into
independent classes. A clique takes at most one vertex from each class,
so the sum of class maximum weights bounds it. Ordered prefix bounds
are recomputed within a partially exposed class; reverse branching visits
each candidate as the largest remaining vertex. Pruning uses only these
valid upper bounds and an already checked positive clique. A finite
complete return is required; a guard returns no optimum or absence claim.

A different upper encoding in `native.py` reconstructs literal eligible
word orbits and replaces a weight-w vertex by w mutually adjacent true
twins. Whole twin sets across distinct orbits are joined exactly when the
literal words are compatible. Any clique can be enlarged to contain all
twins of every represented orbit. Therefore the ordinary maximum clique
size of the expanded graph equals the maximum weighted orbit sum.

For each of the619 cases, the separately written, previously reviewed
native fixed-target kernel is asked for a clique of size one larger than
the weighted producer's positive value. Every native search completes
with no such clique. Expanded graphs have108..240 vertices, within the
unchanged256-vertex implementation domain. Every positive lower witness
is checked against the anchor and all literal word intersections.
This independently checks each finite upper value through a different
encoding/search, but does not constitute independent peer review of this
new theorem. Compiler/runtime correctness and the ordinary reductions
remain trust boundaries.

The largest residual weight is34, hence |F|<=35+34=69. Distribution of
maximum full code sizes across the rooted cases:

| Size | Rooted cases |
| ---: | ---: |
| 58 | 2 |
| 59 | 3 |
| 60 | 11 |
| 61 | 8 |
| 62 | 28 |
| 63 | 7 |
| 64 | 45 |
| 65 | 9 |
| 66 | 22 |
| 67 | 2 |
| 68 | 475 |
| 69 | 7 |

Roots14/26/30/143/182/280/552 attain69. These are not asserted to be seven
inequivalent codes or an enumeration of all maximum families.

## General one-cap Steiner transfer

Let S be a Steiner S(3,5,v), and let C be a five-set meeting every block
of S in at most three points. Exactly ten distinct blocks B meet C in
three points: each triple of C has one parent, and two such triples cannot
have the same parent without that parent meeting C in at least four points.
For each parent choose a_B in B intersect C. Assume the four-tails
Q_B=B minus {a_B} meet pairwise in at most one point. For a new point Y,
define

F = (S minus those ten parents) union {C} union {{Y} union Q_B:all parents B}.

The family has |S|+1 distinct five-sets. Retained old blocks meet C in at
most two points. They meet each replacement in at most two, inherited from
the old Steiner packing. Each replacement meets C in exactly two points.
Two replacements meet in their common Y and at most one tail point.
Old-old intersections are at most two. This proves the transfer lemma.
No priority claim is made for the general trade operation.

## Explicit order-four symmetric 69 construction

`steiner.py` regenerates the classical S(3,5,17) as the images of
P^1(GF4) under PGL(2,16). All4080 projective maps are covered by the
affine and normalized fractional forms in the source. GF16 has polynomial
X^4+X+1; its GF4 subfield is {0,1,6,7}. Encode
subfield[x]+alpha*subfield[y] by 4*y+x, with alpha=2 in the polynomial
representation. Point16 is infinity and point17 is new Y.
The generated68 blocks cover all680 triples of the old seventeen points
exactly once; the derived AG(2,4) star and g-closure are checked literally.

Take C={0,1,4,5,16} and the following ten parent omissions:

| Parent B | Omitted a_B |
| --- | ---: |
| 0,1,4,9,10 | 0 |
| 0,1,5,8,11 | 1 |
| 0,4,5,13,14 | 5 |
| 1,4,5,12,15 | 4 |
| 0,1,2,3,16 | 16 |
| 4,5,6,7,16 | 16 |
| 0,4,8,12,16 | 0 |
| 1,5,9,13,16 | 1 |
| 1,4,11,14,16 | 4 |
| 0,5,10,15,16 | 5 |

The trade certificate is checked against every actual classical parent,
the tail condition, and the literal69 words in WITNESS69.json. The
standalone `check_witness.py`, importing no carrier/generator/search code,
checks all2346 word pairs, the involution g(v)=v xor1 for v<16 (fix16/17),
closure, r_2=r_3=20 and lambda_23=5. There are five g-fixed words.
The degree profile10^1 19^5 20^12 differs from the reproduced specified
ACL69 profile12^1 18^2 19^3 20^12, so these two certificates are not related
by a coordinate permutation. Inequivalence to every previously known69
code and historical novelty are not asserted.

The code is preserved by **h(z)=z^4+alpha**, fixing16/17. Since
alpha^4+alpha=1, h^2(z)=z+1=g(z). Literal word images and the actual
permutation are verified; h has cycle type4^4 1^2. This supplies sharpness
and a compact positive seed with an order-four symmetry.

`steiner_trade.py` closes only the following narrow construction family.
There are24 g-fixed nonblock five-caps containing infinity. Each has two
fixed parents forced to omit infinity and four paired parent orbits, each
with three omission choices, hence81 choices per cap and1944 total.
Exactly96 choices retain all ten distinct pairs of C, and16 satisfy the
full tail compatibility condition: eight caps with two each, sixteen with
none. They give16 distinct labelled codes.

`field_family.py` checks every one of the64 actual maps z -> z^(2^e)+b,
e=0..3, b in GF16, fixing16/17. These maps form a group, preserve the
Steiner plane and commute with g. Their images of the displayed code are
exactly those16 trade codes. The stabilizer within this64-map group is
{identity,g,h,h^3}, cyclic of order four; the full automorphism group is
unclaimed. Thus this is one group orbit of16 labelled codes, not16
inequivalent codes or a classification of every69 construction.

## Reproduction and trust

Use the cold commands in README.md. EXPECTED.json was frozen from preceding
complete experiments and records stable per-fixture counts plus digests of
all actual maps, positive coverage, upper/lower readouts and construction
families. Generated corpora are reconstructed locally. Digests compare
evidence, while the ordinary completeness bridges above and terminating
exact searches justify the quantified claim. Both normal Python and -O
must produce the identical full record; all guards use explicit exceptions.
The sanitized replay checks all619 native cases, not a selected sample.

Author controls compare weighted search with literal brute force on1099
small graph/weight cases and the native kernel with exhaustive five-vertex
graph/target cases (6144). Fifteen deliberate damages independently reject
missing coverage maps/roots/native cases, false transports, an incomplete
producer, duplicate or wrong-weight words, fixed centers, false degrees,
wrong parent omissions and each corrupt pinned input. These controls do
not replace coverage proofs or external independent review.

The only imported upper-bound mathematical premise is the generic23-star
classification, with its reviewed structural dependency. The explicit
69 construction and transfer lemma are standalone. No unrestricted new
bound, full involution-family bound, formalized theorem or independent
review verdict for this contribution is claimed.
