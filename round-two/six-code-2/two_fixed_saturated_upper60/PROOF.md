# Sharp saturated-fixed-point obstruction for A(18,6,5)

Actual author **six-code-2, researcher**, 2026-10-01.

Let F be a family of distinct five-subsets of an eighteen-point set, with
every two words intersecting in at most two points. Write r_v for the
number of words through v and lambda_uv for the number through both u,v.
Suppose an involution g preserves F, moves sixteen points in eight pairs,
and fixes exactly x and y.

**Theorem.** If r_x=r_y=20, then |F|<=60, sharply. The new computation
establishes the sharp60 bound when lambda_xy=4. The multiplicities0 and2
use the explicitly imported published bounds56 and60 below. Consequently,
any such code of size at least61 has at most one saturated fixed point.

This is an author-checked exact computational lemma with ordinary,
unformalized completeness bridges. Independent review is pending. It
does not determine the unrestricted packing number, nor the maximum with
only one saturated fixed point. The construction goal of70 remains open.

## Inputs

The [universal twenty-star audit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md),
review8323, `bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`,
source02c1569568854e575f8b176ea07d552737a7da84, gives two statements:
a quadruple pair packing on seventeen points has at most20 blocks; and
in a20-block packing an uncovered pair cannot join two replication5 points.

The author's [complete twenty-star carrier and positive fixture cover](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-code-2/free_involution_upper68/PROOF.md),
graph8720 `bafkreicxclg3upt7ppxmw2udcefdn2cqfxox7jr5ud7rjcyyxf3dcb234e`,
source69f2312bb468eb59b8ab3d8978fe19b3d86cf58a, covers **every**20-block
quadruple pair packing by23 literal fixtures. Its normalization finds
two replication5 points with the same uncovered high neighbor, produces
the nine-block K4,4-minus-diagonal carrier, and covers3060 deficit
assignments by108 actual relabeling cases. Two distinct exact cover
algorithms agree on all352 rooted packings, each positively mapped to a
fixture. Coverage, rather than historical novelty or pairwise
nonisomorphism of the fixtures, is the needed fact. That source's separate
free-involution upper68 is not applied to the present cycle type. The
generic carrier and its ordinary normalization proof are imported.
Independent review of this earlier author result is still pending.
The carrier's marked-star origin is credited to six-code-3 and
six-reviewer-5 in that source. The published marked carrier is graph8350
`bafkreigsaibox67ch5nagmc6cm225eg7sxfqfvmlcuot75cbi55vvtvwhi`;
this is an origin citation, while the generalized twenty-star cover is
the actual classification premise here.

For the final zero/two corollary we also import:

* [Pair multiplicity0 audit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_absent_pair_review1/REVIEW.md),
  review7747 `bafkreic5krg2bwpfeewirdhqq2vxs76xdkwmx2br7rtolhtb56vr55hsla`,
  sourcecf3cab455baeab79e0ba17dc9bf5e0bfb4f7f022: two saturated points
  of multiplicity0 imply at most56 words.
* [Pair multiplicity2 audit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_pair_two_review2/REVIEW.md),
  review8080 `bafkreie5zvwwz4ttdg35mmbiwxn4tdxx67wse7si7wyky4wxix2lir2ib4`,
  source33143b38349e8db1bb645770a98aac83438b4517: two saturated points
  of multiplicity2 imply at most60. Its (20,19,1) upper57 premise is
  explicitly imported from claim7825/review8026. The prior full upper57
  census is not rerun here; exact links and provenance are in
  DEPENDENCIES.json.

The default reproducer verifies all17 files of the pinned author source
and cold-replays that entire source, including its thirteen-file pinned
dependency checks, the three reviewed validators, and the known69 code.
Checking bytes and executable outputs does not replace the mathematical
normalization and imported proofs.

## Four fixed words through a saturated fixed point

Shorten the20 words through x to a quadruple pair packing Q on seventeen
points. It is preserved by g, whose action on this domain fixes y and
moves the other sixteen points in eight pairs. A point v has replication
rho_v<=5 because its incident quadruples use disjoint triples among the
sixteen other points. With d_v=5-rho_v, sum_v d_v=85-80=5.

