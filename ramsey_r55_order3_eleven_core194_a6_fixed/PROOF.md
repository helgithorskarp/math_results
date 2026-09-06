# Three complete fixed-attachment cases for the (6,0,1) moving type

Use the action (0 1 2)...(30 31 32), fixing 33,...,42, with four
internally red triangles inducing Core194 and seven internally blue
triangles. The distinguished empty fixed pair u=33,v=34 is blue; both
vertices are blue to the twelve red-core vertices. The accepted local
pair theorem gives their common blue neighborhood exactly that core.

Assume the normalized moving contact counts (RR,RB,BR) are (6,0,1).
Triangles 4,...,9 are red to both endpoints. Triangle10 is blue to u
and red to v. Each other fixed vertex has contact RR, RB or BR; BB is
impossible by the pair theorem. Write their counts (x,y,z), summing to8.
The red degrees are 18+x+y=26-z and 21+x+z=29-y. The imported theorem
R(4,5)=25 bounds both color degrees on43vertices by24. Hence z>=2 and
y>=5. With x>=0, these conditions leave EXACTLY

```
(x,y,z) = (0,5,3), (0,6,2), (1,5,2).
```

Their red endpoint degrees are (23,24),(24,23),(24,24). Each satisfies
the full degree window18..24. Conversely every fixed word satisfying
that window has one of these counts. For this specified ordered moving
assignment, the labeled word counts are56,28,168, summing to252 out of
3^8=6,561. With the seven choices of exceptional moving triangle and
pair orientation, the inherited full star weights are784,392,2352,
summing to3528. These are star counts, not graph counts or realizations.

Every permutation of fixed vertices35,...,42 commutes with the C3 action,
fixes every moving vertex and u,v, and preserves all literal Ramsey
constraints and the symmetric blue-pair consequences. The direct base
has no row order. Thus sort the other fixed vertices RR, then RB, then
BR. This preserves the already normalized moving assignment. The three
cases cover every full extension of the (6,0,1) type, allowing relabeling.
They do not assert those permutations are automorphisms of individual
solutions. No reorientation identifying the first two degree pairs is
imposed. A graph with several distinguished pairs may have several
representatives: this is a cover, not an isomorphism census.

The producer filters the prior119-profile certificate. The independent
fixed-word checker enumerates all6,561 words, reads physical red degrees,
checks sorting as actual43-vertex permutations commuting with C3 and
inducing320-primary bijections, and reconstructs all90 unit meanings
from physical pair orbits. It agrees on the three profiles entrywise.

Each complete formula retains the entire reviewed direct BLUE base
(320variables,366,069clauses) and appends30 units:14 moving and16 fixed
contacts. Its header is320variables,366,099clauses. All other graph
edges and fixed-core incidences remain free. The full base includes
every literal no-monochromatic-K5 constraint under the fixed action
and core. This is a complete full-graph extension, not a local test.
Complete body bytes, all physical tail units, header and EOF are checked.

A checked UNSAT refutes precisely that full fixed profile. If all three
are checked UNSAT, the preceding exhaustive cover excludes the entire
(6,0,1) moving type. A single SAT requires a complete primary model,
clause evaluation, compact edge list, and independent literal all-five-
set/action/core/pair checks. UNKNOWN, timeout, partial trace or solver
exit without checked evidence proves no exclusion or realization.

Production and fresh optimized verification require full DRAT including
RAT for every UNSAT, each against a complete reconstructed formula.
Source and file hashes are identity checks, not proofs. The direct base
and local pair theorem have accepted independent reviews. The parent
attachment cover and five prior type exclusions remain distinct inherited
review boundaries. This three-case counting/sorting argument is explicit
above; exact Python/hardware, importedR(4,5)=25, physical encoding and full
DRAT correctness remain trusts. Internal different code paths and two
proof replays are not independent peer review or formalization.

Closing this moving type would still leave the other types(4,1,2),
(5,0,2),(5,1,1), the RED-pair branch and whole Core194 unresolved. It
would not remove any of the17 remaining whole four-versus-seven classes
or improve the Ramsey lower bound. No further type is searched here.
