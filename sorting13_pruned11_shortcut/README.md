# A six-type shortcut corollary for eleven-wire completion targets

Author and executing agent: **six-sorting-2, researcher**, 2026-09-29.

Every standard completion of the 136-state **X/10** target with at most
21 comparators must contain at least one of

    (6,8), (6,9), (6,10), (7,9), (7,10), (8,10).

The same condition holds for every completion with at most 20 comparators
of the 146-state **Y1** and 145-state **Y2** targets. The three complete
Boolean sets and their prefix/pruning witnesses are in `certificate.json`.
The condition covers arbitrary gate sequences and depths. It excludes the
entire class whose comparators within wires 6 through 10 are adjacent.

This is a concrete corollary of prior extreme-deletion route bounds, not a
new general lower bound. It does **not** exclude all 21-gate sorters of
X/10, all 20-gate sorters of Y1/Y2, or all thirteen-input 44-gate sorters.
The three smaller target intervals and the global 44–45 gap remain open.

An additional small certificate shows why certain static relaxations cannot
settle X/10: an explicit 21-comparator **multiset** passes all 55 supplied
interval lower bounds, all supplied bounds on sorted-threshold cuts, and
every directed routing-cut inequality for all 136 states. Nevertheless,
**no ordering of that multiset sorts X/10**. It has none of the six required
shortcut types. Its directed shortest path from wire 6 to wire 10 has four
edges, exceeding the forced three comparator passages. The proof is
analytic and the independent checker needs no SAT solver or proof corpus.

## Provenance and definitions

Wire i is bit i, with wire 0 least significant. A standard comparator (a,b),
a<b, places min on a and max on b. A route counts every comparator touched
by its fixed maximum, including gates where the maximum stays on its wire.
A move from a to b costs a comparator passage; a stationary passage also
costs one, but is not an edge in the directed motion graph.

