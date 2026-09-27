# Exact all-threshold certificates for non-anchored chain endpoints

This gives a uniform endpoint perturbation budget for every supplied finite
mixed chain of anchored short maps and certified R5 motions with radius, total-loss, support-width,
prior-mass, and variance guards. The budget is independent of the chain length
and of its smallest positive step loss. It consumes R8's new mixed-chain
margin, which incorporates R3's polynomial margin, and the peak/stability machinery.

The [proof](PROOF.md) uses the imported chain margin to join the signed low
tail to the entire middle range and the source peak.
The exact [input](INPUT.json) certifies a full prior/cloud family around
fifteen-point endpoints with no norm-preserving anchors. The six familiar
folds used to supply its chain are not new geometry. The suite also consumes
R8's existing mixed-chain input, adding whole prior/cloud/variance guards.

**Status:** complete author argument; independent review pending. The
unrestricted dimension-three problem remains open. Simple transitivity,
qualitative openness, and the chain margin are prior work.
The radius is explicit but extremely small; no practical unrestricted cover
or new Kneser--Poulsen result is claimed.

From the repository root, with CPython 3.11.2 (standard library only):

```sh
python3 -B probability/gaussian_chain_stability_certificate/verify.py
python3 -O -B probability/gaussian_chain_stability_certificate/verify.py
python3 -B probability/gaussian_chain_stability_certificate/verify.py \
  --input probability/gaussian_chain_stability_certificate/INPUT.json \
  --certificate probability/gaussian_chain_stability_certificate/CERTIFICATE.json
```

The first two commands reproduce [EXPECTED.json](EXPECTED.json); the supplied
record mode checks just that record and its pinned dependencies, without
calling or importing the producer. The default suite calls the producer in
a subprocess only for reproducibility and refinement controls.

To regenerate the compact certificate without overwriting it:

```sh
python3 -B probability/gaussian_chain_stability_certificate/certificate.py \
  probability/gaussian_chain_stability_certificate/INPUT.json
```

Expected status: `CHAIN_FAMILY_EXACT_CONTROLS_PASS`. The checked family has
15 labels, 6 steps, ordered loss floor `135/256`, width lower bound
`13/20000`, variance interval `[1,4]`, and budget exponent `12564298226894`.
Only this exponent is stored; its dyadic denominator is never expanded.
Certificate SHA256:
`0c4b5935504cd756a86497381d81685da0c723173189fcfcd3c145303fcdb2de`.

The suite includes 27 negative controls and refinement through 257 links
with an unchanged budget. It is a small rational computation, not a replay
of a large search. The normal and optimized runs were checked against the
expected output (1.74 and 1.96 seconds on CPython 3.11.2, under 23 MiB
reported child RSS). Supplied-record checking took 0.13 seconds. See [FORMAT.md](FORMAT.md) for supplied-input semantics,
[SOURCES.md](SOURCES.md) for provenance, and [DEPENDENCIES.json](DEPENDENCIES.json)
for exact dependency hashes. The written analytic argument is not formalized;
author-side reproducibility does not constitute independent acceptance.

To verify the file manifest, from this directory run `sha256sum -c SHA256SUMS`.
