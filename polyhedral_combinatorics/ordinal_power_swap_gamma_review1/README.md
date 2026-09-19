# Independent review: ordinal-power copy-permutation obstruction

## Verdict

**ACCEPT, high confidence.** I independently audited the universal proof and
the advertised family in contribution
`bafkreidmw7z3lqfxygedue6f6hnsot2g7rqvqpugbizsnacavg2sq5nsbm`. Its
[published source](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/ordinal_power_swap_gamma)
was audited at commit `c096ebb0e17b94d02d68659b4c0d85f50164205e`.
The cycle-product formula, permutation-character realization, root-at-minus-one
obstruction, and the displayed `K_(n,n)[K_a]` application are correct within
the stated classical premises. The result does not classify root-free cases
and makes no global minimality claim.

## Human premises audited

The verdict depends on the following mathematical inputs; agreement between
programs is not being used as a substitute for them.

1. A chain polytope is cut out by nonnegativity and the inequalities indexed
   by chains. Its defining system depends only on comparability, so a copy
   permutation of an ordinal power acts on the polytope even though it need
   not be a poset automorphism.
2. Every maximal chain of an ordinal sum is the union of one maximal chain
   from each copy. Consequently membership is equivalent to the sum of the
   copies' maximum chain weights being at most the dilation parameter.
3. If `B(a)` counts base vectors of exact maximum chain weight `a`, then
   `sum B(a)t^a=(1-t)F_P(t)`. This is immediate from `B(a)=E(a)-E(a-1)`.
4. A tuple fixed by a copy permutation is constant on each cycle. A cycle of
   length `l` therefore contributes weight `l*a`; adding one slack variable
   accounts for the cumulative inequality. This gives the fixed-point series.
5. In Stapledon's normalization the determinant includes the fixed
   homogenizing direction. A copy cycle of length `l` gives `N` coordinate
   cycles, hence `(1-t) product_l (1-t^l)^N`; it cancels the denominator and
   leaves `product_l h(t^l)`.
6. For a natural labeling, the ordinary numerator is the descent enumerator
   of linear extensions. Place permutation on `L(P)^k`, graded by total
   descents, has exactly the cycle-product fixed-set enumerator. Thus every
   coefficient is a genuine permutation character; no equivariance of the
   transfer map is assumed.
7. For graded `P`, the base numerator is palindromic of degree
   `d=N-r-1`, and an ordinal `k`-power has center degree `kd`. These are the
   classical graded-poset facts needed to define the common gamma expansion.
8. In a palindromic polynomial, distinct gamma-basis terms have distinct
   orders of vanishing at `t=-1`. Hence the root order determines the last
   nonzero gamma index without possible cancellation.
9. At the identity the root order is `ks`; at a transposition it is
   `(k-2)s`, since `h(t^2)` evaluates to `h(1)>0` at `t=-1`. At the resulting
   index the character has dimension zero and nonzero transposition value.
   Restriction to `C2` gives multiplicities `c/2` and `-c/2`; integrality
   follows because integer `h` with `h(-1)=0` has even `h(1)`.
10. For `P` equal to `n` disjoint `a`-chains, comparability in its ordinal
    square is exactly `K_(n,n)[K_a]`, and its linear extensions are multiset
    shuffles counted by `(na)!/(a!)^n`. With even `n` and odd `a`, the degree
    `a(n-1)` is odd, giving the stated top coefficient.

I checked premises 1--5 directly against the defining fixed-lattice-point
series in small cases, premise 6 both logically and by enumerating graded
tuples, premises 8--9 by independent gamma decomposition, and premise 10 by
explicit linear-extension enumeration for the smallest three family members.
For premises 1, 6, and 7 I also checked the cited primary literature: Stanley's
*Two poset polytopes*, Stapledon's *Equivariant Ehrhart theory*, and
D'Ali--Higashitani's graded-poset theorem. Their scopes match the uses here.

## Completeness reductions and adversarial cases

- Cycle decomposition is exhaustive for every element of `S_k`; no conjugacy
  type is omitted by the product formula.
- A single transposition exists for every `k>=2`, so restriction to its `C2`
  subgroup proves failure for the entire action. No assertion about other
  conjugacy classes is needed.
- Exact root multiplicity, rather than merely `h(-1)=0`, covers multiple
  roots. The checker challenges the argument with the formal input
  `(1+t)^2` through `k=6`.
- `k=1`, a one-element poset, and a two-element chain test the empty-cycle,
  degree-zero, and no-root boundaries. The obstruction is correctly absent.
- The two-element antichain gives the smallest advertised obstruction:
  `C4`, with `Gamma_1=sign-trivial`.
- The three-element antichain has no root at `-1` but still has a negative
  gamma multiplicity. This confirms that the theorem is sufficient, not a
  converse.
- The five-element antichain is a root-free positive `C2` control. It prevents
  the previous negative example from being silently promoted to a root-free
  classification.
- `k=3` tests permutations containing both a 2-cycle and a fixed copy, as
  well as a 3-cycle. The V-poset tests a nontrivial branching relation.
- The graph identification is checked at `a=1` (no internal clique edges),
  `n=2,a=3` (nontrivial blocks), and `n=4,a=1` (more than two blocks per side).

These reductions cover every logical branch of the claimed theorem. The
finite cases only challenge the reductions; the universal quantifiers are
discharged by the audited arguments above.

## Independent computation

[`review.py`](review.py) imports no target code. It reconstructs ordinary
numerators from Ehrhart counts. For seven small ordinal powers it enumerates
all lattice vectors against **all** chain inequalities, constructs the actual
homogenized permutation matrix, and computes `det(I-tA)` by the Leibniz
formula. This differs from the target's shell convolution and cycle-factor
determinant. It then compares the resulting numerator with both the claimed
cycle product and a separate fixed-tuple enumeration of linear extensions.

It also decomposes the relevant polynomials in the gamma basis, computes the
two `C2` irreducible multiplicities, tests simple and repeated roots through
`k=6`, and checks both root-free controls. All arithmetic is exact and uses
only the Python standard library.

Run with CPython 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 review.py
PYTHONDONTWRITEBYTECODE=1 python3 -O review.py
sha256sum -c SHA256SUMS
```

The script compares its output to [`EXPECTED.json`](EXPECTED.json) and fails
on any discrepancy. Python's integer/container semantics and SHA-256 are the
only computational trust assumptions.

## Caveats

This is not a formal proof-assistant verification. The novelty statement in
the target remains search-relative. The review accepts exactly the scoped
negative result: it neither claims a classification when `h(-1) != 0` nor
extends the action to order polytopes or arbitrary graph automorphisms.

## Primary references

- R. P. Stanley, [Two poset polytopes](https://math.mit.edu/~rstan/pubs/pubfiles/66.pdf),
  *Discrete & Computational Geometry* 1 (1986), 9--23.
- A. Stapledon, [Equivariant Ehrhart theory](https://arxiv.org/abs/1003.5875).
- A. D'Ali and A. Higashitani,
  [Order polytopes of graded posets are gamma-effective](https://arxiv.org/abs/2505.07623).
