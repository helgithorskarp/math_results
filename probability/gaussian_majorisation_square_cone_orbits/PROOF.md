# Full Gaussian majorisation for an asymmetric square-cone family

Exact computer-assisted author proof, 26 September 2026. Independent
mathematical review and proof-assistant formalization are pending.
The finite certificate is essential: it is verified by two different exact
algorithms, not inferred from numerical sampling. The general
three-dimensional conjecture remains open.

## 1. The previously obstructed nine-point family

Use the following order of vectors:

\[
 \begin{split}
 A&=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),\\
 B&=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)),\\
 X&=(0,A,-B),\qquad Y=(0,A,B),\\
 p^*&=(8,12,7,15,44,21,11,23,43)/184.
 \end{split}                                                    \tag{1}
\]

Let \(T\) fix the origin and the four \(A_i\), and send \(-B_j\) to
\(B_j\). It preserves every point's norm. Within either cluster it is
an isometry, and between clusters

\[
 |A_i+B_j|^2-|A_i-B_j|^2=4A_i\cdot B_j\in\{0,8\}.             \tag{2}
\]

Thus it is a contraction of its support, with a global 1-Lipschitz extension
by Kirszbraun's theorem. Of the 36 unordered pairs, 28 distances are
preserved and eight squared distances decrease by eight.

For a probability vector \(p=(p_0,\ldots,p_8)\), write

\[
 \mu_p=p_0\delta_0+\sum_{i=1}^4p_i\delta_{A_i}
                         +\sum_{j=1}^4p_{4+j}\delta_{-B_j},
 \qquad \nu_p=T_\#\mu_p.
\]

**Theorem A.** If

\[
                 \boxed{\quad\|p-p^*\|_1\le\frac1{552},\quad} \tag{3}
\]

then, for every Gaussian variance \(s>0\) and every threshold \(a>0\),

\[
 \boxed{\quad
 \int_{\mathbb R^3}(\mu_p*\gamma_s-a)_+\,dx
 \le \int_{\mathbb R^3}(\nu_p*\gamma_s-a)_+\,dx.
 \quad}                                                       \tag{4}
\]

Here \(\gamma_s\) has covariance \(sI_3\). Thus full majorisation holds
at all variances on a full eight-dimensional neighborhood of weights.
The radius is sufficient, not claimed optimal.

In particular, (3) contains the entire radius-\(1/4000\) weight family
in the team's [asymmetric bridge obstruction](../gaussian_atomic_bridge_obstruction/PROOF.md).
That result proves that this smaller family has no center-law martingale
comparison under any separate endpoint isometries, even after adding common
isotropic Gaussian noise. The prescribed matching admits no continuous
contracting motion in five dimensions, and deterministic common-output
decompositions do not evade that obstruction. Those statements remain valid.
Our proof instead compares finite arrays of **density values after
convolution**.

The team's subsequent [high-variance certificate](../gaussian_asymmetric_eventual_majorisation/PROOF.md)
proved this comparison at the central weights for s >= 13200, and on a
radius-1/25000 weight ball for s >= 16896. Theorem A removes those variance
restrictions and contains both weight classes. That certificate supplies
context; its numerical and asymptotic estimates are not premises here.

## 2. An elementary finite correlation-to-hinge lemma

Let \(E\) be a finite set with an involution \(j\mapsto\bar j\), and
let \(\preceq_A,\preceq_B\) be partial orders on \(E\). A set is
upper for an order if containing \(i\) and having \(i\preceq j\)
forces it to contain \(j\). Suppose

\[
 |S\cap U|\ge |S\cap\bar U|
 \quad\text{for every }A\text{-upper }S\text{ and }B\text{-upper }U.
                                                                  \tag{5}
\]

If nonnegative arrays \((\alpha_j),(\beta_j)\) are respectively
increasing for these orders, then for every real \(h\),

\[
 \sum_{j\in E}(\alpha_j+\beta_j-h)_+
 \ge\sum_{j\in E}(\alpha_j+\beta_{\bar j}-h)_+.                \tag{6}
\]

To prove it for \(h>0\), use the exact identity

\[
 (u+v-h)_+-(u-h)_+-(v-h)_+
   =\int_0^h\mathbf1_{\{u>t\}}\mathbf1_{\{v>h-t\}}\,dt
 \qquad(u,v\ge0).                                             \tag{7}
\]

The separate \(u\)- and \(v\)-terms cancel on summing, because the
involution permutes the \(\beta\)-array. The two strict superlevel sets
in the integral are upper, so (5) gives (6). Boundary equalities in the
arrays cause no issue. For \(h\le0\) both sides of (6) are equal by
linearity. Adding a common constant to both sums, or multiplying them by
a common nonnegative scalar, preserves the assertion.

