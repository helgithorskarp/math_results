# Uniform analytic upper bound for critical tree-stacking counts

Author: Rowan, studio-researcher-4, researcher.
Campaign: Human-authorized Colloquium, 2026-10-05.
Version: rowan_upper_v1, prepared in workday6.

This is an analytic proof component. The parameter lemma below is
unconditional; its tree application has two explicit imported hypotheses:
the exact sibling-classification formula and the maximizing-parent budget.
Their full proofs and audits belong to separate components. This document
does not certify those imports, the lower construction, or the complete
global asymptotic. Another researcher must check this exact new version.

## 1. The integer-parameter lemma

Let \(n\geq3\) be an integer and let \(P\) be a nonempty finite set with
\(|P|\leq n\). For each \(p\in P\), suppose that \(\ell_p,d_p,X_p\) are
integers satisfying

\[
 \ell_p\geq0,\qquad 1\leq d_p\leq n,\qquad X_p\geq1,                 \tag{1}
\]
\[
 X_p\leq2(n-1)2^{\ell_p},                                         \tag{2}
\]
\[
 n\geq \ell_p+1+\frac95d_p-\frac45d_p2^{-\ell_p}.                   \tag{3}
\]

Define

\[
 B=\sum_{p\in P}\binom{X_p+d_p-1}{d_p-1}.
\]

**Lemma.** Under (1)--(3),

\[
 \log_2 B\leq \frac5{36}n^2+6n.                                   \tag{4}
\]

All constants and estimates are uniform in \(P,\ell_p,d_p,X_p\).
There is no lower bound on a positive height and no height cutoff.

**Proof.** Fix \(p\) and write \(\ell=\ell_p,d=d_p,x=d-1\).
Rearranging (3) and multiplying by \(5\ell/9\) gives

\[
 \ell d\leq\frac59\ell(n-1-\ell)+\frac49\ell d2^{-\ell}.             \tag{5}
\]

For every nonnegative integer \(\ell\),

\[
 \ell2^{-\ell}\leq\frac12.
\]

At \(\ell=0\) the quantity is zero. For \(\ell\geq1\), the ratio of
successive terms is \((\ell+1)/(2\ell)\leq1\), so its maximum is attained
at \(\ell=1,2\). Completing the square in the other term of (5) yields

\[
 \ell x\leq\ell d
 \leq\frac5{36}(n-1)^2+\frac29n
 \leq\frac5{36}n^2+\frac29n.                                     \tag{6}
\]

This controls the exponentially small budget correction by a linear
quantity uniformly, including at fixed small heights.

If \(x=0\), its binomial term is one. If \(x\geq1\), put \(m=X_p+x\).
The elementary inequalities

\[
 \binom m x\leq\frac{m^x}{x!},
 \qquad
 x!\geq(x/e)^x
\]

hold for integer \(m\geq x\geq1\). For the second, monotonicity of
\(\ln t\) gives

\[
 \ln(x!)=\sum_{k=1}^x\ln k
 \geq\int_1^x\ln t\,dt
 =x\ln x-x+1
 \geq x\ln x-x.
\]

By (2), \(2^\ell\geq1\), and \(x\leq n\),

\[
 m\leq2(n-1)2^\ell+x\leq3n2^\ell.
\]

Consequently

\[
 \log_2\binom{X_p+x}{x}
 \leq\ell x+x\log_2(3en/x).                                      \tag{7}
\]

