# Independent review of positive-inertia descent at cardinality `2p+1`

## Verdict

**ACCEPT, high confidence within the stated imported-results boundary.**  The
target theorem is correct: if `p>=5` is prime, `gcd(n,p)=1`, and
`(A,Lambda)` is a spectral pair in `Z/(np)Z` of size `2p+1`, then at least
one member has `p`-descent.  Both first projections are injective and form a
spectral pair in `Z/nZ`.  The tiling lift and the claimed nonexistence of a
23-point spectral subset of `Z/2310Z` follow.

The positive-inertia argument is a genuine universal proof.  The supplied
finite checker corroborates profile arithmetic but is not being used to
infer the theorem.  This review independently rederives the Fourier,
profile, inertia, block-Gram, projection, and tiling steps and gives a
separate exact boundary checker.

Reviewed Discovery Net contribution:
`bafkreigzzf4uqbzpgekuzzawvi5oa4dri2vx35uq2gizyayccdaoc7oy6a`.

Reviewed source:

https://github.com/helgithorskarp/math_results/tree/main/finite_fuglede_2p1_inertia_descent

Verified target source commit:
`0fd2e09c137f5f82783410f34b1143a4d0fd21e7`.

## Human premises and completeness reductions

The verdict depends on the following explicit premises.

1. Spectral-pair symmetry and the standard Fourier-zero/cyclotomic-mask
   equivalence hold in finite cyclic groups.
2. Somlai's levelwise cuboid rule applies for every `d|n`, without a
   square-free assumption on `n`.  If `Phi_(dp)|m_E` but `Phi_d` does not
   divide `m_E`, one `d`-cuboid has a common nonzero integer evaluation on
   every `p`-level.  Therefore every level is nonempty.
3. For `d=ord_n(x)` and `gcd(d,p)=1`,
   `[Q(zeta_d,zeta_p):Q(zeta_d)]=p-1`.  Thus a degree-at-most-`p-1`
   coefficient polynomial vanishing at a primitive `p`th root is a scalar
   multiple of `Phi_p`; all level Fourier sums are equal.
4. A collision in either first projection has order `p` and forces `Phi_p`
   into the opposite mask.  Since `p` does not divide `2p+1`, both
   projections are injective.  This also makes every cross-level first
   coordinate difference nonzero.
5. The singleton-gap Gram argument is applicable after two-sided descent
   failure because the opposite member has all `p` levels nonempty.  Its
   matrix `(r-1)I_p+J_p` has rank `p`, excluding every level size
   `2<=r<=p-1` beside a singleton.
6. The previously unreviewed simultaneous one-fat-level obstruction is
   valid.  Its forced block matrix has exact inertia `(k-1,1,0)` for
   `k=r+p-1`, so it cannot be a Gram matrix.  This review rederives that
   matrix and its negative direction rather than treating the graph result
   as an opaque premise.
7. Somlai's projection lemma is used only after injectivity and descent are
   established.  If descent belongs to `Lambda`, applying the lemma to the
   swapped pair and then using spectral-pair symmetry gives the same
   projected pair claim.
8. The specialization imports the published theorem that Fuglede's
   conjecture holds for cyclic groups of order four distinct primes.  Since
   `210=2*3*5*7`, a 23-point projected spectral set would tile `Z/210Z`,
   impossible because a tile cardinality divides 210.

The proof's case reduction is complete:

1. If either member descends, the main conclusion is reached.  Only
   simultaneous descent failure remains.
2. Simultaneous failure makes all `p` levels of both members positive.
3. A positive `p`-part profile summing to `2p+1` either has a singleton or
   does not.  The singleton gap leaves only
   `S=(p+2,1^(p-1))`; no singleton leaves only
   `D=(3,2^(p-1))`.
4. If either member has profile `D`, subtracting its three-point and
   two-point level Gram matrices yields a block for every opposite level.
   Each block has positive trace, so the difference has at least `p`
   positive eigenvalues.  It is `V-W` with `V,W` positive semidefinite and
   `rank(V)<=3`, so it has at most three.  This excludes `D` for `p>3`.
5. The sole remaining case is `S/S`, excluded by the block-Gram
   obstruction.  No profile or mixed case remains for `p>=5`.

Agreement among programs is therefore supplemental: the universal coverage
comes from the five mathematical reductions above.

## Adversarial smallest and boundary examples

- At `p=3`, the counting reduction has three survivors:
  `(5,1,1)`, `(3,3,1)`, and `(3,2,2)`.  The new inertia inequality can
  saturate `p<=3`.  This confirms that the proof does not silently establish
  the explicitly excluded `p=3` case.
