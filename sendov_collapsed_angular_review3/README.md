# Independent review of the collapsed angular optimizer

Reviewer: **six-reviewer-3**, independent mathematical reviewer.
This contribution independently validates the complete angular quartic
formula and its degree-nine/higher optimizer, including spectral collisions.
It also proves a smaller degree-nine near-maximizer distance coefficient:
\[
 \delta\le14p/25\ \Longrightarrow\
 \min_{\psi\in\mathcal O}\|\theta-\psi\|^2\le\delta/(64p),
 \qquad p=10985/33554432.
\]
The target coefficient is \(3/(28p)\); the new squared-distance coefficient
is \(7/48\) of it. Constants are sufficient, not asserted optimal.

[REVIEW.md](REVIEW.md) states the verdict, exact targets, literature,
limitations and improvement opportunities.
[PROOF.md](PROOF.md) supplies the self-contained scalar-characteristic,
collision-uniform, Gram, optimizer and improved-geometry arguments.

From repository root, Python 3.11 standard library:
~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_collapsed_angular_review3/independent_check.py
~~~
The default command checks every field of [expected.json](expected.json):
70 exact checks, 85 rational direct-matrix profiles, six rejected
Gram-certificate mutations, and the improved coefficient. It leaves \(m\)
symbolic; finite profiles are controls. No author imports, solver, numerical
root approximation, external package or large certificate is required.
The elapsed time is diagnostic and is excluded from the fixed manifest.

For supplemental replay, obtain the adjacent author directories from this
repository, unchanged at the audited commits listed in REVIEW, and run:
~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_collapsed_angular_review3/compare_author.py \
  sendov_collapsed_angular_quartic sendov_collapsed_angular_optimizer
~~~
The comparator validates five SHA-pinned input files before loading the
author implementations, replays their manifests and all mutations, and
compares 14 generic coefficient entries using the reviewer's arithmetic.
It checks [author_comparison_expected.json](author_comparison_expected.json).
This optional author replay is not the independence argument. Later author
changes cause a pinned-source failure; retrieve the recorded versions in
a separate scratch checkout instead of weakening the hashes.

Analytic invariant-subspace, compactness and spectral-collision bridges are
ordinary written proofs, not checked by a proof-assistant kernel. The review
covers balanced fixed-angle paths at the collapsed cutoff. Inward motion,
nonlinear mean phase and the maximum-displacement basin stay separate.

Publication consists only of these compact text sources and manifests.
Source commit provenance is recorded with the graph review after the remote
source and reader-facing links have been verified.
