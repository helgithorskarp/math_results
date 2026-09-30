# A sharp radius-five cover/tiling dichotomy for the bent four-hex

Agent: **six-heesch-3**. Role: **researcher**. Date: 2026-09-30.
Status: exact computer-assisted theorem with an independently checked RUP
certificate and written geometric correspondence. No formalization, reviewer
verdict, historical priority claim or finite-Heesch record improvement.

Let P={(0,0),(1,0),(2,0),(2,1)} in the regular hexagonal cell grid, with its
18 original unit boundary ports in the sorted order of hex_domain.boundary.
Assign each port an arbitrary self-compatible color and a state in {-1,0,+1}.
A shared unit interface is allowed exactly when its two original ports have
equal colors and opposite states. The marked model allows six rotations and
integer translations, with no reflections. All equality partitions and all
ternary state assignments are included; no additive charge is assumed.

Write B_r={(x,y):max(|x|,|y|,|x+y|)<=r} and R_r=P+B_r. A rooted cover is a
nonoverlapping packing containing the normalized root P which covers every
cell of R_r and obeys the matching rule at all shared interfaces. It need
not have ranks, complete coronas, connectivity or disc topology.

**Theorem.** Every marking of P with a rooted R_5 cover admits one of the
twelve explicit periodic tilings in
[bend4_directed_cover_tiling.json](bend4_directed_cover_tiling.json).
The radius cannot be lowered to four: the five-color, zero-state marking
already certified to have Euclidean Hc=2 has a checked rooted R_4 cover.

Consequently every finite member of this marked family has Hc,Hh<=4. For
the unmarked Euclidean curved shapes constructed by the fully nonflat
quintic profiles in [quintic_realization.md](quintic_realization.md), allowing
all translations, rotations and reflections, every finite member satisfies

    Hc <= 4,       Hh <= 5.

For zero states the geometric Hh bound improves to four. Hc requires every
prefix to be a disc; Hh allows holes only in the last prefix. A plane tiler is
assigned infinity. This result excludes the seven-corona target throughout
this particular curved family. Other bases and other matching/motion rules
remain outside its scope.

## Exact partition encoding

For each unordered pair i<j introduce E_ij, and interpret E_ii as true. For
each triple i<j<k insert

    (-E_ij or -E_ik or E_jk),
    (-E_ij or -E_jk or E_ik),
    (-E_ik or -E_jk or E_ij).

These clauses say that any two sides of a positive triangle force the third.
Thus positivity, together with the diagonal and symmetry, is an equivalence
relation. Each connected component is a clique, and naming components gives
exactly a self-color partition. Conversely every partition satisfies these
clauses. There are 153 pair variables and 2,448 transitivity clauses. No
numeric color names or renaming symmetry remain.

Each port has Boolean variables p_i,m_i with (-p_i or -m_i). They represent
states +1,-1,0 by (1,0),(0,1),(0,0). For i<j define, by exact Boolean gates,

    M_ij = E_ij and (p_i=m_j) and (m_i=p_j).

For i=j put M_ii=(-p_i and -m_i): a state is opposite itself precisely when
it is zero. These are definitions, rather than one-way implications.
All Bell(18)=682,076,806,159 color partitions and 3^18 state tables occur in
the parameter encoding. Their product is 264,250,529,777,677,991,751.
This is a symbolic universal proof, not enumeration of those tables.

## Complete cover geometry and conditional contacts

For each of the six normalized orientations S enumerate all translations
t=u-v, u in R_5 and v in S. This is exactly the set of translated copies
meeting the target. Remove copies intersecting the fixed root; no compatible
packing can contain them. Keep differently oriented labeled copies even if
their unmarked footprints coincide. There are 900 candidates.

Give each candidate an active variable. For every target cell outside the
root require an active covering candidate. On **every** candidate cell,
including cells outside the target, impose at-most-one occupancy. These
constraints guarantee full-footprint nonoverlap, with no window cutoff.
The target contains 124 cells; the actual candidate union with the root
contains 254. The root's active literal is constant true.

Hash each oriented boundary edge by its two adjacent cell centers, recording
the inside side, candidate index and original port index. An opposite-side
incidence pair is exactly a possible unit-edge contact. Ignore candidate
pairs whose complete footprints overlap: the existing occupancy constraints
already prevent their joint activation. For every remaining contact of
copies a,b with original ports i,j, add

    (-active_a or -active_b or M_ij).

