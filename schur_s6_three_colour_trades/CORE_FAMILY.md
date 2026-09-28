# A fixed-core splitting criterion for a family of 536-colourings

The certificate supplies six disjoint sum-free sets `B_1,...,B_6` in
`[1,536]`, of sizes **34, 38, 35, 39, 37, 42**. Their union has 225 elements.
The sets are listed in [core_family.json](core_family.json).

**Theorem.** Every valid classical six-colouring `C` of `[1,537]` splits at
least four of these six sets: at least four `B_i` contain two different
`C`-colours. Repeated summands are included.

Consequently, let `F` be **any** six-colouring of `[1,536]` satisfying
`F(v)=i` for `v in B_i`. Every valid six-colouring of `[1,537]` must split
at least four of the six colour classes of `F`. The other **311 positions
are not prescribed by this criterion**. The statement holds in particular
for every valid `F` with those fixed core values.

This is a family extension of the baseline component of the earlier
[four-input splitting theorem](SPLITTING.md). The witness vertices no longer
need specified old colours. The certificate also exhibits a Cartesian
family of **2^53 = 9,007,199,254,740,992 distinct valid 536-colourings**
satisfying the core conditions. It does not assert that all assignments to
the 311 unprescribed positions are valid, or classify all valid assignments.
Neither 225 nor 53 is asserted optimal. This supplies no valid 537-colouring
and no new lower or unrestricted upper bound for `S(6)`.

## General criterion

For `B subset [1,N]`, put

    D_N(B) = ((B+B) union positive(B-B)
              union {b/2 : b in B, b even}) intersect [1,N].

Let `B_1,...,B_k` be nonempty, disjoint, sum-free subsets of `[1,N]`, and
let `1 <= r < k`. Assume:

1. For each `i<j`, the union `B_i union B_j` contains an integer Schur
   triple whose vertices use both sets.
2. For every set `I` of `r` indices, the intersection
   `intersection_{i in I} D_N(B_i)` contains a set `W_I` that cannot be
   coloured into `k-r` sum-free classes.

Then every valid `k`-colouring of `[1,N]` splits at least `k-r+1` of the
sets `B_i`.

**Proof.** Suppose `r` of the sets remain monochromatic. Their colours
must be distinct: if two shared a colour, condition 1 would supply a
monochromatic triple. For `v in D_N(B_i)`, giving `v` the colour of that
monochromatic `B_i` creates a triple. The three possibilities are
`v=a+b`, `a+v=b`, or `v+v=a`, with the other vertices in `B_i`.
Thus every vertex of `W_I` avoids all `r` of those colours. Its restriction
uses at most `k-r` colours, contradicting condition 2. At most `r-1` of
the cores can therefore remain monochromatic. This proves the criterion.

If `F` has colour classes `A_i` containing `B_i`, every core split by `C`
also forces its containing `A_i` to split. This proves the stated family
consequence. No values of `F` away from the cores enter the argument.

## The finite instance: k=6, r=3, N=537

The new certificate supplies all 15 pair witnesses using only core
vertices. For condition 2 it reuses the 20 baseline kernels in
[class_splitting.json](class_splitting.json), with the old free palette
interpreted solely as the complement of `I`.

The verifier forgets all old colours outside the 225 core positions. It
enumerates every integer triple through 537, including `x=y`, to compute
which target colours are forbidden by the remaining core vertices. A
forgotten vertex supplies no premise. All **3,189** required kernel/colour
incidences remain blocked. Crucially, it makes **no old class membership
test on the vertices of `W_I`**; only the blocking premises are retained.

It then checks all 20 kernels by the existing exact finite-domain
enumerator. Their sizes are 33--80, and all **720,107** search nodes are
completed. There is no cutoff. Root colour normalization, singleton
propagation, and exhaustive branching are justified in [PROOF.md](PROOF.md).
These facts establish both conditions of the general criterion.

## A positive family of inputs, without enumerating 2^53 words

Start from the directly verified Fredricksen--Sweet 536-colouring in
[fixtures.json](fixtures.json), with provenance in [README.md](README.md).
The new certificate lists 53 different positions outside the cores. At
each such position retain either its old colour or the supplied alternative,
independently. Every other position keeps its old colour.

Write `L(v)` for this set of one or two possible colours. The checker
verifies, for every `x<=y` and `x+y=z<=536`, that

    L(x) intersect L(y) intersect L(z) is empty.

If any independent choice created a monochromatic triple of colour `d`,
then `d` would lie in that intersection, a contradiction. This checks the
whole Cartesian family using the **71,824** integer triples; no sampling
or enormous enumeration is needed. Conversely, a nonempty intersection
would itself permit a bad choice, so this is an exact criterion for such
a product family, including doubling triples.

There are exactly `2^53` different labelled words in this subfamily, since
each switch has two distinct colours at a different position. They also
remain distinct up to global colour permutation: all six nonempty cores
keep their fixed labels, so any permutation identifying two of these words
would have to fix every label. All these words obey the uniform splitting
conclusion. This construction is included to show that the criterion
covers a substantial family, not merely four further fixtures.

## Verification and regeneration

Python 3.11+ and the standard library suffice. From this directory:

```sh
python3 -B check_core_family.py
python3 -B test_core_family.py
```

Expected output:

```text
PASS core_family cores=225 free_positions=311 kernels=20 nodes=720107 product=2^53
core_family_sha256=6933d5d6c4aad46152fbd671a38ac73daf5bba5e7f61edd1d0d7446225ed128a
```

The new certificate is 8,481 bytes and binds the unchanged kernel and
fixture files by SHA-256. Normal and optimized CPython runs agree. The
main check takes about 16 seconds and 17 MiB resident memory. Three test
groups compare the product criterion with every assignment in 351 small
domain systems, covering both valid and invalid families, reject an unsafe
doubling switch and a switch inside a
core, and check forgotten-premise, pair-coverage, and core-disjointness
guards. The existing enumerator and blocking routine have their own
separate controls in `test_checker.py` and `test_splitting.py`.

Optional deterministic regeneration, also standard-library only:

```sh
python3 -B discover_core_family.py --output /tmp/schur-core-family.json
cmp core_family.json /tmp/schur-core-family.json
```

The producer greedily deletes support vertices while preserving coverage
of every required block and pair witness, using 128 fixed-seed orders.
It then chooses compatible binary switches with 128 fixed-seed orders.
The checker imports neither part of that search. Minimality, discovery
completeness, and heuristic success are not proof premises.

The logical trust boundary is the general criterion, the Cartesian-family
argument, literal integer-triple construction, and terminating finite-domain
enumeration. There is no SAT soundness premise, omitted large certificate,
floating-point inference, or proof assistant. Independent researcher review
is pending. No historical novelty is claimed for the elementary principles;
the concrete fixed-core certificate and its uniform family are the increment.