A g-fixed quadruple cannot contain y: the remaining three points would
be a g-invariant odd subset of a fixed-point-free sixteen-set. The
quadruples through y therefore occur in pairs, so rho_y is even and
at most4; d_y is odd and positive. Every other deficit occurs twice,
on a moved point pair. Thus at most two moved pairs have positive
deficit, and at least six moved pairs have replication5 at both ends.

Every one of these six low pairs is covered, by the no-low-low-leave
input. If a quadruple contains the full pair {v,gv}, its image also
contains that pair. Pair uniqueness forces this quadruple to be g-fixed.
A fixed quadruple consists of exactly two full moved pairs. Distinct
fixed quadruples cannot share a full pair. There are therefore at most
four fixed quadruples, and covering six low pairs requires at least
three. Their number is even, since the20 quadruples are partitioned
into fixed blocks and orbits of size2. It is exactly four.

These four fixed quadruples use all eight moved pairs, each once, and
partition the sixteen moved points. Restoring x gives exactly four
g-fixed words through x. The same argument applies to y when r_y=20.

## Possible shared multiplicities and all rooted involutions

A word containing x,y has a three-point tail in the free sixteen-set,
so is not fixed by g. Such words occur in pairs. Their tails are
pairwise disjoint, because sharing a tail point would give intersection
at least3. Hence lambda_xy is even and at most floor(16/3)=5; its only
possibilities are0,2,4. The imported bounds settle0 and2.

For lambda_xy=4, root Q at x and mark its replication4 point y. Transport
Q to one of the23 fixtures using the actual positive point map from the
imported cover. The four shared tails T_i are disjoint triples. The
transported involution pairs these tails in one of three ways. Each tail
pair has six possible bijections, and the four remaining free points
have three matchings. This gives exactly3*6^2*3=324 actual involutions
for every possible replication4 mate. Here x and y are individually
fixed, unlike the swapped-center interface of the earlier theorem.

For each map we keep precisely those whose actual block images preserve
the fixture. Under actual supplied fixture point maps, conjugation
(y,g)->(p(y),p g p^-1) preserves this finite set. The program verifies
every transported map is present, every orbit is disjoint, and their
union covers all valid maps. A subgroup suffices for this cover; no
assumption that an unknown F has the fixture's full group is made.
The positive normalization sends x,y to16,17 and the eight moved
pairs to(0,1),...,(14,15), with every actual point image checked.

Only fixtures17,20,22 survive. They have respectively1,3,3 actual
mate/involution maps, each a single orbit, giving three rooted cases.
All other fixtures have zero surviving maps. The separate literal
checker also compares this entire finite map carrier with the supplied
actual point-group inventory. Its completeness uses the imported
fixture inventory and the explicit324-map argument above.

## Complete second-star enumeration

The twenty x-words include four shared xy words. The y-star needs sixteen
additional words. Exactly four are fixed words; each is y together with
two full moved point pairs. Those four words correspond to a perfect
matching on the eight moved-pair labels. The remaining twelve words
are six paired orbits. In each such orbit the two four-point tails are
disjoint: their intersection is even, and a two-point intersection
would repeat a pair in the shortened y-star.

The primary method tests all105 perfect matchings. Compatibility with
the actual x-words retains20,20,18 configurations for the three roots.
There are18 eligible fixed y-word candidates at each root, and108,120,120
eligible paired y-word candidates before imposing the fixed matching.
For each retained matching, it checks every paired row against it and
enumerates every increasing six-clique of the remaining compatibility
graph. The resulting36-word anchor is checked directly for word size,
distinctness, all intersections, g-invariance, and both degrees20.

The second method uses literal quadruple pair sets. It chooses the six
paired rows first, recursively excluding every already covered actual
pair, then covers the eight moved-pair labels with fixed words. At each
step it chooses the first uncovered label and branches over every
compatible two-label support. This different decomposition is complete:
every valid six-row selection occurs once, and every residual perfect
matching contains an eligible edge through the first uncovered label.
It does not call the primary Y-domain or clique search.

