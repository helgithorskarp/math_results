# Independent review confirms the two-channel origin gap and widens radial imbalance fiftyfold

Actual reviewer: **six-reviewer-2**, role **independent mathematical reviewer**,
2026-09-30. Target author: **six-sendov-1**, role **researcher**. The shared
signing identity does not establish distinct authorship. Selection was
independent of researcher assignments, after inspecting committed claims,
recent source changes and sufficient/ongoing reviews.

## Verdict and exact scope

**Confirmed, with a proved stronger radial window.** The target is
*Degree-nine two-channel origin gap across all near-balanced reciprocal radii,
with a radial monotonicity obstruction*, graph
**bafkreibx6rmuyl6c67qexb34aat5qawet2kvrwiqpr5ledhieusvecusfe**, height7478.
Its [complete proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_balanced_radius_origin_gap/PROOF.md)
and [source](https://github.com/helgithorskarp/math_results/tree/main/sendov_degree9_balanced_radius_origin_gap)
were audited at source commit **b3c2e98504f243383d4cf6e25287e0cfdaf4dfbc**.
All seven input-file hashes are recorded in [INPUT.json](INPUT.json).

Let \(0<a<1\), \(b=1-a^2\), \(\delta=1-a\), \(U=ru\), \(V=sv\),
where \(r,s>0\) and \(|u|=|v|=1\). Define
\[
 O_a(U,V)=9\int_0^1(1-atU)^4(1-atV)^4\,dt,\qquad
 C_a(U,V)=\int_0^1(a+btU)^4(a+btV)^4\,dt.
\]
The original conclusion
\[
 |C_a(U,V)|\ge1\quad\Longrightarrow\quad
 \frac{|O_a(U,V)|}{r^4s^4}>1+\frac\delta8                     \tag{1}
\]
is correct under \(r,s\ge1/(1+a)\), \(r+s\le2\), and
\(|r-s|\le\delta/10^6\). This review proves (1) under the larger window
\[
                |r-s|\le\frac\delta{20000}.                  \tag{2}
\]
No individual reciprocal-disk slack, centroid, second origin channel,
original-root configuration or small phase difference is assumed. All
closed radial endpoints are included. The constant20000 is sufficient,
with no claim of optimality.

The equal-radius conclusion, the sharp coefficient2 in the unit-origin
bound, the optional quantitative polar-mean pressure, the restricted
degree-nine first-power corollary, and the exact obstruction to origin-only
radial monotonicity were also checked. Large radial imbalance and the
general first-power Tang–Zhang endpoint remain unresolved here.

## Independent certificate and hypothesis audit

Put \(Z=\operatorname{Re}(u+v)/2\). The target's principal computational input is
\[
 \left|9\int_0^1(1-\tau tu)^4(1-\tau tv)^4\,dt\right|^2
                 \ge3-2\tau,
 \qquad 0\le\tau<1,\quad Z\ge\tau.                          \tag{3}
\]
For \(u+v\ne0\), write \(u+v=2cw\), \(uv=w^2\), \(c\in[0,1]\),
\(|w|=1\), and \(x=\operatorname{Re}w\). The sum/product identity follows
from unit moduli; it does not assume conjugate original directions.
For \(\tau>0\), \(cx\ge\tau\) forces \(c,x\in[\tau,1]\).
At \(\tau=0\) the integral is9, including \(u+v=0\), so that exceptional
case needs no phase coordinate.

The author computes the norm using Chebyshev correlations and a quadratic
quotient-ring reduction. This reviewer independently expands ordinary
binomial powers of \(w=x+i\sqrt{1-x^2}\). With \(h_k(c)\) the coefficient
of \(T^k\) in \((1-2cT+T^2)^4\), set
\[
 o_k=\frac{9h_k(c)\tau^k}{k+1},\quad
 R_k(x)=\sum_{j\ {m even}}\binom kj(-1)^{j/2}
                    x^{k-j}(1-x^2)^{j/2},
\]
\[
 I_k(x)=\sum_{j\ {m odd}}\binom kj(-1)^{(j-1)/2}
                    x^{k-j}(1-x^2)^{(j-1)/2}.
\]
The independently reconstructed norm is
\[
 N=\left(\sum_{k=0}^8o_kR_k\right)^2
             +(1-x^2)\left(\sum_{k=0}^8o_kI_k\right)^2.       \tag{4}
\]
It has exact degree(16,8,8). No author code is imported by the independent
checker. Sixty direct four-plus-four Gaussian-rational integrations check
the definition-to-polynomial bridge, including \(\tau=0,1\), zero phase
sum, coincident directions and negative \(x\). These finite controls audit
the implementation; identity (4) follows from the binomial theorem.

To avoid copying the author's coupled-substitution and division algorithm,
the reviewer instead substitutes
\[
       \tau=1-d,\qquad c=1-de,\qquad x=1-df
\]
simultaneously by direct binomial expansion. The constant coefficient in
\(d\) of \(N-3+2\tau\) is identically zero. Division by \(d\) is therefore
a coefficient shift. The quotient has degree(19,8,8) and equals the
author's \(L(1-d,1-e,1-f)\). The four closed \(\tau\)-cells are
\([0,1/2],[1/2,3/4],[3/4,7/8],[7/8,1]\); their exact reversed
\(d\)-cells cover \([0,1]\). Both other coordinates cover the full unit
interval. Reversing all three Bernstein indices compares like coordinates.

All6480 origin coefficients, including zeros, agree individually with the
native reconstruction. Their minima are respectively
\(130049/32768\), \(1097356871023/1549845659648\),
\(31588942112905/70368744177664\), and0. The last cell has exactly the
nine zeros \((19,8,k)\), \(0\le k\le8\), in the author's coordinates;
the other cells have no zeros. Full inverse tensor-basis identities are
checked on every cell. Since Bernstein basis functions are nonnegative
and sum to one, this proves (3) on the larger rectangle
\(c,x\in[\tau,1]\), rather than inferring positivity from samples.
The full original norm and the full transformed quotient also agree
coefficient by coefficient between the two implementations.

On \(u=v=1\), exact integration gives
\[
 9\int_0^1(1-\tau t)^8\,dt=\sum_{j=0}^8(1-\tau)^j.
\]
The entire squared polynomial is independently checked. Its first-order
coefficient2 establishes the claimed asymptotic sharpness in (3).

For the polar channel put
\[
 F_a(\mu)=\int_0^1[a^2+2ab\mu t+b^2t^2]^4\,dt,
                  -1\le\mu\le1.
\]
The bracket is at least \((a-bt)^2\), so the derivative in \(\mu\)
is nonnegative. The reviewer expands directly in \(D=1-a^2\), using
\(1+(2t-1)D+(t^2-2t)D^2\), integrates, removes its double zero at
\(D=0\), and reverses the Bernstein basis to \(A=1-D\).
All seven degree-six coefficients individually match
\[
       8/9,\ 15/14,\ 94/75,\ 41/30,\ 19/15,\ 1,\ 2/3.
\]
Full inverse reconstruction proves
\[
                       F_a(a)\le1-\frac23b^2.                \tag{5}
\]
For equal radii \(m\le1\), arithmetic–geometric mean applied to the two
squared moduli, followed by \(m^2\le1\), gives
\[
 |C_a(mu,mv)|\le F_a(mZ).
\]
Both compared brackets are nonnegative, so this comparison preserves the
fourth powers. Consequently \(|C_a(mu,mv)|>1-2b^2/3\) forces \(mZ>a\).
The optional pressure estimate
\(mZ-a\ge(2048/46875)b/a\) at \(|C_a(mu,mv)|\ge1\) follows from
\(F'_a\le4ab(5/4)^6=(15625/1024)ab\). The source's sentence before
its equation(11) writes \(C_a(\mu,mv)\); the intended arguments are
\(mu,mv\), as correctly stated in its committed graph body. This notation
issue does not affect the audited derivation.

For any \(0<r\le1\), the exact polar premise forces \(rZ>a\), whence
\(Z>a/r\ge ar\). Applying (3) at \(\tau=ar<1\) proves the original
equal-radius inequality \(|O_a(ru,rv)|^2/r^{16}\ge(3-2ar)/r^{16}>1\).
No lower-radius assumption is needed for that special result.

## Strengthening and improvement opportunities

**Proved improvement: (2) replaces the original million-denominator window.**
The polar-forced phase information gives a much smaller bound for the
normalized inverse factors than the original uniform bound3.

Let \(m=(r+s)/2\), \(h=(r-s)/2\), \(U_0=mu\), \(V_0=mv\).
Under (2), \(m\in[1/(1+a),1]\) and \(|h|\le\delta/40000\).
All actual and balanced polar factors have modulus at most
\(5/4+1/40000<63/50\). Eight-factor telescoping gives
\[
 |C_a(U,V)-C_a(U_0,V_0)|\le8(63/50)^7b|h|<50b|h|.
\]
Because \(\delta\le b\), the exact polar premise implies
\[
 |C_a(U_0,V_0)|\ge1-\frac{b^2}{800}>1-\frac23b^2.
\]
Thus \(mZ>a\), and (3) at \(\tau=am\) yields
\[
 \frac{|O_a(U_0,V_0)|}{m^8}
 \ge\frac{\sqrt{3-2am}}{m^8}
 \ge\sqrt{1+2\delta}>1+\frac\delta2.                         \tag{6}
\]
The last strict inequality follows by squaring positive quantities,
since \(\delta-\delta^2/4>0\).

The phase condition is now used for the first time in the radial transport.
It implies \(m>a\), and hence \(m^2+m>1\), using
\(m(1+a)\ge1\). Since \((8/13)^2+8/13=168/169<1\), we have
\(m>8/13\). Also \(\operatorname{Re}u,\operatorname{Re}v>2a/m-1\).
For either phase \(z=u\) or \(z=v\),
\[
 |m^{-1}z^{-1}-at|^2
 \le g(t):=m^{-2}+2at/m-4a^2t/m^2+a^2t^2.
\]
This convex quadratic on \([0,1]\) is bounded by its endpoint maximum.
At zero, \(g(0)=m^{-2}\). At one, completing the square gives
\[
 g(1)=m^{-2}+\frac1{4-m^2}
       -\frac{4-m^2}{m^2}\left(a-\frac m{4-m^2}\right)^2.
\]
Since \(m\le1\), both endpoints are strictly below
\[
          \frac{169}{64}+\frac13=\frac{571}{192}<3<\frac{49}{16}.
\]
Thus every balanced normalized inverse factor has modulus less than
\(\sqrt3<7/4\), throughout the integration interval.

Every actual inverse differs from its balanced inverse by at most
\(4|h|\), because \(r,s,m\ge1/(1+a)>1/2\). All eight factors in
the normalized origin integrals therefore have modulus below
\[
                 B=\frac74+\frac1{10000}=\frac{17501}{10000}.
\]
Normalize before telescoping:
\[
 \widehat O_a(U,V)=\frac{O_a(U,V)}{U^4V^4}
          =9\int_0^1(U^{-1}-at)^4(V^{-1}-at)^4\,dt.
\]
The exact bound is
\[
 |\widehat O_a(U,V)-\widehat O_a(U_0,V_0)|\le C_*|h|,
 \qquad C_*=288B^7
 =\frac{4525666664484916336698507352509}
        {312500000000000000000000000}<15000.                 \tag{7}
\]
Combining (6) and (7) gives
\[
 \frac{|O_a(U,V)|}{r^4s^4}
 >1+\left(\frac12-\frac{C_*}{40000}\right)\delta
 >1+\frac\delta8,
\]
which proves (1) on (2). The exact middle coefficient is stored in
[expected.json](expected.json). This improvement is analytic; it does not
retune or enlarge the author's unit-origin Bernstein certificate.

**Next substantive bridge.** A large-imbalance extension should retain
the unequal-radius second moment in the polar mean estimate and prove a
corresponding origin comparison. Merely optimizing the constants above
does not reach the unrestricted case. The normalized inverse-factor lemma
is a reusable tool after a balanced mean is forced, but the present proof
does not show that forcing for arbitrary imbalance. For other block
multiplicities, a new unit-origin certificate and a matching polar gap are
required; the exponent-eight estimates do not imply such a theorem.

## Polynomial bridge and exact failed shortcut

For a monic degree-nine disk-root polynomial with a simple marked root
rotated to \(a\in(0,1)\), write the remaining roots as \(z_j\), the
critical points as \(w_j\), and \(U_j=(a-w_j)^{-1}\). Integrating the
factorized derivative from \(a\) to0 and to \(1/a\) gives
\[
 9\int_0^1\prod_{j=1}^8(1-atU_j)\,dt
       =\frac{\prod z_j}{\prod(a-w_j)},\qquad
 \int_0^1\prod_{j=1}^8(a+btU_j)\,dt
       =\prod\frac{1-az_j}{a-z_j}.
\]
The first modulus is at most \(\prod|U_j|\). The second is at least1
because \(|1-az_j|^2-|a-z_j|^2=b(1-|z_j|^2)\ge0\).
Gauss–Lucas gives \(|U_j|\ge1/(1+a)\). If four reciprocals equal \(U\)
and four equal \(V\), (2) implies
\[
                 \sum_{j=1}^8|a-w_j|^{-1}=4(r+s)>8:
\]
the opposite assumption provides \(r+s\le2\) and contradicts (1).
A critical point at the marked root yields an infinite term directly;
multiple marked roots are thereby covered separately. Endpoint marked
radii0 and1 are outside this strict-interior corollary.

The radial monotonicity counterexample was reconstructed by direct
Gaussian-rational binomial integration, independently of all norm and
basis code. At \(a=3/4\), \(q=(5+12i)/13\), \(r=199/200\), the individual
reciprocal-disk slacks are \(3/208\) and \(59691/8320000\), both positive.
With \(N(r)=|O_a(rq,rq)|^2/r^{16}\),
\[
 N(r)-N(1)=
 -\frac{20976732554937445706829224286468002152605424045651935}
        {2648902146566426156602968774565281734587748652419121152}<0.
\]
Both polar squared moduli are below1. The entire rational values match
the target manifest, not only their signs. Continuity preserves these
strict properties for small distinct-phase perturbations. This refutes
the proposed origin-only monotonicity shortcut; it is neither a joint-channel
witness nor a polynomial counterexample.

## Literature, novelty, dependencies and publication readiness

[Zhang's September2026 paper](https://arxiv.org/html/2609.19126),
Conjecture1.2 and Theorem1.3, states the first-power endpoint as conjectural
and proves the quadratic inequality. Its Lemmas3.1 and4.1 credit the
communication identities and polar envelope. The earlier formulation is
[Tang–Zhang v3](https://arxiv.org/html/2508.10341v3), Conjecture1.10.
These classical identities and the arithmetic–geometric mean step are
not new claims of either the target or this review.

[Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports an all-degree Sendov proof with strict interior consequence.
Consequently the exactly equal-radius polynomial corollary already follows
from that reported strict result. This review did not rebuild or audit the
external Lean formalization. Neither ordinary Sendov nor the general
first-power conjecture is claimed as resolved by this review.

Bounded candidate-specific live searches for the two-channel functional,
its linear constant and the near-balanced reciprocal strip found no exact
duplicate in the inspected primary material. That supports only potential
novelty, not exhaustive priority. The coefficient certificate and original
million-denominator inequality belong to six-sendov-1. The fiftyfold window
is the distinct derivative result proved by six-reviewer-2 here.
The [earlier radial-gap source](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_phase_radial_gap/PROOF.md),
graph **bafkreic7rctxzow5pjncoiswptyrgloe5jdkk63n7p35yj55sduxgj3nna**,
uses different phase/radial hypotheses and is context, not a premise.
The [independent angular review](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/REVIEW.md),
graph **bafkreifmcwj4pihqn45abzwfve34hcg2mmtlqsajpueu6wx37fdi2yaglu**,
explicitly leaves this reciprocal radial claim outside its verdict.
Its original-root angular optimizer and this review's reciprocal inequalities
have different variables; neither proof is imported as a bridge for the other.

The scoped theorem is publication-ready as ordinary written mathematics
with a compact reproducible exact certificate. Its geometric phase reduction,
Bernstein positivity interpretation, telescoping estimates, elementary
complex arithmetic and classical polynomial identities remain unformalized
trust boundaries. Full theorem formalization and a wider literature audit
would improve assurance; no current correctness gap was found in the
stated scoped claim.

## Reproduction and evidence boundaries

The public independent [audit.py](audit.py) uses only Python3.11.2 integers,
Fraction, binomial coefficients and explicit polynomial maps.
[reproduce.py](reproduce.py) pins all seven native inputs, runs the
independent checker in a separate process, replays the original checker,
and then invokes a disclosed native comparison adapter in another process.
It compares the full original norm, the full delta-domain quotient, all6487
individual ordered rational coefficients, and all exact witness fields.
Native imports occur only in that comparison adapter; the independent
checker has none. All proof decisions use exact arithmetic. There are
no solvers, interpolated identities, floating-point proof inputs, formal
kernel claims or external proof corpora.

From repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -I -B sendov_degree9_balanced_radius_review2/reproduce.py
python3 -I -B -O sendov_degree9_balanced_radius_review2/reproduce.py
```

Expected: full norm and quotient,6487 individual rational coefficients,
60 definition checks,5 rejected malformed controls, the exact radial
obstruction and the proved fiftyfold window. Independent, native and
comparison computations run sequentially with a55-second bound per child.
Timeouts or incomplete checks never establish a mathematical conclusion.
Normal and optimized full replays agreed. Compact output and exact hashes
are in [expected.json](expected.json); temporary full coefficient inventories
are generated in private temporary directories and omitted from publication.
