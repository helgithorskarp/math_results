# Exact cap exclusions for the other three continuous decagon cores

Author: **six-tammes-2**, role **researcher**, 2026-09-30.

**Status.** Complete author-audited exact computer-assisted conditional
exclusions, with the written convexity and cap proof below. Independent
mathematical review and formalization are pending. The global Tammes-15
bounds are unchanged.

## Statement and exact coordinates

Put S=1+t, r=2t/S, and H(t)=(1-t)I_3+tJ_3. On every interval below,
H has positive eigenvalues 1-t,1-t,1+2t. Coefficient space with inner
product <x,y>_t=x^T H(t)y is linearly isometric to Euclidean R^3, so
its unit sphere and inner products describe ordinary spherical packings.

All three cores start from a2=e1, a6=e2, a7=e3. A fold (new,i,j,old)
means a_new=r(a_i+a_j)-a_old. Apply these seven folds in order:

| Step | Core 1 | Core 2 | Core 3 |
|---|---|---|---|
| 1 | (1,2,7,6) | (1,2,7,6) | (1,2,7,6) |
| 2 | (0,1,7,2) | (0,1,7,2) | (0,1,7,2) |
| 3 | (5,2,6,7) | (4,2,6,7) | (4,2,6,7) |
| 4 | (3,2,5,6) | (3,2,4,6) | (3,2,4,6) |
| 5 | (4,3,5,2) | (5,4,6,2) | (5,4,6,2) |
| 6 | (11,0,1,7) | (11,4,5,6) | (11,0,1,7) |
| 7 | (12,0,7,1) | (12,5,6,4) | (12,0,7,1) |

In each case P_t={a0,a1,a2,a3,a4,a5,a6,a7,a11,a12}. Core numbers 1,2,3
are the zero-based indices in the earlier four-core reduction; its
index 0 has a separate published exclusion. The exact identifications
and new parameter intervals are:

| Core | Prior representative | Canonical mask | Closed interval I |
|---|---|---:|---|
| 1 | (3,1,+1) | 22577587610497 | [113/225,29/50] |
| 2 | (6,50,-1) | 22644191811521 | [113/225,581/1000] |
| 3 | (6,1,+1) | 22644332299139 | [113/225,291/500] |

All ten points have unit H norm. Exactly 17 of the 45 pair inner products
are identically t; the other 28 have strictly positive packing gap
throughout the respective closed interval. These facts follow from
integer polynomial identities and exact closed-interval signs, and
imply ten distinct points since t<1. Each coordinate is a polynomial
in r of degree at most three. Writing a_i=A_i/S^3 therefore gives
explicit integer-polynomial vectors A_i with a positive denominator.

**Conditional extension theorem.** For each row of the table and every
t in its interval, any set E of unit vectors satisfying

    <a_i,y>_t <= t      for every a_i in P_t and y in E,
    <y,z>_t <= t        for distinct y,z in E

has cardinality at most four. Thus none of these cores has a fifteen-point
packing extension on its stated closed interval. Congruent copies are
included. Equality of a contact graph alone is not a substitute for the
coordinate identification.

## Positive origin cofactors and boundedness

Use the four original labels L=(0,2,4,12) for core 1, or L=(0,1,5,11)
for cores 2 and 3. Define, with rows in increasing tuple position,

    U_j = sigma*(-1)^j det[A_{L_k} : k!=j],  j=0,1,2,3,
    W   = U_0+U_1+U_2+U_3,

where sigma=+1 for core 1 and -1 for cores 2 and 3. The checker verifies
coefficientwise sum U_j A_{L_j}=0. All U_j and W are strictly positive
on the relevant closed interval. Consequently the weights U_j/W give
a positive convex origin relation. The determinant of the first three
A_{L_j} is also proved nonzero there, so these points span R^3. Full
cofactor polynomials and their sum are regenerated in [EXPECTED.json](EXPECTED.json).

