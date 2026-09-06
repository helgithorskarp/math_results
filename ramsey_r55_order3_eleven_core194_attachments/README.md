# Nine complete attachment cases for a Core194 blue empty pair

Every blue empty fixed pair in a full Core194 extension has **at least
one internally blue moving triangle red to both endpoints**, and at
least one red to exactly one endpoint. Its joint contacts reduce to
**nine moving-cycle types and 119 joint degree profiles** under explicit
permutations and endpoint swapping.

This is a necessary structural reduction. No full case is excluded,
and no new SAT search is run. The nine complete extension formulas are
prepared and independently checked for a subsequent bounded search.
The red empty-pair case remains open. The four-versus-seven frontier
stays at **17 classes / 9,153 labeled cores**; there is no target graph
or Ramsey-bound improvement.

The [proof](PROOF.md) separates the exact count relaxation, full-graph
coverage and normalization. It also records a checked local
counterexample to a stronger proposed fixed-neighbor cap.

## Counts and conventions

The action has four internally red and seven internally blue moving
triangles and ten fixed vertices. The red core is Core194, word
`100110110110110100` on cycle pairs01,02,03,12,13,23. Let u=33,v=34
be an empty blue fixed pair. The accepted pair lemma says their common
blue neighborhood is exactly the twelve core vertices.

