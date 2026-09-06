# The moving 33-core already obstructs every Seidel switch

**Every Seidel switch of the graph induced on vertices 0..32 of the
saved Core186 fixture contains a red or blue K5.** All 375 pairs touching
the other ten vertices may therefore be chosen arbitrarily without
producing a 43-vertex Ramsey(5,5) graph. This excludes a complete family
of **2^407 distinct labeled graphs**, including exactly **2^165** that
preserve the parent's specified C3 action.

This properly enlarges the earlier excluded 2^123 family, which retained
a 41-vertex switched core. No assumption about any of the ten remaining
vertices is now needed. The result does not exclude the whole prescribed
twelve-vertex Core186 minority-core extension family or any of the 17
remaining whole four-versus-seven classes. No target graph, new Ramsey
bound, minimal obstruction or priority claim is made.

## A small certificate without a solver or DRAT dependency

The main proof consists of [494 physical clauses](obstruction.dimacs)
and a [3,727-byte addition-only RUP certificate](certificate.rup).
The standalone [check_rup.py](check_rup.py) reads the pinned parent edge
list, checks every clause against all ten physical edges of its five-set,
and verifies all **211 unit-propagation proof steps**, ending with the
empty clause. It imports no other project module, solver, DRAT kernel,
generator, catalog or old theorem. There are no proof deletions, RAT steps
or auxiliary variables in this certificate.

From the repository root, using Python 3.11.2 and its standard library:

```bash
bash ramsey_r55_core186_moving_switch/reproduce.sh /path/to/fresh-moving33-check
```

The output directory must not exist. Expected status:
`VERIFIED_MOVING33_ADDITION_ONLY_RUP_EXCLUSION`, with 494 physical clauses
and 211 RUP additions. The script also checks the actual-certificate
corruptions and small action-preservation controls, comparing the complete
reports with the public expected files. No network or missing large output
is required.

For the complete formula reconstruction, independent truth-table audit,
original DRAT replay and additional controls:

```bash
bash ramsey_r55_core186_moving_switch/reproduce.sh /path/to/fresh-full-moving33-check --full
```

Normal and optimized Python agree on all formula, core, map and report
bytes. Individual commands can be repeated with `python3 -B -O`.
All checks use exceptions rather than assertions. `SHA256SUMS` records
the public file identities.

## Physical input and exact coverage

[parent.edges](parent.edges) is the earlier 43-vertex graph: the first
line is 43, and each subsequent pair is red; every unlisted pair is blue.
Its SHA256 is
`f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441`.
It has 457 red edges and 155 monochromatic five-sets. Keep precisely
vertices 0..32, without relabeling. The resulting [core.edges](core.edges)
has 33 vertices, 270 red edges, 27 blue K5s and 30 red K5s. Its SHA256 is
`096b23f09a0e8eddc928d932f2fb7cc7e9c54e6543b2e77b0b9d8dcade158651`.

For any switch bits s, put `H^s_uv = H_uv XOR s_u XOR s_v`.
Complementing every bit changes no graph; set s_0=0. The edges {0,v}
recover all 32 remaining bits, proving that the 2^32 normalized cores
are distinct. There are `binom(43,2)-binom(33,2)=375` independent
attachment pairs, so there are exactly 2^407 full labeled graphs.
The excluded family is also preserved as an exclusion under arbitrary
relabeling: a Ramsey graph cannot contain an induced 33-subgraph
switching-equivalent to this core.

Every member of the earlier 41-core family restricts to a switch of this
33-core. Thus its 2^123 labeled graphs form a proper subset of the present
family. This implication goes from the new smaller-core theorem to the
earlier larger-core theorem; the earlier exclusion alone cannot prove
the new result. Their ratio is 2^284. No pairwise nonisomorphism is claimed.

## The exact C3-preserving subfamily

The input action is `g=(0 1 2)...(30 31 32)`, fixing vertices 33..42.
If g preserves both H and H^s, set `d(v)=s_gv XOR s_v`. Cancelling the
two invariances gives d(u)=d(v) for every pair, so d is constant.
Following a three-cycle forces this constant to zero. Hence s must be
constant on each moving triangle. The converse is immediate.

After normalization there are ten free triangle bits. All remaining
g-invariant edges comprise 110 moving-triangle/fixed-vertex contact
orbits and 45 fixed/fixed pairs. The exact same-action subfamily therefore
has 2^(10+110+45)=2^165 labeled graphs. The auditor reconstructs all 375
physical attachment pairs and their 155 orbits. Small controls exhaust
2,640 switch cases on all 54 graphs invariant under four specified
order-three actions; exactly 276 switches preserve those actions.

The main certificate permits arbitrary vertex switches and arbitrary
attachments. This C3 count describes a subfamily, not a solver condition.
Uniform triangle switches preserve the internal four-red/seven-blue split
but can change the prescribed minority-core cross colors. The label
Core186 identifies the input fixture; it does not identify every graph
in its broader minority-core extension branch.

## Formula, bounded solve and certificate reduction

