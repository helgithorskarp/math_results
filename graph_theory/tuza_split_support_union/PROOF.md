# Proof of the support-union criterion

All graphs are finite and simple.  A triangle packing is a family of
pairwise edge-disjoint triangles and a triangle cover is a set of edges
meeting every triangle.  Their maximum and minimum sizes are `nu(G)` and
`tau(G)`.

## 1. Statement

Fix a split partition

```text
V(G) = C disjoint-union I,    G[C]=K_k,    G[I] empty,
```

where `k>=3`.  A vertex of `I` is *active* when it has at least two
neighbors in `C`; precisely these independent-side vertices occur in a
triangle.  Put

```text
U = union { N(x) intersect C : x in I is active },    u=|U|.
```

Let `p(k)=nu(K_k)`.  The classical maximum partial Steiner triple-system
formula is

```text
p(k) = (binom(k,2)-L(k))/3,                              (1)

L(k)=0       for k=1,3 (mod 6),
     4       for k=5   (mod 6),
     k/2     for k=0,2 (mod 6),
     k/2+1   for k=4   (mod 6).
```

Define

```text
D(k)=-k^2+2k+8p(k),
u_*(k)=floor((k+sqrt(D(k)))/2).                          (2)
```

The discriminant is nonnegative for every `k>=3`; the residue forms in
Section 4 make this immediate.

**Theorem.** If `u<=u_*(k)`, then `tau(G)<=2nu(G)`.

There is no restriction on the number of distinct neighborhoods in `I`,
their multiplicities, or the order of `G`.

## 2. A cover retaining every active spoke

Choose `L subset C` with `U subset L` and

```text
ell=|L|=max(u,floor(k/2)).                               (3)
```

This is possible because `u<=ell<=k`.  Delete every clique edge with both
ends in `L` or both ends in `C\L`; call the deleted set `D`.

Every triangle entirely in `C` has two vertices on the same side of this
cut and therefore meets `D`.  A triangle with a vertex `x in I` has its
other two vertices in `N(x) subset U subset L`, so its clique edge lies in
`D`.  Inactive vertices lie in no triangle.  Thus `D` is a triangle cover.
No edge incident with `I` is deleted.

The cut has `ell(k-ell)` edges, and (3) maximizes that product subject to
`ell>=u`.  Consequently

```text
tau(G) <= binom(k,2)-b_k(u),                             (4)
b_k(u)=max_{u<=h<=k} h(k-h)
      =floor(k^2/4)                    if u<=ceil(k/2),
       u(k-u)                          if u>=ceil(k/2).
```

At the common endpoint the two expressions agree.

## 3. Clique packing and the exact threshold

The specified clique is a subgraph of `G`, so (1) supplies a packing in
`G` and

```text
nu(G) >= p(k).                                           (5)
```

First suppose `u<=ceil(k/2)`.  By direct substitution in (1),

```text
binom(k,2)-floor(k^2/4) <= 2p(k)                         (6)
```

for each of the six residues of `k` modulo 6.  This is also included in
the elementary residue audit in Section 4.  Equations (4)--(6) prove the
claim in the balanced range.

Now suppose `u>=ceil(k/2)`.  Combining (4) and (5), the two universal
witnesses prove Tuza's inequality exactly when

```text
binom(k,2)-u(k-u) <= 2p(k).
```

After multiplying by four and completing the square, this becomes

```text
(2u-k)^2 <= -k^2+2k+8p(k) = D(k).                        (7)
```

Since `2u-k>=0`, condition (7) is equivalent, for integral `u`, to

```text
u <= floor((k+sqrt(D(k)))/2)=u_*(k).                     (8)
```

The same bound includes the balanced range because `u_*(k)>=ceil(k/2)`.
This proves the theorem.  It also proves that `u_*(k)` is the largest
integer support size for which the displayed clique-only packing and
one-block spoke-preserving cut certify the inequality for every graph.
This certificate exactness is not a converse to Tuza's conjecture.

## 4. Residues and asymptotics

Substituting the four leave values from (1) into (2) gives

```text
3D(k) = k^2+2k       for k=1,3 (mod 6),
        k^2-2k       for k=0,2 (mod 6),
        k^2-2k-8     for k=4   (mod 6),
        k^2+2k-32    for k=5   (mod 6).                  (9)
```

For the relevant residues and `k>=3`, these quantities are nonnegative.
The inequality (6) is checked by inserting the same four values; after
clearing denominators it reduces to a nonnegative quadratic in each
residue, with the cases `3<=k<=8` immediate directly.

Equation (9) gives

```text
sqrt(D(k))/k -> 1/sqrt(3),
u_*(k)/k -> (1+1/sqrt(3))/2.
```

The floor contributes at most `1/k` after normalization.  This completes
all claims.

## 5. Scope and trust boundary

The proof imports only the classical exact formula (1) for maximum
edge-disjoint triangle packings of complete graphs.  The cover is explicit
and the comparison is elementary integer arithmetic.  The accompanying
program checks formula transcription, residue identities, threshold
equivalence, and the cover definition on finite fixtures.  It neither
enumerates candidate counterexamples nor proves the classical packing
theorem anew.
