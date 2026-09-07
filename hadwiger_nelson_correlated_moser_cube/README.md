# Every correlated three-spindle sum is four-chromatic

Let `M` be the seven-point Moser spindle defined below. For **every** complex
number `u` with `|u|=1`, the strict planar unit-distance graph on

\[
S_u=M+uM+u^2M
\]

has **chromatic number exactly four**. Coincident sums are identified and
every actual unit edge is included. Consequently every subgraph of every
member is four-colourable. Each member has at most **343 vertices**, so this
is a complete negative classification of a construction family lying wholly
below the 508-vertex target. It is not a classification of one fixed host,
a sampled-angle experiment, or a record improvement.

The proof combines an exact polynomial event census with **57 positive
colour words**. Its public certificate is **37,391 bytes**. The independent
checker uses no producer geometry, SAT answer, floating-point decision or
assumption that a computer algebra system returned irreducible factors.
No external review or proof-assistant verification is claimed.

## The construction

Put

\[
\rho=(1+i\sqrt3)/2,\qquad r=(5+i\sqrt{11})/6,
\qquad M=(0,1,\rho,1+\rho,r,r\rho,r(1+\rho)).
\]

The order in this tuple fixes all labels. The two diamonds share vertex 0;
their far endpoints are a unit apart. Their eleven unit edges exclude a
three-colouring by the usual diamond argument. The checker independently
recovers those eleven edges and exhausts all `3^7` colour assignments.
Every `S_u` contains `M`, by choosing zero in its second and third factors,
so its chromatic number is at least four.

For exact arithmetic write a point as

\[
x=(a+b\sqrt{33})/36,\qquad y=\sqrt3(c+d\sqrt{33})/36.
\]

The seven integer rows `(a,b,c,d)` are

```text
( 0, 0, 0,0)  (36, 0, 0,0)  (18, 0,18,0)  (54, 0,18,0)
(30, 0, 0,2)  (15,-3,15,1)  (45,-3,15,3)
```

Formal addresses `(i,j,k)` range independently over `{0,...,6}` and name
`m_i+u*m_j+u^2*m_k`. Their label is `49*i+7*j+k`. These 343 labels may
coincide at exceptional parameters; the certificate handles those equalities.

