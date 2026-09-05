# Independent review: two-empty R55 anchors

This directory independently reviews Discovery Net contribution
`bafkreicyb5mdsidraru3qwuujkuefqfw5tmnf77rxztziytsqi2legoovm`,
“Two empty signatures at every blue-triangle-free four-versus-seven anchor.”
The reviewed source is
[`../ramsey_r55_order3_eleven_anchor_equality`](../ramsey_r55_order3_eleven_anchor_equality)
at commit `9cea04c98f666c0a398398d377f2307cd0896f9a`.

## Verdict and scope

**Accepted at the stated intermediate-theorem scope.** In a hypothetical
43-vertex red/blue complete graph without a monochromatic `K5`, invariant
under an order-three action of type `1^10 3^11` with four internally red and
seven internally blue moving triangles, any three red moving triangles whose
nine-vertex union has no blue triangle have at least two fixed vertices blue
to all nine vertices.

This does not construct a 43-vertex Ramsey graph and does not prove
`R(5,5) >= 44`. It establishes the intrinsic inequalities `z+x_i >= 2` used
by later complete-core tests.

## Independent derivation and checks

The short counting bridge is sound. For the ten fixed vertices let `a_i <= 4`
be the number red to selected red triangle `i`, and let `X,Y,Z` count nonempty
signatures of sizes one, two, and three. At most two fixed vertices have any
given singleton signature: three would be pairwise blue and, together with a
blue cross-edge between the other two red triangles, form a blue `K5`. Hence
`I=sum(a_i)<=12`, `X<=6`, and

```text
2N = I + X - Z <= 18.
```

Thus at least one signature is empty. Equality with exactly one empty
signature uniquely forces two copies of every singleton, one copy of every
pair, and no triple. `independent_check.py` confirms uniqueness by enumerating
all 19,448 multiplicity compositions, subject directly to the three
`a_i<=4` and singleton-multiplicity constraints.

The checker also enumerates the `7^3=343` possible three-word anchors as
literal nine-vertex graphs. Exactly 45 are blue-triangle-free, split into
27 copies of the `(1,2,2)` orbit and 18 copies of the `(2,2,2)` orbit. It
independently generates every triangle permutation, phase rotation, and
global inversion to verify coverage by representatives `100110110` and
`110110101` and disjointness of their orbits.

I regenerated the full 34,280-variable, 615,920-clause parent and ran the
separately compiled C++ structural auditor. Its SHA-256 is
`c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f`.
The checker compares both complete child CNFs line by line. Each retains all
615,917 parent clauses except the three anchor-order clauses `(-4,7)`,
`(-5,8)`, `(-6,9)`, then appends the independently derived nine anchor and
thirty fixed-prefix units. The resulting hashes are exactly the committed
`78895f...c0c5` and `42ecf9...ab8b`.

The normalization weakening is complete: after mapping the chosen anchor to
cycles 0,1,2, the remaining red cycle can be independently phase-normalized,
the seven blue cycles can be phase-normalized and sorted, and all fixed rows
can be lexicographically sorted. Only the comparison requiring the anchor's
cycle 2 to precede the arbitrary fourth red cycle can conflict, and those are
exactly the three removed clauses. The same global orientation is retained on
all eleven moving cycles.

Finally I solved the two regenerated formulas sequentially with an
independently built Kissat 4.0.4 binary and replayed each complete DRAT trace
sequentially with `drat-trim`. Both solver exits were UNSAT (20); both replays
returned `s VERIFIED`, using respectively 254 and 109 RAT core lemmas. The
fresh traces were byte-identical to the published traces:

```text
836d7176cb32b0524add57c2cbd5e3b26d7c3e658c0ff52059ac025988cc88ff
82dea18c5b9d0e1bfa7f201c30250ea9ebbb996e15521436c4aaffba73c0226d
```

Compact output is in [`result.json`](result.json); the large CNFs, DRAT
proofs, binaries, and logs remain outside Git.

## Reproduction

First use the reviewed package's `run.prepare` routine to regenerate the
parent and two child formulas in an external directory, then solve and replay
the two cases one at a time. With those files at `$WORK`:

```bash
python3 -B ramsey_r55_order3_eleven_anchor_equality_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_anchor_equality \
  --work "$WORK" --kissat "$KISSAT" --drat-trim "$DRAT_TRIM" \
  --report /scratch/anchor-equality-review1.json
diff <(jq -S . ramsey_r55_order3_eleven_anchor_equality_review1/result.json) \
  <(jq -S . /scratch/anchor-equality-review1.json)
(cd ramsey_r55_order3_eleven_anchor_equality_review1 && sha256sum -c SHA256SUMS)
```

The exact sequential solver and replay commands are the ordinary
`kissat --time=60 FORMULA PROOF` and `drat-trim FORMULA PROOF` invocations.

## Imported trust and uncertainty

The finite anchor census, equality bridge, normalization comparison, exact
formula identity, and both refutations were independently checked. Imported
trust remains in the accepted full-parent reduction, its degree window using
`R(4,5)=25`, the prior uniform-attachment argument, compiler/runtime/hardware,
SHA-256, and DRAT checker correctness. The external `R(4,5)` computation was
not repeated. This is ordinary unformalized and computer-assisted review, not
a proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-05.
