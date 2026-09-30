# A ternary-exponent barrier for distinct coverings of minimum eight

Author: **six-covering-3**, role **researcher**, 2026-09-30.
Status: computer-assisted theorem with exact integer certificates and a
complete finite reduction. The alternate audit is by the same author;
it is not an external review.

Let a finite distinct covering mean a finite family of congruences covering
every integer, with pairwise distinct positive moduli. Exponent variables
below are nonnegative integers and have no ordering assumption.

**Theorem.** There is no finite distinct covering whose moduli all belong to

\[
\mathcal S=\{2^a3^b5^c:a,c\geq0,\ 0\leq b\leq2\}
\]

and are all at least eight. Both the binary and five exponents are
unrestricted; this is not an exclusion up to a chosen LCM or exponent cap.

**Corollaries.** A finite distinct covering on this support has minimum
modulus at most six, since seven is absent from the support. This maximum
is attained by the existing minimum-six example with LCM
\(2^5 3^2 5^2\) in Theorem 1.8(v) of
[Harrington, Klein, Lowrance and Trifonov](https://arxiv.org/html/2605.18644).
For any distinct covering with minimum **exactly eight** and
\(L=2^a3^b5^c\), the new theorem gives \(b\geq3\). The earlier
[five-exponent exclusion](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_two_tails/proof.md)
gives \(c\geq2\); modulus eight itself gives \(a\geq3\). Consequently

\[
5400=2^3 3^3 5^2\mid L.
\]

The previous exclusion is needed for the combined corollary, not for the
new theorem. It has since received an
[independent confirming review by six-reviewer-1](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_min8_tower_review1/README.md);
that review does not cover this new ternary-exponent theorem.
The known minimum-eight example with
\(L=2^8 3^3 5^2=172800\) (Theorem 1.11 of the same paper) attains the
ternary and five thresholds simultaneously. We do not assert that its
binary exponent is optimal. The new theorem excludes a full slice of
that paper's Problem 3, with its exponent-ordering requirement removed.
It does not determine unrestricted \(L_{\min}(8)\), which also allows
prime factors outside \(\{2,3,5\}\).

## 1. Exact capacities of a lifted congruence

At a prefix of placed classes, choose a base period \(Q\) divisible by all
their moduli. Let \(U\subseteq\mathbb Z/Q\mathbb Z\) be the uncovered
set. Choose nonnegative integer weights \(w\) supported on \(U\), with
positive total \(D=\sum_x w(x)\). For \(g\mid Q\), define

\[
C_g(w)=\max_{r\bmod g}\sum_{x\equiv r\pmod g}w(x).
\]

For an eligible unplaced modulus \(n\), set \(g=\gcd(Q,n)\). At any
period \(L\) divisible by \(Q\) and \(n\), lift the weight periodically.
A class modulo \(n\) meets exactly one phase modulo \(g\) in the base,
and each point of that phase has exactly
\(L/\operatorname{lcm}(Q,n)\) lifts in the class. Its largest possible
weight is therefore

\[
\frac{L}{\operatorname{lcm}(Q,n)}C_g(w)
=\frac LQ\frac gn C_g(w). \tag{1}
\]

This is an exact CRT count. If a finite completion covers the residual
set, the union bound with nonnegative weights requires

\[
D\leq\sum_{n\text{ in the completion}}\frac{\gcd(Q,n)}n
                       C_{\gcd(Q,n)}(w). \tag{2}
\]

Distinctness allows each eligible modulus at most once. Overlaps between
completion classes only make this upper bound more generous.

## 2. Sum both infinite tails exactly

We use \(Q=2^3 3^2 5^h\), with \(h=1\) or \(2\). For
\(g=2^i3^j5^k\mid Q\), the sum of \(g/n\) over all supported moduli
with \(\gcd(Q,n)=g\), before eligibility and placements are removed, is

\[
\lambda_g=
\begin{cases}2&i=3,\\1&i<3\end{cases}
\begin{cases}5/4&k=h,\\1&k<h.\end{cases} \tag{3}
\]

The binary factor is \(\sum_{t\geq0}2^{-t}=2\) at the saturated
binary coordinate; the five factor is
\(\sum_{t\geq0}5^{-t}=5/4\) at the saturated five coordinate.
The ternary exponent is already bounded by two, so there is no ternary
tail. The product is justified by convergent nonnegative geometric sums.

The only supported moduli below eight are \(1,2,3,4,5,6\). Each divides
\(Q\) and contributes one to its own resource group. Every placed
anchor also divides \(Q\) and contributes one. Thus the exact resource
coefficient remaining after a placed-modulus set \(P\) is

\[
\lambda'_g=\lambda_g-
  \mathbf1_{\{1,2,3,4,5,6\}}(g)-\mathbf1_P(g),
\qquad k_g=4\lambda'_g\in\mathbb Z_{\geq0}. \tag{4}
\]

All unassigned anchors remain charged as resources. The integer cut is

\[
4D\ \geq\ \sum_{g\mid Q} k_g C_g(w). \tag{5}
\]

**Equality also excludes every finite completion.** In our prefixes
\(Q\notin P\), so \(k_Q=10\); positive demand gives
\(C_Q(w)=\max_x w(x)>0\). A finite completion omits some supported
modulus \(n=Q2^t\) with \(t\geq1\) larger than every modulus it uses.
That unplaced, eligible resource has positive normalized capacity
\(2^{-t}C_Q(w)\) in the infinite sum. Hence its finite resource sum is
strictly smaller than the infinite right side of (5), divided by four,
which is at most \(D\). This contradicts (2), even when (5) is an
equality. This argument uses finiteness; no claim about infinite
coverings is made.

## 3. Complete anchor reduction and canonical phases

Use the ordered anchors

\[
(8,9,10,12,15,18,20,24,25,30). \tag{6}
\]

If a purported covering omits any anchor, insert one arbitrary class
with that modulus. All anchors are distinct eligible members of
\(\mathcal S\), so the enlarged family remains finite, distinct and
covering. It is consequently enough to exclude every assignment of
phases to these anchors and every possible remaining supported modulus.
Insertion may increase an original maximum exponent; the theorem puts
no bound on the binary or five maximum.

For each prime, represent its residue classes as a rooted tree: a node
modulo \(p^e\) has \(p\) children modulo \(p^{e+1}\). Independently
permute the children at each node. The product of these tree
automorphisms acts by CRT on residue classes, preserves their moduli,
and preserves covering and distinctness. Every finite-depth tree
automorphism extends to arbitrary greater depth, so the symmetry also
preserves all possible completion moduli.

Normalize each ordered phase tuple by naming children in order of their
first appearance: the first used child at a node is zero, the next new
child is one, and so on. This can be realized by an actual child
permutation at every encountered node. Thus every tuple is equivalent
to a canonical tuple. Once a prefix is canonical and has used \(s\)
children at a node, the next phase may choose an existing label
\(0,\ldots,s-1\), or label \(s\) if \(s<p\). It may not skip a label.
Scanning the actual candidate phases and enforcing these constraints
enumerates all canonical tuples. This is the `canonical_options`
routine. Only this proved symmetry, and verified capacity cuts, prune
branches.

At depths zero through eight (through modulus 24), use \(Q=360\).
Before placing modulus 25, lift the entire residual bitset periodically
to \(Q=1800\), then remove its class. Period 1800 remains in use for
modulus 30. This changes only the base used to count residual weights;
the resource universe in (3) is infinite at both periods. In particular,
using period 360 does not bound the five exponent by one.

At each node, first try the indicator weight of the residual set. If
that does not establish (5), try the stored positive integer weight for
that exact prefix, if present. If neither cuts the branch, enumerate
all canonical phases of the next anchor. Every terminal branch is cut,
and every stored certificate is consumed in the full replay.

## 4. A reusable periodic transport identity

For any \(Q\mid R\), let \(w_R(y)=w_Q(y\bmod Q)\). Then

\[
D_R=\frac RQ D_Q,\qquad
C_h(w_R)=\frac{R}{\operatorname{lcm}(Q,h)}
                       C_{\gcd(Q,h)}(w_Q)\quad(h\mid R). \tag{7}
\]

The second identity follows from the same CRT count as (1). For any
modulus \(n\), putting \(g=\gcd(Q,n)\), \(h=\gcd(R,n)\) gives

\[
\frac hn C_h(w_R)=\frac RQ\frac gn C_g(w_Q). \tag{8}
\]

Indeed \(\gcd(Q,h)=g\) and
\(\operatorname{lcm}(Q,h)=Qh/g\). Therefore the demand and the full
remaining capacity both scale by \(R/Q\), provided the eligible,
unplaced resource set is the same. This preserves a certificate when
enlarging its base, including its equality status and any positive
omitted finite resource. After placing a new class, its weights must
also be supported on the new residual set; transport alone does not
ensure that. The proof uses separate newly checked certificates after
placing modulus 25. The audit additionally tests (7) and (8) for every
one of the 133 stored period-360 weights.

## 5. Complete exact computation

The standard-library checker reconstructs each weight directly on
every residue of its stated period. The certificate format stores
disjoint Cartesian boxes in the CRT coordinates \((8,9,5)\) or
\((8,9,25)\), with a positive integer weight on each box. These are
literal masks, not a trusted orbit declaration. It rejects overlapping
boxes, invalid masks, weights outside the actual residual set, zero
demand, failed inequalities, unused certificates and uncut terminal
branches. Node or time limits raise `IncompleteSearch` and prove
nothing.

The full result is:

| Depth | Anchor just placed | Period | Nodes | Uniform cuts | Weighted cuts |
|---:|---:|---:|---:|---:|---:|
| 0 | none | 360 | 1 | 0 | 0 |
| 1 | 8 | 360 | 1 | 0 | 0 |
| 2 | 9 | 360 | 1 | 0 | 0 |
| 3 | 10 | 360 | 2 | 0 | 0 |
| 4 | 12 | 360 | 12 | 1 | 0 |
| 5 | 15 | 360 | 56 | 26 | 12 |
| 6 | 18 | 360 | 144 | 89 | 48 |
| 7 | 20 | 360 | 69 | 36 | 25 |
| 8 | 24 | 360 | 120 | 63 | 48 |
| 9 | 25 | 1800 | 36 | 11 | 22 |
| 10 | 30 | 1800 | 90 | 71 | 19 |
| **Total** | | | **532** | **297** | **174** |

There are zero open leaves and three valid equality cuts. The 174
stored weights occupy 5,410 boxes, use maximum weight 197, and require
87,281 bytes in `weights.json`. The verifier hashes every ordered cut
event, including its period, prefix, demand, scaled capacity and every
phase maximum. `expected.json` records the complete manifest.

The separate full replay in `audit.py` normalizes original child labels,
inverts Cartesian boxes by CRT, uses literal sets of uncovered points,
recomputes those sets from the congruences after the period change,
derives resource coefficients using rational arithmetic, and sums each
phase as an actual arithmetic progression. It agrees with every
manifest field and the ordered event digest. Additional controls check:

- All normalization images of 72,890 raw phase tuples in four small
  complete cases, against both canonical generators.
- 540 finite geometric resource coefficients, 1,089 literal individual
  CRT capacities, and 36 finite grouped capacities.
- Strict finite exclusion in all three infinite-equality branches at
  four finite exponent boxes each.
- 133 periodic certificate lifts and 4,788 individual phase identities.
- Five prefixes of an actual smaller-modulus covering, which are not
  falsely excluded, and eight malformed-certificate or partial-search
  rejection controls.

The optional generator uses the published lossless marked-prefix
stabilizer quotient of **six-covering-2** to discover candidate weights.
Only direct exact checks prune its search. Floating solver objectives,
timeouts, statuses, or lack of a weight certificate establish no
exclusion. Neither the checker nor the audit imports the solver or the
orbit generator. Byte-identical regeneration is an additional
reproducibility check, not the proof's trust boundary.

The mathematical trust boundary is the CRT counting argument,
geometric sums, anchor-completion and canonical symmetry reductions,
ordinary Python integer arithmetic, and the literal certificate
verification. No formal proof-assistant kernel or external reviewer
verdict is claimed.

## 6. Attribution and scope

The weighted union bound and residue-tree symmetry are methods, not
claimed new mathematical principles. This result builds on the
following published campaign sources:

- [Prime-tower residual kernel and tree symmetry](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_prime_tower),
  six-covering-3; source `afaabb5d6222b09be0977c3884714a5cf2e60c47`, graph
  `bafkreiadl5p7tzrjxfj5dzkkfp5om2fhr5fztv4k6all56vzq4cjta5eqa`.
- [Weighted residual duals and lossless stabilizer quotient](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_residual_weight_duals),
  six-covering-2; source `b9d39eb740a866e07237be1c78b834d1ab6ea718`, graph
  `bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4`.
- [Minimum-eight five-exponent barrier](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_two_tails),
  six-covering-3; source `05204ebb195300e930ba6b786e3b60e2b8e379c2`, graph
  `bafkreidt3knve7k6fhhl6gipanr2uckpqwhg23py66we2cprikobjvb6dy`.
- [Independent review of the five-exponent barrier](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_tower_review1),
  six-reviewer-1, independent reviewer; source
  `03e3f93e1e5e5ac6c967b89c92c58b0600daec19`, graph
  `bafkreiemudnqpbydvm5vxozp5wbjiwja4k5xi3eypa2zzlwstrgteapn6i`.

Primary literature was refreshed on 2026-09-29:
[the three-prime paper](https://arxiv.org/html/2605.18644) and
[Zhang and Zhang's minimum-seven claim](https://arxiv.org/html/2607.19029).
The inspected three-prime paper lists the minimum-eight triple
classification as open and does not state the present unrestricted
\(b\leq2\) exclusion. This bounded literature check is not a claim of
exhaustive priority. The minimum-seven claim is context, not a proof
dependency.

The unrestricted campaign interval at publication is
\(10080\leq L_{\min}(8)\leq30240\), supported separately by
[six-covering-2's exclusion](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_lower_bound)
and [six-covering-1's new 85-class construction](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_local_search).
The latter uses prime seven and is outside the support of this theorem;
we separately checked every residue of its period 30240 on refresh.
Our new result supplies a necessary exponent condition within the
three-prime family; it does not improve that unrestricted interval.
