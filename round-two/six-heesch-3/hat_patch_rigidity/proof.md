# A 25-hat contact network permits only the existing hat continuum locally

Actual author: **six-heesch-3**, role **researcher**, 2026-10-01.

This is a written local rigidity proof with an exact finite rank and
contact certificate. It gives a restriction on one proposed route to a
finite Heesch number of at least seven. It constructs no finite-seven tile
and makes no exclusion of other contact networks or distant deformations.

## Statement and hypotheses

The fixture in [input.json](input.json) consists of 25 copies of the hat,
with one straight side subdivided, giving 14 labelled boundary ports. Its
136 shared complete ports define a fixed labelled contact network.
They come from one application of Craig S. Kaplan's `hatviz` substitution
to the initial H metatile. Coordinates and all reference poses are exact
integers after removing the original common half-scale and fixing copy
zero to the identity. The reference polygon area is `8*sqrt(3)`.

**Local rigidity theorem.** In some neighbourhood of this reference
configuration, allow all 14 prototype endpoints to move and each of the
24 nonroot copies to translate and rotate, keeping its handedness.
Fix the root pose to the identity. Require the two labelled endpoint
coincidences of every one of the 136 complete shared ports to persist.
Every such endpoint configuration belongs to the five-parameter family
of orientation-preserving similarities of

    Tile(1, sqrt(3)*(1+lambda)),  lambda near zero,

with the corresponding copy poses. No other local endpoint motion exists.

Now additionally represent each prototype port as a normal graph over its
new chord, and require that every labelled complete shared port in the
network still coincides as a whole boundary arc. All 14 normal displacement
functions must be identically zero. In particular this applies to
sufficiently small C1 boundary perturbations retaining those contacts,
without symmetry or polynomial assumptions on the profiles.

The polygons in this remaining family tile the plane by the published hat
continuum theorem. Consequently a sufficiently small perturbation retaining
this complete labelled contact network cannot have finite Heesch number.
This conclusion is conditional on retaining the network. A packing with
the same endpoints but unfilled lenses between its curves need not retain
the complete shared-port contacts, and is outside the profile conclusion.

This theorem does not assert that every seven-corona hat patch contains
the fixture. It does not impose this network on a different shape or
exclude splitting ports, changing the contacts, or leaving the stated
neighbourhood. Its neighbourhood is proved to exist but is not given a
numerical radius.

## 1. Reference coordinates and independent geometric decoding

Use axial coordinates with physical map

    L(x,y)=(x+y/2, sqrt(3)*y/2).

The prototype's CCW endpoint list is

    (0,0), (-1,-1), (0,-2), (1,-2), (2,-2), (2,-1),
    (4,-2), (5,-1), (4,0), (3,0), (2,2), (0,3),
    (0,2), (-1,2).

Port i joins endpoint i to endpoint i+1 modulo 14. Ports 2 and 3 are
the two unit halves of the original length-two straight side. The squared
length of an axial vector `(x,y)` is `x*x+x*y+y*y`. Eight ports have length
one and six have length `sqrt(3)`.

A pose stores `[a,b,c,d,e,f]`, acting as

    (x,y) -> (a*x+b*y+c, d*x+e*y+f).

The checker proves each linear part R preserves the axial Euclidean Gram
matrix, and has determinant h in `{+1,-1}`. The root pose is the identity.
The direct geometric reader imports no substitution code. It checks the
prototype is simple, triangulates it into 11 positive-area triangles,
and uses exact separating axes to exclude interior overlap between every
pair of reference copies. Artificial endpoint 3 is retained for all port
calculations but removed from the triangulation. The triangulation areas
sum to the polygon area.

For every port of every copy, the reader reconstructs its two world
endpoints. It groups identical endpoint pairs, proving there are precisely
136 complete shared ports, with opposite interior sides. Their adjacency
graph connects all 25 copies. It also extracts 31 distinct relations
between original port indices and their parameter order.

The fixture is data extracted from a published tiling construction; this
packing check is independent of that construction's implementation. The
25-copy configuration is not claimed to be a complete corona witness.

## 2. Function-valued rigidity, including parameter reversal

First fix the reference endpoints and poses. Let e_i be the chord vector
of port i and n_i its outward unit normal. An arbitrary normal graph has
parametrization

    gamma_i(t) = v_i + t*e_i + q_i(t)*n_i,  0<=t<=1,
    q_i(0)=q_i(1)=0.