For \(r=x/n\in(0,1]\), the function
\(\phi(r)=r\ln(3e/r)\) has derivative
\(\phi'(r)=\ln(3/r)>0\). Therefore

\[
 x\log_2(3en/x)\leq n\log_2(3e)<4n.                               \tag{8}
\]

The last strict bound uses \(e<3\) and \(3e<9<16\), not a
floating-point approximation. For example, the series
\(e=2+\sum_{k\geq2}1/k!\) is strictly less than
\(2+\sum_{k\geq2}2^{1-k}=3\), since \(k!\geq2^{k-1}\) and some
inequalities are strict.

Every summand, including the \(x=0\) case, is at most
\(2^{(5/36)n^2+(38/9)n}\), by (6)--(8). Since there are at most \(n\)
summands and \(\log_2n\leq n\) for integer \(n\geq1\),

\[
 \log_2 B
 \leq\frac5{36}n^2+\frac{38}9n+\log_2n
 \leq\frac5{36}n^2+\frac{47}9n
 \leq\frac5{36}n^2+6n.
\]

This proves (4). \(\square\)

## 2. Exact tree interface and the degree-potential identity

Let \(T\) be a finite \(n\)-vertex tree. A legal pebbling move removes two
pebbles from a vertex and places one at an adjacent vertex. A stacked
configuration has nonempty support consisting of exactly one vertex;
already stacked configurations need zero moves. Define
\(\operatorname{stack}(T)\) to be the least integer \(k\geq2\) such that
every mass-\(k\) configuration can be stacked.

Let \(N(T)\) count the nonstackable functions
\(c:V(T)\to\mathbb Z_{\geq0}\) of mass
\(\operatorname{stack}(T)-1\), individually, without an automorphism quotient.
For \(n\geq3\), let \(L\) be the graph leaves, let
\(L_p=\{z\in L:z\sim p\}\), and put \(d_p=|L_p|\).

For an oriented edge \(u\to v\), define the structural deficit

\[
 a_{u\to v}=
 \begin{cases}
 1,&\deg_T(u)=1,\\
 3+2\sum_{w\sim u,\ w\ne v}a_{w\to u},&\deg_T(u)>1.
 \end{cases}                                                     \tag{9}
\]

For a parent \(p\) of graph leaves, set
\(X_p=(a_{p\to z}-1)/2\), where \(z\in L_p\).
The recurrence shows that this value is independent of the chosen sibling
leaf. The exact sibling-classification input identifies the relevant
parents \(P^*\) as those for which their leaves attain the maximum threshold
score, and gives the formula

\[
 N(T)=\sum_{p\in P^*}\binom{X_p+d_p-1}{d_p-1}.                     \tag{10}
\]

Precisely, the score of such a leaf is
\(E(z)=a_{p\to z}+|L|=1+2X_p+|L|\). The imported threshold theorem
states that the maximum of these leaf scores is \(\operatorname{stack}(T)\).
Thus \(P^*\) is a nonempty subset of the graph-leaf parents maximizing
\(X_p\). Keep every tied maximizing parent. Formula (10), including the
exhaustiveness of the classified configurations, is an import here, not a
consequence of the estimates in Section1.

Let \(C=\{u:\deg_T(u)>1\}\) be the nonleaf core. For \(n\geq3\), it is a
nonempty connected subtree: the internal vertices of a path between
nonleaves are nonleaves. Every graph-leaf parent belongs to \(C\).
Define the **core eccentricity**

\[
 \ell_p=\max_{u\in C}\operatorname{dist}_T(p,u).
\]

It is an integer at least zero. It is distinct from the structural deficit
\(a_{p\to z}\) and from full-tree eccentricity.

**Identity.** For every graph-leaf parent \(p\),

\[
 X_p=\sum_{u\in C}\deg_T(u)\,2^{\operatorname{dist}_T(p,u)}.         \tag{11}
\]

**Proof.** If \(B\) is the \(u\)-side component after removing \(uv\),
induction on its size in (9) gives

\[
 a_{u\to v}
 =1+\sum_{\substack{w\in B\\\deg_T(w)>1}}
       \deg_T(w)\,2^{\operatorname{dist}_T(v,w)}.                  \tag{12}
\]

For a graph leaf \(u\), the sum is empty and the identity is immediate.
Otherwise \(u\) has \(k=\deg_T(u)-1\) children. Each child contributes its
constant one and its descendant sum. The constant part of (9) is
\(3+2k=1+2\deg_T(u)\). The factor two on every descendant sum increases
its distance exponent by one, exactly changing the basepoint from \(u\)
to \(v\). This proves (12).

Apply (12) to \(p\to z\) with \(z\) a graph leaf. Its \(p\)-side component
contains every nonleaf, and
\(\operatorname{dist}_T(z,u)=1+\operatorname{dist}_T(p,u)\) for each
\(u\in C\). Subtract one and divide by two to obtain (11).
\(\square\)

In particular, \(X_p\) is a positive integer. The tree degree sum gives

\[
 X_p\leq 2^{\ell_p}\sum_{u\in C}\deg_T(u)
 \leq2(n-1)2^{\ell_p}.                                           \tag{13}
\]

Use full-tree degrees in (11)--(13), not degrees within \(C\).
Also \(1\leq d_p\leq n\) and \(|P^*|\leq n\).

## 3. The consumed structural budget and the tree upper implication

The structural input needed here is the following exact statement:
for every \(p\in P^*\),

\[
 n\geq\ell_p+1+\frac95d_p-\frac45d_p2^{-\ell_p}.                    \tag{14}
\]

**Tree upper implication.** Assume the threshold/classification input
described with (10) and the universal maximizing-parent input (14).
Then every such tree of order \(n\geq3\) satisfies

\[
 \log_2 N(T)\leq\frac5{36}n^2+6n.                                 \tag{15}
\]

**Proof.** Formula (10), identity (13), and budget (14) match exactly the
integer-parameter lemma with \(P=P^*\). \(\square\)

The implication (15) remains conditional on the two imported mathematical
inputs until their respective component proofs and exact-version internal
checks are supplied. Its analytic estimates impose no core-endpoint,
uniqueness-of-maximizer, minimum-height, or automorphism assumption.

## 4. Compatibility with the stronger full-eccentricity budget

For a nonstar tree and \(p\in P^*\), write
\(H_p=\operatorname{ecc}_T(p)\). Then

\[
 H_p=\ell_p+1.                                                    \tag{16}
\]

Indeed, every graph leaf is adjacent to a core vertex, so the full distance
is at most \(\ell_p+1\). A core vertex \(q\) farthest from \(p\) is an
endpoint of the nontrivial core. It has one core neighbor and full degree
at least two, hence has a graph-leaf neighbor at distance \(\ell_p+1\)
from \(p\). This gives equality. For a star centered at \(p\), the
same equality is \(1=0+1\).

The stronger nonstar budget offered by the separate structural component is

\[
 (d_p-1)(1-2^{1-H_p})
 \leq\frac54(n-1-d_p-H_p).                                       \tag{17}
\]

Substitute (16), multiply by four, and rearrange:

\[
 n\geq\ell_p+\frac65+\frac95d_p
       -\frac45d_p2^{-\ell_p}+\frac45\,2^{-\ell_p}.                 \tag{18}
\]

Its right side exceeds that of (14) by
\(1/5+(4/5)2^{-\ell_p}>0\). Thus the exact stronger nonstar budget
(17) supplies the consumed weaker input (14).
This is only an algebraic interface conversion; it does not prove (17).
The full-eccentricity and core-eccentricity conventions must not be swapped.

## 5. Boundaries, global maximum, and checking scope

For a star of order \(n\geq3\), the center is its only leaf parent,
\(\ell_p=0\), \(d_p=n-1\), and \(X_p=n-1\) by (11). Budget (14)
holds with equality, so this case is covered directly without using (17).
The imported formula gives the exact star count
\(\binom{2n-3}{n-2}\). A summand with \(d_p=1\) always equals one;
all ties were retained in the sum bounded in Section1.

For \(T=K_2\), a mass-two configuration \((1,1)\) is nonstackable, and
the other mass-two configurations are already stacked. Every mass-three
configuration is either already stacked or has piles of sizes two and one;
a move from the size-two pile stacks it. Consequently
\(\operatorname{stack}(K_2)=3\), \(N(K_2)=1\), and (15) holds at \(n=2\)
without the core/parent-budget conventions.

If the two imports hold universally at their stated scopes, maximizing
(15) over all \(n\)-vertex trees gives

\[
 \log_2 M(n)\leq\frac5{36}n^2+6n\qquad(n\geq2).
\]

There are finitely many tree isomorphism types of a fixed order, and the
counts are invariant under relabeling, so the maximum is attained.
The counts themselves are of individual vertex functions, not automorphism
orbits. This provides only the upper half of Statement B242.
Neither an eventual all-order lower bound nor the full shared asymptotic
is proved by this component.

The new-version internal checker should independently inspect Sections1--5:
the uniform budget correction, factorial/entropy estimate and constant;
the recurrence-to-full-degree identity; exact \(P^*\)/count/height interfaces;
the algebraic (17)-to-(14) conversion; and the star, \(d=1\), ties and \(K_2\)
boundaries. The classification's exhaustiveness and the universal structural
proof remain separate imports and checks.

## Provenance

The sibling classification, structural deficit recurrence, degree-potential
identity and the factorial/entropy method are prior work. This component
exposes the analytic implication and its exact universal input interface;
it makes no historical-priority or optimal-linear-constant claim.

- Inherited sibling source, unchanged immutable version:
  https://github.com/helgithorskarp/math_results/blob/d4c0ebbc94ca2855f4fdc547549eed41d63d704c/tree_stacking_extremal_classification/README.md
  (SHA256 725400c0263838bb584fca6a2951ff8fd75a31619bb1394201e08940144fcbf8).
  Graph artifact:
  bafkreigrlfot45gncrzuggfqitcuxbwmxdwto2kav4srp47b6zbmslfl5u.
- Inherited degree-potential/core source at the corrected immutable commit:
  https://github.com/helgithorskarp/math_results/blob/80b058418b869fcee4762ae8d4ec930acc33e7a2/tree_stacking_global_growth/README.md
  (SHA256 02c41193ae367eae230456b0aaea79d9180e1d6cf6f2f6a4c066e5d06b56ee89).
  Graph artifact:
  bafkreig3oqhdokuty7lzkshxkua2ukcbrm672naprwkxpbz6opmnnh3qzu.
- The committed restricted-family linear-remainder review already uses
  factorial/entropy estimates:
  bafkreih76pzukitjoutfawrvr5hpldol2uwl2bov6qfr5noiy2cnlpazem.
- The weaker budget was proposed as Nova203(C) and separately internally
  checked at its selection-feasibility scope by Iris218. The stronger
  nonstar budget was proposed in Atlas206 and separately internally checked
  at its selection-feasibility scope by Nova217. These old checks do not
  certify new structural or assembled source versions.
- The earlier frozen Rowan conditional note had SHA256
  f39ad2a74c4a4a17789fd0541dd48a0056565340f67ee264417371810404bca0;
  Iris231 checked that earlier exact input only. This expanded source
  requires its own internal check.
