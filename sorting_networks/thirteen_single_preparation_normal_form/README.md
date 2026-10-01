# B11 single-preparation construction reduction

**six-sorting-1, researcher**, 2026-10-01.

Subsequent result: [the boundary-touch certificate](../thirteen_class13_boundary_obstruction/PROOF.md)
excludes all five class13 tails. It also records the correction of the
displayed proof table: image16 has51 rows and image18 has54. The literal
certificate and the general single-preparation theorem remain unchanged.

Every eleven-event B11 C22 witness can be sought as
`E_minus; A; f; E_plus; T`: at most four effective events precede the
unique unary first10 event f, A is a shortest comparator-function
representative on at most four jointly empty ports, |A|<=5, and T is
an ordinary nine-wire tail of at most11-|A| gates. Loops are moved
within each phase, preserving their order, and never across f.

For the complete repeated-(1,2) parent class13, all5385 effective
orders reduce to six commuting event arrangements and288 local
function cases. Exact prefix activity removes134 of139 image/budget
pairs. The five remaining ordinary nine-wire instances have row/budget
pairs **59/11,56/10,56/10,54/9,51/9**. Their literal row sets and prefix
data are in [certificate.json](certificate.json); the written
arbitrary-depth coverage argument is in [PROOF.md](PROOF.md).
None of the five tails is excluded by this publication. GlobalS13
remains44..45 and B11 remains22..23; this is an existence reduction.

From this directory, use Python3.11+ with assertions enabled:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B generate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B verify.py
```

Standard library only, exact integers, one process/thread and no solver.
The first command recreates the certificate when absent and otherwise
compares it entrywise. Expected status:
`SINGLE_PREPARATION_AND_FIVE_TAILS_GENERATED`.
The second uses independent full13 inverse profiles, all small rank
permutations and scalar simulation. Expected status:
`INDEPENDENT_SINGLE_PREPARATION_AND_FIVE_TAILS_VERIFIED`, with2214
states/22536 edges, monoid counts1,2,11,261,1,214,464 full11 control
function equalities,26,624 clamped inputs,274,432 actual-marked
obstruction checks, and the five row/budget pairs above. Every closure
finishes; no timeout, beam cutoff or solver answer is a proof premise.

All comparator labels in the certificate are zero-based indices in
`combinations(range(11),2)`. Local monoid labels instead use
`combinations(range(j),2)` and the increasing literal J-port list.
`class13.triples` entries are
`[pre_event_labels, first10_label, post_event_labels, multiplicity]`.
`class13.local_map_cases` entries are
`[triple_id, local_map_id, image_id, tail_budget]`.
`class13.image_budget_pairs` adds a representative prefix case ID and
its first prefix activity obstacle `[event,family,domain]`, or null.
`class13.remaining_completion_pairs` identifies the five residual
images and actual prefix cases. `class13.images9[id]` is the full input
set for ordinary directed ports0..8, corresponding to B11 ports1..9
and original ports2..10.

For example, reconstruct every residual B11 prefix and its exact tail
instance without inspecting the exploratory workspace:

```python
import itertools, json
from pathlib import Path
import generate as g
f = json.loads(Path('fixture.json').read_text())
c = json.loads(Path('certificate.json').read_text())
root = (tuple(f['initial_low']), tuple(f['initial_high']), False)
for image_id, budget, case_id in c['class13']['remaining_completion_pairs']:
    triple_id, map_id, _, _ = c['class13']['local_map_cases'][case_id]
    bl, fl, al, _ = c['class13']['triples'][triple_id]
    before = tuple(g.GATES[k] for k in bl)
    state = root
    for gate in before:
        state = g.successor(state, gate)
    J = g.empty(state)
    pairs = tuple(itertools.combinations(range(len(J)), 2))
    labels = c['local_monoids'][len(J)-1]['representative_words'][map_id]
    A = tuple((J[pairs[k][0]], J[pairs[k][1]]) for k in labels)
    prefix = before + A + (g.GATES[fl],) + tuple(g.GATES[k] for k in al)
    print(case_id, prefix, budget, c['class13']['images9'][image_id])
```

A tail witness is translated by +1 to B11 ports, appended to its prefix,
then translated by +1 again and appended to G22. It must be checked on
all158 B11 rows and all8192 original13 Boolean inputs before being called
a44-comparator construction. All36 ordinary nine-wire comparators and
arbitrary serial orders remain legal. No arbitrary wire permutation is
used as a sorting equivalence.

[dependencies.json](dependencies.json) records exact sources and graph
references, including the complementary ten-event result by
six-sorting-2. The [manifest](source-manifest.json) records hashes,
reproduction measurements and malformed-certificate controls. Both
algorithms are by this author; written bridges remain unformalized
and no external-review verdict is asserted. The small comparator-map
catalogue is auxiliary evidence, with no standalone priority claim.
