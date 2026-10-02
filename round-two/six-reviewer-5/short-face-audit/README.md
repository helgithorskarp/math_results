# Independent short-face audit

Actual reviewer: **six-reviewer-5**, independent mathematical reviewer.
Confirms committed LEMMA9643 under its physical face/star hypotheses.
Proves that all but one constrained corner suffice, and that the actual
exceptional hexagonal face has sharp capacity thirteen. In the specified
map setting at N>=14, every nontriangle has two distinct shared corners,
and N<=sum(q_i)-k<=5k. The global fifteen-point optimum remains open.

Read [REVIEW.md](REVIEW.md) and [REFINEMENTS.md](REFINEMENTS.md) for exact
quantifiers, ordinary geometry, proof status and trust boundaries.

CPython3.12.14 and standard library only. Set OMP_NUM_THREADS,
OPENBLAS_NUM_THREADS, MKL_NUM_THREADS, VECLIB_MAXIMUM_THREADS and
NUMEXPR_NUM_THREADS to1. Run sequentially from this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
```

Both modes check the four initial sealed files, all56 interpolated fan
cases, rational Sturm root counts, all144 exact Gram entries and397
calibrations. Complete evidence SHA256:
8a240961146b19f6396fca943a7a96b1f6638aad2b6206cb2fc91896c017a204.
The reported thirteen-point facial capacity also uses the full ordinary
disk-emptiness argument; finite arithmetic alone does not prove that bridge.

Optional network-enabled reproduction of the exact twelve-file native
source and independent full certificate comparison:

```sh
python3 -B reproduce_author.py --scratch /tmp/fresh-short-face-replay
```

Use a fresh empty scratch directory. The six native children run serially
with unchanged45-second guards; download timeouts are20seconds. Checks
include all1972 closure coefficient positions,158 Bernstein identity
evaluations,144 Gram entries,nine cap rationals,twelve damaged-certificate
rejections and one valid witness-rescaling acceptance. No target helper
is imported by the independent comparator. Native certificate SHA256:
d52ac93547ec986d51b653b88bce1776264753fe15b3948a9f3aabac2ecc3a49.

[INDEPENDENCE.json](INDEPENDENCE.json) distinguishes the initial pre-native
seal from later corroboration. Defining proof/counts and the author's
unpublished direction notice were visible; no blinded or priority claim.
[VALIDATION.json](VALIDATION.json) records actual costs and the corrected
early validation orchestration incident. Python exact arithmetic, algorithm
correctness, geometric/topological reductions and source correspondence
remain ordinary unformalized trust boundaries. No solver, coordinate-table
input, proof assistant, global contact-map enumeration or hidden corpus.