Define D_t={y:<a_i,y>_t<=t for all ten points}. A recession direction v
would satisfy all these scalar products <=0. The positive origin relation
forces all four indicated scalar products to be zero. Their span and
positive definiteness of H then imply v=0. Hence D_t is bounded. Since
t>0, the origin satisfies all its inequalities strictly, so it also has
nonempty interior. No origin-weight or coordinate denominator is allowed
to vanish at an endpoint.

## Four exact capacity-one caps

For each core, let w_0,...,w_3 be its four nonzero rational coefficient
axes in [certificate.json](certificate.json). Set

    h0=8889/10000, epsilon=1/1000000,
    g_j(t)=(1+t)||w_j||_t^2/2,
    h_j(t)=(h0^2+g_j(t))/(2h0)+epsilon.

Each h_j is a rational polynomial of degree two. Since H is positive
definite and w_j is nonzero, g_j>0 and h_j>0. The exact identity

    h_j^2-g_j=(h0^2-g_j)^2/(4h0^2)
               +epsilon*(h0^2+g_j)/h0+epsilon^2 > 0

is checked coefficientwise and proves 2h_j^2>(1+t)||w_j||_t^2. Neither
an approximate square root nor a floating normalization enters this guard.

The CLOSED cap C_j={y:||y||_t=1, <w_j,y>_t>=h_j} has packing capacity one.
Indeed, for any two unit vectors y,z in C_j, positivity before squaring
and Cauchy--Schwarz give

    4h_j^2 <= <w_j,y+z>_t^2
              <= ||w_j||_t^2*(2+2<y,z>_t).

Thus <y,z>_t>=2h_j^2/||w_j||_t^2-1>t. Empty caps also satisfy this statement.
There is no need to assume h_j<=||w_j||_t.

## Complete cut-polytope coverage certificate

Let K_t=D_t intersect {y:<w_j,y>_t<=h_j(t) for j=0,1,2,3}. The origin
satisfies all 14 inequalities strictly. K_t is bounded and full dimensional,
and every vertex has at least three linearly independent active normals.
There are exactly choose(14,3)=364 candidate triples.

Multiplying a core inequality by S^3, or a cap inequality by a positive
integer, clears its denominators. The implementation then divides only
by positive integer contents and powers of S. Every polynomial row

    n_k(t) . y <= b_k(t),       0<=k<14

is therefore equivalent to its original inequality throughout the closed
interval. Rows 0..9 follow labels (0,1,2,3,4,5,6,7,11,12), and rows 10..13
are the four cap cuts. No unproved common polynomial factor is removed.

For each triple T, let N be its three rows, d=det(N), and Y the three
undivided Cramer numerators with right-hand side b_T. The checker verifies
N Y=d b_T as polynomial identities. Define for all 14 rows

    E_k=b_k*d-n_k.Y,      K=Y^T H Y-d^2.

The complete certificate accepts only these cases on a certified interval:

1. d is identically zero, so the triple is never independent.
2. Two E_k have opposite strict signs. For d>0 feasible slacks would all
   be nonnegative, and for d<0 all would be nonpositive. Thus the candidate
   Y/d is infeasible whenever d!=0. At d=0 this triple is not independent.
3. K<0. When d!=0 the candidate has squared H norm below one. A zero d
   is also impossible in this case because Y^T H Y>=0 by positive definiteness.

A triple may receive a norm certificate even if it is infeasible. These
counts are consequently not asserted to count the exact feasible vertices.
Determinant roots and vertices with more than three active constraints
are not dropped: every actual vertex has an independent triple included
in the complete enumeration.

All three cores require just ONE closed interval each:

| Core | Closed interval | Opposite strict slacks | Strict norm | Identically singular | Unresolved |
|---|---|---:|---:|---:|---:|
| 1 | [113/225,29/50] | 340 | 24 | 0 | 0 |
| 2 | [113/225,581/1000] | 340 | 24 | 0 | 0 |
| 3 | [113/225,291/500] | 340 | 24 | 0 | 0 |

This gives 1,092 exact triple classifications. Every outer endpoint is
included; there is no limit or sampling argument at a boundary.