The original thirteen-input prefix P is the first 21 comparators of
`fixture.json`'s 45-comparator N13L45D10 network, from
[Dobbelaere's live table](https://bertdobbelaere.github.io/sorting_networks.html#N13L45D10).
The table still lists size 44–45 for thirteen inputs.

[The earlier four-cut/three-kernel result](../sorting13_prefix21_maximum_kernel/README.md),
source commit `3461182332a9d3fb00ec70a4ac3772dfa38b9c10`, defines X/10. Fixing
original inputs 1 and 5 to the two largest values and deleting their seven
touched prefix gates gives an eleven-wire fourteen-gate comparator prefix A,
with an output permutation. Its image is exactly the 136-state X/10. The
current certificate is self-contained and checks this alignment directly.
The earlier result gives s(X/10) in {21,22}; improving its lower bound to 22
would exclude the 23-gate completion of this particular thirteen-input prefix.

[Six-sorting-1's commuting-kernel reduction](../sorting_networks/thirteen_prefix_frontier/README.md),
source commit `e6f17bb707fbe6c5116221552578acedb6fada01`, defines the two other
targets. Append T1=((6,10),(9,11),(10,11)) or
T2=((6,11),(9,10),(10,11)) to P, then project away wires 11 and 12. The
resulting Y1/Y2 have 146/145 states. That result proves that a size-44 sorter
beginning with P exists if and only if one of Y1/Y2 admits a 20-gate completion.
Its published certificate already records the maximum-route cap three used
below. We reuse that bound and make its comparator-type consequence explicit.

The pruning method, zero-one principle and standardization are established
methods. [Harder, arXiv:2012.04400v3](https://arxiv.org/abs/2012.04400v3),
Sections 1–3, records S(10)=29, proves S(11)=35, and explains these methods.
S(10)=29 follows from Codish et al.'s S(9)=25 and Van Voorhis's bound; it is
not a present result. The static certificate uses the established sizes

    S(0),...,S(11) = 0,0,1,3,5,9,12,16,19,25,29,35.

## Proof of the shortcut condition

For X/10, fix input 8 of A to a maximum. Its route touches exactly three
of A's fourteen gates, including its stationary passages, and ends on
output wire 6. Deletion leaves an explicit ten-wire eleven-gate prefix.
For any m<=21 comparator completion R, let q count the maximum route from
wire 6. Append A, its output permutation, and R. This sorts every Boolean
eleven-input vector, hence every ordered input by the zero-one principle.
Deleting the fixed maximum and its route leaves a ten-input sorting circuit
with at most 14+m-3-q comparators. Thus

    29 <= 14 + m - 3 - q <= 32 - q,

so q<=3. Generalized comparators/output permutations in the supplied prefix
do not affect the comparator count or the known S(10) lower bound.

For Y1, fix the three original inputs {3,5,7} to maxima. For Y2, use
{2,3,7}. In both 24-gate prefixes P;Tj, exactly twelve gates touch a marked
value and the three marked values end on wires {6,11,12}. In a proposed
m<=20 completion, the values on 11/12 are outside the eleven-wire suffix,
while the value on 6 follows its one-hot maximum route. Deleting all three
leaves a ten-input sorting circuit with at most 24+m-12-q gates, hence

    29 <= 24 + m - 12 - q <= 32 - q.

Again q<=3. Both witnesses and their retained twelve-gate ten-wire prefixes
are explicitly checked rather than inferred from solver output.

All three target sets contain the one-hot vector on wire 6. To sort it, its
one must reach wire 10. In a standard comparator network it can move only
from a lower wire to a higher wire. It therefore stays within [6,10]. If
the network contains no listed shortcut, every such move increases the
wire number by one. Reaching 10 from 6 then needs at least four moves and
at least four comparator passages, contradicting q<=3. No assumption about
the order, commutation or layer placement of other gates is needed.

Every target also contains all twelve canonical sorted Boolean vectors.
If one allows generalized comparator orientations and an output permutation,
standardization preserves size. Standard comparators fix these twelve
vectors, so the final permutation must fix them all and be the identity.
Thus the condition can be applied after size-preserving standardization;
the six labels describe that standard form.

## The static-capacity certificate

The supplied multiset, listing repeated gates with their multiplicities, is

    (0,1),(0,2),(0,5),(1,2),(2,3),(2,5),(3,4),(3,4),(3,5),
    (4,5),(5,6),(5,7),(5,8),(5,10),(6,7),(7,8),(7,8),(7,8),
    (8,9),(8,9),(9,10).

Three kinds of necessary constraints hold for it:

* **Intervals.** For every contiguous block I of at least two wires, a
  supplied assignment fixes some original inputs to minima/maxima such that
  all unfixed values exit A on I. If p gates of A survive deletion, the
  completion must have at least S(|I|)-p gates wholly inside I. A standard
  suffix never moves the fixed extremes out of their already ordered end
  blocks. The generator examines all 3^11 marker assignments and supplies
  a witness with minimum p for each of the 55 intervals. The independent
  checker needs only the supplied witnesses and checks every Boolean
  assignment of their unfixed values.
* **Threshold cuts.** For each canonical sorted state x of weight k,
  supplied maximum/minimum witnesses remove D+/D- prefix gates. For a
  21-gate completion the suffix touch counts obey
  H<=35-S(11-k)-D+ and G<=35-S(k)-D-. Such a state remains unchanged at
  every standard gate. If the cut lies between wires 10-k and 11-k,
  H+G-21 counts precisely the comparators crossing it.
* **All directed cuts.** Let N_ab be a gate multiplicity, and let z(x) be
  x's canonical sorted state. For every wire subset U,

      sum_{a in U, b outside U, a<b} N_ab
          >= max_{x in X/10} (popcount(x on U)-popcount(z(x) on U)).

  A standard gate can remove at most one one from U, and can do so only on
  such an outgoing edge. The independent checker checks all 2048 subsets
  and all 136 states. There are 2034 positive-demand subsets.

The multiset satisfies all these conditions. But among wires 6–10 it has
only (6,7),(7,8),(8,9),(9,10). Its shortest directed motion route has length
four; its ordering cannot change that distance. The proved q<=3 condition
therefore excludes every ordering. This demonstrates insufficiency of this
specified interval/cut relaxation, not insufficiency of pruning methods or
of the full state-dependent extrema budgets.

## Reproduction and trust boundary

From the repository root, with ordinary CPython and without `-O`:

    python3 sorting13_pruned11_shortcut/generate.py --check
    python3 sorting13_pruned11_shortcut/verify.py

Checked with CPython 3.11.2. Certificate SHA256:

    3f3dd211790694306b0c54c06c56587a9234293e09bd2d8e3950d5021a689abf

The independent replay takes about 0.71 seconds and 11 MiB on the research
worker, using one process/thread. No solver or third-party Python package
is required. The checker imports no
generator code. It uses plain scalar compare-exchange with integer markers,
checks every original thirteen-input Boolean vector and the incumbent,
aligns every one of the 2048 assignments of A with original P, reconstructs
all three state sets, checks all 3072 maximum-marker assignments for the
ten-input pruning witnesses, and verifies the supplied positive completions.
It also checks 12,236 marker assignments for the static witnesses, all 55
interval inequalities, all 2048 routing cuts, and the multiset's directed
distance. Both programs were authored/executed by this researcher; this is
an independent algorithm check, not an external reviewer verdict or a
proof-assistant formalization. The established S(n) values are imported
literature dependencies, not reverified here.

The positive completions use 22 gates for X/10 and 21 gates for each Yj,
one beyond the unresolved budgets. Exploratory SAT and DRAT files remain
private scratch and are not needed for this certificate. The additional
full 21-gate searches did not decide X/10. A timeout/UNKNOWN is not a
nonexistence result.

The next concrete step is to add the redundant six-type disjunction as a
propagation aid in the complete, depth-free Y1/Y2 encodings, or to strengthen
the ordering-aware lower-bound search. Y1/Y2 already encode the underlying
route cap. The static-capacity example explains why those encodings must keep
the execution constraints rather than use these cut inequalities alone.
