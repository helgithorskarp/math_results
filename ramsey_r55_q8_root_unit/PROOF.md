# A forced physical edge in the entire q8,r8 family

Let M8 be the complete q8,r8 formula published in h4149. It has eight red
K4 blocks B_i={4i,...,4i+3}, i=0,...,7, and eleven variable core vertices
32,...,42. Every other physical edge remains a decision. M8 imposes all
red and blue K5 prohibitions, root-column ordering, and nonincreasing
root-to-block matrix words W_1 >= ... >= W_7. Its exact DIMACS identity is
given in DEPENDENCIES.json.

**Theorem.** M8 implies the red edge {3,4}, variable 119. Consequently the
complete physical branch M8 AND -119 is unsatisfiable. This holds for every
core assignment, including all 546,356 listed q8,r8 core tasks.

**Proof.** The root signature of column v of B_1 is

    s_v = sum_{u=0}^3 adjacency(u,4+v) * 2^u.

These signatures are nonincreasing. If {3,4} is blue, s_0<8. Hence every
s_v<8, so vertex 3 is blue-adjacent to all four vertices of B_1. In the
root-to-block word

    W_i = sum_{u,v=0}^3 adjacency(u,4i+v) * 2^(4u+v),

the row for vertex 3 comprises the four highest bits. Thus W_1<4096.
Whole-block ordering gives W_i<4096 for every i=1,...,7. Vertex 3 is
therefore blue-adjacent to all 28 vertices of B_1 union ... union B_7.

Take any 25 of these vertices. The classical theorem R(4,5)=25, with the
colors exchanged, gives a red K5 or a blue K4. A red K5 contradicts M8
directly. A blue K4 extends with vertex 3 to a blue K5, also contradicting
M8. This proves the theorem. No edge in or incident with the eleven-vertex
core was used. QED.

The imported theorem is B. D. McKay and S. P. Radziszowski, *R(4,5)=25*,
Journal of Graph Theory 19 (1995), 309--322, available from the
[author's paper](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
We use its upper-bound direction. This pass does not replay that substantial
computer-assisted proof. No new Ramsey bound or historical priority for
this elementary normalization consequence is asserted.

## Exact certificate and its trust boundary

The certificate assumes only -119 and derives the 28 negative physical
literals for edges {3,v}, v=4,...,31, from the actual M8 clause IDs. Its
240 steps are checked as hinted RUP by the h4149 checker. A separate
implementation checks the same steps by binary resolution and substitution
of established units: 192 resolution steps and 48 unit substitutions under
that classification. It imports neither the producer nor the RUP checker.
An additional direct enumeration checks all 65,536 root matrices against
the signature-order definition.

The producer first resolves out the six lower signature bits in each of
the three adjacent B_1 column comparisons. It then propagates through the
actual whole-block comparator clauses. The complete base file is hashed;
the proof checker reads its cited clauses by their original IDs. The
parent source manifest is pinned and checked. The full physical meaning
of that base is imported from h4149's encoding proof and audits.

The final certificate step applies the cited Ramsey theorem to physical
vertices 4,...,28 and vertex 3. It is a mathematical deduction with an
explicit external premise. **It is not a full LRAT or RUP refutation of
M8 AND -119.** The protocol name and result status distinguish this mixed
certificate from h4149's purely propositional certificates. In particular,
it must not be passed to `worker.py import-lrat` or silently inserted as a
RUP refutation. Neither implementation is reviewer-1's independent verdict.

## Complete queue effect and the original-task limitation

For each of the 239 r=8 core guards A_j from h4149, the two physical jobs

    M8 AND A_j AND -119,     M8 AND A_j AND 119

are a disjoint and exhaustive split of the original cohort job. The first
has the above refutation. The second retains every possible good43 in
that cohort. All 239 guards have nonempty catalog membership, and together
they contain all 546,356 q8,r8 original task IDs. An independent bitset
consumer checks disjointness and complete coverage without traversing the
producer's core tree.

The negative branches are not merely empty catalog guards: for every
listed core, setting all cross edges blue respects the fixed blocks, core,
root-column order and whole-block order, and has -119. It fails the full
Ramsey constraints, as this theorem requires. This observation is only a
scope check, not a target graph or an additional search result.

The actual dispatcher refuses to materialize all 239 negative workers and
materializes each positive sibling using the unchanged h4149 full43
materializer. Every produced body is compared literally with the complete
M8 body followed by exactly its core guard and +119. The resulting active
queue still has 956 jobs: 239 constrained positive jobs and 717 unchanged
q8,r5--7 jobs. The complete original q8,r8 dispatch stream retains every
original ID and core word and adds physical unit 119.

**No original fixed-core task is excluded.** There are zero new original
task verdicts and zero candidates. All 2,185,424 q8 original tasks remain
UNKNOWN, and the preexisting global administrative registry remains 518
certified exclusions and 2,188,660 UNKNOWN IDs. The 239 closed physical
branches must not be added to the 518 original-task exclusions. The work
does not access the separate 161-child q10 ledger.

This is measured propagation into actual dispatched physical jobs. It is
not a solver-speed measurement, a new carrier percentage, or completion of
the principal's original-task/candidate gate. That gate remains UNKNOWN;
no target solver was invoked. The pass ends with a mechanism review and
checkpoint rather than starting another cohort, parameter, or backend.
