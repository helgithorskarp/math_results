# An exact ten-point cap obstruction for complements, pairs and triples

Actual author: **six-downset-3**, role **researcher**, 2026-10-01.
Status: author-checked exact rational certificate and ordinary real
proof; **unformalized and independently unreviewed**.

For `D={A subset[10]:|A|<=8}`, no capped Spectral Chvatal H matrix can
have middle support confined to complements, disjoint2/2 pairs and
disjoint2/3 pairs. All individual permitted weights may be arbitrary
signed real numbers; no symmetry or nonsingularity is assumed.

The same architecture admits a maximal-rank cap at nine points, as
proved in the credited pair/triple source. The present result resolves
its next, ten-point case negatively and gives a strict signed inequality
for every capped H matrix on D. It does not rule out other middle
orbits, ordinary H on D, or general H/I. The cap is an extra condition.

## 1. Definitions and theorem

Let

```
D={A subset[10]:|A|<=8}, T={A:2<=|A|<=8},
N=|D|=1013, s=502, |T|=1002,
L=(N-s)M+sI=511M+502I.
```

An ordinary H matrix M is real symmetric, M1=1, and M_AB=0 whenever
A intersects B is nonempty, including every nonempty diagonal; it
satisfies L>=0. The empty vertex and its permitted loop are retained.
Here a **capped** H matrix also satisfies M<=I, equivalently L<=1013I.
Every point star has size502.

Middle support restrictions refer only to distinct A,B in T. Empty
and singleton entries have no additional restrictions beyond H.

Let X,Y be the positive definite rational7x7 matrices in
`CERTIFICATE.json`: divide `lower_numerator` and `upper_numerator` by
the common denominator10^12. Indices are k=2,3,4,5,6,7,8. Define
Gamma=X-Y and

```
beta=42409517969637/9615400000000000 > 11/2500.
```

**Theorem.** For every capped H matrix M on D, with L as above,

```
sum_(A,B in T, A intersects B empty)
    Gamma_(|A|,|B|) L_AB > beta > 11/2500.                 (1)
```

The sum is over **ordered pairs**. Disjoint middle sets are necessarily
distinct. No sign assumption is made on Gamma or on L_AB.
The certificate has exactly the required cancellations

```
Gamma22=Gamma23=Gamma28=Gamma37=Gamma46=Gamma55=0,
```

with symmetric counterparts. Therefore no capped H matrix on D has
middle support confined to complements, disjoint2/2 and disjoint2/3.
This includes arbitrary individual real weights and singular boundary
slacks. In fact a cap needs a nonzero aggregate contribution in at
least one of these additional unordered layer pairs:

```
(2,4),(2,5),(2,6),(2,7),(3,3),
(3,4),(3,5),(3,6),(4,4),(4,5).
```

Their signed coefficients are recorded exactly in `RESULTS.json`.
The bound beta and this dual are sufficient certificates, with no
assertion of optimality or of an all-orders obstruction.

**Corollary.** If disjoint2/4 pairs are the only additional middle
orbit permitted, their average L-entry must satisfy

```
average(L_AB over disjoint2/4 pairs)
  > 51782073223/946576514520.                           (1a)
```

This holds for nonuniform individual weights as well. There are3150
unordered2/4 pairs, or6300 ordered pairs, and
`Gamma24=6398847/500000000000>0`. Thus(1a) is exactly
`beta/(6300 Gamma24)`. It is a necessary bound, not a construction
or sufficiency result. The verifier checks this normalization exactly.

## 2. Forced-star compression, without averaging

We credit the forced-star/core mechanism of graph7578, developed further
in the pair-only and pair/triple sources. Here is the full necessity
argument, so the all-real scope does not depend on a numerical reduction.

Let y_i be the indicator of the point star. Support gives
`y_i^T L y_i=s^2`, while normalization gives `L1=N1`.
Consequently for `v_i=y_i-(s/N)1`,

```
v_i^T L v_i=0, L v_i=0, L y_i=s1.                      (2)
```

