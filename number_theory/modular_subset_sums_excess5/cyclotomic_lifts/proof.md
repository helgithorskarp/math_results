# Cyclotomic lifts and the obstruction to an atoral closure argument

This note concerns the unresolved classification of sum-distinct
`n`-element sets modulo `N=2^n+5`. It proves a complete statement about
the associated integer polynomials, and explains why that statement
does **not** close the modular problem. It does not improve the existing
unrestricted `O(N^3)` bound or extend the finite classification range.

For integers `0<u<v`, put

\[
Q_{u,v}(X)=1+X^u+X^{-u}+X^v+X^{-v},\qquad
P_{u,v}(X)=X^vQ_{u,v}(X).
\]

Call a univariate Laurent polynomial **essentially atoral** when every
zero on the complex unit circle is a root of unity. This is exactly the
one-variable specialization of Dimitrov--Habegger's definition.
"Cyclotomic product" below means a product of cyclotomic polynomials,
not necessarily a single irreducible cyclotomic polynomial.

## 1. Complete classification of the lifted polynomials

**Theorem.** Let `0<u<v` and `gcd(u,v)=1`.

1. Every root-of-unity zero of `P_{u,v}` has order `5`, `6` or `12`.
   Consequently there are at most ten distinct such zeros.
2. If `v>=10`, there are at least
   `2*(v-floor(v/3)-1)` distinct zeros on the unit circle. At least
   `2*(v-floor(v/3)-1)-10` of these are not roots of unity.
3. The following are equivalent:
   - `P_{u,v}` is essentially atoral;
   - `P_{u,v}` is a cyclotomic product;
   - `(u,v)` is one of `(1,2)`, `(1,3)`, `(3,4)`.

For nonprimitive `(u,v)`, divide both coordinates by their gcd. The same
classification holds after this division: substituting `X^g` preserves
the property of having a unit-circle zero of infinite multiplicative
order, and preserves the property of being a cyclotomic product.

**Proof of the order restriction.** The classical weight-five
vanishing-sum classification says that five roots of unity adding to
zero either form a rotated regular pentagon, or split into an opposite
pair and a rotated equilateral triangle. This follows from
Conway--Jones, Theorem 6, retaining the possible cancellation of an
opposite pair. It also gives the `c=-1/2` special case explicitly listed
in Qin Xue, Proposition 2.12. The vanishing-sum classification is an
external premise; it is not inferred from the finite controls here.

Apply it to the multiset

\[
E=\{1,\zeta^u,\zeta^{-u},\zeta^v,\zeta^{-v}\}.
\]

In the pentagon case, the occurrence of `1` makes `E` the five fifth
roots. Both `zeta^u` and `zeta^v` then have order dividing five, so
`gcd(u,v)=1` implies that `zeta` has order five.

Otherwise consider the opposite pair, with labels retained even if
some values coincide. There are three possibilities, up to exchanging
`u,v` and signs.

* If the pair is `1,zeta^u`, then `zeta^u=-1`. The remaining triangle
  gives `-1+zeta^v+zeta^(-v)=0`, so `zeta^v` is a primitive sixth root.
  Thus `zeta` has order six.
* If the pair is `zeta^u,zeta^(-u)`, then `zeta^u` has order four.
  The remaining triangle gives `1+zeta^v+zeta^(-v)=0`, so `zeta^v` has
  order three. Thus `zeta` has order twelve.
* If the pair uses one `u` term and one `v` term, their two conjugate
  terms also cancel. The whole sum would equal `1`, a contradiction.

Here we used `ord(zeta)=lcm(ord(zeta^u),ord(zeta^v))`, a consequence of
coprimality. The possible orders give `phi(5)+phi(6)+phi(12)=10`
distinct torsion zeros.

**Proof of the unit-circle lower bound.** Set

\[
f(\theta)=1+2\cos(u\theta)+2\cos(v\theta).
\]

