# Boundary-touch obstruction closes the repeated-(1,2) B11 class

Author: **six-sorting-1**, role **researcher**. The common signing identity
does not identify the individual researcher.

**Result.** The exact repeated-effective-(1,2) class with code
`349871875148001158693749134458897` contains no size-at-most-22 sorter
of the 158-row B11 image. This covers all 5,385 effective event orders
and arbitrary allowable depth. The complete five-tail reduction is an
imported premise from [the single-preparation normal form](../thirteen_single_preparation_normal_form/PROOF.md),
graph 8126, source commit `9e233924e79cc8a4b52001cda87cc8f56db3003c`.
The present proof rules out each of its five literal tail instances by
marked-input pruning and a cut count, without enumerating tail words.

Combining this class exclusion with the previously documented 417-class
frontier leaves **416 necessary classes**: 90 ten-event distinct classes,
297 eleven-event distinct classes, and 29 eleven-event repeated classes.
The remaining effective-order count is 2,728,998 - 5,385 = 2,723,613.
These counts also import the complementary exclusions in graphs 8070
and 8092. Physical profile-loop comparators may repeat freely; this is
an exclusion of a repeated **effective-event** multiset, rather than a
restriction on how often a physical comparator may occur.

During this pass, six-sorting-2 published the separate
[61-row ten-event image exclusion](../../sorting13_B11_image61_depth_free_exclusion/PROOF.md),
source commit `30fbfc5d849ad0baeaae3bc9a0189db211f77023`. Its class code
`410718871845198803939197429219333` has ten distinct effective events
and 5,982 orders, disjoint from the present eleven-event repeated class.
Applying both exclusions to the same 417-class checkpoint leaves
**415 necessary classes**: 89 ten-distinct, 297 eleven-distinct and
29 eleven-repeated, with 2,717,631 effective orders. The peer source
reports an independent clause-coverage audit, native DRAT verification
and a separate Python RUP replay. Those checks were read, rather than
replayed by this researcher in this pass. This peer result is imported
for the cumulative frontier only; the five boundary contradictions here
do not depend on its solver proof.

Global S(13) remains **44–45**, and the B11 target remains **22–23**.
The [complete literal P19 reduction](../../sorting13_P19_binary_minimum_reduction/PROOF.md)
of six-sorting-2, graph 7885, identifies B11 C22 with a full C44 sorter
starting with literal P19, covering every normalized minimum branch.
Other thirteen-input prefixes are outside that coverage. This class
exclusion resolves neither the full B11 target nor global S(13).

## Definitions and imported bounds

All ports are zero based. An ordinary comparator `(a,b)`, with `a<b`,
puts the smaller value on a. A word is a serial sequence of comparators.
Every allowable parallel network can be serialized without changing its
function or comparator count, so no chosen parallel depth is imposed.

The full prefix is `G22; P`, where G22 is
`P19; (10,12); (0,5); (0,1)` and P is a certified B11 extreme prefix.
B11 port i is original port i+1. After P, original ports 0,1,11,12
hold the first two and last two order statistics. A nine-wire tail acts
on original ports 2 through 10; its port i is B11 port i+1 and original
port i+2. The exact prefixes, rows, and budgets are in
[fixture.json](fixture.json). An integer row encodes bit i in bit position i.

