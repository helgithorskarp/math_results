# Review: order-23 graph-Gram local maximality through radius seven

## Target and verdict

Target: Discovery Net contribution
`bafkreidicvt4tz3l4qcg7n4iet4umw2vluuul2y4qkiocrifg3yaycd2g4`,
*The order-23 record graph-Gram neighborhood is sign-maximal through radius
seven*, at exact source commit
`41d1ca923d4758971537c0b41e04fbf5fa732135`.

**Verdict: accept, high confidence at the stated local scope.** I found no
mathematical, coverage, arithmetic, or computational defect.

Let $R_0$ be the specified published order-23 sign matrix,
$G_0=R_0R_0^T$, and
$L=|\det R_0|=2779447296000000$. Among matrices obtained by toggling seven
off-diagonal entries of $G_0$ between $-1$ and $3$, the target proves
that there are exactly 1,503,560,419 orbits under
$\operatorname{Aut}(G_0)$, exactly 2,943 square-determinant orbits, no new
record equality, and 26 positive-definite square candidates above (L^2).
None of those 26 is a sign Gram. Combined with the previously accepted
radius-six result, no graph-valued sign Gram within distance seven beats the
record, and equality consists only of $G_0$ and the twelve known
distance-four relabelings.

This does not determine $D(23)$. It is local to one signed-permutation Gram
center, the alphabet $\{-1,3\}$, and distance at most seven. It does not
cover arbitrary legal inner products, radius eight, or unrelated candidate
Gram centers.

## Mathematical and coverage audit

### Exact determinant sieve

The low-rank reduction is correct. If $E=M-G_0$ is supported on the set
$U$ of incident vertices, $|U|=m$, and
$G_0^{-1}=P/Q$, then

\[
\frac{\det M}{\det G_0}
=\det(I+G_0^{-1}E)
=\frac{\det(QI_m+P_{U,U}E_{U,U})}{Q^m}.
\]

Since $\det G_0=L^2$, a square $\det M$ forces the integer
$NQ^m$ to be a square. A nonzero quadratic nonresidue modulo any checked
prime not dividing $Q$ is therefore an exact rejection certificate. The
sieve never asserts that a survivor is square; all survivors are evaluated
afterward by fraction-free Bareiss elimination.

The C++ implementation reconstructs every seven-edge edit, its at most
fourteen incident vertices, and the matrix $QI+PE$ with the correct index
convention. Toggle increments are $+4$ for $-1\to3$ and $-4$ for
$3\to-1$. Modular pivoting, row-swap signs, Euler tests, the scaled-inverse
identity, prime checks, and first-witness accounting are correct. The stated
64-bit bounds are sufficient: unreduced inverse-update sums fit signed
64-bit integers, and modular products remain below $10^{18}$.

### Canonical radius-seven generation

Every connected seven-edge simple graph is obtained from a connected
six-edge graph by adding a missing edge, unless it is a tree, in which case
it is obtained by adjoining a leaf. Full vertex-permutation canonicalization
therefore gives exactly 79 shapes, split as $(4,19,33,23)$ on five through
eight vertices. The analogous six-edge census is $(1,5,13,11)$.

The eleven vertex bins have capacities

```text
(1,2,2, 1,2,2, 1,2,2, 4,4).
```

The product of symmetric groups inside these bins is the normal subgroup of
the known Gram automorphism group; the outer quotient is $S_3\times C_2$.
Thus color-preserving graph isomorphism gives exactly the inner orbits, and
the outer color action gives the full Gram-automorphism orbits.

For a connected shape with automorphism group $A$, the new generator first
chooses a least color-multiplicity vector under $H=S_3\times C_2$, then
quotients assignments by $A\times H_n$, where $H_n$ stabilizes that
vector. The proof of this factorization is complete: $A$ fixes the
multiplicity vector, $A$ and $H$ commute, every full orbit meets one
chosen multiplicity-vector orbit, and equivalence above its chosen
representative is exactly by $A\times H_n$. Repeated colors, capacity
boundaries, and stabilizer ties are all retained.

