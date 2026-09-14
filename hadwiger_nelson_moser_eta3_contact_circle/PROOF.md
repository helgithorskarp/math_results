# Exact closure of the eta-cubed contact circle

## 1. Family and scope

Put

\[
 \alpha=i\sqrt3,\quad \beta=i\sqrt{11},\quad
 \rho=(1+\alpha)/2,\quad \eta=(5+\beta)/6
\]

and

\[
 M=\{0,1,\rho,1+\rho,\eta,\eta\rho,
       \eta(1+\rho)\}.
\]

The eleven unit pairs of `M` form the Moser spindle, so its chromatic number
is four. Fix

\[
 u=\eta^3=(-5+8\beta)/27
\]

and, for an arbitrary unit complex number `v`, form the set

\[
 S(v)=M+uM+vM.
\]

Edges are **all** pairs of distinct physical points at Euclidean distance one.
The claim is that this strict graph is exactly four-chromatic for every `v`.
It has at most 343 points and always contains `M`, so it suffices to prove a
four-colouring.

This theorem concerns one fixed first phase and its conjugate. It does not
close the full two-phase family and gives no global Hadwiger--Nelson bound.

## 2. Exact base arithmetic

Use

\[
 E=\mathbb Q(\sqrt{33},\alpha)
   =\{a+b\sqrt{33}+c\alpha+d\beta:a,b,c,d\in\mathbb Q\}.
\]

The exact tuple arithmetic is inherited from the independently replayable
collision package. Direct enumeration shows that

\[
 B=M+uM
\]

has 49 distinct points. Thus `B+vM` has 343 distinct points whenever
`v` is outside `E`: an equality with a nonzero `M`-difference would express
`v` as a quotient of two elements of `E`; with zero `M`-difference, the
injectivity of `B` applies.

The accepted base-field colouring embeds `E` into the unramified quadratic
extension of `Q_2` and colours integral points by their residue in `F_4`.
All points of `B` and `M` pass the exact integrality check. Therefore:

- if `v` lies in `E`, the complete graph on `S(v)` is four-colourable;
- if `v` is outside `E` and has no mixed unit contact, the 1,617 Cartesian
  edges are coloured by the sum of the two factor residues.

Possible collisions when `v` lies in `E` do not cause a problem because the
base-field colour is attached to the physical point itself.

## 3. Exhaustive contact reduction

Let `a` be a nonzero difference of `B` and `b` a nonzero difference of `M`.
A mixed edge satisfies

\[
 N(a+vb)=1.
\]

Since `N(v)=1`, multiplication by `v` turns this equation into

\[
 c v^2+S v+\bar c=0,\qquad
 c=\bar a b,\qquad S=N(a)+N(b)-1. \tag{1}
\]

When `v` is outside `E`, (1) has the monic minimal polynomial

\[
 v^2-Tv+J=0,\qquad T=-S/c,\quad J=\bar c/c. \tag{2}

Consequently every other contact at this phase has exactly the same `(T,J)`
key. Grouping difference directions by that exact key recovers the complete
mixed edge set; there is no numerical root clustering.

The generator enumerates 1,224 nonzero differences of `B` and 34 of `M`, hence
41,616 ordered difference-direction pairs. The local trace argument from the
dependency closes 38,844 directions whose trace valuation is at least `-1`.
For clarity, the argument covers `T=0`, nonnegative valuation by direct residue
colouring, valuation `-1` by the unique-lowest-valuation obstruction, and
valuation zero also by the unit-trace embedding theorem.

For the remaining directions, physical roots require

\[
 \Delta=4N(a)N(b)-S^2>0.
\]

Exactly 816 directions have nonpositive `Delta`. If
`s=Delta/3` has a square root in the real subfield, the roots already lie in
`E` and the base-field case applies. In this fixed phase no direction surviving
the preceding filters has this last form. The remaining 1,956 labelled
directions group into exactly 922 distinct irreducible quadratics, involving
134 exact radicands.

For each group the two physical roots are constructed exactly as

\[
 v=T/2\ \pm\ \frac{\alpha}{2c}\sqrt{s}. \tag{3}

The verifier checks `N(v)=1` and (2) for both signs.

## 4. Exceptional graphs and positive certificate

Every exceptional root gives an injective 343-point support. The graph begins
with 1,617 Cartesian edges and has the following complete edge census, counted
once per irreducible quadratic (the two conjugate roots have the same graph):

| Edges | Quadratics |
|---:|---:|
| 1,618 | 554 |
| 1,619 | 240 |
| 1,621 | 76 |
| 1,622 | 20 |
| 1,624 | 12 |
| 1,625 | 8 |
| 1,631 | 12 |

`certificate.json` contains 80 distinct four-colour words on the fixed order
`B x M` and a 922-entry assignment. The verifier does not call SAT. For every
quadratic it:

1. regenerates all contact directions from exact field arithmetic;
2. constructs both roots (3) and all 343 physical points;
3. checks all 58,653 point pairs for both roots by each of two exact metric
   formulas;
4. requires both reconstructed edge lists to equal the contact-key graph; and
5. checks the assigned word on every reconstructed edge.

This is 108,156,132 exact unordered-pair audits. A constant word is rejected
in all 922 cases. The certificate words can be regenerated deterministically
with CaDiCaL, but only their direct positive verification is trusted.

Together with the base-field, no-contact, and local-trace cases, the inventory
is exhaustive for every unit `v`. Since `M` is contained in every support, the
chromatic number is exactly four.

Finally, multiplication by `lambda=eta*rho` followed by complex conjugation
maps `M` to itself. It sends `u=eta^3` to `eta^-3` and `v` to `bar(v)`, proving
the conjugate-circle statement. The verifier checks this seven-point symmetry
exactly.

## 5. Trust boundary and construction consequence

There is no floating-point geometry in the theorem. Trust remains in the
unformalized quadratic/contact reduction and cited local-field colouring,
ordinary exact Python enumeration, the C++17 integer kernel, and the compiler.
The two native metric formulas are independently derived but share the exact
coordinate generator; this is an author audit, not independent peer review.

This closes the richest first-phase power found in the preceding discovery
census (32 simultaneous extra contacts before local filtering), and does so
for its entire free `v`-circle. It is therefore a meaningful construction-search
boundary: continuing to sample `eta^3` or `eta^-3` cannot yield a sub-509
five-chromatic graph. Other injective first phases remain open.
