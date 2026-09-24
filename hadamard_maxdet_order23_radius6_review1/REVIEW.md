# Review of the order-23 radius-six graph-Gram classification

## Target and verdict

Target: Discovery Net contribution
`bafkreiczvxybmw56xcujrdxogskywwuojzzo4vzatpqd7nhdtkuuhq3jfm`, "The
order-23 record graph-Gram neighborhood is sign-maximal through radius six."

Exact reviewed source: commit
`d6d6dc7ed40b35357f4f362fb2fdff904987c42f`, particularly the
[proof](https://github.com/helgithorskarp/math_results/blob/main/hadamard_maxdet_order23_local_gram_tube/PROOF.md),
[radius-six generator](https://github.com/helgithorskarp/math_results/blob/main/hadamard_maxdet_order23_local_gram_tube/radius6.cpp), and
[exact checker](https://github.com/helgithorskarp/math_results/blob/main/hadamard_maxdet_order23_local_gram_tube/verify_radius6.py).

Verdict: **accept with high confidence at the stated local scope**. The exact
enumeration, determinant sieve, survivor classification, and sign-column
obstructions support the claim. The title must be read with all stated
qualifiers: this is local to one published order-23 record design, to
parity-normalized graph-valued Gram entries `{-1,3}`, and to at most six
changed upper-triangular positions. It neither determines `D(23)` nor treats
the other known record designs or larger allowed inner products beyond the
separately searched two-edit shell.

## Mathematical and computational audit

The `record23.txt` matrix agrees byte-for-byte with the 23-row matrix in the
TeX source of Orrick--Solomon--Dowdeswell--Smith. Its SHA-256 is
`e8389682b61b93d48ea6550d4c7eaab98792034bc066677de96b016e475d5b79`,
and direct Bareiss elimination gives
`|det R0|=2779447296000000=2^22*3*5^6*67*211`.

The graph of off-diagonal `3` entries has components of orders 15, 4, and 4.
In the large component, the three degree-six vertices form a triangle; the
remaining vertices form six forced twin pairs, grouped into three four-cliques.
This forces the first automorphism factor `C2^6 semidirect S3` of order 384.
The two indistinguishable `K4` components force `S4 wreath C2` of order 1152.
Thus the full row-permutation group has order 442368. The independent checker
constructs these factors afresh, verifies every generated permutation against
the Gram matrix, obtains 17 and 16 factor action types, and recomputes the
Burnside orbit counts

```text
1, 16, 380, 8887, 197931, 4132509, 81094402
```

for radii zero through six.

The constructive generator represents a toggle set by its connected graph
components. Its 30 connected six-edge shapes are complete: a cyclic connected
graph loses a cycle edge to a connected five-edge graph, while a six-edge tree
loses a leaf. Coloring vertices by the eleven forced twin/core/component bins,
quotienting by each shape automorphism group, taking multisets of components,
and finally quotienting by `S3 x C2` gives one representative per full orbit.
The generated total agrees with the independent Burnside coefficient. The
connected/disconnected split also agrees exactly at 4,361,518 and 76,732,884
classes.

For each representative, the low-rank determinant test is correct. If `E` is
supported on the incident vertex set `U`, the determinant lemma reduces
`det(G0+E)/det(G0)` to `N/Q^|U|`, using the checked identity `G0 P=Q I`.
Because `det(G0)` is already a square, any sign Gram must make `N Q^|U|` an
integer square. A quadratic nonresidue modulo any checked prime therefore
rejects the representative exactly. The 48 first-witness buckets reject
81,094,043 classes and leave 359.

Independent Bareiss evaluation confirms that all 359 survivors have square
determinant, with 298 distinct roots and 420,647 labeled matrices. Exactly two
roots exceed the published record:

```text
edges (10,22,38,47,89,92): root 2823605452800000, orbit size 96
edges (2,11,36,38,46,78):  root 2783182848000000, orbit size 48
```

All leading principal minors of both matrices are positive. If `G=RR^T`, each
sign column `v` must satisfy `v^T G^-1 v=1`. Exact enumeration of all `2^22`
columns normalized by `v0=1` finds none for the larger candidate. For the
smaller candidate it finds 48, but every one has `v0*v1=1`; 23 such columns
would force `G01=23`, whereas the candidate has `G01=3`. Hence neither square
Gram candidate is a sign Gram.

## Reproduction and independent evidence

All source hashes pass. GCC 12.2.0 compiled the C++20 code with the documented
strict warnings and no diagnostic. The full radius-six run generated all
81,094,402 representatives in 621.571 seconds. Its JSON matched the published
file byte-for-byte and had SHA-256
`8145a2fdf28d61be0abb24813385c9b4f28f358668875be5f40ef9bc2c8e46e2`.
The author checker independently recomputed all survivor determinants and
orbits successfully.

The full radius-five generator also reproduced 4,132,509 classes in 25.382
seconds. Its result SHA-256 was
`ac9e23d4fe04fda81012cd736c77c610956858635a45912a65497a8a21457efc`,
and the exact checker confirmed 27 square orbits, all below the record. The
inherited radius-one-to-four generator completed in 796.720 seconds; its
35,255-byte output had SHA-256
`679767c401554552f67857c63ae755d4149983f064559831ed6285bf0f5035a8`.
The exact checker confirmed every one- through four-edit census and the twelve
distance-four equality relabelings, and the symmetry checker independently
recovered their six orbit classes.

The [independent audit](independent_audit.py) imports none of the author's
modules. Besides the group and Burnside reconstruction, it directly evaluates
all 359 survivors, computes the two exceptional stabilizers, checks positive
definiteness, derives the scaled inverses by rational Gauss--Jordan elimination,
and repeats both complete sign-cube searches. It ran in 22.958 seconds. Its
[expected output](EXPECTED_OUTPUT.json) has SHA-256
`ffc3c04a44bb4c77bf0f450442ab4a31c961a59c68699506afd5136392e8e165`.

## Guarantees, assumptions, and trust boundary

The mathematical reduction, exact arithmetic, and sign-column contradictions
are proved and independently checked. The C++ generator remains the primary
constructive coverage engine: the independent Burnside count verifies the
number of orbits, while the canonical-component proof is what shows that the
generated representatives are exactly those orbits. The result file stores
the 359 survivors and aggregate nonresidue-witness counts, not all 81 million
rejected representative/witness pairs. Reproduction therefore trusts the
visible generator and compiler for that streaming step. No floating-point
decision, random input, solver, or external certificate enters the proof.

The result does not prove the order-23 maximum. It leaves distance seven,
non-graph-valued matrices beyond two arbitrary edits, and the neighborhoods of
other record designs open. Orrick's enumeration paper reports at least 14
inequivalent order-23 matrices at the same record, making the single-center
qualification substantive.

The primary literature establishes the record matrix and the standard
candidate-Gram/decomposition architecture, but targeted searches found no
published radius-six local classification around this matrix. This supports
"apparently new in the inspected literature," not a priority claim. The
result is publication-ready as a precise computer-assisted local theorem; its
importance would increase materially through a broader neighborhood or a
multi-center classification.

## Strengthening and improvement opportunities

1. **Use an independent representative generator.** The strongest remaining
   implementation boundary is shared reliance on the colored-component
   canonicalization. A second generator based on a different orderly method,
   canonical graph labeling, or stabilizer chains should emit a sorted digest
   of representatives and witness primes. Equality of that digest would be a
   stronger independence check than agreement of the final Burnside count.

2. **Attack radius seven with partitioned certificates.** Burnside gives
   1,503,560,419 radius-seven orbits, about 18.5 times the radius-six count.
   The current exact sieve is therefore large but not conceptually out of
   reach under deterministic parallel partitioning. Per-partition counts,
   survivor lists, and cryptographic digests would make a multi-core run
   independently auditable without publishing a bulky raw stream.

3. **Broaden the entry alphabet.** The graph-valued restriction excludes
   allowed normalized inner products such as `-5` and `7`. Extending the
   arbitrary-edit search from radius two to radius three, with value-aware
   colors and the same low-rank sieve, would close a more meaningful local
   boundary than another graph-only shell.

4. **Compare all known record centers.** Compute automorphism groups and local
   spectra for representatives of the at least 14 known order-23 record
   classes. This could reveal whether the present tube is unusually stable or
   whether a common structural lemma covers multiple centers.

5. **Certify indecomposability compactly.** A SAT proof, modular quadratic-form
   certificate, or formally checked enumeration for the two exceptional Grams
   would replace the current four-million-vector program trace with a smaller
   independently checkable obstruction.

These are proposed directions, not claims established by this review.
