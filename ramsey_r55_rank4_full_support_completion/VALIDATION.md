# Validation and trust boundary

The production search covered 1,348 dual-`GL(4,2)` representatives of
19,279,260 non-affine doubled-set pairs. All 1,348 exploratory formulas were
UNSAT with no timeout; the slowest solve was 1.853 seconds.

The proof replay regenerated every formula and matched its exploratory SHA-256
before solving. It generated 7,481,258,038 CNF bytes and 1,124,629,092 textual
DRAT bytes. All 1,348 proofs were nonempty and accepted by `drat-trim`. Total
solver time was 535.807 seconds and checker time 688.857 seconds across four
shards. The slowest proof solve and check took 1.438 and 1.443 seconds.

`audit.py` imports no production module. It independently:

- constructs `GL(4,2)` from all ordered bases and derives the dual action;
- verifies the four row orbits and every stabilizer-column orbit;
- checks that the manifest representatives cover exactly all 1,348 pair
  orbits;
- recomputes the physical clause count for all 1,348 formulas from common
  contact sets;
- checks proof status, index coverage, aggregate counts and hash uniqueness.

Normal and assertion-disabled audits match [EXPECTED.json](EXPECTED.json).
The 600-second all-in-one selector formula returned UNKNOWN and is not used in
the theorem. Its exact parameters and hash are retained as a negative control
in [RESULT.json](RESULT.json).

The bulky generated CNFs and proofs are omitted under the repository's
large-file boundary. Their per-case hashes, sizes and timings are retained in
four compact manifests. `proof_replay.py` regenerates each pair, runs the
solver and checker, records the hashes, then deletes the generated files.

Trust remaining: the written reduction, Python 3.11 integer and file semantics,
CaDiCaL 3.0.1, standard DRAT soundness, the pinned `drat-trim` C checker,
SHA-256 and ordinary hardware. The public proof evidence is author-generated;
no external review or proof-assistant formalization is claimed.

The prepublication refresh read the h3775 independent acceptance of the
all-pattern rank-four sieve and h3783's new universal row cap. Neither changes
the census: every class in this profile has multiplicity two. The h3771
contact sieve is used only as the survivor interface; this package makes no
new claim about its global removal percentage.