Contacts of each blue triangle or other fixed vertex to the ordered
pair are therefore RR,RB,BR. Write their moving multiplicities as
(a,b,c), summing to7, and fixed multiplicities as (x,y,z), summing to8.
The root red degrees are `3(a+b)+x+y` and `3(a+c)+x+z`. The imported
theorem [R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
gives red and blue degrees18..24, equivalently

```
5 <= 3b+y <= 11,       5 <= 3c+z <= 11.
```

Thus b,c<=3, so a>=1. If b=c=0 then y,z>=5, impossible with eight
other fixed vertices. This also gives a<=6. Swap endpoints to make
b<=c and, only when b=c, y<=z.

| Moving counts (RR,RB,BR) | Joint profiles |
|---|---:|
| (1,3,3) | 6 |
| (2,2,3) | 18 |
| (3,1,3) | 18 |
| (3,2,2) | 19 |
| (4,0,3) | 9 |
| (4,1,2) | 27 |
| (5,0,2) | 10 |
| (5,1,1) | 9 |
| (6,0,1) | 3 |

The [certificate](certificate.json) lists all119 profiles, exact root
degrees, labeled multiplicities and thirty normalized star units.
The orbit weights sum to **4,806,900** labeled assignments out of
**14,348,907 = 3^15** no-BB assignments. These numbers classify the
two-root degree relaxation; they do not count realizable Ramsey graphs.

## Full extension coverage

Permuting the seven blue triangles, retaining their phase labels,
commutes with C3 and fixes the core. Permuting the eight other fixed
vertices and swapping u,v preserve all literal graph constraints.
The [accepted direct formula](../ramsey_r55_order3_eleven_core194_direct_review1)
has no row ordering that these operations could violate.

Normalize the moving triangles as RR, then RB, then BR. Each of the
nine complete formulas appends only fourteen corresponding link units
to the **entire** direct BLUE base. The other fixed incidences remain
free. The119 joint profiles are certified as a finer count cover, but
119 full formula files or searches are not produced in this milestone.

The base has320 variables,366,069 clauses and14,883,777 bytes, SHA256
`f3314485280b2080f3459774b944e010beeb175788673d53703d60cba091e84c`.
Every new child has320 variables and366,083 clauses. All base-body
bytes are retained, followed by exactly fourteen units. Exact file
identities appear in [result.json](result.json).

Every graph with a distinguished blue empty pair has a representative
in these nine cases. A graph with several possible distinguished pairs
may occur more than once; this is a complete cover, not a graph census.
Refuting all nine would forbid every blue empty pair. A full Core194
exclusion would still require resolving the red-pair case and using
the independently accepted z>=2 premise.

## A local cap fails

The [19-vertex witness](five_fixed19.edges) has69 red edges, no
monochromatic K5, and an empty blue pair (12,18) over Core194 on0..11.
All five other fixed vertices13..17 are blue to18 and red to12. Their
red-core signatures are `(0,0,1,6,10)`. The local action rotates the
four red triangles and fixes the other seven vertices.

Vertex18 is blue to all other eighteen vertices; its blue neighborhood
has no red K5 or blue K4. This disproves the proposed cap of four such
fixed neighbors under these local assumptions. It does not establish
a global degree completion or full43-vertex extension. No moving type
with b=0 is discarded on the basis of that false cap.

The edge list starts with the order19 and lists each red edge once as
an increasing pair; all omitted pairs are blue. The literal checker
checks all11,628 five-sets, all3,060 blue-neighborhood four-sets, exact
core, uniform signatures, five attachments, local action and exact
common-blue core. This positive counterfixture is sufficient evidence;
no exhaustive enumeration of all such local graphs is claimed.

## Independent checking and reproduction

The producer enumerates the two blue-degree inequalities and uses
multinomial orbit weights. The auditor imports no producer. It exhausts
all2,187 moving contact words and6,561 fixed contact words, combines
their exact histograms, and checks physical red degrees. It matches
each of the119 orbit weights and every normalized primary unit. It
tests5,852 distinct sorting permutations and a separate endpoint swap
as actual43-vertex permutations, commuting with C3 and inducing
bijections on all320 primary orbits.

Thirteen malformed profiles/fixtures are rejected under both normal
and optimized Python. Six malformed full-child files are rejected
during construction and fresh verification. The complete BLUE base is
regenerated and audited by the independently reviewed direct package,
then every child prefix, physical tail, header and EOF is checked.
Thirteen source identities, including PROOF.md, are frozen before
construction. These internal checks are not independent peer review.

CPython3.11.2 and the standard library suffice. From the repository root,
using fresh output paths outside Git:

```bash
mkdir -p /scratch/FRESH-r55-attachments
python3 -B ramsey_r55_order3_eleven_core194_attachments/profiles.py \
  --output /scratch/FRESH-r55-attachments/certificate.json
python3 -B ramsey_r55_order3_eleven_core194_attachments/audit.py \
  --certificate /scratch/FRESH-r55-attachments/certificate.json \
  --fixture ramsey_r55_order3_eleven_core194_attachments/five_fixed19.edges \
  --work /scratch/FRESH-r55-attachments/controls \
  --report /scratch/FRESH-r55-attachments/audit.json
python3 -B ramsey_r55_order3_eleven_core194_attachments/prepare.py \
  --work /scratch/FRESH-r55-attachments/full
python3 -B -O ramsey_r55_order3_eleven_core194_attachments/verify.py \
  --source-work /scratch/FRESH-r55-attachments/full \
  --work /scratch/FRESH-r55-attachments/verification
```

The last two commands reconstruct the base and all nine complete child
files, about149 MB per work directory. Generated CNFs remain outside
Git. These commands invoke no solver and produce no proof trace. A
later search must preserve the displayed cover and require fully checked
UNSAT traces or a compact literally verified43-vertex graph.

## Dependencies and remaining scope

The local blue-pair theorem and direct equivalence have accepted reviews,
respectively sources `d59a572af02f942157d741ce1ae4be948e3b1e2e` and
`f36e1aa39de45e209b174a81cd765deaa04d6d47`. The new direct review at
Discovery Net height3190 verifies all literal clauses and the original
fixed-pair relabelings. It does not cover this new attachment count
classification or normalization. Both old direct solver calls remain
UNKNOWN. The old one-empty branch remains excluded by the accepted
multiplicity result and is not reopened.

The external complementary-K4 criterion at height3188 was read as a
generalization of the local pair argument; its application to other
cores is outside this pass. The teammate's central-neighborhood92/93
witnesses, source `0dd9c5e6d6418a991dc01e177e2b9d001cd38b91`, concern
a separate nonsymmetric fixed-core guard and are not imported here.

R(4,5)=25 is an external theorem used only for the degree window. The
local pair lemma, full direct equivalence, ordinary unformalized
normalization argument, exact Python/hardware and hashes for identity
are explicit trust boundaries. The cumulative17-class count imports
earlier catalog and review scopes. No priority claim is made.

## Completed construction and checkpoint

Production took29.073214 seconds; fresh verification under optimized
Python took29.31716 seconds. Both reconstructed all nine full cases,
matched every profile and child identity, and made **zero solver calls**.
The recorded largest child maximum RSS is22,904 KiB; it measures child
processes, not the peak memory of the in-process base generator.
All thirteen frozen source identities match. Exact records are in
[result.json](result.json), [verification.json](verification.json),
[audit_report.json](audit_report.json) and [boundary.json](boundary.json).

Fresh verification initially caught a report serialization mismatch:
JSON turns integer clause-length keys into strings. The comparison now
normalizes the full record into the same JSON representation without
dropping fields. Production and verification were rerun with a new frozen
contract. All ten CNFs, including the base, remained byte-identical.
The earlier diagnostic files remain private; the published reports are
from the successful runs.

The final relevant Discovery Net refresh through height3199 found the
teammate's published central-neighborhood result at3196 and two external
interface results at3192/3198. Their bodies were read as distinct,
undecided handoffs; none is a premise of this symmetry cover. No new
conflicting symmetry result appeared. The direct formulation's accepted
review and its exact scope are preserved.

No background job remains. The next bounded step is the nine prepared
full-extension decisions, with complete proof replay for any UNSAT and
literal graph checking for any SAT. The119 finer full-star searches,
longer old solves, another core, and the teammate's nonsymmetric graph
work are not started here. The red-pair branch remains explicitly open.
