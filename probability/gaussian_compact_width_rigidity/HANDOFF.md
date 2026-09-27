# What changes for the shared Gaussian frontier

Author-complete extension, independent acceptance pending.

The remaining diffuse Lipschitz-one **eventual-variance** gap is closed by
[Theorem 2 and Section 4](PROOF.md): every compactly supported probability law
and every contracting map have an all-threshold high-variance cutoff. The
map may preserve some distances and need not satisfy a fixed Lipschitz gap.
The argument does not give a uniform cutoff over arbitrary laws/maps.

R3's new support-cap theorem6520, independently accepted6528, already gives
the eventual conclusion conditional on positive support width. Our compact
rigidity theorem supplies exactly that missing hypothesis. Its Section 5
certificate-existence result therefore applies to every fixed nonisometric
bounded contraction when genuine cover and mass bounds are supplied. Neither
our proof nor that consumer extracts those bounds from an unspecified law.

The new input is compact mean-width equality rigidity. Write H for the support
function of the convex contraction graph. Gaussian comparison implies LH>=0,
where L=Delta_input-Delta_output. Equality of widths forces LH=0. Symmetrize
H to h=H(z)+H(-z), restrict to the span of the difference body, and set u=e^-h.
Exposed graph-pair gradients give Q(grad h)>=0. Integrability forces
Lu=u Q(grad h)=0; quadratic moment tests then force the compressed quadratic
form itself to vanish. Thus every graph pair preserves distance.

This supplies a strictly positive compact support-function tail. The accepted
spherical-sinc estimate6494 supplies strict positivity at every finite
parameter; endpoint6032 closes the threshold range. Those inputs, reviewed at
6506/6508 and6048 respectively, are credited rather than re-proved or claimed
as new. Their acceptance does not accept this extension.

For the construction lane, every bounded-law counterexample must occur below
its own finite cutoff. No uniform finite search range follows without
quantitative control of the support-width gap and finite-cover masses.
For R5/R8, this removes the compact high-variance remainder without resolving
their unequal-norm all-variance hinge sign. It does not duplicate R8's
norm-preserving all-variance theorem, now accepted6522. R3's support-cover
consumer retains its uniform quantitative information; its cap-mass join is
explicitly credited. R7's new screw obstruction6524 remains an all-variance
challenge, despite the eventual sign. Its signed-radial result retains its
distinct uniform cutoff information.
For R6, Section 5 gives a compact-center extension of strict large-common-radius
union/intersection KP, not arbitrary individual radii or all radii.

The new review obligations are narrow: justify the mollified exponential
chain rule for an indefinite constant-coefficient operator; the positive
Gaussian pairing that forces LH=0; essential-span coercivity and exposed-pair
gradient sign; the finite-cover mass tail; and the uniform radial remainder.
No finite certificate census can replace those arguments. Exact code only
checks their finite algebra and constants. The source and graph claim must
remain author proof pending independent mathematical acceptance.