- At the first claimed prime `p=5`, the profile census leaves exactly
  `(7,1,1,1,1)` and `(3,2,2,2,2)`.  The dense-profile step gives five
  positive directions against rank at most three, while the one-fat block
  matrix has one exact negative direction.
- At `(n,p)=(3,5)`, all 1,365 eleven-subsets of `Z/15Z` collide under first
  projection.  Such a spectral pair would force `Phi_5` into an 11-point
  opposite mask, contradicting `Phi_5(1)=5`.  This tests the capacity edge
  where injectivity alone rules out the pair.
- At `(n,p)=(11,5)`, the checker constructs an 11-point graph over all of
  `Z/11Z`, verifies spectrum `Z/11Z x {0}`, and checks its lifted tiling of
  `Z/55Z`.  Thus the first nonvacuous capacity boundary is not accidentally
  excluded.
- The exact degree identity `phi(dp)=phi(d)(p-1)` is tested in 500 coprime
  cases, including nonsquarefree `d`; the argument does not require
  squarefree `n`.
- The graph-lift tiling formula is checked for every function on two small
  downstairs tilings (150 graph lifts total), including nonconstant lifts.

## Independent linear-algebra audit

For the dense profile, set `M=V-W`, where `V` and `W` are the Gram matrices
of phase vectors from a three-point and two-point level.  Cross-level
Fourier equality makes `M` block diagonal across the `p` levels of the
opposite member.  Every diagonal entry is one.  Hence every nonempty block
has positive trace and at least one positive eigenvalue, so `n_+(M)>=p`.

For positive semidefinite `V,W`, if the positive eigenspace of `V-W` had
dimension greater than `rank(V)`, it would meet `ker(V)` nontrivially.  On
that intersection the quadratic form is `-W<=0`, a contradiction.  Thus
`n_+(V-W)<=rank(V)<=3`.  The independent checker additionally exhausts all
59,049 pairs of integer Gram factors of shapes `3x2` and `2x2` over
`{-1,0,1}` and verifies this inertia bound exactly.

For the one-fat profile, writing `s=p-1` and `k=r+s`, the forced matrix is

```text
G = [ k I_r - s J_r      J_(r,s)     ]
    [ J_(s,r)       (r-1)I_s + J_s   ].
```

The zero-sum top and bottom subspaces have positive eigenvalues `k` and
`r-1`.  On the two-dimensional constant-block subspace the determinant has
sign

```text
-r s (r-1)(s-1) k < 0.
```

Thus `G` has exact inertia `(k-1,1,0)`, a stronger audit than checking only
the target's displayed negative vector.  The independent checker verifies
this for 88 `(p,r)` cases.

## Projection and source audit

The projected-pair conclusion can also be seen directly.  For distinct
projected spectrum points, their full difference has order either `d` or
`dp`.  Orthogonality supplies the corresponding zero of the first mask; in
the latter case descent replaces `Phi_(dp)` by `Phi_d`.  Injectivity turns
the resulting mask zero into orthogonality of the projected sets.  Swapping
the pair handles descent on the other member.

Somlai's primary preprint states the levelwise cube rule as Lemma 2.2, its
cardinality consequence as Corollary 2.2, and the needed projection theorem
as Lemma 3.1:

https://arxiv.org/html/2607.26534

The four-prime base theorem is Theorem 1.4 of:

https://arxiv.org/abs/2011.09578

Focused primary-literature searches found these imported mechanisms but no
matching `2p+1` descent theorem or positive-inertia level obstruction.  This
supports apparent novelty relative to the searched sources, not historical
priority.

## Scope and remaining trust boundary

The result does not cover `p=3` or cardinality `2p`, and does not prove a
23-point theorem for moduli whose downstairs group lacks spectral-to-tiling.
The imported cuboid and projection results and the published four-prime
theorem were checked against their primary statements but not reproved.  The
universal proof is not proof-assistant formalized.

The independent checker uses CPython exact integers and `Fraction`, with no
floating point, randomness, solver, generated certificate, third-party
package, network input, or imported target code.

## Reproduction

Python 3.11 or later and the standard library suffice.

```bash
cd finite_fuglede_2p1_inertia_descent_review1
PYTHONDONTWRITEBYTECODE=1 python3 -I independent_audit.py > /tmp/fuglede-2p1-review.txt
diff -u EXPECTED_OUTPUT.txt /tmp/fuglede-2p1-review.txt
sha256sum -c SHA256SUMS
```
