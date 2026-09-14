# Four concurrent P36 patches

Put

\[
 \omega=(1+i\sqrt3)/2,\qquad R=\mathbb Z[\omega],\qquad
 \rho(a+b\omega)=a-b\pmod3,
\]

and define the radial triangular patch

\[
 P=P_{36}=\{a+b\omega:a,b\in\mathbb Z,
                    a^2+ab+b^2\le36\}.
\]

Every graph below is the **strict** physical unit-distance graph: equal point
representations are merged and every pair of distinct physical points at
distance one is an edge.

## Theorem

**Theorem.** For arbitrary unit complex numbers
`alpha_0,alpha_1,alpha_2,alpha_3`, the strict unit-distance graph on

\[
 \alpha_0P\cup\alpha_1P\cup\alpha_2P\cup\alpha_3P
 \tag{1}
\]

is four-colourable.

The patch has 127 points and 342 internal unit edges, so (1) has at most
`4*127-3=505` physical points: the four origins coincide. The conclusion
includes every rotation, rational or irrational, every additional
coincidence and every additional unit edge. Reflections add no cases because
conjugation preserves `P`.

This is a restricted-family exclusion, not a global lower bound for
five-chromatic plane unit-distance graphs.

## The residue-form four-colouring

Use four colour names `A,B,+,-`. For every layer `i`, choose two bits,
equivalently a sign `s_i` in `{1,-1}` and a zero-class name `t_i` in `{A,B}`.
Colour its formal point `alpha_i z`, for nonzero `z in P`, by

\[
 c_i(z)=
 \begin{cases}
 t_i,&\rho(z)=0,\\
 \mathop{\rm sign}(s_i\rho(z)),&\rho(z)\ne0.
 \end{cases}
 \tag{2}
\]

Give the common origin colour `A`, independently of the `t_i`.

This is proper inside every layer. Reduction modulo three is a ring
homomorphism and `N(z)=rho(z)^2 (mod 3)`, so a unit difference has nonzero
residue. If the two endpoints have nonzero residues, their residues and hence
their sign colours are opposite; if one has residue zero, the two endpoints
use disjoint colour types.

Consider two layers `i,j` and normalize their relative rotation to `alpha`.
A proper cross edge `z -- alpha w` imposes the following bit equations:

- if both residues are nonzero, then
  `s_i*s_j=-rho(z)*rho(w)`;
- if both residues are zero, then `t_i` and `t_j` must differ;
- a mixed-residue edge imposes no equation.

A physical coincidence imposes the equality versions:

- for nonzero residues, `s_i*s_j=rho(z)*rho(w)`;
- for two zero residues, `t_i=t_j`.

No coincidence changes zero residue to nonzero residue. The exact pair census
described below verifies that all sign equations belonging to any one layer
pair agree, and likewise all zero-class equations agree. Thus the only
possible failure of (2) is an inconsistent XOR cycle among the four layers.

The exceptional treatment of the origin causes no problem. Every one of its
unit neighbours has norm one and hence nonzero residue. A proper zero-to-zero
cross edge therefore never uses the origin.

## Complete pair-event inventory

Write a relative rotation as `alpha=x+i*sqrt(3)y`, so
`x^2+3y^2=1`. For ordered nonzero points `z,w in P`, put

\[
 w\bar z=A+B\omega,\qquad k=N(z)+N(w)-1.
\]

The contact equation `|z-alpha w|=1` becomes the rational line

\[
 (2A+B)x-3By=k.                                      \tag{3}
\]

Conversely, every root of (3) on the rotation ellipse gives exactly that
contact. Primitive normalization and the quadratic formula therefore give a
finite, exhaustive inventory of every relative phase having a nonuniversal
cross contact. Coincidences are separately enumerated as
`alpha=z/w` with `N(z)=N(w)`; every one occurs in the contact-phase inventory.

The exact inventory contains:

| object | count |
|---|---:|
| primitive contact lines | 528 |
| relative event phases | 594 |
| rational / irrational phases | 162 / 432 |
| coincidence phases | 54 |

The six units of `R` act on phases without changing the physical patch.
After quotienting by them there are 99 event classes, 27 rational and 72
irrational. The verifier checks every stored contact by substituting the
corresponding sparse-radical phase into its squared distance, and checks every
stored coincidence in exact Cartesian coordinates.

## Why only triangles and four-cycles remain

Make two XOR constraint graphs on the four layer indices: one for the sign
variables and one for the zero-class variables. Pair consistency excludes an
inconsistent two-cycle. Any inconsistent binary system contains an
inconsistent simple cycle, hence with at most four layer vertices it contains
one of length three or four.

Every edge of such a constraint cycle comes from a proper contact or a
coincidence, hence its relative rotation belongs to the exact event inventory.
Normalize one cycle vertex to phase one. Multiplying any other phase by a
sixth root of unity leaves its copy of `P` unchanged, so it is legitimate to
use the 99 canonical phase classes.

For triangles, choose two nonidentity event classes `alpha,beta` and retain
the pair exactly when `conjugate(alpha)*beta` is also an event. There are 186
normalized rows.

For a four-cycle `1--alpha--theta--gamma--1`, both `alpha` and `gamma` are
event classes. Moreover `theta` lies in both products `alpha E` and
`gamma E`, modulo a sixth root of unity, where `E` is the nonidentity event
inventory. Grouping these exact products gives 4,231 possible target classes
and 8,100 normalized rows with four distinct patches. Chords are not dropped:

| active pair interfaces in the full placement | rows |
|---:|---:|
| 4 | 5,304 |
| 5 | 2,472 |
| 6 | 324 |

Thus the test includes fully active four-patch placements as well as chordless
cycles. All 186 triangle systems and all 8,100 four-cycle systems have
solutions for both sets of XOR variables. Therefore no arbitrary placement
can have an inconsistent XOR system, and (2) supplies its four-colouring.

For every enumerated row the verifier goes further: it merges all exact
coincidences, rebuilds the complete strict edge set from the exhaustive pair
inventory, constructs the physical colour word (2), checks agreement among
all coincident labels, and tests every edge. The four-cycle representatives
range from 451 to 505 physical vertices and from 1,368 to 1,446 strict edges.
These finite physical checks certify the reduction; no abstract chromatic
graph is substituted for a plane realization.

## Computational trust boundary and scope

The continuum reduction to finitely many pair phases is the elementary
argument (3). The finite event, triangle and four-cycle censuses are an exact
computer-assisted premise. `verify.py` uses Python integers, `Fraction`, and
sparse formal squarefree radicals. It uses no floating-point predicate, SAT
verdict, external graph file or private input. The two compact certificate
hashes commit to each normalized phase row, reconstructed strict edge stream,
and explicit physical colour word. `controls.py` confirms that deliberately
inconsistent triangle and square parity cycles are rejected.

The result is the natural four-orientation continuation of the earlier
[three full concurrent-lattice theorem](../hadwiger_nelson_three_full_triangular_lattices/README.md),
but does not use that author-side theorem as a premise. It instead proves the
finite `P36` statement directly. The earlier three-lattice theorem remains
author-checked and pending independent review at the time of this package.

`P36` is the largest norm-ball triangular patch having at most 127 points;
`P37` has 139. Consequently four generic copies of `P36` fit below the
509-point record threshold, while four generic copies of the next radial
patch do not. This theorem does not cover four full lattices, four translated
patches without a common point, five or more patches, different lattice
scales, or nonradial 127-point selections. It constructs no five-chromatic
graph and does not improve the 509-vertex record.
