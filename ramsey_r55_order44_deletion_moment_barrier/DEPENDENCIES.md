# Dependencies, overlap, and status

The current published frontier is 43<=R(5,5)<=46. The primary paper
[Angeltveit--McKay, R(5,5)<=46](https://arxiv.org/html/2409.15709v2)
was consulted, especially its definition, degree bound, and distinction
between complete catalogue coverage and gluing. We import R(4,5)<=25,
not any catalogue or gluing output. The other imported Ramsey bound is
R(3,5)<=14 from [Greenwood--Gleason, Combinatorial Relations and Chromatic
Graphs](https://doi.org/10.4153/CJM-1955-001-4). Those classical theorems
are not reproved or formally verified here.

Rooted density and PSD methods are classical; see
[Razborov, Flag algebras](https://doi.org/10.2178/jsl/1203350785).
The finite sampling coefficients used here have the direct counting proof
in METHOD.md. No novelty claim is made for the general moment method.

The generator and Bareiss-checking design are adapted from R2's
[seven-vertex moment barrier](../ramsey_r55_seven_vertex_moment_barrier),
source commit `4f3f9dea13f704716c0d53a17861554fd3f4d519`.
INHERITED_SOURCE.json records the six original file hashes. The present
test regenerates the systems at orders 43 and 44 with unrestricted
codegree cap 13, their different degree domains, and a new exact
degree-support equality. The inherited rational M10 point is not used
as the final certificate. No R2 physical enumeration or queue was run.

The start and final Discovery Net queries both had indexed height 4363,
2,207 contributions, 10,837 relations, and no query errors. Exact
neighbourhood bodies, extension/clone work, the neighbourhood-occurrence
reduction h3501, and relevant reviews were inspected. The reviewed
maximal-connectivity proof was read but is not a premise. The defective
historical order-five automorphism exclusion is not used. The source-only
392..511 and fault-Hamiltonicity results were distinguished from committed,
reviewed evidence and are not premises of the new certificate.

The full principal report of 2026-09-13 01:00:48 UTC and the supplemental
01:14:23 report were read. The latter reassigns R2 to global pentagon
incidences and leaves the order-44 contract unchanged. The shared source
advanced during this pass from
`341df3a06290c05db684eba21241f2be3c9b9468` to the R3 alternating-path and
R4 order-45 coloured-deck checkpoints. Their reports were inspected before
publication; neither was imported or executed. R4's degree-24 occurrence
LP at order 45 is distinct from this averaged, unrestricted order-44
moment test. Both failures reinforce the decision not to start another
moment sequence.

No theorem for a physical Ramsey class follows from this package.
The positive rational point refutes the possibility of an infeasibility
certificate in exactly the displayed cone. It neither settles R(5,5)
nor proves that the point has a finite-graph realization. All generated
arrays and exploratory evidence are retained outside Git; no pending
Discovery Net transaction is resubmitted.