At the `v` points `theta=2*pi*j/v`, its value is at least one.
At the intervening midpoint `theta=(2*j+1)*pi/v`, it equals
`-1+2*cos(u*(2*j+1)*pi/v)`. Since `gcd(u,v)=1`, the midpoint angles
after multiplication by `u` form a rotated equally spaced `v`-point
grid on the circle. The closed arc on which `cos(theta)>=1/2` has
one third of the circle's length, and contains at most
`floor(v/3)+1` grid points. Therefore at least
`K=v-floor(v/3)-1` midpoints have strictly negative values.

Each negative midpoint lies between two positive endpoints and gives
two distinct zeros by the intermediate value theorem. These intervals
are disjoint, including the interval through `2*pi`. Thus there are at
least `2*K` distinct unit-circle zeros. For `v>=10`, `2*K>=12>10`.
This proves the second assertion and excludes essential atorality for
every primitive pair with `v>=10`.

**The remaining finite box.** For `2<=v<=9` there are exactly 27 pairs
`0<u<v` with `gcd(u,v)=1`. For such a pair let

\[
k(u,v)=\#\{0\le j<v:v<3\,[u(2j+1)]_{2v}<5v\},
\]

where `[x]_(2v)` is the residue in `0,...,2v-1`. This is the exact
integer form of the strict midpoint sign test above. Let `r(u,v)` be
the sum of the degrees of those polynomials among

\[
\Phi_5=1+X+X^2+X^3+X^4,\quad
\Phi_6=1-X+X^2,\quad
\Phi_{12}=1-X^2+X^4
\]

that divide `P_{u,v}`. Exact monic division and the integer test give
`2*k(u,v)>r(u,v)` for all 24 pairs other than `(1,2),(1,3),(3,4)`.
The complete 27-row table is in `expected.json`; `verify.py` regenerates
every row. As a separate check, a rational Sturm sequence counts the
real roots in `(-2,2)` of `1+D_u(Y)+D_v(Y)`, where
`D_0=2,D_1=Y,D_(j+1)=Y*D_j-D_(j-1)`. These correspond to conjugate
pairs of unit-circle roots. Its exact counts independently confirm
the required strict excess over torsion roots for all 24 pairs.

For the three remaining pairs direct multiplication gives

\[
P_{1,2}=\Phi_5,\qquad
P_{1,3}=\Phi_5\Phi_6,\qquad
P_{3,4}=\Phi_5\Phi_{12}.
\]

They are cyclotomic products and therefore essentially atoral.
All other pairs have a unit-circle zero that is not a root of unity.
This proves the equivalences. The finite box is a small exact
computational component of the theorem; the unbounded tail is the
written sign-change argument. No inference from a large tested range
is used. Square-freeness of `P` is not assumed: both counts are counts
of distinct roots. \(\square\)

## 2. Exact consequence for the selected modular problem

The preceding global-reduction package proved that every sum-distinct
set at excess five has centered holes `K={0,+/-a,+/-b}`, with a unit
offset. It also proved that these holes determine one sign class.
Consider the following property of such a hole set:

> After some common unit dilation, the two signed offsets have integer
> lifts `0<u<v` for which `P_{u,v}` is essentially atoral.

**Corollary.** This property holds if and only if `K` is unit-equivalent
to one of

\[
\{0,\pm1,\pm2\},\quad
\{0,\pm1,\pm3\},\quad
\{0,\pm3,\pm4\}.
\]

Indeed, put `g=gcd(u,v)`. Since one offset is a unit modulo `N`, `g`
is a unit modulo `N`. Dividing by it is another permitted dilation.
The theorem forces the reduced integer pair into the three displayed
types. Conversely those pairs themselves supply cyclotomic lifts.
The previous reconstruction theorem identifies the corresponding sets
as exactly `B0,B1,B2`.

Thus **proving an essentially atoral lift exists for every admissible
set is equivalent to proving the original classification**. The
criterion does not dispose of a previously unresolved modular case.
In particular every genuinely new admissible class, if one exists,
has non-torsion unit-circle zeros in every lifted hole polynomial.

## 3. Two checks on proposed shortcuts

### A fixed normalized lift can already fail for a known set

