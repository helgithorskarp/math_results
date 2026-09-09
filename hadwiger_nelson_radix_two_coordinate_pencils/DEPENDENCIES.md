# Inputs and proof boundaries

| Durable input | Use | Source commit |
|---|---|---|
| h4105, `hadwiger_nelson_complex_radix_architecture` | Complete event definitions; producer's direct geometry. Accepted at h4123. | `95687bd35321aa6fb767fc508eac6ab186ba6d2e` |
| h4163 review of h4151, `hadwiger_nelson_radix_four_active_closure_review1` | Verifier's independent enumeration of all displacement rows and exact norm polynomials. | `8582de0bcafbda3a125c52bdf9e2fa8a49622521` |
| h4171, `hadwiger_nelson_radix_five_active_pencil` | Named five-pencil subset, full exact-five cover classification, and baseline 132,232,896 survivors after h4167 exclusions. | `d35119a821a2da13c0e015e731caebe662a7def0` |
| Reviewer-1 h4171 report, `hadwiger_nelson_radix_five_active_pencil_review1` | Newly consumed ACCEPT for cover/lift counts; pair figures accepted conditionally on h4117. | `0acf6d436934f7173fb983fc1485259ac220eb11` |
| h4177, `hadwiger_nelson_radix_five_active_orbits` | Newest exact-five versus six-or-more pair/stabilizer interface, regenerated and digest checked in this pass. | `4cd2879bd7e5528a9f7a8aef82ad862f48ede2fc` |
| h4175, `hadwiger_nelson_radix_reflection_axes` | Preserved prior checkpoint; free-action bounds inherited through h4177. No axes are reopened. | `48f368fea677d1185d50946f44f9c7d3f5543c00` |
| h4117, `hadwiger_nelson_complex_radix_d3_quotient` | Imported global-cover completeness for numerical pair-mode claims. | `f84e35de3a61a7f849ebae61a1df34639a3b0152` |

The h4177 contribution reference is
`bafkreib4hsice7oizasmbvsb4avviwhpn7glxkilvfewlf3ymsxxefqmiy`.
Its independently produced/checkable table is 2,331,829 bytes and is
regenerated outside the repository. See `HANDOFF.md` for its command and hash.
The h4171 reference is
`bafkreibg2oy54raymeyrdphyhzqgpr3ko45vqvlqwwwka2o34qipbzacwi`.

The new nonconcurrence proof is characteristic-zero algebra plus a complete
finite enumeration. It does not require the earlier collision, circle,
reflection-axis or lower-active exclusions, and it does not use the open
eight-active search. Its interpretation as the exact-five mode refinement
imports h4171 and the complete h4117 quotient through h4177; avoiding the new
quintets is only a necessary condition for remaining candidates.

Certificate generation uses CPython 3.11.2, SymPy 1.14.0 and the installed
python-flint 0.8.0 arithmetic backend. Rational linear algebra generates
witnesses; its correctness is not trusted because all supplied identities are
checked by standard-library integer/Fraction arithmetic. The verifier
reconstructs covers by explicit 16-point masks rather than affine spans.
Shared `exact.py` supplies elementary Q(ω) operations and the identity checker;
the independent census uses separate predecessor geometry and cover logic.
All three census hashes and the entrywise normalization transcript agree.

Checks under ordinary and optimized Python agree; corrupt identities and a
missing exceptional-power step are rejected. The finite proof and elementary
power-compatibility argument are not formalized in a proof assistant. No
floating-point equality, external private dataset, CAS verdict, SAT verdict
or uncommitted exploratory transcript is a proof dependency.

This result is author-checked pending reviewer-1's independent assessment.
The new reviewer report accepts h4171's cover and curve-lift census, with its
pair counts conditional on h4117. No independent acceptance of h4177, h4175
or this new result is inferred from internal team reproduction.
