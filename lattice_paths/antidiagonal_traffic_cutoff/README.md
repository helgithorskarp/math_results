# Antidiagonal traffic anomaly: exact cutoff at 496

## Result

Gil, Liang, Odetola, and Weiner consider monotone north-east lattice paths
from `(0,0)` to `(n,n)` that avoid one point `B`.  When `B` lies on the
antidiagonal, their Proposition 7.2 reduces the possible migration of a
maximum-traffic point from `(1,1)` to a boundary point to the inequality

\[
 R_n(a)=\frac{G(n,a)}{D(n)}>1,
\]

where

\[
 D(n)=\frac1n {2n-2\choose n-1},\qquad
 G(n,a)=\frac{n-2a+1}{n-a}{n\choose a}{n-2\choose a-1}.
\]

They verified that `max R_n(a) < 1` for `496 <= n <= 2000` and conjectured
that it remains below one forever (Conjecture 7.4 in
<https://arxiv.org/abs/2609.01562>).

We prove the conjecture.

**Theorem.** For every integer \(n\ge 496\) and every integer
\(1\le a<n/2\), one has \(R_n(a)<1\).  Consequently, for every obstruction
on `x+y=n`, the maximum traffic is attained at `(1,1)` and `(n-1,n-1)`.
The cutoff is sharp: at `n=495`, `a=240` gives `R_n(a)>1`.

The proof is exact computation for `496 <= n <= 9999`, followed by a
uniform analytic estimate for `n >= 10000`.  The computation uses integers
only and tests one candidate per `n`; the next section proves why that is
complete.

## Proof

Put \(k=n-2a\), so \(k>0\) and \(k\equiv n\pmod 2\), and write
\(\mathcal R_n(k)=R_n((n-k)/2)\).  Direct substitution gives

\[
 \mathcal R_n(k)=
 \frac{2n(k+1)}{n+k}
 \frac{\binom n{(n-k)/2}\binom{n-2}{(n-2-k)/2}}
      {\binom{2n-2}{n-1}}.                                      \tag{1}
\]

### Unimodality and the unique candidate

The adjacent quotient from Lemma 7.3 of the source paper becomes

\[
 \frac{\mathcal R_n(k+2)}{\mathcal R_n(k)}
 =\frac{(n-k)(n-k-2)(k+3)}{(n+k+2)^2(k+1)}.                     \tag{2}
\]

The right side exceeds one exactly when

\[
 F_n(k):=n^2-5n-2-(7n+1)k-2nk^2>0.                             \tag{3}
\]

Moreover,

\[
 F_n(k+2)-F_n(k)=-(8nk+22n+2)<0.
\]

Thus the allowed sequence of \(\mathcal R_n(k)\)'s is unimodal.  Its maximum
is at the first allowed `k` for which `F_n(k) <= 0` (with a harmless tie if
equality occurs).  Since `F_n(k) < 0` whenever
\(k\ge\sqrt{n/2}\), a maximizing `k` always satisfies

\[
 k<K_n:=\sqrt{n/2}+2.                                           \tag{4}
\]

This proves the completeness of the finite verifier.

### A binomial bound

Let \(N\ge2\), let \(0\le k<N\) have the same parity as `N`, and set
\(\epsilon_N=0\) for even `N` and \(\epsilon_N=1\) for odd `N`.  Then

\[
 {N\choose (N-k)/2}
 \le 2^N\sqrt{\frac{2}{\pi N}}
 \exp\!\left(-\frac{k^2-\epsilon_N}{2(N+k)}\right).             \tag{5}
\]

Here is an elementary derivation.  The central estimate

\[
 {N\choose\lfloor N/2\rfloor}
 \le 2^N\sqrt{\frac{2}{\pi N}}                                 \tag{6}
\]

follows from the standard Wallis bound in even dimension.  For odd
`N=2m+1`, reduce it to the even case using
\({2m+1\choose m}=\frac{2m+1}{m+1}{2m\choose m}\); after squaring,
the remaining inequality has positive difference
\(2m^2+m-1/2\).

If `N=2m` and `k=2r`, divide the left side of (5) by the central
coefficient.  Its logarithm is at most

\[
 -\sum_{j=1}^r\frac{2j-1}{m+j}
 \le -\frac{r^2}{m+r}=-\frac{k^2}{2(N+k)}.
\]

If `N=2m+1` and `k=2r+1`, the same argument gives

\[
 -\sum_{j=1}^r\frac{2j}{m+j+1}
 \le-\frac{r(r+1)}{m+r+1}
 =-\frac{k^2-1}{2(N+k)}.
\]

We used only `log(1-x) <= -x`.  This proves (5).

We also need the following lower bound, valid for `m >= 1`:

\[
 {2m\choose m}>
 \frac{4^m}{\sqrt{\pi m}}\exp\!\left(-\frac1{7m}\right).        \tag{7}
\]

Indeed, the Robbins bounds

\[
 \sqrt{2\pi m}(m/e)^m e^{1/(12m+1)}
 <m!<
 \sqrt{2\pi m}(m/e)^m e^{1/(12m)}
\]

give an error exponent greater than

\[
 \frac1{24m+1}-\frac1{6m}
 =-\frac1{8m}-\frac1{24m(24m+1)}> -\frac1{7m}.
\]

Apply (5) with `N=n` and `N=n-2`, apply (7) with `m=n-1`, and use

\[
 \frac12\left(\frac1{n+k}+\frac1{n+k-2}\right)>\frac1{n+k}.
\]

Equation (1) then yields, with \(\epsilon=\epsilon_n\),

\[
 \mathcal R_n(k)<
 \frac{4(k+1)}{\sqrt{\pi n}}\frac n{n+k}
 \sqrt{\frac{n-1}{n-2}}
 \exp\!\left(\frac1{7(n-1)}-\frac{k^2-\epsilon}{n+k}\right).    \tag{8}
\]

### Uniform tail

Let `k` maximize \(\mathcal R_n\), let `K=K_n`, and put
\(c=(1+K/n)^{-1}\).  By (4),

\[
 \frac{k^2-\epsilon}{n+k}
 \ge \frac c n\big((k+1)^2-(2K+2)\big).
\]

Since \(t e^{-ct^2}\le(2ce)^{-1/2}\) for every \(t>0\), (8) implies

\[
 \mathcal R_n(k)<
 \sqrt{\frac8{\pi e c}}\sqrt{\frac{n-1}{n-2}}
 \exp\!\left(\frac1{7(n-1)}+\frac{c(2K+2)}n\right).             \tag{9}
\]

For `n >= 10000`, elementary decimal bounds give

\[
 \sqrt{\frac8{\pi e}}<0.969,\quad
 c^{-1/2}<1.004,\quad
 \sqrt{\frac{n-1}{n-2}}<1.0001.
\]

For completeness: use \(\pi>3.141\), \(e>2.718\), and
`K/n <= 1/sqrt(2n)+2/n < 0.007272`.  The remaining exponent in (9) is less
than

\[
 \frac1{7\cdot9999}+\frac{\sqrt2}{100}+\frac6{10000}
 <0.014765.
\]

The geometric-series bound \(e^x<1/(1-x)\) for `0<x<1` makes its exponential
less than `1.015`.  Therefore the right side of (9) is below

\[
 0.969\cdot1.004\cdot1.0001\cdot1.015
 =0.987567886914<1.                                             \tag{10}
\]

This proves the theorem for `n >= 10000`.  The exact verifier covers the
remaining range and also confirms sharpness at `n=495`.

## Reproduction

Requires CPython 3.11 or later; no third-party packages are used.

```bash
python3 verify_finite_range.py | tee /scratch/antidiagonal-traffic-output.txt
diff -u expected_output.txt /scratch/antidiagonal-traffic-output.txt
```

Expected running time is about one second on a contemporary CPU.  The script
uses exact arbitrary-precision integer comparisons.  It recursively updates
the three central binomial coefficients, checks those recurrences against
`math.comb` at six boundary/checkpoint values, and constructs the two
off-central ratios as products of integers.  No floating-point value is used
for any pass/fail decision; the printed decimal is descriptive only.

## Scope and trust boundary

The infinite tail, unimodality reduction, and completeness reduction are
ordinary mathematical arguments.  The finite bridge trusts CPython's
arbitrary-precision integer arithmetic, `math.comb` at the stated
checkpoints, the short verifier, the operating system, and hardware.  There
is no solver, randomness, floating point in a decision, external dataset, or
large generated artifact.

The result resolves only Conjecture 7.4 for a single point obstruction on the
antidiagonal of a square grid.  It does not classify the curved transition
boundaries away from that antidiagonal, rectangular grids, or extended
obstructions.

## Sources

- Juan Gil, Zhenni Liang, Ayodeji Odetola, and Michael Weiner, *Points of
  maximal traffic on a grid with obstruction*, arXiv:2609.01562 (2026):
  <https://arxiv.org/abs/2609.01562>.
- Herbert Robbins, *A Remark on Stirling's Formula*, American Mathematical
  Monthly 62 (1955), 26--29: <https://doi.org/10.2307/2308012>.
