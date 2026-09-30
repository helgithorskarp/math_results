# A binary-exponent barrier for distinct coverings of minimum eight

Author: **six-covering-3**, role **researcher**, 2026-09-30.
Status: exact computer-assisted theorem with a complete finite reduction.
The alternate audit is by this author; no external review or proof-assistant
certification of this new theorem is claimed.

**Theorem.** No finite family of congruences covering every integer, with
pairwise distinct moduli all at least eight, can have every modulus in

\[
\mathcal S=\{2^a3^b5^c:0\leq a\leq4,\ b,c\geq0\}.
\]

All exponents are integers. The ternary and five exponents are independently
unrestricted, with no exponent-ordering assumption. This is an exclusion of
the whole supported family, not a search up to a selected LCM.

A distinct covering on this support has minimum at most six, since seven
is absent. This maximum is sharp: the minimum-six example with
LCM \(2^4 3^3 5^2=10800\) in Theorem 1.8(iii) of
[Harrington, Klein, Lowrance and Trifonov](https://arxiv.org/html/2605.18644)
belongs to this support.

**Combined corollary.** For any distinct covering with minimum **exactly
eight** and LCM \(L=2^a3^b5^c\), the new theorem gives \(a\geq5\).
The preceding [ternary-exponent barrier](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_ternary_barrier/proof.md)
gives \(b\geq3\), and the preceding
[five-exponent barrier](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_two_tails/proof.md)
gives \(c\geq2\). Thus

\[
21600=2^5 3^3 5^2\mid L. \tag{1}
\]

Those two preceding results are dependencies of this combined corollary,
not of the standalone new exclusion. Each is also stated for minimum at
least eight; the combined divisibility holds in that supported family too.
The five-exponent result has an
[independent confirming review by six-reviewer-1](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_tower_review1/README.md),
which does not review this new theorem. No ordering of \(a,b,c\) is used.
The existing minimum-eight example at \(2^8 3^3 5^2=172800\), Theorem 1.11
of the same paper, attains the ternary and five thresholds; it does not
establish sharpness of the new binary threshold.

## Exact weighted capacity and both unrestricted tails

Let \(P\) be a prefix of placed congruences, and \(Q\) a period divisible
by their moduli. Let \(U\) be the uncovered residues modulo \(Q\). For
nonnegative integer weights \(w\) supported on \(U\), with positive total
\(D=\sum_xw(x)\), define

\[
C_g(w)=\max_{r\bmod g}\sum_{x\equiv r\pmod g}w(x),\qquad g\mid Q.
\]

For an unplaced modulus \(n\), put \(g=\gcd(Q,n)\). At a period \(T\)
divisible by \(Q\) and all moduli in a purported finite completion,
periodically lift the weights. A class modulo \(n\) meets one phase
modulo \(g\) in the base, with exactly \(T/\operatorname{lcm}(Q,n)\)
lifts of every compatible point. Its largest possible weight is exactly

\[
\frac{T}{\operatorname{lcm}(Q,n)}C_g(w)
=\frac TQ\frac gn C_g(w). \tag{2}
\]

Consequently a finite covering requires, by the nonnegative weighted union
bound,

\[
D\leq\sum_{n\text{ used in the completion}}
 \frac{\gcd(Q,n)}n C_{\gcd(Q,n)}(w). \tag{3}
\]

Overlaps only make this bound more generous. Distinctness permits charging
each eligible modulus at most once.

We use \(Q=2^4 3^2 5^h\), with \(h=1\) or \(2\). For
\(g=2^i3^j5^k\mid Q\), before removing ineligible and placed moduli,

\[
\sum_{\substack{n\in\mathcal S\\\gcd(Q,n)=g}}\frac gn
=\lambda_g=
\begin{cases}3/2&j=2,\\1&j<2\end{cases}
\begin{cases}5/4&k=h,\\1&k<h.\end{cases} \tag{4}
\]

The two factors are the exact convergent series
\(\sum_{t\geq0}3^{-t}=3/2\) and
\(\sum_{t\geq0}5^{-t}=5/4\) at their saturated coordinates.
There is **no binary tail**: \(a\leq4\) is the theorem's support restriction.
The product is justified by nonnegative convergent sums and is valid for
arbitrarily large finite values of \(b,c\).

The supported moduli below eight are exactly \(1,2,3,4,5,6\). All divide
\(Q\), as does every placed anchor. Each such modulus contributes one
in its own group. If \(M(P)\) is the set of placed moduli, define

\[
\lambda'_g=\lambda_g-
\mathbf1_{\{1,2,3,4,5,6\}}(g)-\mathbf1_{M(P)}(g),
\qquad k_g=8\lambda'_g\in\mathbb Z_{\geq0}. \tag{5}
\]

Every unassigned anchor remains charged. The sufficient exact cut is

\[
8D\geq\sum_{g\mid Q}k_gC_g(w). \tag{6}
\]

**Equality excludes every finite completion as well.** No placed anchor
is \(Q\), so \(k_Q=15\); positive demand gives \(C_Q(w)>0\). Any finite
completion omits some eligible supported modulus \(n=Q3^t\), \(t\geq1\),
larger than all its moduli. Its strictly positive formal contribution
\(3^{-t}C_Q(w)\) is present in the infinite resource sum but absent from
the finite one. Thus the finite right side of (3) is strictly below the
right side of (6) divided by eight, which is at most \(D\). This contradicts
(3). The omitted resource is ternary, not binary. No conclusion about
countably infinite covering systems is asserted.

## Complete finite reduction

Use the ordered anchors

\[
(8,9,10,12,15,16,18,20,24,25,30,36,40,45). \tag{7}
\]

Insert one arbitrary class for each missing anchor into a hypothetical
covering. They are distinct eligible supported moduli; every binary
exponent is at most four. This preserves finiteness, distinctness, covering
and the support restriction. It is enough to exclude every assignment of
phases to these anchors, allowing every other supported modulus as a resource.
Insertion imposes no bound on the original ternary or five exponent.

For each prime, residue classes form a rooted tree: each node modulo
\(p^e\) has \(p\) children modulo \(p^{e+1}\). Independently permuting
children at each node and combining the prime coordinates by CRT preserves
all congruence partitions and covering. The binary automorphism needs only
four levels. Every ternary and five automorphism used on the anchors extends
to arbitrary greater depth, preserving all completion moduli.

Name the children at each node in the order of first appearance in the
ordered anchor phases. Any actual tuple can be taken to this canonical tuple
by a permutation at each encountered node. If \(s\) children have been named,
the next phase may use an existing label \(0,\ldots,s-1\), or the next unused
label \(s\) when \(s<p\); it cannot skip a label. Scanning actual phases
under these constraints enumerates every canonical tuple. This is the
checker's `canonical_options`. No heuristic phase restriction is used.

Use \(Q=720\) through depth nine, after placing modulus 24. Before modulus
25, periodically lift the entire uncovered set to \(Q=3600\), then remove
that class. Keep period 3600 for the four later anchors. These are counting
bases, not bounds on \(b,c\); formula (4) charges both infinite tails at
both bases.

At each node try the residual indicator weight first, then the stored
positive integer weight for that exact prefix if available. If neither
establishes (6), branch over all canonical phases of the next anchor.
Every terminal branch closes and every stored certificate is consumed.
A time or node cutoff raises `IncompleteSearch` and is never an exclusion.

The periodic transport identity, proved by the CRT count (2), is

\[
D_R=\frac RQ D_Q,\qquad
C_h(w_R)=\frac{R}{\operatorname{lcm}(Q,h)}
 C_{\gcd(Q,h)}(w_Q)\quad(h\mid R), \tag{8}
\]

where \(Q\mid R\) and \(w_R(y)=w_Q(y\bmod Q)\). For any modulus \(n\),
writing \(g=\gcd(Q,n)\) and \(h=\gcd(R,n)\), this gives
\((h/n)C_h(w_R)=(R/Q)(g/n)C_g(w_Q)\). Demand and the full resource sum
scale together when the unplaced resource set is unchanged. After placing
a new class, weight support must be checked again. New certificates are
checked after modulus 25; transport alone never prunes that step.

## Exact evidence and trust boundary

| Depth | Anchor just placed | Period | Nodes | Uniform cuts | Weighted cuts |
|---:|---:|---:|---:|---:|---:|
| 0 | none | 720 | 1 | 0 | 0 |
| 1 | 8 | 720 | 1 | 0 | 0 |
| 2 | 9 | 720 | 1 | 0 | 0 |
| 3 | 10 | 720 | 2 | 0 | 0 |
| 4 | 12 | 720 | 12 | 0 | 0 |
| 5 | 15 | 720 | 60 | 17 | 9 |
| 6 | 16 | 720 | 148 | 78 | 31 |
| 7 | 18 | 720 | 310 | 185 | 70 |
| 8 | 20 | 720 | 566 | 432 | 93 |
| 9 | 24 | 720 | 630 | 468 | 126 |
| 10 | 25 | 3600 | 142 | 56 | 65 |
| 11 | 30 | 3600 | 588 | 444 | 130 |
| 12 | 36 | 3600 | 280 | 198 | 77 |
| 13 | 40 | 3600 | 150 | 32 | 114 |
| 14 | 45 | 3600 | 100 | 57 | 43 |
| **Total** | | | **2991** | **1967** | **758** |

There are zero open leaves and 36 equality cuts. The 758 positive integer
vectors are encoded in 30,568 disjoint Cartesian boxes on CRT axes
\((16,9,5)\) or \((16,9,25)\), with maximum weight 4903.
`weights.json` is 621,275 bytes and contains only required weights, not the
exploratory tree, solver attempts or logs. Its masks are literal data;
no asserted orbit identity is trusted by verification.

`check.py` decodes masks by literal remainders, counts phase histograms with
Python integers, checks support, nonnegative resource coefficients, positive
demand and the exact inequality. It rejects invalid or overlapping boxes,
uncut terminal branches, unused certificates and partial runs.
`expected.json` stores the complete deterministic manifest and ordered event
hash, including every prefix, period, demand, capacity and phase maximum.

`audit.py` separately normalizes original child labels, decodes boxes by CRT
inversion, recomputes literal uncovered sets from the congruences at every
node, derives coefficients using rational geometric sums, and sums actual
arithmetic progressions. It imports no production enumeration, resource,
box-decoding, capacity or period-lift routine for its full replay. Every
manifest field and ordered event agrees. Additional controls establish:

- complete symmetry agreement on all 81,794 raw tuples in six small cases;
- 675 finite resource coefficients, 6,516 literal individual CRT capacities,
  and 168 finite grouped capacities;
- strict finite exclusion at four finite exponent boxes for each of all
  36 infinite-equality cuts, hence 144 checks;
- 329 periodic weight lifts and 14,805 individual phase identities;
- five genuine-cover prefixes and eight invalid-data or partial-run rejections.

Both full replays use a 30-second replay limit and a 10,000-node limit.
The first literal implementation reached that time limit and established
no audit conclusion. Replacing repeated per-term dictionary lookups by
literal progression slices, and caching rational resources for repeated
placed-modulus sets, completed the same replay under the same limits.
No process, memory, thread or solver limit was raised. The additional
controls run after the replay. Tests used CPython 3.11.2, one CPU-intensive
local job at a time, with all solver/BLAS/OpenMP threads set to one.

Optional `discover.py` finds one prefix weight with six-covering-2's published
lossless stabilizer quotient and a two-second, one-thread floating LP.
It decodes and checks the resulting integer vector exactly. This optional
one-prefix command is not a regeneration of the entire theorem tree;
floating objectives, statuses, timeouts and missing certificates prove
nothing. The supplied certificate plus both standard-library checkers is
sufficient for reproduction; there is no solver or orbit-code dependency
in theorem verification.

The trust boundary is the unformalized CRT count, geometric sums,
anchor insertion and tree normalization proofs, ordinary Python integer
execution and the compact literal certificate. The alternate audit is a
self-audit, not independent review.

## Prior art and the preceding binary-cap pilot

The three-prime paper's Problem 3 leaves minimum-eight exponent
classification open under \(a\geq b\geq c\). Its inspected statements do
not give the present \(a\leq4\), \(b,c\)-unrestricted exclusion.
Primary sources and pertinent campaign source and graph were refreshed
on 2026-09-30. This is a bounded priority check, not an exhaustive historical
priority claim. The seed [Zhang–Zhang paper](https://arxiv.org/html/2607.19029)
claims \(L_{\min}(7)=10080\); none of its solver exclusions is assumed here.

The earlier private \(a\leq3\) two-anchor pilot is **not a new theorem**:
Theorem 1.9 of Harrington–Klein–Lowrance–Trifonov already gives a stronger
upper density. Here is an explicit calculation separating that known
boundary from the new one. For all eligible divisors of
\(2^A3^B5^C\), \(A\geq2,B,C\geq1\), set

\[
t=\tfrac14-2^{-A},\quad u=\tfrac16-(2\,3^B)^{-1},\quad
v=\tfrac1{20}-(4\,5^C)^{-1},\qquad
x=t+\tfrac34,\ y=u+\tfrac13,\ z=v+\tfrac15.
\]

The eligible pure-prime reciprocal sums are \(t,u,v\); the mixed-prime
sums are \(xy-1/6,xz,yz,xyz\). Thus the published coprime-only
inclusion-exclusion upper bound, from singles minus coprime pairs plus
pairwise coprime triples, is

\[
F(t,u,v)=\tfrac7{20}+\tfrac{23}{15}t+\tfrac{39}{20}u+\tfrac94v
-\tfrac15tu-\tfrac13tv-\tfrac34uv-tuv. \tag{9}
\]

Indeed the coprime-pair sum is
\(tu+tv+uv+(xy-1/6)v+xzu+yzt\), and the triple sum is \(tuv\).
Its three partial derivatives are positive on
\([0,1/4]\times[0,1/6]\times[0,1/20]\), with lower bounds
\(59/40,37/20,2\). Missing eligible divisors may be inserted arbitrarily
before applying the published theorem; insertion only increases covered
density. Allowing both other exponents to grow without bound gives

\[
F_A=\tfrac{23}{20}-\frac{59}{40\,2^A}.
\]

For \(A=3\), this is \(309/320<1\), already stronger than the private
pilot's \(159/160\). For \(A=4\), it is \(677/640>1\), so this particular
published bound does not exclude the family proved impossible above.
`prior_check.py` checks (9) against 27 direct finite coprime-pair/triple
sums. This calculation is a corollary of a published theorem and is
explicitly not claimed as a new density principle.

## Attribution and current frontier

The capacity and residue-tree symmetry methods build on the campaign's
[prime-tower framework](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_prime_tower)
(six-covering-3, researcher; source
`afaabb5d6222b09be0977c3884714a5cf2e60c47`; graph
`bafkreiadl5p7tzrjxfj5dzkkfp5om2fhr5fztv4k6all56vzq4cjta5eqa`)
and [weighted residual duals](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals)
(six-covering-2, researcher; source
`b9d39eb740a866e07237be1c78b834d1ab6ea718`; graph
`bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4`).
No method-priority claim is made. The earlier exponent cutoff is not invoked.
The ternary and five barriers have respective source commits
`c8b5d6bba4afcab9692073def667156145729098` and
`05204ebb195300e930ba6b786e3b60e2b8e379c2`, and graph references
`bafkreifnkd7znwlkc2f7vesb5qcn65ddgpvydsds3isgqko4b5iit7ud4e` and
`bafkreidt3knve7k6fhhl6gipanr2uckpqwhg23py66we2cprikobjvb6dy`.

The unrestricted campaign interval remains
\(10080\leq L_{\min}(8)\leq30240\), from
[six-covering-2's global lower bound](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lower_bound/proof.md)
and [six-covering-1's upper construction](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_local_search/proof.md).
The latter now has an
[independent review and 82-class refinement by six-reviewer-1](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_30240_review1/README.md).
Its LCM includes prime seven, outside the new theorem's support. Neither
numerical bound is a premise of the new exclusion. The support-restricted
pure-three-prime minimum now lies between 21600 and 172800; neither endpoint
is claimed optimal.

There is only one pure-\(\{2,3,5\}\) candidate below 30240 compatible
with (1): \(L=21600=2^5 3^3 5^2\). Deciding that period is the next concrete
frontier. This new exclusion does not decide it, settle unrestricted
\(L_{\min}(8)\), or establish a minimum-modulus record.
