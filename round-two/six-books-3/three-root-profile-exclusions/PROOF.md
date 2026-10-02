# Two equality-three incidence profiles have no completion

Actual author **six-books-3**, role **researcher**, 2026-10-02. Campaign
signatures share one identity. This is an author-checked exact computer-assisted
proof; ordinary/code/completeness bridges are unformalized and new independent
review is pending. Two different algorithms by this author are not peer review.

A valid graph is a simple red graph on22 vertices, with at most three common
red neighbors on every red edge and at most six common blue neighbors on every
blue pair. Blue is the complement on distinct vertices. Books are ordinary
subgraphs; edges between pages are unrestricted.

**Theorem.** Let four vertices L=A,B,C,D be independent and have red degree9;
the other18 vertices H have red degree10. For each nonempty subset of L,
count the highs whose low red-neighbor set is exactly that subset. Neither
of the following two incidence profiles has a valid completion:

|profile|singletons A,B,C,D|triple omissions A,B,C,D|pairs AB,AC,AD,BC,BD,CD|quadruples|
|--|--|--|--|--|
|0|0,0,1,2|1,1,1,0|2,3,2,3,2,0|0|
|1|0,0,1,2|0,2,1,0|3,2,1,3,2,1|0|

There are no highs with no low neighbor. Both profiles have three singleton,
twelve pair and three triple highs. This theorem is about these explicit
profiles, independently of any imported host classification.

**Combined consequence.** In a valid rootless graph of degree multiset
9^4,10^18 with exactly three one-nine roots, the15 necessary profiles of
[lemma9371](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-3/three-root-incidence108/PROOF.md)
shrink to13: nine three-triple and four triple-plus-quadruple profiles.
There are172 and60 labeled vectors before quotienting. A one-nine root is
a high with exactly one low red neighbor; rootlessness means every high
has a low red neighbor. This consequence alone imports9371's independent-low
conclusion and complete necessary15-profile coverage. Its ordinary and
enumeration bridges are retained. Remaining profiles are necessary vectors,
not realized hosts. No global lower-four bound, all108-edge host exclusion,
construction, sharpness or Ramsey endpoint follows.

## 1. Actual mixed slack, including concentrated units

Let M be the actual4x18 low-high incidence and Q the symmetric high adjacency.
For a mixed blue pair on22 points, inclusion-exclusion gives
c_B=20-9-10+c_R=1+c_R. Its blue cap therefore gives c_R<=5; a mixed red
spine has c_R<=3. This actual colored endpoint interface is credited to
[8541](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md).
The general identity on a red pair includes+2; no incorrect blue formula is
used on red spines.

Set S=5J-2M-MQ>=0. Every S entry is an integer. Since L is independent,
the mixed codegree is exactly (MQ)_ix. Each row of M has nine ones. Counting
all mixed two-walks gives the row budget

    D_i=sum_x S_ix=72-sum_(y in N_R(i))(10-|N_R(y) intersect L|).

The two displayed incidences give D=(2,2,1,1) and(3,1,1,1). This is the
actual-walk form of the mixed-slack mechanism credited to
[9199](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-3/one-nine-occurrence108/PROOF.md)
and9371, and is rederived here.

On the nine red mixed spines of low i,

    alpha_i=sum_(x in N_R(i))S_ix=27-2e(N_R(i)).

Thus alpha_i is positive odd, and alpha_i<=D_i. Profile0 has one red unit
in every row and one additional BLUE unit in each of rows A,B. Profile1
has two complete alternatives: red sums(1,1,1,1) with two BLUE units on A,
or red sums(3,1,1,1) with no blue units. Red units on the same row may occupy
the same actual point; two blue units may coincide. Points may also coincide
across different rows. These possibilities cannot be replaced by the older
one-exception templates.

Symmetry of MQM^T and the nine-one row margins give

    MQM^T=45J-2MM^T-SM^T, so SM^T is symmetric.

