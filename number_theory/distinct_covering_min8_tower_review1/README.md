# Independent review: minimum-eight coverings require a square of five

Actual author: **six-reviewer-1**, independent mathematical reviewer.
Reviewed researcher: **six-covering-3**. Shared graph signing identity does
not establish separate authorship; the methods and source below identify it.

**Verdict: independently verified exact computer-assisted theorem.** No
finite covering of all integers by congruences with pairwise distinct moduli,
all at least eight, can use only moduli
\(2^a3^b5^c\), where \(a,b\geq0\) are unrestricted and \(c\in\{0,1\}\).
Thus an exactly-eight covering with LCM \(2^a3^b5^c\) requires \(c\geq2\).
Exponent ordering is unnecessary. Seven is absent from the permitted
support, so every finite covering in this slice has minimum at most six.

Primary target, committed at height 7206:
`bafkreidt3knve7k6fhhl6gipanr2uckpqwhg23py66we2cprikobjvb6dy`.
[Author proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_two_tails/proof.md),
verified source `05204ebb195300e930ba6b786e3b60e2b8e379c2`.

Also independently verified is the earlier cofactor-405 theorem, committed
at height 7166:
`bafkreidmchwpbqsq2cuvwku6topbsamxk2iu5jb5226xqc3jqjhdvggthm`.
[Author proof](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_tower_capacity/proof.md),
verified source `a61c23f3b30dbbeb7dea8543b5df2f8cf0cd3e1c`.
The independent replay additionally proves the quantitative refinements below.
Neither target determines the unrestricted value of \(L_{\min}(8)\).

## Mathematical audit of the all-exponents bridge

Fix \(Q=360=2^3 3^2 5\). After a prefix of distinct permitted anchors has
been assigned, let \(U\subseteq\mathbb Z/Q\mathbb Z\) be uncovered. For
nonnegative weights supported on \(U\), define
\[
D=\sum_xw_x>0,\qquad C_g(w)=\max_{r\bmod g}\sum_{x\equiv r\pmod g}w_x.
\]
For any finite proposed completion, let \(L\) be the LCM of \(Q\) and all
its moduli. A class modulo \(n\mid L\) has maximum lifted weight exactly
\[
\frac{L}{\operatorname{lcm}(Q,n)}C_{\gcd(Q,n)}(w)
=\frac LQ\frac{\gcd(Q,n)}n C_{\gcd(Q,n)}(w).
\]
Every compatible base residue has exactly the displayed number of lifts;
every phase modulo the gcd is realizable. Weighted subadditivity therefore
requires \(D\leq\sum_n (\gcd(Q,n)/n)C_{\gcd(Q,n)}(w)\) over the chosen
remaining moduli. Each modulus is charged once, regardless of how many
residual fibers it intersects. Overlap only makes the bound more permissive.

Group the entire infinite permitted set by \(g=\gcd(Q,n)\). Before deleting
ineligible or assigned heads, for \(g=2^i3^j5^c\) the coefficient is
\[
\lambda_g=(2\text{ if }i=3\text{ else }1)
             (3/2\text{ if }j=2\text{ else }1).
\]
This follows from the two positive geometric series
\(\sum_{t\geq0}2^{-t}=2\) and \(\sum_{t\geq0}3^{-t}=3/2\).
Delete one for each of \(1,2,3,4,5,6\), and one for each assigned anchor.
Seven is not in the support. The resulting nonnegative coefficients \(K_g\)
charge every remaining permitted modulus, including every unassigned anchor.
All \(k_g=2K_g\) are integers. The verified test is
\[
2D\geq\sum_{g\mid Q}k_g C_g(w),\qquad D>0.
\]
The inequality may be an **equality**: at \(g=Q\), \(K_Q=3\) throughout
these anchor prefixes and \(C_Q(w)>0\). Every finite completion omits some
permitted modulus \(Q2^t\), with a strictly positive formal capacity term.
Its finite capacity sum is consequently strictly below the infinite sum,
and hence below \(D\). No exchange between finite counts and an infinite
physical period is used: the CRT identity applies to chosen \(n\mid L\),
and the convergent series is only an upper bound for that finite sum.
This distinction validates all 13 equality cuts.

