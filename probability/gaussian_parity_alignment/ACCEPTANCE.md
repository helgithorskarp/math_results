# Independent acceptance and scope

On 27 September 2026, the
[independent review](../gaussian_parity_alignment_review_frontier/REVIEW.md)
accepted the correctness of the theorem and applications at author source
commit `f11610f52076d5e02797e45f586e83e46fb3fe3f`.
The review source is `a855db965f92b7011fbf6034a2df765d2fb1d745`.

Discovery Net review **6404** is
`bafkreigyhde3roohzmpa57eduxrldugycju4hg6koeu7czyopaoayprm4q`.
Its `VERIFIES` and `REPRODUCES` relations to original **6396**,
`bafkreicuhkfttm4ixgn55hupyfhfj6tqvfsxjy6qnkjc7zb5umisbfnke4`,
were confirmed in the committed graph at indexed height6407.

The accepted scope is:

- Every positive Gaussian variance and every hinge threshold for bounded
  atomic or nonatomic mixtures of complete, uniformly weighted even-sign
  four-point orbits, with arbitrary orbit masses, axis lengths and parities.
- The stated continuous-box contraction and the eight-site benchmark with
  priors constant on its two tetrahedral orbits, including the specified
  further uniform scaling.
- Both finite ball-union and ball-intersection comparisons with radii
  constant within each four-point orbit.

The reviewer reproduced the author checks and supplied a separate exact
[checker](../gaussian_parity_alignment_review_frontier/independent_check.py)
using Walsh characters, direct kernel controls, and independent geometric
calculations. The universal mixture/Jensen argument, all-points box estimate
and dominated limits remain reviewed written mathematics. The accepted
radial theorem and indecomposable-interval reduction remain dependencies.
This is independent correctness acceptance, not formal verification.

Nonuniform intra-orbit weights, arbitrary eight-site priors, independent
radii within an orbit, and spatial perturbations are outside the acceptance.
Historical novelty of the ball-volume consequences remains uncertain.
In particular, a labelled motion obstruction does not by itself rule out
weight- or radius-preserving target relabellings. No separation from every
classical continuous-motion application is claimed.

The original proof, checker and expected record are unchanged. Their record
SHA256 remains
`8c514711602ed3cc8ae3455490f2c0c1e5cbcece0a5f65b02eaef12d0efa9d1c`.
The original proof's pending-review wording records its status when written;
this file and the linked review give the updated status. Unrestricted
dimension-three Gaussian majorisation remains open.
