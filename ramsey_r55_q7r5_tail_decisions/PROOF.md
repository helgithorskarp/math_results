# Complete residual decisions remove complete physical43 tasks

Red means an edge. A good43 is a graph of order 43 with no red or blue K5.
The finite statement proved here is recorded entry by entry in RESULTS.json:
exactly the cores listed in TASKS.json as excluded have no tail of the form
below. Every retained core has a literal 23-vertex tail witness. There are no
undecided tail cases. Retained full 43-vertex tasks remain UNKNOWN.

## Connection to the complete global family

In the h3887 task `bo1-q7-r5-cIIIIII`, vertices 0..19 form five disjoint red
K4 blocks, vertices 20..23 and 24..27 form two blue K4 blocks, and vertices
28..42 induce catalog core I. The whole set 20..42 is the residual after
red K4 exhaustion. It contains no red K4. As an induced subgraph of a good43,
it also contains no blue K5. These are constraints of the original complete
physical task, rather than an extra hypothesis about its unknown edges.

Relabel that residual internally as follows:

    tail 0..14  -> physical 28..42 (catalog core C),
    tail 15..18 -> physical 20..23 (blue clique U),
    tail 19..22 -> physical 24..27 (blue clique V).

Leave every edge between C,U,V free. A negative decision of this *entire*
tail problem implies UNSAT for the corresponding full physical43 task.
A positive tail decision supplies no values on the other 20 vertices and
does not imply a full-task SAT result.

Thus removing all certified negative indices from the q7,r5 macro class,
and retaining every other h3887 task, preserves its global target cover.
No carrier denominator, q10 child count, or separate reduction percentage is
multiplied into this calculation. In particular q7,r7 at the same core index
is a different task and is not excluded by this result.

## Exact physical tail encoding

There are 120 core-to-block edges and 16 U-to-V edges, hence 136 Boolean
physical variables. They are numbered from one in lexicographic order of
unordered tail pairs. All 105 core edges and twelve internal blue edges are
fixed. There is no constant variable in this encoding.

For every four-subset, forbid all six edges red. For every five-subset,
forbid all ten edges blue. A clause is omitted precisely when a fixed edge
already satisfies it; otherwise substitute only the fixed edges and retain
every remaining physical literal. This is necessary and sufficient for the
tail property. Red K5s are already impossible because red K4s are forbidden.

An independent polynomial count checks the clause totals. If the core has
e red edges, t red triangles, and u blue triangles, the physical layer has

    red-four clauses = 16e + 8t,
    blue-five clauses = C(8,5) + 15 C(8,4) + (105-e) C(8,3) + u C(8,2).

Every catalog core is checked literally to have neither color K4. No
unverified isomorphism finder or automorphism census is used.

## Normalization used to decide the tail

For x in U or V let its signature be the unsigned 15-bit word of red
adjacency to core vertices, with core vertex i contributing bit i.
Independently sort the four vertices of each blue block in nondecreasing
signature order. Then swap U and V if necessary to put their complete
60-bit signature words in nondecreasing order. This relabels every tail
edge, including U-to-V edges, and fixes the core labels. Both blue blocks
have the same size and fixed internal color, so these are always permitted
isomorphisms of the tail problem. Ties remain allowed.

Every tail therefore has at least one normalized labeling, and every
normalized model is a tail. No full-graph automorphism is assumed. No orbit
count is needed. The six 15-bit comparisons and one 60-bit comparison use
143 prefix-equality variables, numbered 137..279, and 858 clauses.

For each comparison, p denotes equality of all earlier, more significant
bits (true before its first bit). At current bits x,y enforce

    p -> (x <= y),
    z <-> (p and (x = y))

when a next prefix z is needed. The last bit has only the first constraint.
The published auditor checks the complete truth table of every actual gate,
including the initial constant-prefix and final-bit cases. Induction shows
the conjunction is equivalent to unsigned word order, with a unique
auxiliary extension for each physical assignment satisfying that order.

This normalization is used *inside the residual decision*. It is not
appended to the original h3887 physical formulas: independently imposing
both labeling conventions on a full graph would require an additional
compatibility proof. The receiving interface instead removes whole tasks
whose tails are impossible and emits the unchanged parent formula for each
retained task. A saved positive tail is not fixed during emission.

## Complete finite computation and independent checks

All 640 catalog indices, in their original order, are included. Each exact
279-variable formula is solved by the CaDiCaL300 engine in python-sat
1.9.dev15. There is no timeout verdict in the completed table. Every UNSAT
has a complete independently checked DRAT proof for its exact formula.
Every SAT has a physical edge word checked by direct enumeration of all red
four-subsets and blue five-subsets. RESULTS.json binds each original CNF
and negative proof to its SHA-256; TAIL_WITNESSES.json supplies every positive
physical tail. Proofs are not assumed unique across replays.

The auditor imports no encoder code. It decodes graph6 through a separate
integer/matrix implementation, reconstructs the entire physical literal
stream, checks the independent clause-count formulas, and exhaustively
checks the actual comparator gates. The positive and negative controls
exercise complete tail relabelings, tied signatures, corrupted formulas,
false witnesses, and all assignments of short comparator circuits.
VALIDATION.json records the completed checks and their measured scope.

Bulk generated CNFs and proof streams stay outside Git. `reproduce.py`
regenerates and checks every case with the published tool/input pins.
The fast `verify.py` mode audits encodings and saved SAT witnesses; it does
not claim to recheck negative proofs without `--run` and `--drat-trim`.

## Trust and limitations

Each individual exclusion needs only its fixed literal core and the finite
proof computation. Catalog completeness is an imported premise of the
h3887 *global coverage* theorem, not a premise that turns a solver timeout
into a decision. The author catalog is
https://users.cecs.anu.edu.au/~bdm/data/ramsey.html ; exact input hashes and
parent source identities are in INPUTS.json.

Remaining trust includes the unformalized reduction, Python exact-integer
and file semantics, the published encoder/auditor, DRAT verification,
toolchain/runtime and hardware. This is not a proof-assistant formalization
or an external review of the new result. No historical-priority claim is
made for residual decision or clique-block relabeling.

The unfinished exploratory encodings and conditional-core traces are not
premises of any published decision. No fixed H92/H93 subsystem, failed
good19 packing bridge, saved-parent repair, ambient deletion, or invalidated
h3687 automorphism claim is used. The 161 h3987 q10 children remain UNKNOWN.
No good43 is constructed, and no Ramsey lower-bound improvement is proved.
