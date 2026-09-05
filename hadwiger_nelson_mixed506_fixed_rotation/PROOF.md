# Every translation of the fixed mixed506 rotation is four-colourable

Let `E=Q(alpha,beta)`, `alpha=i sqrt(3)`, `beta=i sqrt(11)`, and
`R=Q(sqrt(33))`, with the specified Euclidean complex embedding. Let
`A159,V214` be the exact archived source sets in
[the source package](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md).
Define

\[
\nu=(5+i\sqrt{11})/6,\qquad B=A159\cup\nu A159,
\qquad u=(1+i\sqrt{15})/4.
\]

**Theorem (exact computer-assisted fixed-family closure).** For every
translation `h in C`, the entire strict unit-distance graph on

\[
B\ \cup\ (u V214+h)
\]

is four-colourable. The same holds for `u bar(V214)+h`, since the fixed
second source is conjugation-invariant. The sources have 292 and 214
vertices, so disjoint placements have 506 vertices. Overlapping placements
are included. There is no denominator, algebraicity or magnitude restriction
on `h`.

This closes one specified relative rotation of the alternative B292/V214
family. It does not close other rotations, general two-gadget constructions,
the sealed Parts pool, or the general negative-trace stratum. It produces
no five-chromatic graph and does not improve the 509-vertex benchmark.

The proof has two parts. A local argument forces a precise congruence on
any two cross contacts of a hypothetical non-four-colourable placement.
Applying it at both 2-adic embeddings leaves 849,532 necessary three-contact
seeds. Exact modular evaluation rejects all of them as possible points on
a common unit circle. Every step of the finite enumeration is reproduced
with independent source/local arithmetic and a different circle identity.

## 1. Source and field facts

Both source sets are subsets of `E`. The public verifier independently
reconstructs `B` using generic real-radical multiplication and checks
292 distinct vertices, 1,251 strict unit edges and connectedness. The
normalised second source `S=V214-V214[0]` has 214 distinct vertices,
977 strict unit edges, is connected and satisfies `bar(S)=S`. The first
archived second-source vertex is the real number `1-sqrt(33)/6`, so the
normalisation preserves reflection invariance. Since translations are
arbitrary, replacing `V214` by `S` does not change the family. In the finite
census put `P=B`, whose first vertex is zero.