Duplicate geometric contacts that give the same copy pair and unordered
port pair need only one clause. The exhaustive inventory has 66,390 distinct
contact equations, with 19,195 overlapping copy pairs omitted from this
inventory. Contacts involving the root are included.

Soundness follows by decoding the active footprints, the color cliques and
the ternary states. Every actual shared edge appears in the inventory and
therefore matches. For completeness, delete nonroot copies missing R_5
from any admissible rooted cover. Each retained copy appears in the exact
translation list. Its occupancy, partition, states and actual contacts
satisfy the formula. Pairs omitted for overlap cannot be simultaneously
active. No candidate, motion, label or degenerate state is lost.

## Periodic witnesses and their necessary exclusions

Each stored motif has integer periods (a,0),(b,c), with a,c>0 and 0<=b<a.
The definition-level checker in color_state.py does not trust the torus
solver or its edge encoding. It lifts each fundamental-domain cell to the
unique motif owner and its exact lattice displacement. It checks coverage,
nonoverlap, every boundary neighbor and inverse original-port indices.
Period crossings and contacts to a translate of the same motif copy are
included. This proves a full-plane unmarked base tiling and returns its
finite set F of required original-port pairs.

A motif is valid for a color/state table exactly when every M_ij, (i,j) in
F, is true. Every such table has an explicit periodic marked tiling.
Finiteness therefore requires the single clause

    OR over (i,j) in F of (-M_ij).

All twelve clauses are added to the rooted-cover formula. Eleven motifs
are reused from [cover_tiling_dichotomy.md](cover_tiling_dichotomy.md); the
twelfth, with determinant four and one motif copy, was found and checked
in the earlier incomplete directed search. Their determinants are
8,8,8,8,8,8,16,8,8,16,16,4. No negative result from that search is assumed.

## Independently checked contradiction

The frozen formula has **4,917 variables and 80,679 clauses**, SHA256

    beefe212f62cf2a3de904eb2b4f074e06bdd6633604eca0ab2e210053c0b4d53

A cold Glucose4 solve used no assumptions and returned UNSAT at 11,229
conflicts, within the unchanged 20,000-conflict budget. Its 1,544,726-byte
proof has SHA256

    0185bd4506ae71b5d353b7dfb690a3b2cf0a07653b310d2944832ff692ebedb1

Pinned DRAT-trim, invoked with -U -p, independently reports **s VERIFIED**,
0 RAT core lemmas, 7,870 core lemmas out of 11,230 total, 14,658 core input
clauses and 830,181 resolution steps. Thus the final original formula has
a checked RUP contradiction. Every marking with a rooted R_5 cover must
violate at least one of the twelve motif-exclusion clauses, which proves
the theorem.

This also resolves the earlier UNKNOWN directed branch and strengthens
the earlier zero-state radius-seven result. Its old numeric and canonical
numeric inputs exhausted their budgets; no mathematical conclusion was
drawn from those attempts. A different equivalent encoding supplied the
present proof without raising resource limits.

## Corona and geometric consequences

In a complete marked corona, the unit neighbor halo of the preceding cell
union must be present in the next prefix: otherwise an exposed unit edge
would remain on its boundary. Induction gives R_k contained in the k-prefix.
Deleting copies missing R_k gives the rooted-cover relaxation above.
Hence five complete marked coronas force a periodic tiling, and every
finite marked member has Hc,Hh<=4. This is a one-way reduction; a rooted
cover alone does not prove complete coronas.

The geometric family uses f(t)=t^2(1-t)^2 and profiles

    f(t)[A_s+B_c(2t-1)],
    eta=1/(100m), epsilon=eta/10, A_s=s*epsilon, B_c=c*eta>0,

for the m distinct colors, renamed 1..m. The earlier atomic locking and
quintic proofs show that complete disc coronas force grid placement, a
common handedness, equal colors and opposite states. Valid marked coronas
deform to the curved shapes. The whole-plane correspondence also holds.
Therefore geometric Hc equals marked Hc, and five disc coronas on a finite
curved member are excluded. Although arbitrary reflected placements are
initially allowed geometrically, the common-handedness proof reduces them
to this six-rotation marked model. Reflections must not be enabled in the
marked formula.

With nonzero states, a wrong same-color direction can leave a small lens
hole in the final geometric prefix. Exact Hh correspondence is not assumed.
Discarding the hole-permitted last layer yields Hh<=Hc+1, hence Hh<=5 here.
With zero states every mismatched color already forces overlap, so Hh
corresponds exactly and is at most four. These geometric bridge arguments
are written proof dependencies, not consequences of the SAT checker.

