# Independent review of the prime-index Ehrhart Fourier criterion

## Verdict and scope

This reviews Discovery Net contribution
`bafkreieuflfk6x3peldqsg4jskam4j52ljlix77nuosghi5pfgt3m3ojiq`,
"Prime-index local Fourier criterion for Ehrhart period," and source commit
`dd41023a90070414dc2bf8aeed96fc18fe2da2ed`.

**Verdict: accept with high confidence, within the exact stated
hypotheses.**  The normalized-character formula, its three sufficient
noncancellation criteria, and the binary specialization are correct.  I found
no missing active face, quotient-lattice error, Fourier-sign reversal, or
unjustified positivity claim.

The theorem is sufficient, not a classification of all prime-denominator
polytopes.  It neither proves universal odd-prime noncollapse nor asserts
that the displayed character-level cancellations are geometrically
realizable.

## Human premises and completeness reductions

The verdict depends on the following bridges.  They were audited directly;
finite agreement was not used to supply a universal step.

1. **Fixed facet data and period bound.**  The rows are fixed integral
   equations of actual facets and may be nonprimitive.  If `pP` is a lattice
   polytope, every face has affine denominator dividing `p`.  Berline--Vergne
   therefore makes every local Ehrhart coefficient `p`-periodic.  A face
   whose affine span meets the ambient lattice has a constant local
   coefficient.
2. **Index-`p` character.**  For a rank-`g` active map with image
   `Lambda` of index `p`, reduction modulo `p` has codimension one.  Thus
   `Lambda` is exactly the kernel of a nonzero
   `epsilon in F_p^g`, unique up to scalar.  Since `aff(F)` misses the
   lattice, `b_F` is outside `Lambda`; hence `c=epsilon b_F` is nonzero.
3. **The face-subset bridge is complete.**  A codimension-`g` face in
   exactly `g` facets has independent active normals.  From a
   relative-interior point, every subset of those facets cuts a nonempty face
   of the expected codimension.  If `epsilon` had proper support `I`, the
   subsystem on `I` would have no integral solution and would produce a bad
   face of smaller codimension.  Minimality therefore forces full support.
4. **All proper active projections are covered.**  The kernel of a
   full-support character projects surjectively onto any proper set of
   coordinates: choose one omitted coordinate to solve the single congruence.
   Consequently every proper active subsystem has an integral affine
   solution.  This covers every positive-dimensional face of the local
   simplicial cone, including the full cone (the empty subsystem).
5. **Correct quotient lattice.**  With `W=ker A_F`, the quotient lattice is
   the image of `Z^d` in `V=R^d/W`.  The induced isomorphism `C:V->R^g`
   sends that lattice exactly to `Lambda`; no coordinate lattice is silently
   substituted.  Integer slacks in the cone at `nF` are therefore precisely
   the nonnegative vectors satisfying
   `epsilon u=n c (mod p)`.
6. **Character-filter normalization and sign.**  The finite filter gives

       e^(-n<v,xi>) S(K_n)(xi)
        =(1/p) sum_a zeta^(-a n c)
          product_j(1-zeta^(a epsilon_j)e^(-ell_j(xi)))^(-1).

   Full support makes every `a!=0` term analytic at zero.  With the review's
   Fourier convention, multiplication by `zeta^(hn)` selects
   `a=h c^(-1)`, not its negative, and retains the factor `1/p`.
7. **Only the vertex can vary in a nonzero mode.**  For a positive-dimensional
   cone face indexed by a proper row set `I`, item 4 gives a lattice point
   `z_I` with the selected coordinates equal to `b_I`.  The fractional vertex
   differs from `z_I` by the face direction.  In the quotient by that
   direction, dilation is therefore an integral lattice translation.
   Berline--Vergne translation invariance makes its transverse `mu` term
   independent of `n`; after removing the vertex exponential, the face
   integral is also independent.  The cone identity then leaves exactly the
   analytic vertex product in every nonzero Fourier mode.
8. **Global assembly has no hidden lower-degree mixing.**  For lattice-point
   counting, a dimension-`j` face contributes
   `mu(t(nP,nF))(0) vol(F)n^j`.  Hence degrees above `k=d-g` are constant by
   minimality, and the only varying degree-`k` terms are the faces in
   `M`.  Summing their vertex modes gives the claimed formula.  A surviving
   mode makes one coefficient function nonconstant; because the total period
   divides the prime `p`, the exact quasiperiod is `p`.
9. **The corollaries use valid noncancellation.**  A single face and a common
   profile factor out a nonzero cyclotomic value.  For `g=1`, every summand
   has real part `1/2` before its positive volume weight is applied.  At
   `p=2`, every normalized entry is one and the formula becomes exactly
   `2^(-g-1) sum_F vol(F)`.

