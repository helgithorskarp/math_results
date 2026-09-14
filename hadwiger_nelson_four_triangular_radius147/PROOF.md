# Four common-point translated P36 patches are four-colourable

Put

```text
omega = (1+i*sqrt(3))/2,
P_N = {a+b*omega : a,b in Z and a^2+a*b+b^2 <= N}.
```

The exact computation in `verify.py` proves the following finite-event
theorem.

> For arbitrary unit complex numbers `alpha_0,...,alpha_3`, the complete
> strict unit-distance graph on
>
> ```text
> alpha_0 P_147 union ... union alpha_3 P_147
> ```
>
> is four-colourable. Equal points are identified and every pair at distance
> exactly one is an edge.

This theorem is well above the 508-point target when applied to all of
`P_147`. Its record-relevant consequence is instead the following exact
closure.

> Any four translated and rotated copies of `P_36` with a common physical
> point have a four-colourable complete strict unit-distance graph. Their
> union has at most 505 distinct points.

The result is a restricted-family exclusion, not a global vertex lower bound
and not a five-chromatic construction.

## 1. Why P147 covers every common-point translation

The norm `N(a+b*omega)=a^2+a*b+b^2` is squared Euclidean length. Suppose

```text
Q_j = t_j + alpha_j P_36,       |alpha_j|=1,
```

and choose `q` in all four copies. There is an `a_j` in `P_36` such that
`q=t_j+alpha_j a_j`. After translating `q` to zero,

```text
Q_j-q = alpha_j(P_36-a_j).
```

For `z,a_j` in `P_36`, the triangle inequality gives

```text
|z-a_j| <= |z|+|a_j| <= 12,
```

and therefore `N(z-a_j)<=144<148`. In particular
`P_36-a_j` is contained in `P_147`. A four-colouring of the four full rotated
`P_147` patches restricts to the translated `P_36` union. Reflections require
no additional case because `P_36` is invariant under complex conjugation.

There are 127 points in `P_36`. A common point belongs to all four copies, so
the union has at most

```text
4*127-3 = 505
```

points. This is the largest radial Eisenstein norm-ball patch whose generic
four-copy common-point union is below 509: `P_37` has 139 points. The ambient
choice `P_147` contains the full translated difference hull needed for
`P_36`; the next norm ball `P_148` is the natural `4*37` boundary.

## 2. Residue-form four-colourings

For `z=a+b*omega`, define

```text
r(z) = a-b mod 3.
```

Every internal unit edge of an Eisenstein patch changes this residue. Use two
disjoint colour palettes:

- colours 0 and 1 for nonorigin points with residue zero;
- colours 2 and 3 for points with residue 1 or 2.

The common origin is assigned colour 0. Each layer `j` has two binary choices:
a zero-palette bit `z_j`, and a sign bit `s_j` that decides which of residues
1 and 2 receives colour 2. Internal unit edges are proper for every choice.

For two layers at a fixed relative rotation, all cross contacts and all
coincidences reduce to at most one XOR equation in each channel:

- a zero-to-zero unit edge requires `z_j xor z_k = 1`;
- a zero-to-zero coincidence requires `z_j xor z_k = 0`;
- a nonzero-to-nonzero edge or coincidence similarly fixes one sign XOR;
- a mixed-residue edge is automatically proper because the palettes are
  disjoint.

The exact pair audit fails if one interface imposes both XOR values in one
channel. Consequently, a globally consistent assignment of the layer bits is
an explicit proper four-colouring of the full physical union. Coincident
formal labels receive the same colour by the equality constraints.

## 3. Complete contact-phase inventory

Write a relative rotation as

```text
beta = x+i*sqrt(3)*y,       x^2+3*y^2=1.
```

For two nonzero Eisenstein points `u,v`, expanding
`|u-beta*v|^2=1` gives one rational line

```text
A*x+B*y=C.
```

The checker derives this line from the ordered point pair, primitive-normalizes
it, and intersects it exactly with the unit ellipse. A line has zero, one or
two intersections, determined by an integer discriminant. Rational roots use
`Fraction`; irrational roots use sparse squarefree-radical dictionaries.
Contacts involving the common origin are phase-independent. All equal-point
events are separately derived from ratios of equal-norm Eisenstein points.

Thus every relative phase that can add a nonuniversal strict unit edge or a
coincidence is included. Every stored phase is checked to have unit norm,
every stored contact is re-evaluated in Cartesian exact arithmetic, and every
stored coincidence is checked as coordinate equality. The six unit rotations
preserve `P_147`, so phases are quotientable by this exact symmetry.

## 4. Why triangles and four-cycles suffice

After identical layer sets are removed, the sign and zero equations each form
a simple labelled graph on at most four layer vertices. An inconsistent XOR
system contains a parity-inconsistent cycle. Pair inconsistency was excluded
at the interface audit, so a shortest inconsistent cycle has length three or
four.

The verifier enumerates every normalized active triangle. For four-cycles it
uses the equivalent two-edge-path criterion. Normalize one layer to phase 1.
For a path

```text
1 -- alpha -- tau
```

the two edge labels have a definite XOR sum. Two paths to the same `tau` with
opposite sums are exactly an inconsistent four-cycle. Paths are grouped by
exact canonical target phase and independently by the sign and zero channels.
The synthetic control inserts two opposite-labelled paths and requires the
detector to find them.

The complete P147 census contains no inconsistent pair, triangle, or
four-cycle in either channel. Hence both binary systems are solvable for every
four-layer placement, and Section 2 supplies the claimed physical
four-colouring.

## 5. Scope and trust boundary

The theorem covers arbitrary rotations of four full concurrent `P_147`
patches and, by restriction, arbitrary four `P_36` isometric copies with a
common point. It does not cover four translated patches with empty total
intersection, five or more patches, larger record-relevant components, or
arbitrary plane unit-distance graphs.

The computation uses CPython integers, `Fraction`, deterministic iteration,
sparse squarefree radicals, the stated finite-event reduction, and the
published P36 arithmetic engine pinned by SHA-256. The preceding P36 theorem
and that engine have an independent high-confidence review, but the expanded
P147 census is author-side unless separately reviewed. No floating-point
predicate, SAT verdict, abstract graph realization, random input, or omitted
large certificate is used.