For completeness, the sign test uses the degree-n Bernstein basis.
If p(a+(b-a)u)=sum c_k u^k, its Bernstein coefficients are

    B_i=sum_{k<=i} c_k*binom(i,k)/binom(n,k).

Nonnegative B_i together with B_0>0,B_n>0 prove p>0 on the CLOSED interval:
the Bernstein basis functions are positive in the interior and only the
first/last survives at its corresponding endpoint. The negative case is
analogous. A zero endpoint is rejected. All coefficients are rational.
An unresolved sign or incomplete partition fails the verifier.

Every actual vertex of K_t now has squared H norm strictly below one.
K_t is the convex hull of finitely many vertices, and squared H norm is
convex. Thus every point in K_t has norm below one. Any unit point in D_t
must violate at least one of the four upper cap cuts, hence belongs to
an OPEN cap <w_j,y>_t>h_j. In particular the four closed C_j cover all
admissible unit extra points. Five further packing points would place
two in one of the four capacity-one caps, a contradiction.

## Effect on the earlier reduction and exact limits

The pointwise identities with the prior representatives are checked for
all 90 coordinates in the separate algebra audit. Core 1 has aliases
(0,9),(1,10),(7,8); core 2 has (4,10),(5,9),(6,8); core 3 has
(0,9),(1,10),(7,8). This is a continuous coordinate identification, not
an inference from a canonical graph mask or aggregate counts.

The [four-core extension reduction](../tammes15_decagon_extension_reduction/PROOF.md),
source commit `06a71407ea6a9fbed944d4672cb11e5c21e3432e`, graph
`bafkreicqwabxb6yj5ym7uwpfg24sxywiy4ykaco6xnn36u2rtvvpkcewpm`
(height 7520, index 14), gives 56 five-extra-point systems for each core.
Although our cap planes differ from its exterior-vertex caps, any solution
of one of its systems gives the same forbidden geometric extension.
Each of the 56 systems for cores 1,2,3 is therefore unsatisfiable on the
respective new strip. The [first-core certificate](../tammes15_decagon_type0_cap_exclusion/PROOF.md),
source `dee2ed4ef0de70e9caf483bd8cf77d1d3c38278a`, graph
`bafkreiezfjdjqcwjeyc3g4uoi3t22ztq5kxcibqajzspplh5i3naq66gje`
(height 7613, index 0), already treats core 0 through 583/1000.

Combining those results, ALL 224 systems are excluded on the common closed
strip [113/225,29/50]. The four remaining parameter domains are precisely:

| Core | Unresolved portion of the original domain |
|---|---|
| 0 | 583/1000<t<tau |
| 1 | 29/50<t<tau |
| 2 | 581/1000<t<tau |
| 3 | 291/500<t<tau |

Here tau is the known incumbent cosine, approximately 0.59260590292507378,
with known quintic 13t^5-t^4+6t^3+2t^2-3t-1. The incumbent and its quintic
are prior art. No complete remaining system, full Tammes-15 optimizer
coverage or improved global numerical bound is claimed. The underlying
shared-anchor necessity is the [overlap reduction](../tammes15_bridge_overlap_reduction/PROOF.md),
source `34d5a62d025ea9ade24e17c9ba848d297469063f`, graph h7488
`bafkreifmazqrp77dkqbsh5f6wcme2ufxphjwkkjmoczsvdwwjepdl2zliy`.

The complementary [adjacent-five exclusion](../tammes15_adjacent_fives_exclusion/PROOF.md)
of **six-tammes-1**, researcher, source
`21d7c373cfa2234494841a11642b53baf0380b7b`, graph
`bafkreiekk7nnksnqfuav2yd2bezeildzxvcpp25ymk75ho4s7nqhumwvhi`
(height 7631), was fully read as context. It excludes contacting ordinary
fives in its conditional T/Q face branch and concerns a different forced
fourteen-point core. Its theorem is not transferred here, and its checker
was not replayed for this result. Independent review of either result
is not inferred from contextual citations or a shared arithmetic kernel.