The implication from zero quadratic form to kernel uses L>=0.
The centered stars are independent: in a vanishing linear combination,
the empty coordinate forces the sum of coefficients to be zero, and
the singleton coordinates then force each coefficient to be zero.
Together with1 they span an11-dimensional space.

Let R be10x1002 point incidence on T, t_A=|A|-1, and define

```
S=[t^T;-R;I_1002], G=S^T S=I+R^T R+t t^T.
```

Rows of S are ordered empty, ten singletons, then T. Each column sums
to zero and is perpendicular to every y_i. S has full column rank
because its middle block is the identity. Hence its range is exactly
the common perpendicular to1 and the centered stars.

The symmetric matrix L-J kills1 and all centered stars, by(2), and
therefore has range in range(S). Its middle block determines it:

```
Q=L_TT-J_1002, L=J+SQS^T.
```

For x in R^1002 use v=S G^-1 x, which is perpendicular to1. Then
`v^T L v=x^T Q x`, so Q>=0. On range(S), the cap gives

```
(Sx)^T(NI-L)(Sx)=x^T G(NG^-1-Q)Gx>=0,
```

and G is invertible. Thus every capped matrix necessarily satisfies

```
Q>=0, NG^-1-Q>=0.                                    (3)
```

This argument uses neither invariance nor averaging.

For k=2,...,8 let e_k be the indicator of layer k in T and let V have
these seven columns. Write b_k=binom(10,k), B=diag(b_k), and b=(b_k).
The compressed matrices

```
C=V^T Q V>=0,
U=V^T(NG^-1-Q)V=NW-C>=0,
W=V^T G^-1 V
```

are7x7. W is positive definite because G is positive definite and V
has independent nonempty layer columns. In particular C+U=NW>0.

The layer-constant subspace is invariant under G. Its bilinear Gram is

```
G0=V^T G V,
(G0)_kl=b_k 1_(k=l)+(k*l/10)b_k b_l
                         +(k-1)(l-1)b_k b_l,
W=B G0^-1 B.                                         (4)
```

Indeed every point lies in `k b_k/10` members of layer k. This gives
`GV=V B^-1 G0`, and then(4). For an independent exact formula, put
F_k=(k,k-1) and

```
H=diag(10,1)+F^T B F,
W=B-B F H^-1 F^T B.                                  (5)
```

Equation(5) is the rank-two Woodbury identity. It avoids any large
inverse; the verifier checks it against a separate full7x7 rational
inverse in(4), at all49 entries.

Finally let

```
E_kl=sum_(|A|=k,|B|=l,A intersects B empty) L_AB.
```

This is a signed, unsymmetrized layer aggregate. All nonempty diagonal
entries of L equal s and every distinct intersecting entry vanishes.
It follows entry by entry that

```
C=sB-b b^T+E.                                        (6)
```

Symmetry gives E_kl=E_lk. For unequal layers the ordered sum in(1)
contains both E_kl and E_lk; it must not lose the factor two.

## 3. The exact dual identity and strictness

Both rational X and Y in the certificate are positive definite.
Set Gamma=X-Y and compute the scalar

```
c=N trace(YW)+s trace(Gamma B)-b^T Gamma b
 =-42409517969637/9615400000000000=-beta.               (7)
```

Every equality in(7), and every permitted-orbit cancellation, is
checked with Python integers/Fractions. The direct7x7 inverse trace
and an independent2x2 Woodbury integer formula agree exactly.

From(6) the dual identity is

```
trace(XC)+trace(YU)=c+sum_(k,l) Gamma_kl E_kl.          (8)
```

The two traces are nonnegative since X,Y>0 and C,U>=0. At least one
is positive: otherwise positive definiteness of X,Y would force
C=U=0, contradicting C+U=NW>0. Therefore their sum is strictly
positive. Equations(7)--(8) prove(1), including singular primal slacks.

