# The saved C3 graph cannot be repaired by changing only phases

Every phase reassignment that preserves the saved score-123 graph's
pair multiplicities, internal triangle colors, and root contacts retains
**three explicit blue five-cliques**. This excludes that entire
`3^73`-member labeled family as a source of a Ramsey(5,5;43) graph,
including phase changes involving all fourteen moving triangles.
It does **not** prove that score 123 is optimal in that family.

A single degree-preserving multiplicity trade removes this fixed
obstruction. A completed bounded phase search on its `3^76`-member
family found a graph with **177 defects**, so it did not improve the
saved score 123. The traded family is **not excluded**; 177 is an
achieved score, with no optimality claim. No Ramsey coloring, global
symmetry restriction, or new Ramsey-number bound is obtained.

## Exact phase family and its obstruction

The [parent graph](baseline.edges) is the
[previous fourteen-cycle construction](../ramsey_r55_c3_fourteen_construction).
Its vertices are `0,...,42`. Write

    T_i = {3i,3i+1,3i+2}, 0 <= i < 14;  z = 42.

The action rotates each `T_i` and fixes `z`. Triangles `T_0,...,T_6`
are internally red, and `T_7,...,T_13` internally blue. Its red degree
histogram is `20^6 21^28 22^9`, and it has 453 red edges.
Edge files begin with `43`, followed by sorted red pairs `u v`; omitted
pairs are blue. The parent SHA-256 is

    36c4a4ff6359e56ece7c9a6b41e35fae02cb04d72e56d832dc1a4dc056c6e88e

For `i<j`, let `c_ij` be the number of red neighbors in `T_j` of any
vertex of `T_i`. This lies in `{0,1,2,3}`. An invariant bipartite pair
is the union of three matchings indexed by the phase difference
`t-s mod 3` between vertices `3i+s` and `3j+t`.

Fix every `c_ij`, every internal color, and every contact from a
triangle to `z` as in the parent. A pair with multiplicity 0 or 3 is
fixed. A pair with multiplicity 1 has three choices for its red
matching, and one with multiplicity 2 has three choices for its blue
matching. The parent has 10 zero pairs, 33 one pairs, 40 two pairs,
and 8 three pairs. Thus its phase family has exactly

    3^73 = 67,585,198,634,817,523,235,520,443,624,317,923

**distinct labeled graphs**. Each assignment changes physical adjacency
uniquely; no quotient by isomorphism, triangle relabeling, or phase gauge
is taken. Every labeled degree is preserved, but this is a stricter
restriction than preserving degrees alone.

In every member of this family, `T_10={30,31,32}` is blue internally,
all edges from `z` to `T_2` and `T_10` are blue, and `c_(2,10)=0`.
Consequently the three sets

    {6,30,31,32,42}, {7,30,31,32,42}, {8,30,31,32,42}

are blue five-cliques under **every** phase assignment. This is the
complete proof of the exclusion. The lower bound of three defects is
not asserted to be attained. No exhaustive search, solver, extremal
catalog, degree-profile theorem, or older repair theorem is a premise.

[proof.py](proof.py) reconstructs the dense physical adjacency matrix,
checks the action, all 91 multiplicities and the displayed witnesses,
and literally enumerates all five-sets to identify all cliques made
solely of fixed-color pairs. Exactly these three occur in the parent.
The literal witness check and the argument above suffice for the
universal family exclusion; enumerating fixed five-sets is an additional
check. The code imports neither the template producer, native objective,
nor the inherited physical graph checker.

The [earlier four-triangle barrier](../ramsey_r55_c3_four_triangle_barrier)
allows multiplicities to change on up to four triangles and proves
score 123 is uniquely minimal there. This phase-family result has a
different scope: multiplicities are fixed but support can involve all
fourteen triangles, and only a lower bound of three is proved. Neither
result's family contains the other's in general. No earlier switching
separation is asserted for new traded graphs.

## One explicit degree-preserving trade

The pass first checked the profile before freezing degrees. The degree
window 18 through 24 holds. The profile has inherited weight `W=45`
(six plus nine vertices each of weight three), while the campaign's
[hard local-deficiency branch](../ramsey_r55_exceptional_degree_sieve)
requires `W<=39`. Thus this fixed degree profile is outside that **hard
branch**; it is not globally excluded. The remaining low-deficiency
branch is not decided. This contextual check does not enter the
phase-family proof or the search objective.

To escape the persistent blue cliques while preserving degrees, change
four multiplicities:

| Pair | Parent | Traded |
| --- | ---: | ---: |
| `(2,10)` | 0 | 1 |
| `(0,5)` | 0 | 1 |
| `(0,2)` | 2 | 1 |
| `(5,10)` | 3 | 2 |

Every affected triangle has one increment and one decrement. Each of
its three vertices therefore has net degree change zero. All root
contacts and internal colors remain fixed. The checker verifies this
per physical label and checks the exact four count changes.

[template.py](template.py) chooses this template by the fixed protocol:
consider `+(2,10),+(k,l),-(2,k),-(10,l)` in lexicographic `(k,l)` order,
with all four indices distinct; reject counts outside 0 through 3;
select the first template with no all-fixed monochromatic five-set.
The feasible earlier choices `(0,1),(0,3),(0,4)` have respectively
6 red, 21 red, and 3 blue fixed five-cliques. `(0,5)` is the first
passing choice. This is a deterministic selection prefix, **not** an
exhaustive classification of all quotient trades.