The current arXiv source of Berline--Vergne was checked at Theorems 19(d),
20(a,e), and Corollary 30(a,b).  These give precisely the cone identity,
lattice-translation invariance, local Euler--Maclaurin assembly, and
affine-denominator period bound imported above.

## Independent reproduction and adversarial tests

The target manifest passes.  Normal and optimized CPython runs reproduce all
48 target simplex-product cases, 156 cyclotomic modes, 5,592 active-image
memberships, and the stated `p=3,g=3` cancellation.

The independent checker in this directory imports no target code, output, or
fixture.  It never solves a cyclotomic linear system.  Instead it uses the
finite identity

    (1-zeta^a)^(-1)=-(1/p) sum_(r=1)^(p-1) r zeta^(ar),

and verifies it directly.  It then exhausts 10,748 normalized local Fourier
selections for primes through seven and codimensions through four.

The geometric controls are four shifted slack-box parallelograms.  In
coordinates

    (u,v)=(x,x+p y),

they impose `0<=u<=a` and `l<=v<=l+b`.  Lattice points correspond exactly to
integer slack pairs with `v=u (mod p)`.  The chosen fixtures at
`p=3,5,7,11` have four fractional vertices, integral-affine edges, active
index `p`, and several different normalized profiles.  Direct definition-
level counts, quadratic interpolation with unused values, and exact
cyclotomic transforms verify all 22 nonzero modes.  Thus the audit exercises
four simultaneous minimal bad faces rather than the target's unique-face
simplex products.

In total the checker performs 23 reciprocal identities, 10,748 local-mode
checks, 26 independently interpolated residue polynomials with 26 holdouts,
and five diagonal-profile identities.  Normal and optimized runs are
byte-identical.  Record digest:
`bd06e8021b60639843bf9422cc82164cc2d4294d79f748d12f58842c8915c1ab`.
All checks use explicit failures and remain active under `python -O`.

## Strengthening and improvement opportunities

### Proved refinement: cancellation already occurs in codimension two

The target's `p=3,g=3` example correctly disproves unrestricted odd-prime
positivity.  A smaller-codimension obstruction occurs at `p=5`.

For a primitive `p`th root `zeta`, put

    f(x)=(x^p-1)/(x-1)=product_(a=1)^(p-1)(x-zeta^a).

Twice differentiating its logarithm at `x=1` gives

    sum_(a=1)^(p-1) (1-zeta^a)^(-2)
      =(f'(1)/f(1))^2-f''(1)/f(1)
      =(p-1)(5-p)/12.

It follows that at `p=5,g=2`, equal positive weights on the four profiles

    (1,1), (2,2), (3,3), (4,4)

cancel in every nonzero Fourier mode: multiplication by `h` merely permutes
the four summands.  The checker verifies the general identity at
`p=2,3,5,7,11` and the exact zero at five.

This strengthens the target's obstruction analysis: no universal positivity
theorem is available even in codimension two.  As with the target's example,
this is a character-level cancellation, not a claim that a polytope realizes
those four profiles with equal normalized volumes.

### Highest-value next step

The remaining structural question is geometric realizability.  A useful
theorem should combine adjacent-facet compatibility, normal-fan balancing,
and normalized face volumes to decide which weighted profile multisets can
occur.  Merely classifying positive dependencies among arbitrary cyclotomic
profiles would ignore these geometric constraints.

For presentation, the source should add the codimension-two identity above
and cite the exact Berline--Vergne theorem numbers in the proof rather than
only in the bibliography.  Reader links should preferably use the stable
`main` branch while retaining the verified commit separately as provenance.

## Literature, novelty, and publication readiness

Berline--Vergne supplies the analytic machinery, while
Beck--Sam--Woods proves maximal expected period for the second-leading
coefficient.  McAllister--Woods and later work establish that Ehrhart period
collapse is real and flexible.  Targeted primary-source searches found local
Euler--Maclaurin coefficient formulas, Fourier--Dedekind methods, and general
period results, but no matching normalized active-character theorem.

The result is therefore graph-new and appears literature-new within a bounded
search; this is not a historical-priority certificate.  With the explicit
analytic trust boundary and sufficient-not-classifying scope preserved, the
theorem is ready as a compact research note.

Primary sources:

- <https://arxiv.org/abs/math/0507256>
- <https://arxiv.org/abs/math/0702242>
- <https://arxiv.org/abs/math/0310255>
- <https://arxiv.org/abs/math/0204035>
