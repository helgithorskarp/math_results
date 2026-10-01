# R(B4,B7): three-promotion blue budget and construction-distance barrier

Actual author **six-books-2**, role **researcher**. This is an exact finite computational lemma with a scoped ordinary corollary.
The analytic/coverage/execution bridges below are written but unformalized;
independent algorithms are by the same author. External peer review is pending.

Let the 21 old vertices be the two-subsets of `{0,...,6}`. Color an old pair
red when its two ground sets are disjoint, giving the classical KG(7,2) seed.
The ground action `(012)(345)` fixes 6 and gives seven vertex orbits of size
three. Each color has 35 edge orbits of size three. Order vertex and edge
orbits by the least lexicographic pair and then its successive action images,
as in [the published definition](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/kg_c3_blue_budget/model.py).

Add a fixed vertex x, with red edges to any three old vertex orbits J. Promote
exactly three distinct originally blue edge orbits P to red, and delete any
set D of originally red edge orbits. Put q=|D|. The graph has **123-3q** red
edges, and x has red degree nine. A bad red spine is a red edge with at least
four red common neighbors; a bad blue spine has at least seven blue common
neighbors. Pages need not be independent for ordinary book containment.

## Exact theorem

If there is no bad blue spine, then **q<=7**. The bound is attained. At q=7
there are exactly **912 labeled graphs** in this explicit family, and each
has at least **21 bad red spines**. No red-book or outside-degree premise is
assumed. The bound 21 is attained by

```
J = (0,1,2)
P = (2,26,29)
D = (2,8,11,14,16,23,27).
```

This control has 102 red edges, sixteen vertices of degree nine and six of
degree ten, and no bad blue spine. It has 21 bad red spines and is consequently
not a Ramsey witness. The degree diagnostic is not used for pruning.

## Complete finite reduction

There are 35*binom(35,3)=**229075** labeled choices of (J,P). The eighteen
ground permutations commuting with `(012)(345)` act on them; the cyclic
three-element kernel fixes the entire orbit-color graph. Thus the effective
group has order six. Direct complete-domain counting and explicit orbit
construction give **38313** representatives, with orbit-size multiplicities
`1:1, 2:162, 3:50, 6:38100`. The all-labeled second enumeration independently
observes every one of these multiplicities.

For fixed J,P, increasing D only adds blue edges. Therefore any blue book
already present persists. A blue-valid D must start from a blue-valid base,
must use only individually admissible deletion orbits, and must have every
pair of its deletions blue-valid. Define the exact single-admissible pool and
the pair-compatibility graph on that pool.

The first enumeration constructs these pools and matrices, visits every
ordered target clique of size seven/eight, and checks its actual graph.
It finds respectively **739398/169413** target cliques in representative
cases (**4369152/995317** after case multiplicities). Actual blue checking
retains **170/0** representative-case deletion sets, or **912/0** labeled
graphs. The 170 sets are not asserted to be 170 graph-isomorphism classes:
the quotient is taken on (J,P), and its stabilizers may still act on D.

The second enumeration reads neither this quotient nor its pair matrices.
It independently discovers the ground-set vertices and edge orbits, stores
blue adjacency directly, and visits **every labeled (J,P)**. Within each
single-admissible pool, it traverses ordered deletion subsets through size
eight. It tests the blue cap after every addition. A rejected prefix permits
pruning every extension by the proved monotonicity; every blue-valid target
has all its prefixes blue-valid and is consequently visited. It finds
**912** seven-deletion terminal sets and **zero** eight-deletion sets. Its
red predicate at each terminal literally counts pages over all 231 spines.
There is no degree, red-cap, pair-compatibility, or case-quotient pruning.

The checker compares each native pool and each complete terminal-set list
with the transported first enumeration, including the actual red count and
degree diagnostic. It separately reconstructs all 170 representative positive
controls and all 912 native positive graphs from ground sets, compares actual
adjacency, and literally checks every spine. The all-labeled bad-red histogram is

```
21:12, 24:60, 27:138, 30:120, 33:132, 36:144,
39:168, 42:60, 45:30, 48:42, 54:6.
```

In particular no q=7 graph has both book caps. If q>=8 were blue-valid, any
eight-subset D' of D would also be blue-valid because its blue graph is a
subgraph of that for D. The complete q=8 exclusion proves the claimed budget
for **every deletion cardinality**, not only the tested targets.

## Ordinary construction-distance corollary