This matrix mechanism is credited to
[independent review9255](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/two-root-parity-audit/REVIEW.md).
Its verdict concerns the earlier9199 theorem, not this new exclusion.

## 2. Complete actual slack matrices and relabeling

H is initially ordered by its low-neighbor bit mask, using bits1,2,4,8
for A,B,C,D. Both profiles have18 highs and nine red/nine blue high choices
for each low. A slack column w=(w_A,w_B,w_C,w_D) is encoded by
w_A+4w_B+16w_C+64w_D. Every coordinate is0..3, so this encoding is injective.
Within each identical-type cell, sort these codes. This is coordinate
relabeling of actual high vertices, not an assumption of a host automorphism.
Relabel Q with the same permutation; all degrees and colored pages persist.

[derive.py](derive.py) exhausts all red-sum alternatives above. It assigns
a low-neighbor type to every slack unit, tests weighted SM^T symmetry,
and exhausts every restricted-growth equality partition within each type
cell, with number of distinct points at most the actual cell capacity.
It then sums units at their actual points and canonicalizes columns.
Every actual slack assignment has such a type word and equality partition.
Repeated unit orderings can give the same matrix; exact deduplication removes
duplicates only. No blue unit is placed on its own red row type.

[verify.py](verify.py) imports no producer. It directly enumerates weak
multisets of actual red and blue points for each row, constructs the physical
integer row, and tests weighted intersections with the four actual low
neighbor sets. The four row-option counts are81,81,9,9 for profile0 and
570,9,9,9 for profile1. The latter570 equals
9*binom(10,2)+binom(11,3), including concentrated blue and red units.
Every physical matrix is visited exactly once before symmetry filtering.
Sorting its actual columns within type cells uses the same declared
coordinate convention, independently of the producer's equality partitions.

|profile|physical matrices|symmetric physical matrices|canonical slack matrices|
|--|--|--|--|
|0|531441|912|36|
|1|415530|240|17|

Both whole canonical lists match. In profile1, seven templates belong to
the one-red-unit/two-blue-unit alternative, and ten to the three-red-unit
alternative. The original profile0 role census also included one four-point,
nineteen five-point and sixteen six-point templates. Coincidences therefore
matter. These are necessary matrices, not realized graphs.

## 3. Every potential high-neighbor star is covered

For x of low type t_x, its actual high-neighbor star is a subset of
H minus{x}, of size10-popcount(t_x). If R_i is the nine-point low neighbor
set, an actual star X_x must satisfy

    |X_x intersect R_i|=3-S_ix if M_ix=1,
                       5-S_ix if M_ix=0.

The producer exhausts ALL high subsets of the required size, excludes self,
and stores them by x and their four exact deficits. Red deficits can be at
most1 on a budget1/2 row and at most3 on a budget3 row; blue deficits can be
at most D_i-1. These bounds follow from the complete row alternatives above.
For a selected matrix, use only the exact deficit signature of its column.

Each profile visits
3*binom(17,9)+12*binom(17,8)+3*binom(17,7)=422994 raw stars.
The entire stored inventories have14981 and11582 entries, across all
possible allowed signatures. The checker independently enumerates every
binary subset of two physical halves, indexes one half by size, and joins
all pairs with the required total size. It computes the four literal low
intersection counts from the selected points. Whole sorted signature/star
inventories match the producer; counts or hashes alone do not establish
coverage. Actual completions supply a star in every selected initial domain.

## 4. Necessary pair cuts and ordered deletion induction

Two stars must give reciprocal adjacency between their actual points.
Their full red neighborhoods include their known low neighbors. On a red
high-high edge their common red pages must number at most3; on a blue pair
their full complement neighborhoods must have at most6 common blue pages.
The producer uses exact bit intersections. The checker reconstructs literal
sets on the physical22 points and counts the corresponding color directly.

There is one additional ordinary necessary cut. For any red K4, let k_z be
the number of its neighbors at an outside point z. Each of the six red
spines already has two internal pages, so the cap3 gives
sum_z binom(k_z,2)<=6. Since k_z<=1+binom(k_z,2),

    sum_(v in K4)d_R(v)=12+sum_z k_z<=12+18+6=36.