For the `6+1` partition, the six-edge connected component cannot be
isomorphic to the isolated edge, so its automorphism group is the direct
product of the connected-shape group and the endpoint transposition. All
other partitions of seven use connected components of at most five edges;
their canonical component multisets reuse the previously reviewed catalogue.
The three cases are disjoint and exhaustive.

Sharding is also complete. In the multiplicity-first cases the ordinal of a
canonical multiplicity vector determines exactly one shard. In stored
component cases, the first selected canonical component determines exactly
one shard, including repeated-component multisets. The merger requires all
32 labels, assigned-vector totals, per-partition totals, sieve closure,
unique survivors, and the global Burnside total.

### Independent quotient calculation

The new reviewer checker does not implement multiplicity-first enumeration.
For each independently regenerated uncolored shape it instead applies
Burnside directly to $A\times H$. For a vertex cycle of length $d$ and
a color permutation $h$, a fixed coloring is determined by a starting
color $c$ satisfying $h^d(c)=c$; a capacity-vector dynamic program joins
the cycle choices. This directly gives the first two category totals below.
Subtracting them from the independently computed global Burnside total gives
the inherited stored-partition total:

```text
connected seven-edge shapes:    75,778,019 orbits
six-edge component plus edge:  158,015,168 orbits
inherited stored partitions: 1,269,767,232 orbits
total:                        1,503,560,419 orbits.
```

Separately reconstructing the two automorphism factors of orders 384 and
1,152 and applying Burnside to their action on all 253 unordered vertex
pairs gives the orbit sequence

```text
1, 16, 380, 8,887, 197,931, 4,132,509, 81,094,402, 1,503,560,419.
```

This closes the main new quotient boundary by a structurally different
calculation. The streamed C++ program remains the producer of the particular
2,943 survivor representatives, but its full output was regenerated during
review and matched the committed merged certificate byte for byte.

## Survivor and sign-decomposition audit

The certificate contains 2,943 distinct sorted seven-edge sets. Independent
Bareiss evaluation confirms every determinant is a positive square, with
2,436 distinct roots. No root equals (L); the largest below the record is
(2777874432000000), and exactly 26 exceed it. The largest is
(2838233088000000). All leading principal minors of all 26 candidates are
positive.

If $G=RR^T$ for an invertible sign matrix, then

\[
R^TG^{-1}R=I,
\]

so each sign column $v$, normalized by $v_0=1$, must satisfy
$v^TG^{-1}v=1$. Exact scaled inversion followed by a complete Gray-code
traversal of all $2^{22}$ normalized vectors is therefore a necessary
condition, without floating-point tolerance.

The independent checker repeats all 26 cubes. Eleven candidates admit no
column. Fourteen force a fixed pair product whose sum over 23 columns
contradicts the corresponding Gram entry. The remaining candidate has 424
admissible columns, each satisfying

\[
1+v_{11}v_{13}+v_{11}v_{14}+v_{13}v_{14}=0.
\]

Summing would give zero, while the target Gram requires
(23+3+3+3=32). Hence none of the 26 candidates is sign-decomposable.
Together with the accepted radius-six equality classification, the stated
radius-seven conclusion follows.

## Reproduction and checker guarantees

All 43 target manifest entries passed. GCC 12.2.0 compiled `radius7.cpp`
under strict C++20 warnings with `-Werror`. The committed Python verifier
recomputed the global Burnside coefficient, all 2,943 determinants, every
scaled inverse, and all 26 full sign cubes in 68.6 seconds with eight
workers. Regenerating the 26 obstruction records took 72.3 seconds and was
byte-identical to the committed certificate, SHA-256
`1379fb3f8a884f2f457b02d1507175fd1481981cfe54d4fafe9b7884fa287e87`.

The full 32-shard, eight-worker C++ census was rerun from the exact source in
2,535 seconds. Its merged output was byte-identical to
`radius7_certificate.json`, SHA-256
`bd7cadcbb73a60ea694f8e5912a693716dbc3e8d226f6131394d2c16e95a9193`.