| Fixture | Fixed-first configurations | Literal six-row choices | Complete XY anchors |
| --- | ---: | ---: | ---: |
| 17 | 20 | 1581 | 15 |
| 20 | 20 | 2259 | 15 |
| 22 | 18 | 2227 | 9 |

The two methods agree on **every actual anchor**, not just these counts.
There are39 distinct36-word anchors in total. No heuristic or symmetry
assumption about their eventual completions is introduced.

## Complete residual packing graphs and sharpness

All further words avoid16,17 because both point-stars are already full.
The remaining sixteen-set has a free involution, so every five-word
orbit has size2. Scan all4368 five-subsets of that set. Retain a row
exactly when its two actual words are mutually compatible and are
compatible with every anchor word. Two rows are adjacent exactly when
all four cross-word intersections are at most2. Thus every completion
is exactly a clique, with size36 plus twice its cardinality.

The resource implementation separately starts from all8568 five-subsets
of the eighteen-set. There are416 triple-orbit resources and3416 internally
valid word orbits:56 fixed and3360 paired. A closed word orbit occupies
an entire actual triple orbit, so two rows conflict precisely when their
canonical resource sets intersect. This is an exact encoding, not an
extra condition. For every anchor the reproducer compares every
resource vertex and edge with the direct word-intersection graph.

The39 residual graphs have52--138 vertices. A Python proper-coloring
branch-and-bound algorithm finds all maximum cliques; independent C++
P/X pivot enumeration uses only a cardinality cutoff, rejecting any
larger clique reached. The color bound is valid because each greedy
color class is an independent set. Recursive neighbor restriction
preserves the clique invariant. Increasing/decreasing vertex selection
and removal cover every eligible extension. In the P/X method, standard
maximal-clique pivot coverage, together with its safe cardinality
cutoff, covers every maximal clique at or above the target. A clique
larger than the Python target therefore causes rejection, not success.
The two searches agree on every complete maximum family in every case.
Neither a guard, timeout, nor an incomplete search supplies an absence
verdict; all production cases return COMPLETE.

| Maximum anchor completion size | Number of cases |
| --- | ---: |
| 54 | 1 |
| 56 | 20 |
| 58 | 8 |
| 60 | 10 |

Hence all multiplicity4 codes in the stated symmetry/saturation class
have at most60 words. witness.json supplies60 actual words from
fixture17, matching0, case3. The direct literal pairwise checker verifies
weight5, distance at least6, invariance under(0 1)...(14 15), fixed
points16,17 with replications20 each, and pair multiplicity4. Together
with the imported zero/two bounds this proves the theorem sharply.

## Status, historical comparison and reproduction

The classical point bound is Brouwer's
[1975 report](https://ir.cwi.nl/pub/6883/6883D.pdf). The established69
construction is [Aw--Chee--Ling2003, Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf).
The maintained [primary table](https://aeb.win.tue.nl/codes/Andw.html),
refreshed2026-10-01, still lists69--72; the campaign's separately reviewed
upper71 remains context. The present theorem changes neither endpoint.
Bounded concept searches and the committed graph refresh did not locate
this specific two-fixed saturated theorem; no historical-priority claim
is made for the witness or the exact local fixture count.

Run reproduce.py as documented in README.md. All calculations are exact
integer/set operations. Eleven positive, corruption and incomplete-status
controls include all64 four-vertex graphs at every clique cardinality.
Normal, optimized and sanitized cold runs check every new case; their
metrics are recorded in VALIDATION.json. Generated anchors, graphs,
maximum families, binaries and logs stay outside the source bundle.

Trust boundaries are the ordinary normalization, involution-carrier,
fixed-word and search-completeness arguments, CPython/GCC, the same
author's two implementations, and the named published premises. This is
not a formal proof or an independent peer verdict. The default run
replays the full prior twenty-star proof; its transitive upper57 premise
remains an explicitly imported result.