For the selected template, all 54 possible single-orbit realizations
of these four count changes are physically scored. The first minimum
has score 186 and is saved as [traded.edges](traded.edges).
The trade gives 76 mixed pairs, so its full phase family has `3^76`
distinct labeled members. The dense checker finds no five-set whose
ten pairs are all fixed in one color. This removes only the displayed
kind of obstruction; it does not establish Ramsey feasibility or
exclude other unavoidable defects.

## Completed bounded phase experiment

The experiment uses exactly this one template, with all 76 ternary
phases free. Root and internal colors remain fixed. There are 16 starts,
25,000 phase moves per start, and seeds `2026090621+r`, `0<=r<16`.
Start zero uses the saved traded graph; other starts draw all phases
using the specified SplitMix64 modulo-three rule. This is a deterministic
pseudorandom protocol, not an exactly uniform sampling claim.
The calibration repeats the first two seeds for 2,000 steps and is
not additional production coverage.

All 400,000 production moves completed in 193.775 seconds on the
production host. Every restart found a best score of 177. The first
winner, [best.edges](best.edges), has **123 blue and 54 red five-cliques**
and the unchanged degree histogram `20^6 21^28 22^9`.
[restarts.tsv](restarts.tsv) records the complete best phase word,
seed, initial score, best score and step for every restart.
There was no zero-score early exit or STOP condition.

This failed the constructive gate of a physical score below 123.
The search is heuristic and visits only a tiny part of the family;
it proves no lower bound on the traded template's optimum. No further
trade, restart batch, larger cap, switching census or proof phase
was started after this result.

### Objective, checks, and trust boundary

For each physical five-set and each color, [search.cpp](search.cpp)
intersects the allowed phase values for each pair occurring in the
set. A fixed edge of the wrong color or an empty intersection discards
that event. Otherwise the event occurs exactly when each involved
phase belongs to its recorded subset of `{0,1,2}`. Identical events
are merged with their physical multiplicities. The model has 126,126
weighted events. It counts all physical defects, including sets using
the root or vertices outside a changed pair.

The incremental state keeps the number of violated phase conditions
per event and exact gains for each alternative phase. An event with
no violations contributes its negative weight to moves that break it;
one with exactly one violation contributes its positive weight to
moves repairing that sole violation. All other single-phase gains
are zero. Updates use explicit integer membership differences, and
every predicted score change is checked. Full state and gains are
rebuilt every 5,000 production moves and at restart boundaries.
Seven-step tabu, aspiration, one-percent random moves and the stated
bad-event escape are heuristic choices, not mathematical assumptions.
The total weight of all projected events is at most `2*962598`, so
accumulated count and gain arithmetic, including intermediate updates,
is safely inside signed 32-bit range. Completed scores are at most
962,598. Unsigned SplitMix64 operations are modulo `2^64`. Time is
metadata only. There is no solver or floating-point decision.

The first development calibration failed an incremental-score check
in optimized code and was discarded. The frozen integer-membership
version passed release and ASan/UBSan calibration with identical graph,
model and restart words. No compiler-root-cause claim is made and no
result uses the rejected version.

[control.cpp](control.cpp) evaluates all `3^5=243` assignments on five
selected phase variables and a 200-move walk with full state rebuilds.
[audit.py](audit.py) discovers physical pair orbits using the action,
imports no native model or gain code, and checks each of these 443
states by direct clique recursion. It also checks all production
initial and best scores, every saved winner's labeled degrees, and
exact equality of the first winner's full red/blue defect lists under
literal five-set enumeration and separate clique recursion.
[physical.py](physical.py) is disclosed byte-identical reuse of the
previous checker; [imports.json](imports.json) records this boundary.

The dense proof checker rejects four witness/trade mutations.
Normal and assertion-disabled Python outputs agree for the proof,
443 controls and full graph audit. These are author checks, not
external peer review or formalization. The simple displayed witness
proof establishes the negative theorem; the C++ optimizer is needed
only to reproduce how the unsuccessful traded fixture was found.
No universal negative conclusion relies on the heuristic or its gains.

## Reproduction

Tested with CPython 3.11.2 standard library and GCC 12.2.0, C++20.
From the repository root, using a fresh output directory:

```sh
bash ramsey_r55_c3_phase_template_obstruction/reproduce.sh /tmp/r55-phase-audit
```

The default verifies the exact obstruction and trade, regenerates the
selected template, reruns all 443 native/physical controls, audits the
saved 16-start results, and checks file hashes. It **does not rerun the
400,000-move search**. Expect
`VERIFIED_FIXED_PHASE_OBSTRUCTION_AND_DEGREE_TRADE`,
`VERIFIED_443_PHYSICAL_PHASE_CONTROLS`, and
`VERIFIED_PHASE_TRADE_GRAPH_SCORES` with score 177.

To repeat the full search and compare every restart word and graph:

```sh
bash ramsey_r55_c3_phase_template_obstruction/reproduce.sh /tmp/r55-phase-replay --search
```

Allow roughly four minutes on comparable hardware. Both modes require
only the bundled files, Python and a compiler. Native runs require fresh
output paths; STOP is honored between starts and incomplete status
cannot imply a completed batch. Binaries, native logs, scratch states
and rejected development versions remain outside Git. Compact controls
and all saved best words are included. The original full run used the
same hash-frozen production source now published; the packaged default
audit was run, without claiming a second full search.

The current lower bound remains 43; see
[Angeltveit--McKay's 2026 paper](https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.70029)
for current Ramsey context. No historical-priority claim is made for
phase parametrizations or degree-preserving alternating-cycle trades.
The exact local obstruction is reported to prevent spending a future
pass on phase-only repair of the unchanged parent template.
