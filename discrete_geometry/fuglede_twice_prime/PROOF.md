# The twice-prime spectral boundary

All groups are additive. Put `G=Z_n x Z_p`, where `n>=2`, `p>=3` is prime,
and `gcd(n,p)=1`. The character indexed by `(b,s)` is
`(a,j) -> zeta_n^(ab) zeta_p^(js)`. A spectral pair `(A,Lambda)` consists of
equally sized sets whose square character matrix has orthogonal columns;
it then has orthogonal rows too. A level fixes the `Z_p` coordinate.
Projection always means the first-coordinate map to `Z_n`.

## Main theorem

Assume that `Z_n` contains no spectral set of cardinality `p` or `2p`.
A set `A subset G` of cardinality `2p` is spectral if and only if:

1. every level is a pair `A_j={a_j,b_j}`;
2. `n` is even and, for some `0<=t<v_2(n)`, all nonzero differences
   `b_j-a_j mod n` have binary valuation `t`.

The valuation uses the representative in `{1,...,n-1}` and is independent of
the ordering of the pair. Every admitted set has the explicit spectrum and
tiling complement

\[
\Lambda_t=\{0,n/2^{t+1}\}\times\mathbb Z_p,
\qquad
T_t=\{(x,0):0\le x<n,\ x\bmod 2^{t+1}<2^t\}.                 \tag{1}
\]

Thus spectral-to-tiling in `Z_n` implies spectral-to-tiling at cardinality
`2p` in `G`: neither excluded base cardinality divides `n`.
The base exclusions are hypotheses, not an assumed general divisibility
principle for spectral sets. Neither square-free `n` nor `p>n` is required.

### Unconditional structural alternative

For any `2p`-point spectral pair `(A,Lambda)` in `G`, exactly one of these
profile cases occurs:

- Some level of one member is empty. Both projections are injective and
  form a `2p`-point spectral pair in `Z_n`.
- Both members have profile `(2^p)`. Each has the binary form above and
  tiles explicitly.
- One member has profile `(p+1,1^(p-1))` and the other `(2^p)`. A `p`-point
  spectral pair in `Z_n` is obtained by the extraction in Section 5.

These are alternatives for an existing pair; existence of the third case
for coprime parameters is not asserted. Its conclusion is a base spectral
pair, not a tiling claim about the original unbalanced member.

## 1. Cyclotomic and pairing facts

For `c_j in Q(zeta_n)` and `h != 0 mod p`,

\[
\sum_{j=0}^{p-1}c_j\zeta_p^{hj}=0
\quad\Longrightarrow\quad c_0=\cdots=c_{p-1}.                \tag{2}
\]

Indeed, `Q(zeta_np)` has degree `p-1` over `Q(zeta_n)`, so the minimal
polynomial is `1+X+...+X^(p-1)`; reindex by `j -> hj`. Thus two frequencies
on distinct levels have equal character sums on all levels of the opposite
member. This also holds when their first coordinates coincide.

A nonzero sum `R+S` of two unit complex numbers determines their unordered
pair: the product is `(R+S)/conj(R+S)`, determining the quadratic with roots
`R,S`.

For `n`th roots `R,S,T,U`, put

\[
C_0=R\overline T+S\overline U,\qquad
C_1=R\overline U+S\overline T.
\]

If `0<k<p` and `k C_0+(p-k)C_1=0`, then `C_0=C_1=0`. Reduce in
`Z[zeta_n]` modulo a maximal ideal above `p`. Distinct `n`th roots remain
distinct on reduction: otherwise a nontrivial root of order `d|n` reduces
to 1, and its geometric-sum identity gives `d=0` in characteristic `p`,
contrary to coprimality. The displayed equation reduces to

\[
k(R-S)(\overline T-\overline U)=0.
\]

Hence `R=S` or `T=U` already over the complex numbers, so `C_0=C_1`; the
original equation makes both zero.

**Consequence.** Suppose the values of two characters on each pair
`P_j={x_j,y_j}` have fixed nonzero sums. If the characters are orthogonal
on the union of the `p` pairs, they are orthogonal on every pair separately.
Two-root rigidity fixes both unordered value pairs; their `p` inner products
are either `C_0` or `C_1` and sum to zero. If only one value occurs it is zero;
otherwise the preceding argument applies.