This is the elementary upper-orthant/supermodular comparison principle,
proved here to avoid an external stochastic-order premise. It is not
claimed as a new general principle.

## 3. Polynomial orders on 48 signed permutations

Let \(G\) be the group of all signed coordinate permutations in
\(\mathbb R^3\), of size 48. Label its elements from 0 to 47 by first
listing permutations \(\pi\) of \((0,1,2)\) lexicographically, then
sign triples \(\epsilon\in\{-1,1\}^3\) lexicographically, with action

\[
                  (gx)_i=\epsilon_i x_{\pi_i}.                 \tag{8}
\]

Central negation \(g\mapsto-g\) is the fixed-point-free involution
\(j\mapsto j\mathbin{\mathrm{xor}}7\) on these labels.

For \(C=A\) or \(B\), and four nonnegative weights \(q\), put

\[
                   F_C^q(x)=\sum_{i=1}^4q_i e^{C_i\cdot x}.
                                                                  \tag{9}
\]

Every signed-permutation orbit contains a vector with
\(x_1\ge x_2\ge x_3\ge0\). On this chamber make the substitution

\[
 e^{x_1}=uvw,\qquad e^{x_2}=vw,\qquad e^{x_3}=w,
 \qquad u,v,w\ge1.
                                                                  \tag{10}
\]

Let \(e=g^TC_i\). Multiplying its exponential monomial by the common
positive monomial \(uv^2w^3\) yields

\[
 u^{e_1+1}v^{e_1+e_2+2}w^{e_1+e_2+e_3+3}.                    \tag{11}
\]

All three exponents are nonnegative. Their degree bounds are
\((2,4,6)\), for both lists of centers. Set \(u=1+U,v=1+V,w=1+W\).
The resulting polynomial

\[
 P_{C,g}^{q}(U,V,W)
    =uv^2w^3 F_C^q(gx)                                      \tag{12}
\]

has 105 possible monomial positions and coefficients linear in \(q\).
There are only finitely many coefficients, and all calculations below
use integers and rational numbers.

For a pair of group labels \(g,h\) and one monomial position \(k\),
denote the coefficient of \(P_{C,h}^q-P_{C,g}^q\) by
\(d_{C,g,h,k}\cdot q\), where \(d_{C,g,h,k}\in\mathbb Z^4\).
Use the integer base vectors

\[
                  a^*=(12,7,15,44),\qquad b^*=(21,11,23,43).
                                                                  \tag{13}
\]

Define \(g\preceq_C h\) if, for every coefficient position, either
\(d_{C,g,h,k}=0\) as a full linear form, or its value at the corresponding
base vector in (13) is strictly positive. The strict clause excludes
accidental equalities that would not persist under weight perturbation.
The definitions yield partial orders; reflexivity, antisymmetry, and
transitivity are also checked explicitly.

The two order matrices are stored compactly in
[CERTIFICATE.json](CERTIFICATE.json). Row \(i\) is the integer bit mask of
all labels \(j\) with \(i\preceq_C j\), including \(i\). The
constructor regenerates every entry from (8)--(13); the separate checker
verifies every claimed coefficient inequality from repeated polynomial
multiplication without importing the constructor.

## 4. The finite certificate and the uniform weight margin

**Certificate lemma.** The orders just defined have these exact properties:

| Quantity | Order A | Order B |
|---|---:|---:|
| Comparable ordered pairs, including the diagonal | 875 | 871 |
| Upper sets, including the empty and full sets | 1541 | 1645 |
| Minimum nonzero coefficient value at the base divided by \(184\|d\|_\infty\) | \(1/552\) | \(1/184\) |

Furthermore, for all 2,534,945 pairs of their upper sets,

\[
                    |S\cap U|-|S\cap(-U)|\ge0.                \tag{14}
\]

Here is the complete finite verification procedure and why it suffices.
Each individual coefficient in (11) after shifting is a product of three
binomial coefficients. The constructor builds the four individual-center
coefficient columns at each of 48 group elements, examines all ordered
pairs, and uses the rule following (13). The minimum margins in the table
are computed over every nonzero coefficient of every retained comparison.
Witnesses for their attainment are included in the compact certificate.
For example, an A coefficient has linear form \((2,3,0,-1)\), whose value
at \(a^*\) is one and whose infinity norm is three.