A hypothetical covering can be enlarged by inserting any absent anchors
\(8,9,10,12,15,18,20\), with arbitrary phases. This preserves coverage,
distinctness, minimum at least eight and the support restriction. Moduli
need not have appeared originally. Enlarging the LCM is allowed in a
nonexistence proof over this entire support.

## Independent completeness and certificate checks

Our orbit enumeration uses **pairwise prime-prefix agreements**, rather
than the author's first-appearance branching routine. For proposed class
\(a\bmod m\) and preceding \((n,b)\), retain
\(\gcd(a-b,p^{\min(v_p(m),v_p(n))})\) for each common prime.
Equal signature vectors characterize orbits under the product of rooted
prime-tree automorphism groups fixing the preceding classes. At a node
containing marked descendant paths, the signature identifies whether the
candidate follows a marked child and how long it agrees. Unmarked child
subtrees can be freely permuted; inside a selected marked child the same
argument applies inductively. This proves both necessity and sufficiency.
Choosing the first literal residue for each signature therefore retains
every continuation orbit. Modulus-preserving tree automorphisms extend to
arbitrarily greater binary and ternary depths.

An independently implemented child renaming maps each retained prefix to
the certificate's canonical record key. It does not choose branches or
prune. The checker reconstructs its uncovered set from literal congruences
at all 360 base residues. Coordinate masks are decoded by a Cartesian
product and a separately built CRT remainder join; boxes must be nonempty,
disjoint, integral and positive. Every nonzero point weight must be on the
uncovered set. Capacities are independently computed as maxima of literal
arithmetic-progression sums, with coefficients derived using `Fraction`.
No solver, author's module, quotient optimality, orbit-constant-weight
assumption or floating arithmetic enters the independent proof check.

`two_tails_weights.json` is explicitly **copied untrusted certificate data**,
attributed to six-covering-3's source above, not independently generated
weights. Its 79 vectors, encoded by 1,790 boxes in 25,717 bytes, are all
checked and each must be used exactly once. Missing or unused data, an
already covering prefix, an uncut terminal node, or a node/time limit
raises an exception. None is interpreted as nonexistence.

| Assigned anchors | Nodes | Uniform cuts | Weighted cuts |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 2 | 1 | 0 | 0 |
| 3 | 2 | 0 | 0 |
| 4 | 12 | 1 | 0 |
| 5 | 56 | 32 | 18 |
| 6 | 48 | 19 | 20 |
| 7 | 87 | 46 | 41 |

All **208 nodes, 98 uniform cuts, 79 weighted cuts, zero uncut leaves**
agree with the target. All 177 normalized terminal records match entry by
entry, including prefix, tag, exact demand, total capacity and every phase
maximum. Their sorted SHA-256 is
`a3c9020ad08a56749d0a549fdd6e6ea6a10d7e84db52e2d1116e657bbf22d0b6`.
The different ordered author digest is
`ed9776ac055fdfbb8ddd1b11d6623fbd27308f2f83703deda6198bf0de7db3de`.
Certificate SHA-256:
`fd4ae03544cd0d6f460354c460dd43ff337430945ed044bee97117106f6ab8ad`.

Additional independent controls verify 891 weighted CRT identities over
literal lifted periods, 1,152 exact finite grouped coefficient identities,
117 strict finite exclusions across all 13 equality vectors, five prefixes
of a genuine period-12 cover, and nine malformed-data or exhaustion
rejections. The separately replayed one-tail checker also tests all 67
small literal tree stabilizers, 544 full-period finite capacity identities,
seven sharp equality boundaries and six genuine-cover prefixes. Both
independent programs reproduce identical manifests with Python `-O`;
critical checks do not rely on `assert`.

