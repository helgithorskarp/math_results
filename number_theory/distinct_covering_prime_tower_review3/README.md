# Independent audit of the prime-tower covering cutoff

Actual reviewer: **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-29. The target identifies its authoring agent as six-covering-3,
researcher. The shared signing key does not establish distinct authorship;
independence here consists of target selection, mathematical derivation, and
the separately implemented evidence described below.

Target: **Exact residual-fiber reduction and exponent cutoff for distinct
prime-tower coverings**, committed reference
`bafkreiadl5p7tzrjxfj5dzkkfp5om2fhr5fztv4k6all56vzq4cjta5eqa`.
Reviewed source commit: `afaabb5d6222b09be0977c3884714a5cf2e60c47`.
The [target proof](../distinct_covering_prime_tower/proof.md) supplies the full
statement and source context.

## Verdict and scope

**Confirmed, with high confidence as an ordinary mathematical proof.** The
residual-width argument, anonymous multiset continuation, independent local
cofactor symmetries, finite-state count, path shortening, and exact-minimum
completion conditions are valid. The computational evidence supports these
bridges on its explicitly bounded test domains. No general theorem follows
from finite testing alone, and neither implementation is proof-assistant
formalized.

Precisely, let p be prime, M positive with gcd(p,M)=1, and m>=2. Put
s=min{e:p^e>=m}, k=tau(M), and W=floor((k-1)/(p-1)). Write v=nu_p(m).
If m/p^v divides M, existence of a distinct covering with minimum exactly m
and LCM p^A M for some A>=0 is equivalent to existence with

\[
s\le A\le s+\binom{2^M-1+W}{W}-1.
\]

If the divisibility condition fails, exact minimum m is impossible for every
A. The corresponding G-orbit bound in the target is also confirmed. This
does not determine L_min(8), bound several independently varying prime
exponents, or establish practical complexity for the large cofactor graph.

## Independent mathematical validation

There is a direct counting proof of the width inequality, independent of the
target's recurrence. At depth e, choose one y_r in each nonempty residual
fiber U_r. In the period p^A M, mark every point with cofactor coordinate y_r
and p-prefix r. There are exactly n_e p^(A-e) marked points. Earlier classes
cover none. A class of exponent j>e covers at most p^(A-j) marked points:
its p-prefix lies in one parent r and either its cofactor residue accepts y_r
or it does not. If there are at most k_j classes at exponent j, the union
bound gives

\[
n_e p^{A-e}\le\sum_{j=e+1}^A k_j p^{A-j}.
\]

Dividing gives the finite-horizon bound. With k_j<=k the bound is strictly
less than k/(p-1) for a finite horizon, giving W, including the forbidden
integer equality boundary. The empty state and A=e are covered separately
by n_e=0. When M=1, W=0; the reduction does not accidentally allow a finite
distinct covering by prime powers with minimum at least two.

For continuation, only classes of larger exponent remain. Such a class acts
in one descendant of one surviving prefix. A bijection between equally
labeled residual subsets therefore transports a complete continuation while
preserving the single resource for each (j,d). Resources are shared across a
whole depth; the argument introduces no separate per-parent allowance.
Empty fibers may be discarded because future operations there can be
omitted. Completion restores omitted admissible moduli after coverage.

An independent congruence-preserving cofactor permutation in each parent
also transports all later residue choices, keeping every individual modulus
unchanged. It need not preserve earlier congruences. For example, removing
0 modulo 3 from both binary-prefix fibers gives residual masks (6,6), both
representing {1,2}. Translating only the first fiber gives (5,6). This cannot
be induced by transforming the earlier single modulus-three class into a
single modulus-three class, but it gives the same continuation possibilities.
The target correctly treats it as continuation normalization.

The finite-state count includes the empty multiset. After depth s, every d|M
is admissible and the transition is stationary. Removing a repeated-state
segment leaves a valid path. Its physical realization at the smaller depth
has enough prefixes: each step produces p children of the presently active
parents, and distinctness is still enforced once per d at that depth. A
simple path has at most N-1 edges, rather than N. For m/p^v|M, v<=s makes
m|p^s M; adding m and the terminal period establishes the claimed exact
minimum and exact LCM. A smaller original exponent can be padded to s.

## Independent evidence and reproduction

Run from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  NUMEXPR_NUM_THREADS=1 \
  python3 number_theory/distinct_covering_prime_tower_review3/audit.py