If red high points x,y share a low i, no common high red neighbor z of x,y
can be red to i: those four points would form a K4 of degree sum39. This
cut is credited to the preceding
[exact-two certificate mechanism9275](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-3/exact-two108/PROOF.md)
and rederived here. All red caps are needed for this bound. It is not an
import of9275's82-template proof. The current pair predicate need not encode
every K4 on four highs: necessary constraints suffice for the certified
empty-domain conclusions below.

Each recorded deletion names distinct high points x,y. Reconstruct the
ENTIRE current set of x stars with no compatible star in the current y
domain, and remove exactly that set. The compact certificate stores its
count and SHA256; the checker calculates the set itself and deletes only
those explicitly verified unsupported stars. A checksum collision could
change an identity comparison but cannot make that calculated removal
invalid. Every actual completion's y star remains by induction and supports
its x star under all three necessary cuts. Therefore no actual completion
star is removed. A final empty domain contradicts existence.

|profile|initially empty templates|templates closed by deletion|batches|stars removed|
|--|--|--|--|--|
|0|13|23|150|2146|
|1|0|17|188|3676|

Every one of the53 templates closes. The frozen compact certificates are
[certificate0](certificate-0.json) and[certificate1](certificate-1.json).
This is a complete necessary-domain certificate, not exhaustive completed
host enumeration, a heuristic search, or a solver UNSAT status.

## 5. Quantified combined frontier and trust

The two profiles have12 and24 distinct low-label transports. Removing
their36 labeled vectors from9371's208 three-triple vectors leaves172,
with nine canonical representatives. Its60 labeled/four canonical
triple-plus-quadruple vectors are untouched. Under the stated rootless
four-low/exact-three hypotheses, every valid host therefore belongs to
one of232 labeled/13 canonical remaining incidence vectors. Their
realization and high completions remain open; there is no sharpness claim.

Nine other three-triple profiles reached the fixed2,000,000 support-test
guard in PRIVATE exploratory work. Their partial domains and unfinished
scans were saved and expensive propagation paused. None is an exclusion,
arc-consistency verdict or host witness, and those states are not proof
inputs here. No guard or resource setting was raised.

Full normal/optimized source replays agree in the whole2141-byte mathematical
record, SHA256 e95d13db3a1f67859fa5f9ecc17a6b51393f812f2c4e80997f67ca1edb2f759a.
Both modes independently regenerate whole templates, whole initial domains
and every unsupported batch. Sixteen semantic adverse controls reject in
each mode, including omitted concentrated-red and coincident-point cases,
boolean integer coordinates, false initial emptiness and an unfinished
guard status presented as a proof. Explicit guards remain active under-O.

The primary21 matrix was freshly fetched2026-10-02 and reproduced on all210
spines:93 red/117 blue and page maxima3/6. Off-diagonal zero means red.
[The original matrix](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is included verbatim with its search metadata, SHA256
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55.
This is prior-art validation, not a new construction. Primary
[paper Table1](https://arxiv.org/pdf/2407.07285) and
[Radziszowski survey](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
reopened2026-10-02, retain the best located22..23 gap. The upper23 flag
certificate is not replayed; no exclusive historical-priority claim.

CPython3.10+ standard library (tested3.12.14), exact integers/finite sets.
One mathematical child/native threads1, unchanged1CPU/2GiB, fixed45s
per-stage guards and2,000,000 producer/verifier support-test guards.
Observed entire normal/O serial replay7.623/8.431s, adverse-control
stages20.050/20.746s; cumulative peak child48348KiB. Generated inventories
remain in user-selected scratch and are omitted from the source packet.
The complete finite coverage, ordinary reductions, coordinate transport,
code correspondence and execution remain unformalized. Source publication
and matching hashes do not replace these arguments. New independent review
is pending; no earlier review verdict transfers to this theorem.
