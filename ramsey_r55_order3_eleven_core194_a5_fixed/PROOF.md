# Complete fixed-attachment cover of the two Core194 a=5 moving types

The action is (0 1 2)...(30 31 32), with fixed vertices 33,...,42.
The first four moving triangles are internally red and induce the
Core194 word 100110110110110100; the remaining seven are internally blue.
The distinguished empty fixed pair u=33,v=34 is BLUE, and both endpoints
are blue to the twelve red-core vertices. The independently accepted pair
lemma says their common blue neighborhood is exactly that core. Thus
every other moving triangle and fixed vertex has contact RR, RB or BR.
This statement does not guarantee existence of a blue empty pair.

Let (a,b,c) be the moving contact counts and (x,y,z) the other fixed
contact counts, in RR,RB,BR order. Then a+b+c=7, x+y+z=8, and the red
endpoint degrees are 3(a+b)+x+y and 3(a+c)+x+z. The imported theorem
R(4,5)=25 implies the degree window 18,...,24 in a 43-vertex target.
The accepted attachment cover allows b<=c and, when b=c, y<=z.

This milestone addresses ONLY the complete a=5 stratum:

* (5,0,2): the degrees are 23-z and 29-y. Exactly the ten nonnegative
  triples with x+y+z=8 and y>=5 meet the degree window. Here b<c fixes
  the endpoint orientation. Sorting fixed vertices 35,...,42 by contact
  preserves the moving normalization.
* (5,1,1): the degrees are 26-z and 26-y. Exactly the triples with
  y,z>=2 and x+y+z=8 meet the window. There are fifteen ordered triples,
  or nine with y<=z. To normalize a word with y>z, swap u,v AND swap
  moving triangles 9 and 10 phase-preservingly, then sort the fixed
  vertices. The first five blue triangles 4,...,8 have RR contact,
  triangle 9 has RB contact and triangle 10 has BR contact. The coupled
  swap restores these moving contacts. Swapping endpoints alone fails
  to preserve this already fixed moving assignment.

These are relabelings of the family, not assertions that they are
automorphisms of individual graphs. Each commutes with the stated C3
action, fixes the red core pointwise and preserves the distinguished
unordered pair and all internal colors. The direct base has no row-order
constraint. Literal Ramsey constraints and the symmetric pair consequences
are invariant under the relabelings. Seven adjacent transpositions of
the other fixed vertices generate their sorting group; together with
the coupled endpoint/triangle swap they cover every required map.
Graphs with multiple choices of distinguished pair can have several
representatives. This is a full extension cover, not an isomorphism census.

The producer filters the accepted 119-profile certificate. The separate
audit imports the physical orbit utility but no profile producer. For
each moving type it visits all 3^8=6,561 fixed words, computes literal
red degrees, constructs the actual 43-vertex normalization map and
checks transport of all thirty contacts. It checks vertex/C3/320-primary
bijections and reconstructs the normalized units physically. It matches
every count, degree, full-star weight and unit in all nineteen profiles.
For (5,0,2), 21 moving placements and two pair orientations multiply
the fixed-word count by 42. For (5,1,1), there are 42 moving placements;
its normalized fixed-word histogram already combines the two endpoint
orientations when unequal. The total is 195,342 labeled star assignments
in the degree relaxation, not 43-vertex graph realizations.

In addition to the ordinary invariance argument, all 366,069 complete
base clauses are checked under each of the eight generating permutations,
and the relevant fourteen moving units are checked as a set. A deliberately
uncoupled endpoint swap is rejected as a moving normalization. Eight
corrupted profile certificates and seven corrupted complete child files
are rejected. These controls supplement, rather than replace, the proof.

Every complete child keeps the entire independently reviewed direct BLUE
base (320 primary variables, 366,069 clauses) and appends thirty units:
fourteen moving and sixteen fixed contacts. Each child has 320 variables
and 366,099 clauses. All unmentioned edges and fixed-core incidences remain
free. There is no additional local relaxation, selected degree profile,
M stratum or symmetry constraint. Complete base bytes, physical unit tail,
header and EOF are checked against a freshly reconstructed base. The
base generator and its checker use distinct arithmetic/orbit and
five-set/possible-clique constructions.

Checked UNSAT excludes the corresponding complete fixed profile. All ten
or all nine checked refutations would exclude the corresponding entire
moving type; all nineteen would exclude the entire a=5 stratum. A single
SAT requires a complete 320-primary model, evaluation of every clause,
compact edge list and the separate literal five-set/action/core/pair graph
checker. UNKNOWN, timeout and partial proof trace establish no exclusion.
No claim of exclusion follows from an unchecked solver exit.

The bounded production uses one 90-second solver call per case and two
workers. Each actual UNSAT must pass full DRAT including RAT, in production
and again against fresh reconstructed formulas under optimized Python.
Sources, solver/checker binaries and case evidence are hashed. Hashes are
identity checks, not proof substitutes. Pending refutations are checkpointed
before checking. Same-contract resume preserves UNKNOWN outcomes and
finishes or replays certificates. A STOP file prevents queued starts while
active bounded jobs finish.

The direct base, pair lemma, original attachment cover, five earlier moving
type exclusions, and the entire (6,0,1) exclusion have independent accepted
reviews. The new specialized a=5 cover/formulas/refutations remain a new
author-checked trust boundary until independently reviewed. Exact Python,
ordinary finite counting and relabeling, physical encoding, imported
R(4,5)=25, hardware and the full DRAT checker remain trusts. Two author
proof replays do not constitute peer review or formalization.

Even exclusion of all nineteen profiles would leave moving type (4,1,2),
the RED-pair branch, whole Core194, and all seventeen current whole classes
open. No Ramsey lower-bound improvement follows. The pass stops after this
nineteen-profile decision checkpoint, before any other type or phase.