For a complete shared port on copies a and b, the transported outward
normals are opposite. Orthogonal projection onto the common chord makes
the two parameters either t and t, or t and 1-t. Thus full arc coincidence
implies

    q_i(t) = -q_j(t)        if endpoint order agrees,
    q_i(t) = -q_j(1-t)      if endpoint order reverses.       (1)

These equations incorporate reflected copies. A normal graph has a unique
point over each chord parameter; coincidence as sets therefore implies
the pointwise equations. No approximate fit of curves is used.

Use a lifted graph with nodes `(i,r)`, for i=0,...,13 and r=0,1, carrying
the functions q_i(t) and q_i(1-t). Encode node `(i,r)` by `2*i+r`.
For a contact with reversal bit epsilon, add both edges

    (i,r) -- (j,r XOR epsilon),  r=0,1.

Every edge imposes negation. An odd closed walk gives its starting function
equal to its own negative, so that function vanishes identically over the
reals. Connectivity propagates zero through its component.

The reader verifies exactly these four connected components, with the
displayed odd triangles:

| Component nodes | Odd closed walk |
|---|---|
| 0,11,12,19,20,27 | 0,11,12,0 |
| 1,10,13,18,21,26 | 1,10,13,1 |
| 2,5,6,9,14,17,22,25 | 2,5,22,2 |
| 3,4,7,8,15,16,23,24 | 3,4,23,3 |

They cover all 28 nodes, proving all 14 profile functions vanish. Using
only a scalar sign graph would miss the distinction between a forced-zero
profile and one allowed to be antisymmetric. The lifted odd walks establish
pointwise zero here, rather than only a zero integral or zero charge.

## 3. The endpoint Jacobian

Let R_a and t_a be the reference linear part and translation of copy a.
Prototype endpoint coordinates v_i may move freely. Each nonroot copy
has two translation variables and one local rotation variable, retaining
its determinant. There are

    2*14 + 3*24 = 100 real variables.

For each shared port, equate its two corresponding endpoint pairs. There
are 544 scalar equations, with repetitions retained. They are smooth
functions of these variables, including at the artificial straight join.
No preservation of the straight join is assumed in advance.

Set

    A=[[-1,-2],[2,1]],  so L*A=sqrt(3)*J*L,

where J is Cartesian rotation by 90 degrees. Parametrize the rotation of
copy a by `exp(omega_a*A)*R_a`. A shared endpoint between `(a,i)` and
`(b,j)` has linearization

    R_a*dv_i - R_b*dv_j + dt_a - dt_b
       + omega_a*A*R_a*v_i - omega_b*A*R_b*v_j = 0.        (2)

Root translation and rotation variables are omitted. All coefficients in
the `544 x 100` Jacobian M are integers. The row order and complete matrix
are reconstructed from the fixture; the matrix itself is not published.
Its compact JSON row-stream SHA256 is

    349b3ec9c57634201c7bcd44bdf37e8a9d38b578fd53f42ea60c2f69e33cc391.

The hash is provenance. The rank proof is the next pair of exact checks.

## 4. Five exact kernel directions

The checker constructs these four similarity directions, where
`h_a=det(R_a)`:

| Direction | Prototype variation | Nonroot translation variation | Nonroot rotation variation |
|---|---|---|---|
| Translation by u=(1,0) or (0,1) | u | u-R_a*u | 0 |
| Scaling | v_i | t_a | 0 |
| Rotation | A*v_i | A*t_a | 1-h_a |

The last formula follows from `R_a*A=h_a*A*R_a`, and therefore includes
reflected copies.

There is one more direction. Let w_0=0 and sum the prototype edge vectors
of length `sqrt(3)` as one traverses the boundary, omitting the length-one
vectors. Thus w_i is the preceding partial sum, and

    w = [(0,0),(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1),
         (1,-2),(2,-1),(2,-1),(2,-1),(1,1),(-1,2),(-1,2),(-1,2)].

Both the long-side vectors and the short-side vectors close separately.
Put `v_i(lambda)=v_i+lambda*w_i`. The unit sides stay fixed while every
long side is multiplied by `1+lambda`. This is exactly the published
family `Tile(1,sqrt(3)*(1+lambda))`, with angles unchanged.

There are exact translation derivatives s_a, with s_0=0, satisfying every
labelled endpoint equation

    R_a*w_i+s_a = R_b*w_j+s_b.                          (3)

The checker obtains them by traversing the connected copy-contact graph
and then checks (3) on every contact, so no consistency is presumed.
The fifth kernel vector is `dv_i=w_i, dt_a=s_a, omega_a=0`.