Minkowski sums, rotation and the Moser spindle are standard construction
tools; see [Heule, *Trimming Graphs Using Clausal Proof Optimization*](https://arxiv.org/abs/1907.00929).
No novelty is claimed for those operations. This package classifies the
specific correlated family `M+uM+u^2M`, using an independently implemented
quartic event computation. It does not reuse the earlier
[heptagon–spindle rotation-family implementation](../hadwiger_nelson_heptagon_moser_sum/ROTATION_FAMILY.md).

## Reduction of the whole unit circle to polynomial cases

Use the bijection

\[
u=\frac{1+i\sqrt3t}{1-i\sqrt3t}\quad(t\in\mathbb R),
\]

which omits only `u=-1`. Let `D=1+3t^2`; it is strictly positive for real
`t`. For a pair of distinct formal addresses let `a,b,c` be 36 times the
three corresponding spindle differences. They lie in
`Q(sqrt(33))+i sqrt(3) Q(sqrt(33))`. For `lambda=0,1`, define

\[
F_\lambda(t)=D^2\bigl(|a+ub+u^2c|^2-1296\lambda\bigr).
\]

This is a polynomial of degree at most four over `K=Q(sqrt(33))`.
`F_1(t)=0` is exactly the unit-edge condition; `F_0(t)=0` is exactly
coincidence of the two sums. There is no real denominator exception.

For a directly reproducible coefficient formula write

```text
k  = |a|^2+|b|^2+|c|^2-1296*lambda,
h  = b*conjugate(a)+c*conjugate(b) = hx+i sqrt(3) hy,
j  = c*conjugate(a)               = jx+i sqrt(3) jy.
```

The ascending coefficients of `F_lambda` are

```text
k+2hx+2jx,  -12hy-24jy,  6k-36jx,  -36hy+72jy,  9k-18hx+18jx.
```

The producer uses this Laurent-norm expansion. The independent checker instead
constructs every address's real and imaginary polynomial numerators with
denominator `36D^2`, expands the squared distance to degree eight, and checks
the exact cancellation of `D^2` coefficient by coefficient. Across all
**58,653** unordered address pairs, the full event-polynomial/pair incidence
lists agree entry by entry.

Exactly **1,617** pair conditions `F_1` vanish identically. They are precisely
the Cartesian-cube edges of the spindle. No distinct-address `F_0` vanishes
identically. At all remaining parameters, assign the colour
`c(i) XOR c(j) XOR c(k)` in the group `(Z/2Z)^2`, where `c` is the supplied
proper spindle four-colouring. This is proper on every Cartesian edge.

There are 9,544 distinct nonzero, nonconstant normalized unit-event
polynomials and 9,444 distinct nonconstant collision-norm polynomials.
Each `F_0` is nonnegative on the real axis. Therefore every real root of it
is repeated and is a root of `gcd(F_0,F_0')`. Conversely any real root of
that gcd is a collision. This reduces the collision census without omitting
any real coincidence, including repeated or degenerate parameters.

## Factor coverage, reality and equality constraints

The generator proposes factorizations of all unit-event polynomials and
all collision gcds. The verifier checks **18,988 exact product identities**
over `K`, up to a nonzero scalar, against its own polynomials and gcds.
The resulting list has **8,094 distinct nonconstant polynomial pieces**.
Factorization completeness and irreducibility are not trusted assertions.

To show that those pieces share no roots, the checker reduces them by

```text
p = 2^61-1 = 2305843009213693951,
sqrt(33) -> 1971369914087038467 modulo p.
```

Lucas–Lehmer proves the displayed modulus prime, and the square-root congruence
is checked. Every degree is preserved. The product `P` of all reduced pieces
has degree **28,253** and satisfies `gcd(P,P')=1` over the prime field.
Hence the original pieces are squarefree and pairwise coprime over `K`:
a common factor would force a zero resultant, and its reduction could not
give coprime polynomials with preserved degrees. This finite-field check
uses exact FLINT polynomial arithmetic. No large product polynomial is stored
in the repository.

A Sturm sequence over `K`, with exact integer/rational comparisons of
`a+b sqrt(33)` in the positive real embedding, counts the real roots of
each piece. The counts are:

| Real roots in a piece | Pieces |
|---:|---:|
| 0 | 1,084 |
| 1 | 1,529 |
| 2 | 3,733 |
| 3 | 812 |
| 4 | 936 |

Thus **7,010** pieces cover exactly **15,175 distinct finite real
parameters**. These are polynomial cases, not an assertion that the resulting
graphs are pairwise nonisomorphic.

For a real root of a piece `f`, include the generic edges and every unit
event divisible by `f`; require equal colours on every pair in a collision
gcd divisible by `f`. The product identities and pairwise coprimality prove
that these are all the unit and collision events at that root. Every real
root of the same piece consequently has the same formal graph and equality
relation, even without an irreducibility assumption.

The word assigned to each real case is checked against all its unit-edge
inequalities and collision equalities. It descends to a proper colouring of
the actual point quotient. Across these cases the checker performs 97,414
exceptional edge comparisons and 7,988 equality comparisons, in addition
to 92,169 generic-edge comparisons for the 57 words. Eighty-two real cases
have collisions; finite cases range from 70 to 343 points and from 240 to
1,645 unit edges.

Finally `u=-1` is independently checked by exact integer-coordinate addition.
It gives **100 points and 392 unit edges**, with its own verified colouring
assignment. This handles the omitted parameter. The generic case, every
finite exceptional parameter and `u=-1` are now covered, proving the upper
bound four. The contained spindle proves equality. Deleting vertices or
edges preserves the upper bound.

## Reproduction

Reference environment: CPython 3.11.2, SymPy 1.14.0 and python-flint 0.8.0.
Use a virtual environment and install `requirements.txt`. From this directory:

```sh
python3 propose.py --out /scratch/hn-moser-cube-data --workers 4
python3 verify.py --work /scratch/hn-moser-cube-data --check-expected
python3 -O verify.py --work /scratch/hn-moser-cube-data --check-expected
python3 controls.py --work /scratch/hn-moser-cube-data
sha256sum -c SHA256SUMS
```

The independent verifier itself needs only Python's standard library and
python-flint. SymPy is used to propose factorizations and in the additional
rational-root controls. Proposal files are generated in the specified scratch
directory; they are deliberately omitted from Git.

The reference proposal run took about 14.1 seconds with four processes.
Independent verification took 18.7 seconds in both normal and optimized modes;
the observed cumulative child peak was about 120 MiB. The complete deterministic
result is in `expected.json`. Certificate SHA-256:

```text
75314b977c3708dce8fad86e737b90d892981e29c49df152c7a5459dd5eb36db
```

Additional controls check all 115,689 event-pair incidences under
`t -> -t` and address reversal `(i,j,k)->(k,j,i)`, 289 quadratic sign cases,
six root-multiplicity fixtures, and 200 seeded polynomial pieces against
SymPy's separate rational-polynomial real-root counter using field norms.
Twenty-two malformed or inconsistent inputs are rejected. These are checks
run by the author, not independent peer review.

Optional certificate regeneration requires `requirements-search.txt`:

```sh
python3 search.py --work /scratch/hn-moser-cube-data \
  --output /scratch/hn-moser-cube-data/regenerated.json
cmp certificate.json /scratch/hn-moser-cube-data/regenerated.json
```

The pinned PySAT 1.9.dev15 / CaDiCaL 1.9.5 producer uses one-hot four-colouring
constraints after identifying coincident addresses. Three vertices of a
contained unit triangle are fixed to colours 0,1,2, which loses no colouring
up to palette permutation. Previously found words are reused across cases.
It made 56 SAT calls, all positive, with at most 345 reported conflicts;
the declared budget was 2,000,000 per call. It regenerated the certificate
byte for byte. Neither these solver answers nor that budget is part of the
proof: the saved positive words are directly checked.

The remaining trust boundary is the written geometric/polynomial reduction,
quadratic-field and rational arithmetic in the small verifier, Sturm's theorem,
Lucas–Lehmer's theorem, exact FLINT modular polynomial arithmetic, Python and
the direct colour comparisons. No external graph dataset, imported chromatic
claim, numerical root isolation, irreducibility oracle or UNSAT trace is needed.

## Campaign scope

This family is retired in full for the target. It does not cover independently
chosen rotations in `M+uM+vM`, different summands, other exponent patterns or
larger constructions. No follow-up enlargement was started in this pass.

The team's [T721 fixed-host closure](../hadwiger_nelson_t721_weighted_cover/README.md)
and its [independent acceptance](../hadwiger_nelson_t721_weighted_cover_review1/README.md)
remain intact. The teammate's [inertial-field barriers](../hadwiger_nelson_inertial_field_barrier/README.md)
and their [review](../hadwiger_nelson_inertial_field_barrier_review1/README.md)
were read for coordination and are not premises here. This pass followed the
06:54Z direction to classify a candidate-bearing construction space outside
the retired fixed hosts, using exact computational certification.

The [509-vertex Parts construction](https://arxiv.org/abs/2010.12665) remains
the comparison target. This campaign has not established a five-chromatic
planar unit-distance graph on at most 508 vertices. No priority claim is made
for this family classification.