The first algorithm enumerates A-upper sets by disjoint branching on a
remaining vertex. Including it forces all its successors; excluding it
forces exclusion of all its predecessors. These branches exhaust and
partition the possible upper sets, so the recursion is complete. For
each resulting upper set \(S\), it constructs a bijection

\[
       (-S)\setminus S\ \longrightarrow\ S\setminus(-S),
       \qquad n\longmapsto p\text{ with }n\preceq_B p.        \tag{15}
\]

An exact augmenting-path algorithm finds these monotone matchings for all
1541 sets. The verifier checks every returned endpoint, order relation,
uniqueness, and cardinality. There are 1539 nonempty matchings, containing
25,463 matched edges in total. If \(U\) is B-upper, a matched negative
vertex in \(U\) has its positive partner in \(U\), proving (14) for
every such \(U\) without assuming a matching theorem as a black box.

The second algorithm imports no constructor code. It reconstructs the
polynomials by repeated multiplication by \(1+U,1+V,1+W\), verifies
the coefficient margins, and generates upper sets by breadth-first
addition: a vertex can be added after all its strict successors have been
added. Every upper set has such an ordering, so this enumeration is also
complete. It then directly checks all 1541 times 1645 integer count
differences in (14). The minimum is zero. The digest of the lexicographically
ordered count list, storing each gap plus 48 in one byte, is

```text
720d164fd164fe9028ccc1fef96779ce3b3709af3d18cd458f41bea1adb06d73
```

The digest is a compact reproduction identifier, not a substitute for
performing the finite checks. The independent calculation uses neither
the first upper-set recursion nor its matching algorithm. Intentional
reversal/corruption of an order is rejected. Both programs fail loudly
and retain all checks under optimized Python.

Now suppose (3). For any nonzero coefficient form in an A comparison,

\[
 \begin{split}
 d\cdot(p_1,p_2,p_3,p_4)
 &\ge d\cdot(a^*/184)-\|d\|_\infty\|p-p^*\|_1\\
 &\ge \|d\|_\infty(1/552-\|p-p^*\|_1)\ge0.
 \end{split}                                                   \tag{16}
\]

The B comparison has the larger margin \(1/184\) and satisfies the
same conclusion. Identically zero forms stay zero. Thus every coefficient
of every ordered difference remains nonnegative throughout (3), including
its boundary. Since \(U,V,W\ge0\), (12) gives

\[
 g\preceq_A h\Longrightarrow F_A^{p_A}(gx)\le F_A^{p_A}(hx),
 \quad
 g\preceq_B h\Longrightarrow F_B^{p_B}(gx)\le F_B^{p_B}(hx)     \tag{17}
\]

for every \(x\) in the whole chamber. No grid in \(x\) is used.

## 5. Transfer to every Gaussian variance and every hinge

Fix \(s>0\). For a point \(x\) in the chamber define

\[
 \alpha_g=e^{-1/s}F_A^{p_A}(gx/s),\qquad
 \beta_g=e^{-3/(2s)}F_B^{p_B}(gx/s).                           \tag{18}
\]

The factors come from \(|A_i|^2=2\) and \(|B_j|^2=3\).
They are common within each cluster and positive, so (17) makes these
arrays increasing in the two certified orders. The Gaussian densities are

\[
 \begin{split}
 (\mu_p*\gamma_s)(gx)&=\gamma_s(x)[p_0+\alpha_g+\beta_{-g}],\\
 (\nu_p*\gamma_s)(gx)&=\gamma_s(x)[p_0+\alpha_g+\beta_g].
 \end{split}                                                   \tag{19}
\]

Equation (14) and the lemma in Section 2 apply with
\(h=a/\gamma_s(x)-p_0\). This threshold may be negative, which was
included in that lemma. Multiplying (6) by \(\gamma_s(x)>0\) yields

\[
 \sum_{g\in G}((\nu_p*\gamma_s)(gx)-a)_+
 \ge\sum_{g\in G}((\mu_p*\gamma_s)(gx)-a)_+.                 \tag{20}
\]

Every orbit meets the chamber and the sums in (20) are group invariant.
Consequently (20) holds for every \(x\in\mathbb R^3\), including chamber
walls with repeated orbit points. Integrating and using orthogonal
invariance of Lebesgue measure shows that each sum integrates to 48 times
its corresponding hinge. The hinges are finite, bounded by total mass one.
This proves Theorem A.

This step uses an exact functional inequality on each orbit. It assumes
neither a continuous contracting motion nor an entropy-to-majorisation
implication, and involves no asymptotic or numerical Gaussian integration.

## 6. Homogeneous weight cones and arbitrary radial laws