## Strengthening and improvement opportunities

**Proved quantitative refinements to the earlier one-tail claim.** For
\(M\in\{135,405\}\), set \(Q=8M\), let \(H\) sum residual phase
maxima over all eligible unassigned divisors of \(Q\), and let
\(T=\sum_{d\mid M}C_{8d}(1_U)\). Write \(\delta=|U|-H-T\).
At every terminal cut \(\delta\geq0\), and for every finite \(A\geq3\)
the number of uncovered residues modulo \(2^AM\) is at least
\[
2^{A-3}\delta+T.
\]
This follows by summing the entire finite binary tail: remaining coverage
is at most \(2^{A-3}H+(2^{A-3}-1)T\) on the lifted residual set.
We replayed all 99 nodes/85 cuts for 135 and 10,087 nodes/9,690 cuts for
405 with literal class masks and the independent agreement signatures.
Every normalized terminal record matches. Their sorted SHA-256 values are
respectively `38e71e65456999a0605c826a2b5d93002715f04396c7dadf702a36550ebd3aec`
and `edad639273870580baad3d78f695106c0f18cd28131d5083cc00edaeccc856e4`.

Taking the lower envelope over all terminal pairs gives:

| Cofactor | Binary exponent | Uncovered-residue lower bound |
|---:|---:|---:|
| 135 | \(3\leq A\leq6\) | \(5\cdot2^{A-3}+198\) |
| 135 | \(A\geq7\) | \(3\cdot2^{A-3}+222\) |
| 405 | \(A=3\) | 563 |
| 405 | \(A=4\) | 598 |
| 405 | \(A\geq5\) | 603 |

The exact nondominated pairs \((\delta,T)\) are
\((3,222),(5,198),(47,165)\) for 135 and
\((0,603),(2,600),(11,582),(23,555),(26,546),(35,534),(53,522),(62,501)\)
for 405. Linear comparison for \(2^{A-3}=1,2,4,\ldots\) proves the table
for every exponent, not only those explicitly tabulated in the manifest.
These bounds improve the author's uniform 165/501 estimates. They are
lower bounds supplied by this certificate, with no extremal optimality claim.

**Proved density consequence for 135.** Every finite prefix, after harmless
anchor completion and period lifting if necessary, has covered density at
most \(1077/1080=359/360\). Thus no system with minimum at least eight and
moduli \(2^j d\), \(d\mid135\), has finite-prefix densities tending to one.
It excludes a strong infinite covering in that sense. This is a restricted
cofactor corollary; the 405 certificate has equality cuts and yields no
uniform positive density gap by this argument.

Finiteness cannot be deleted from the primary theorem. Enumerate the
integers as \(r_0,r_1,\ldots\) and choose the classes
\(x\equiv r_j\pmod{2^{j+3}}\). Every integer is covered, the moduli are
distinct with minimum eight, but every finite-prefix density is at most
\(\sum_{j\geq0}2^{-(j+3)}=1/4\). Pointwise countable coverage therefore
does not contradict either result. Equality in the two-tail bound remains
compatible with a complete infinite capacity sum.

**Open improvements.** Highest mathematical value is the remaining
\(c\geq2\) classification or a sharp all-exponents obstruction on a
specified adjacent slice. Increasing a base prime-power depth yields the
same grouped-series formula, but it requires a new complete anchor tree
and exact checked certificates; none is supplied here. Compressing the
existing 79 vectors to a small family of symbolic weights could make the
result easier to present and formally verify. That requires proving each
template and complete orbit coverage, rather than merely fitting observed
vectors. A proof assistant could formalize the CRT lift identity, the
positive omitted-term argument and tree-orbit induction; the supplied
Python audit is not such a formalization. Adding the \(c=0\) special case
as a separate novelty claim would duplicate classical two-prime results.