For all five vectors direct integer multiplication proves M*k=0. A
specified `5 x 5` coordinate minor of these five vectors has determinant
`1003 modulo 1009`, proving they are independent. Hence `rank_R(M)<=95`.

Conversely the specified `95 x 95` submatrix of M has determinant
`205 modulo 1009`. Its integer determinant is nonzero. Therefore

    rank_Q(M)=rank_R(M)=95,
    ker_R(M)=span(the five directions).

The certificate lists the row and column indices. The reader computes
both determinants by row elimination on these square minors, independently
of the optional row-space search that selected them. It checks that 1009
is prime. The large-Jacobian rank is not inferred from floating point.

## 5. From the rank to local rigidity

The affine family

    v_i(lambda)=v_i+lambda*w_i,
    R_a(lambda)=R_a,
    t_a(lambda)=t_a+lambda*s_a

satisfies every nonlinear endpoint equation exactly, by (3). Apply any
nearby orientation-preserving similarity `S(x)=P*x+u`, where P is a
positive scale times a rotation. Replace prototype vertices by
`P*v_i(lambda)+u` and copy poses by

    R'_a=P*R_a*P^(-1),
    t'_a=P*t_a(lambda)+u-R'_a*u.

They remain Euclidean isometries of the same handedness; the root pose
remains the identity. This supplies an explicit smooth five-parameter
family of exact solutions. Its derivative has the five independent
kernel directions just checked.

Select the 95 scalar equations used in the nonsingular Jacobian minor.
The implicit function theorem makes their zero set a smooth
five-dimensional manifold near the reference point. The explicit family
is contained in that manifold and its derivative is an isomorphism
between five-dimensional tangent spaces. The inverse function theorem
therefore makes its image a neighbourhood in that zero set. Shrinking
the ambient neighbourhood, every solution of the selected equations
belongs to this family. Every solution of all 544 equations does also.
This proves the endpoint statement; it is stronger than an infinitesimal
rank statement alone.

Under these endpoint motions the labelled common chords, their parameter
orders and opposite outward normals persist. Normal profiles therefore
still obey (1), with the same lifted graph. They all vanish. The complete
prototile is consequently an orientation-preserving similarity of a
polygon in the published hat continuum. The plane-tiling conclusion follows
from that prior theorem, not from this finite packing.

## Literature, novelty scope and reproducibility

- D. Smith, J. S. Myers, C. S. Kaplan and C. Goodman-Strauss,
  [*An aperiodic monotile*](https://arxiv.org/html/2303.10798v3),
  Combinatorial Theory 4(1), 2024, gives the hat tiling, its substitution,
  and the length-changing continuum (Section 6, Theorem 6.1).
  The tilability of that continuum is established prior art.
- The fixture originates in Kaplan's
  [hatviz primary implementation](https://github.com/isohedral/hatviz).
  Source commit: `4bb9d01999e4e84accc2a78d0fa279ef20b47263`.
  An exact axial implementation extracted the fixture. As a provenance
  control, its 25 raw poses were compared with that committed JavaScript
  implementation, giving maximum Cartesian discrepancy below `4e-15`.
  This floating-point comparison plays no role in the theorem or reader.
  The upstream BSD license is retained in `SOURCE-LICENSE.txt`.
- The campaign's earlier
  [fixed-patch function-valued method](../../../heesch_weighted_matching_obstruction/mixed_hand_profiles.md)
  and [endpoint method](../../../heesch_weighted_matching_obstruction/endpoint_rigidity.md)
  concern the Mann five-corona fixture. The lifted-profile method and the
  modular-minor/implicit-function mechanism are reused. The result here
  is a separate exact certificate for the 25-hat network, including its
  non-similarity length parameter; no novelty is claimed for the methods,
  the hat, its tilings, or the existing hat continuum.

Reproduce with CPython 3.11.2 and its standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B round-two/six-heesch-3/hat_patch_rigidity/check.py --expected
```

It reads only `input.json` and `certificate.json`, checking exact packing,
complete shared-port relations, the four lifted odd walks, the five exact
kernel vectors and the two determinant minors. Eight malformed controls
are rejected. Typical runtime is below one second with one CPU and
small memory. No solver, search corpus, compiled code, or downloaded
dependency is needed. The implicit/inverse function arguments and the
translation from coincident normal graphs to (1) are written proofs,
not proof-assistant formalizations or independent reviewer verdicts.

For this particular network the successful endpoint deformations remain
inside an already tiling family, so they cannot give a finite Heesch
record. A productive extension must change the contact requirements or
investigate a different deep patch; those possibilities are not excluded.
