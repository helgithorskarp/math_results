# Unary minimum kernels need two preceding nonkernel gates

Author and executing agent: **six-sorting-1, researcher**.

Let Y1 and Y2 be the published eleven-wire targets with146 and145 Boolean
rows, respectively. Their explicit rows and13-wire prefixes are literal
in `fixture.json`. Consider a standard20-comparator sorting completion
of either target, with **exactly one passage on the one-zero-1 route**.
If its minimum kernel contains a unary gate, **at least two gates outside
that kernel precede its final merge**. Depth and the remaining gate order
are arbitrary.

Here the minimum kernel tracks the zero routes of the three one-zero
rows on wires0,1,5. A kernel gate touches at least one occupied zero
position; a binary gate touches two such positions, while a unary gate
touches one. A nonkernel gate avoids all currently occupied positions.
These are execution events, not fixed comparator types.

There are exactly154 possible kernel words under the witnessed route
capacities(3,1,3): one binary-only word,25 words with one unary gate,
and128 with two unary gates. The306 unary front prefixes, and all35,464
ways to place exactly one nonkernel gate before their last merge across
the two targets, violate a second-minimum Kraft bound. The least verified
weight is5/4. Thus a one-unary kernel finishes no earlier than the fifth
gate of the Y tail, and a two-unary kernel no earlier than the sixth.

This is a necessary interleaving condition. It excludes neither all
unary-containing completions nor all20-gate completions. Y1/Y2 remain
20 versus21, and the global thirteen-input44–45 question remains open.
The binary-only branch and prefixes containing at least two earlier
nonkernel gates are outside this exclusion.

## Pruning and kernel coverage

Let P be the21-gate prefix in the fixture. The24-gate prefixes are

    P;T1, T1=(6,10),(9,11),(10,11),
    P;T2, T2=(6,11),(9,10),(10,11).

They put the two global maxima on11/12 and have the complete Y images
on0..10. A Y20 completion therefore gives a44-gate thirteen-input sorter.
Each proper Y row has a zero on at least one of0,1,5; exactly those three
one-zero rows occur. Thresholding commutes with compare-exchange.

The original nonlow masks4095,7167,6143 put a marked global minimum on
Y wires0,1,5 and delete2,3,2 prefix gates. Imported S(12)=39 gives the
suffix route bounds3,2,3. The present conditional branch sets the middle
bound to1. Passages include stationary comparisons.

The zero on1 can reach0 in one passage only via(0,1). This must be the
last kernel gate: any later kernel passage would also touch this route.
Before it, the routes from0 and5 have coalesced at0. Their binary merge
is(0,m), where m is the current location of the zero from5. Both routes
have at most one further passage beyond these two binary merges.

Consequently the full kernel classification is:

* No unary: (0,5),(0,1).
* One unary on route0 before its merge: (0,p),(0,5),(0,1), with
  p in{2,3,4,6,7,8,9,10}.
* One unary on route5: (min(5,p),max(5,p)),(0,min(5,p)),(0,1), with the
  same eight choices.
* One shared unary after the first merge: (0,5),(0,p),(0,1), p=2..10.
* Two unaries: one on each of0 and5, in either order, before their
  binary merge. Each order has64 choices. In the5-first order, a moved
  zero makes its new location occupied and vacates5; route0's partner
  choices change accordingly.

There can be no other unary: it would exceed a leaf capacity. Nonkernel
events leave these three one-zero trajectories unchanged, so this
classification also applies with arbitrary intervening nonkernel gates.
`generate.py` enumerates support histories; `verify.py` independently
constructs this closed classification and compares the exact word list.

With no earlier nonkernel gate, the prefix is the kernel itself. With
exactly one, it is inserted before some kernel gate at a pair avoiding
every occupied position at that moment. The checker derives these
positions by three individual zero trajectories. This covers all35,464
placements, including placements after a unary or first binary merge.
No unary gate is moved to the front by a commutation assumption.

## Second-minimum obstruction

For each candidate prefix Q, comprising P;Tj followed by the proposed
kernel and at most one inserted nonkernel gate, choose every one of the78
original input pairs for the two smallest values. The other eleven values
are arbitrary and above them. Write D(Q;a,b) for the number of Q gates
touching either marked minimum. Comparison of minimum markers depends
only on their thresholds, so this deletion count is independent of the
ordering of the eleven middle values.

The kernel puts the global minimum on0. Monotonicity extends the three
one-zero executions to every proper Y row. After the last(0,1), any gate
on0 would violate the assumed one-passage route. Thus0 is unused in the
remaining suffix. Wires11/12 are also outside the Y completion. Removing
these three fixed extrema leaves ten wires.

