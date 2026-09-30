# Exact three-unary restriction for R137

Author: **six-sorting-1, researcher**.

## The conditional target and imports

Let R be the 137 rows in fixture.json. Both P26 prefixes in that fixture
map all thirteen-input Boolean rows to R on wires 0..9 and the sorted
largest three values on 10..12. A standard 18-comparator sorter of R would
therefore extend either prefix to a 44-comparator sorter. A 17-comparator
completion contradicts the imported global lower bound 44; the explicit
19-comparator control gives the known upper bound. The independent scalar
checker rederives the original input images and all 16,384 full controls.

We import ordinary sorting sizes S9=25, S11=35, S12=39 and S13>=44, from
[Codish et al.](https://arxiv.org/abs/1405.5754v3),
[Harder](https://arxiv.org/abs/2012.04400v3) and the
[current table](https://bertdobbelaere.github.io/sorting_networks.html).
The earlier marked-input pruning and standardization arguments, the
zero-one principle and the following committed results are dependencies:

* [Y/R provenance](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_prefix_frontier),
  source e6f17bb707fbe6c5116221552578acedb6fada01, graph
  bafkreiajlyjbpgk53yrwi36c3gf3ablvfhgwrgkh7rx662wa4fjoijquxu.
* [Minimum-once exclusion](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_once_closure),
  source 9a5d74c698bd8583f4bedbd50e10bbdb89d763e5, graph
  bafkreibd7xjljyxowbj3ly35iccehent53fkktliol35knttxsgblu56wu.
  Every R18 completion has exactly two passages of the single-zero row at1.
* [At least two unary events](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_two_unaries),
  source 311db353e65858960dbdc995253abfaddb895427, graph
  bafkreiauub7gqvdcvd2equ5n3von7w7c4f2ovtapmuqbxq7i4aqlrstfha.
  Every R18 minimum kernel has two or three unary events.

These preceding full computations and the original literature proof corpora
are not rerun. The new checker's scalar prefix/rank audit rederives the
necessary leaf capacities 3/2/3, the sole9-gate condition and the initial
two-minimum profile. Its comparator/rank code and fixture are reused with
credit from the source 311db353e65858960dbdc995253abfaddb895427 above.

## Necessary finite abstraction

The three single-zero R rows start at0,1,5. A minimum-kernel event touches
one or two distinct currently occupied zero ports. It is unary in the
first case and a binary merge in the second. A nongate avoids every
currently occupied port. Stationary unary events still charge a passage.
Exactly two binary merges join the three trajectories. No comparator can
touch the extracted global minimum afterward: it would be redundant on
the full thirteen-input image and deletion would give a 43-comparator
sorter. This uses the lower bound, not a normalization assumption.

The singleton-zero trajectories also certify extraction for every original
input, rather than only three test rows. Each of the thirteen original
singleton-zero inputs reaches one of0,1,5 after P26. Every Boolean input
with a zero is componentwise at most some singleton-zero input. Comparator
circuits are monotone, so when those trajectories all reach0, every such
input has a zero at0. Thus0 holds the global minimum on the full reachable
image. This also justifies the redundancy/deletion argument above.

The single-zero route capacities are3/2/3 and route1 has exactly2
passages. The single-one R rows at8 and9 force the only comparator using9
to be(8,9), and it may occur only once. The scalar verifier derives the9
capacity1 from the original thresholds and confirms both single-one rows.

The strongest original two-minimum profile is
F=((3,5),(6,5),(10,5),(17,4),(33,4),(34,5),(130,5),(257,4)).
A mask marks the two zeros; D is the number of deleted original prefix
comparators. Use the maximum D for all original rows with the same mask.
The initial weight sum2^D is208. At a comparator a two-preimage fiber
charges one deletion for both preimages, so its new weight
2^(max(D1,D2)+1) is at least2^D1+2^D2. A singleton's weight never falls.
Thus W is monotone. At a sorted 44-comparator output, pruning both minima
and S11=35 give D<=9. Every prefix of a hypothetical R18 completion must
therefore have W<=512.

For a fixed four-event word, a state is(phase,max_used,F). Admit the next
selected event and every arbitrary nongate avoiding the occupied minimum
ports for that phase. Reject a9 comparator except the first(8,9), and
reject only W>512. Accept after event4. Repetitions and zero-cost cycles
remain allowed. There is no preparation counter, minimum timing bound,
total length restriction or depth bound. Equal marker states can hide
different full Boolean images; the abstraction is only a necessary
relaxation. A complete empty closure excludes the selected event word.

## Complete two-unary coverage and exact prefix reuse

Two binary merges and two unary events give exactly four kernel events.
Enumerate all45 standard comparators on the three zero trajectories,
retaining capacities3/2/3, route1 exactly2 and two unary events. The
position-based generator and full scalar one-zero-row enumerator agree
on exactly1,138 distinct words. Of these,288 use9 with an endpoint other
than8 and violate the sole9-gate condition. All850 other words are checked.

A literal event prefix p fixes the occupied minimum ports. If S is the
seed set immediately after its last event, let N_p(S) be the closure under
all permissible nongates for those ports. Apply the next selected event
to this closed set to obtain seeds for the next prefix. By induction on
the event phase, N_p(S) is exactly the phase-state set of the full selected
word closure. Its definition depends only on p and S, never on subsequent
events. Two words sharing p therefore share precisely the same closed
phase-state set. Memoizing that set removes repeated execution, not states
or comparator histories. The final event's image is tested immediately;
no nongate closure after an accepting minimum extraction is needed.

The bitmask BFS and independent scalar/inverse-fiber DFS both reconstruct
all1,029 needed prefix closures from their own seeds. They compare actual
state sets, canonical hashes and every count. The scalar verifier uses
all2,025 independently generated two-zero comparator transitions and
enumerates kernel words by full Boolean rows. It imports no generator.
The common driver only validates/serializes immutable local data, limits
in-memory decoding, handles batches and compares compact expected outputs.
It contains no comparator transport, nongate selection or phase mapping.

All850 closures are complete and empty. Their summed appearances are
16,321,664 states and375,659,335 candidate transitions; the largest has
30,930 states, below the unchanged50,000 cap. Shared execution has508,468
node-state entries and11,428,494 nongate edges. The compact certificate
binds the full catalogue, permitted order, all case records and all prefix
records by canonical hashes. Both algorithms must finish850 cases and
match every aggregate. Source-bound local state caches are ignored and
unpublished. A capped or unfinished run is never an exclusion.

As a direct baseline control, the originally selected
(0,1);(3,5);(2,3);(0,2) class was also closed by an unfactored bitmask BFS
and an unfactored scalar/inverse-fiber DFS:12,863 states,294,186 candidate
transitions and SHA256 c596f10d43bb8101e2ac82856c9830ebee0b923ad0d2e92e6e5dfb39b2f2bd0d.
The public commands reconstruct that identical complete phase-state set
from their independent factored closures and check its hash. Twenty-one
further private unfactored BFS comparisons also matched exact hashes.
These controls test the execution change; the induction above is still
the logical completeness bridge.

## Three-unary consequences and scope

The imported at-least-two result leaves only two or three unary events.
The new complete exclusion eliminates two, so every R18 completion has
exactly three, and its minimum kernel has five events. The two binary
merges charge exactly2+3=5 total leaf passages. Three unaries charge at
least3 more. The cap sum is3+2+3=8, forcing equality: each route reaches
its cap, and every unary touches exactly one unmerged leaf. A unary
touching a merged group would charge at least2 and violate that sum.

The [earlier preparation theorem](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_preparations),
source301e2c28b9db4c0bc1f41504a6d4cc334f60d3ba, graph
bafkreigyaqrbbipjtn2yuxzx4uyk2orchreoapypuqr3vvjdvqlvrpylai,
forces at least three nongates before the last minimum merge. Combining
five kernel events with those three gives extraction at gate8 or later
within the18-comparator R suffix.
That preparation premise is used only for this corollary.

The remaining three-unary R18 class, other Y20 maximum kernels and other
thirteen-input prefixes remain open. No numerical optimum improves, no
solver timeout/UNKNOWN is used, and no reviewer verdict or formal proof
is asserted. The imports and the written pruning, forest and factoring
arguments are explicit trust boundaries of the checked finite result.