## Sharpness and the cover/corona gap

[bend4_fivecolor_radius4.cover.json](bend4_fivecolor_radius4.cover.json)
contains a directly checked rooted R_4 cover with 30 copies, 120 cells and
422 matched boundary incidences. Its colors are

    [1,1,1,1,2,1,3,1,4,1,5,5,4,1,1,1,3,2]

and all states are zero. This is the unchanged marking already certified
to have Hc=2 and 2<=Hh<=3: its two-corona lower witness and independent
third-corona RUP proof are in cover_tiling_dichotomy.md and the earlier
certificate package. The new cover checker uses inverse original-port
decoding and checks all footprints and the entire target. Thus radius four
does not imply a plane tiling even for zero states. The dichotomy threshold
five is sharp as a rooted-cover statement; the actual maximal finite corona
depth in this family is not determined.

## Reproduction and trust boundary

From the repository root, standard-library Python suffices for:

    python3 heesch_weighted_matching_obstruction/equivalence_certificate.py check

With Python-SAT1.8.dev24 installed, run:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      python3 heesch_weighted_matching_obstruction/validate_equivalence.py

It must match equivalence_validation_expected.json. The tests evaluate all
33,867 equality-graph assignments through six ports, obtaining Bell counts
1,2,5,15,52,203; 3,072 color/state compatibility cases including invalid
Boolean states; and 8,640 motif-block truth cases. Independently reconstructed
cell contacts match all 413,832 candidate-pair cases, including the **entire
radius-five research instance**. There are also 24 fixed-table comparisons
with the old global-edge encoding, nine independently decoded SAT covers
and direct rechecks of all twelve periodic motifs.

Generate and solve into private scratch:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      timeout 55s python3 heesch_weighted_matching_obstruction/equivalence_certificate.py \
      solve --output-dir scratch/bend4_directed

Use generate instead of solve to regenerate only the input. Both modes
must produce the same CNF hash above. The default Circuit dependency is
heesch_polyomino_euler_cnf; --unmarked-source can specify a separate copy.
Its Circuit and topology hashes are checked against the earlier pinned
dependency before generation. There is no preprocessing or assumption list.

Use DRAT-trim at commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985,
source SHA256 d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee,
built with GCC12.2.0 via cc -O2 -std=gnu11, then:

    /path/to/drat-trim \
      scratch/bend4_directed/bend4_directed_cover_tiling.cnf \
      scratch/bend4_directed/bend4_directed_cover_tiling.drat -U -p -t 50

The source replayer reproduced both input and proof hashes before publication.
Versions, hashes and exact summaries are recorded in
[directed_cover_tiling_evidence.json](directed_cover_tiling_evidence.json).
The standing scope was one CPU, 2GiB and TasksMax128, all threads one and at
most one intensive job. The decisive search peak RSS was 59,220KiB.
Generated CNF/proof corpora remain in scratch and are not published.
Python, the gate/contact compiler, the independent checker and the written
geometric bridge are the trust boundaries. No proof-assistant or independent
reviewer verdict is claimed.

## Literature, collaboration and next frontier

The prior framework is Kaplan's [2022 polyform paper](https://arxiv.org/abs/2105.09438),
Mann's [2004 manuscript](https://faculty.washington.edu/cemann/Heesch.pdf)
and the earlier linked profile/locking and rooted-cover results. Mann's
imbalance method, periodic tiling tests and SAT encodings are credited prior
mechanisms. Six-heesch-1's rooted-covering work supplies the cited context
and pinned Circuit; the complete hexagonal color/state encoding is proved
above. No absolute novelty claim for equivalence-relation encoding is made.

Six-heesch-2's [215-cell polyiamond reproduction](../heesch_polyiamond_hexapillar/README.md)
now supplies five unmarked coronas with a written all-motion finite bound,
reproducing Mann's known hexapillar and qualifying the unlimited-size
polyform-five target. Its theorem is separate from this curved family.
Kaplan's [2025 survey](https://arxiv.org/html/2509.12216v1) still reports six
for the general Euclidean finite record; the 2026 hyperbolic-plane result
[arXiv2603.27827](https://arxiv.org/abs/2603.27827) concerns another geometry.
We retain the Euclidean seven-corona assignment.

The next construction search must change the bent-four-hex footprint or
matching/geometry mechanism. The incomplete zigzag branch has seventeen
checked periodic motifs and can reuse the validated equality encoding.
No finite seven-corona witness has been produced.
