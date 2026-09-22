# Orthant envelopes fail shadow convexity

We rule out a standard proposed route to the sharp planar orthant
projection bound: the largest envelope-to-body area ratio, optimized
over the origin, is **not convex under parallel chord movements**.

For the constant-area quadrilaterals

$$
Q_s=\operatorname{conv}\{(-1,0),(1,0),(s,1),(0,-1)\},
\quad 0\leq s\leq2,
$$

the optimized ratio is exactly $6-8/(s^2+2s+4)$.
At $s=0,1/2,1$ the ratios are $4,94/21,34/7$; the midpoint
exceeds the average of the endpoints by $1/21$.

The [proof](PROOF.md) derives the sharp ratio and unique best origin
for a full kite family using explicit polygon inequalities, vertex
preimages, and concavity in the origin. It also shows that the area
centroid need not be optimal.

The proposed global planar constant $16/3$ remains unresolved here.
This result closes the convexity-based reduction, and does not
rule out a weaker endpoint principle or another proof method.
Independent review is pending.

## Reproduce

CPython 3.11.2 and the standard library, from this directory:

~~~sh
python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

The checker uses exact rational arithmetic and complete vertex
enumeration of the original four-dimensional constraints.
An independent polygon-section calculation checks areas, and
polynomial interpolation certifies the displayed local area identity
with explicit degree bounds.

Normal and optimized output SHA-256: ebf3287e66d574f0718ab2127c774675678d62d11b1e4e9ff7304d411ac9f278.

Files: [proof](PROOF.md), [checker](verify.py),
[fixtures](WITNESS.json), [expected output](EXPECTED.json),
[sources and scope](SOURCES.md), [hash manifest](SHA256SUMS).
