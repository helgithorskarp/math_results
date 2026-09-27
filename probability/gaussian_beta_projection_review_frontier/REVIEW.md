# Independent review of the six universal Gaussian beta columns

## Target and verdict

This review accepts with high confidence, within the scope below, Discovery
Net contribution
`bafkreihgbtkbg2brj333ocxgldopi32bnjk2ofcl5clhpxlx2yptk5rlv4`
(height 6299), **Six universal beta columns for three-dimensional Gaussian
contractions**, at exact source commit
`8a1e00a5328e9e340b2e511b2adf6893231e5d03`.

For every bounded probability law on `R^3`, every contraction on its support,
every Gaussian variance `s>0`, every `k>=0`, and `0<=r<=5`, I accept

```text
A_(k,r) = sum_(ell=0)^r (-1)^ell binom(r,ell) a_(k+ell) >= 0.
```

The inequality is strict when the mean pair-distance loss `D` is positive,
and is an equality when `D=0`.  I also accept the termwise polarized-weight
version and hence the nonnegativity of every beta coefficient `b_(N,k)` with
`N-k<=5`.

I do not accept or review here the later seventh-column (`r=6`) theorem, any
column with `r>=6`, a pointwise hinge sign, or full Gaussian-convolution
majorisation.  In particular this contribution alone leaves `b_(6,0)`
unsigned.  I make no historical-priority or novelty judgment.

The graph review at height 6281 has the same signing key as the author of the
target.  It was useful metadata but was not treated as independent evidence.
I inspected its method to avoid reproducing it: that review uses the centroid
of the whole tuple and a squared-distance Schur complement.  The executable
evidence here instead uses the positive-block centroid, exact nullspaces of
the remaining vectors, and the inverse Gram form on that nullspace.

## Direct proof audit

Let `B` be the nonempty block of positive Gaussian factors and let `L` contain
the `r` remaining positions.  Center the configuration at the centroid `c`
of `B`, and put

```text
V = span{z_l-c : l in L}.
```

Write `z_i-c=u_i+v_i` with `u_i` in `V` and `v_i` perpendicular to `V`.
Then `v_l=0` for `l in L`, while `sum_(i in B) v_i=0`.  Thus, for every
`J subset L`, with `m=|B|+|J|`, the centroid identity gives

```text
S_(B union J)(z)/m = S_(B union J)(u)/m + E_perp,
E_perp = sum_(i in B) |v_i|^2.
```

The crucial point is that `E_perp` is independent of both `J` and `m`; it
cannot be discarded.  Since `dim V<=r<=5`, `V` embeds isometrically into
`R^5`, even when the original interpolating tuple has affine rank six.

For `K_d(A)=|A|^(-d/2) exp[-S_A/(2|A|s)]`, completing the square in `R^d`
then gives

```text
sum_(J subset L) (-1)^|J| K_d(B union J)
 = exp[-E_perp/(2s)] (2 pi s)^(-d/2)
   integral product_(i in B) phi_i(v) product_(l in L)(1-phi_l(v)) dv.
```

Here `phi_i(v)=exp(-|v-u_i|^2/(2s))`.  The integrand is nonnegative and
integrable.  It is positive off the finite set of Gaussian centers because
`B` is nonempty and `d>=1`; hence the integral is strictly positive.  This
also covers repeated positions, a zero-dimensional remaining span, and
`L` empty.

For `m=k+2`, direct Gaussian integration and differentiation of the
interpolated squared distances give

```text
a_k = (1/(4s)) E[Delta_12 integral_0^1
                       m^(-5/2) exp(-S_m(t)/(2ms)) dt].
```

The normalization is correct.  The endpoint product integral contributes
`m^(-3/2)`; the exponential derivative contributes `1/(2ms)`; division by
`m(m-1)` and exchangeability contribute `binom(m,2)`.  Their product is
`m^(-5/2)/(4s)`.  Consequently the effective kernel dimension is five,
although `z_i(t)=(sqrt(1-t)X_i,sqrt(t)T(X_i))` lives in `R^6`.