The probability ball is an explicit subset of a larger usable class.
For \(C=A,B\), define the closed polyhedral cone

\[
 \mathcal K_C=\{q\in[0,\infty)^4:
       d_{C,g,h,k}\cdot q\ge0
       \text{ for all }g\preceq_C h\text{ and all }k\}.        \tag{21}
\]

The finite list of defining forms is generated from the compact certificate
and (11). By definition, membership gives every order comparison (17).
The proof of Theorem A therefore works for **any** nonnegative origin
mass and cluster weights \(p_A\in\mathcal K_A,p_B\in\mathcal K_B\)
whose combined mass is one. In particular, the two cluster masses are
arbitrary and independent.

There is also a nonatomic extension. Let \(L<\infty\), let
\(\eta_A,\eta_B\) be any probability laws on \([0,L]\), and let
\(q_A(r),q_B(t)\) be measurable probability vectors in
\(\mathcal K_A,\mathcal K_B\), respectively, almost everywhere.
Choose arbitrary \(c,m_A,m_B\ge0\) with \(c+m_A+m_B=1\), and put

\[
 \begin{split}
 \mu={}&c\delta_0
   +m_A\int\sum_i q_{A,i}(r)\delta_{rA_i}\,d\eta_A(r)\\
   &+m_B\int\sum_j q_{B,j}(t)\delta_{-tB_j}\,d\eta_B(t).
 \end{split}                                                   \tag{22}
\]

**Theorem B.** The map fixing \(rA_i\) and sending \(-tB_j\) to
\(tB_j\) is a contraction on this support, and \(\mu*\gamma_s\)
is majorised by \((T_\#\mu)*\gamma_s\) for every \(s>0\).

The cross squared-distance loss is
\(4rtA_i\cdot B_j\in\{0,8rt\}\), including unequal radial shells;
within each cluster distances are preserved. The pieces intersect only at
zero, where the map is consistent. Kirszbraun again gives a global extension.

For the analytic part, replace (18) by

\[
 \begin{split}
 \alpha_g&=m_A\int e^{-r^2/s}
                 F_A^{q_A(r)}(rgx/s)\,d\eta_A(r),\\
 \beta_g&=m_B\int e^{-3t^2/(2s)}
                 F_B^{q_B(t)}(tgx/s)\,d\eta_B(t).
 \end{split}                                                   \tag{23}
\]

Each nonnegative rescaling of a chamber point stays in the chamber, so
every integrand preserves its corresponding finite order. Positive
integration preserves those inequalities too. Bounded support ensures
finite values, and the proof (19)--(20) applies verbatim.

An explicit sufficient condition in (22), avoiding cone membership tests,
is

\[
 \left\|q_A(r)-\frac{(12,7,15,44)}{78}\right\|_1\le\frac1{234},
 \qquad
 \left\|q_B(t)-\frac{(21,11,23,43)}{98}\right\|_1\le\frac1{98}.
                                                                  \tag{24}
\]

These constants are the same coefficient margins after normalizing the
cluster masses: \((184/78)(1/552)=1/234\) and
\((184/98)(1/184)=1/98\). Both conditional weight classes have nonempty
three-dimensional interior. Neither a small cluster mass nor a variance
restriction is imposed.

## 7. Scope, reproducibility, and the remaining problem

Theorem A settles the full Gaussian comparison for the team's explicit
asymmetric obstruction family, including its entire previously certified
\(1/4000\) weight neighborhood. Theorem B gives arbitrary bounded radial
laws and radius-dependent directional weights in explicit cones. The
earlier motion, covariance, and common-output obstructions are compatible
with this result: they exclude different proof mechanisms.

All assertions about arbitrary spatial points, variances, thresholds,
weights in the stated neighborhoods, and radial measures follow from
the polynomial positivity and analytic reduction. The essential finite
claim (14) is checked exhaustively. This distinguishes the result from
an exploratory grid, a finite list of successful Gaussian integrals, or
a purely formal manipulation of an unproved sign.

No claim is made for arbitrary weights outside (21), arbitrary
three-dimensional contractions, or new Kneser--Poulsen cases. In particular,
equal-radius comparisons for complete symmetric ray layers can already
follow by vertical folding and relabeling. Gaussian comparison for a new
weight family is not itself a novelty claim about those support volumes.

Run both exact algorithms and the manifest check as documented in
[README.md](README.md). All source, finite data, and trust boundaries are
included. [SOURCES.md](SOURCES.md) credits the configuration, the prior
obstructions, their independent review, and the primary problem source.
