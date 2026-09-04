# A four-color field obstruction to two-overlap gadget composition

Identify the Euclidean plane with the complex plane and put

\[
E=\mathbb Q(\alpha,\beta),\qquad
\alpha=i\sqrt3,\quad \beta=i\sqrt{11},\quad
s=\sqrt{33}=-\alpha\beta.
\]

Thus every element is uniquely `a + b s + c alpha + d beta`, with rational
coefficients. Its real and imaginary coordinates are
`(a+b sqrt(33), c sqrt(3)+d sqrt(11))`. In particular, this is a restricted
coordinate set, and should not be confused with the larger Cartesian plane
`Q(sqrt(3),sqrt(11))^2`.

**Theorem.** The strict unit-distance graph on all of `E` has chromatic
number four. There is an explicit coloring computable using integer
arithmetic on any four rational coefficients.

The method is the classical residue-field coloring mechanism described by
David Speyer for the standard Moser construction ring in Polymath16. We give
a self-contained extension to arbitrary rational coefficients, then apply it
to the archived Parts gadget families. No priority claim is made for the
field-coloring theorem or its method.

## 1. A compatible binary square root

There is a root `r` of `r^2=33` in the 2-adic integers with `r=1 mod 8`.
For completeness, write `r=1+8t`. The required equation becomes

\[
f(t)=4t^2+t-2=0.
\]

If `f(t_j)=0 mod 2^j`, exactly one of `t_j` and `t_j+2^j` is a root modulo
`2^(j+1)`, since `f'(t)=8t+1` is odd. Starting modulo one and lifting one
binary digit at a time gives a compatible sequence and hence a 2-adic root.
This also proves uniqueness in the stated branch. The implementation returns
only the finitely many digits needed for an input's denominator.

Let `omega` satisfy `omega^2+omega+1=0` over `Q_2`. This polynomial is
irreducible modulo two, and its root generates a quadratic field `U`.
Set `alpha_2=1+2 omega`; then `alpha_2^2=-3`. The assignments

\[
\alpha\longmapsto\alpha_2,\quad
\beta\longmapsto(r/3)\alpha_2,\quad s\longmapsto r
\]

define an embedding `iota:E -> U`. They preserve the defining relations;
injectivity also follows from `r` being irrational over `Q` and `alpha_2`
being outside `Q_2`. Complex conjugation is carried to the automorphism
`omega -> omega^2`, with `r` fixed.

## 2. Every unit displacement has a nonzero residue

Write `iota(z)=A+B omega`, with `A,B in Q_2`. The conjugate norm is

\[
\iota(z\overline z)=A^2-AB+B^2.
\]

For nonzero `A+B omega`, put `m=min(v_2(A),v_2(B))`, taking `v_2(0)=infinity`.
Then `A=2^m A_0`, `B=2^m B_0`, where `A_0,B_0` are 2-adic integers and at
least one is odd. For each nonzero pair in `F_2^2`,

\[
A_0^2-A_0B_0+B_0^2=1\pmod2.
\]

Consequently `v_2(A^2-AB+B^2)=2m`. If `|z|=1`, its norm is exactly one,
so `m=0`: both local coordinates are integral and at least one is odd.
This is the entire arithmetic obstruction.

## 3. Coloring the whole field, including nonintegral points

For `x in Q_2`, let `epsilon(x)` be the coefficient of `2^0` in its binary
expansion. Such an expansion has only finitely many negative powers. Define

\[
C(z)=\big(\epsilon(A),\epsilon(B)\big)\in\mathbb F_2^2,
\qquad \iota(z)=A+B\omega.
\]

If `x-y` is integral, the negative-power digits of `x` and `y` agree, and
`epsilon(x)-epsilon(y) = x-y mod 2`. Now suppose `|z-w|=1`. Section 2 shows
that the two local coordinate differences are integral and at least one is
odd. Therefore `C(z) != C(w)`.

This defines a coloring on all of `E` without choosing coset representatives.
It is **not** an additive homomorphism on the whole field: for example,
`C(1/2)=(0,0)` but `C(1)=(1,0)`. On each coset of the local integer ring,
the adjacency argument is ordinary reduction modulo two. In particular, no
invalid ring homomorphism from a characteristic-zero field to `F_4` is being
asserted.

For the lower bound, `E` contains the Moser spindle. The seven points in
`verify.py` have its eleven strict unit edges. In a three-coloring, the two
triangles on one common edge force the two other vertices to have the same
color. Applying this to the two rhombi forces their outer endpoints to have
the same color as their shared root, but those endpoints are adjacent.
Thus three colors are impossible and the upper bound four is attained.