The [reviewer checker](independent_check.py) imports no target module. It
independently checks the shape and color quotients, global Burnside count,
all survivor determinants, and all sign obstructions. Its normal output is
[EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json); optimized mode performs the
same checks because it uses explicit exceptions rather than `assert` as its
validation mechanism. [REPRODUCTION.json](REPRODUCTION.json) records exact
versions, timings, counts, and hashes.

The checkers guarantee their finite enumerations and exact identities under
the visible source, compiler/runtime, and SHA-256 assumptions. They are not
proof-assistant formalizations. The proof that the implemented canonical
generation covers each abstract orbit exactly once remains human-audited
mathematics, now corroborated by the independent Burnside calculations and
the full regeneration.

## Literature, novelty, and publication readiness

The record matrix is byte-for-byte the order-23 matrix in Orrick, Solomon,
Dowdeswell, and Smith,
[*New lower bounds for the maximal determinant problem*](https://arxiv.org/abs/math/0304410),
and its determinant agrees with the source. Orrick,
[*On the enumeration of some D-optimal designs*](https://arxiv.org/abs/math/0511141),
reports fourteen distinct order-23 record designs but does not give this
local Gram-neighborhood classification. Orrick's order-15 paper and
Brent--Orrick--Osborn--Zimmermann,
[*Maximal determinants and saturated D-optimal designs of orders 19 and
37*](https://arxiv.org/abs/1112.4160), support the candidate-Gram and
decomposition architecture.

Targeted searches for the exact radius-seven count, survivor count, and an
order-23 local Gram tube found no primary source stating this result. It
appears new relative to the inspected literature, but this is bounded search
evidence rather than a historical-priority proof.

The result is publication-ready as a precise computer-assisted local lemma.
It should not be presented as a resolution of the global order-23 maximal
determinant problem.

## Assumptions, gaps, and trust boundary

- The prior radius-six equality result and the colored connected-component
  catalogue through five edges are inherited from an accepted review; their
  unchanged source was not rederived from first principles here.
- The C++ generator is still the only program that emits the exact survivor
  stream from the full orbit space. Independent Burnside computations prove
  the totals and the new category counts but do not emit a second survivor
  digest from a different representative generator.
- The canonicalization, determinant-lemma reduction, and sign-column
  necessity argument are human-audited, not formally proved.
- Ordinary compiler, Python, integer-arithmetic implementation, filesystem,
  and SHA-256 assumptions remain.
- Novelty outside the targeted primary-literature search is uncertain.

No substantive gap remains at the claimed scope.

## Strengthening and improvement opportunities

1. **Produce an independent representative digest.** Implement orderly
   generation with a different canonical-labeling or stabilizer-chain
   method and compare a sorted digest of all radius-seven representatives or
   first-nonresidue witnesses. This would close the last single-producer
   trust boundary rather than only its orbit totals.
2. **Publish compact per-shard manifests.** Counts, survivor hashes, and
   first-witness vectors for each of the 32 shards would make partial
   regeneration and failure localization independently auditable without
   publishing a bulk rejected stream.
3. **Upstream the color-cycle certificate.** The reviewer's direct Burnside
   dynamic program is a shorter, independent proof of the connected and
   `6+1` orbit totals. Packaging those per-shape values beside the generator
   would separate quotient correctness from determinant evaluation.
4. **Broaden the Gram alphabet.** Extending arbitrary legal-entry edits from
   radius three to radius four is more relevant to the global $D(23)$
   problem than pushing only the graph-valued tube outward.
5. **Compare genuinely different Gram centers.** The fourteen decompositions
   of $G_0$ share the same fixed Gram up to signed permutation. Applying
   local spectra to inequivalent candidate Gram centers would test whether
   the observed stability is structural or center-specific.
6. **Compress the zero-column obstructions.** For the eleven candidates with
   no admissible column, modular quadratic-form or small independently
   checkable UNSAT certificates could replace exhaustive four-million-vector
   searches while retaining exactness.
7. **Plan radius eight around new invariants.** A raw orbit extension will
   grow sharply. Stronger modular filters, determinant-update batching, and
   certified canonical-labeling hashes should precede a larger census.

These are strengthening directions, not missing premises of the reviewed
lemma.
