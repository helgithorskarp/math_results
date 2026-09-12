# Global reconstruction and counting for modular subset sums

This extends the [long-chain classification](../proof.md) to results
that apply to **every** admissible set. The excess-five classification
remains the main research target.

Let n>=1 and N=2^n+t, where t>=3 is odd, and require all 2^n subset sums of an
n-element set A in Z/NZ to be distinct. The [written proof](proof.md)
establishes:

1. **Sharp cycle exclusion.** If 2^n>(t-1)^2/4, the signed doubling
   graph of A has no cycle, including cycles in proper subgroups.
   An explicit infinite family attains equality with a cycle.
2. **Reconstruction and counting.** Above that threshold, the centered
   missing subset sums determine A up to independent signs. Therefore
   the number of actual sets is at most
   `2^n * binomial((N-1)/2, (t-1)/2) = O_t(N^((t+1)/2))`.
   This improves the exponent in the estimate stated in the modular
   source paper by one for fixed odd t>=3.
3. **Unrestricted excess-five bound.** For n>=3, the count is at most
   `(N-5)*(N-1)*(N-3)/8 = O(N^3)`.
4. **A one-parameter reduction at excess five.** Every centered hole
   set is a unit dilate of `{0,+/-1,+/-b}`, where
   `2 <= b <= (N-1)/2` and `gcd(b,N)` is 1 or 3. Its circulant
   determinant must be exactly 5 or 20, respectively. The core b
   determines at most one unit/sign class of A.

The full **Glaudo–Kravitz Theorem 1.5** is an external mathematical
premise for reconstruction. The proof explicitly accounts for its
proper-subgroup moves. A concrete boundary example at N=289 shows
that distinct sign classes can share centered holes when the strict
threshold is replaced by equality.

The general odd-excess argument supplies the selected excess-five
bound; it is not a new parameter-selection program. The unrestricted
O(N^2) bound and the eventual three-class classification remain open.

## Exact unrestricted classification through n=14

The determinant criterion gives a necessary congruence in any prime
field with an N-th root of unity. The finite certificate checks
**every allowed b** for each n=5,...,14. All 14,735 candidates are
covered, and the only surviving cores belong to the three known
types B0, B1 and B2. Reconstruction proves that these are all
equivalence classes in that range, with exactly
`3 * 2^(n-1) * phi(N)` actual subsets for each n.

This computation covers arbitrary admissible sets, including the
entire former chain-free residual at these parameters. It is a
finite consequence of the uniform reduction, not evidence that
replaces the all-n proof. For n>=15 the core condition remains
necessary; passing it does not certify existence.

## Replay and trust

From this directory, run:

```sh
python3 reproduce.py
```

CPython 3.11.2 and the standard library suffice; assertions must be
enabled. The replay takes approximately 16 seconds on the development
machine. Expected status:

```text
GLOBAL_EXCESS_COUNT_AND_CORE_PACKAGE_VERIFIED
```

- `certificate.json` gives one prime and exact-order root per n.
  Their validity is checked deterministically by trial division and
  modular exponentiation.
- `sieve.py` covers the complete scalar range and recomputes every
  modular determinant residue. The certificate does not assume an
  unproved restriction on doubling components or chosen sets.
- `controls.py` imports no sieve code. It checks all 49 small
  candidate circulants by direct Gaussian elimination, comparing
  their determinants with separate spectral products. It also uses
  literal subset sums for the known types, six sharp boundary
  constructions, the nontrivial proper-subgroup example, and complete
  small controls for the general reconstruction threshold.
- `expected.json` records the compact results and hashes of ordered
  determinant residues. The replay compares every summary entry
  and digest, and rejects an invalid root and a composite modulus.
- `SHA256SUMS` covers source and compact evidence. No large external
  certificate, solver, floating-point calculation or unrecorded data
  is required.

The uniform theorem is a written proof using the cited reconstruction
theorem. The finite classification also trusts Python integer
arithmetic, the exact enumeration and its coverage proof. The small
matrix checks do not constitute a second exhaustive implementation
at n=14. No proof-assistant formalization or independent peer review
is claimed.

See [literature.md](literature.md) for exact source statements and
the limits of the novelty and open-status searches.
