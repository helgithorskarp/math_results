# One complete moving-core switching decision

This scope is fixed before solving. Let H be the graph induced on vertices
0 through 32 of parent.edges. There are eleven moving C3 triangles and
no fixed vertices in this core. For arbitrary bits s_v, put
H^s_uv = H_uv XOR s_u XOR s_v. Set s_0=0 without loss: adding one to
every bit changes no pair. Decide whether any H^s has neither a red K5
nor a blue K5. One Kissat call is capped at 300 CPU seconds with a
330-second wall guard. UNKNOWN is no conclusion. Finish proof checking
or physical SAT decoding, then checkpoint before any further scope.

## Coverage and relation to the preceding family

The 32 remaining bits give exactly 2^32 distinct labeled cores because
the pairs {0,v} recover those bits. In a 43-vertex extension, all
binom(43,2)-binom(33,2)=375 remaining pairs are free. Thus this complete
family has exactly 2^407 labeled graphs. Every member of the preceding
41-core switching-and-two-attachment family restricts on 0..32 to a
switch of H. Its 2^123 labeled graphs form a proper subset of this
family, by these exact cardinalities. The smaller core requires a new
decision; exclusion of the old larger core does not imply this exclusion.

If H's action g=(0 1 2)...(30 31 32) also preserves H^s, define
d(v)=s_gv XOR s_v. Cancelling H's g-invariance in every switched pair
gives d(u)=d(v) for all distinct u,v. So d is constant. Summing over a
g-cycle of length three forces that constant to zero. Hence s is
constant on each moving triangle. Conversely such bits preserve g.
After normalization there are ten free triangle bits. There are 110
free moving-triangle/fixed-vertex contact orbits and 45 fixed/fixed
pairs. Precisely 2^(10+110+45)=2^165 members preserve this same action.
This counts a subfamily; no symmetry restriction is used in the main
32-bit decision. The switches can change the prescribed minority-core
cross colors, so the name Core186 does not claim a whole minority-core
extension exclusion. The original internal triangle colors are preserved
by the C3-invariant subfamily.

## Exact formula and physical certificate

For each physical five-set and each desired monochromatic color, anchor
one local bit at zero. Its incident edges force the other four bits.
Check all ten pairs. If they agree, these bits and their common
complement are precisely the two assignments making that five-set
monochromatic in that color. Delete assignments contradicting s_0=0.
Negating each remaining assignment gives a clause of width four or five.
Thus the full formula is equivalent to absence of both colors of K5.

The separate auditor enumerates all 32 spins for each of 1,024 possible
five-vertex base graphs, then reconstructs every physical clause. A
compact selected subformula need only contain necessary conditions:
each width-four row adjoins vertex 0 with bit zero; each width-five row
already names five vertices. Under the falsifying bit values all ten
actual switched pairs must have the same color. An UNSAT proof of those
selected conditions suffices even without trusting full-formula completeness.

The disclosed generic DRAT kernel keeps clause multiplicities. RUP tests
unit propagation after negating a candidate clause. For a non-RUP clause
C with first literal p, every clause D containing -p must make
C union (D minus {-p}) RUP. These tests preserve satisfiability: if a
model falsifies C, flip p to satisfy it. Only clauses D containing -p
can become false. RUP of the displayed clause forces some literal of
D other than -p to be true in the old model, so D remains satisfied.
This argument also permits fresh variables. A tautological tested
resolvent is automatically implied. Deletions only weaken the formula;
the final RUP empty clause proves contradiction. No line may follow it.

## Evidence requirements

Freeze input and production source hashes before the solve. Compare
the complete formula and audit in normal and optimized Python; keep
the old source, formula, proof and logs untouched. Validate local truth
tables, physical-clause decoding, proof multiplicities, fresh RAT
variables and corrupted certificates. The independent physical checker
imports neither generator nor solver. Its proof kernel is reused from
the previous package, ultimately the teammate's Paley package; this is
disclosed reuse, not an independently rewritten proof algorithm.

UNSAT is claimed only after a complete physical proof check. SAT requires
the complete 33-vertex edge list and an independent check of every
five-set; it is not a 43-vertex target. All 17 whole C3 classes and the
global Ramsey problem remain open unless separately resolved. No
catalog completeness, old heuristic correctness, degree bound or prior
switching exclusion is a premise of the new physical certificate.
