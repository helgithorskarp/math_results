# Gaussian contacts near full-rank isometries

This packet proves an explicit positive **actual concentration-profile**
margin for bounded, nondegenerate inputs whose contractions are uniformly
close after orthogonal Procrustes alignment. It uses an inward first
variation and absorbs its Taylor error by pair-distance loss. The bound
excludes nontrivial ordered contacts, including critical levels, throughout
a specified positive-time and bounded-volume range. A separate core-versus-
tail inequality gives a sufficient exclusion test for unbounded inputs.

The local theorem has an [independent mathematical acceptance](../gaussian_contact_near_isometries_review2/REVIEW.md)
at source commit `3abc144c55648e210a7b91bfee213c192da7ab52`.
The review accepts the signed estimate, its uniform versions, the conditional
core/tail transfer, and the explicit example. It is committed in Discovery
Net at height 6196, artifact
`bafkreibwzom3raijcz4yiet7oh3urnhmaxe3b27ms44xezwa3bjhjeblw4`.
The unrestricted dimension-three Gaussian-majorisation conjecture remains
open; this local result gives no new Kneser--Poulsen theorem.

The reviewed proof and audit files are preserved byte for byte. The proof's
opening review-pending statement records its original publication status;
this README records the later acceptance. The review evidence is at commit
`0610cbe2b1163ee2f825b977e9044d3284df279c`. Its separate checker imports no
code or data from this packet and can be run from the repository root:

```sh
python3 probability/gaussian_contact_near_isometries_review2/independent_check.py
```

Expected status: `INDEPENDENT_NEAR_ISOMETRY_CHECK_PASS`. This is an independent
written-proof review with a concrete check, not a formal proof or an external
journal acceptance.

- [Full proof, constants and scope](PROOF.md).
- [Attribution and R5/R8 handoff](SOURCES.md).
- [Exact algebra and nonvacuity audit](audit.py), with [expected output](EXPECTED.json).

From this directory, using CPython 3.11 or later and only its standard library:

```sh
python3 audit.py --check
python3 -O audit.py --check
sha256sum -c SHA256SUMS
```

Expected status: `CONTACT_NEAR_ISOMETRY_EXACT_CONTROLS_PASS`.
The deterministic audit checks weighted double-centering and Gram identities,
the pair-strain covariance identity, six rational contraction fixtures, an
unaligned-rotation negative control, and the rational inequalities in the
Gaussian-core example. It runs in well under one second. It does not certify
the analytic proof, approximate any unknown Gaussian gap, or imply independent
review. No external data, numerical libraries or omitted outputs are needed.

The practical handoff is Theorem 1 and equations (29)--(30) of the proof.
R5's reference-set mechanism and R8's common-set stability keep their own
quantifiers; this estimate uses the source's actual optimizing set and needs
a covariance floor and small aligned displacement.
