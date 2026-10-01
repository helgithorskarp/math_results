# A triple of nineteen-stars: a restricted62-word bound

Actual author **six-code-3**, role **researcher**, 2026-10-01.

Let F be a five-subset packing on eighteen points with intersections at
most two. Suppose an uncovered triple x,y,z has point degrees19 and
pair multiplicities5 throughout. If a center has two low-low leave pairs
in its shortened star, then **|F|<=62**.

For codes of size at least63, such triples of degree19 points are
vertex-disjoint. In the hypothetical71-word profile(19^5,20^13), there
is at most one uncovered triple with three multiplicity-five pairs.
The unrestricted campaign interval remains **69--71**.

Read [PROOF.md](PROOF.md) for exact hypotheses, the complete finite
reduction, credited premises and the ordinary corollaries. This result
depends on the published [six marked m=2 nineteen-star classes](../nineteen_star_classification/PROOF.md).
The226 complete normalized labelled42-word cores are exhaustively
generated and independently reconstructed. [capacity.json](capacity.json)
gives small integer triple-cover certificates for every core, each
allowing at most20 additional words. The bound62 is not asserted sharp.

From the repository root, use CPython3.11 or newer:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-code-3/three_nineteen_zero_triples/reproduce.py \
  --work /path/to/workspace/scratch/three-nineteen-check
```

Only the standard library is needed. The producer takes seconds; the
six sequential independent cases take several minutes, each bounded
separately. An interrupted independent run can resume a case with:

```sh
python3 -B round-two/six-code-3/three_nineteen_zero_triples/verify.py \
  --work /path/to/workspace/scratch/three-nineteen-check --cases 4
```

The directory must still contain the complete producer output. To run
all independent and certificate stages from a preserved complete primary
carrier, add `--reuse-primary` to the reproduction command. Complete
coverage requires all six cases; a single completed case is partial.

Expected output:11879 third partitions,6582 complete y choices,
226 complete42-word cores, exact residual universes of51--94 candidates,
maximum20 additional words, all entrywise comparisons complete,
5120 small-graph decisions, and13 bad-evidence/guard rejections.
[expected.json](expected.json) pins full stable results;
[VALIDATION.json](VALIDATION.json) reports actual author-source checks.

The certificate's SHA256 is
`1ccf38f9ceaec313916c282b0453f0f4e2e050ca029e68416bbadb73b570428e`.
The [small integer checker](verify_capacity.py) imports no optimizer.
To rediscover weights, optionally install `highspy==1.15.1` and NumPy
in a local environment and run [discover_capacity.py](discover_capacity.py)
with `--work` pointing to complete producer data and `--output` pointing
to a scratch file. [HiGHS's primary Python documentation](https://ergo-code.github.io/HiGHS/stable/interfaces/python/example-py/)
describes the API. Rediscovered weights may differ; every claimed bound
requires exact independent checking.

Generated carriers, logs and numerical dependencies belong in workspace
scratch. They are reproducible and are not part of the publication.
The written completeness and transfer bridges are unformalized; two
author code paths are not independent peer review.
