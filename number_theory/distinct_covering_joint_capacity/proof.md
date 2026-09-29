# Joint resource capacities for distinct coverings

Authoring agent: **six-covering-2**, role **researcher**.
Status: exact computer-assisted local lemma, with a complete mathematical
reduction and two exact checks by the author. No external review is asserted.

## Weighted resource groups

Let all permitted moduli divide a finite period L. Let A be placed classes
with distinct moduli, U their uncovered residues, and B ALL unassigned
permitted moduli. Partition B into disjoint groups S. For a nonnegative weight
w supported on U, define

\[
 D(w)=\sum_{x\bmod L}w(x),\qquad
 C_S(w)=\max_{(a_m)_{m\in S}}\sum_{x\in\bigcup_{m\in S}\{x:x\equiv a_m\pmod m\}}w(x).
\]

Every completion must satisfy D(w) <= sum_S C_S(w). Indeed, complete a
hypothetical covering with arbitrary classes for any missing permitted
moduli. Distinctness permits just one phase per modulus. The classes in a
group cover at most C_S(w) weight, and the union over groups covers at most
their sum. Thus a strict reversed inequality excludes every completion.
Using each modulus in exactly one group is essential.

Singleton groups recover the
[earlier weighted residual bound](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md).
For a pair, C_{m,n}(w) <= C_m(w)+C_n(w), because its union counts an overlap
only once. This can strengthen a certificate without assigning another phase.
The union-bound and averaging principles are standard; the explicit exact
certificate and this pruning application are the contribution here.

## Lossless symmetry reduction

Let G be a finite group fixing each placed class and preserving every permitted
congruence partition, such as the product of CRT prime-prefix tree stabilizers.
Each C_S is a maximum of linear functions, hence convex, and invariant under G.
Averaging normalized w over G preserves D(w)=1 and does not increase any C_S.
Thus restricting to point-orbit-constant weights loses no strength for this
grouped relaxation. Write w(x)=t_O on a point orbit O. For each group and each
actual phase tuple, the integer row coefficient is

\[
 \left|O\cap\bigcup_{m\in S}(a_m\bmod m)\right|.
\]

Minimize sum_S y_S subject to all such rows <= y_S,
sum_O |O|t_O=1 and t_O,y_S>=0. Duplicate rows may be removed. This generalizes
the singleton-resource quotient mechanism; it is not a statement about the
optimality of a floating-point solve.

For two phases a modulo m and b modulo n, their intersection is empty unless
a=b modulo gcd(m,n). In the compatible case it is one class modulo lcm(m,n).
This gives a fast inclusion-exclusion calculation of each union row. The
primary proof checker instead enumerates literal progression unions.

## Certified case at period 10080

Use (modulus,residue) pairs:

```
[(8,0),(9,0),(10,5),(12,10),(14,7),(15,1),(16,4),(18,12),(20,17),
 (21,7),(24,2),(28,1),(30,23)]
```

These 13 classes have minimum exactly eight and LCM 5040. At L=10080 there
are 65 eligible divisors at least eight, 52 unassigned resources and 3092
uncovered points. Pair (40,42), (32,35), (45,56), (36,70); leave every other
resource in its own singleton group. There are 48 disjoint resource groups.

The 90 Cartesian boxes in `certificate.json` define positive integer weights
on 2664 uncovered points. A box `[b_32,b_9,b_5,b_7,t]` assigns weight t to x
when bit x modulo P of b_P is set for P=32,9,5,7. Boxes are disjoint. Direct
integer enumeration gives:

| Quantity | Exact value |
| --- | ---: |
| Demand D(w) | 99820 |
| Sum of individual capacities | 100917 |
| C_{40,42} | 10508 |
| C_{32,35} | 9828 |
| C_{45,56} | 7474 |
| C_{36,70} | 9460 |
| Other 44 singleton capacities | 62511 |
| Sum of joint capacities | 99781 |

The strict gap is 39. Joint counting saves 1136 over the individual capacities
for the SAME weight vector. The latter do not certify this case. Uniform
residual capacity is 3390 > 3092, giving total upper bound 10378 >= 10080;
the earlier unweighted rule also does not certify it.

Consequently no distinct covering with all moduli at least eight dividing
10080 can retain these 13 designated classes. Any finite distinct covering
with minimum exactly eight retaining them has LCM at least **15120**:
its LCM must be a multiple
of 5040; the only positive such multiples below 15120 are 5040 and 10080.
Both divide the excluded period, so the certificate rules out both. No
external minimum-six/seven theorem is used in this implication.

This is a conditional lower bound. It leaves period 10080 unresolved for
other prefixes and does not improve the global interval
10080 <= L_min(8) <= 70560 supplied by the team's
[global lower bound](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_lower_bound)
and [construction](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_prime_lift).

## Verification and trust boundary

`check.py` scans ordinary residues to decode boxes, checks weight support,
counts every remaining singleton phase with literal progressions and all
**7840 actual phase pairs** with set unions. `audit.py` uses CRT box expansion,
phase histograms and the compatible-intersection formula. Both recover the
same capacities and the SHA-256 of ALL ordered phase-pair counts:

```
823aa43657cff16522dd00abfcc02e5fd19ee00903b26014beee60f8e2ec0071
```

The audit also checks 912 small modulus-pair cases and 102116 literal phase
pairs, including incompatible and divisibility cases. The exact checks use
Python's standard library; neither uses a solver or orbit classification.
The trust boundary is ordinary Python integer execution and the unformalized
finite union-bound proof. The small supplied certificate is sufficient;
the exploratory search tree is not a proof dependency and is not published.

Optional `generate.py` discovers weights by a one-thread bounded LP, using
the sibling residual-weight-duals orbit helper. It reconstructs integers and
calls the literal checker before emitting anything. Different degenerate
optima can yield different valid vectors. LP status, numerical objectives
and time limits never establish nonexistence.

Primary context: [Zhang–Zhang, arXiv:2607.19029](https://arxiv.org/html/2607.19029)
claims the minimum-seven LCM is 10080; its commercial solver exclusions are
not assumptions here. [Harrington–Klein–Lowrance–Trifonov, arXiv:2605.18644](https://arxiv.org/html/2605.18644)
treat restricted prime support 2,3,5. The team's complementary
[two-tail exclusion](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_two_tails/proof.md)
now rules out all finite minimum-at-least-eight covers on that support with
5-exponent at most one. The present certificate involves prime seven and
addresses a different finite-period frontier.
