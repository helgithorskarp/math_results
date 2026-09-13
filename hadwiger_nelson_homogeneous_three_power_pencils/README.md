# Homogeneous pencils on three powers cannot occur

**For any three distinct nonnegative radix exponents**, five nonmonomial Eisenstein-unit norm events whose F4 signatures form a full homogeneous pencil cannot all occur at a physical complex parameter.

The proof isolates a geometric restriction on three free complex vectors. If their five normalized pencil forms all have modulus one, then either two vector lengths coincide, or their squared lengths are exactly **1/4, 3/4, 7/4**. The all-unit case is impossible. Three distinct powers of one positive radius cannot satisfy these alternatives. Hence a simultaneous five-event pencil needs at least four coefficient positions.

For the selected homogeneous class, this closes all **36** such A5 pencils and **4,608** lifts, including the **24** h4195 residual pencils / **3,072** lifts selected for this pass. A separate exact calculation proves complex-affine nonconcurrence for those 24 residual pencils as well. No orbit allowance is used or updated.

The general proof has a 93,468-byte rational certificate, checked with Python's standard library. It contains 161 polynomial identities of total degree at most four. The checker covers all 32 sign cases, verifies the 1,152 three-variable lifts by two normalization methods, and checks the all-unit boundary. Both free-vector alternatives have explicit positive witnesses, so the common-radix step is essential.

- [Proof and precise scope](PROOF.md)
- [Portable checker](verify.py), [exact arithmetic](exact.py), [certificate](certificate.json)
- [Reproduction](REPRODUCE.md), [expected result](EXPECTED.json), [controls](controls.py)
- [Exact A5 interface](A5_INTERFACE.json), [optional complex-affine audit](finite_a5.py)

The theorem concerns the fixed scale of T+zT+...+z^nT, with T={0,1,omega}. The theorem also allows exponent zero, recovering the earlier two-coordinate affine-pencil exclusion. Pencils involving four coefficient positions and an extra arbitrary common dilation are outside its scope. A5 is not closed, and no five-chromatic construction is obtained. The proof is author-checked; external independent review is outstanding.

The published record remains 509 vertices according to [Parts](https://arxiv.org/abs/2010.12665), corroborated in [Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4), checked on 2026-09-13. This result does not improve it.