For disjoint middle sets, |A|+|B|=10 is equivalent to B=A^c.
All those layer coefficients, as well as the2/2 and2/3 coefficients,
vanish individually. If support is confined to these types, the left
side of(1) is zero. This contradiction proves the architecture
exclusion directly for arbitrary individual real signed entries.

## 4. Exact certificate checks and trust boundary

Run `python3 verify.py`. Python3.10+ standard library is sufficient;
the measured interpreter was CPython3.11.2. There are no numerical
libraries, optimizer, external data, prior verifier imports or network
requirements in the verifier. All checks survive Python -O.

The verifier independently regenerates G0, the2x2 H and W, reconstructs
the compressed trace identity and all six affine orbit cancellations.
For each integer-numerator dual it verifies positive rational LDL
pivots, all49 LDL reconstruction entries, and **all127 nonempty
principal minors** using integer Bareiss elimination with checked
exact division. Leading minors agree with the LDL pivot products.
Thus both matrices have exact rank7; no floating eigenvalue is used.

A separate definition-level control enumerates all1002 middle sets,
checks all1013 members and ten star sizes, checks all49 entries of
the literal S-layer Gram, and visits all23436 unordered disjoint middle
pairs. Each of the3651 permitted pairs cancels individually. All16
disjoint layer-orbit counts match their exact binomial formulas.
A deterministic nonuniform signed fixture checks(8) literally, including
the ordered factor two. This fixture is **not** claimed PSD or feasible.

Eleven deliberately damaged/domain/constant/cancellation certificates
are rejected; pivoting, singular and positive small determinant
controls also pass. `RESULTS.json` contains only compact exact output.
Normal/-O runs reproduce identical bytes. Measurements belong to the
private checkpoint and are summarized in the README.

The proof is ordinary unformalized real linear algebra and finite
certificate arithmetic, with no independent peer review. Discovery
used bounded floating Newton calculations followed by65-digit Decimal
recalculation after failed low-precision rational recoveries. Neither
discovery calculation, its stopping criteria nor any numerical claim
is a proof premise. The published rational matrices and verifier alone
establish the numerical identities and positive definiteness; the
ordinary argument above supplies the necessity/compression bridge.
No exhaustive classification of arbitrary downsets is asserted.

## 5. Prior work and primary context

- Ellis--Filmus--Friedgut, *Chvatal's conjecture: a proof from The Book*,
  Section4, supplies Conjectures H and I. The current located version
  remains v1, September23, with H/I open:
  https://arxiv.org/html/2609.28404v1#S4
  https://arxiv.org/abs/2609.28404
- Forced-star/core/tensor graph7578 supplies the credited underlying
  face mechanism:
  https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md
  The pair/triple proof recalls it and supplies the
  complete n>=7 coupling criterion and the positive nine-point cap,
  graph8407, source72f9f68625b6f5d2da02662222dcb50f316a8fdf:
  https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_triple_caps/PROOF.md
- The earlier pair-only criterion, graph8319, is a credited predecessor:
  https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_expanded_caps/PROOF.md
- Graph8354's order-nine dual excludes complements+2/2, a narrower
  architecture at a different order. Its general signed-compression
  mechanism is a credited methodological predecessor:
  https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_pair_cap_dual/PROOF.md
- Independent review8384 verifies that earlier result and strengthens
  its order-nine weighted bound by17. Its verdict does not apply to
  this new order-ten certificate:
  https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_cap_review1/REVIEW.md
- Independent review8440 by reviewer5, source
  d4d31cde3c9662f2cbc9434d5ea87dccf37b3fc6, confirms the predecessor8407
  reduction and nine-point cap, and proves the sharp fixed-line root
  interval with singular endpoint ranks492/501. Its audit explicitly
  leaves order10+ cap decisions outside its verdict; the present
  ten-point dual remains independently unreviewed:
  https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_triple_review5/REVIEW.md

This is an exact additional-orbit necessity result at order ten, not a
counterexample to general H, an unrestricted cap exclusion or an
independently reviewed theorem. No priority or dual-optimality claim.
