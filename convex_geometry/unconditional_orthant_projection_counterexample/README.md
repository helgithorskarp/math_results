# The unconditional orthant projection conjecture is false

An explicit unconditional convex body in four dimensions has a planar
orthogonal projection satisfying

$$
\frac{|P_EK|_2}{|P_E(K\cap\mathbb R_+^4)|_2}
=\frac{61}{15}>4.
$$

This refutes Conjecture 3 of
[Fradelizi–Manui–Mark Meyer–Ndiaye, arXiv:2607.03582v1](https://arxiv.org/html/2607.03582v1).
The example is the convex hull of three centered coordinate boxes:

$$
K=\operatorname{conv}\big([-1,1]^4,\,
 [-1,1]\times[-3,3]\times\{0\}^2,\,
 \{0\}^3\times[-3,3]\big),
$$

and $E$ is spanned by $(2,0,-2,1)$ and $(0,2,0,3)$.
The corresponding rank-two map has image areas $122$ and $30$.
A common area Jacobian cancels in their ratio.

The [proof](PROOF.md) also gives:

- A family with normalized ratio $(43+6t)/60$, for $17/6<t\leq3$.
- Counterexamples for every $2\leq n\leq m-2$, amplified by products.
  Together with the already known line and hyperplane cases, this
  classifies all dimension pairs.
- An explicit smooth unconditional counterexample with positive
  Gaussian curvature and a rationally certified strict margin.

The narrower $\ell_q$-ball and asymmetric $L_p$-zonoid conjectures are
not settled by this construction. The optimal replacement constant
is not determined. The result has an exact author-checked certificate;
independent review and proof-assistant formalization are not claimed.

## Reproduce

Python 3.11.2, standard library only; no installation, solver, external
data, floating-point geometry, or search run is required.
From this directory:

~~~sh
python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Both executions produce the same 2,697-byte output with SHA-256

~~~text
bff89432521d271292fbe1c7f18f9b63534ae8d230ff84f4d5b1b219f3d6e498
~~~

The verifier checks every box corner against the polygon facets,
cross-checks shoelace areas by vertical integration of the raw
generators, verifies the orthogonal projector, checks parameter
endpoints and the smoothing margin, and rejects six corrupted
certificates. The base body without the added rectangle gives equality.
Measured author runs took approximately 0.15–0.26 seconds.

Files: [proof](PROOF.md), [exact witness](WITNESS.json),
[verifier](verify.py), [expected output](EXPECTED.json),
[source and priority notes](SOURCES.md), and [hash manifest](SHA256SUMS).
The analytic bridges and precise computational trust boundary are
stated in the proof.
