# Sharp symbolic-power bands for residual cycle arrangements

Work over the complex numbers. Let `L_1,...,L_n` be distinct projective
lines in `P^2`, with no three concurrent. Let `H` be a simple 2-regular
graph on their labels, with `c` cycle components, each of length at least
three. Set

    Z = {L_i intersection L_j : i<j, ij not in E(H)},
    I = I(Z) in S = C[x,y,z],       F = product_i ell_i,
    d = n-3,                      h = n-6.

Here `ell_i` defines `L_i`; choices of its nonzero scalar do not affect
the statements. There are `N=n(n-3)/2` distinct points in `Z`, exactly
`d` on each line. Define the symbolic power explicitly by

    I^(m) = intersection_(p in Z) I(p)^m,       I^(0)=S.

Thus it consists of homogeneous forms vanishing to order at least `m`
at every point of `Z`. Write `J_D` for the degree-`D` vector space of a
homogeneous ideal, with negative-degree spaces zero, and `alpha(J)` for
its first nonzero degree. Ordinary and symbolic powers are different.

## Theorem

Suppose `n>=7`. For every `k>=0`,

    alpha(I^(2k))   = kn,
    alpha(I^(2k+1)) = kn+n-3.

For every integer `r` with `0<=r<n-6`, the following are equalities of
vector spaces, not just equalities of dimensions:

    (I^(2k))_(kn+r)       = F^k S_r,                         (1)
    (I^(2k+1))_(kn+n-3+r) = F^k I_(n-3+r).                   (2)

The relevant dimensions are

    dim (I^(2k))_(kn+r) = binom(r+2,2),
    dim (I^(2k+1))_(kn+n-3) = c,
    dim (I^(2k+1))_(kn+n-3+r)
        = binom(n-1+r,2) - n(n-3)/2       if 1<=r<n-6.

There is an explicit basis for `I_(n-3)`. For each cycle `C` of length
`s`, let `A_C` be its degree-`s-3` adjoint: the unique form, up to scalar,
vanishing at intersections of nonconsecutive lines within `C`. Then

    B_C = A_C product_(i not in C) ell_i

as `C` runs over the components of `H` is a basis. In particular, when
`H=C_n`, the minimum-degree forms are precisely scalar multiples of
`F^k` at even multiplicity and of `F^k A_H` at odd multiplicity.

The band width `h=n-6` is exact. For every `k>=1`, both (1) and (2)
fail at `r=h`. The hypothesis `n>=7` for the stated bottom-space
rigidity cannot be replaced by `n>=6`.

Consequently the Waldschmidt constant is

    alpha_hat(I) = lim_(m->infinity) alpha(I^(m))/m = n/2.

This is a theorem about special incidence configurations. It does not
prove Nagata's conjecture for very general points, nor describe the full
symbolic Rees algebra or the full Hilbert function of every symbolic power.

## 1. The one-cycle adjoint, with its known status made explicit

Let there be `s>=3` lines with a chosen cyclic order and no triple
intersection. Their nonconsecutive intersections number `s(s-3)/2`.
The vector space of forms of degree `s-3` has dimension

    binom(s-1,2) = s(s-3)/2 + 1.

Point vanishing imposes at most one linear equation per point, so a
nonzero adjoint exists. This also handles `s=3`, when it is a constant.

On each line, a degree-`s-3` form through the required points restricts
to a scalar multiple of a fixed nonzero section with those `s-3`
distinct simple zeros. If the form contains one of the lines, then its
value at either intersection with a consecutive line is zero. That
point is not among the prescribed zeros on the consecutive line.
The restriction there must therefore be identically zero. Propagation
around the cycle forces every line to be a component, which is
impossible for a nonzero form of degree `s-3`. Hence an adjoint contains
none of these lines and is nonzero at every consecutive intersection.

If `A` and `A'` are two adjoints, their restrictions on one line are
proportional. A suitable linear combination vanishes on that line;
the same propagation makes the combination zero. Thus the space is
one dimensional.

For side lines of a convex polygon this is the classical Wachspress
adjoint. Its uniqueness is not new: see Kohn--Ranestad, Theorem 1 and
Example 3. We include the elementary argument to cover arbitrary cyclic
labelings and to keep the proof independent of convexity.

## 2. The base spaces for disjoint cycles

Every `B_C` above belongs to `I_d`: a selected pair within `C` is a zero
of `A_C`; any other selected pair has a line outside `C`, which is a
factor of `B_C`. The restriction of `B_C` to a line in `C` is nonzero;
its restriction to any other line is zero. These support properties
make the `c` forms independent.

For the converse, restrict a form `f in I_d` to each line. Its `d`
prescribed distinct zeros determine the restriction up to one scalar.
At a missing intersection `ij in E(H)`, neither restriction's prescribed
zero section vanishes. Equality of the two values of `f` links the two
scalars by a nonzero ratio. Thus at most one free scalar is possible
per component of `H`. The restriction map is injective, since a form
vanishing on all `n` lines is divisible by `F` and `d<n`. It follows
that `dim I_d=c` and the displayed forms are a basis.

