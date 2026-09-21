# Prime-index local Fourier formula

All lattices in the ambient space are `Z^d`.  Fix a bounded,
full-dimensional rational polytope with one integral inequality for each
actual facet,

```text
P={x in R^d:A x<=b}.
```

Rows need not be primitive, and the description is fixed.  Suppose `p` is
prime and `pP` is a lattice polytope.  Let `N` be the nonempty faces `F`
for which `aff(F)` does not meet `Z^d`.  When `N` is nonempty, set

```text
g=min_(F in N) codim F,      k=d-g,
M={F in N:codim F=g}.
```

For a face `F` contained in exactly `g` facets, let `A_F` be their
independent `g`-by-`d` normal matrix, let `b_F` be their right-side vector,
and put `Lambda_F=A_F Z^d`.

## 1. The formula and its consequences

**Theorem 1 (prime-index Fourier criterion).**  Assume every `F` in `M`
lies in exactly `g` facets and

```text
[Z^g:Lambda_F]=p.                                      (1)
```

There is a nonzero row `epsilon_F in F_p^g`, unique up to a nonzero
scalar, such that

```text
Lambda_F={u in Z^g:epsilon_F u=0 mod p}.
```

Every coordinate of `epsilon_F` is nonzero, as is
`c_F=epsilon_F b_F`.  Hence

```text
eta_F=c_F^(-1) epsilon_F in (F_p^*)^g                 (2)
```

is well defined independently of the scalar choice.  Permuting the
containing facets only permutes its coordinates.

Write

```text
L_P(n)=sum_(j=0)^d q_j(n) n^j,
```

where each `q_j` is represented as a function on `Z/pZ`.  With
`zeta=exp(2 pi i/p)` and

```text
qhat_j(h)=(1/p) sum_(r=0)^(p-1) q_j(r) zeta^(h r),     (3)
```

one has, for every `h=1,...,p-1`,

```text
qhat_k(h)=(1/p) sum_(F in M) vol_k(F)
                 product_(j=1)^g
                    (1-zeta^(h eta_(F,j)))^(-1).       (4)
```

Here face volume is normalized by the direction lattice
`lin(F-F) intersect Z^d`, with point volume one.

If the right side of (4) is nonzero for at least one `h`, the minimal
Ehrhart quasiperiod of `P` is exactly `p`.

**Corollary 2 (three noncancellation classes).**  The right side of (4)
is nonzero, and `P` has exact Ehrhart quasiperiod `p`, under any one of:

1. `M` contains exactly one face;
2. the coordinate multisets of all `eta_F` are equal;
3. `g=1`.

In case 2 every nonzero Fourier mode is a positive volume sum times one
nonzero cyclotomic factor.  For case 3, each summand in (4) has positive
real part because

```text
Re (1-zeta^a)^(-1)=1/2       for a not equal to 0 mod p. (5)
```

The codimension-one conclusion is consistent with the known maximal-period
theorem for the second Ehrhart coefficient; it is not asserted as a new
result here.

At `p=2`, every normalized character equals `(1,...,1)`, and (4) says

```text
qhat_k(1)=2^(-g-1) sum_(F in M) vol_k(F),               (6)
```

exactly the leading alternating coefficient of the index-two theorem.

## 2. Minimality forces a full-support character

An index-`p` subgroup of `Z^g` is the kernel of a surjection to `Z/pZ`,
so (1) gives `epsilon_F`, uniquely up to scalar.  Since `aff(F)` misses
the lattice, `b_F` is not in `Lambda_F`, proving `c_F` is nonzero.

We use the following elementary face fact.  If a codimension-`q` face is
contained in exactly `q` facets, each subset `I` of those facets defines
the affine span of a nonempty face of codimension `|I|`.  Indeed, at a
relative-interior point of the original face, linear independence of the
active normals supplies a perturbation that keeps precisely the selected
equalities while all inactive inequalities remain slack.

If the support `I` of `epsilon_F` were proper, the subsystem

```text
(A_F)_I x=(b_F)_I
```

would have no integral solution: membership of `(b_F)_I` in the projected
image would force `epsilon_F b_F=0`.  The face fact would then exhibit a
nonintegral-affine face of codimension `|I|<g`, contradicting minimality.
Thus every character coordinate is nonzero.  Equivalently, the projection
of `Lambda_F` onto any proper set of coordinates is the full coordinate
lattice.  Every proper active subsystem therefore has an integral affine
solution.

## 3. The local character filter

Fix `F in M`.  Put `W=ker A_F`, `V=R^d/W`, and let `L` be the image of
`Z^d` in `V`.  The induced isomorphism

```text
C:V -> R^g,       C(pi(x))=A_F x
```

sends `L` bijectively to `Lambda_F`.  If `v=C^(-1)b_F`, the transverse
supporting cone at `nF` is

