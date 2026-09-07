# Reduction and finite proof

## Family

Let `A` and `B` have orders 20 and 23. A rank-four red cross matrix has a
full-rank factorization `M = U V^T` over `F_2`. In this family the rows of `U`
contain all 15 nonzero vectors once plus five distinct vectors a second time.
The rows of `V` contain all 15 nonzero vectors once plus eight distinct vectors
a second time. Thus a labeled factor-multiset type is selected by a five-set
`R` and an eight-set `C` of nonzero vectors.

Permuting vertices within `A` or `B` does not affect completion. Replacing
`U` by `UL` and `V` by `V(L^-1)^T` preserves `M`, so the dual action of
`GL(4,2)` acts on `(R,C)`. The affine-hyperplane choices
`C={y:w dot y=1}` are already excluded for every `R` by h3757, independently
accepted at h3761. There are therefore

```text
binom(15,5) * (binom(15,8)-15) = 19,279,260
```

new pairs to cover.

## Retained-family interface

The h3765 all-pattern sieve, independently accepted at h3775, requires
nonzero row multiplicity at most four, nonzero column multiplicity at most
five, zero-row multiplicity at most one and zero-column multiplicity at most
two. The full-support profile passes these conditions. The later universal
four-set result h3783 strengthens the row cap from four to three, which the
profile also passes. The h3771 contact sieve imposes further necessary
conditions depending on the cross contacts and leaves all 443 internal edges
free.

The computation below does not assume that a particular member passed the
contact sieve. It tests physical completion for every member of the profile.
Consequently the UNSAT result excludes, in particular, every h3771 survivor
in this profile. The exact Discovery Net dependencies are:

- affine-family exclusion h3757:
  `bafkreiffq7rohzu5n36ofcrt6gyxnvm5trsv2itm3i7irz6rn6ooxc5d3m`;
- independent affine review h3761:
  `bafkreifojsvu5b2odgdvbnpeqxc7nle6v6kwbccssh7jnrmnhgbpjxcqge`;
- all-pattern sieve h3765 and review h3775:
  `bafkreiavk3pxk4pgvc3qtvaidwel6soziainidwpzv6qxrdnsnzllyf4au` and
  `bafkreidecchjvcc76x2y6ly7nl7nebqoqxrt6bujkey7u3gauq7gu2zxve`;
- contact-sieve interface h3771:
  `bafkreifgvetmpnhwbxy3g54shh5mg46n67y6g7jagspxnczdz65wjz45vm`;
- four-set row cap h3783:
  `bafkreid3nkrla4lawza3mmhtribgfzhsfhjlc5hsgri4pzklunsejid42q`.

## Orbit coverage

The production enumerator uses adjacent basis swaps and one transvection.
Their generated group has order 20,160, so it is all of `GL(4,2)`. Breadth-
first orbit marking partitions the 19,279,260 pairs into 1,348 orbits, of
sizes between 840 and 20,160.

The independent audit constructs all 20,160 ordered bases directly. The
five-subsets split into four orbits of sizes 168, 315, 840 and 1,680. Their
stabilizers have respectively 201, 661, 394 and 92 orbits on the 6,420
non-affine eight-subsets. These counts sum to 1,348, and the canonical
stabilizer images of the manifest representatives equal every such orbit.

## Physical completion formulas

Fix one representative `(R,C)`. Its 460 cross edges are the fixed dot
products of the corresponding factor labels. The remaining 443 within-side
pairs are Boolean variables, with true meaning red.

For each five-set `S` of physical vertices:

- if every fixed cross edge in `S` is red, add the clause saying at least one
  internal edge in `S` is blue;
- if every fixed cross edge in `S` is blue, add the clause saying at least one
  internal edge in `S` is red.

If a fixed cross edge already has the opposite color, that monochromatic case
is impossible and no clause is needed. Hence a truth assignment satisfies the
formula exactly when the fixed cross matrix has a physical completion with no
red or blue five-clique. No degree bound, local relaxation or omitted internal
edge is involved.

The 1,348 formulas have 139,963 to 143,680 clauses, totaling 190,848,992.
Every formula is distinct. CaDiCaL returned UNSAT for every case, emitted a
nonempty textual DRAT proof, and `drat-trim` verified every proof. Therefore no
non-affine member has a good43 completion. Combining this with h3757 excludes
the complete full-support multiplicity profile.

## Limits

This family is one broad stratum inside the retained rank-four cut family. It
does not cover factor lists omitting nonzero labels, using zero labels, or
having other allowed multiplicities. A hypothetical good43 need not have any
rank-four 20+23 cut. The result does not change `R(5,5) >= 43`.
