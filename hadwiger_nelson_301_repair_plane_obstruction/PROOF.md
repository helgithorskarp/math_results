# Exact nonrealizability proof

Let G be the labelled graph in the sibling package's `graph.json`, pinned by
SHA256 `7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb`.
We prove that no function p:V(G)->R^2 satisfies
`||p(u)-p(v)||^2=1` for all 1452 edges. Injectivity is not assumed.

## 1. An odd wheel excludes even noninjective maps

Suppose a vertex h is adjacent to every vertex of an odd closed walk
`v_0,...,v_(2r),v_0`, whose consecutive vertices are adjacent. In a putative
unit-edge map, all p(v_i) lie on the unit circle about p(h). Consecutive
points on that circle are distance one apart, so their angle increments
are +pi/3 or -pi/3 modulo2pi. Closing the walk requires a sum of an odd
number of signs to be divisible by6. That is impossible by parity.

This proof allows distinct rim vertices to have the same image. Spoke and
rim edges themselves prevent the adjacent coincidences relevant to the
argument. In particular it includes K4, the wheel with a triangular rim.

Given nonadjacent vertices a,b, identify b with a in the abstract graph,
retaining all edges and removing repeated edges. If the quotient contains
an odd wheel, any unit-edge map of G must satisfy p(a)!=p(b): equality would
induce a prohibited unit-edge map of the quotient. For an adjacent pair the
inequality is immediate without a quotient.

The certificate lists 558 diagonal inequalities. The checker verifies
276 directly as edges and the other282 by explicit odd wheels in these
one-pair quotients. It checks every wheel spoke and rim edge by its inverse
image in the original graph. No enumeration-completeness claim is needed;
the listed witnesses suffice. Every named quotient vertex is a valid
representative, every rim is simple and odd, and the hub is outside the rim.

## 2. Mandatory four-cycle equations

Let a,b,c,d be a graph four-cycle and suppose p(a)!=p(c) and p(b)!=p(d).
Both p(b) and p(d) are on the unit circles centred at p(a),p(c). Two distinct
centres have at most two common circle points. Since the two common points
here are distinct, reflection in the midpoint of the centres interchanges
them. Consequently

    p(a)-p(b)+p(c)-p(d)=0.

This argument handles every position of the centres; tangency would allow
only one common point and is excluded by the established inequality. It
requires no convexity or generic-position assumption.

The certificate supplies 279 four-cycles and both certified diagonal
inequalities for each. Therefore all279 vector equations above hold in any
unit-edge map of G, even if other vertex pairs coincide.

Translate p(0) to zero. For either the x or y coordinates let z be the301-
entry scalar coordinate vector. Form the280 by301 integer matrix A from
the279 alternating four-cycle rows and the row fixing coordinate0. Then

    A z=0.

The certificate gives a301 by55 sparse rational matrix P with AP=0. Its
rows at the55 `free_labels` form the55 by55 identity, so P has rank55.
Independent elimination modulo the prime1000000007 gives rank(A)=246 in
that field. A nonzero246 by246 minor modulo that prime is a nonzero integer
minor, so rank_Q(A)>=246. The55 independent rational null vectors give the
reverse inequality. Thus rank_Q(A)=246 and P is a basis of the full kernel.
The same rank holds over R because A is rational. Every possible coordinate
vector is therefore z=P t for some t in R^55.

The checker verifies primality by trial division, the modular elimination,
all exact entries of AP, and every identity row of P. It does not trust a
producer rank, modular rank as an upper bound, or a guessed parametrization.

## 3. Contradictory exact norm identity

For an edge uv let d_uv be row_u(P)-row_v(P). The certificate assigns the
following integer weights to18 actual edges; all other weights are zero.

| Edge | Weight | Edge | Weight |
|---|---:|---|---:|
| 0-143 | 4452 | 1-132 | -8730 |
| 0-144 | 76 | 1-136 | 4905 |
| 0-147 | -3500 | 1-148 | 8910 |
| 0-148 | -11394 | 1-168 | 4230 |
| 0-151 | -3264 | 1-176 | -825 |
| 0-152 | 3340 | 1-179 | -2376 |
| 0-153 | 7236 | 2-115 | 3960 |
| 0-156 | -8928 | 2-133 | -1980 |
| 0-159 | 636 | 2-169 | 3960 |

Exact rational multiplication verifies both

    sum_uv lambda_uv d_uv^T d_uv = 0_(55 by55),
    sum_uv lambda_uv = 708.

Writing x=P s, y=P t, the first identity implies

    sum_uv lambda_uv ||p(u)-p(v)||^2
      = s^T (sum_uv lambda_uv d_uv^T d_uv) s
        + t^T (sum_uv lambda_uv d_uv^T d_uv) t
      = 0.

If all graph edges have length one, the left side instead equals708.
This contradiction proves the theorem. Negative multipliers are permitted:
this is an exact polynomial identity, not a positivity or optimization bound.

## Scope and prior evidence

The upstream source proves that G is exactly five-chromatic, vertex-critical,
K2,3-free and K4-free. The present theorem leaves all of those abstract claims
unchanged. It excludes every unit-edge image of this fixed graph in the
Euclidean plane, regardless of the physical image order, coordinate field,
symmetry, or inherited source coordinates. No restriction is imposed on
distances between nonadjacent vertices.

Four-cycle methods have already been used elsewhere in the campaign,
including the generalized Mycielski square-chain obstruction and the H510
realization classification. This application uses a different certificate:
odd-wheel quotient witnesses make selected parallelogram equations valid
without injectivity, and an exact weighted norm identity then contradicts
unit lengths. No priority claim is made for the underlying geometric lemmas.

The only computational premise of the geometric theorem is the direct
standard-library verification of the named graph and compact certificate.
No floating-point calculation, SAT status, LRAT proof, CAS rank assertion,
unchecked search boundary, or physical realization of the abstract source
is assumed. The upstream chromatic proof is useful motivation, not a premise
of the nonrealizability theorem.