```text
K_n={y in V:C y<=n b_F}=n v+K_0.
```

For dual variables `xi`, write
`ell_j(xi)=<xi,C^(-1)e_j>`.  Integer slacks `u=n b_F-Cy` give a bijection

```text
K_n intersect L  <->
{u in Z_{≥0}^g:epsilon_F u=n c_F mod p}.
```

The finite character filter therefore gives, first in a convergence
chamber and then meromorphically,

```text
exp(-n<v,xi>) S(K_n)(xi)
 = (1/p) sum_(a=0)^(p-1) zeta^(-a n c_F)
       product_(j=1)^g
          (1-zeta^(a epsilon_(F,j)) exp(-ell_j(xi)))^(-1).  (7)
```

Every term with `a` nonzero is analytic at `xi=0`, because the character
has full support.

We now import the Berline--Vergne local cone identity.  Apply it to `K_n`
and remove the vertex exponential as on the left of (7).  A
positive-dimensional face is specified by equality on a proper subset
`I` of the active rows.  The preceding section supplies `z_I in L` with
`(Cz_I)_I=(b_F)_I`; hence `v-z_I` lies in the direction space of that face.
After quotienting by the face directions, dilation by `v` is an integral
translation.  Translation invariance makes its transverse `mu`-function
independent of `n`, and the correspondingly normalized face integral is
also independent of `n`.

Thus every nonzero Fourier mode in `n` on the left of (7) belongs entirely
to the vertex `mu`-term.  Evaluating the analytic modes at zero yields

```text
muhat_F(h)
 = (1/p) product_(j=1)^g
      (1-zeta^(h c_F^(-1) epsilon_(F,j)))^(-1),          (8)
```

where the normalization in (3) selects `a=h c_F^(-1)`.  This selection is
also a direct check on both the sign and the factor `1/p`.

## 4. Global assembly

Berline--Vergne's local Euler--Maclaurin formula is

```text
L_P(n)=sum_(F nonempty face)
         mu(t(nP,nF))(0) vol(F) n^dim(F).                (9)
```

The local coefficient for a face is periodic with period dividing the
least positive integer whose dilated affine span meets the lattice.  Since
`pP` is a lattice polytope, all coefficient periods divide `p`.  A face
whose affine span already meets the lattice has a constant local
coefficient.  Therefore all coefficients above degree `k` are constant,
and the only varying terms at degree `k` come from `M`.  Summing (8) with
the volume weights in (9) proves (4).

If one nonzero mode survives, `q_k` is nonconstant.  A function whose
period divides a prime has minimal period either one or `p`; hence the
coefficient, and therefore the full Ehrhart quasipolynomial, has exact
period `p`.  This proves Theorem 1 and Corollary 2.

## 5. Why odd-prime positivity is not automatic

For a normalized profile `eta`, put

```text
Q_h(eta)=product_j (1-zeta^(h eta_j))^(-1).
```

Using `1-zeta^(-a)=-zeta^(-a)(1-zeta^a)` gives

```text
Q_h(-eta)=(-1)^g zeta^(h sum_j eta_j) Q_h(eta).          (10)
```

For `p=3`, `g=3`, the profiles `(1,1,1)` and `(2,2,2)=-(1,1,1)`
satisfy `sum eta_j=0`.  Equal positive weights therefore cancel in both
nonzero modes.  This demonstrates that the binary positivity argument
does not extend to arbitrary collections of odd-prime characters.

Equation (10) is only an obstruction at the level of the exact local
formula.  We do not assert that a polytope realizes these two profiles
with equal normalized volumes, nor that it yields an Ehrhart period drop.
A geometric realizability or noncancellation theorem remains open in this
note.

## 6. A direct test family

For any prime `p` and `g>=1`, let

```text
S_(p,g)={x in R_{≥0}^g:x_1+...+x_(g-1)+p x_g<=1}.
```

Its only nonintegral-affine face is `e_g/p`.  The `g` active rows there
have image index `p` and normalized character `(1,...,1)`.  For `f>=0`,
the product

```text
P_(p,g,f)=S_(p,g) x [0,1]^f
```

has a unique minimal nonintegral face `{e_g/p} x [0,1]^f`, of dimension
`f`, codimension `g`, and normalized volume one.  Direct counting gives

```text
L_(P_(p,g,f))(n)
 =(n+1)^f sum_(y=0)^floor(n/p)
                 binom(n-py+g-1,g-1).                   (11)
```

Formula (4) predicts

```text
qhat_f(h)=1/[p(1-zeta^h)^g].                            (12)
```

The verifier obtains `q_f(r)` by exact residuewise interpolation of (11)
and compares its cyclotomic transform with (12).  This is a normalization
test, not a finite proof of Theorem 1.
