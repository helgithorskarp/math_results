# Sage's separate review of Lyra's interval-signature fiber reduction

Reviewer: Sage, literature-researcher-1. Author: Lyra, literature-researcher-2.
Date: 2026-10-05. Verdict: **accept the entire stated uniform partial scope,
Claims 1–3, for every m,k>=1**, with the exclusions below. This is internal
different-researcher checking, not external peer review or a novelty verdict.
Full target410 remains unsolved.

Reviewed proof `BOUNDARY_FIBER_ENTROPY.md` has SHA256
70493a11d1be718c3ebc2e2ffe3b6955c57d3e581b96cbe80a8c4a6334342051.
The unchanged received four-file packet is pinned by manifest SHA256
10ea204ebeae4f2de0cfeaac8c3616f258179b00d41f79d5b47f8e8ea9527a96.
This scope is separate from my boundary/root acceptances493/495 and from the
author's public boundary-completion packet. Neither earlier verdict is expanded.

## Uniform reconstruction

Write q=2k+1, N=qm-2k and z_i=1+qi for 0<=i<m. Upper k labels of each
gap between consecutive targets are an increasing prefix P; lower k labels
are an increasing suffix S. The middle word consists of the targets in input
order. These three disjoint sets partition [N]. The fixed middle position
band, starting at k(m-1), and the affine inverse (z-1)/q+1 recover the input.
For m=1 the guards are empty and the assertions hold directly.

For a proposed boxed occurrence with values b<a<d<c, the selected minimum b
cannot be in the increasing prefix, and the selected maximum c cannot be in
the increasing suffix. If b were in the suffix, c would also be there; if c
were in the prefix, b would also be there. Thus b and c must be middle targets.

I checked the author's two gap-index blocker arguments and also reconstructed
the following equivalent extremal blockers. If a were a prefix guard, write
c=z_t. Since there is a smaller middle target b, t>=1, and the prefix contains
c-1. If a<c-1, that guard follows a in P, precedes middle b, and has value
strictly between b and c. It is unselected and shades the rectangle. If a=c-1,
there is no integer d strictly between a and c. Both cases exclude prefix a.
Now a is a middle target. If d were a suffix guard, write b=z_r. The larger
middle target a exists, so r<m-1 and the suffix contains b+1. We have
b<b+1<a<d<c. That guard follows middle c but precedes d in the increasing
suffix, again shading the rectangle. Hence d cannot be in the suffix.

All four selected points lie in the middle. Guards are horizontally outside
their entire span. The increasing affine target map preserves precisely every
strict-interior test among middle points. This proves both directions and the
complete occurrence bijection, including multiplicities and the fixed position
shift k(m-1). Nonavoiding input is preserved as nonavoiding input; there is no
arbitrary-input repair.

For any global integer value interval containing at least two targets, it
contains a complete gap between some consecutive targets. Thus at least k
retained prefix guards and k retained suffix guards determine its first k and
last k entries, independently of the input order. If the interval contains zero
or one target, its whole restricted word is fixed. This covers every interval,
with the full known alphabet [N], and proves equality of the entire signature
Sigma_(N,k) for all input permutations. No standardization of sparse labels is
used, and intervals containing fewer than k entries cause no exception.

Let beta_(m,k) count the ENTIRE avoiding signature fiber at length N, rather
than just guarded images. Injectivity and occurrence preservation give
a_m<=beta_(m,k)<=a_N. For any ONE fixed k, a uniform exponential bound on a_n
immediately bounds beta by D^N after increasing D to at least1. Conversely,
beta_(m,k)<=D^(qm-2k) for all m gives a_m<=(D^q)^m. The constant may depend
on the fixed k. This proves precisely the claimed growth equivalence. The
guarded avoiding slice has a_m members; it is not a factorial avoiding family.

## Independent finite controls and trust boundary

`check_lyra_signature_fiber.py` constructs the map independently by residue
classes and computes every retained interval boundary using selected positions.
Its expected complete occurrence sets use Sage's direct four-index/interior
scan from the already frozen `check_lyra_boundary.py`, with actual sparse labels.
The author map and signature functions are imported only as implementations
under test; the author's verifier and definition checker do not supply expected
answers. The written proof above establishes the unbounded quantifiers.

All459 inputs (every permutation with m1..5 and k1,2,3) agree on the image,
full alphabet, decoding, injectivity, complete occurrence correspondence and
common signature. All102917 interval entries are compared. The ordered complete
occurrence stream matches the author SHA256
d4a65a4b89c77f9ff7ff44ec2ad37b1b70ba09f01ea7173c4017d1e540bb7a8c.
The two distinct avoiding outputs56718234 and56781234 share their whole k3
signature. All received source bytes were checked before and after execution.
Runtime1.200seconds,22460KiB peak RSS, Python3.11.2, one process/thread.

Reproduce from this research directory:

```sh
python3 -B check_lyra_signature_fiber.py --author-dir received/lyra_signature_fiber_v1 --output /tmp/sage-lyra-signature-fiber.json
```

The review manifest pins this written review, checker, immutable helper and
`artifacts/lyra_signature_fiber_reproduction_v1.json`.

## Exact exclusions

No exponential bound for beta, factorial construction, universally compatible
completion root, full growth answer, novelty or priority claim is established.
I do not verify the coordinator's range-top-k encoding theorem or a bound on
the number of signatures here; none is a dependency of Claims1–3. This proof
also does not assert that a signature alone determines current avoidance.
Lyra owns publication of this exact separate scope. Target410 and its agreed
full-success criterion remain unchanged.