```

Dependencies: CPython >=3.10 and its standard library; checked with CPython
3.11.2, one process/thread, approximately 2.2 seconds and 18 MiB peak RSS.
The script uses explicit checked failures and also works under Python -O.
It imports no target code or target fixture data. Its output must equal the
compact [expected.json](expected.json).

Expected output SHA-256:
`069a4d3c7763ef231ba7a268d08825f509faa3b3abe75438bfd6c58d3a2c9c94`.

The checker exhausts literal congruence-class coverage unions in the integer
period, retaining prefix labels until the final comparison. It performs
3,334 parameterized parent-state checks: all ordered pairs of residual
subsets for M=3 and M=5 in two binary-prefix parents, all ordered triples for
M=2 in three ternary-prefix parents, every single M=9 subset, and 518 chosen
two-parent M=9 assignments. The complete successor sets, rather than only
their cardinalities, agree whenever the proposed state keys agree.

Separately, it enumerates actual leaf permutations of six small residue
trees instead of using the target's recursive subset-type encoding. The
group orders are 2,8,128,6,1296,120 and their subset-orbit counts are
3,6,21,4,20,6. It checks 1,338 ambient maps, including independent local
cofactor actions and parent permutations, for exact bijections of every
individual next-layer congruence-class family. Checking generators proves
the same transport property for their compositions; the full independent
two-parent group need not be enumerated.

There are 91 separate bounded full-period feasibility controls, without the
width cut or a symmetry quotient, with the exact-minimum divisibility check
kept separate from at-least-m feasibility. Their compact table hash is
`15557af864fe8f21d4e406bbb74cfc2ba63a62ce00504bc4839264a612e3add3`.
The M=9 exponent cutoffs reproduce 131330, 1832, and 212. All 720 permutations
of the M=6 residue set are independently screened for congruence preservation:
12 remain, with 13 subset-orbits. The incorrect factor-orbit product is 12.

The target's complete source command was also replayed, with its JSON compared
entry by entry to its published expected file. Its output SHA-256 is
`f350c03e0b7fac8d6ac675b44634d6dfff3774be71234a7f9d20b9a2f46c7e7e`,
matching the committed claim. This replay is distinguished from the independent
audit. No large cofactor closure or independently generated construction is
claimed. Ordinary Python correctness and the unformalized general proofs
are explicit trust boundaries; no solver, floating arithmetic, imported
large certificate, or commercial-solver exclusion is required.

## Literature status and publication readiness

Candidate-specific primary-source inspection confirms that the CRT digit
representation and divisor completion precede this work. Harrington,
Klein, Lowrance and Trifonov, [arXiv:2605.18644](https://arxiv.org/html/2605.18644),
Section 2 and Problem 3, supply the fixed-prime-support context. Zhang and
Zhang, [arXiv:2607.19029](https://arxiv.org/html/2607.19029), Section 2, explicitly
use divisor completion. Klein, [Integers 26 (2026), A38](https://math.colgate.edu/~integers/aa38/aa38.pdf),
Section 3, treats multiplicity budgets in covering integer programs. None
of their computational exclusion claims is a premise of this review.

The particular combination of an exact residual multiset, its width barrier,
and a single-unbounded-exponent cutoff was not located in these primary
sources or targeted searches. This supports a potentially useful structural
contribution; it does not establish literature priority. CRT, finite-state
path shortening, Burnside counting, and the group fact below should be
attributed as existing mathematical tools. The statement and proof are
ready for consideration as a scoped structural lemma, with priority and
practical computational impact still needing careful assessment.

## Strengthening and improvement opportunities

**Proved refinement: identify the full allowed cofactor group.** Write
M=product_i q_i^b_i. The group of *all* permutations preserving residue
classes for every individual divisor of M is, under CRT,

\[
G_{\max}=\prod_i \operatorname{Aut}(T(q_i,b_i)),
\]

where T(q,b) is the depth-b rooted q-ary residue tree. To prove this,
preservation of the partition modulo q_i^b_i makes the i-th output coordinate
depend only on the i-th input coordinate and defines a bijection on it.
Preservation modulo all lower q_i powers makes that bijection a tree
automorphism. Conversely, independent such coordinate maps preserve every
divisor-class partition. This identifies the largest permissible symmetry
group for the target's stated symmetry corollary; it does not assert that
all other possible continuation equivalences come from these permutations.

For g=(g_i), let the cycle lengths of g_i be ell_ij. The product permutation
has cycle count

\[
c(g)=\sum_{j_1,\ldots,j_t}
\frac{\prod_i\ell_{i j_i}}{\operatorname{lcm}_i(\ell_{i j_i})}.
\]

Each product of cycles has that many orbits, each of length the stated LCM.
Thus H=|G_max|^-1 sum_g 2^c(g) supplies the target's sharpest cutoff within
this permutation-group normalization. Subset-orbit counts of the factors
cannot be multiplied: the M=6 independent control gives 13, while 3*4=12.
A cycle-index implementation for residue-tree groups is the concrete next
lemma/tool needed to evaluate composite-cofactor H without enumerating the
whole group. This is a proved application of the target's corollary and
classical group facts, not a priority claim or a new numerical L_min(8) bound.

**High-value computational use, still unproved:** combine the exact residual
quotient with a certified complete reachable closure or a sound residual
potential on a nontrivial cofactor. In particular, L=10080=2^5*315 is the
next period left open by the campaign's separately claimed
[minimum-eight lower bound](../distinct_covering_min8_lower_bound/proof.md),
reference `bafkreihbmsoga46xbfhoklyxsfg3utwtcji4wkiszwrpbdffvuucffe3cy`.
The present proof gives necessary widths n_3<=9 and n_4<=6 there, using
tau(315)=12. Turning those cuts into an exclusion requires complete initial
case coverage and a checkable closed-state or inequality certificate. A
bounded failed search would not suffice. This review has not independently
verified that separate numerical lower-bound contribution.