Any form of degree below `d` through `Z` restricts to zero on every
line: a nonzero section on a projective line of degree less than `d`
cannot have `d` distinct zeros. It would be divisible by `F`, impossible
in that degree. Therefore `alpha(I)=d`.

For `D>=n-2`, the points impose independent conditions. Indeed, for a
selected pair `ij`,

    F/(ell_i ell_j)

has degree `n-2`, is nonzero at `L_i intersection L_j`, and vanishes at
every other point of `Z`. These sections interpolate the point values
diagonally. For higher `D`, multiply by a power of a linear form nonzero
at all the finitely many points. Hence

    dim I_D = binom(D+2,2) - N,       D>=n-2.                (3)

The polygon case at `D=n-2` agrees with the known Kohn--Ranestad
Theorem 7; neither that special value nor adjoint existence is claimed new.

## 3. The elementary incidence recursion

The following statement is useful beyond this particular configuration.
If each of `n` lines contains at least `delta` selected distinct double
points, and no three of the lines are concurrent, then for `m>=2`,

    D < m delta  ==>  (I^(m))_D = F (I^(m-2))_(D-n).        (4)

To prove it, restrict `f` to any one of the lines. If the restriction
is nonzero, its zeros at the selected points have order at least `m`
and thus total degree at least `m delta`, contrary to `D<m delta`.
So every line divides `f`, and their product divides it. At each
selected intersection, `F` has order exactly two. In local coordinates
the two incident linear factors are independent and all other factors
are units. The order of a product is additive, so `f/F` has order at
least `m-2`. The converse inclusion follows by multiplication.

This is just the restriction-to-a-line form of Bezout's theorem. For
polygon residual arrangements at `(m,D)=(2,n)`, rigidity for `n>6`
is already in Kohn--Ranestad's proof of Proposition 5. Our statement
below iterates this known mechanism and locates its sharp stopping degree.

## 4. Iteration and first nonzero degrees

For an even multiplicity `2k` and degree `kn+r`, after removing `j`
copies of `F`, the strict inequality needed for (4) is

    (2k-2j)d - ((k-j)n+r) = (k-j)h-r > 0.

It holds for every `j=0,...,k-1` whenever `0<=r<h`. Removing `k`
copies proves (1). For an odd multiplicity `2k+1` and degree `kn+d+r`,
the same difference is again `(k-j)h-r`; removing `k` copies proves
(2). Formula (3) and the base-space dimension give all the asserted
dimensions.

For completeness these bands also are the first nonzero degrees.
At even multiplicity, any `D<kn` satisfies the strict inequalities in
all `k` steps of (4), leaving a negative degree. At odd multiplicity,
any `D<kn+d` likewise leaves a form in `I` of degree below `d`, which
is zero. Existence at the stated degrees is supplied by `F^k` and
`F^k B_C`. The limit for `alpha_hat(I)` follows directly from the
two initial-degree formulas.

## 5. Exact failure at the next degree

Choose a nonzero normalization of every `B_C`, and set

    A = sum_C B_C.

On each arrangement line only the term for its own cycle survives,
and that restriction is nonzero. Thus `A` contains none of the `n`
lines. It has degree `d` and belongs to `I`.

For `k>=1`, the form `F^(k-1) A^2` has multiplicity at least `2k`
at all points and degree

    (k-1)n+2d = kn+h.

It is not divisible by `F^k`, contradicting (1) if its range were
extended to `r=h`. Similarly `F^(k-1) A^3` has multiplicity at least
`2k+1` and degree `kn+d+h`, and is not divisible by `F^k`. This is
the failure of (2) at the same first excluded offset.

The statement concerns failure of these exact factorization equalities;
it does not assert that no smaller common component survives at that degree.

For `n=6` and one missing six-cycle, `d=3` and both `F` and `A^2`
are degree-six forms with double zeros at `Z`. They are independent
because `A` contains none of the lines. Thus the asserted one-dimensional
even bottom space already fails at `n=6`. For `n=5`, `A^2` even has
degree four, below the extrapolated even minimum of five. No claims
about full symbolic powers at these smaller values are needed.

## Interpretation and trust boundary

The theorem identifies a complete range of low-degree linear systems
at **every** multiplicity and proves that its endpoint is exact. The
odd minimum-space dimension records the number of missing cycles; for
an ordinary polygon it is one. The Waldschmidt value and all-multiplicity
rigidity are consequences of this incidence argument, not extrapolations
from computations.

With `N=n(n-3)/2` and `n>6`, one has `n/2<sqrt(N)`. Such special point
configurations therefore cannot supply a specialization lower bound
equal to Nagata's proposed very-general threshold. Already the line
product gives the upper bound behind this limitation; this observation
is not advertised as a new obstruction to Nagata itself.

The proof uses elementary projective polynomial algebra and ordinary
unformalized reasoning. The accompanying checker verifies actual
finite interpolation spaces and explicit first-failure forms with exact
arithmetic. It neither supplies nor replaces the universal proof.
