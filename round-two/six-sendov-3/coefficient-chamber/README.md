# Effective first power on a complex coefficient chamber

Actual author **six-sendov-3**, role **researcher**, 2026-10-02.
Complete ordinary author proof; **unformalized and independently unreviewed**.

For every $0<\eta\le2^{-16}$, set $a=1-\eta$. Suppose the complex monic
degree-nine polynomial $p(z)=z^9+\sum_{j=0}^8c_jz^j$ satisfies $p(a)=0$,
all nine originals lie in the closed unit disk, and
$|c_j|\le8\eta$ for $j=1,\ldots,8$. The constant is uncapped and is
determined by the anchor. For its eight multiplicity-counted criticals,

$$
 F=\sum_j|a-\zeta_j|^{-1}>8+2\eta.
$$

Moreover $F\le8+3\eta$ implies $H=\sum_j|\zeta_j|^2<30\eta$ and

$$
 |c_j|<\frac9j\binom8{9-j}(15\eta/4)^{(9-j)/2}.
$$

This $H$ is energy about zero, rather than distance to a comparison
critical multiset. Arbitrary complex coefficients, critical collisions
and the cyclic example with all criticals zero are included. Original
simplicity and critical localization are proved. Rotation covers any
marked root of modulus $1-\eta$.

The region contains the actual covered comparison branch from
[9113](../validated-boundary-branch/PROOF.md), confirmed in its scope by
[9174](../../six-reviewer-3/certified-branch-audit/REVIEW.md), and a physical
open neighborhood of $z^9-a^9$. The branch is an optional scope comparison;
the main inequalities have a self-contained proof.
[9492](../../six-sendov-1/coefficient-chamber-sharp/PROOF.md) already proves
a stronger exclusion on the smaller $2\eta$ chamber without original-disk
or anchor assumptions. No new smaller-chamber claim is made here.

Read [PROOF.md](PROOF.md) for the complete argument and
[LITERATURE.md](LITERATURE.md) for prior roles. The decisive constraint
averages two independently existing cube-root originals, cancels $c_6,c_3$,
and bounds the actual half-normal error by $1728\eta^2$.
The marked logarithmic derivative gives a coarse energy bound; the entire
reciprocal tail and three finite substitutions improve it to $30\eta$.

From the repository root, CPython 3.11.2 standard library only:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-3/coefficient-chamber/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-3/coefficient-chamber/verify.py
```

Both runs compare the complete typed canonical [expected.json](expected.json),
not just counts. There are 11 identity records, including the full eight-row
cube-root table, and 45 whole-domain scalar margins (29 core and 16 optional
branch-context margins). Twelve mathematical changes must reject. Missing,
malformed, altered, duplicate-key, nonfinite and boolean/integer-confused
fixtures also fail under optimized Python; [VALIDATION.json](VALIDATION.json)
records all 16 external rejections and actual serial resource use.
Sparse polynomial identities compare every coefficient; no polynomial
evaluation grid, floating sign or sampled root enters the checker.
The canonical record SHA256 is
`e873cdfa8e4cef69b183209b8ee6a5653c538961e32c620638a83c04daec23a7`.

The executable corroborates finite algebra and budgets. Rouché root counting,
Taylor remainders, actual disk normals, Maclaurin, the entire Legendre tail,
Cauchy and the positive-divisor bootstrap remain ordinary written mathematics
outside a formal kernel. It imports no earlier checker or numerical fixture.
Optional branch comparisons inherit only the explicitly listed old cover;
see [dependencies.json](dependencies.json).

All-competitor coverage outside this chamber, global branch optimality and the
unrestricted first-power conjecture remain open. A legal comparison branch
or the present coefficient estimate supplies no global chamber-entry theorem.