For each marked input pair, the other marked minimum exits Q on some
retained wire i. Its corresponding one-zero row occurs in the ten-wire
image. If its remaining suffix route has qi passages, deleting the two
marked minima from the complete13-wire sorter leaves an11-input sorting
circuit with at most44-D-qi gates. Imported S(11)=35 forces

    qi <= 9-D(Q;a,b).

Taking the strongest supplied bound ci for each occupied leaf gives a
necessary Kraft inequality

    sum_i 2^(-ci) <= 1.

Indeed the one-zero routes form a merge tree; a binary gate joins two
supports and a unary gate adds a passage on one support. Their actual
depths di satisfy Kraft's inequality, including unary passages, and
di<=ci implies2^(-di)>=2^(-ci). Every enumerated candidate instead gives
weight at least5/4. Therefore none has the required suffix, whatever its
depth or order. The classification then proves the stated two-nonkernel
condition.

## Reproduction and trust boundary

Six compact text files contain the literal fixture,154 kernel words,
aggregate certificate, two independent algorithms and this proof.
There are no SAT libraries, full formulas, solver traces or large
enumeration dumps. Use ordinary CPython3.11 or later, without `-O`:

```sh
python3 generate.py --check
python3 verify.py
```

The packed Boolean generator produces the exact certificate and a digest
over every cap profile. The independent checker uses distinct scalar
ranks, a closed kernel classification, individual zero trajectories and
all78 marked input pairs per candidate. Expected counts are306 unary
fronts,35,464 single-nonkernel placements, and2,790,060 distinct-rank
assignments. It also checks16,384 original Boolean images, six
single-minimum witnesses and the21/22-gate positive controls on32,768
original inputs. The22 control duplicates one gate of the known21 tail
and commutes(0,1) forward; its unary kernel finishes at the third gate,
showing that the20-gate hypothesis is essential. Weakened pruning bounds
are rejected as obstructions.

No independent-person review or formalization is claimed. Mathematical
dependencies are the written classification, pruning and Kraft bridges,
and the established small sorting-size bounds. Native solver results
from exploratory construction searches are not part of this proof.

## Sources and remaining construction lane

Y1/Y2 and their prefix equivalence are from
[the earlier frontier](../thirteen_prefix_frontier/README.md), source
`e6f17bb707fbe6c5116221552578acedb6fada01`. The minimum-once branch belongs
to its [mixed-pruning split](../thirteen_prefix_frontier/MIXED.md), source
`7b5c4164b36ac1e334d573f714d3ec4efbd59592`. The maximum-kernel prerequisite
is [six-sorting-2's result](../../sorting13_prefix21_maximum_kernel/README.md),
source `3461182332a9d3fb00ec70a4ac3772dfa38b9c10`.

This complements the [53/41-state exact minima](../thirteen_minimum_kernel_obstruction/README.md),
source `f3dfb24efdd85481de7901efdc1383a46ee96bf5`, which cover specific
binary-front subcases. The new statement concerns the other, unary
minimum kernels; it does not duplicate those suffix exclusions. The
separate [X/10 shortcut and static-capacity result](../../sorting13_pruned11_shortcut/README.md)
by six-sorting-2, source `5a9a621797abcf8ec702a62c15a7ee0c033d9d04`,
was checked for overlap. It proves a six-type maximum shortcut and a
different static relaxation obstruction, not this interleaving bound.

The freshly read [minimum/refill reduction](../../sorting13_minimum_passage_reduction/PROOF.md)
by six-sorting-2, source `aedd5f48b84a375cbd671d1daf331ede87815959`,
forces minimum1 to have one passage in the different K18 target. Here
that route count is a stated hypothesis on Y20, and the proof uses
second-minimum Kraft obstructions. Neither target's conclusion is
silently transferred to the other.

The primary small-size source is [Harder, arXiv:2012.04400v3](https://arxiv.org/abs/2012.04400v3),
including S(11)=35, S(12)=39, standardization and pruning. Those lower
certificates were not rerun. The [primary network table](https://bertdobbelaere.github.io/sorting_networks.html)
still gives44–45 for thirteen inputs on2026-09-30. The general pruning
and Kraft methods are prior art; no historical priority is claimed.

The constructive next step is a unary minimum kernel with two or more
interleaved nonkernel gates, or a different remaining binary-front
target. No exclusion of those classes follows from the present count.
