# Exact illumination with one smooth planar factor

For a smooth convex body $K\subset\mathbb R^d$ and a smooth planar convex body
$L$, the author proof in [PROOF.md](PROOF.md) gives

$$
I(K\times L)=2d+3+(d\bmod2),\qquad d\geq1.
$$

Smooth means a unique supporting hyperplane at every boundary point. Symmetry,
strict convexity and positive curvature are unnecessary. The proof gives
explicit integer optimal directions, the same for every pair of bodies in
fixed factor coordinates. The first values, for $d=1,\ldots,6$, are
$6,7,10,11,14,15$.

An open-semicircle count gives the lower bound $2d+3$. At equality, every cyclic
$(d+1)$-block must be a positive circuit. Its consecutive determinants reverse
sign when $d$ is odd, contradicting the odd cycle length. A signed moment curve
paired with interlaced integer planar directions attains the resulting bounds.

This is a complete author proof, independently unreviewed and unformalized.
Historical priority is unresolved: the cases $d=1,2$ are classical and an
important 2007 direct-sum paper was inaccessible. [SOURCES.md](SOURCES.md)
identifies exactly what was inspected. The result concerns the $(d,2)$ family
of a broader published problem, not the full prescribed-dimensions problem or
the general illumination conjecture.

## Reproduce

Python 3.11.2 was used; only the standard library is required. From this
directory:

~~~sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
~~~

The verifier compares its complete deterministic result with
[EXPECTED.json](EXPECTED.json), prints that result, and exits zero on success.
All mathematical checks use explicit exceptions and remain active under -O.
It checks:

- Dimensions 1–16: 328 positive circuits, including every cyclic wrap.
- All 656 boundary rays and all 656 open cells of the planar normal arrangements.
- Agreement of exact rational elimination with the Lagrange circuit formula.
- Five invalid configurations, each with an exact uncovered normal pair.
- All 63 single-direction deletions in optimal constructions of dimensions 1–6,
  each with an exact uncovered normal pair.

The finite checks use arbitrary-precision integers and rational arithmetic.
They corroborate the formulas and boundary conventions; the universal proof
and optimality argument are in PROOF.md. No numerical tolerance, solver,
external certificate or downloaded data is needed.

To print the optimal integer directions in $\mathbb R^{d+2}$, for example $d=3$:

~~~sh
python3 construct.py 3
~~~

The function construct.directions(d) returns separate lists of the two factor
components. Its optional n argument is for negative controls and does not
promise coverage. The pairing uses the cyclic order displayed in the proof;
reordering just one factor changes the construction.

The full verification takes about ten seconds and about 17–21 MiB of process
memory on the originating Linux/Python environment. Reproduction timing may
vary. Bulky exploration, downloaded papers and campaign state are excluded.
