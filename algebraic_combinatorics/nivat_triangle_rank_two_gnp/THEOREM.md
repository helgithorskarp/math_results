# Periodic-mask rigidity and the rank-two Farey-triangle stratum

All configurations below are indexed by `Z^2`.  A binary configuration is
viewed either over `F_2` or, after replacing its symbols by `0,1`, over the
integers.  Laurent polynomials act by finite linear combinations of shifts.

## 1. Period-lattice norm lemma

**Lemma.**  Let `a:Z^2 -> Z` have a nonzero integer Laurent-polynomial
annihilator, and let `q:Z^2 -> Z` satisfy

```text
q(z+(m,0))=q(z)=q(z+(0,n))
```

for positive integers `m,n`.  Then the pointwise product `qa` also has a
nonzero integer Laurent-polynomial annihilator.

**Proof.**  Choose nonzero

```text
p in Z[X^+-1,Y^+-1],       p a=0.
```

Over the complex numbers form the orbit norm

```text
N_(m,n)(p)=product_(zeta^m=1, eta^n=1) p(zeta X,eta Y).       (1)
```

The Laurent ring is a domain, so this product is nonzero.  Galois
automorphisms permute its factors.  Its coefficients are therefore rational
algebraic integers and hence integers.  Substitution `X -> zeta_0 X`, for any
`m`th root `zeta_0`, permutes the factors in (1); the analogous statement
holds for `Y`.  Consequently

```text
N_(m,n)(p) in Z[X^(+-m),Y^(+-n)].                            (2)
```

(Here the notation means that every `X` exponent is divisible by `m` and
every `Y` exponent by `n`.)  The factor with `zeta=eta=1` is `p`, so (1)
annihilates `a`.  By (2), every shift appearing in the norm is a period of
`q`.  Coefficient by coefficient,

```text
N_(m,n)(p)(qa)(z)=q(z) N_(m,n)(p)a(z)=0.                    (3)
```

Thus the same nonzero integer polynomial annihilates `qa`.  This proves the
lemma.  A Laurent monomial shift reduces the argument to ordinary
polynomials if desired.  QED

## 2. XOR by a doubly periodic mask preserves integral annihilation

**Corollary.**  Let `c,q` be binary configurations, with `q` doubly periodic.
If the integer lift of `c` has a nonzero annihilator, then so does the integer
lift of

```text
s=c XOR q.
```

**Proof.**  Choose coordinate periods `m,n` for `q` and let `N` be the norm
from the lemma applied to an integer annihilator of `c`.  The lemma says that
`N` annihilates both `c` and the pointwise product `cq`.  In the integer lift,

```text
s=c+q-2cq.                                                   (4)
```

The polynomial `X^m-1` annihilates `q`, so the nonzero product
`(X^m-1)N` annihilates all three terms in (4).  QED

## 3. Periodic masks preserve four-dot rigidity

Let `u,v` be a unimodular pair in `Z^2`, and let `S_(u,v)` be the binary
four-dot system

```text
ker((1+X^u)(1+X^v)).
```

**Theorem.**  If `s` belongs to `S_(u,v)`, `q` is any doubly periodic binary
configuration, and

```text
c=s XOR q,
```

then low complexity of `c` with respect to any finite nonempty window forces
`c` to be periodic.  Equivalently, every affine periodic translate of a
unimodular binary four-dot system has the generalized Nivat property.

**Proof.**  Suppose `P_c(D)<=|D|`.  The standard low-complexity annihilator
lemma gives the `0,1` integer lift of `c` a nonzero integer annihilator.  By
the preceding corollary the integer lift of `s=c XOR q` has a nonzero integer
annihilator.

A unimodular change of coordinates takes `u,v` to the standard basis and
preserves finite-window pattern counts, nonzero periods, and existence of an
integer annihilator.  The strong form of Kari--Moutot's four-dot theorem says
that a member of `ker((1+X)(1+Y))` whose integer lift has a nonzero
annihilator is periodic.  Hence `s` has a nonzero period `w`.

The period lattice of `q` has finite index.  Some positive multiple `kw`
belongs to it.  Both `s` and `q`, and therefore their XOR `c`, have period
`kw`.  QED

Notice that the mask is allowed to depend on the configuration; no bound on
its periods is used.

## 4. Rank-two Farey-triangle GNP theorem

Put

```text
F=(1+X)(1+Y)(1+XY) over F_2.
```

The preceding Farey-triangle decomposition and directional-rank theorem give
every `c in ker(F)` a representation

```text
c(i,j)=A(j)+B(i)+C(j-i) mod 2,                              (5)
```

and define `rho(c)` as the representation-independent number of nonperiodic
sequences among `A,B,C`.

**Corollary (complete rank-two stratum).**  If `rho(c)=2`, then for every
finite nonempty `D subset Z^2`,

```text
P_c(D)>|D|.                                                  (6)
```

Thus every member of the Farey-triangle kernel with `rho(c)<=2` satisfies the
generalized Nivat conclusion.  Any counterexample for the triangle kernel
must have `rho(c)=3`; equivalently, every nonzero binary annihilator of that
counterexample is divisible by the whole squarefree polynomial `F`.

**Proof.**  In a rank-two representation exactly one of `A,B,C` is periodic.
Its associated directional layer in (5) is doubly periodic: it already has
the direction of its layer as one period, and the one-dimensional sequence
period supplies an independent period.  The sum of the other two layers is a
four-dot configuration in their two directions.  Any two directions among
the Farey triple are unimodular.  The theorem therefore says that low
complexity would make `c` periodic.  The directional-rank theorem says that
rank two is nonperiodic, a contradiction.  This proves (6).  The `rho<=1`
case is already periodic, and the annihilator-gcd equivalence is the earlier
directional-rank formula.  QED

## Scope and trust boundary

This closes the whole rank-two stratum, for arbitrary periods and arbitrary
finite windows.  It does **not** decide the rank-three stratum or the full
generalized Nivat property of `ker(F)`, and it does not address the original
rectangular Nivat conjecture.

The proof imports two published facts: low complexity gives a nonzero
integer annihilator, and the integer-annihilator form of the binary four-dot
theorem.  The orbit-norm lemma and its application to rank two are proved
above.  `verify.py` exactly audits small orbit norms, their factorization and
period-sublattice support, the multiplier identity, and 32,768 finite cyclic
instances of (5).  Finite computations are checks of the formulas, not a
substitute for the universal proof.