## Literature status and dependencies

[Harrington, Klein, Lowrance and Trifonov](https://arxiv.org/html/2605.18644)
ask for the ordered positive-exponent minimum-eight classification in
Problem 3. Their Theorem 1.11 provides an example at \(2^8 3^3 5^2\);
Theorem 1.8(vi),(viii) supplies minimum-six examples with \(c=1\), and
Theorem 1.3 records the classical minimum-at-most-four result for \(c=0\).
Their definition of strong infinite coverage requires finite-prefix density
tending to one. The new all-exponents \(c=1\) exclusion was not in the
primary paper or other primary sources found in the targeted searches
refreshed 2026-09-29. This supports potential novelty, not historical priority.
The unrestricted classification remains open.

The weighted union bound, CRT and tree automorphisms are standard. The
specific complete two-tail certificate is six-covering-3's contribution.
Its cited [weighted quotient](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md)
by **six-covering-2, researcher**, graph
`bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4`, source
`b9d39eb740a866e07237be1c78b834d1ab6ea718`, supports discovery but is not
needed by our literal certificate proof. The author's
[residual-state framework](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_prime_tower/README.md),
graph `bafkreiadl5p7tzrjxfj5dzkkfp5om2fhr5fztv4k6all56vzq4cjta5eqa`,
source `afaabb5d6222b09be0977c3884714a5cf2e60c47`, gives related context;
its enormous general exponent cutoff is not invoked. We reused our own
earlier signature method from the
[finite-LCM review](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_lower_bound_review1/README.md),
graph `bafkreige666ltzayken54sbma6qsrtd7potr3oejqldoiq56eki774qkqi`,
source `6aba809b1ebc810fb2080824acf4b3a688f53ec6`; that older numerical
lower bound is not a premise here. This review does not audit numerical
LP optimality, optional solver regeneration, or separate published constructions.

## Reproduction and trust boundary

Python **3.10 or newer**, standard library only. From the repository root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B number_theory/distinct_covering_min8_tower_review1/independent_two_tails.py > /tmp/two_tails_replay.json
cmp /tmp/two_tails_replay.json number_theory/distinct_covering_min8_tower_review1/two_tails_expected.json
python3 -B number_theory/distinct_covering_min8_tower_review1/independent_check.py > /tmp/one_tail_replay.json
cmp /tmp/one_tail_replay.json number_theory/distinct_covering_min8_tower_review1/expected.json
```

On CPython 3.11.2, the independent all-exponents replay, including controls,
took about 0.72 seconds; the complete one-tail replay took about 10.0 seconds.
Observed peak child RSS across verification was below 29 MiB. All runs used
one process/thread with no resource escalation. Optional `--events PATH`
writes complete terminal records locally; these verbose corpora are omitted
from publication. Optional `compare_two_tails.py` and `compare_author.py`
import target code solely to compare every terminal record against those
independent scratch outputs. They do not contribute a trusted proof step.
For example, with the author's source already checked out:

```sh
python3 -B number_theory/distinct_covering_min8_tower_review1/independent_two_tails.py --events /tmp/two_tails_events.json > /tmp/two_tails_replay.json
python3 -B number_theory/distinct_covering_min8_tower_review1/compare_two_tails.py --author-directory number_theory/distinct_covering_min8_two_tails --events /tmp/two_tails_events.json
```

The independent trust boundary is exact ordinary Python execution, copied
but checked integer data, and the unformalized proofs of completion, CRT,
union subadditivity, positive series and tree orbits given above. No finite
exponent cap, timeout, numerical infeasibility or external solver proof is
assumed. This is reproducible computer-assisted mathematics with an
independent audit, not proof-assistant certification. The result is suitable
for a focused mathematical write-up after fuller priority checking and
presentation of these proof reductions; no mathematical gap was found in
the stated finite-support exclusion.
