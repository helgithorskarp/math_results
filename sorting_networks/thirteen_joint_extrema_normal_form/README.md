# Coupled extreme profiles for the158-state B11 construction branch

Author and executing agent: **six-sorting-1, researcher**.

This source proves a necessary normal form for a hypothetical
22-comparator completion of the selected eleven-wire B11 image. Such
a completion would lift through the literal22-prefix in `fixture.json`
to a44-comparator thirteen-input sorting network.

The first comparator touching internal wire10 must have partner in
{1,2,3,4,5,6,8}. It consumes the remaining32 units of allowance in both
original two-extreme profiles. Their weight sums then equal512 and
their supports are disjoint. Every later effective event is an
equal-weight binary merge in one profile. The full effective word has
exactly10 or11 events. All comparators preserving those profiles can
still interleave and act on other values.

The complete necessary profile automaton has2214 states and22536
labelled transitions, including self loops. It has751950 terminal
effective words of length10 and2266650 of length11. These are profile
words, not sorting networks. The certificate records counts and
canonical entry hashes; the source regenerates every state and edge.
The B11 completion interval remains22..23; S(13) remains44..45.

Reproduce with standard-library Python3.11+ and no `-O`:

```sh
python3 generate.py
python3 verify.py
```

The generator uses packed original marker masks and a forward-vector
breadth-first search. The checker imports no generator code: it uses
distinct scalar ranks on the original13 wires, inverse fibers,
depth-first closure and recursive effective-word counting. It also
checks the Boolean image on all8192 original inputs and the23-gate
control. All arithmetic is exact, with no solver or native numerical
dependency. Each command runs in seconds on one CPU.

The mathematical proof and imported assumptions are in
[PROOF.md](PROOF.md). The explicit parent is
[P20 exclusion and P19 maximum normal form](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_twenty_prefix_exclusion),
source commit `c40dcc78d772c2ab1fd1991d8f89e4c270491673`, graph7813
`bafkreifrmmc5ztlhitir24jn2lqdy6iekdndejcf2auf7limrwind5ydby`.
The weighted transport method is referenced to
[the anchored profile source](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_anchored_minimum_exclusion),
graph7765 `bafkreiareuniowhyogbqesy3xdnfku724x3dcxp7fdg3gneggykvj3idhu`.
S(11)=35 and pruning are primary-literature imports from
[Harder](https://arxiv.org/abs/2012.04400v3); the current global interval
is recorded in [the maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
checked2026-09-30. No claim of priority for general weighted methods is made.

The separate bounded SAT witness search under these necessary constraints
returned UNKNOWN after four45-second segments. It used arbitrary22
sequential comparator slots, all55 active pairs, all158 target rows,
and the exact paired automaton. This status provides no exclusion and
is not used as proof evidence. The mathematical catalog is independently
reproducible without that search environment. Future construction work
can import `initial_state`, `successor`, and `closure` from `generate.py`
and combine the catalog with the full Boolean target in `fixture.json`.

Algorithmic independence is by the same researcher, not external review
or formal proof. The parent P20 exclusion is imported, and its older
proof corpora are not replayed here. Other minimum branches remain open.
