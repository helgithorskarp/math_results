# One preparatory block in the eleven-event B11 branch

Author: **six-sorting-1, researcher**, 2026-10-01. This is a conditional
construction reduction with exact finite auxiliary certificates. It does
not construct a thirteen-input size44 sorter or exclude all such sorters.

Use the literal G22 from [fixture.json](fixture.json):
P19;(10,12);(0,5);(0,1). Original ports0 and12 hold the global extremes;
original ports1..11 are internal B11 ports0..10. Its exact Boolean image
is the specified158-row B11 set. All comparators below send their smaller
value to their lower numbered endpoint. The
[P19 coverage theorem](https://github.com/helgithorskarp/math_results/blob/main/sorting13_P19_binary_minimum_reduction/PROOF.md)
makes B11 C22 the complete target for a size44 sorter beginning with
literal P19, including every normalized minimum branch and arbitrary
allowable depth. Other thirteen-wire prefixes are outside this coverage.

Import the necessary coupled-profile relaxation from
[graph7871](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_joint_extrema_normal_form/PROOF.md).
Its weights, measured in units32, are initially

```
low  = (4,2,2,2,2,0,2,0,0,0,1)
high = (0,0,0,0,0,4,0,2,4,4,1).
```

For a comparator a<b the low endpoint weights become
(2 max(low[a],low[b]),0), and the high weights become
(0,2 max(high[a],high[b])). Each sum is at most16. The parent also
excludes first10 partners0,7,9; that necessary restriction is retained
unchanged here, with a flag recording whether10 has been touched.
The terminal vectors
are16 at internal0 for low and16 at internal10 for high. An effective
event changes this coupled state; a profile loop preserves it. Every B11
C22 sorter follows this necessary graph and has ten or eleven effective
events. Exact source commits and artifact references are in
[dependencies.json](dependencies.json).

The teammate's
[ten-event postponement theorem, graph8092](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_ten_event_loop_postponement/PROOF.md)
commutes all loops past all events in the ten-event branch. That theorem
explicitly leaves the eleven-event unary branch separate. Here its one
refill is isolated rather than commuting loops across it.

**Lemma 1: phase support and the four-port bound.** Before the first
touch of internal10, both sums are15, their common support is exactly10,
and its two weights are1. All other positive weights are powers of two
at least2. Every preceding effective event is an equal-weight binary
merge in one profile, with both opposite-profile endpoint weights zero.
It removes one port from the occupied union. A jointly empty port never
refills during this phase.

For completeness, before touching10 a unary transfer or an unequal
merge of positive powers of two at least2 would increase its profile
sum by at least2, exceeding16. Equal binary merges preserve the sum.
The other profile has zero weights at those ports, because their only
common occupied port is the untouched10. This proves the pre-f
invariants inductively. The parent's allowed first10 edges then give
the stated unary split in the eleven-event branch. With both sums
saturated after f, only equal binary merges and jointly empty loops
are possible.

In an eleven-event word the first10 event f=(p,10) is minimum-unary and
maximum-unary: p was jointly empty, and becomes occupied only in the
low profile. It refills exactly that one port. After f both sums are16
and their supports are disjoint. Every later effective event is an
equal-weight binary merge in one profile, and again removes one port
from the union without any refill. At either phase a profile loop has
exactly two jointly empty endpoints.

If k effective events precede f, the jointly empty set J immediately
before f has size k. Each profile has weight14 outside10. A sum of
powers of two equalling14 requires at least three positive summands:
14 has three nonzero binary digits, and carrying cannot increase that
minimum. The two supports outside10 are disjoint. Thus their union
contains at least3+3+1=7 of the11 ports, so k=|J|<=4. Unary f requires
p in J, hence 1<=k<=4. After f the union has12-k ports, and the terminal
union has2; there are10-k later binary events.

These assertions follow from the weight rules. Independently, both
programs check them on all2214 states and22536 labelled edges of the
entire parent relaxation, including12535 self loops. There are593
minimum-unary entry edges, classified by |J|=1,2,3,4 as13,100,240,240.
No first4 preparation cut or class restriction is needed for this lemma.

**Lemma 2: one-block normalization.** Every physical word in the
eleven-event branch is equivalent on all ordered inputs, by disjoint
comparator commutations preserving its length, to

```
E_minus ; A ; f ; E_plus ; B.
```

Here E_minus has k events, f is the unique first10 event, E_plus has10-k
events, A uses only J, and B uses only internal1..9. For a size22 word,
|A|+|B|=11.

Proof: a loop before f uses two ports jointly empty at its own time.
Before f those ports never refill, so every later pre-f effective event
is disjoint from that loop. Exchange adjacent loop/event pairs until
all pre-f events precede all pre-f loops. Keep their respective orders.
The analogous exchanges after f put every post-f event before every
post-f loop. Each exchanged pair commutes on arbitrary values. A uses
only ports empty immediately before f. B uses only ports empty in the
terminal union, namely1..9. No loop is exchanged across f. Overlapping
loops retain their order; no pairwise commutation of those loops is
assumed. This proves the statement.

**Lemma 3: at most five preparatory gates suffice.** Let two ordinary
comparator words have the same full Boolean function. For any threshold,
thresholding commutes with each min/max comparator. If their outputs
differed on some ordered input, a threshold at the larger of two
differing output values would distinguish their Boolean functions.
Thus full Boolean function equality implies equality on all ordered
inputs, including inputs with repeated values.

The complete closure of ordinary comparator functions on j<=4 ports
has the following sizes and maximum shortest representative lengths.

| j | Distinct functions | Labelled transition edges | Maximum shortest length |
|---|---:|---:|---:|
| 1 | 1 | 0 | 0 |
| 2 | 2 | 2 | 1 |
| 3 | 11 | 33 | 3 |
| 4 | 261 | 1566 | 5 |

The generator enumerates full Boolean bit-plane functions by breadth
first search until closure. The checker separately enumerates functions
on all j! distinct-rank permutations. Equality on those permutations
implies equality on arbitrary inputs: refine the input order, then
project ranks monotonically to the original, possibly tied, values.
Both enumerations recover the same shortest representative words and
every transition, including933 self loops at j=4. The latter shortest
length histogram is1,6,27,76,114,37 at lengths0 through5.
These small finite counts are auxiliary certificates; no separate
novelty or priority claim is made for comparator-function enumeration.

Apply a shortest representative of A's function to the increasing
list of its literal ports J. This preserves the full11-port function
on all inputs and never changes either marked profile, because J is
jointly empty throughout A. Its length h is at most5 and no greater
than |A|. The resulting circuit has at most22 gates. Consequently
|B|<=11-h. A completion of fewer than22 gates can be padded after its
sorted B11 output with ordinary comparisons on internal1..9. This
preserves sorting on the promised B11 inputs. The padding assertion
does not assert function equality on arbitrary inputs outside B11.

**Theorem 1: finite preparatory-block construction reduction.** An
eleven-event B11 C22 sorter exists if and only if there are an allowed
eleven-event effective word E_minus;f;E_plus, a shortest local comparator
function representative A on its pre-f empty set J, and a tail T on
internal1..9 of length at most11-|A| sorting the exact nine-wire image
after E_minus;A;f;E_plus. Here 1<=|J|=|E_minus|<=4 and |A|<=5.

The forward direction is Lemmas1-3. Terminal marked profiles place the
second original minimum and maximum at original1 and11, respectively;
the four held original extremes are on0,1,11,12. Exact Boolean replay
equivalently confirms B11 extremes on its0 and10. Sorting the other
nine ports is sufficient and necessary. Conversely any such T gives
a B11 word of at most22 gates and can be padded as above, then lifted
through G22. The zero-one principle gives a full13 sorter on arbitrary
inputs whenever its8192 Boolean inputs sort. The serial word reduction
retains all comparator orders and imposes no parallel-depth bound.

There may be up to261 local functions when |J|=4. The theorem does not
declare that all eleven-event class arrangements have one fixed event
order, or that all preparatory blocks can be removed.

**Theorem 2: the complete repeated-(1,2) class reduces to five tails.**
Fix the exact parent effective-multiset class13 (zero based) of
[graph7936](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_extreme_multiset_quotient/PROOF.md),
with decimal code349871875148001158693749134458897. Its multiset contains
(1,2) twice; the other nine effective gates are distinct. A B11 C22
sorter in this class exists if and only if at least one of the following
five literal nine-wire images has an ordinary sorter within its budget.
Nine-wire port i means B11 port i+1, or original port i+2.

| Certificate image ID | Rows | Tail gate budget | Prefix case ID |
|---|---:|---:|---:|
| 0 | 59 | 11 | 0 |
| 1 | 56 | 10 | 2 |
| 8 | 56 | 10 | 17 |
| 16 | 51 | 9 | 30 |
| 18 | 54 | 9 | 32 |

Documentation update, 2026-10-01, six-sorting-1: the original proof table
swapped the row counts of images16 and18. The unchanged certificate has
51 rows for image16/case30 and54 for image18/case32. Their subsequent
exclusion is proved in [the boundary-touch certificate](../thirteen_class13_boundary_obstruction/PROOF.md).

The full row sets, prefix reconstruction data, and all eliminated cases
are in [certificate.json](certificate.json). All36 ordinary nine-wire
pairs are allowed, at arbitrary serialized gate order. Row counts
alone are not exclusion evidence.

Proof: independently traversing the exact class's forward reduced
quota graph and original13 inverse quota graph gives all5385 effective
orders. Canonicalize E_minus and E_plus separately by exchanging
adjacent disjoint comparators only. An occurrence depends on each
earlier occurrence sharing a port; topological orders of this dependency
relation are connected by such exchanges. There are six canonical
triples, with pre-event lengths1,2,3,4 appearing1,2,2,1 times and
order multiplicities2268,1260,315,240,630,672. This preserves functions,
not merely profile states. It introduces no wire-permutation quotient.

Combine those triples with every shortest local function representative
on J. This gives288 normalized prefixes. Direct replay on all158 B11
rows gives108 distinct literal nine-images and139 image/budget pairs.
The producer and independent checker compare every prefix, image and
budget entry. Two prefixes with the same image and budget have precisely
the same ordinary tail-existence question, even if their labelled
input maps or their pruning activity differ.

For one representative of each of the139 pairs, check the thirteen
clamped domains selected by the saturation/activity result
[graph7944](https://github.com/helgithorskarp/math_results/blob/main/sorting13_B11_pruning_saturation_activity/PROOF.md).
The present checker independently reconstructs their thirteen original
marked pairs and all26,624 clamped Boolean assignments. On every one
of the288 normalized prefixes it directly checks that each actual
marked pair has total touched count D=9 and ends at original0,1 or11,12.
A tail on the intervening nine ports cannot touch these marked routes.

Suppose a tail within the stated budget sorted its representative
image. Lift and pad to a full44 sorter. Pruning a selected marked pair
leaves44-9=35 comparisons on11 free inputs, meeting established
S(11)=35 from [Harder's primary paper](https://arxiv.org/abs/2012.04400v3).
Every retained comparison must swap some free Boolean assignment;
otherwise deleting that comparison leaves an eleven-input sorter
of size34. In134 representative prefixes a retained comparison is
ordered on the entire corresponding current clamped domain. The
checker additionally verifies each recorded obstruction directly on
all2048 actual -2,-1 or2,3 marked/free assignments (274,432 checks),
confirming that both compared entries are free Boolean values and
never swap. Thus those134 image/budget pairs have no allowed tail.
This implication applies to every equivalent prefix with that pair,
because any sorter of its image would also sort the obstructed
representative image with the same budget. The five listed pairs are
the only pairs without such a prefix obstruction. Conversely each
is furnished with an actual normalized prefix, so a valid tail gives
the required B11 sorter. This proves both directions.

**Evidence, attribution and remaining scope.** The generator uses
forward reduced weights and bit planes; the checker uses full13
inverse fibers, distinct-rank permutation maps and scalar row lists.
It imports neither the generator nor a solver. In addition to the
complete finite closures, one interleaved22-gate control per each of
the593 unary entry edges is normalized and locally compressed; both
algorithms check equality on all2048 eleven-bit inputs per control
(1,214,464 function equalities). These controls can be nonsorting
words and are not claimed as sorter witnesses. The known full45
positive control is checked on all8192 original inputs.

Both algorithms are by this researcher. Algorithmic independence is
not external-person review or a proof-assistant check. The written
all-real support/commutation/threshold/pruning bridges and the
published necessary-profile and P19 coverage theorems remain explicit
trust boundaries. Source publication itself is not a proof.

The general front/end normalization literature, including
[Codish et al., arXiv1507.01428](https://arxiv.org/abs/1507.01428), and
standard comparator commutation and zero-one reasoning are prior work.
The scoped additions here are the one-block reduction for this unary
B11 branch and the exact five-tail reduction of class13. A targeted
primary-literature/committed-graph search did not identify this specific
reduction; this is not an exhaustive priority certification.

The [maintained table](https://bertdobbelaere.github.io/sorting_networks.html)
was checked live2026-10-01 and still gives S(13)=44..45. B11 remains22..23.
At the original reduction checkpoint, combining six-sorting-2's
graph8092 ten-event exclusions with this
researcher's [graph8070 repeated-(0,1) exclusions](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_repeated01_activity_exclusion/PROOF.md)
leaves417 necessary classes:90 ten-distinct,297 eleven-distinct and30
eleven-repeated. Neither theorem here excludes class13 or reduces
that417 count. The five tails were then unresolved. The subsequent
boundary-touch certificate linked above excludes them, reducing this
417-class checkpoint to416 by itself. A global size44 exclusion also requires arbitrary-prefix
coverage outside literal P19.
