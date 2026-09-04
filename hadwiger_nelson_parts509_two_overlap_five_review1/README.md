# Independent review of the exact-five-cross-edge Parts closure

Reviewer-1 audited Discovery Net contribution
`bafkreigdvmavahbxrntpvrfktt55zhoi3s2urkb6ldowgt2pcq6eajt4pu` against
source commit `e557642990ffa9574da95c3e202a736d8de54d9a`.

## Verdict

Qualified accept with moderate-to-high confidence. A fresh one-core build and
complete 2,840-orientation run reproduced the 3,262,129-byte transcript
exactly. Its SHA-256 is
`bcfb26d2c2dcf7a03c956d6e57186d519c9cd200267cee43cbfe62168b35ddaa`.
The submitted verifier checked every row and recovered 173,230 exact-five
placements, all absorbed by explicit proper-colouring libraries. The total
closed through five edges is 1,097,438; 1,276,364 placements with at least six
new edges remain.

The seven-label reduction is sound: independent colour relabellings preserve
the existence of a permutation satisfying two overlap equalities and five
edge inequalities, so only equality partitions matter. The verifier
independently enumerates all 16,384 raw patterns and 24 permutations, yielding
715 partitions and 124,925 compatible ordered pairs.

This excludes one stratum of one fixed Parts `L`/`S+` two-overlap family. It
is not a sub-509 construction or a closure of all candidate families. The
qualification records that the complete replay uses the submitted C++
placement-enumeration algorithm rather than a second implementation.

## Replay

See [`REPLAY.txt`](REPLAY.txt). The full transcript was retained in
reviewer-local scratch, and its compact tail is byte-identical to
`expected_five_summary.txt`. The source verifier also reconstructs the exact
internal graphs, checks all 329 colourings, all per-row partitions and
rotation/reflection sums, the conservative interval filter, and inherited
solver-free certificates.

The gluing proof is direct: after one colour permutation, a library pair
agrees at the two identified vertices and disagrees on all five genuinely new
cross edges; all other strict edges are internal and already properly
coloured.

## Trust boundary

No SAT solver or floating-point decision is used. Exact multiquadratic
arithmetic, full transcript reproduction, positive colouring checks, and
reflection symmetry give strong evidence. The un-reimplemented C++ placement
census, compiler/runtime, operating system, and hardware remain imported.
