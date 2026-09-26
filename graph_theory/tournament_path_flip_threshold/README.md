# Tournament path flip threshold

The asymptotic minimum density of direction flips needed for a non-TAS path
exists. This resolves Question 6.1 in
[Chen and Lin, arXiv:2609.14655v1](https://arxiv.org/html/2609.14655v1).
Writing the limit as $\beta$, the proof also gives

$$
  \frac1{1665}\leq\beta\leq\frac12-\frac2{\pi^2}
  =0.297357632715324\ldots.
$$

The lower bound is Chen--Lin's. The upper bound and existence argument
are proved in [PROOF.md](PROOF.md), together with

$$
 \beta=\inf_{w\ \text{not TAS}}\frac{r(w)+1}{|w|},
$$

where $r(w)$ counts changes between consecutive edge directions.
The exact value of $\beta$ remains open.

The existence proof reflects and repeats an arbitrary counterexample.
The upper bound mixes consistently directed and alternating segments in
small perturbations of regular carousel tournaments.

## Exact, finite evidence

[certificate.json](certificate.json) specifies a rational weighted
tournament with 13 classes, a compressed 8000-edge word, and a positive
integer vector. Integer arithmetic verifies an amplifying matrix
inequality and all 8000 padding cases. It proves a concrete corollary:

$$
 f(n)\leq 3n/10\qquad\text{for every }n\geq240{,}000{,}000.
$$

The compressed path family and the transfer from weighted matrices to
finite tournaments are explicit in the proof. The certificate does not
claim that the unamplified 8000-edge word is already non-TAS.

From the repository root, run:

    python3 graph_theory/tournament_path_flip_threshold/verify.py
    python3 graph_theory/tournament_path_flip_threshold/audit.py

Both use only the Python standard library. They were checked with
CPython 3.11.2 and 3.12.14. Verification takes under one second on the
research host; the definition-level audit takes about one second.
The exact verifier output is [expected.json](expected.json).

Certificate SHA-256:

    12de26019b31308c2c78bcd003c575ab45f6f72a3de80a42326fa12def927baa

The verifier checks the matrix inequality by direct vector propagation
and separately by matrix powers using repeated squaring. Both round down
with arbitrary-precision integers. The audit compares transfer counts
against direct enumeration of vertex maps, checks reflection and flip
counts, verifies the perturbation's polynomial identities exactly, and
rejects damaged certificates.

## Scope and trust

The limit theorem and the sharper analytic bound rest on the written
proof, using the spectral theorem, Perron--Frobenius theory and the
implicit function theorem. The finite certificate is an additional
computer-assisted result; it does not by itself prove the sharper bound.
The checker trusts Python's integer arithmetic and the inspected source.
There are no solver certificates, floating-point assumptions, external
datasets, or omitted large artifacts in verification.

NumPy was used only to discover the rational example. Neither a numerical
eigenvalue nor search completeness is used as proof. This work has not
been formally verified or independently peer reviewed. The claim of
novelty is limited to the targeted primary-source and Discovery Net search
on 26 September 2026; see [LITERATURE.md](LITERATURE.md).
