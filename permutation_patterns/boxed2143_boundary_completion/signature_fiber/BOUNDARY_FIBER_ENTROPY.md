# The full avoidance entropy persists inside one interval boundary signature

Author: Lyra (literature-researcher-2), 2026-10-05. New separate uniform partial
argument, awaiting Sage's check. Earlier boundary/root packets remain frozen.
Full target410 is unsolved. This is a compatible-state multiplicity reduction,
not a superexponential construction: its avoiding inputs are exactly the
already unresolved avoiding permutations.

## Guard map and exact occurrence preservation

Fix integers m>=1 and k>=1. Set q=2k+1, N=q*m-2k and
z_i=1+q*i for i=0,...,m-1. In each value gap(z_i,z_(i+1)), put its upper k
labels z_i+k+1,...,z_i+2k into a prefix P, and its lower k labels
z_i+1,...,z_i+k into a suffix S. Arrange each of P and S in increasing order
across all its labels. Both are empty when m1. For sigma in S_m define

    Phi_(m,k)(sigma) = P + (z_(sigma_1-1),...,z_(sigma_m-1)) + S.

This uses each label1,...,N once. It recovers sigma from the fixed middle
position band and the affine formula(z-1)/q+1.

**Claim1.** Every boxed2143 occurrence of Phi is wholly inside that middle
band. The affine label map is therefore a bijection from the occurrences of
sigma to those of Phi; in particular Phi avoids iff sigma avoids.

Proof: let selected roles be(a,b,c,d), with b<a<d<c. The prefix and suffix
are increasing. Thus the selected minimum b cannot be in the prefix: an
earlier a there would be smaller. The selected maximum c cannot be in the
suffix: a later d there would be larger. If b were in the suffix then c
would also be there; if c were in the prefix then b would be there. Hence b
and c lie in the middle band. Write c=z_t. The first selection a can only
be in prefix or middle, and d can only be in middle or suffix.

Suppose a is a prefix guard in gap i. If d=z_s is middle, a<d<c implies
s>=i+1 and t>=s+1, so t>=i+2. If d is a suffix guard in gap j, a<d forces
j>i, because prefix guards in a gap exceed all suffix guards in that gap;
d<c then t>=j+1, again t>=i+2. In either case choose any prefix guard in
gap t-1. Such a point exists because k>=1 and t>=i+2. It occurs after a in
the increasing prefix and before middle b, and has value larger than a but
smaller than c. It therefore lies in the open rectangle and contradicts
emptiness. No a can be in the prefix.

Now a=z_s is middle. Since b<a, write b=z_r with r<s; thus s>=1. If d is
a suffix guard in gap j, a<d gives j>=s. Choose any suffix guard in gap s-1.
It occurs before d in the increasing suffix and after middle c, and its
value exceeds z_(s-1)>=b and is below a<c. It shades the open rectangle.
No d can be in the suffix. All four selections are therefore middle.

For a middle-only selection, its horizontal span is contained in the middle
band, so no guard point is in that span. Affine labels preserve exactly all
middle-point order and strict-interior comparisons. This proves both directions
and equality of occurrence multiplicities for arbitrary m,k,sigma. QED.

## One complete signature shared by every input

Let Sigma_(N,k)(w) list the first at most k and last at most k retained
entries of w|[lo,hi] for EVERY global integer value interval. The prior
boundary composition uses k3. This theorem does not assume that those k3
summaries alone decide current avoidance of an arbitrary full word.

**Claim2.** For fixed m,k, Sigma_(N,k)(Phi_(m,k)(sigma)) is independent of
sigma, even when sigma is not avoiding.

Proof: an interval containing at least two middle labels contains the entire
value gap between two consecutive ones. That gap supplies k prefix and k
suffix guards. Thus its first k retained entries are all prefix guards and
its last k retained entries are all suffix guards; both orders are fixed.
For an interval containing zero or one middle label, its complete restricted
word has fixed prefix, that uniquely determined middle label if present, and
fixed suffix. It too is independent of sigma. All intervals are covered.
The known full label set is [1,N], so no omitted-label sentinel convention is
needed. QED.

Define beta_(m,k) to be the number of boxed2143-avoiding permutations of length
N whose signature equals that of Phi_(m,k)(identity). This is the ENTIRE
signature fiber, not merely outputs of the guard format. Since Phi is
injective and occurrence preserving,

    a_m <= beta_(m,k) <= a_((2k+1)m-2k).

**Claim3.** For any one fixed k>=1, bounded-exponential growth of a_n is
equivalent to a uniform bound beta_(m,k)<=D^((2k+1)m-2k) for some D>=1 and
every m>=1. Forward is the upper inequality. Reverse gives
a_m<=D^((2k+1)m-2k)<=(D^(2k+1))^m for every m. Thus even this explicit sequence
of single signature fibers retains the full agreed growth decision.

No bound on beta is supplied. The guard format's avoiding slice has exactly
a_m members, not m! members. Claims1--3 therefore establish neither side of
the target. In particular the k3 map of length7m-6 is not an all-input avoiding
completion construction.

## Context and relation to the other lanes

The interval formulation is source-known (Kitaev--Qiu--Xu, arXiv2609.13764v1,
Theorem3.2, https://arxiv.org/html/2609.13764v1). This proof is a direct guard
construction, without a novelty or priority claim. Sage's distinct checked
band-marker map preserves the original entropy inside one min/max Cartesian
pair; its exact public source is
https://github.com/helgithorskarp/math_results/tree/2d02dc425cf66e89a01676bae3f19b076caf28c8/boxed2143_cartesian_marker_obstruction_20261005 .
Here the guards establish independence of the entire interval first/last-k
signature, including the k3 interface used by our completion algorithm. No
identification with Sage's particular tree pair or Quinn's maximum shape is
assumed. This is a separate claim, not an expansion of either acceptance.

The coordinator's primary range-top-k context note483 motivates distinguishing
the number of signatures from the number of avoiding words inside them. The
present argument does not rely on that encoding theorem or claim its new
verification. It gives a self-contained exact obstruction to ignoring fiber
weights, even if an exponential signature-count bound is already known.

## Author finite controls

`check_boundary_fiber.py` uses the literal quadruple/shading definition to
compare COMPLETE occurrence sets and the exact role-position shift, and checks
every value-interval prefix/suffix signature. It covers all459 pairs of a
permutation m<=5 and k in{1,2,3}, including nonavoiding inputs; checks recovery;
and tests a proposed constant fiber bound beta<=1 with the explicit m2,k3
two-word collision. These are falsification controls for the uniform proof,
not a different-researcher check or an inference of infinite growth.

Reproduce with Python3.11 standard library:

    python3 -B check_boundary_fiber.py

The missing entropy bound or universally compatible-root invariant remains
the research obligation. The target and full-success criterion are unchanged.
