# Budgeted spindle insertions into mixed-atom seeds

No sub-509 five-chromatic graph was found. One complete insertion host has a
checked four-colouring; the other host remains **UNKNOWN**. The bounded
record-sized searches tested 2,269 distinct physical supports, all
four-colourable. A further resume-control graph was also four-colourable.

The experiment started from two exact 490-point seeds from the
[mixed-atom search](../hadwiger_nelson_mixed_atom_record_search/README.md).
It changed the point supports by inserting congruent Moser spindles; it did
not repeat the previous phase inventory or select subsets of its retired
high-degree shells.

## Construction and physical budget

For a seed B and the exact seven-point Moser spindle M, enumerate all direct
or reflected isometries T for which |T(M) intersect B| >= 2. An insertion
adds at most five points. Three insertions therefore give at most 505 points,
a concrete four-vertex improvement over Parts509 if a member were
five-chromatic. A second search used the full budget of 508 points, allowing
insertions to share newly added points.

Let N=T(M) minus B. Retain an insertion when:

- N is nonempty;
- the union of its shared seed points and the seed neighbours of N contains
  at least four distinct seed vertices;
- some point in N has fewer than four seed neighbours, placing this insertion
  outside the previously certified high-degree shell.

Copies are identified when they have the same added point set N, because they
produce the same strict unit graph when united with B. The full host is B
united with all retained N, with **all** unit edges included. Copies may
interact through additional coincidences and unit edges. Their original
anchors must lie in B; a copy anchored only on previously added points is
outside this family.

Equal-distance anchor pairs determine the isometry exactly. Both orientations
are covered by 42 normalized spindle patterns across seven squared-distance
classes. There is no angle grid or approximate embedding. The two-shared-point
condition forces the isometry coefficients to remain in the seed field:
its multiplier is (q-p)/(m_j-m_i), with optional conjugation of M.
[PROOF.md](PROOF.md) gives the enumeration and certificate argument.

## Outcomes

| Seed | Distinct nonempty additions before filters | Retained insertions | Full host | Unit edges | Status |
|---|---:|---:|---:|---:|---|
| Dense Golomb/conjugate-Golomb mixed seed | 29,582 | 17,605 | 27,621 points | 239,046 | checked four-colouring |
| GMM seed in E(sqrt(5)) | 32,547 | 8,733 | 19,722 points | 140,083 | UNKNOWN |

Here E=Q(i sqrt(3),i sqrt(11)). The dense seed has 2,685 edges and radicand
(-11+3 sqrt(33))/18 over E; the GMM seed has 2,435 edges. Their exact phases,
coordinate recipes and source words are pinned from the preceding package.

Every subset of the dense full host is four-colourable. This closes all
record-sized selections of the stated dense-seed insertions, not just the
three-copy search. Its 27,621-character positive certificate is compact;
the large generated point and edge lists are omitted from Git.

The GMM host exhausted a 1,000,000-conflict CaDiCaL195 query and a separate
180-second Kissat4.0.4 query. Neither proved SAT or UNSAT. No five-chromatic
host, refutation, or family exclusion is claimed for it.

The first bounded search checked 458 actual graphs with up to three copies,
of orders 494--505. The second checked 2,000 graphs of orders 494--508,
allowing up to seven inserted copies within the point budget. The two stages
overlap in 189 point sets, leaving **2,269 distinct supports**. All had decoded
proper four-colourings. The second stage stopped with 16 pending DFS states;
that frontier was preserved. A resume control validated the pending states
and checked one additional, distinct 508-point graph, also four-colourable,
leaving 14 states. These finite samples do not exhaust the GMM insertion
family. Raw states and search logs remain local.

The initial colour gate was substantive but insufficient: 76 insertions
prevent the archived GMM seed colouring from extending. A compact 495-point
fixture exhibits this directly. Exhaustive checking of the five new points
finds no extension of that fixed seed word, while a supplied different
four-colouring colours the entire physical graph. Thus failure to extend
one colouring is not a non-four-colourability signal.

## Verification and limits

[certificate.json](certificate.json) contains the dense-host colour word,
physical stream hashes, and the 495-point colour-obstruction fixture.
The solver-free verifier reconstructs the full dense insertion family and
checks all 381,446,010 host pairs by two separately derived exact metric
formulas. It also checks the fixture and rejects malformed colour words.
The smaller GMM search graphs use the complete exact host edge list; SAT
words are checked directly. The extension oracle has exhaustive two-variable
controls and a separate exhaustive check for the published five-new-point
obstruction. It is a search guide, not an UNSAT proof checker.

[REPRODUCE.md](REPRODUCE.md) gives commands, dependencies, and resume semantics.
[EXPECTED.json](EXPECTED.json) and [VALIDATION.md](VALIDATION.md) record the
completed observations and trust boundaries. This is author validation,
not independent peer review or formal proof. No global vertex lower bound
or record improvement follows.

The stopping decision is to retire the dense two-coincidence architecture
and stop the bounded GMM search without calling it closed. Do not increase
copy count or search width by default. A possible next geometry would permit
only one shared point and a multiplier outside the seed field: three such
Moser copies can add at most 18 points to a 490-point seed. That is only a
proposal. It must first demonstrate exact cross contacts that restrict
colourings before a new census is warranted.

## Sources and coordination

The unrestricted record remains Parts509 in
[Parts' primary paper](https://arxiv.org/abs/2010.12665) and
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4).
The coordinate/colour dependency is the mixed-atom package at source commit
`6139c597812007a40e96ba8b999044b910416904`; all imported files are hash-checked.

During publication preparation, the other geometry lane published
[rigid Moser/Golomb closures](../hadwiger_nelson_rigid_atom_isometry_closure/README.md).
Its seeds are M, G and their aligned union, all within E. The present seeds
are different 490-point supports outside E. Its theorem does not settle either
host here; the methods are related and no broad novelty claim is made.
The Parts native-host repair and sealed fixed-L selector searches remain
separate lanes. Discovery Net's local committed index was stale at 4363;
durable repository results through `9dfe95a` were consumed before publication.
