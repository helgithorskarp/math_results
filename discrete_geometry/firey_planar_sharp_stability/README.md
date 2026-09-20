# Sharp planar Firey area stability

For a centrally symmetric planar convex body \(K=C+x\) containing zero,
let \(M\) be the largest area of an inscribed parallelogram with opposite
vertices \(0,2x\). For every \(1<p<\infty\), we prove

\[
(2+c_q)|K|-|K+_p(-K)|\ge
\bigl(2+c_q-2^{2/p}\bigr)(|K|-M),
\quad q=p/(p-1),\quad
c_q=\frac{2\Gamma(1+1/q)^2}{\Gamma(1+2/q)}.
\]

This gives a sharp linear bound on relative area lost to an inscribed
origin-vertex parallelogram, uniformly over all such bodies, including
nonsmooth ones. The coefficient is attained by a continuous hexagon family
converging to the original extremizers. The proof classifies every equality
case and yields the sharp lower hexagon deficit constant for all \(p>1\).
It strengthens an existing planar inequality and equality classification;
the earlier upper hexagon stability constant is explicitly credited.

Read [PROOF.md](PROOF.md) for the full statement, the support-function
transform, its smooth-to-general justification, and the prior-work boundary.
This is an unformalized analytic and geometric proof. It has not received
independent review at initial publication.

## Reproduction

Tested with CPython 3.11.2 and mpmath 1.3.0. From this directory, use an
environment outside the repository:

```sh
python3 -m venv /tmp/firey-stability-venv
/tmp/firey-stability-venv/bin/pip install -r requirements.txt
/tmp/firey-stability-venv/bin/python verify.py --check
sha256sum -c SHA256SUMS
```

Run ordinary Python, without `-O`, because the checker uses assertions.
The script reads only the adjacent [EXPECTED.json](EXPECTED.json) when
`--check` is used, makes no network requests, and writes its result to stdout.
Omit `--check` to regenerate the JSON independently of the expected file.
The recorded replay took 45.5 seconds and about 34 MB maximum resident memory.

The compact check set contains:

* 55 polygon/parameter cases comparing direct integration of the original
  Firey support function with the new surface-measure formula;
* exact rational areas, maximizers and containment of comparison
  parallelograms, plus 33 exact invertible-linear transformation checks;
* 15 hexagon deficit formula checks, three nonpolygonal disk/ellipse
  controls, endpoint beta-integral checks, and three rejected invalid inputs.

The parameters are \(p=5/4,3/2,2,3,6\). Polygon fixtures cover the complete
equality family's endpoints and two interior parameters, unbalanced
hexagons, octagons with boundary/interior/central translations, and a
strict square example with the origin away from an edge midpoint.

Geometry uses `fractions.Fraction`. Numerical quadrature uses 50 decimal
digits and a comparison threshold of \(10^{-28}\); this is **not** an
interval enclosure or a certified error bound. Numerical checks corroborate
the proof and do not establish a universal theorem. Expected values are
rounded to 18 significant digits for stable compact output.

## Scope and stopping point

The theorem concerns two-dimensional Lebesgue area, finite \(p>1\), full
dimensional convex bodies, and a fixed distinguished origin. It makes no
claim about higher dimensions or a stronger metric such as Hausdorff or
Banach--Mazur distance. When the body's center is zero, the comparison
parallelogram is degenerate and the area statement remains valid.

The graph's reviewed uniform-stability gap is closed by the stated theorem,
subject to review. Further work should begin with a concrete objection or
a separately specified structural question, rather than parameter tables.