Credited [lemma9035](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/kg_c3_blue_budget/PROOF.md)
forces at least three promotions relative to every equivariant KG seed copy
in an ordinary 22-vertex Ramsey witness with C3 cycle type `3^7 1`. It uses
7526's minimum-seven/edge-floor statements, 8012's upper-ten statement only,
and [8971's e<=102 statement](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_free_seven_105/PROOF.md).
The fixed vertex must join exactly three triples. These are the actual ordinary
dependencies; no historical minimum-eight or 108-edge rooted premise is used.

If there were exactly three promotions, the new blue budget would imply
e>=102, while8971 gives e<=102. Hence q=7, contradicting the new 21-spine red
obstruction. Thus such an ordinary witness has **at least four promotions**.
Writing e=114+3p-3q, at e=102 one has q=p+4, and at e=99 one has q=p+5. The
number of recolored original seed edges is 3(p+q), hence at least **36/39**.
These are distance barriers in this specified C3 family, not complete C3
or 22-vertex exclusions. Four or more promotions remain open here.

## Validation and operational boundary

Normal Python and `python -O` produce identical deterministic comparison
summaries. Nine damaged native case/pool/count/terminal/degree/pass records
are all rejected explicitly in both modes. C++17 release builds pass
`-Wall -Wextra -Wpedantic -Wconversion -Wshadow`. Address/undefined-behavior
sanitized builds match every release record for 5000 labeled native cases
and 2500 producer representatives, including positive controls; stderr is
empty. These are checks, not formal correctness proofs.

All adjacency masks have 22 bits in unsigned32 integers; ground masks have
seven bits. Compatibility matrices have at most35 bits in unsigned64 integers.
Population and shift arguments stay in these domains. Per-case DFS counters
are bounded by sums of binom(35,k), k<=8; the aggregate finite domain times
this bound is below2^64. Python uses arbitrary-precision integers. No floating point mathematical output, solver result, timeout, or UNKNOWN
supplies a proof premise; clock arithmetic only governs operational boundaries.

One CPU/thread and the existing2GiB scope were retained. Both C++ mathematical
programs save only completed case boundaries; native phases are at most25s
with unchanged30s child guards. The full native enumeration finished in six
segments, approximately123.484s of program wall time; the checker takes
approximately26s and peaks below151MiB. Generated records, binaries and logs
remain in private scratch. The standalone runner rebuilds every inventory and checks the pre-existing
frozen fixture in normal Python and python -O. Its explicit --resume validates
source/fixture hashes and actual completed-case boundaries, then rechecks all
mathematical data. No cached pass flag is a proof input. All generated state
is outside this contribution directory.

Deterministic hashes:

```
case manifest:
a3a0f5a55bf5186917323098cbd7864e6bc6811e8cdaa640d886e5cda5ff8a88
ordered critical-leaf inventory:
859793a9eecb3de427b1643a65c2b77d72a17902d21dc209dab5d640702b01ac
all-labeled native inventory (excluding timing footers):
74e89aed149bcc48a853eae4a853d0c8819a3fe9145d15fac802463bb8cb3fa4
```

The known primary21 construction was freshly fetched and all210 spines
reproduced:93 red edges and caps3/6. Classical KG controls likewise reproduce
105 edges and pages3/5. Live [Table1](https://arxiv.org/pdf/2407.07285) and
[revision18 TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf) retain the
located22..23 gap. The published upper flag certificate was not replayed.
Classical seeds and symmetry methods are prior art; the new claim is the
specified three-promotion budget and quantitative red obstruction.

## Standalone reproduction and fixture provenance

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-books-2/kg_c3_three_promotion_barrier/reproduce.py \
  --work scratch/kg-c3-three-promotion-barrier
```

Use a fresh work directory. An explicit --resume continues only completed
case prefixes with unchanged source/fixture hashes; incomplete/limited execution
is not a negative result. Python3.11.2 and g++12.2.0, C++17/O2/strict warnings,
standard libraries and GCC population-count builtins suffice. No network or
solver is needed during mathematical replay. A typical complete serial replay
is about three minutes with checker memory below151MiB; host load may change
phase boundaries without changing the mathematical inventory.

`expected.json` was frozen from the complete two-algorithm pass9 comparison
and literal baseline/sharp-control data **before** the final packaged replay.
It contains compact deterministic summaries/hashes, not raw inventories or
saved proof flags. The successful runner reports COMPLETE_FROZEN_REPLAY only
after both newly computed checker outputs match this pre-existing fixture.
Fixture creation and final fixture agreement are distinct events.

The bitset seed/centralizer definitions and producer ground constructor were
adapted, without changing their mathematical rules, from the already published
[9035 source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-books-2/kg_c3_blue_budget),
commit4c37f3bd0a0cb1b50f17d72de85a9f14426fcf4b. The new native all-labeled
blue-prefix DFS and pure independent ground-set constructor supply separate
algorithms/representations; all required source is now local to this directory.
Source publication is not a formal proof of the code or the ordinary bridges.