These elementary ingredients were combined for two-point levels in the
earlier [fuglede_two_point_levels](../fuglede_two_point_levels/PROOF.md).

## 2. Empty-level projection

If a level of `A` is empty, then for two frequencies on different levels,
(2) makes all sums over `A`'s levels zero. For two frequencies on the same
level, their total first-coordinate inner product is already zero.
Consequently the square matrix, indexed by the original points and frequencies,

\[
H_{(a,j),(b,s)}=\zeta_n^{ab},
\]

satisfies `H* H=2p I` and is invertible. Repeated first coordinates would give
repeated rows or columns, so both projections are injective and form a
spectral pair in `Z_n`. If a level of `Lambda` is empty, use row-column
symmetry. This argument works at any cardinality.

## 3. Only two nonempty profiles

Suppose every level of both members is nonempty. If `A` has a singleton
`{alpha}` and an `r`-point level `{a_1,...,a_r}`, with `2<=r<p`, select one
frequency `(b_j,j)` on each level of `Lambda`. Equation (2) gives

\[
\sum_{i=1}^r\zeta_n^{(b_j-b_k)(a_i-\alpha)}=1\qquad(j\ne k).
\]

The `p` vectors `(zeta_n^(b_j(a_i-alpha)))_(i=1)^r` have Gram matrix
`(r-1)I_p+J_p`, of rank `p`, impossible in `C^r`. This is the earlier
singleton-gap argument, now without a projection-injectivity assumption.

If a profile contains 1, every other entry is 1 or at least `p`. Two entries
at least `p` give total at least `3p-2>2p`. Its only possible form is
`S=(p+1,1^(p-1))`. Without a 1 all entries are at least two and their sum
forces `D=(2^p)`. Apply the same argument to `Lambda`.

## 4. Two one-fat-level profiles are impossible

Suppose both profiles are `S`. Let `{a_1,...,a_(p+1)}` be the fat level of
`A` and `alpha` a singleton coordinate. For a first coordinate `b` of
`Lambda`, set `v_b=(zeta_n^(b(a_i-alpha)))_(i=1)^(p+1)`.

For a difference of `Lambda` points on distinct levels, (2) implies
`zeta_n^((b-c)(alpha_j-alpha))=1` for every singleton coordinate `alpha_j`
of `A`. Subtracting two such differences through a fixed singleton of
`Lambda` gives the same equality for two points on its fat level.
Orthogonality of two fat-level frequencies has no `p`-phase; its normalized
singleton contributions all equal 1. Therefore the `p+1` fat-level vectors
`v_b` have pairwise inner product `-(p-1)` and squared norm `p+1`. Their
sum would have squared norm

\[
(p+1)((p+1)-p(p-1))=(p+1)(-p^2+2p+1)<0\qquad(p\ge3).
\]

This contradiction is the twice-prime specialization of the earlier
block-Gram obstruction; a smaller principal block already suffices here.

## 5. New bridge: paired-level spectral extraction

Suppose `A` has profile `S` and `Lambda` profile `D`. Translate `A` in the
first coordinate so that a singleton is `(0,s)`. Its fat level is on a
different level `t`; write its first coordinates as `U`, with `|U|=p+1`,
and write `Lambda_j={x_j,y_j}`. For every `u in U`, (2) applied to the rows
`(u,t),(0,s)` says that

\[
c_u=\zeta_n^{u x_j}+\zeta_n^{u y_j}                         \tag{3}
\]

is independent of `j`. Put `Z={u in U:c_u=0}` and `N=U\Z`.
Distinct fat-level rows are orthogonal without a `p`-phase. The consequence
in Section 1 makes rows from `N` orthogonal on each pair separately. At most
two nonzero vectors in `C^2` are mutually orthogonal, so `|N|<=2`.

For `z in Z`, its values on each pair are opposite. For any choice of one
point `x_j` per pair, the vectors

\[
w_z=(\zeta_n^{z x_j})_{j=0}^{p-1}
\]

are mutually orthogonal: their inner products are half those of the original
fat-level rows. Thus `|Z|<=p`. If `|N|=0`, this contradicts `|U|=p+1`.
If `|N|=1`, the `p` rows indexed by `Z` already form a square orthogonal
character matrix on the selected first coordinates.