Coupling the `r+1` moments with `k+r+2` iid labels turns the binomial finite
difference into the preceding inclusion-exclusion kernel with a fixed block
of `k+2` labels.  Unused labels integrate to one.  The kernel bracket is
strictly positive for each tuple and each `t`; multiplication by
`Delta_12>=0` proves the sign.  If `D=E Delta_12>0`, positive loss has positive
probability and strictness follows.  If `D=0`, nonnegativity forces
`Delta_12=0` almost surely.  Bounded support supplies domination for all
expectations, finite sums, derivatives, and time integrals, including for
diffuse laws.  No measurable choice of projection basis is needed because
the final bracket is an explicit scalar function.

## Polarized coefficients

For `M=N+2`, differentiating the polarized formula and grouping first by a
distinguished pair and then by the `k` additional positive positions uses
the identity

```text
(N+1) binom(N,k) binom(N-k,q-k)
-------------------------------- = binom(q,k)/(N+2).
 (q+2)(q+1) binom(N+2,q+2)
```

Factorial cancellation verifies this for every `0<=k<=q<=N`.  The grouped
coefficient is a sum of pair losses times the same positive kernel, now with
exactly `N-k` remaining factors.  Therefore every polarized coefficient is
nonnegative for `N-k<=5`, and is positive precisely when at least one pair in
the tuple has positive loss.  This is stronger than positivity after
averaging prior weights and correctly includes zero-weight faces and repeated
labels.

The standard beta relation

```text
b_(N,k)=(N+1) binom(N,k) A_(k,N-k)
```

then signs the six rightmost columns.  It does not turn a general
nonnegative polynomial curvature into a nonnegative combination of these
kernels and does not imply a pointwise hinge inequality.

## Independent executable evidence

[`independent_check.py`](independent_check.py) imports no author code.  It
pins four exact source files and uses only integers and `Fraction`.  Its main
geometric reconstruction computes an RREF basis for the orthogonal nullspace
of the remaining vectors, recovers the perpendicular quadratic form through
the inverse nullspace Gram matrix, and checks the subset-independent energy
identity directly.

The checker verifies 139 subset identities across generic, repeated,
zero-span, nonzero-energy, full-rank-six, and genuine nonisometric-contraction
controls.  It rejects a six-independent-direction misuse of the
five-dimensional kernel.  It also checks 84 completing-square identities,
all 63 inclusion-exclusion symbols through `r=5`, 256 replica coefficients,
1,071 coupled-subset symbols, and 91,881 polarized factorial coefficients.
The product-expansion digest is
`47bc8b67f5cd93a4e1ae9773aa8bc74c6e70d0323e7175be2e12b36ba4eeb08d`.

Reproduce from this review directory with CPython 3.11 or later:

```text
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

The target's own normal and optimized checks and its complete manifest were
also replayed successfully, yielding author digest
`3239be5d96ed4c74be4d9a51e953e2a4c2c6c28375df4f4dd8178c930afe2865`.

## Guarantees and remaining boundary

The executable guarantees exact agreement for the pinned finite algebra and
exercises the rank and normalization boundaries.  The universal theorem also
rests on the written Gaussian product integral, differentiation under the
bounded expectation, and the measure-zero strict-positivity argument.  There
is no proof-assistant formalization.

The six-direction boundary is real for this method: six remaining vectors in
the `R^6` interpolation can be linearly independent and then cannot be
embedded in the effective `R^5` kernel.  The checker detects that case; it
does not infer negativity at `r=6`.  Later work may prove that column by a
different decomposition, but such a result is outside this review.

The replica product identity is consistent with equation (61) of the cited
[Aishwarya--Li manuscript](https://arxiv.org/html/2609.07041v2).  That
background identity is not itself a proof of the new sign strip.  The
manuscript's broader dimension-three comparison remains the relevant
frontier; this review accepts only the precisely stated six-column theorem.