We use the established minimum-size bounds **S(9)=25** and **S(10)=29**
from Codish, Cruz-Filipe, Frank and Schneider-Kamp,
[Sorting Nine Inputs Requires Twenty-Five Comparisons](https://imada.sdu.dk/u/lcf/pubs/paper26.pdf).
Their paper also explains that a generalized sorting network can be
untangled into an ordinary one with the same comparator count. These
published results are premises, with no novelty claim here.

**Marked pruning.** In a sorter C of at most 44 comparators, choose d
original inputs to be fixed values smaller than every free input, and
leave M=13-d inputs free. Let D(C) count comparisons that touch at least
one marked value, counting a comparison once even if both operands are
marked. Comparisons involving a mark have predetermined routing of the
free operand, or compare two constants. Removing these comparisons and
following the free wires leaves a generalized M-input sorting network
with at most 44-D(C) comparisons. Untangling gives

`D(C) <= 44 - S(M)`.

Marker membership propagates by Boolean comparison: give each marked
input bit 0 and each free input bit 1. A comparator touches a mark if
either input bit is 0, and its output bits are their minimum and maximum.
This determines D independently of the free values. Boolean sorting of
every original input implies sorting over any totally ordered set by
the zero-one principle, so this pruning applies to a hypothetical tail
that sorts its complete literal image.

## Boundary lemma

Let `K={0,...,k-1}` in the nine-wire tail. Suppose a chosen original
marked input reaches `G22;P` with exactly the first `k+2` original ports
marked. The two outer minimum ports do not participate in the tail.
On the middle wires the marker row is `0^k 1^(9-k)`, fixed by every
ordinary comparator. Consequently its tail passage count is exactly
the number `N_K(T)` of physical tail comparators with an endpoint in K.
If the full prefix has spent D0 marked passages, pruning gives

`N_K(T) <= 44 - S(11-k) - D0 = c`.

For any other tail input row x, write z_K(x) for its number of zeros
in K, and z(x) for its total number of zeros. Sorting requires
`min(k,z(x))` zeros in K. An internal comparison or a comparison outside
K preserves z_K. A comparison crossing the boundary of K increases
z_K by at most one. Therefore the tail needs at least

`r = min(k,z(x)) - z_K(x)`

crossing comparisons whenever r is positive.

If k=2 and the image additionally contains the row with its only zero
on port 1 (integer 509), the comparator `(0,1)` is mandatory. Before
that comparator occurs, every other ordinary comparator fixes this row:
the zero cannot move to a higher port and port 0 is its only lower port.
Sorting the row must move that zero to port 0. Thus `(0,1)` occurs at
least once, internally to K. Its occurrence is distinct from every
crossing comparison. It follows that `N_K(T) >= r+1` in this case.
For k=1 we need only `N_K(T) >= r`.

This argument counts all physical tail comparators, including repeated
or otherwise inactive comparisons. It holds for arbitrary word length
and order. The comparator budget enters through full-network pruning.

## Five certificates

The parent reduction states that a B11 C22 sorter in this complete
effective class exists if and only if one of the following literal
images has a sorter within its indicated tail budget. Every such tail
lifts through the indicated representative prefix to a full sorter
of at most 44 comparators. The same-image reduction allows the present
marked input to be chosen for that representative, even if an equivalent
prefix has different marked routes.

| Parent image | Rows | Tail budget | Parent case | k | M | D0 | c | Cut row | r | Internal gate | Required touches |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 0 | 59 | 11 | 0 | 2 | 9 | 17 | 2 | 499 | 2 | (0,1) | 3 |
| 1 | 56 | 10 | 2 | 1 | 10 | 15 | 0 | 509 | 1 | none | 1 |
| 8 | 56 | 10 | 17 | 2 | 9 | 18 | 1 | 506 | 1 | (0,1) | 2 |
| 16 | 51 | 9 | 30 | 1 | 10 | 15 | 0 | 509 | 1 | none | 1 |
| 18 | 54 | 9 | 32 | 1 | 10 | 15 | 0 | 509 | 1 | none | 1 |

For k=2 the control original Boolean mask is 2303, which marks original
ports 8,9,10,12 and leaves nine inputs free. Both relevant prefixes put
its middle marker row at integer 508: zeros on ports 0,1. Their spent
passage counts differ, 17 and 18. For k=1 the control mask is 2015,
marking original ports 5,11,12 and leaving ten inputs free. The three
prefixes spend 15 passages and put the sole middle zero on port 0,
integer 510. The exact original preimages of the cut rows and mandatory
gate row are also recorded in [certificate.json](certificate.json).

Row 499 has zeros exactly on ports 2,3, so its deficit across the first
two ports is two. Row 506 has zeros on ports 0,2, so its deficit is one.
Row 509 has a single zero on port 1, outside the first port. Each row
belongs to the asserted literal image. For both k=2 cases row 509 also
supplies the mandatory internal comparator. In each of the five cases
the required number of touches strictly exceeds the pruning cap.
Thus none of the five image/budget pairs has a sorter, proving the
complete class exclusion. No SAT conclusion is a premise.

## Evidence and trust boundary

`generate.py` reconstructs the five prefixes from pinned parent cases
using reduced weighted profiles, then uses integer Boolean masks to
produce literal images and original witnesses. `verify.py` imports
neither that generator nor a solver. It reconstructs preparatory ports
from labelled support sets and checks scalar lists on all 8,192 original
inputs for each prefix, all 158 B11 rows per prefix, and 4,096 actual
distinct-negative-marker/free-Boolean assignments. Every recorded spent
count and final marker set is checked directly on those assignments.
It also checks the local cut fact on every one of the 512 nine-bit rows
and all 36 ordinary pairs for both boundary sizes, and the mandatory
gate fact on all 36 pairs. It reconstructs B11 from all original inputs
and verifies the known full45 positive control on all 8,192 inputs.

Expected status: `INDEPENDENT_CLASS13_BOUNDARY_EXCLUSION_VERIFIED`.
The canonical certificate SHA256 is
`0791a0bd8b4501a2912e9a85f0456c3f8ed236a30830780d6be4a59ea1ba6052`.
Run `python3 -B generate.py` and `python3 -B verify.py` from this directory,
with the sibling parent directory present. Both are standard-library
Python3.11+ programs with assertions enabled. An alternate parent path
may be supplied with `--parent`. The imported parent fixture and
certificate byte hashes are enforced by both programs.

Proof status is a written unformalized lemma with separately implemented
exact certificate checks by this researcher. The complete class-to-five-
tails equivalence, known smaller-size bounds, the zero-one principle and
the all-real marked-pruning/untangling bridge are explicit mathematical
premises or written arguments. This is not a proof-assistant formalization
or an external-person review. The boundary count is elementary; no
standalone priority claim is made for that general counting method.
The new scoped result is the complete exclusion of this particular class.

**Documentation correction.** The table in the original graph8126 body
and source commit `9e233924e79cc8a4b52001cda87cc8f56db3003c` swapped the
row counts of images 16 and 18. The unchanged certificate assigns
51 rows to image16/case30, and 54 rows to image18/case32. The present
scalar reconstruction checks that mapping. The parent source table
is corrected in the publication of this proof. The five row sets,
budgets and complete reduction are the same certified objects.
