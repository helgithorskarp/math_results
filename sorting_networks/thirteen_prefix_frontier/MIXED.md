# Mixed pruning splits both completion frontiers into two route branches

Author and executing agent: **six-sorting-1, researcher**.

For each of the explicit eleven-wire sets Y1 (146 states) and Y2 (145
states), every standard **20-comparator** sorting suffix satisfies at least
one of these conditions:

* **Maximum branch:** wire 10 appears in exactly one comparator, (9,10).
* **Minimum branch:** (0,1) appears exactly once; wire 1 is unused before
  that comparator, and wire 0 is unused afterward.

Thus the fixed thirteen-input prefix problem reduces to **four restricted
construction targets**, with arbitrary depth. A sorter satisfying either
branch suffices; the branches can overlap. Bounded probes are recorded in
`filtered_report.json`; they provide no nonexistence certificate. The global
44-versus-45 question and these conditional 20-versus-21 targets remain open.

The result refines the [two-frontier reduction](README.md), source commit
`e6f17bb707fbe6c5116221552578acedb6fada01`. That proof uses
[six-sorting-2's three-kernel lemma](../../sorting13_prefix21_maximum_kernel/README.md),
source commit `3461182332a9d3fb00ec70a4ac3772dfa38b9c10`. The input sets,
prefixes and original extreme bounds are unchanged in `certificate.json`.

The new `mixed_certificate.json` supplies **134 distinct bounds** with
smaller numerical right sides than the sums of the earlier separate
maximum/minimum bounds. It also records all eighteen entries of the two
three-by-three single-extreme tables; fourteen repeat entries among the 134.
The independent checker validates 152 witness entries, including repeats.
The proof needs witnessed counts, not a claim that those counts are maximal.

## Mixed deletion bound

Fix some original inputs to the largest values, some to the smallest, and
leave k middle values arbitrary. Mark these groups by colors 2,0,1,
respectively. A standard comparator acts as min/max on the colors regardless
of the ordering of values within a group. Deleting gates touched by an
extreme leaves a sorting circuit on the k middle inputs. A gate touched by
both groups is counted once.

If the24-gate prefix deletes D gates and a proposed20-gate suffix deletes
H gates, its surviving sorting circuit has at most44-D-H gates. The
established lower bound L(k) therefore gives

    H <= 44 - L(k) - D.

This is an application of established extreme-value pruning, not a new
general pruning theorem. Standardization and pruning are explained in
[Harder, arXiv:2012.04400v3](https://arxiv.org/abs/2012.04400v3). In particular,
[Codish et al., arXiv:1405.5754v3](https://arxiv.org/abs/1405.5754v3) proves
S(9)=25; the lower-bound array and the published S(13)>=44 deduction are
documented in the preceding README. For a21-gate control, replace44 by45.

In each prefix, assign original inputs **{2,3,5}** to the three largest
values, input **10** to the smallest, and leave nine middle values. Exactly
**16** prefix gates touch an extreme. Two maxima exit on wires11/12; the
remaining maximum exits on wire10 and the minimum on wire1. The certificate
encodes this assignment as base-three738391. Hence any20-gate suffix has

    H(maximum from10 OR minimum from1) <= 44 - 25 - 16 = 3.

The earlier separate bounds give two passages for each route, allowing a
sum of four. The mixed count includes their union, with an intersection
counted once. The other witnessed single-high/single-low capacities are:

| Maximum start | Y1: min0 | Y1: min1 | Y1: min5 | Y2: min0 | Y2: min1 | Y2: min5 |
|---|---:|---:|---:|---:|---:|---:|
| 6 | 5 | 4 | 6 | 5 | 4 | 5 |
| 9 | 5 | 4 | 6 | 5 | 4 | 7 |
| 10 | 4 | **3** | 4 | 4 | **3** | 5 |

All table entries use S(9)=25. The 134 selected bounds have seven or
nine middle wires and use the established S(7)=16 or S(9)=25.

## Why the two central routes are disjoint

A20-gate sorter of either set gives a44-gate thirteen-input sorter after
its24-gate prefix. The published lower bound44 implies that no gate can be
redundant on all Boolean inputs; otherwise deletion gives a43-gate sorter.
In particular, every suffix gate must act nontrivially on some row in Yj.

Direct checks of both complete input sets give **bit1<=bit10** initially.
Let t be the first (0,1) comparator. It must exist, because the input with
its only zero on wire1 must finish with that zero on wire0.

Before t, wire1 cannot increase: without (0,1), it can only meet higher
channels and receive min. Wire10 never decreases. Thus (1,10) is redundant
before t. At t, wire0 receives min(previous0,previous1), which is at most
the previous wire10. Thereafter wire0 never increases and wire10 never
decreases. Thus (0,10) is redundant after t.

The one-hot input on wire10 stays fixed, so its passage count qH equals
the number of gates using wire10. In the single-zero input on wire1, the
zero stays on1 before t, then stays on0 afterward. A gate shared by these
two tracked routes would therefore be (1,10) before t or (0,10) after t.
Both are redundant and absent. The tracked gate sets are disjoint, giving

    qH + qL = H <= 3.

Both qH and qL are at least one. Wire10 must receive a one from the one-hot
input on9; the zero on1 must reach0. Consequently **qH=1 or qL=1**.

If qH=1, the unique gate involving10 is (9,10), since the one initially
on9 cannot leave9 by any other gate before it. If qL=1, its sole passage
is (0,1); every earlier gate involving1 and every later gate involving0
would be another passage. These are exactly the two stated branches.
Conversely any20-gate sorter in either branch is a completion of Yj, so
the disjunction is a complete existence reduction. No gate is added and
no layer count is selected.

For Y1, the stronger initial rectangle
max(bits0,1,2,3)<=bit10 persists under every standard comparator: a prefix
maximum cannot increase and a suffix minimum cannot decrease. Therefore
(0,10),(1,10),(2,10),(3,10) are permanently redundant and may be forbidden.
Y2 does not satisfy that rectangle; its proof uses the phase argument above.

## Branch-specific shortcut consequences

The existing certificate bounds the one-hot route from6 and the single-zero
route from5 by three passages. The maximum branch must include one of

    (6,8), (6,9), (7,9).

The one from6 must reach9 before the unique (9,10), leaving at most two
earlier passages. Without a listed gate, the directed path6->9 needs three
moves. This sharpens [six-sorting-2's six-type shortcut corollary](../../sorting13_pruned11_shortcut/README.md),
source commit `5a9a621797abcf8ec702a62c15a7ee0c033d9d04`.

The minimum branch must include one of

    (0,3), (0,4), (0,5), (2,5).

The zero from5 must reach0 before (0,1), which contributes another stationary
passage. Wire1 is unavailable before that pivot. Without a listed gate,
the shortest descending path5->0 through {0,2,3,4,5} needs three moves;
at most two earlier passages are available. The independent checker
replays both small directed-distance calculations. These disjunctions are
optional SAT propagation clauses, not additional assumptions.

## Why both input sets remain necessary

There is no coordinate permutation sending Y2 into Y1. Their sizes differ
by one, so such a mapping would identify Y2 with Y1 after deleting one row.
Column6 of Y2 contains123 ones. A column of Y1 would then contain123 or124
ones. Its column sums are

    [35,11,61,62,69,59,121,61,70,118,141],

which contain neither value. The reverse inclusion is excluded by cardinality.
This only rules out this simple permutation-subsumption relation.

## Reproduce and inspect the certificates

Use ordinary CPython3.11.2 without `-O`, GCC12.2.0 or a C++17 compiler, and
one process/thread at a time. From this directory:

    mkdir -p scratch
    g++ -O2 -std=c++17 -Wall -Wextra -Wpedantic mixed_prefix_enum.cpp -o scratch/mixed-prefix-enum
    python3 generate_mixed.py --binary scratch/mixed-prefix-enum --check
    python3 verify_mixed.py

The C++ generator uses ternary colors and enumerates 1,532,883 inputs with
at least two marked maxima per prefix. It collects 4,070/4,054 nested output
pairs and selects the compact witnesses. The Python checker imports neither
generator nor SAT code: it decodes each witness, assigns thirteen distinct
ranks in three blocks, and checks the deleted-gate count, both residual
threshold rows, the pruning bound and the21-gate control. It also checks
the initial orders, column obstruction and branch shortcut distances.
The mixed certificate SHA256 is

    c4434c95c9a359916c8b93fb40661815d19b21dfe3d75043a2a1cf2b3e392a83.

The optional solver layer uses the unchanged baseline `sat_encoding.py` and
the pinned packages in `requirements.txt`. Add your workspace-local solver
environment to PYTHONPATH; set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS and
MKL_NUM_THREADS to1. Additional controls:

    PYTHONPATH=scratch/solver-env python3 check_filters.py
    PYTHONPATH=scratch/solver-env python3 filtered_search.py --case 2 --budget 21 --route-branch min_once --mixed-bounds mixed_certificate.json --branch-shortcut --freeze-known --seconds 45 --segments 1 --out scratch/positive.json
    PYTHONPATH=scratch/solver-env python3 filtered_search.py --case 2 --budget 20 --route-branch max_once --mixed-bounds mixed_certificate.json --branch-shortcut --seed-deletion 19 --seconds 45 --segments 2 --out scratch/search.json

The filters also apply the published future-component theorem and fixed
edge bits from [Codish et al., arXiv:1507.01428v1](https://arxiv.org/html/1507.01428v1),
Theorem2 and Lemma1. Each comparator is its own sequential slot, retaining
arbitrary allowable depth. Future components are intervals; a gate can be
within one component or join adjacent ones. Pure-side cut clauses follow
from conservation of ones, and disjoint adjacent gates can be ordered
lexicographically without changing cost or extreme-touch totals. No
co-saturation step adds comparators to a size budget.

`check_filters.py` checks 9,452 complete short words, 2,916 mixed-path bounds,
9,216 partial eleven-wire branch words, and 4,681 first-pivot phase words,
using independent scalar/union-find predicates. It retains a sorter with
an internal future-component gate. Known21-gate controls satisfy both
branches and are checked directly on all8,192 original Boolean inputs.
The optional `--no-phase-bans` reproduces the earlier maximum-branch probe;
`--branch-shortcut` adds the proved small disjunction. Actual probe flags,
formula hashes and UNKNOWN results are in `filtered_report.json`.

The analytic argument is not formalized. Both implementations are by this
researcher; independent algorithms do not constitute external review.
Published lower bounds remain dependencies. No solver timeout, unchecked
UNSAT answer or incomplete search is used as a mathematical exclusion.
