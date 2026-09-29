# A necessary square of five for minimum-eight coverings on prime support 2, 3, 5

Actual authoring agent: **six-covering-3**. Role: **researcher**.
Status: exact computer-assisted theorem. The full alternate audit below is
by the same researcher; no independent review or formalization is asserted.

**Theorem.** There is no finite covering of all integers by congruences with
pairwise distinct moduli, all at least eight, drawn from

\[
\mathcal S=\{2^a3^b5^c:a,b\geq0,\ c\in\{0,1\}\}.
\]

Both exponents `a` and `b` are unrestricted. Their ordering is irrelevant.
In particular, an exactly-eight covering with LCM `2^a*3^b*5^c` must have
`c>=2`. Every finite distinct covering using the displayed support has
minimum modulus at most six: seven is absent from the support, and all
larger possible minima have just been excluded.

The theorem is a restricted-support classification, rather than a new
unrestricted numerical bound for `L_min(8)`. Finite coverings are essential
to the equality argument. No nonexistence of infinite coverings is claimed.

## Weighted capacity and all finite continuations

Fix a positive base period `Q`. Place some distinct permitted anchor
congruences with moduli dividing `Q`, and let `U` be their uncovered set in
`Z/QZ`. For nonnegative weights `w_x` supported on `U`, set

\[
D=\sum_{x\bmod Q}w_x,
\qquad C_g(w)=\max_{r\bmod g}\sum_{x\equiv r\pmod g}w_x
\quad(g\mid Q).
\]

Consider any finite proposed completion, and take `L` to be the LCM of
`Q` and all its moduli. Lift `w` periodically to `Z/LZ`. Its total weight is
`(L/Q)D`. If a remaining congruence has modulus `n`, write `g=gcd(Q,n)`.
CRT shows that its maximum possible weight is exactly

\[
\frac{L}{\operatorname{lcm}(Q,n)}C_g(w)
 =\frac LQ\frac gn C_g(w).
\]

Indeed, each compatible base residue has `L/lcm(Q,n)` lifts in that class,
and an arbitrary phase modulo `g` can be realized by a phase modulo `n`.
The union bound and the fact that each modulus is used at most once give
the necessary condition

\[
D\leq\sum_{n\ \text{chosen in the completion}}\frac{\gcd(Q,n)}n
                C_{\gcd(Q,n)}(w).                                      \tag{1}
\]

This is valid for overlapping anchors, omitted permitted moduli and
arbitrary phases of every future congruence.

More generally, suppose the full remaining permitted modulus set is infinite
and its geometric capacity sum converges. Define

\[
K_g=\sum_{\substack{n\text{ remaining and permitted}\\\gcd(Q,n)=g}}g/n.
\]

If `D>0`, then every `C_g(w)>0`. A finite subset omits a strictly positive
term of the convergent sum. Therefore

\[
\boxed{\quad D\geq\sum_{g\mid Q}K_gC_g(w),\quad D>0
       \quad\Longrightarrow\quad\text{no finite completion}.\quad}       \tag{2}
\]

Equality is safe in (2), although a finite-resource weighted union bound
requires a strict inequality. This proves a reusable weighted extension
of the one-tail capacity lemma cited below, without a finite exponent cap.

## Exact two-tail coefficients at period 360

Set `Q=360=2^3*3^2*5`. For `g=2^i*3^j*5^c`, with
`0<=i<=3`, `0<=j<=2`, and `c=0,1`, first include all moduli in `S`,
including ineligible small ones. The grouped coefficient is

\[
\lambda_g=
\begin{cases}2&i=3,\\1&i<3\end{cases}
\ \cdot\
\begin{cases}3/2&j=2,\\1&j<2.\end{cases}                              \tag{3}
\]

For an unsaturated prime exponent there is a unique possible exponent in
the modulus. At the binary boundary the sum is
`sum_{a>=3} 2^(3-a)=2`; at the ternary boundary it is
`sum_{b>=2} 3^(2-b)=3/2`. The two factors multiply, and the fixed exponent
of five contributes one. Thus (3) includes all binary and ternary tails,
including moduli beyond every finite LCM.

Remove the ineligible moduli `1,2,3,4,5,6`, each by subtracting one from
its coefficient. There is no modulus seven in `S`. Remove each placed
anchor modulus in the same way. These moduli all divide `Q`, so their
individual term `g/n` is exactly one. All coefficients remain nonnegative.
Write `k_g=2*K_g`; they are nonnegative integers. The precise certificate
test is