The accepted [base-field result](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
provides a conjugation-compatible embedding into
`U=Q_2(omega)`, `omega^2+omega+1=0`. For `O=Z_2[omega]`, `v(2)=1`,

\[
N(A+B\omega)=A^2-AB+B^2,
\qquad v_2(Nz)=2v(z).
\tag{1}
\]

Every Euclidean unit displacement in `E` therefore lies in `O` and has
nonzero residue in `F_4`. Each connected source occupies one additive
`O`-coset, and residues of differences from a source anchor properly
colour all its strict unit edges.

Use both embeddings, indexed by `j=0,1`:

\[
\begin{array}{c|ccc}
&\sqrt{33}&\alpha&\beta\\ \hline
\iota_0&r&1+2\omega&(r/3)(1+2\omega)\\
\iota_1&-r&1+2\omega&-(r/3)(1+2\omega),
\end{array}
\]

where `r` is the root of `r^2=33` with `r=1 mod 8`. The second is the first
composed with the field automorphism
`(a,b,c,d) -> (a,-b,c,-d)` in the basis `1,sqrt(33),alpha,beta`.
It also commutes with complex conjugation and satisfies (1). Both
normalised sources lie in the integral coset at both places; this is
checked for every point.

The fixed rotation has modulus one and minimal polynomial
`Z^2-(1/2)Z+1` over `E`. Indeed adjoining it is equivalent to adjoining
`sqrt(5)`, which is not in `R=Q(sqrt(33))`. Write `K=E(u)`. It is a field
closed under complex conjugation because `bar(u)=1/u`.

## 2. Arbitrary translations reduce to K

For each potential contact `e=(p,q) in P x S`, form the offset centre

\[
z_e=p-uq\in K.
\]

The contact is a cross unit edge at translation `h` exactly when
`|h-z_e|=1`. Distinct label pairs give distinct centres: equality of two
centres would imply `p-p'=u(q-q')`, forcing both differences zero because
`u notin E`.

An overlap puts `h=p-uq in K` immediately. Otherwise the copies are
disjoint. If they have at most two cross edges, take proper source
four-colourings and permute one. Each edge forbids exactly six of the
24 permutations, so at least twelve remain compatible. Thus these
placements are four-colourable.

If there are at least three cross contacts, three distinct centres lie
on the unit circle about `h`. They are noncollinear. Put
`d_i=z_i-z_0` for two of them and `k=h-z_0`. Subtracting the two unit
circle equations gives

\[
k\overline{d_i}+\overline k d_i=N(d_i),\qquad i=1,2.
\]

The determinant `bar(d_1)d_2-bar(d_2)d_1` is nonzero by noncollinearity.
Solving this two-by-two system expresses `k`, hence `h`, in `K`.
Consequently every placement that could fail four-colourability has
`h in K`. This argument supplies the unrestricted-translation bridge;
the search does not merely assume algebraic translations.

## 3. First negative trace and colour saturation

Write `h=m-u n` uniquely with `m,n in E`. For any actual cross edge set
`x=p-m`, `y=q-n`. Multiplying `|x-u y|^2=1` by `u` and reducing by its
minimal polynomial yields

\[
N(x)+N(y)-\tfrac12\overline x y=1.
\tag{2}
\]

This is a necessary equation in `E`. We never assume it is sufficient
for an arbitrary pair. Its derivation and the first-negative-trace
colouring boundary appear in the
[preceding result](../hadwiger_nelson_first_negative_trace/PROOF.md);
the needed local arguments are included here.

Fix either local embedding and suppress it in the notation. If both
centred sources are integral, multiply (2) by two and reduce modulo two:
`bar(res(x))res(y)=0`. Both residues cannot be zero, since then the left
side of (2) is even. Thus every cross edge joins a zero residue to a
nonzero residue. The common centred residue colouring is proper on the
entire strict union. An overlap forces `x=u y` and hence `x=y=0`; by
connectedness both centred sources are then integral, and their shared
point receives colour zero. All overlapping placements are covered.

For a non-four-colourable placement both local embeddings must instead
have a nonintegral centred source. On a cross edge write `a=v(x)`,
`b=v(y)`. The three terms in (2) have valuations

\[
2a,\qquad 2b,\qquad a+b-1.
\]

If the minimum of `a,b` is negative, uniqueness of a smallest term rules
out `a=b` and `|a-b|>1`. The only possibility is `-k,1-k`, `k>=1`.
The more negative source is fixed for the whole placement at this place:
all its points differ integrally and retain valuation `-k`. Every cross
endpoint on the other side has valuation `1-k`.

Below we prove a stronger contact restriction. It implies that the less
negative side's contact endpoints all have the same anchored residue
colour. If the more negative boundary omits a residue colour, permute
that single opposite boundary colour into the omitted colour. This gives
a proper colouring of the full union. Therefore a non-four-colourable
placement must use all four more-negative boundary residues at **both**
places. The identity of the more negative source may differ between the
two places; all four orderings are retained in the census.

## 4. Two-contact rigidity: matching and a congruence modulo eight

Order the centred sources so an anchor and every contact have valuations
`v(x)=-k`, `v(y)=1-k`, `k>=1`. Equation (2) is unchanged by this exchange:
conjugating it interchanges `x,y`, since its trace coefficient is real.
For any contact put

\[
X=2^k x,\qquad Y=2^{k-1}y,\qquad \varepsilon=2^{2k}.
\]

Both `X,Y` are units in `O`, and (2) becomes

\[
N(X)+4N(Y)-\overline X Y=\varepsilon.
\tag{3}
\]

Rearrange it as

\[
Y=X+\frac{4N(Y)-\varepsilon}{\overline X}.
\tag{4}
\]

Compare two contacts `(X,Y)` and `(X',Y')`. Norm differences of integral
points have valuation at least that of their difference. Inversion of
units preserves difference valuations. Since `v(epsilon)>=2`, subtracting
(4) gives

\[
v\big((Y'-Y)-(X'-X)\big)
\ \ge\ 2+\min\{v(X'-X),v(Y'-Y)\}.
\tag{5}
\]

If exactly one difference were zero, or if the two nonzero valuations
differed, the left side would have the smaller valuation, contradicting
(5). Thus one difference is zero if and only if both are zero; otherwise
both have the same finite valuation and (5) gains at least two powers of
two over that common value.

Returning to the unscaled sources, for distinct contacts `(p,q),(p',q')`
with `p,p'` on the more negative side, this proves

\[
v(q'-q)=v(p'-p)+1,
\qquad
v\big((q'-q)-2(p'-p)\big)\ge v(p'-p)+3.
\tag{6}
\]

In particular the cross graph is a **matching**: sharing an endpoint
would force sharing the other. All less negative endpoints have a single
residue colour because `v(p'-p)>=0`. Also

\[
q-2p\pmod{8O}
\quad\hbox{is constant across every cross contact.}\tag{7}
\]

If the source roles are reversed, the constant is `p-2q mod 8O` instead.
Translations by source anchors do not affect constancy or boundary
saturation. This makes (7) a restriction directly on the fixed normalised
source coordinates, independent of the unknown `m,n,k,h`.

The matching statement and valuation scaling are uniform for this trace,
not observations from the finite gadgets. The proof also works for a
relative trace `T=D/2` with any local unit `D`: in (3) the cross term is
`-D bar(X)Y`, and (6) has `2D^{-1}(p'-p)` in its second expression.
Only the fixed real trace `1/2` is used in the finite closure below.

## 5. Complete finite contact reduction

Encode a prospective cross pair `(i,j)` by `e=214i+j`, where
`0<=i<292`, `0<=j<214`. There are exactly 62,488 such pairs. At each
local place use colour encoding `a+b omega -> a+2b` modulo two.
For an ordering `d=(d_0,d_1) in {0,1}^2`, let `d_l=0` mean `P` is the
more negative source at place `l`, and `d_l=1` mean `S` is more negative.
Attach to each contact the four-component key formed by the two
coefficients modulo eight of

- `q_j-2p_i` at place `l`, if `d_l=0`;
- `p_i-2q_j` at place `l`, if `d_l=1`.

For every ordering all 4,096 possible keys occur. By (7), the actual
contacts of a non-four-colourable placement all belong to one cell.
Keep a cell only when its full list of prospective contacts contains all
four more-negative boundary colours at each place. Passing this test is
necessary, not sufficient.

From every retained cell enumerate one contact of first-place colour
zero, one of colour one, and one of colour two, in that order. Each list
is in increasing contact-label order. A non-four-colourable placement,
being saturated, necessarily contains such a triple. It is unnecessary
to enumerate a fourth contact if every such triple is already impossible.
No geometric translation or symmetry quotient is omitted by this reduction.

The complete census is:

| More negative sources at the two places | Retained cells | Contacts in those cells | Necessary triples | Pass mod 1321 | Pass both primes |
|---|---:|---:|---:|---:|---:|
| B, B | 3,018 | 50,037 | 237,488 | 315 | 0 |
| B, S | 3,416 | 53,415 | 217,531 | 108 | 0 |
| S, B | 3,521 | 54,863 | 183,105 | 59 | 0 |
| S, S | 3,594 | 56,418 | 211,408 | 211 | 0 |
| Total | 13,549 | 214,733 | 849,532 | 693 | 0 |

Totals count each ordering separately. They are counts of necessary
contact seeds, not counts of Euclidean placements or distinct graphs.

## 6. Exact circle exclusion by two finite fields

For three offset centres `z_0,z_1,z_2`, use real coordinate vectors
`v=z_1-z_0`, `w=z_2-z_0`. Set

\[
A=|v|^2,\quad B=|w|^2,\quad
\Delta=v_xw_y-v_yw_x,
\quad M_x=Aw_y-Bv_y,\quad M_y=Bv_x-Aw_x.
\]

If the centres lie on a unit circle, its relative centre solves the two
dot-product equations and equals `(M_x,M_y)/(2 Delta)`. Hence necessarily

\[
M_x^2+M_y^2-4\Delta^2=0.\tag{8}
\]

For actual three-contact centres `Delta!=0`, as proved in Section 2.
The modular test does **not** divide by `Delta` or discard cases where
it vanishes modulo a prime; (8) is evaluated as a polynomial.

All offset coordinates lie in
`Z[1/2,1/3,sqrt(3),sqrt(5),sqrt(11)]`. Evaluate this ring in each finite
field using the following roots:

| Prime | sqrt(3) | sqrt(5) | sqrt(11) |
|---:|---:|---:|---:|
| 1321 | 321 | 416 | 501 |
| 5281 | 1302 | 325 | 1874 |

Primality and the three square identities are checked directly. Both
primes are coprime to every source-coordinate denominator. Thus an exact
zero of (8) must evaluate to zero at both primes. This is a ring map on
the indicated coordinate ring, not a homomorphism from an entire
characteristic-zero field into a finite field. The unknown translation
is never evaluated, so its denominator causes no exceptional case.

Of the 849,532 seeds, exactly 693 pass the first evaluation. None passes
the second. Therefore there is no triple required by a hypothetical
non-four-colourable placement. Combining Sections 2 through 5 proves the
full theorem for every complex translation. No SAT assumption or numerical
approximation enters the closure.

## 7. Independent validation and exact trust boundary

`census.py` reconstructs the normalised source sets, obtains both local
images from the pinned field arithmetic, groups contacts by congruence
keys, and evaluates (8) in real modular Cartesian coordinates.
`expected.json` records the full cell-size histograms and deterministic
hashes of every retained cell, every enumerated triple and every survivor
of the first prime, separately for all four orderings.

`audit.py` imports neither the producer nor its field/local arithmetic.
It rebuilds `B` using generic real-radical multiplication, normalises `S`
with a common integer denominator 72, and checks all source edges and
connectedness. Its local images use an independent finite lift:
`r=1+8t`, `4t^2+t-2=0`; exhaustive `t mod 64` determines the required
branch with more precision than needed. It sorts contact records and
reconstructs every retained cell and ordered triple.

For the geometric exclusion it evaluates paired modular images of
`z` and `bar(z)`, using a checked square root of minus one. Pair distances
are products of conjugate differences. If `a,b,c` are the three squared
side lengths, its circle test is the independent Heron identity

\[
abc-4ab+(a+b-c)^2=0.\tag{9}
\]

This polynomial equals (8), but uses a different formula and coordinate
representation. The complete local-image, cell, triple and first-prime
survivor streams agree with the producer, not merely the total counts.
The independent run also rejects every seed by the second prime.

`controls.py` verifies the generic cleared-denominator contact difference
identity in an exact sparse polynomial ring. It checks the genuine
[20-vertex saturation witness](../hadwiger_nelson_first_negative_trace/PROOF.md):
all six contact-pair differences obey (6), the two-place cell retains its
four boundary colours, and all four of its three-contact subsets pass
both circle formulas at both primes. It also checks a rational unit-circle triple and
rejects radius-two and collinear triples. The positive witness is
three-chromatic; its role is to show that the necessary filters retain a
real saturation configuration, not to claim a five-chromatic construction.

These are independent author implementations, not external review or
proof-assistant formalization. The trust boundary is the accepted
base-field embedding, exact archived coordinates, the unformalized
valuation/translation reductions, finite enumeration completeness and
ordinary Python integer arithmetic. There is no hidden search, solver
proof trace, floating-point equality or omitted large certificate.

The [fixed inner construction](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
is reused; no alternative angle, trace stratum or historical Parts census
is enumerated. Local valuation and modular polynomial arguments are
classical; no novelty priority is claimed. Primary record context:
Parts, [Graph minimization](https://arxiv.org/abs/2010.12665), and
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 2026-09-05, retain the 509-vertex benchmark. This result is a
complete negative certificate for the one stated construction family.
