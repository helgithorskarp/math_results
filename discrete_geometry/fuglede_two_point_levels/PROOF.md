# Two-point levels: spectral descent or a common binary character

All groups are additive. Write `Z_n = Z/nZ` and `zeta_n = exp(2 pi i/n)`.
The character indexed by `(u,s)` on `Z_n x Z_p` is
`chi_(u,s)(a,j) = zeta_n^(u a) zeta_p^(s j)`.
A set `A` is spectral if a set `Lambda` of `|A|` distinct characters gives
pairwise orthogonal columns on `A`. The square character matrix then has
orthogonal rows as well. A tiling `A + T = G` always means unique representation.

Let `p` be prime, `n >= 2`, and `gcd(n,p)=1`. Suppose

\[
A=\bigcup_{j\in\mathbb Z_p}\{(a_j,j),(b_j,j)\},\qquad a_j\ne b_j\pmod n.
\tag{1}
\]

A **level** fixes the second coordinate. A full prime fiber fixes the first
coordinate and contains all `p` second coordinates; (1) does not require one.
Set `Delta_j = b_j-a_j mod n`, using its representative in `{1,...,n-1}`.

## Theorem

The set (1) is spectral if and only if at least one of the following holds.

1. **Common binary character.** The integer `n` is even and all `Delta_j`
   have the same binary valuation `t`, with `t < v_2(n)`.
2. **Base descent.** The projection `pi:A -> Z_n` is injective, and `pi(A)`
   is a spectral set of cardinality `2p` in `Z_n`.

More precisely, any spectrum occupying at least two second-coordinate levels
forces alternative 1. Any spectrum occupying only one such level forces
alternative 2. No claim is made that these alternatives are disjoint, or that
every spectrum in alternative 1 has product form.

In alternative 1 an explicit spectrum and tiling complement are

\[
\Lambda_t=\{0,n/2^{t+1}\}\times\mathbb Z_p,
\qquad
T_t=\{(x,0):0\le x<n,\ x\bmod 2^{t+1}<2^t\}.
\tag{2}
\]

Consequently, if `Z_n` has no spectral set of cardinality `2p`, then (1) is
spectral exactly when alternative 1 holds, and every such spectral set tiles
by (2). The base exclusion is a hypothesis here, not a general divisibility
assertion about spectral cardinalities.

## Three elementary facts

**Cyclotomic coefficients.** If `c_j in Q(zeta_n)` and
`sum_j c_j zeta_p^(h j)=0` for `h != 0 mod p`, all `c_j` are equal.
Indeed `Q(zeta_n,zeta_p)=Q(zeta_np)` has degree `p-1` over `Q(zeta_n)`,
because `gcd(n,p)=1` and `phi(np)=phi(n)(p-1)`. The minimal polynomial is
`1+X+...+X^(p-1)`; permuting the coefficients by `j -> h j` proves the claim.

**Two-root rigidity.** A nonzero sum `q=R+S` of two unit complex numbers
determines their unordered pair, with repetitions allowed. Since
`conj(q)=q/(RS)`, their product is `q/conj(q)`; they are the roots of the
resulting quadratic. This fact does not apply to the zero sum.

**Reduction of roots.** In `Z[zeta_n]`, choose any maximal ideal over `p`.
Such an ideal exists: reducing the monic polynomial `Phi_n` modulo `p`
gives a nonzero finite ring with a maximal ideal. Distinct `n`th roots of
unity have distinct reductions when `p` does not divide `n`. Otherwise their
quotient `eta != 1`, of order `d | n`, would reduce to 1, and
`1+eta+...+eta^(d-1)=0` would reduce to `d=0` in characteristic `p`, a
contradiction. Roots are units, so taking their quotient is valid.

Here is the pairing consequence used below. For four `n`th roots `R,S,T,U`,
put

\[
C_0=R\overline T+S\overline U,\qquad
C_1=R\overline U+S\overline T.
\]

If `0<k<p` and `k C_0+(p-k) C_1=0`, then `C_0=C_1=0`.
Reduce the equality modulo the chosen maximal ideal:

\[
0=k(C_0-C_1)=k(R-S)(\overline T-\overline U).
\]

Since `k` is nonzero in the residue field, reduction of roots shows `R=S`
or `T=U` already in the original field. Thus `C_0=C_1`, and the original
characteristic-zero equality gives `p C_0=0`. This proves the consequence.

## Necessity: a spectrum on multiple levels

For `d in Z_n`, define

\[
f_j(d)=\zeta_n^{d a_j}+\zeta_n^{d b_j}.
\]

If `(u,s),(v,r)` are in a spectrum and `s != r`, orthogonality and
cyclotomic coefficients give

\[
f_0(u-v)=f_1(u-v)=\cdots=f_{p-1}(u-v).
\tag{3}
\]

If a difference between frequencies on different levels has common value
zero in (3), it is a common antipodal character for all the pairs in (1).
Otherwise all such values are nonzero, and proceed as follows.

There are `2p` frequencies and only `p` levels, so two distinct frequencies
`(u,s),(v,s)` occupy the same level. Since the spectrum occupies multiple
levels, choose a third `(w,r)` with `r != s`. Set `d_1=u-w`, `d_2=v-w`.
By (3) and two-root rigidity, for every point level `j` the unordered
`d_1` character values are a fixed pair `{R,S}`, and the unordered `d_2`
values are a fixed pair `{T,U}`. Relabel the two points on each level so
that their `d_1` values are `(R,S)`. Their `d_2` values are then either
`(T,U)` or `(U,T)`. When a pair has equal entries either labeling can be
used; the following identity is unaffected.