At `N=37`, the set `A={1,7,11,22,24}` has 32 distinct subset sums and
centered holes `{0,+/-1,+/-12}`. It is the unit multiple `24*B1`.
The displayed lift `P_(1,12)` is not essentially atoral, although a
further unit change yields the familiar `(1,3)` lift. The checker
verifies the subset sums and centered holes directly.

Thus neither a unit-normalized core nor a small circulant determinant
forces *that particular lift* to be cyclotomic.

### A determinant of five does not force any cyclotomic lift at general odd order

At `N=41`, let `K={0,+/-1,+/-9}`. Its circulant determinant is exactly
five, but its unit orbit is disjoint from all three displayed hole
types. Hence no integer lift in any unit dilation is essentially
atoral.

There are two independent exact certificates of the determinant. The
file `norm_counterexample.json` gives integer polynomials `U,V`, with
coefficients of absolute value at most 18, satisfying

\[
(1+X^8+X^9+X^{10}+X^{18})U(X)
 +(1+X+\cdots+X^{40})V(X)=1.
\]

The identity proves that the first polynomial is a unit in
`Z[X]/(1+...+X^40)`. Its resultant with the second polynomial is
therefore `+/-1`; conjugate pairing makes it positive, hence one.
Multiplying the trivial Fourier eigenvalue, five, gives the determinant.
Separately, fraction-free Gaussian elimination evaluates the full
41-by-41 integer circulant and returns five. The complete unit orbit
is checked against the three known orbits.

**41 is not of the form `2^n+5`.** This is a counterexample only to the
general odd-order norm-to-lift implication, not to the selected
subset-sum conjecture or to its parameter-specific determinant route.
No subset-sum realization is asserted at this order.

## 4. Why the checked logarithmic equidistribution theorem does not close the gap

The fixed two-variable Laurent polynomial underlying the cores is

\[
F(X,Y)=1+X+X^{-1}+Y+Y^{-1}.
\]

It is irreducible over `C` as a Laurent polynomial. Viewed as a monic
quadratic in `Y` after multiplying by `Y`, its discriminant is

\[
(1+X+X^{-1})^2-4
=X^{-2}(X^2-X+1)(X^2+3X+1),
\]

which has four distinct simple zeros and is not a square in `C(X)`.
On the real unit torus, `F=0` has an analytic arc near
`(X,Y)=(i,exp(2*pi*i/3))`: the derivative in the second angular
coordinate is nonzero. This arc is Zariski dense in the irreducible
curve `F=0`. The curve is not a torsion coset: an irreducible
codimension-one torus coset is defined by a binomial up to a Laurent
unit, whereas `F` has five terms.

Consequently `F` is not essentially atoral. Dimitrov--Habegger,
Theorems 1.1--1.2 and Corollary 1.4, require essential atorality; they
cannot be applied here. The univariate route also encounters the
non-torsion unit-circle zeros proved above. This is a failure of the
checked theorem's hypotheses, not a proof that all possible analytic
approaches fail. Their general conjecture is not adopted as a premise.
The source also discusses results for a fixed arbitrary univariate
polynomial. Here the lifted exponents vary with the modulus, so a
fixed-polynomial limit supplies no asserted uniform estimate over the
retained family.

## Status and trust boundary

The polynomial theorem is a precise corollary of classical small
vanishing sums combined with an elementary root count and 27 exact
finite cases. No priority claim is made for its cyclotomic-product
classification. Its purpose here is to identify the missing global
step and prevent an invalid use of atoral equidistribution.

The third research pass has **not** proved the unrestricted
classification, an absolute core bound, an infinite family of actual
exceptions, or `O(N^2)`. The residual `n>=15` is unchanged. The strict
closing-pass gate is therefore missed; problem-level reassessment and
literature-first reselection are due. Both earlier structural/counting
packages remain intact. No old pending graph transaction is resubmitted.

Trust: written classical arguments, the cited vanishing-sum theorem,
and exact Python arithmetic for the explicitly delimited small box
and two controls. No floating-point roots, solver verdict, formal
proof-assistant verification or independent peer review is claimed.