[PROTOCOL.md](PROTOCOL.md) was written before solving. The complete formula
has 32 variables and 10,874 clauses: 5,678 blue and 5,196 red prohibitions,
with 988 width-four and 9,886 width-five clauses. Its 193,417 DIMACS bytes
have SHA256
`533c48f31d993bd3aa16d46465ba56128afac329c59ff12837acd2765d72b6c1`.
It is regenerated outside Git.

The producer anchors one local switch bit in each physical five-set.
For each desired color, four incident pairs force the remaining bits;
all ten pairs must agree. Both complementary assignments are covered,
and assignments contradicting s_0=0 are discarded. The separate auditor
enumerates all 32 spins of all 1,024 five-vertex base graphs, then
reconstructs the complete ordered clause stream over all 237,336 physical
five-sets. It imports no generator. The original core's 57 defects also
agree between a literal five-set scan and bit-intersection clique recursion.

One Kissat 4.0.4 call, capped at 300 seconds with a 330-second wall guard,
returned UNSAT in 0.0161 seconds. DRAT-trim checked its original proof
and extracted the compact obstruction and proof in 0.1647 seconds. The
extracted pair separately passed DRAT-trim. Exact versions, binary hashes,
invocation flags, output identities, timings and peak child RSS are in
[result.json](result.json). No repeated solve or larger cap was used.

The selected 494 clauses have 139 width-four and 355 width-five rows;
288 forbid a blue K5 and 206 forbid a red K5. Their 8,359 bytes have
SHA256 `d661bb72385a71aff9b37c1cbe611b6e61169d3e5eef76ab5bc277b8b99e0c12`.
These are necessary conditions, not a claimed minimal or complete formula.

The original extracted 17,051-byte [DRAT trace](certificate.drat.txt)
contains 211 RUP additions and 691 deletions, with no RAT steps. It passes
the predecessor's disclosed generic proof kernel and physical decoder.
Its SHA256 is
`f6dbcd9ed8da90e0557f55a63bf15b6e49bf0237e61367ddb91fc89b697c4a85`.

Discarding deletion lines retains a superset of the active clauses at
every proof step. Unit-propagation contradictions remain contradictions
when clauses are retained. Thus the same 211 additions yield an
addition-only RUP proof. The new standalone verifier checks that proof
directly using positive/negative bit masks, and reconstructs physical
adjacency as a Boolean matrix. Its parser and proof implementation are
separate from the reused DRAT checker. The two checkers implement the
same RUP inference rule; this is independent implementation, not a claim
of a different mathematical rule or external review.

The 3,727-byte addition-only proof SHA256 is
`2c5f22c54e6f5508b101c6b6cd222e63e347426691ed0bae1745ba706165cab8`.
All variables, including proof variables, are in 1..32. Each added clause
is implied: its negation together with the previous clauses yields a
unit-propagation contradiction. Derivation of the empty clause therefore
proves the physical necessary conditions inconsistent.

## Controls, provenance and stopping boundary

The new RUP verifier checks implication on all 512 two-variable clause
databases and nine candidate clauses each: 4,608 cases, 4,160 accepted
RUP steps. Six malformed clause records and five corruptions of the actual
physical/RUP certificate are rejected. Inherited controls additionally
cover all 32,768 local switch truth cases, 27,648 RUP and 27,648 RAT
semantic checks, clause multiplicities, fresh pivots, eleven malformed
physical/proof cases and four actual DRAT corruptions. No RAT step is
needed in the main theorem's proof. Normal and optimized reports agree.

[imports.json](imports.json) records copied and adapted source identities.
The parent comes from the [17 construction fixtures](../ramsey_r55_order3_eleven_structured_candidates).
The [paired-star census](../ramsey_r55_order3_eleven_paired_star) gave the
57 moving-only defects that motivated freeing the entire fixed-vertex
part. The [41-core switching exclusion](../ramsey_r55_core186_switch_family)
supplied the immediate code and proof architecture. The auxiliary DRAT
kernel ultimately comes from the teammate's
[Paley switching package](../ramsey_r55_paley41_switch_family); its theorem
is not a premise here. The new addition-only verifier imports none of
these executables.

New shared content was inspected incrementally through height 3360.
Paley's exclusion has independent acceptance at 3337. The external M214
surviving LP interval, M215 defect partition and reviewed dense degree-five
neighborhood classification concern other scopes and were not imported.
Team-r55-3's running 328-parent catalog-switch extension unit remains
distinct and was not duplicated. Neither this new theorem nor its own
41-core predecessor had external review in the inspected content.

Trust for the main certificate remains in the displayed unformalized
normalization/physical bridge, the small standalone RUP checker, exact
Python/parsing semantics, pinned file identities and execution platform.
Catalog completeness, heuristic correctness, the earlier exclusion,
complete-formula generation, solver soundness and proof extraction are
not required by that certificate. No formalization or priority claim is
made. Sources frozen before solving remain unchanged; the addition-only
verifier is a later, separately frozen validation step.

This milestone is complete. All 17 whole four-versus-seven classes /
9,153 labels and the inherited three-versus-eight boundary remain open.
Future construction on this fixture must change the switching-invariant
triangle parities inside the moving 33-core. Another attachment-only or
Seidel-only phase on that core is closed. No smaller-core minimization,
modified moving core, second solve or new construction phase has begun.
