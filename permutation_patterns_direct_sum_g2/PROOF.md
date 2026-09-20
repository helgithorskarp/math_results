# Proof of direct-sum locality

## 1. Intrinsic input

We use the committed intrinsic rooted-lens theorem.  For each adjacent
position boundary `p|p+1` of a permutation `w`, take the least permutation
interval containing those two positions, standardize it, and retain the
corresponding local root.  The theorem says

```text
j(w) = number of boundaries whose least rooted interval is a lens.       (1)
```

This is a proved translation of Ray--West Proposition 8.5 and Corollary
8.6, not a computational conjecture.  Its proof and exact audits are in the
repository directory `permutation_patterns_intrinsic_g2` and in Discovery
Net contribution
`bafkreid5j6wjz76hzdubwyuwa7f3sxaowzd2khypeybf6bsjbhtybea34y`.

We also recall the elementary lens cut lemma.  A rooted lens which is a
direct sum across its root is exactly

```text
delta_u direct_sum delta_v                              (u,v>=1),          (2)
```

where `delta_d=d...(2)(1)`.  Dually, a rooted lens which is a skew sum
across its root is exactly a skew sum of two increasing permutations.  One
way to see (2) is to use the two path words defining a lens: a direct-sum
cut first forces the central width parameter `w=1`, then the alternating
central rows force `h=1`; the two paths become the two decreasing blocks.
This lemma is proved in full in `permutation_patterns_g2_minimizers`.

For a permutation `w` of length `n`, put

```text
L_down(w)=1  iff  w(1)...w(b)=b...(2)(1), b=w(1),
R_down(w)=1  iff  w(n-a+1)...w(n)=n...(n-a+1),
                         a=n+1-w(n).                    (3)
```

Both conditions allow an anchor of length one.

## 2. Least intervals under a direct sum

Let `pi=alpha direct_sum beta`, with `alpha` of length `r`.  Write the
canonical sum decompositions into nonempty sum-indecomposable factors as

```text
alpha=A_1 direct_sum ... direct_sum A_k,
beta =B_1 direct_sum ... direct_sum B_l.                  (4)
```

The least interval at a boundary internal to `alpha` is unchanged after
forming `pi`.  Indeed, its least interval in `alpha` is still an interval of
`pi`, while an interval using a position of `beta` must also cross the
summand junction and is strictly larger.  The same argument applies to a
boundary internal to `beta`.  Formula (1) therefore preserves every
internal contribution to `j`.

The least interval at the junction is exactly

```text
A_k direct_sum B_1.                                      (5)
```

Its union is certainly an interval.  Any smaller interval crossing the
junction has a value range crossing the sum cut, so its intersection with
`A_k` would be a proper terminal sum component of `A_k`, or its intersection
with `B_1` would be a proper initial sum component of `B_1`.  Either option
contradicts sum indecomposability.

By the lens cut lemma, the rooted interval (5) is a lens exactly when both
`A_k` and `B_1` are decreasing.  The last canonical component `A_k` is
decreasing exactly when `alpha` has the terminal anchor in the definition of
`R_down`: if `x=alpha(r)`, that component is
`r,r-1,...,x`, of length `r-x+1`.  Similarly, `B_1` is decreasing exactly
when `L_down(beta)=1`.  Hence the junction contributes

```text
R_down(alpha)L_down(beta).                               (6)
```

This proves both necessity and sufficiency without enumerating insertion
triples.

For comparison with the original insertion language, if the two anchors
have lengths `a=r+1-alpha(r)` and `b=beta(1)`, the successful junction is
witnessed explicitly by

```text
(12; (r-a+1,r), (r+2,r+b+1))
  ~ (12; (r+2,r+b+1), (r-a+1,r)).                        (7)
```

The exact checker audits (7), but the structural proof is (1)--(6).

## 3. Main formula and iterations

Adding the unchanged internal boundaries to (6) proves

```text
j(alpha direct_sum beta)
 = j(alpha)+j(beta)+R_down(alpha)L_down(beta).             (8)
```

The endpoint indicators themselves satisfy

```text
L_down(alpha direct_sum beta)=L_down(alpha),
R_down(alpha direct_sum beta)=R_down(beta).
```

Induction in (8) consequently gives

```text
j(w_1 direct_sum ... direct_sum w_t)
 = sum_i j(w_i)
   + sum_(i=1)^(t-1) R_down(w_i)L_down(w_(i+1)).           (9)
```

## 4. Skew-sum dual

The correction `j` is invariant under the dihedral symmetries of a
permutation matrix.  Complementation takes a direct sum to a skew sum.  Put

```text
L_up(w)=1 iff, for b=n+1-w(1),
             w(1)...w(b)=w(1),(w(1)+1),...,n,

R_up(w)=1 iff, for a=w(n),
             w(n-a+1)...w(n)=1,2,...,a.
```

Applying (8) after complementation gives

```text
j(alpha skew_sum beta)
 = j(alpha)+j(beta)+R_up(alpha)L_up(beta).                (10)
```

## 5. Consequences and boundary

For a decreasing permutation of length `d`, both descending anchors equal
one and `j=d-1`.  Applying (9) to a direct sum of decreasing layers recovers
the known layered formula `j=m-1`; complementation recovers the colayered
case.

The theorem also explains a useful negative finding.  The permutation
`2413` is bondless, has `j=2`, and has both descending anchors zero.  Hence

```text
j((2413)^(direct_sum t))=2t.                              (11)
```

No junction creates a bond, so this is an infinite bondless family.  Thus a
putative uniform bound on `j` for bondless permutations is false; direct-sum
locality, rather than bond count alone, is the stable invariant.

The intrinsic rooted-lens theorem already computes `j` for arbitrary
permutations, and the exact minimizer theorem already classifies the case
`j=m-1`.  The new content here is the algebraic decomposition rule
(8)--(10), closing the explicit `0/1` direct-/skew-sum bridge suggested in
the independent review of the layered theorem.  It does not replace those
stronger global results or address codimension three.
