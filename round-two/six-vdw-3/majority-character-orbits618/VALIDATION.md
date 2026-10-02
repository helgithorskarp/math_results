# Validation and trust boundary

Author: **six-vdw-3, researcher**,2026-10-02. The producer and checker are
two implementations by the same author. No external review of this
majority result is claimed. The previously independently reviewed affine
lemma9659 is a genuine premise only for the repeated-root branch.

The producer uses permutations of input labels, Euler's criterion, sum
majority,618-bit intersections and deterministic greedy traversal orders.
Only positive actual AP pairs are used as evidence. Exhaustion of a
greedy traversal is not a packing optimum or a mathematical exclusion.
The checker does not import the producer: it constructs the51 nonzero
squares, uses conditional majority and enumerates ordered source-root
pairs whose inverse coordinates send them to0 and1. It directly checks
all seven residues and colors, all free roots and disjoint column supports.

The exact checked domains and counts are:

| Domain | Complete coverage |
|---|---:|
| Distinct-root normalized parameter states |404|
| S3 parameter orbits |69|
| Orbit sizes |66 of size6,2 of size3,1 of size2|
| Burnside fixed states |404 for identity,2 for each other permutation|
| Root-pair maps and regular color identities |2424 maps,242400 values|
| State/map compositions |14544|
| Original ordered distinct-root triples |1061106|
| Character multiplicativity inputs |10404|
| Joint palette and repeated-root truth inputs |128 and224|
| Majority sign-identity truth assignments |8|
| Field/translation/phase CRT parameter sets |63036|
| Six-row phase cycle inputs |1920 across all64 rows|
| Legal phase rows |6, exactly rotations of000111|
| Illegal-phase actual column witnesses |5974|
| Representative positive APs and literal points |621 and4347|
| Transported positive APs and literal points |3636 and25452 across404 states|
| Chosen transport color-exchange states |238 unchanged,166 exchanged|
| Small-hole cardinality/distance controls |10 classes,1000 values|
| Semantic certificate damages rejected |14 per mode|

Every representative uses nine supports of seven distinct field columns,
covering63 columns without using any of its three roots. Field0 is a
root in every normalized majority state. Start0 is therefore never
accepted. Actual nonzero cyclic steps are preserved by the unit CRT
transport; steps are reversed when needed for a positive interval lift
with endpoint at most2472. The checker verifies the lifts literally.

The14 damage controls change coverage, indices, state parameters,
palette domain, AP-pair length, start/step domains, root freedom, field
repetition, disjointness, short-orbit representatives or literal colors.
They run with explicit exceptions and remain active under `python -O`.
All ordinary algebraic bridges are written in [PROOF.md](PROOF.md).
The exhaustive finite root/map checks supplement those proofs; they do
not replace their quantifiers over arbitrary coefficients and edit colors.

The source-pinned reproduction runs generator then checker in each of
normal and optimized CPython, serially, using only the standard library
and one numerical thread. Its fixed20-second per-child guard is an
operational limit, not mathematical evidence if reached. It requires
byte-for-byte equality of the complete69-row certificate and of the
complete checker JSON. The local author used CPython3.11.2.

[expected.json](expected.json) records exact counts, certificate hash,
literal transcript hashes and damage rejections. [verification.json](verification.json)
records the author's normal/optimized agreement. [SOURCE_PINS.json](SOURCE_PINS.json)
pins every public source/evidence file other than itself. A fresh run of
[reproduce.py](reproduce.py) writes a separate verification receipt in
the requested work directory; source publication is not a proof premise.

No native solver, floating-point calculation, exhaustive coloring census,
large proof corpus or external data file is required. This is an exact
finite obstruction for the stated majority family, with an earlier
affine-character premise for repeated roots. No conclusion about ten
disjoint supports, optimal repair size, existence after nine edits,
arbitrary XOR618 exclusion or a numerical W(2,7) improvement follows.
