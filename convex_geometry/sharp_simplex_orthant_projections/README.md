# Sharp simplex projections of unconditional bodies

We determine the largest possible ratio

$$
\frac{|P_EK|_n}{|P_E(K\cap\mathbb R_+^m)|_n}
$$

when $K$ is unconditional and its positive projection is a simplex.
The ambient dimension may vary. The unique maximizing placement of
the origin is the simplex barycenter for every $n\geq2$.

The sharp constants satisfy

$$
C_1=2,\qquad C_2=\frac{16}{3},\qquad C_3=\frac{127}{8},\qquad
\lim C_n^{1/n}=\frac{2}{r^2}e^{r-1}\approx3.573712,
\quad r=\frac{\sqrt5-1}{2}.
$$

The [proof](PROOF.md) gives an explicit central-section formula for
every $C_n$, rational upper and lower bounds within a factor $n+1$,
and exact finite realization by coordinate boxes.
For a positive triangle with origin barycentric coordinates $c_i$,
the sharp ratio is $6-2\sum_i c_i^2$. A nine-dimensional example
attains $16/3$ with image areas $72$ and $27/2$.

The main structural step is the exact envelope
$\mathcal E(Q)=\{x-y:x,y,x+y\in Q\}$: every full projection is contained
in this set, and every polytopal $Q$ admits a lift attaining it.
This leads to strict concavity in the simplex placement.

These are sharp results for simplex positive images. The global
constant for arbitrary positive images, minimum ambient dimension,
and the narrower $\ell_q$-ball/zonoid conjectures are not determined.
Independent review is pending; no proof-assistant formalization is claimed.

## Reproduce

CPython 3.11.2 and the standard library; no solver, external input,
floating-point geometry, or package installation.
From this directory:

~~~sh
python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

The identical normal/optimized output has SHA-256

~~~text
c6eb381243618683184ad71e8d30d5abd9d78116c86a807685a9bf37cdbffe99
~~~

Checks include the coordinate-box lift and its orthogonal projector,
28 rational triangle placements using two different polyhedral
descriptions, and the three-dimensional constant using both facet
tetrahedra and exact integration of polygonal sections. Seven malformed
controls are rejected. The continuum extremal and asymptotic theorems
are established by the written proof, not by finite sampling.

Files: [proof](PROOF.md), [witness](WITNESS.json),
[verifier](verify.py), [expected output](EXPECTED.json),
[sources and scope](SOURCES.md), [hash manifest](SHA256SUMS).