The `u-v=d_1-d_2` character sum on a level is accordingly either `C_0` or
`C_1`. If `k` levels use the first matching, the orthogonality of the two
frequencies on level `s` reads

\[
k C_0+(p-k)C_1=0.\tag{4}
\]

If `k=0` or `k=p`, every actual level sum is the same, and (4) makes it
zero. If `0<k<p`, the pairing consequence makes both possible sums zero.
Thus in every case there is some `d != 0 mod n` with

\[
f_j(d)=0\quad\hbox{for every }j.\tag{5}
\]

The first case above supplies its cross-level difference `d`; in the second
case `d=u-v` is nonzero since the frequencies are distinct on the same level.

Equation (5) means `zeta_n^(d Delta_j)=-1`. Hence `n` is even and
`d Delta_j = n/2 mod n`. Write `s_2=v_2(n)`. Reducing this congruence modulo
`2^s_2` shows

\[
v_2(d)+v_2(\Delta_j)=s_2-1.
\]

Here take the representative `1 <= d < n`; the congruence itself ensures
both valuations are below `s_2`. All the differences therefore have the
same valuation `t=s_2-1-v_2(d)<s_2`. This establishes alternative 1.

## Necessity: a spectrum on one level

Write `Lambda=B x {s}`. If two different points of `A` have equal first
coordinate, the corresponding rows of the square character matrix are
proportional, contrary to row orthogonality. Thus `pi` is injective.
Deleting the unit row factors `zeta_p^(s j)` leaves the character matrix
of `(pi(A),B)` in `Z_n`. This is a spectral pair of size `2p`, proving
alternative 2.

## Sufficiency and tiling

In alternative 2 a spectrum `B` for `pi(A)` lifts to `B x {0}` on `A`.

In alternative 1, `Delta_j` is an odd multiple of `2^t`. With
`delta=n/2^(t+1)`, we have `zeta_n^(delta Delta_j)=-1` on every level.
Two frequencies of (2) with different first coordinates are therefore
orthogonal level by level. Those with equal first coordinates and distinct
second coordinates have inner product `2 sum_j zeta_p^(h j)=0`.
There are `2p` frequencies, proving spectrality.

Let `H_t={x in Z_n: x mod 2^(t+1)<2^t}`. Addition by any `Delta_j`
interchanges this residue half and its complement, because
`Delta_j=2^t mod 2^(t+1)`. Thus `{0,Delta_j}+H_t=Z_n` uniquely.
Translating by `a_j` gives `{a_j,b_j}+H_t=Z_n` uniquely on every level.
Since `T_t=H_t x {0}`, this proves the asserted tiling. Notice that the
same complement works for arbitrary offsets `a_j`.

## Consequence in Z/2310Z

Identify `Z_2310` with `Z_210 x Z_11` by ordinary residues. Suppose a set
`A` contains exactly two points in each residue class modulo 11.
Then

\[
A\text{ is spectral}
\quad\Longleftrightarrow\quad
A\text{ contains exactly one point in every residue class modulo }22.
\tag{6}
\]

To exclude base descent, use Kiss--Malikiosis--Somlai--Vizer,
*Fuglede's conjecture holds for cyclic groups of order pqrs*, Theorem 1.4;
see [the precise source alignment](SOURCES.md). A spectral set of size 22
in `Z_210` would tile that group, implying `22 | 210`, which is false.
Since `v_2(210)=1`, the theorem forces an odd difference in every level,
equivalently one even and one odd point in each residue class modulo 11.
That is precisely a complete set of residues modulo 22, proving (6).

Every set in (6) tiles by the fixed subgroup `22 Z_2310` and has spectrum
`105 Z_2310`, the annihilator of that subgroup. This eliminates the whole
balanced two-point-level family from the possible 22-point counterexamples.
It makes no assertion that arbitrary 22-point spectral sets have balanced
levels, and does not settle the general `Z_2310` problem.

## A necessary boundary and a distinct family

Coprimality cannot be dropped even from the descent-or-binary statement.
In `Z_6 x Z_3` take

\[
\begin{split}
A&=\{(0,0),(4,0),(0,1),(1,1),(1,2),(3,2)\},\\
\Lambda&=\{(b,b\bmod3):0\le b<6\},\\
T&=\{(0,0),(4,1),(2,2)\}.
\end{split}
\]

The group `T` has order 3, `A` is a transversal of its cosets, and
`Lambda=T^perp`. Thus `A` is spectral and tiles by `T`. Its level differences
are `4,1,2`, which fail the binary condition, and its first-coordinate
projection is not injective. The checker verifies the literal character
inner products and all translations without assuming a cyclic CRT map.

At `(n,p)=(210,11)`, the example
`A_j={2j,2j+1}`, `0<=j<11`, satisfies (6) and contains **no** full prime
fiber. It demonstrates that the present family is not contained in the
earlier full-prime-fiber family. The two theorems also impose different
base exclusions; no unqualified logical generalization is claimed.

## Verification boundary

The argument above is the universal proof. `verify.py` provides exact finite
corroboration and boundary checks, not a proof of an infinite classification.
It exhaustively searches spectra of small balanced sets by character zeros,
checks found spectra and explicit spectra using independent Ramanujan traces,
and checks the two-matching identity by both exact arithmetic methods.
Neither method uses floating point to decide a root sum. `expected.json`
records the complete declared test scope. No formal proof assistant or
independent mathematical review is claimed.