\[
2D\ \geq\ \sum_{g\mid360} k_gC_g(w),\qquad D>0.                       \tag{4}
\]

Zero coefficients are dropped. Unassigned anchors are always retained in
the capacity sum. At `g=Q`, the coefficient is six at every tested prefix.
If `w` is nonzero, `C_Q(w)>0`; an omitted modulus `Q*2^t` supplies an
explicit positive missing tail term for any finite proposed completion.
This also gives a direct proof of every equality cut in this computation.

## Complete anchor reduction

Use the seven anchor moduli

    8, 9, 10, 12, 15, 18, 20.

A hypothetical covering can be completed by inserting any missing anchor
modulus with any phase. This preserves coverage, distinctness and the
support condition, and makes the new base period divide the lifted LCM.
It therefore suffices to exclude every assignment of these seven phases.

In each CRT prime-power coordinate, write digits from least to most
significant. Independently permuting the children at any prefix-tree node
preserves every prime-prefix cylinder. The product of these automorphisms
maps each congruence to one with the same modulus. A finite-depth action
extends to every greater binary or ternary depth; hence it maps future
permitted congruences as well as the anchors.

While inserting the anchors in the displayed order, name children `0,1,...`
in first-appearance order at every node. For a node with `t` children
already seen, the next digit may be an existing label below `t` or the next
label `t`, if `t<p`. Any original phase assignment has such a normalized
image: process its digits and extend each partial child naming to a
permutation. Consequently the canonical search covers every possible
assignment and continuation. This argument includes omitted original
anchors, arbitrary residues and arbitrarily large future exponents.

At every node the checker first tries the uniform vector `w=1_U`. If (4)
fails and the prefix has a stored certificate, it expands and checks that
integer vector at every literal residue modulo 360. Otherwise it expands
every canonical child. Reaching an uncovered terminal prefix without a
certificate raises an error. A prefix which already covers also raises an
error, since it would contradict the theorem. Unused certificates, node
limits and time limits are rejected; they never count as successful proofs.

## Complete computation and certificate format

The verified canonical tree is:

| Number of assigned anchors | Nodes | Uniform cuts | Weighted cuts |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 2 | 1 | 0 | 0 |
| 3 | 2 | 0 | 0 |
| 4 | 12 | 1 | 0 |
| 5 | 56 | 32 | 18 |
| 6 | 48 | 19 | 20 |
| 7 | 87 | 46 | 41 |

There are **208 nodes, 177 terminal cuts, and zero uncut leaves**.
Ninety-eight cuts are uniform and 79 use stored integer weights. Thirteen
terminal inequalities are equalities, justified by the finite-tail argument.

`weights.json` contains 79 pairs `[prefix_residues, boxes]`. A box is
`[binary_mask, ternary_mask, five_mask, positive_integer_weight]` on the
Cartesian CRT axes of lengths `8,9,5`. Bit `a` of an axis mask selects
coordinate residue `a`. Its weight is assigned to every point in the
Cartesian product. Boxes must be nonempty and disjoint. Unlisted points
have weight zero. The 1,790 boxes occupy **25,717 bytes**. The largest
integer weight is 571. The literal checker does not assume the boxes are
orbits, or trust the algorithm which found them.

Certificate SHA-256:

    fd4ae03544cd0d6f460354c460dd43ff337430945ed044bee97117106f6ab8ad

Ordered complete proof-event SHA-256:

    ed9776ac055fdfbb8ddd1b11d6623fbd27308f2f83703deda6198bf0de7db3de

`expected.json` records every node/cut count, exact status and both hashes.

## Discovery and validation boundaries

The optional discovery LP uses nonnegative per-point orbit weights `t_O`
and nonnegative phase capacities `y_g`, with normalization
`sum_O |O|t_O=1` and phase rows
`sum_{O projecting to R} (|O|/|R|)t_O <= y_g`.
It minimizes `sum_g (k_g/2)y_g`. The marked-prefix stabilizer fixes each
placed class. Group averaging cannot increase a nonnegative sum of convex
phase maxima, so six-covering-2's published quotient applies unchanged.
This lossless quotient is useful for discovery; its correctness and numerical
optimality are not needed to trust a literally checked weight vector.

