# Complete Core194 (4,1,2) fixed-attachment cover

Fix the action (0 1 2)...(30 31 32), fixing vertices 33,...,42.
Moving triangles 0,...,3 are internally red, inducing Core194 with word
100110110110110100; triangles 4,...,10 are internally blue. The marked
empty fixed pair u=33,v=34 is BLUE, and both endpoints are blue to the
twelve red-core vertices. The independently accepted pair lemma gives
their common blue neighborhood exactly that core. Thus every other
moving triangle and fixed vertex has contact RR, RB or BR, never BB.

Assume the normalized moving contact counts are (4,1,2). The first four
blue triangles 4,...,7 have RR contact, triangle 8 has RB contact, and
triangles 9,10 have BR contact. Let (x,y,z) count the eight other fixed
vertices of types RR,RB,BR. Then x+y+z=8 and the red endpoint degrees are

    d_R(u)=15+x+y=23-z,  d_R(v)=18+x+z=26-y.

The imported theorem R(4,5)=25 bounds both color degrees by 24 in a
43-vertex Ramsey(5,5) graph, giving red degrees in 18,...,24. The window
is equivalent here to y>=2 and z<=5, in addition to nonnegativity and
x+y+z=8. For y=2,...,8 there are respectively 6,6,5,4,3,2,1 choices of z,
giving exactly 27 full fixed profiles. The other endpoint orientation
has moving counts (4,2,1) and is normalized by the accepted parent cover.
Within (4,1,2), no further endpoint swap or identification of y,z is used.

For the specified ordered moving assignment, every permutation of fixed
vertices 35,...,42 commutes with C3, fixes all moving vertices and u,v,
and preserves the literal Ramsey constraints and symmetric pair
consequences. The direct base has no row order. Sorting the fixed vertices
RR, then RB, then BR therefore covers every full extension of the moving
type without disturbing its fourteen moving units. These are relabelings
of a family, not asserted automorphisms of individual solutions. Multiple
marked pairs may represent a graph, so this is a cover, not an isomorphism
census. No existence of a BLUE empty pair in every graph is assumed.

For a physical census, of all 3^8=6,561 words, the counts with y>=2 total
6,561-2^8-8*2^7=5,281. Among them exactly 28 have z>=6 (y=2,z=6,x=0).
Hence 5,253 words meet the full window. The inherited labeled full-star
weight is 210*5,253=1,103,130: 7!/(4!1!2!)=105 moving placements and two
pair orientations. These are star assignments, not graph realizations.

The producer filters the accepted 119-profile certificate. A separate
checker imports physical orbit utilities but no profile producer, visits
every fixed word, computes literal degrees and checks the actual thirty
contacts under each sorting map. It checks vertex/C3/320-primary bijections
and all 810 normalized unit meanings, matching every count, degree, weight
and unit in the 27 profiles. The complete base's 366,069 clauses are checked
under each of seven adjacent fixed transpositions: 2,562,483 clause images.
All fourteen moving units are preserved. Eight malformed profile records
and seven malformed complete child files are rejected.

Every child retains the entire independently reviewed direct BLUE base
(320 variables, 366,069 clauses), appending 30 physical units: fourteen
moving and sixteen fixed contacts. Each complete child has 320 primary
variables and 366,099 clauses. All unmentioned edges and fixed-core
incidences are free. No selected degree sequence, M stratum, added symmetry
rule or local relaxation is used. Fresh arithmetic/full-five-set generation
and physical-orbit/possible-clique reconstruction agree on the complete
base; every body byte, physical tail, header and EOF is checked.

A checked UNSAT excludes exactly its complete fixed profile. All 27
checked refutations would exclude the entire (4,1,2) moving type. Combined
with the earlier five moving exclusions, complete (6,0,1) closure and
complete a=5 closure, that would exclude EVERY BLUE empty pair in Core194.
Consequently the empty fixed vertices would form a red clique; there are
at least two by the accepted multiplicity theorem and at most four since
a red clique of size five is forbidden. This is a direct conditional
corollary of complete closure, not a new red-branch search.

A SAT outcome requires a complete 320-primary model, clause evaluation,
compact edge list and separate literal five-set/action/core/pair checking.
UNKNOWN, timeout, partial trace and unchecked exit establish no exclusion.
The bounded contract uses two workers and one 90-second call per case;
every actual UNSAT must pass full DRAT including RAT in production and
again against fresh complete formulas under optimized Python. Hashes
identify files, not proofs. Pending proofs are saved before checking;
same-contract resume preserves UNKNOWN and rechecks terminal evidence.
STOP prevents queued starts while bounded active work finishes.

The direct base, pair lemma, original cover, five earlier exclusions,
complete (6,0,1) closure and multiplicity theorem have accepted independent
reviews. At this frozen contract, the a=5 closure and this new specialized
27-profile cover/formulas/refutations remain unreviewed independently.
Any combined blue-branch closure imports the a=5 boundary explicitly.
Ordinary finite counting/relabeling, exact Python/hardware, physical
encoding, imported R(4,5)=25 and the full DRAT checker remain trusts.
Author cross-checks and two proof replays are not peer review or formalization.

Even complete blue-branch closure would leave the RED-pair branch, whole
Core194 and all 17 current whole classes open. It would not improve the
Ramsey lower bound or establish a target graph. This pass stops at the
complete 27-profile decision checkpoint, before any red-branch or other
major proof phase.
