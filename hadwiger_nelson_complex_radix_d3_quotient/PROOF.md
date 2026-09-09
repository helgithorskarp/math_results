# Proof and exact enumeration

## 1. Physical D3 symmetry

Write `T={0,1,omega}`, where `omega^2=omega-1`, and

    A5(z)=T+zT+z^2T+z^3T+z^4T.

For `R(z)=omega^2 z`, direct arithmetic in `Z[omega]` gives

    omega^(2j) T = T+c_j,   c_j=0,-1,-omega,0,-1 for j=0,...,4.

Consequently

    A5(R(z)) = A5(z)-z-omega*z^2-z^4.

This is a translation.  Also `conjugate(T)=1-T`, so

    A5(conjugate(z)) = sum(zbar^j,j=0..4)-conjugate(A5(z)),

which is a translation followed by a Euclidean reflection.  These identities
hold for point sets, hence also after coincident labels are identified and all
unit pairs are included.  Thus the strict physical graphs at `z`, `R(z)`, and
`C(z)=conjugate(z)` are isometric.

The relations `R^3=C^2=1` and `CRC=R^-1` give a D3 action.  In real parameters
`z=x+i sqrt(3)y`,

    R(x,y)=((-x-3y)/2,(x-y)/2),   C(x,y)=(x,-y).

The six sectors cut out by the three reflection axes show that every orbit has
a representative in

    K={x>=0, 0<=y<=x}.

HN2 proved that a possible non-four-colourable parameter satisfies
`1/4 < x^2+3y^2 <= 4`, giving the stated radial chamber.  Boundary points can
have reflection stabilizers, so uniqueness in the closed chamber is not
claimed.

## 2. Exact action on curves and collisions

For a displacement polynomial `P_d(z)=sum d_j z^j`, pullback by the generators
acts on its coefficient word as

    R: d_j -> d_j omega^(2j),
    C: d_j -> conjugate(d_j),

up to multiplication of the whole word by a sixth root of unity.  Therefore
the same formulas permute both the unit-event loci `|P_d(z)|=1` and the
collision loci `P_d(z)=0`.

The producer applies these coefficient-word formulas to HN2's complete exact
inventories.  The verifier does not reuse the word route for event curves: it
substitutes the two rational linear maps above directly into every one of the
2,797 primitive integer polynomials in `x,y`, clears denominators, primitive-
normalizes, and looks up the result in the source inventory.  All 5,594
pullbacks agree with the producer permutations.  Both actions satisfy the D3
relations exactly.

Orbit partitioning then gives:

| objects | orbit sizes 1,2,3,6 | total orbits |
|---|---:|---:|
| 2,797 active curves | 5, 4, 112, 408 | 529 |
| 2,400 collision polynomials | 2, 2, 78, 360 | 442 |

The sorted fixed-point counts for the six curve permutations are
`13,13,117,117,117,2797`; for collisions they are
`6,6,80,80,80,2400`.  Burnside's formula independently recovers 529 and 442.

## 3. The asymmetric pair cover

Let `E` be HN2's 264,800 unordered pairs of distinct active curves.  Its colour
protector construction is not D3-invariant, so quotienting `E` as though it
were invariant would be invalid.  The computation instead forms the complete
closure

    D3 E = {g(e): g in D3, e in E}.

It has exactly 785,380 distinct systems and 132,130 D3 orbits.  Their orbit-size
histogram is

    size 1: 4; size 2: 6; size 3: 2,452; size 6: 129,668.

For an additional coverage check, the numbers of these orbits containing
exactly 1,2,3,4,6 original members of `E` are respectively
`21,186; 104,910; 398; 608; 5,028`.  These products sum to 264,800.

If an injective possible counterexample `z` lies on a source pair `e in E`,
choose `g` taking `e` to the canonical representative `q` of its pair orbit.
Then `g(z)` lies on `q`, and it represents the same physical-isometry class as
`z`.  Hence solving the 132,130 representative systems over the whole plane
covers every candidate D3 orbit.

There are two valid but different downstream interfaces:

1. solve one canonical system per pair orbit over the whole plane, then quotient
   its solutions; or
2. restrict parameter solutions to `K`, but retain all 785,380 systems in the
   D3 closure.

In general one cannot simultaneously force both the curve pair and its point
into independently chosen canonical representatives.  Thus restricting the
132,130 canonical systems to `K` is not certified complete.

## 4. Bounds on exceptional parameter orbits

HN2 proved that distinct active curves are absolutely irreducible and hence
coprime.  For each canonical pair, projective Bezout bounds its complex common
points by the product of its two degrees.  Summing once per pair orbit gives

    7,785,424

as an upper bound on D3 orbits of injective exceptional parameters.  This is
conservative because different systems can cover the same parameter orbit and
because nonreal, infinite, and multiple intersections are counted.

Every collision-parameter orbit contains a root of one canonical collision
polynomial.  The 442 representatives have degree histogram

    degree 1: 2; degree 2: 10; degree 3: 60; degree 4: 370,

whose degree sum is 1,682.  Adding the injective and collision allowances gives

    7,785,424 + 1,682 = 7,787,106.

Since every parameter D3 orbit gives a single physical graph-isometry class,
this also bounds the number of isometry classes in HN2's exceptional cover.
It is only an allowance, not evidence that any represented graph is
non-four-colourable.

## 5. Computational trust boundary

The proof computation uses only exact integers and rational numbers in the
CPython standard library.  It imports HN2's pinned source package at commit
`95687bd35321aa6fb767fc508eac6ab186ba6d2e`; completeness and irreducibility of
that package's curve, pair, and collision inventories remain explicit input
dependencies.  This package independently reconstructs the source inventories,
checks the digit-set isometries, checks all event-polynomial substitutions,
checks both D3 actions and relations, partitions every finite set, and verifies
the certificate hashes and counts.  No CAS, SAT/SMT solver, floating-point
decision, or external review verdict is used.