## 4. Explicit finite algorithm

Suppose the input is

\[
z=(a+b s+c\alpha+d\beta)/D,
\quad a,b,c,d\in\mathbb Z,\quad D>0.
\]

Write `D=2^e m` with `m` odd. Then

\[
A=\frac{3a+3br+3c+dr}{3D},\qquad
B=\frac{6c+2dr}{3D}.
\]

To obtain the zero-th binary digits, compute `r mod 2^(e+1)`, multiply each
numerator by the inverse of `3m` modulo `2^(e+1)`, and extract bit `e`.
No floating-point or approximate-distance operation occurs. To check the
norm formulas directly, put `P=3a+3br+3c+dr` and `Q=6c+2dr`. Using `r^2=33`,
expansion gives

\[
P^2-PQ+Q^2=9\big(a^2+33b^2+3c^2+11d^2+2(ab+cd)r\big).
\]

The digit-extraction argument also shows independence from the chosen
integer representation of `z`.
`coloring.py` implements exactly these formulas.

## 5. Two overlaps force the transformed gadget into the same field

**Corollary.** Let `A,B` be any subsets of `E`, and let `g` be any Euclidean
isometry. If `A intersection g(B)` contains at least two distinct points,
then the strict unit-distance graph on `A union g(B)` is four-colorable.
There is no denominator bound, overlap upper bound, or vertex-count bound.

Indeed, write `g(z)=u z+t` or `g(z)=u conjugate(z)+t`, with `|u|=1`.
Choose two overlaps `g(b_j)=a_j`, `j=1,2`, with `a_1 != a_2`. In the first
case,

\[
u=(a_1-a_2)/(b_1-b_2),\qquad t=a_1-u b_1;
\]

in the second replace each `b_j` on the right by its conjugate. Because `E`
is a field closed under conjugation, `u,t in E`. Hence the entire union lies
in `E`, and Section 3 colors all its strict unit edges.

The same argument works inductively for arbitrarily many gadgets originally
in `E`: if each new placed gadget shares two distinct points with the
existing union, the entire construction stays four-colorable. A common
initial Euclidean isometry of the whole construction does not change this
conclusion.

## 6. Consequence for the archived Parts gadgets

The exact coordinate files for `v159e646` and `v214e977` have nonzero entries
only in the four positions displayed at the start of this proof. The
standard-library verifier checks this from hash-bound inputs.

Therefore all two-overlap placements of two copies of either gadget, and
all mixed two-overlap placements, are four-colorable. This subsumes the
previous high-overlap and low-denominator exclusions. Their previously
published full two-overlap census sizes were:

| Family | Placements in the previous census |
|---|---:|
| [159 with 159](../hadwiger_nelson_nonmono159_overlap10) | 1,665,624 |
| [159 with 214](../hadwiger_nelson_nonmono159_214_overlap20/README.md) | 2,557,868 |
| [214 with 214](../hadwiger_nelson_nonmono214_overlap30/README.md) | 3,992,708 |
| Total | 8,216,200 |

These counts are quoted from the earlier artifacts, not recomputed here and
not needed for the corollary. The theorem also covers constructions beyond
those finite censuses, including the inductive composition described above.

A successful construction from these gadgets must escape this field
obstruction. In particular, a two-gadget composition using them must have
at most one overlap. Increasing the denominator within the two-overlap
family cannot help.

## Sources and status

- David Speyer, comments of 25 April 2018 (13:17 and 13:34) and 26 April 2018
  (09:10), in [Polymath16, second thread](https://dustingmixon.wordpress.com/2018/04/22/polymath16-second-thread-what-does-it-take-to-be-5-chromatic/).
  These give the residue-field coloring mechanism and its 2-adic context.
  The full-field extension and composition application are proved above;
  neither is inferred merely from an unverified claim about a unit group.
- Jaan Parts, [Graph minimization](https://arxiv.org/abs/2010.12665), for the
  underlying finite configurations and the 509-vertex record construction.
- David A. Madore, [The Hadwiger-Nelson problem over certain fields](https://arxiv.org/abs/1509.07023),
  for related reduction methods and the distinction from the larger real
  coordinate field. Its bound for `Q(sqrt(3),sqrt(11))^2` is not a claim
  about the restricted complex field used here.

The infinite claim has the analytic proof above. The executable supplies
finite implementation checks and coordinate alignment, not an exhaustive
computation over the infinite field. The proof has not been formalized in a
proof assistant.
