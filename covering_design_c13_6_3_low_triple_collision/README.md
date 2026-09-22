# Low-triple collision theorem for the exceptional `C(13,6,3)` profile

This directory proves a non-enumerative structural theorem about the
exceptional point-degree profile `(12,9^12)` for a hypothetical 20-block
`(13,6,3)` covering.

Let `h` be the degree-12 point.  After deleting `h`, let `A` be the twelve
size-five residues of the blocks through `h`, and let `B` be the eight
size-six blocks avoiding `h`.  The preceding exact theorem shows that no
low triple lies in three members of `A`.

For two distinct rows in the indicated family, define

```text
k = max |A_i intersect A_j|,
l = max |B_i intersect B_j|.
```

Then `k` is one of `2,3,4` and `l` is one of `3,4,5`.  If `r_T` denotes the
total multiplicity of a low triple `T` among all twenty rows, then

```text
                    l=3   l=4   l=5
              k=2     4     6    11
              k=3     5     7    12
              k=4     8    10    15
```

is a lower-bound table for

```text
sum_T binomial(r_T - 1, 2).
```

In particular, every such cover has a low triple of total multiplicity at
least three.  Since no three through-`h` residues share a low triple, at
least one block through that triple avoids `h`.

The proof uses only double counting and the integer inequality
`binomial(s,3) >= s-2`.  It replaces a potential local-orbit catalogue by
nine global maximum-intersection classes.  It does **not** exclude the
profile and does not determine `C(13,6,3)`.

## Reproduction

CPython 3.11 or newer and the standard library suffice.

```bash
python3 audit.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

Expected status: `VERIFIED_LOW_TRIPLE_COLLISION_TABLE`.

The audit independently minimizes the three block-intersection collision
sums over all integer histograms with the forced totals.  It is a finite
check of the numerical table, while the written proof establishes its
application to covering designs.

## Files

- `PROOF.md`: complete double-counting proof and scope;
- `audit.py`: exact dynamic-programming audit of all numerical minima;
- `EXPECTED.json`: pinned audit output;
- `SOURCES.md`: primary-source and graph provenance;
- `SHA256SUMS`: compact source manifest.

