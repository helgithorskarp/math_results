# Complex-radix exact viability interface for team-hn-3

HN-2 owns this single architecture and its physical graph realization,
chromatic testing, and candidate decisions. The declared finite-obstruction
gate is complete. Its exceptional set remains live; it is not a collection
of known non-four-colourable graphs.

Generate the exact interface with `export_frontier.py --out NEW_PATH`.
The file contains:

- `curves`: stable IDs, integer polynomials in x,y, and canonical displacement
  coefficient lists in the basis (1,omega);
- `pair_systems`: all 264,800 necessary intersection systems;
- `nonzero_collision_polynomials`: all 2,400 collision polynomials, constant
  term nonzero, with degree at most four over Q(omega);
- the radial constraint, four-curve condition and certificate hash.

The physical interpretation is z=x+i sqrt(3)y with x,y real. Coordinates of
label a are exactly sum a_j z^j, with a_j in (0,1,omega). Injective possible
counterexamples have 243 physical vertices and at least four vanishing
active curves. Pair-system solutions need not be real, injective, distinct,
or four-curve intersections. Coincidence roots also remain undecided except
for the proven radial exclusions. Do not infer viability from the Bezout
allowance.

The highest-value complementary interface is an exact reduction of the
whole pair/collision frontier using the four-curve and radial predicates,
or physical symmetry, with reproducible completeness. HN-2 retains all
chromatic searches; do not independently search the same graph family.

Two exact parameter symmetries are available for such a reduction:

    R(z)=omega^2*z,
    A5(R(z)) = A5(z) - z - omega*z^2 - z^4;

    C(z)=conjugate(z),
    A5(C(z)) = sum_{j=0}^4 conjugate(z)^j - conjugate(A5(z)).

They generate D3 on the parameter plane. The first identity follows from
omega^(2j)T=T+c_j with c_j=0,-1,-omega according to j mod 3; the second
uses conjugate(T)=1-T. All six digit identities are checked in `controls.py`.
In real coordinates R sends (x,y) to ((-x-3y)/2,(x-y)/2), and C sends
(x,y) to (x,-y). No symmetry class count is claimed in this package.

Preserve h4085 and reviewer-1's h4097 acceptance as the retired three-wheel
obstruction; h4091/h4093/h4099 are closed exact supporting evidence for that
older architecture. None is a mathematical premise of the present radix
proof. Internal checks of this interface cannot replace reviewer-1.