If `|N|=2`, say `N={u,v}`, the unordered pair of `u` values is fixed,
say `{R,S}`, by (3). Here `R!=S`, since otherwise its pairwise inner product
with `v` would be `R conj(c_v)!=0`. Order each pair so that
`zeta_n^(u x_j)=R` and `zeta_n^(u y_j)=S`. Orthogonality with a row `z in Z`
then gives

\[
0=(R-S)\sum_{j=0}^{p-1}\overline{\zeta_n^{z x_j}}.
\]

Thus all `p-1` rows `w_z` are orthogonal to the constant vector. Frequencies
`Z union {0}` give a square orthogonal character matrix on the selected
first coordinates. The added frequency is distinct because `c_0=2`.

In either case the square matrix is invertible, so its columns cannot repeat:
the chosen first coordinates are distinct. We have constructed a `p`-point
spectral pair in `Z_n`. This closes the mixed profile without assuming a
full vertical fiber or inferring a common spectrum from level counts alone.

## 6. Balanced pairs have a common binary character

Suppose both profiles are `D`, and write `A_j={a_j,b_j}`. Cross-level
frequency differences have constant pair sums by (2). If one such sum is
zero, its first-coordinate difference is a common antipodal character.
Otherwise choose two frequencies `(u,s),(v,s)` on one level and any `(w,r)`
on a different level. The characters `u-w` and `v-w` have fixed nonzero
pair sums. Their total inner product is zero by orthogonality of the first
two frequencies. Section 1 makes it zero on every pair. In either case a
nonzero `d in Z_n` satisfies

\[
\zeta_n^{d(b_j-a_j)}=-1\quad\hbox{for every }j.              \tag{4}
\]

Hence `n` is even. With `s_2=v_2(n)`, the congruence
`d(b_j-a_j)=n/2 mod n` gives `v_2(d)+v_2(b_j-a_j)=s_2-1`. The pair
differences have a common valuation `t<s_2`.

Conversely, that condition gives
`zeta_n^((n/2^(t+1))(b_j-a_j))=-1`. Formula (1) is a spectrum: unequal first
coordinates cancel pairwise; equal first coordinates and unequal second
coordinates give a complete prime Fourier sum. Every difference is
`2^t mod 2^(t+1)`, exchanging the two residue halves in (1). Thus all pairs
tile their levels by the same complement. Interchanging the members proves
the binary form for `Lambda` too.

This completes the unconditional alternative. Excluding both base sizes
leaves exactly the balanced alternative, proving the main theorem.

## 7. Order 2310 and exact enumeration

Kiss--Malikiosis--Somlai--Vizer's four-prime theorem proves Fuglede in
`Z_210`. It excludes spectral sets of sizes 11 and 22 there because neither
cardinality divides 210. Using ordinary CRT residues, the theorem gives,
for every 22-element subset `A` of `Z_2310`,

\[
A\text{ is spectral}\quad\Longleftrightarrow\quad
A\text{ contains exactly one element in each residue class modulo }22.
\tag{5}
\]

Every admitted set tiles by `22 Z_2310` and has spectrum `105 Z_2310`, the
annihilator of that subgroup. There are exactly `105^22` such labeled subsets,
not counted up to symmetry. This accounts for the entire size-22 branch.
It is not claimed as a new spectral-to-tiling solution: Liang's August 2026
preprints make broader claims, including all square-free moduli; see SOURCES.md.

More generally, under the base hypotheses, odd `n` admits no such set. If
`n` is even and `s=v_2(n)`, their exact number is

\[
\sum_{t=0}^{s-1}\left(\frac{n^2}{2^{t+2}}\right)^p.          \tag{6}
\]

For a fixed first point, there are `n/2^(t+1)` possible nonzero differences
of valuation `t`. Divide the number of ordered pairs by two and choose an
unordered pair independently on every level. Different valuations give
disjoint families.

## Scope and verification

The universal proof is above; exact finite audits in `verify.py` test the
new extraction and the classification from character orthogonality. They do
not replace a proof for unbounded parameters. Coprimality and an odd prime
are required; nothing is claimed for noncoprime factors or cardinality `3p`.
See [SOURCES.md](SOURCES.md) for credited inputs and the broader prior claims
in Liang's retrieved and inspected August 2026 preprints.