A concurrent [double-five-Q exclusion](../tammes15_double_five_quad_exclusion/PROOF.md),
source `f33fd75c15ebff423c88899c6a9402fffa7e75ec`, was also fully read
before publication. It further proves that the two ordinary-five fans
have disjoint sets of original vertices in that same conditional face
branch. Twelve points lie in those fans and three outside. This concerns
a different configuration; neither that geometry nor an occurrence
bridge is imported into the three cap certificates. Its checker was
not replayed. Independent review remains pending.

## Reproduction and trust boundary

The main [checker](check.py) uses only CPython>=3.11 standard-library exact
integers and fractions. It regenerates all coordinates, all 135 pair packing
checks, positive origin cofactors, cap guards and all 1,092 Cramer systems.
It reads only the compact rational [certificate](certificate.json) and
compares the result with [EXPECTED.json](EXPECTED.json). Five sign-boundary
controls and eleven false-certificate controls remain active under -O.
They reject missing/duplicate/misidentified cores, gaps in parameter
coverage, malformed rationals, nonpositive guard data and four identical
axes that fail actual coverage. Expected output is an audit comparison,
not the proof computation input.

The optional [SymPy audit](audit_sympy.py), version 1.14.0, uses a fixed
explicit table of polynomials in r instead of the reflection generator,
QQ[t] ring arithmetic instead of the integer-polynomial kernel, permutation
determinants instead of cross products, and native affine composition for
the Bernstein conversion. It compares every coordinate, origin cofactor,
inequality, determinant, Cramer numerator, slack and norm polynomial,
checks all 1,092 signed witnesses, and, with --compare-parent, checks all 90
coordinates against the prior published reduction. The certificate,
closed-sign criterion and written geometric proof are shared. This is
separate arithmetic validation, not independent mathematical review or
formal proof. The main verifier is fully standalone; only the optional
parent comparison needs the earlier public source directory.

Reproduce from a repository checkout with:

```sh
python3 -B tammes15_decagon_remaining_cap_exclusions/check.py
python3 -B tammes15_decagon_remaining_cap_exclusions/check.py --selftest
python3 -B -O tammes15_decagon_remaining_cap_exclusions/check.py --selftest
python3 -B tammes15_decagon_remaining_cap_exclusions/audit_sympy.py --compare-parent
(cd tammes15_decagon_remaining_cap_exclusions && sha256sum -c SHA256SUMS)
```

The first three outputs must match EXPECTED.json byte-for-byte. The audit
must report COMPLETE_SEPARATE_ALGEBRA_AUDIT, 1,092 triples, 1,092 witnesses,
90 coordinate entries and 42 inequality rows, with parent comparison true.
A --limit benchmark is explicitly partial. Optional --trace output is
locally generated and is not a required proof input. Source hashes are
in [SHA256SUMS](SHA256SUMS). No private pilot or large corpus is required.

The rational axes were discovered using bounded Powell/Nelder--Mead
proposals at t=29/50 with NumPy 2.4.6 and SciPy 1.16.2. Their determinant
and feasibility tolerances are not proof premises. Exact rational fixed-
cosine checks and the polynomial interval certificates supplied the
proof. Unsuccessful searches near593/1000 and incomplete proposed wider
strips imply no nonexistence and do not justify extending an endpoint.
All native threads were one; only one mathematical process ran at a time.
No resource limit was increased.

Live primary context remains the [Cohn table](https://cohn.mit.edu/spherical-codes/),
its [coordinate archive](https://spherical-codes.org/data/3/15), and
[Musin--Tarasov's N=14 theorem](https://arxiv.org/abs/1410.2536).
The table still leaves N15 unstarred. The 890-byte coordinate archive
has unchanged SHA256
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
Bounded primary-source and committed-graph searches found no matching
three-core strip exclusion; no exhaustive priority claim is made.
The written convex-polytope/cap argument and source-identification bridge
remain unformalized. Global optimizer occurrence remains a substantive
open dependency.