`generate.py` imports that researcher's public `orbits.py`, calls SciPy's
HiGHS LP interface with exactly one thread and a two-second per-LP limit,
rounds candidate orbit weights at increasing integer scales, and checks
every candidate exactly before storing it. The complete regeneration used
94 LP calls and reproduced the certificate bytes and proof-event hash.
Floating infeasibility, failed reconstruction or timeout only causes more
branching. None is a mathematical exclusion. Generation itself fails if
its complete frontier cannot be closed within its declared limits.

The standard-library `check.py` expands boxes by scanning literal residues
and testing coordinate bits. It computes every capacity by direct integer
population arrays. The separate `audit.py` uses Cartesian products and
CRT inversion to decode boxes, set-based class removal, arithmetic
progression sums, and normalization of complete original phase tuples.
It calls none of the production symmetry, box decoding, resource or phase
counter routines in its complete replay. Every manifest field and every
ordered proof event agrees.

Additional controls check all normalized assignments for four small modulus
tuples; 216 finite grouped coefficient identities; 1,332 individual CRT
capacity identities by scanning full lifted periods; 64 grouped finite
capacities; and 52 strict finite exclusions corresponding to the 13 infinite
equalities. Five prefixes of a genuine positive covering survive the
general weighted rule. Eight malformed-data or operational-limit controls
are rejected. These are self-audits, rather than external review.

The remaining trust boundary is exact ordinary Python execution and the
unformalized CRT, union-bound, completion, tree-symmetry and convergent-series
arguments. No solver status, external nonexistence certificate, finite
exponent bound, or published minimum-seven lower bound is assumed.

## Literature, dependencies and unresolved scope

[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644),
Problem 3, asks for the minimum-eight classification at LCM `2^a*3^b*5^c`,
with ordered positive exponents. The theorem excludes its entire `c=1`
slice without needing the ordering. Their Theorem 1.8(vi),(viii) gives
finite minimum-six examples with `c=1`, so the new minimum-six upper bound
for this support is sharp using their existing constructions. Their
Theorem 1.11 constructs a minimum-eight cover at 172800 with `c=2`.
[Zhang–Zhang](https://arxiv.org/html/2607.19029) claims `L_min(7)=10080`;
its solver exclusions are not dependencies here. These primary sources and
targeted current literature searches were refreshed on 2026-09-29. The
specific all-exponents `c<=1` exclusion was absent from the sources and
committed graph inspected. No exhaustive priority claim is made.

The proof combines and builds on these team artifacts, with actual roles
identified because their graph signatures share an identity:

- **six-covering-2, researcher:** [weighted residual obstruction and lossless
  stabilizer quotient](../distinct_covering_residual_weight_duals/proof.md),
  source `b9d39eb740a866e07237be1c78b834d1ab6ea718`, graph
  `bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4`.
  Optional generation reuses its attributed `orbits.py` directly.
- **six-covering-3, researcher:** [one-tail exact capacity exclusion](../distinct_covering_min8_tower_capacity/proof.md),
  source `a61c23f3b30dbbeb7dea8543b5df2f8cf0cd3e1c`, graph
  `bafkreidmchwpbqsq2cuvwku6topbsamxk2iu5jb5226xqc3jqjhdvggthm`.
  The new weighted two-tail argument removes its ternary-exponent restriction.
- **six-covering-3, researcher:** [residual-state/tree-symmetry framework](../distinct_covering_prime_tower/README.md),
  source `afaabb5d6222b09be0977c3884714a5cf2e60c47`, graph
  `bafkreiadl5p7tzrjxfj5dzkkfp5om2fhr5fztv4k6all56vzq4cjta5eqa`.
- Current unrestricted interval context only: **six-covering-2, researcher**,
  [10080 lower bound](../distinct_covering_min8_lower_bound/proof.md), source
  `47fdc5d58c3401f2496f8a4970fc7ef56eb6853a`, graph
  `bafkreihbmsoga46xbfhoklyxsfg3utwtcji4wkiszwrpbdffvuucffe3cy`;
  **six-covering-1, researcher**, [70560 construction](../distinct_covering_min8_prime_lift/README.md),
  source `fff90195de828ddc9a189ce9af3651ea1245e80a`, graph
  `bafkreiabb5iw2mfr7si2svpnt6tkhaodule7mkdejetbgcqpvcm55dqede`.

The unrestricted interval remains `10080 <= L_min(8) <= 70560`. The upper
construction uses prime seven and is outside the present support. The
`c>=2` classification, minimum-nine existence on full support 2,3,5, and
the exact unrestricted value of `L_min(8)` remain unresolved here.
